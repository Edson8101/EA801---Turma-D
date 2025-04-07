#Bibliotecas necessárias
from machine import Pin, PWM, SoftI2C
from ssd1306 import SSD1306_I2C
import interface
import neopixel
import time
import random

# Configuração OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Inicializa a matriz de LEDs (5x5 = 25 LEDs)
chain = neopixel.NeoPixel(Pin(7), 25)

# Inicializa os botões
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

# Define o pino para o buzzer
buzzer = PWM(Pin(21))

# Define as dimensões da matriz de LEDs
matrix_width = 5
matrix_height = 5

# Define as cores
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (10, 0, 0)
COLOR_GREEN = (0, 10, 0)
COLOR_OFF = (0, 0, 0)

# Padrão da matriz inicial (todos os LEDs acesos na cor vermelha)
M_default = [
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1]
]

# Função para exibir a matriz de LEDs
def draw_matriz(matriz, color):
    """Exibe a matriz de LEDs."""
    for i in range(25):
        chain[i] = COLOR_OFF  # Apaga todos os LEDs
    
    for row in range(5):
        for col in range(5):
            if matriz[row][col] == 1:
                index = row * 5 + col
                chain[index] = color

    chain.write()

# Função para medir o tempo de reação do jogador
def medir_reacao():
    # Aguarda o verde ser aceso e o botão ser pressionado
    start_time = time.ticks_ms()  # Inicia o contador de tempo
    while True:
        if (button_a.value() == 0) and (button_b.value() == 0):  # Botões pressionados novamente
            reaction_time = time.ticks_ms() - start_time  # Calcula o tempo de reação
            bip_buzzer(2000,0.3)  # Emite um bip de 0.3 segundos
            return reaction_time

# Função para fazer o bip no buzzer
def bip_buzzer(duty,duration):
    buzzer.freq(440)          # Define a frequência do som (440Hz, som padrão)
    buzzer.duty_u16(duty)     # Define o volume do som (1000, volume médio)
    time.sleep(duration)           # Duração do bip (0.1 segundos)
    buzzer.duty_u16(0)        # Desliga o buzzer

# Função para fazer a contagem regressiva e ir apagando os LEDs da matriz
def contagem_regressiva():
    time.sleep(1)
    """Apaga os LEDs um por um antes de acender o verde."""
    matriz = [row[:] for row in M_default]
    for i in range(4, -1, -1):
        for j in range(4, -1, -1):
            matriz[i][j] = 0
        draw_matriz(matriz, COLOR_RED)
        bip_buzzer(1000, 0.1)
        time.sleep(1)  

    time.sleep(random.uniform(1, 4))  # Aguarda um tempo aleatório antes de acender o verde
    draw_matriz(M_default, COLOR_GREEN)  # Acende todos os LEDs verdes



# Fica na tela de orientação enquanto não for definido os jogadores
start_game = True
reacA = 0
reacB=  0    
while True:
    if start_game: # Se nenum dos jogadores terem feito nenhuma tentativa de jogar
        draw_matriz(M_default, COLOR_RED)  # Exibe os LEDs em vermelho inicialmente
        interface.tela_inicial()  # Exibe a tela inicial do jogo

    else: # Caso contrário exibe os ultimos tempos de reação
        draw_matriz(M_default, COLOR_RED)  # Exibe os LEDs em vermelho inicialmente
        interface.display_oled(reacA,reacB)

    #Detecta se é o Jogador A 
    if (button_a.value() == 0):
        start_game = False
        #Aguarda os dois botões serem pressionados simultaneamente para iniciar a contagem
        while not ((button_a.value() == 0) and (button_b.value() == 0)):
                interface.start()
        else:
            contagem_regressiva()
            reacA = medir_reacao()
            
            print(f"Tempo de reacao A: {reacA} ms")  # Exibe o tempo de reação no console do computador
    #Detecta se é o Jogador B
    if (button_b.value() == 0):
        start_game = False
        #Aguarda os dois botões serem pressionados simultaneamente para iniciar a contagem
        while not ((button_a.value() == 0) and (button_b.value() == 0)):
                interface.start()
        else:
            contagem_regressiva()
            reacB = medir_reacao()
    
            print(f"Tempo de reacao B: {reacB} ms")  # Exibe o tempo de reação no console do computador
            