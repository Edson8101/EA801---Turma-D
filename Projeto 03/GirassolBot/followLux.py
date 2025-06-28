from machine import I2C, Pin, PWM, SoftI2C
import time
import ssd1306

# --- Configuração do I2C para BH1750 ---
i2c = I2C(1, scl=Pin(3), sda=Pin(2))

addr_left = 0x23  # BH1750 com ADO=GND
addr_right = 0x5C  # BH1750 com ADO=VCC

def read_lux(i2c, addr):
    try:
        i2c.writeto(addr, b'\x10')  # modo de medição contínua
        time.sleep(0.18)  # tempo para medição (180ms)
        data = i2c.readfrom(addr, 2)
        lux = ((data[0] << 8) | data[1]) / 1.2
        return lux
    except Exception as e:
        print(f"Erro no sensor {hex(addr)}:", e)
        return -1

# --- Configuração do I2C para a tela OLED (128x64) ---
oled_i2c = SoftI2C(scl=Pin(15), sda=Pin(14))  # Ajuste os pinos conforme necessário
oled = ssd1306.SSD1306_I2C(128, 64, oled_i2c)
oled.fill(0)

# --- Configuração dos pinos do driver HW-166 ---
# Motor A
ain1 = Pin(4, Pin.OUT)
ain2 = Pin(9, Pin.OUT)
pwma = PWM(Pin(10))
pwma.freq(1000)

# Motor B
bin1 = Pin(19, Pin.OUT)
bin2 = Pin(18, Pin.OUT)
pwmb = PWM(Pin(16))
pwmb.freq(1000)

# Standby driver
stby = Pin(20, Pin.OUT)

# Botões
botao_a = Pin(5, Pin.IN, Pin.PULL_UP)  # Botão A para ligar/desligar
botao_b = Pin(6, Pin.IN, Pin.PULL_UP)  # Botão B para inverter os motores

# Estado do robô (inicialmente ligado)
robo_ligado = True
invertido = False  # Estado para inversão dos motores

# Funções auxiliares para controle do motor

def motor_a_forward(speed):
    ain1.value(1)
    ain2.value(0)
    pwma.duty_u16(speed)

def motor_a_backward(speed):
    ain1.value(0)
    ain2.value(1)
    pwma.duty_u16(speed)

def motor_a_stop():
    pwma.duty_u16(0)
    ain1.value(0)
    ain2.value(0)

def motor_b_forward(speed):
    bin1.value(1)
    bin2.value(0)
    pwmb.duty_u16(speed)

def motor_b_backward(speed):
    bin1.value(0)
    bin2.value(1)
    pwmb.duty_u16(speed)

def motor_b_stop():
    pwmb.duty_u16(0)
    bin1.value(0)
    bin2.value(0)

# Função para alternar o estado do robô
def alternar_robo():
    global robo_ligado
    robo_ligado = not robo_ligado
    
    limpar_linhas(0, 1)
    
    if robo_ligado:
        stby.value(1)  # Liga o robô
        print("Robô ligado")
        exibir_mensagem("ROBO LIGADO", 0, limpar_linha=False)  # Linha 0
        exibir_mensagem("Pronto p/ operar", 1, limpar_linha=False)  # Linha 1
    else:
        motor_a_stop()  # Para os motores
        motor_b_stop()
        stby.value(0)  # Desliga o robô
        print("Robô desligado")
        exibir_mensagem("ROBO DESLIGADO", 0, limpar_linha=False)  # Linha 0
        exibir_mensagem("Aguardando...", 1, limpar_linha=False)  # Linha 1

# Função para inverter a direção dos motores
def inverter_motores():
    global invertido
    invertido = not invertido
    print("Inversão de direção dos motores!")

# Função para exibir mensagens na tela OLED
def exibir_mensagem(mensagem, linha=0, limpar_linha=True):
    if limpar_linha:
        oled.fill_rect(0, linha*10, 128, 10, 0)  # Limpa apenas a linha
    oled.text(mensagem, 0, linha*10)
    oled.show()

# Função para limpar múltiplas linhas
def limpar_linhas(*linhas):
    for linha in linhas:
        oled.fill_rect(0, linha*10, 128, 10, 0)
    oled.show()
    
# --- Parâmetros do robô ---
VEL_MAX = 30000  # velocidade máxima PWM (0 a 65535)

THRESHOLD_DIFF = 15.0  # Lux, diferença mínima para virar
THRESHOLD_LOW = 10.0   # Lux, luz baixa (ambiente escuro)

# --- Loop principal ---
while True:
    # Verifica se o botão A foi pressionado (ligar/desligar)
    if botao_a.value() == 0:  # Botão A pressionado
        alternar_robo()
        #exibir_mensagem("Ligando/Desl Robô")  # Exibe mensagem de ação
        time.sleep(1)  # Debounce para evitar múltiplos acionamentos

    # Verifica se o botão B foi pressionado (inverter motores)
    if botao_b.value() == 0:  # Botão B pressionado
        inverter_motores()
        exibir_mensagem("Invertendo Motores")  # Exibe mensagem de inversão
        time.sleep(1)  # Debounce para evitar múltiplos acionamentos

    # Se o robô estiver ligado, continua o funcionamento normal
    if robo_ligado:
        lux_left = read_lux(i2c, addr_left)
        lux_right = read_lux(i2c, addr_right)
        print(f"Luz esquerda: {lux_left:.1f} Lux | direita: {lux_right:.1f} Lux")

        # Se ambos baixos → sem luz ou ambiente escuro
        if lux_left < THRESHOLD_LOW and lux_right < THRESHOLD_LOW:
            # Parar ou girar para buscar luz
            motor_a_stop()
            motor_b_stop()
            exibir_mensagem("Ambiente Escuro!")  # Mensagem de ambiente escuro
            print("Ambiente escuro, parando.")
            time.sleep(0.5)
            continue

        diff = lux_left - lux_right

        if abs(diff) < THRESHOLD_DIFF:
            # Luz equilibrada, seguir em frente
            if invertido:
                motor_a_backward(VEL_MAX)
                motor_b_backward(VEL_MAX)
            else:
                motor_a_forward(VEL_MAX)
                motor_b_forward(VEL_MAX)
            exibir_mensagem("Seguindo em Frente...")  # Mensagem de movimento para frente
            print("Seguindo em frente.")
        elif diff > 0:
            # Luz mais forte na esquerda → virar esquerda
            if invertido:
                motor_a_stop()
                motor_b_backward(VEL_MAX)
            else:
                motor_a_stop()
                motor_b_forward(VEL_MAX)
            exibir_mensagem("Virando para Esquerda")  # Mensagem de virada à esquerda
            print("Virando para esquerda.")
        else:
            # Luz mais forte na direita → virar direita
            if invertido:
                motor_a_forward(VEL_MAX)
                motor_b_stop()
            else:
                motor_a_forward(VEL_MAX)
                motor_b_stop()
            exibir_mensagem("Virando para Direita")  # Mensagem de virada à direita
            print("Virando para direita.")

    time.sleep(0.1)
