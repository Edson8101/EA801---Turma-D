from machine import I2C, Pin, PWM, SoftI2C
import time
import ssd1306

# --- Configuração do I2C para BH1750 ---
i2c = I2C(1, scl=Pin(3), sda=Pin(2))
BH1750_ADDR = 0x23  # Somente 1 sensor em uso

def read_lux(i2c, addr):
    try:
        i2c.writeto(addr, b'\x10')  # Medição contínua
        time.sleep(0.18)
        data = i2c.readfrom(addr, 2)
        lux = ((data[0] << 8) | data[1]) / 1.2
        return lux
    except:
        return -1

# --- OLED ---
oled_i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = ssd1306.SSD1306_I2C(128, 64, oled_i2c)
oled.fill(0)

# --- Motores ---
ain1 = Pin(4, Pin.OUT)
ain2 = Pin(9, Pin.OUT)
pwma = PWM(Pin(10))
pwma.freq(1000)

bin1 = Pin(19, Pin.OUT)
bin2 = Pin(18, Pin.OUT)
pwmb = PWM(Pin(16))
pwmb.freq(1000)

stby = Pin(20, Pin.OUT)

# --- Botões ---
botao_a = Pin(5, Pin.IN, Pin.PULL_UP)
botao_b = Pin(6, Pin.IN, Pin.PULL_UP)

# --- Estado do robô ---
modos = ["Desligado", "Seguir 100+", "Seguir 200+", "Seguir 500+"]
modo_index = 0  # começa desligado
invertido = False
thresholds = [None, 100, 200, 500]

VEL_MAX = 30000

# --- Funções de motor ---
def motor_a_forward(speed): ain1.value(1); ain2.value(0); pwma.duty_u16(speed)
def motor_a_backward(speed): ain1.value(0); ain2.value(1); pwma.duty_u16(speed)
def motor_a_stop(): pwma.duty_u16(0); ain1.value(0); ain2.value(0)

def motor_b_forward(speed): bin1.value(1); bin2.value(0); pwmb.duty_u16(speed)
def motor_b_backward(speed): bin1.value(0); bin2.value(1); pwmb.duty_u16(speed)
def motor_b_stop(): pwmb.duty_u16(0); bin1.value(0); bin2.value(0)

def motores_parar():
    motor_a_stop()
    motor_b_stop()

# --- Tela OLED ---
def exibir_mensagem(msg, linha=0):
    oled.fill_rect(0, linha * 10, 128, 10, 0)
    oled.text(msg, 0, linha * 10)
    oled.show()

def atualizar_estado_oled():
    oled.fill(0)
    exibir_mensagem("Modo:", 0)
    exibir_mensagem(modos[modo_index], 1)

# --- Giro 360° ---
def giro_360_encontrar_luz():
    print("Iniciando varredura 360°")
    maior_lux = -1
    melhor_direcao = None

    for i in range(4):  # 4 etapas de 90 graus
        motor_a_forward(VEL_MAX)
        motor_b_backward(VEL_MAX)
        time.sleep(0.6)  # Pequeno giro

        lux = read_lux(i2c, BH1750_ADDR)
        print(f"Leitura {i+1}: {lux:.1f} Lux")

        if lux > maior_lux:
            maior_lux = lux
            melhor_direcao = i

        motores_parar()
        time.sleep(0.2)

    print(f"Maior luz encontrada: {maior_lux:.1f} Lux em direção {melhor_direcao}")
    return maior_lux

# --- Alternar modo com botão A ---
def alternar_modo():
    global modo_index
    modo_index = (modo_index + 1) % len(modos)
    atualizar_estado_oled()
    if modo_index == 0:
        stby.value(0)
        motores_parar()
        print("Robô desligado.")
    else:
        stby.value(1)
        print(f"Modo ativo: {modos[modo_index]}")

# --- Inverter motores com botão B ---
def inverter_motores():
    global invertido
    invertido = not invertido
    print("Inversão de direção!")

# --- Inicialização ---
atualizar_estado_oled()
ultimo_estado_a = botao_a.value()
ultimo_estado_b = botao_b.value()

# --- Loop principal ---
while True:
    estado_a = botao_a.value()
    estado_b = botao_b.value()

    if estado_a == 0 and ultimo_estado_a == 1:
        alternar_modo()
        time.sleep(0.3)
    ultimo_estado_a = estado_a

    if estado_b == 0 and ultimo_estado_b == 1:
        inverter_motores()
        exibir_mensagem("Invertendo", 2)
        time.sleep(0.3)
    ultimo_estado_b = estado_b

    if modo_index > 0:
        limiar = thresholds[modo_index]
        lux = read_lux(i2c, BH1750_ADDR)
        exibir_mensagem(f"Luz: {lux:.1f} Lux", 3)

        if lux >= limiar:
            # andar para frente
            if invertido:
                motor_a_backward(VEL_MAX)
                motor_b_backward(VEL_MAX)
            else:
                motor_a_forward(VEL_MAX)
                motor_b_forward(VEL_MAX)
            exibir_mensagem("Seguindo Luz", 2)
        else:
            motores_parar()
            exibir_mensagem("Procurando Luz", 2)
            maior = giro_360_encontrar_luz()
            exibir_mensagem(f"Max: {maior:.1f}", 2)
    else:
        motores_parar()

    time.sleep(0.1)
