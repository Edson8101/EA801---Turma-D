```from machine import I2C, Pin, PWM
import time

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

# --- Configuração dos pinos do driver HW-166 ---

# Motor A
ain1 = Pin(17, Pin.OUT)
ain2 = Pin(18, Pin.OUT)
pwma = PWM(Pin(16))
pwma.freq(1000)

# Motor B
bin1 = Pin(20, Pin.OUT)
bin2 = Pin(8, Pin.OUT)
pwmb = PWM(Pin(19))
pwmb.freq(1000)

# Standby driver
stby = Pin(10, Pin.OUT)

# Ativa o driver
stby.value(1)

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

# --- Parâmetros do robô ---
VEL_MAX = 50000  # velocidade máxima PWM (0 a 65535)

THRESHOLD_DIFF = 15.0  # Lux, diferença mínima para virar
THRESHOLD_LOW = 10.0   # Lux, luz baixa (ambiente escuro)

# --- Loop principal ---

while True:
    lux_left = read_lux(i2c, addr_left)
    lux_right = read_lux(i2c, addr_right)
    print(f"Luz esquerda: {lux_left:.1f} Lux | direita: {lux_right:.1f} Lux")

    # Se ambos baixos → sem luz ou ambiente escuro
    if lux_left < THRESHOLD_LOW and lux_right < THRESHOLD_LOW:
        # Parar ou girar para buscar luz
        motor_a_stop()
        motor_b_stop()
        print("Ambiente escuro, parando.")
        time.sleep(0.5)
        continue

    diff = lux_left - lux_right

    if abs(diff) < THRESHOLD_DIFF:
        # Luz equilibrada, seguir em frente
        motor_a_forward(VEL_MAX)
        motor_b_forward(VEL_MAX)
        print("Seguindo em frente.")
    elif diff > 0:
        # Luz mais forte na esquerda → virar esquerda
        motor_a_stop()
        motor_b_forward(VEL_MAX)
        print("Virando para esquerda.")
    else:
        # Luz mais forte na direita → virar direita
        motor_a_forward(VEL_MAX)
        motor_b_stop()
        print("Virando para direita.")

    time.sleep(0.1)
``` 
