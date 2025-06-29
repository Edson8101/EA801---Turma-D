from machine import Pin
import time

# Colunas = saídas
col_pins = [Pin(x, Pin.OUT) for x in (9, 8, 28)]

# Linhas = entradas com pull-down
row_pins = [Pin(x, Pin.IN, Pin.PULL_DOWN) for x in (18, 19, 20, 4)]

# Mapa da matriz do teclado
key_map = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['*', '0', '#']
]

def ler_teclado():
    for c in range(3):
        col_pins[c].high()

        for r in range(4):
            if row_pins[r].value() == 1:
                # Debounce simples
                time.sleep(0.05)
                if row_pins[r].value() == 1:
                    while row_pins[r].value() == 1:
                        time.sleep(0.01)
                    col_pins[c].low()
                    return key_map[r][c]

        col_pins[c].low()
    return None
