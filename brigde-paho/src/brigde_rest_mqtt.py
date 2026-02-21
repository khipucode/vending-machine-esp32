import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion  # <-- Importação que estava faltando!
import json
import requests
import time
import ssl
import unicodedata
import re
import threading

# ==========================================
# 1. CONFIGURAÇÕES
# ==========================================

# HiveMQ (Origem)
HIVEMQ_BROKER = "68bab72200f34603a77607d137ae118c.s1.eu.hivemq.cloud"
HIVEMQ_PORT = 8883
HIVEMQ_USER = "vendingmqtt"
HIVEMQ_PASS = "123456IoT"
TOPIC_SUB = "vending/machine/#"  # <-- Curinga para pegar /status e /vendas

# Ubidots (Destino MQTT)
UBIDOTS_BROKER = "industrial.api.ubidots.com"
UBIDOTS_PORT = 1883
UBIDOTS_TOKEN = "BBUS-2ZiGS45Bv0mDa3XzHxIJLkQkUNV3Oo"
DEVICE_LABEL = "vending-machine"

# ThingSpeak (Destino REST)
TS_API_URL = "https://api.thingspeak.com/update"
TS_WRITE_API_KEY = "M7Q4FAV1YSYGCRN8" 

# Variáveis Globais de Controle
receita_total = 0.0
last_ts_send_time = 0.0
ts_lock = threading.Lock()

# ==========================================
# 2. BASE DE DADOS DE PRODUTOS
# ==========================================
PRODUTOS = {
    1: {"nome": "Batata Chips Clássica", "preco": 5.00},
    2: {"nome": "Doritos Queijo", "preco": 6.50},
    3: {"nome": "Chocolate Barra", "preco": 4.50},
    4: {"nome": "Biscoito Recheado", "preco": 3.00},
    5: {"nome": "Amendoim Salgado", "preco": 2.50},
    6: {"nome": "Goma de Mascar", "preco": 1.50},
    7: {"nome": "Refrigerante Lata", "preco": 5.00},
    8: {"nome": "Suco de Caixinha", "preco": 4.00},
    9: {"nome": "Água Mineral", "preco": 3.00},
    10: {"nome": "Barra de Cereal", "preco": 2.00},
    11: {"nome": "Pipoca Doce", "preco": 3.50},
    12: {"nome": "Bala de Gelatina", "preco": 4.00},
    13: {"nome": "Cookies", "preco": 5.50},
    14: {"nome": "Snack de Queijo", "preco": 4.50},
    15: {"nome": "Torrada Integral", "preco": 3.00},
    16: {"nome": "Bombom", "preco": 1.00}
}

# ==========================================
# 3. FUNÇÕES UTILITÁRIAS
# ==========================================
def to_snake_case(texto):
    """Remove acentos, converte para minúsculas e substitui espaços por underscores."""
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9]+', '_', texto)
    return texto.strip('_')

# ==========================================
# 4. FUNÇÕES DE ENVIO
# ==========================================
def send_to_ubidots(payload):
    """Envia dados para o Ubidots usando um client MQTT temporário (Publish Single)."""
    topic = f"/v1.6/devices/{DEVICE_LABEL}"
    
    print(f"\n[Ubidots - ENVIANDO] Tópico: {topic}")
    print(f"[Ubidots - ENVIANDO] Payload:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")
    
    try:
        import paho.mqtt.publish as publish
        publish.single(
            topic=topic,
            payload=json.dumps(payload),
            hostname=UBIDOTS_BROKER,
            port=UBIDOTS_PORT,
            client_id="Ubi_Bridge_" + str(int(time.time())),
            auth={'username': UBIDOTS_TOKEN, 'password': ''}
        )
        print(f"[Ubidots - SUCESSO] Dados entregues ao broker.")
    except Exception as e:
        print(f"[Ubidots - ERRO] Falha ao enviar dados: {e}")

def send_to_thingspeak_task(payload):
    """Função executada em thread separada para respeitar o limite do ThingSpeak sem travar o MQTT."""
    global last_ts_send_time
    
    with ts_lock:
        current_time = time.time()
        elapsed = current_time - last_ts_send_time
        
        # Garante o delay obrigatório de 15 segundos
        if elapsed < 15.0:
            sleep_time = 15.0 - elapsed
            print(f"\n[ThingSpeak - AGUARDANDO] Pausa de {sleep_time:.1f}s exigida pela API gratuita...")
            time.sleep(sleep_time)
            
        print(f"\n[ThingSpeak - ENVIANDO] Endpoint REST: {TS_API_URL}")
        print(f"[ThingSpeak - ENVIANDO] Payload:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")
            
        try:
            response = requests.post(TS_API_URL, data=payload, timeout=10)
            if response.status_code == 200 and response.text != '0':
                print(f"[ThingSpeak - SUCESSO] Entrada registrada (Entry ID: {response.text}).")
            else:
                print(f"[ThingSpeak - ERRO] Falha na API. Código: {response.status_code}, Resposta: {response.text}")
        except Exception as e:
            print(f"[ThingSpeak - ERRO] Falha na requisição HTTP: {e}")
        finally:
            last_ts_send_time = time.time()

