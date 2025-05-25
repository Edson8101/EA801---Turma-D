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
servo.write(90) # Inicializa o servo motor em 90º (fechado)

#Inicializa o acelerômetro
mpu = MPU6050()

# Função para dar o beep no buzzer
def bip_buzzer(duty,duration):
    buzzer.freq(440)          # Define a frequência do som (440Hz, som padrão)
    buzzer.duty_u16(duty)     # Define o volume do som (1000, volume médio)
    time.sleep(duration)           # Duração do bip (0.1 segundos)
    buzzer.duty_u16(0)        # Desliga o buzzer


# Senha inicial
senha_padrao = "*801"
senha_digitada = ""
senha_salva = ""
tentativas = 3  # contador inicial
# Variáveis de controle das telas
cadastro = False
bloqueado = False
aberta = False
fechada = False

print("Sistema iniciado")
iface.limpar_display()

while True:
    tecla = ler_teclado()
    accel = mpu.read_accel_data() # read the accelerometer [ms^-2]
    aX = accel["x"]
    aY = accel["y"]
    aZ = accel["z"]
    print("x: " + str(aX) + " y: " + str(aY) + " z: " + str(aZ))

    if aberta:
        iface.atualizar_display("Fechadura travou",0)
        iface.atualizar_display("aberta, leve",12)
        iface.atualizar_display("para manutencao",21)
        time.sleep(0.1)
    elif fechada:
        iface.atualizar_display("Fechadura travou",0)
        iface.atualizar_display("fechada, leve",12)
        iface.atualizar_display("para manutencao",21)
        time.sleep(0.1)
    elif not cadastro:
        iface.exibe_tela_inicial()
    elif not bloqueado and cadastro:
        iface.atualizar_display("Insira a senha:", 0)
    else:
        iface.exibe_tela_inicial()

    if tecla:
        bip_buzzer(1000,0.1)
        if tecla == "#":
            senha_digitada = ""
            iface.line_erase(21)
        else:
            senha_digitada += tecla
            iface.atualizar_display("*" * len(senha_digitada),21)

        if len(senha_digitada) == 4:
            if bloqueado:
                if senha_digitada == senha_padrao:
                    iface.limpar_display()
                    iface.atualizar_display("Desbloqueado!", 0)
                    time.sleep(1)
                    bloqueado = False
                    senha_digitada = ""
                    tentativas = 3
                    iface.limpar_display()
                else:
                    iface.limpar_display()
                    iface.atualizar_display("Senha padrão errada", 0)
                    time.sleep(1)
                    senha_digitada = ""

            elif senha_digitada == senha_padrao:
                iface.limpar_display()
                iface.atualizar_display("Nova senha:", 0)
                nova_senha = ""
                while len(nova_senha) < 4:
                    t = ler_teclado()
                    if t:
                        if t == "#":
                            nova_senha = ""
                            iface.line_erase(12)
                        else:
                            bip_buzzer(1000,0.1)
                            nova_senha += t
                            iface.atualizar_display("*" * len(nova_senha),12)
                            time.sleep(0.2)
                senha_salva = nova_senha
                iface.limpar_display()
                iface.atualizar_display("Senha atualizada", 0)
                time.sleep(1)
                iface.limpar_display()
                cadastro = True
                senha_digitada = ""
                tentativas = 3

            elif senha_digitada == senha_salva:
                senha_digitada = ""
                iface.limpar_display()
                iface.atualizar_display("Senha correta", 0)
                servo.write(0)  # Abre a porta
                time.sleep(2) # Espera a porta abrir e estabelecer na posição

                accel = mpu.read_accel_data() # Inicia o acelerometro pra garantir que a tranca esteja aberta
                aY = accel["y"]
                if not (-3 <= aY <= 1):
                    iface.limpar_display()
                    fechada = True
                else:
                    iface.limpar_display()
                    while not (porta.value() == 1):
                        iface.atualizar_display("Aguardando", 0)
                        iface.atualizar_display("fechar...", 12)
                        time.sleep(0.1)
                    else:
                        servo.write(90)  # Fecha a porta
                        time.sleep(0.5)

                    iface.limpar_display()
                    time.sleep(2) # Espera a porta fechar e estabelecer na posição
                    accel = mpu.read_accel_data() # Inicia o acelerometro pra garantir que a tranca esteja fechada
                    aY = accel["y"]
                    if not ( aY <= -7):
                        iface.limpar_display()
                        aberta = True # Fechadura travou aberta

            else:
                tentativas -= 1
                iface.limpar_display()
                iface.atualizar_display("Senha incorreta", 0)
                time.sleep(1)
                if tentativas == 0:
                    iface.limpar_display()
                    iface.atualizar_display("Sistema bloqueado", 0)
                    time.sleep(5)
                    iface.limpar_display()
                    senha_digitada = ""
                    bloqueado = True
                    cadastro = False
                else:
                    senha_digitada = ""
                    iface.limpar_display()
    
    time.sleep(0.1)
