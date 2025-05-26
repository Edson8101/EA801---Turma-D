from machine import SoftI2C,Pin
from ssd1306 import SSD1306_I2C
import time


# Configuração OLED
i2c = SoftI2C(scl=Pin(3), sda=Pin(2))
oled = SSD1306_I2C(128, 64, i2c)

def limpa_display():
    oled.fill(0)  # Limpar display
    oled.show()

# Tela inicial
def tela_inicial():
    oled.text("Insira a senha", 0, 0)
    oled.text("padrao:", 0, 12)
    oled.show()

def atualizar_display(texto,linha):
    oled.text(texto, 0, linha)
    oled.show()

def limpar_display():
    oled.fill(0)
    oled.show()

def limpar_linha(linha):
    oled.fill_rect(0, linha, 128, 10, 0)
    oled.show()