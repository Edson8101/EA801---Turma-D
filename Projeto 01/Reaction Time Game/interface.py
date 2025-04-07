from machine import SoftI2C,Pin
from ssd1306 import SSD1306_I2C


# Configuração OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Tela inicial
def tela_inicial():
    oled.fill(0)
    oled.text("Reaction Time", 0, 0)
    oled.text("Welcome to Reaction", 0, 12)
    oled.text("Time Game.Define", 0, 21)
    oled.text("players A and B.", 0, 31)
    oled.show()

# Função para exibir os últimos tempos de reação no display OLED
def display_oled(reacA,reacB):
    oled.fill(0)  # Limpar display
    oled.text("Reaction Time", 12, 0)
    oled.text(" ", 0, 10)
    oled.text("Last Times:", 0, 20)
    #coloca um espaço em branco
    oled.text(" ", 0, 30)
    oled.text(f"Player A = {reacA}ms", 0, 40)
    oled.text(f"Player B = {reacB}ms", 0, 50)
    oled.show()

# Função para exibir orientações no display OLED
def start():
    oled.fill(0)
    oled.text("Press two bottons", 0, 0)
    oled.text("to start and", 0, 10)
    oled.text("get ready.", 0, 19)
    oled.show()