# ==========================================
# 5. LÓGICA DE PROCESSAMENTO E CALLBACKS
# ==========================================
def process_vending_data(data):
    """Interpreta as mensagens recebidas e orquestra os envios."""
    global receita_total
    
    prod_id = data.get("id", 0)
    estoque = data.get("estoque_atual", 0)
    temp = data.get("temp", 0)
    hum = data.get("hum", 0)
    pir = data.get("pir", 0)

    # 1. Preparar Payload Ubidots (Base Ambiental/Status)
    ubi_payload = {
        "temperatura": temp,
        "humidade": hum,
        "presenca_pir": pir,
        "status": 1
    }

    # 2. Preparar Payload ThingSpeak (Base)
    ts_payload = {
        "api_key": TS_WRITE_API_KEY,
        "field3": temp,
        "field4": hum,
        "field5": pir,
        "field9": receita_total # Mantém o último valor acumulado
    }

    # Se houve venda comercial (id != 0 e ID válido)
    if prod_id > 0 and prod_id in PRODUTOS:
        produto = PRODUTOS[prod_id]
        nome = produto["nome"]
        preco = produto["preco"]
        nome_snake = to_snake_case(nome)
        
        # Atualiza métricas comerciais globais
        receita_total += preco
        
        # Adiciona dados da venda ao payload do Ubidots
        ubi_payload[f"estoque_{nome_snake}"] = estoque
        ubi_payload["venda"] = {"value": 1, "context": {"nome_produto": nome, "preco": preco}}
        ubi_payload["receita_total"] = receita_total
        
        # Adiciona dados da venda ao payload do ThingSpeak
        ts_payload["field6"] = prod_id
        ts_payload["field7"] = preco
        ts_payload["field8"] = estoque
        ts_payload["field9"] = receita_total
        
        print(f"[EVENTO INTERNO] Venda processada: {nome} (R$ {preco:.2f}) | Estoque: {estoque}")
    else:
        print("[EVENTO INTERNO] Nenhuma venda detectada (id=0). Atualizando apenas sensores.")

    # Disparar envios
    send_to_ubidots(ubi_payload)
    threading.Thread(target=send_to_thingspeak_task, args=(ts_payload,), daemon=True).start()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[HiveMQ] Conectado com sucesso! Inscrevendo-se nos tópicos: {TOPIC_SUB}")
        client.subscribe(TOPIC_SUB)
    else:
        print(f"[HiveMQ] Falha na conexão. Código de retorno: {rc}")

def on_message(client, userdata, msg):
    try:
        payload_str = msg.payload.decode('utf-8')
        
        print(f"\n{'='*60}")
        print(f"[HiveMQ - RECEBIDO] Tópico: {msg.topic}")
        try:
            pretty_json = json.dumps(json.loads(payload_str), indent=2)
            print(f"[HiveMQ - RECEBIDO] Dados:\n{pretty_json}")
        except json.JSONDecodeError:
            print(f"[HiveMQ - RECEBIDO] Dados brutos (não-JSON): {payload_str}")
        print(f"{'='*60}")
        
        data = json.loads(payload_str)
        process_vending_data(data)
        
    except json.JSONDecodeError:
        print(f"[Erro] A mensagem recebida não é um formato JSON válido.")
    except Exception as e:
        print(f"[Erro] Falha ao processar a mensagem no on_message: {e}")

# ==========================================
# 6. INICIALIZAÇÃO DO LOOP PRINCIPAL
# ==========================================
def main():
    print("Iniciando MQTT Bridge: HiveMQ -> Ubidots / ThingSpeak...")
    
    # Cliente iniciado SEM um client_id forçado, gerando um aleatório automaticamente
    client = mqtt.Client(CallbackAPIVersion.VERSION1)
    
    client.username_pw_set(HIVEMQ_USER, HIVEMQ_PASS)
    client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
    
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(HIVEMQ_BROKER, HIVEMQ_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[Sistema] Desconectando e encerrando a ponte MQTT...")
        client.disconnect()
    except Exception as e:
        print(f"\n[Erro Crítico] Falha na inicialização MQTT: {e}")

if __name__ == "__main__":
    main()
