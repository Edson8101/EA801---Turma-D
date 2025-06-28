from machine import Pin, PWM, ADC
import utime
import random
import neopixel
import time
import math
from time import sleep
from math import atan2, degrees



# Inicializa o display
chain = neopixel.NeoPixel(Pin(7), 25)

# Inicializa o joystick e botoes A e B
adc_x = ADC(Pin(27))
adc_y = ADC(Pin(26))
joystick_button = Pin(22, Pin.IN, Pin.PULL_UP)
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)


#definindo variaveis de posicao e de angulo
posx = 0
posy = 0
angulo_x = 0
angulo_y = 0
# Define os valores mínimos e máximos dos conversores AD
adc_min = 300
adc_max = 65535

# Tamanho da matriz de LEDs
matrix_size = 5

LED_MATRIX = [
    [24, 23, 22, 21, 20],
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]]

class Servo:
    
    # Construtor
    def __init__(self):
        self.FREQ = 50
        self.pulse_min = 2000 # 0º ~ 0.61 ms
        self.pulse_max = 7800 # 360º ~ 2.38 ms
        self.duty = self.convert(0)  # Começa em 90º
    
    # Configura o pino e inicia o PWM a 0º
    def attach(self, pino):
        self.pin = Pin(pino)
        self.pwm = PWM(self.pin)
        self.pwm.freq(self.FREQ)
        self.pwm.duty_u16(self.duty)
    
    # Converte o angulo em pulso
    def convert(self, angulo):
        if angulo <= 0:
            return self.pulse_min
        if angulo >= 180:
            return self.pulse_max
        
        pulso = self.pulse_min + int( (angulo / 180) * (self.pulse_max - self.pulse_min) )
        return pulso
    
    # Recebe o angulo e controla o servo
    def write(self, angulo):
        self.duty = self.convert(angulo)
        self.pwm.duty_u16(self.duty)




#definindo um offset para a escala de leitura de joystick
def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Define as dimensões da matriz de LEDs
matrix_width = 5
matrix_height = 5

# Define a cor atual do LED
current_color = (50, 0, 0)


# Define o estado atual do botão do joystick
joystick_button_pressed = False

def map_adc_to_position(adc_value, adc_min, adc_max, matrix_size):
    position = int((adc_value - adc_min) / (adc_max - adc_min + 1) * matrix_size)
    return min(max(position, 0), matrix_size - 1)


    
# Inicializar ADC para os pinos VRx (GPIO26)
adc_vrx = ADC(Pin(27))
adc_vry = ADC(Pin(26))

def acender_led_joystick(valor, posx, posy):
    brilho = map_value(valor, 0, 65535, 0, 255)  # Normalizar para 0-255
     
    x, y = posx, posy  # Escolher um LED fixo da matriz (ajuste conforme necessário)
    
    indice = LED_MATRIX[x][y]
    chain[indice] = current_color  # Define a cor do LED
    chain.write()  # Atualiza os LEDs

# Apagar todos os LEDs
def apagar_todos():
    for i in range(25):
        chain[i] = (0, 0, 0)
    chain.write()
    
    
# Instancia os dois servos
servox = Servo()
servoy = Servo()

# Anexa aos pinos GP15 e GP16
servox.attach(15)
servoy.attach(16)


while True:


        vrx_value = adc_vrx.read_u16()  # Lê joystick X
        vry_value = adc_vry.read_u16()  # Lê joystick Y

        acender_led_joystick(vrx_value, posx, posy)  # Atualiza LED com brilho proporcional
        utime.sleep(0.1)  # Pequeno delay para estabilidade
        
        if vrx_value < 500:
            
            if posy <= 3:
                utime.sleep(0.2)
                posy+=1
                apagar_todos()
                print (vrx_value)
                print ("posicao X:",posy)
                angulo_x = posy*180/4
                servox.write(angulo_x)
                servoy.write(angulo_y)
                print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                
            else :
               posy = 0
               utime.sleep(0.2)
               apagar_todos()
               print (vrx_value)
               print ("posicao X:",posy)
               angulo_x = posy*180/4
               servox.write(angulo_x)
               servoy.write(angulo_y)
               print("angulo x:", angulo_x, "| angulo y:", angulo_y)
               
               
        if vrx_value > 60000:
            if posy >= 1:
                utime.sleep(0.2)
                posy -= 1
                apagar_todos()
                print (vrx_value)
                print ("posicao X:",posy)
                angulo_x = posy*180/4
                servox.write(angulo_x)
                servoy.write(angulo_y)
                print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                
            else :
                posy = 4
                utime.sleep(0.2)
                apagar_todos()
                print (vrx_value)
                print ("posicao X:",posy)
                angulo_x = posy*180/4
                servox.write(angulo_x)
                servoy.write(angulo_y)
                print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                
        if vry_value < 500:
            if posx >=1:
                utime.sleep(0.2)
                posx -= 1
                apagar_todos()
                print (vry_value)
                print ("posicao Y:",posx)
                angulo_y = posx*90/4
                servox.write(angulo_x)
                servoy.write(angulo_y)
                print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                
            else:
                posx=4
                utime.sleep(0.2)
                apagar_todos()
                print (vry_value)
                print ("posicao Y:",posx)
                angulo_y = posx*90/4
                servox.write(angulo_x)
                servoy.write(angulo_y)
                print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                
        if vry_value > 60000:
            if posx <= 3:
                utime.sleep(0.2)
                posx += 1
                apagar_todos()
                print (vry_value)
                print ("posicao Y:",posx)
                angulo_y = posx*90/4
                servox.write(angulo_x)
                servoy.write(angulo_y)
                print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                
            else:
                posx = 0
                utime.sleep(0.2)
                apagar_todos()
                print (vry_value)
                print ("posicao Y:",posx)
                angulo_y = posx*90/4
                servox.write(angulo_x)
                servoy.write(angulo_y)
                print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                
