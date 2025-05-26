import core1_interface as iface
from machine import Pin,PWM
from motor import Servo
from teclado import ler_teclado
import time
from MPU6050 import MPU6050

# Inicia o core 1 para a interface
iface.iniciar_interface()
time.sleep(0.1)  # espera o core1 iniciar e entrar no loop

# Define o pino para o buzzer
buzzer = PWM(Pin(21))
# porta = Pin(28, Pin.IN)  # Botão de abrir/fechar cofre
porta = Pin(9, Pin.IN, Pin.PULL_DOWN)
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

#Inicializa o Servo motor
servo = Servo()
servo.attach(28)  # Pino do servo motor
servo.write(0) # Inicializa o servo motor em 90º (fechado)

#Inicializa o acelerômetro
mpu = MPU6050()

while True:
    accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]

    print("x: " + str(aX) + " y: " + str(aY) + " z: " + str(aZ))
    time.sleep(1)
        