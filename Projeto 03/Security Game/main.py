import core1_interface as iface
from machine import Pin, PWM
from teclado import ler_teclado
import time
import urandom

# ——————— HARDWARE ———————
buzzer           = PWM(Pin(21))
fechadura        = Pin(17, Pin.OUT)                # solenoide
sensor_porta     = Pin(14, Pin.IN, Pin.PULL_DOWN)  # 1=fechada, 0=aberta
sensor_fechadura = Pin(16, Pin.IN, Pin.PULL_DOWN)  # 1=trava ok, 0=falha

# ——————— ESTADOS & FLAGS ———————
senha_padrao   = "*801"
override_buf   = ""       # buffer que monitora a senha padrão
aberta         = False    # falha: travou aberta
fechada        = False    # falha: travou fechada

state          = "INIT"   # INIT → GAME → INPUT → PASSWORD
rounds         = 0        # quantas fases já completou
seq_len        = 4        # tamanho da sequência atual
sequence       = []       # sequência sorteada
input_seq      = ""       # buffer do que o jogador digitou no GAME
n_rounds       = 4        # número de rodadas para vencer

# ——————— FUNÇÕES AUXILIARES ———————
def bip(d, dur):
    buzzer.freq(440)
    buzzer.duty_u16(d)
    time.sleep(dur)
    buzzer.duty_u16(0)

def sorteia_seq(n):
    return [urandom.getrandbits(8) % 10 for _ in range(n)]

def mostra_seq(seq, delay=1.5):
    for d in seq:
        iface.limpar_display()
        iface.mostrar_central(str(d), scale=7)
        time.sleep(delay)
    iface.limpar_display()

def abrir_porta():
    """Fluxo de abertura da solenoide via senha padrão."""
    iface.limpar_display()
    iface.atualizar_display("Feche Logo", 0)
    iface.atualizar_display("a porta!", 12)
    fechadura.value(2)
    time.sleep(1)
    # espera a porta fechar
    while sensor_porta.value() != 1:
        fechadura.value(2)
        time.sleep(0.1)
    else:
        time.sleep(1)
        fechadura.value(0)
        iface.limpar_display()

# ——————— SETUP ———————
iface.iniciar_interface()
iface.limpar_display()
time.sleep(0.1)
iface.display_oled1("BitDog", scale=3)
print("Jogo iniciado, aguardando '*' ou senha master")

# ——————— LOOP PRINCIPAL ———————
while True:
    tecla = ler_teclado()

    # ————— Override da senha padrão em qualquer momento —————
    if tecla:
        if tecla == "*":
            override_buf = "*"
        elif override_buf:
            override_buf += tecla
        if override_buf == senha_padrao:
            override_buf = ""
            abrir_porta()
            state     = "INIT"
            input_seq = ""
            continue

    # ————— Tela de manutenção, se ocorrer falha —————
    if aberta:
        iface.atualizar_display("Fechadura travou",  0)
        iface.atualizar_display("aberta, leve",      12)
        iface.atualizar_display("para manutencao",   21)
        time.sleep(0.1)
        continue
    if fechada:
        iface.atualizar_display("Fechadura travou",  0)
        iface.atualizar_display("fechada, leve",     12)
        iface.atualizar_display("para manutencao",   21)
        time.sleep(0.1)
        continue

    # ————— Máquina de estados —————
    if state == "INIT":
        iface.atualizar_display("Jogo Iniciado",    0)
        iface.atualizar_display("pressione * para", 12)
        iface.atualizar_display("comecar",          21)
        if tecla == "*":
            state   = "GAME"
            rounds  = 0
            seq_len = 4

    elif state == "GAME":
        iface.limpar_display()
        iface.atualizar_display("Decore a seq.", 0)
        time.sleep(1)
        sequence = sorteia_seq(seq_len)
        mostra_seq(sequence, delay=1.2)
        input_seq = ""
        state     = "INPUT"

    elif state == "INPUT":
        # apaga tudo se apertar '#'
        if tecla == "#":
            input_seq = ""
            iface.limpar_display()

        # coleta dígitos válidos
        elif tecla and tecla.isdigit():
            bip(1000, 0.1)
            input_seq += tecla
            iface.limpar_display()
            iface.atualizar_display(input_seq, 12)

            # avalia só quando completar a sequência
            if len(input_seq) == len(sequence):
                if input_seq == "".join(str(d) for d in sequence):
                    rounds  += 1
                    seq_len += 1
                    if rounds == n_rounds:
                        # jogador venceu → abre a solenoide sem pedir senha
                        abrir_porta()
                        state = "INIT"
                    else:
                        state = "GAME"
                else:
                    # erro → Game Over
                    iface.limpar_display()
                    iface.atualizar_display("Game Over", 0)
                    time.sleep(1.5)
                    state = "INIT"
                input_seq = ""

    time.sleep(0.1)

