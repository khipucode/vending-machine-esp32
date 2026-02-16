# Conexões do Sistema Vending Machine (ESP32)

Este documento detalha a pinagem completa para a montagem do circuito utilizando um ESP32, Multiplexador CD74HC4067 (16 canais), sensores e atuadores.

---

## 1. Multiplexador (CD74HC4067)
Responsável por controlar até 16 servomotores usando apenas 5 pinos do ESP32.

| GPIO ESP32 | Pino CD74HC4067 | Função | Descrição |
| :--- | :--- | :--- | :--- |
| **GPIO 19** | **S0** | Endereço A (Bit 0) | Controle binário de seleção de canal. |
| **GPIO 18** | **S1** | Endereço B (Bit 1) | Controle binário de seleção de canal. |
| **GPIO 5** |  **S2** | Endereço C (Bit 2) | Controle binário de seleção de canal. |
| **GPIO 23** | **S3** | Endereço D (Bit 3) | Controle binário de seleção de canal (Novo pino). |
| **GPIO 4** | **SIG** (ou COM) | Sinal (Signal) | Entrada do PWM gerado pelo ESP32 para ser distribuído. |
| **GND** | **EN** (Enable) | Ativação | **Obrigatório** conectar ao GND para o chip funcionar. |
| **3V3** | **VCC** | Alimentação Lógica | Alimenta o chip multiplexador (Nível lógico 3.3V). |
| **GND** | **GND** | Terra | Referência comum. |

---

## 2. Servomotores (Saída do Multiplexador)
Os servos **não** se conectam ao ESP32, mas sim às saídas do Multiplexador e à Fonte Externa.

| Pino CD74HC4067 | Fio do Servo | Função | Descrição |
| :--- | :--- | :--- | :--- |
| **C0** até **C15** | **Laranja/Amarelo** | Sinal PWM | Conecte o fio de sinal de cada servo em um canal (C0=Prod 1, etc). |
| **N/A** | **Vermelho** | VCC Servo | Ligar direto no **+5V da Fonte Externa**. |
| **N/A** | **Marrom/Preto** | GND Servo | Ligar direto no **GND da Fonte Externa**. |

---

## 3. Display OLED (I2C)
Interface visual para o usuário.

| GPIO ESP32 | Pino OLED | Função | Descrição |
| :--- | :--- | :--- | :--- |
| **GPIO 21** | **SDA** | Dados (Data) | Comunicação I2C. |
| **GPIO 22** | **SCL** | Clock | Comunicação I2C. |
| **3V3** | **VCC** | Alimentação | Alimentação do módulo display. |
| **GND** | **GND** | Terra | Referência comum. |

---

## 4. Teclado Matricial (4x4)
Entrada de dados do usuário.

| GPIO ESP32 | Pino Teclado | Função | Descrição |
| :--- | :--- | :--- | :--- |
| **GPIO 32** | Pino 1 | Linha 1 | Varredura de teclas. |
| **GPIO 33** | Pino 2 | Linha 2 | Varredura de teclas. |
| **GPIO 25** | Pino 3 | Linha 3 | Varredura de teclas. |
| **GPIO 26** | Pino 4 | Linha 4 | Varredura de teclas. |
| **GPIO 27** | Pino 5 | Coluna 1 | Leitura de teclas. |
| **GPIO 14** | Pino 6 | Coluna 2 | Leitura de teclas. |
| **GPIO 12** | Pino 7 | Coluna 3 | Leitura de teclas. |
| **GPIO 13** | Pino 8 | Coluna 4 | Leitura de teclas. |

---

## 5. Sensores e Atuadores Extras
Monitoramento ambiental e feedback.

### Sensor DHT22 (Temperatura e Umidade)
| GPIO ESP32 | Pino DHT22 | Função | Descrição |
| :--- | :--- | :--- | :--- |
| **3V3** | Pino 1 (VCC) | Alimentação | Ligar também um lado do **Resistor 10kΩ**. |
| **GPIO 15**| Pino 2 (DATA)| Dados | Ligar também o outro lado do **Resistor 10kΩ** (Pull-up). |
| **N/C** | Pino 3 | - | Não conectado. |
| **GND** | Pino 4 (GND) | Terra | Referência comum. |

### Sensor PIR (Movimento)
| GPIO ESP32 | Pino PIR | Função | Descrição |
| :--- | :--- | :--- | :--- |
| **5V (Ext)**| VCC | Alimentação | A maioria dos módulos HC-SR501 prefere 5V. |
| **GPIO 34**| OUT | Sinal Digital | Pino "Input Only" do ESP32, ideal para leitura de sensores. |
| **GND** | GND | Terra | Referência comum. |

### Buzzer (Ativo)
| GPIO ESP32 | Pino Buzzer | Função | Descrição |
| :--- | :--- | :--- | :--- |
| **GPIO 2** | Positivo (+) | Sinal | Aciona o som (HIGH = Apita, LOW = Mudo). |
| **GND** | Negativo (-) | Terra | Referência comum. |

---

## 6. Distribuição de Energia (Crítico)

| Fonte | Destino | Descrição |
| :--- | :--- | :--- |
| **Fonte Externa 5V (+)** | **Servos (VCC)** | Alimenta a força dos motores. |
| **Fonte Externa 5V (+)** | **PIR (VCC)** | Alimenta o sensor de presença. |
| **Fonte Externa GND (-)** | **Servos, PIR, Mux** | Terra dos periféricos. |
| **Fonte Externa GND (-)** | **ESP32 (GND)** | **GND COMUM:** Obrigatório unir GND da fonte e do ESP32. |
| **USB / Pin Vin** | **ESP32** | Alimentação do processador. |
