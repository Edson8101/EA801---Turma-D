from machine import SoftI2C,Pin
from ssd1306 import SSD1306_I2C
import time
from framebuf import FrameBuffer, MONO_HLSB

# # Configuração oled1
i2c1 = SoftI2C(scl=Pin(3), sda=Pin(2))
oled1 = SSD1306_I2C(128, 64, i2c1)
# # Configuração oled2 (se necessário)
i2c2 = SoftI2C(scl=Pin(1), sda=Pin(0))
oled2 = SSD1306_I2C(128, 64, i2c2)

def limpa_display():
    oled2.fill(0)  # Limpar display
    oled2.show()

# Tela inicial
def tela_inicial():
    oled2.text("Insira a senha", 0, 0)
    oled2.text("padrao:", 0, 12)
    oled2.show()

def atualizar_display(texto,linha):
    oled2.text(texto, 0, linha)
    oled2.show()

def limpar_display():
    oled2.fill(0)
    oled2.show()

def limpar_linha(linha):
    oled2.fill_rect(0, linha, 128, 10, 0)
    oled2.show()

def mostrar_central(texto: str, scale: int = 4):
    """
    Desenha texto (normalmente 8×8 por caractere) escalado *scale* vezes,
    centralizado na OLED 128×64.
    """
    # prepara um FB temporário do tamanho do texto original
    w_char = 8
    h_char = 8
    buf = bytearray(h_char * ((len(texto)*w_char + 7)//8))
    fb = FrameBuffer(buf, len(texto)*w_char, h_char, MONO_HLSB)
    fb.fill(0)
    fb.text(texto, 0, 0, 1)

    # calcula posição para centralizar o bloco inteiro
    total_w = len(texto) * w_char * scale
    total_h = h_char * scale
    x0 = (128 - total_w) // 2
    y0 = (64  - total_h) // 2

    # limpa a tela
    oled2.fill(0)

    # percorre cada pixel do framebuffer e, se estiver “ligado”,
    # desenha um bloco scale×scale na tela principal
    for py in range(h_char):
        for px in range(len(texto)*w_char):
            if fb.pixel(px, py):
                oled2.fill_rect(
                    x0 + px*scale,
                    y0 + py*scale,
                    scale, scale,
                    1
                )

    oled2.show()


def display_oled1(texto: str, scale: int = 4):
    """
    Desenha texto (normalmente 8×8 por caractere) escalado *scale* vezes,
    centralizado na OLED 128×64.
    """
    # prepara um FB temporário do tamanho do texto original
    w_char = 8
    h_char = 8
    buf = bytearray(h_char * ((len(texto)*w_char + 7)//8))
    fb = FrameBuffer(buf, len(texto)*w_char, h_char, MONO_HLSB)
    fb.fill(0)
    fb.text(texto, 0, 0, 1)

    # calcula posição para centralizar o bloco inteiro
    total_w = len(texto) * w_char * scale
    total_h = h_char * scale
    x0 = (128 - total_w) // 2
    y0 = (64  - total_h) // 2

    # limpa a tela
    oled1.fill(0)

    # percorre cada pixel do framebuffer e, se estiver “ligado”,
    # desenha um bloco scale×scale na tela principal
    for py in range(h_char):
        for px in range(len(texto)*w_char):
            if fb.pixel(px, py):
                oled1.fill_rect(
                    x0 + px*scale,
                    y0 + py*scale,
                    scale, scale,
                    1
                )

    oled1.show()
