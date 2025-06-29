from interface import *
import _thread
import time

# Fila de comandos a serem processados no core 1
comandos = []

def atualizar(msg, linha=0):
    comandos.append(("atualizar", msg, linha))

def limpar():
    comandos.append(("limpar",))

def line_erase(linha):
    comandos.append(("limpar_linha", linha))

def exibe_tela_inicial():
    comandos.append(("tela_inicial",))

def escrever_central(msg):
    comandos.append(("mostrar_central", msg))

def escrever_oled1(msg, scale=4):
    """
    Envia uma mensagem para ser exibida na OLED 1, centralizada e escalada.
    """
    comandos.append(("mostrar_central1", msg, scale))

def interface_core():
    while True:
        if comandos:
            comando = comandos.pop(0)

            if comando[0] == "atualizar":
                atualizar_display(comando[1], comando[2])
            elif comando[0] == "limpar":
                limpar_display()
            elif comando[0] == "limpar_linha":
                limpar_linha(comando[1])
            elif comando[0] == "tela_inicial":
                tela_inicial()
            elif comando[0] == "mostrar_central":
                mostrar_central(comando[1])
            elif comando[0] == "mostrar_central1":
                display_oled1(comando[1], comando[2])
        time.sleep(0.05)

def iniciar_interface():
    _thread.start_new_thread(interface_core, ())
