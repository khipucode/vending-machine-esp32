import tkinter as tk
import paho.mqtt.client as mqtt

# Novas Configurações ThingSpeak
MQTT_SERVER = "mqtt3.thingspeak.com"
CLIENT_ID = "HDInDg8bLCACOA01EwcCKBQ"
USER = "HDInDg8bLCACOA01EwcCKBQ"
PASS = "lsdf/MEfQ0QX+/ZEMc5RrWeQ"
CHANNEL_ID = "3267232"
TOPIC = f"channels/{CHANNEL_ID}/subscribe/fields/field1"

class VendingDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Vending Machine MQTT - ThingSpeak")
        self.root.geometry("900x980")
        self.root.configure(bg="#1a1a1a")

        self.produtos_img = {} 
        self.referencias_canvas = {}

        # Grid 4x4
        frame_grid = tk.Frame(root, bg="#1a1a1a")
        frame_grid.pack(pady=20)

        for i in range(16):
            # Mudança: O número do produto (para lógica) é de 1 a 16.
            num_produto = i + 1 
            # Se suas imagens ainda são 101, 102..., usamos essa variável para o arquivo
            nome_arquivo = 100 + num_produto 
            
            linha = i // 4
            coluna = i % 4
            
            canvas = tk.Canvas(frame_grid, width=200, height=200, 
                              bg="#2d2d2d", highlightthickness=1, highlightbackground="#444")
            canvas.grid(row=linha, column=coluna, padx=5, pady=5)
            
            try:
                img = tk.PhotoImage(file=f"img/{nome_arquivo}.png")
                self.produtos_img[num_produto] = img 
                id_obj = canvas.create_image(100, 100, image=img)
                self.referencias_canvas[num_produto] = (canvas, id_obj)
            except:
                id_obj = canvas.create_text(100, 100, text=f"PRODUTO\n{num_produto}", fill="gray", justify="center")
                self.referencias_canvas[num_produto] = (canvas, id_obj)

        # Tela LED
        self.led_display = tk.Label(root, text="AGUARDANDO PEDIDO...", 
                                   font=("Fixedsys", 24, "bold"), 
                                   bg="black", fg="#00FF00", width=40, height=2)
        self.led_display.pack(side="bottom", pady=30)

        # Configuração MQTT
        self.setup_mqtt()

    def setup_mqtt(self):
        # Tratamento para suportar tanto paho-mqtt v1 quanto v2
        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=CLIENT_ID)
        except AttributeError:
            self.client = mqtt.Client(client_id=CLIENT_ID)

        self.client.username_pw_set(USER, PASS)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        try:
            self.client.connect(MQTT_SERVER, 1883, 60)
            self.client.loop_start() # Roda em thread separada
        except Exception as e:
            self.led_display.config(text="ERRO DE CONEXÃO", fg="red")
            print("Erro:", e)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Conectado ao ThingSpeak com código {rc}")
        client.subscribe(TOPIC)

    def on_message(self, client, userdata, msg):
        try:
            valor_recebido = msg.payload.decode()
            print(f"MQTT Recebido: {valor_recebido}")
            num_prod = int(valor_recebido)
            
            # Atualiza interface na thread principal
            self.root.after(0, lambda: self.processar_venda(num_prod))
        except ValueError:
            print("Mensagem recebida não é um número válido")

    def processar_venda(self, num):
        if num in self.referencias_canvas:
            self.led_display.config(text=f"PRODUTO {num} LIBERADO!", fg="yellow")
            self.vibrar(num, 15) # Inicia a vibração (15 repetições)
        else:
            self.led_display.config(text=f"CÓDIGO {num} INVÁLIDO", fg="red")

    def vibrar(self, num, vezes):
        canvas, obj_id = self.referencias_canvas[num]
        
        if vezes > 0:
            # Em vez de mover (que causa drift), redefinimos a coordenada exata
            offset_x = 7 if vezes % 2 == 0 else -7
            canvas.coords(obj_id, 100 + offset_x, 100)
            self.root.after(40, lambda: self.vibrar(num, vezes - 1))
        else:
            # Terminou de vibrar: volta pro centro exato (100, 100)
            canvas.coords(obj_id, 100, 100)
            # Oculta para dar o efeito que "caiu" da máquina
            canvas.itemconfig(obj_id, state='hidden')
            # Repõe o produto após 2 segundos
            self.root.after(2000, lambda: self.repor(num))

    def repor(self, num):
        canvas, obj_id = self.referencias_canvas[num]
        canvas.itemconfig(obj_id, state='normal')
        self.led_display.config(text="AGUARDANDO PEDIDO...", fg="#00FF00")

if __name__ == "__main__":
    root = tk.Tk()
    app = VendingDashboard(root)
    root.mainloop()
