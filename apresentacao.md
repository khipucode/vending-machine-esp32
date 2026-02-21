# Apresentação — Ativação do Sistema Vending Machine

Este documento descreve os **passos necessários para iniciar e verificar o funcionamento completo do sistema Vending Machine**, incluindo simulador local, integração MQTT e monitoramento em plataformas IoT.

---

## ✅ 1. Executar o sistema localmente

### 1.1 Entrar na pasta do projeto

Abra o terminal e acesse o diretório principal:

```bash
cd /home/leaonid/Documentos/CPQD_FIAP_PROJECTS/VENDING-MACHINE
```

---

### 1.2 Executar o simulador da Vending Machine (Tkinter)

Entre na pasta:

```bash
cd ~/BOARD/
```

Execute o simulador:

```bash
python3 vmachine.py
```

👉 Isso abrirá o **simulador da Vending Machine** em interface gráfica (Tkinter).

---

### 1.3 Executar a ponte REST ↔ MQTT

Abra outro terminal e entre na pasta:

```bash
cd ~/PAHO-MQTT/
```

Execute o script:

```bash
python3 brigde_rest_mqtt.py
```

📌 Este script é responsável por:

* Receber dados do **HiveMQ**
* Publicar dados no **Ubidots**
* Publicar dados no **ThingSpeak**

---

## ✅ 2. Rodar a simulação no Wokwi

Acesse o projeto de simulação:

https://wokwi.com/projects/456531482103047169

▶️ Clique em **Run Simulation** para iniciar o sistema embarcado virtual.

---

## ✅ 3. Verificar o Broker MQTT (HiveMQ)

Acesse o HiveMQ apenas para confirmar que o broker está ativo e funcionando.

✔ Verifique se há conexão ativa e mensagens sendo transmitidas.

---

## ✅ 4. Monitorar tópicos MQTT no MQTT Explorer

Abra o **MQTT Explorer** e observe:

* Tópicos do **HiveMQ**
* Tópicos enviados ao **ThingSpeak**

👉 Confirmar se mensagens estão sendo publicadas corretamente.

---

## ✅ 5. Verificar dados no ThingSpeak

Acesse o canal utilizado pelo projeto:

https://thingspeak.mathworks.com/channels/3267232

✔ Conferir atualização dos dados em tempo real.

---

## ✅ 6. Verificar dashboard no Ubidots

Acesse o dashboard:

https://stem.ubidots.com/app/dashboards/6974714b56d9016892e7abd0

✔ Validar:

* Recebimento dos dados
* Atualização dos widgets
* Comunicação IoT funcionando

---

## 🎯 Fluxo geral do sistema

```
Wokwi Simulation
        ↓
     HiveMQ (MQTT Broker)
        ↓
brigde_rest_mqtt.py
        ↓
 ┌───────────────┬───────────────┐
 │   ThingSpeak  │    Ubidots    │
 └───────────────┴───────────────┘
```

---

## ✅ Sistema pronto

Se todos os passos acima funcionarem corretamente, o sistema estará:

* Simulando a Vending Machine
* Comunicando via MQTT
* Publicando dados em plataformas IoT
* Monitorável em tempo real

---
