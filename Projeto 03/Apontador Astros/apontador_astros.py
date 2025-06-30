from machine import Pin, PWM, ADC, RTC, SoftI2C , UART
from ssd1306 import SSD1306_I2C
import utime
import random
import neopixel
import time
import math
from time import sleep
from math import atan2, degrees

# Configuração dos botões
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

# Configuração OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)
#------------------------------------------------------------------------------------------------
# Configurar UART (ajuste pinos conforme seu microcontrolador)
uart = UART(1, baudrate=9600, tx=8, rx=9)

# Define o fuso horário (ex: Brasil -3)
FUSO = -3

def converter_para_decimal(grau_minuto, direcao):
    graus = int(grau_minuto) // 100
    minutos = float(grau_minuto) % 100
    decimal = graus + minutos / 60
    if direcao in ['S', 'W']:
        decimal = -decimal
    return decimal

def processar_linha(line):
    if line.startswith('$GPRMC'):
        partes = line.split(',')
        if partes[2] == 'A':  # sinal válido
            hora_utc = partes[1]  # hhmmss
            data = partes[9]      # ddmmyy
            lat = partes[3]
            lat_dir = partes[4]
            lon = partes[5]
            lon_dir = partes[6]

            # Extrair hora, minuto, segundo
            hh = int(hora_utc[0:2])
            mm = int(hora_utc[2:4])
            ss = int(hora_utc[4:6])

            # Aplicar fuso horário e ajustar para 24h
            hora_local = (hh + FUSO) % 24

            # Extrair dia, mês, ano
            dia = int(data[0:2])
            mes = int(data[2:4])
            ano = 2000 + int(data[4:6])

            # Converter coordenadas para decimal
            lat_dec = converter_para_decimal(float(lat), lat_dir)
            lon_dec = converter_para_decimal(float(lon), lon_dir)
#------------------------------------------------------------------------------------------------

# Lista de modos
modos = ["Modo Livre", "Modo Sol", "Modo Lua", "Modo Marte"]

modo_selecionado = 0  # Modo que o usuário está navegando
modo_ativo = 0        # Modo confirmado e executado

# Variáveis para controle de debounce dos botões A e B
ultimo_estado_a = 1
ultimo_estado_b = 1
ultimo_tempo_a = utime.ticks_ms()
ultimo_tempo_b = utime.ticks_ms()

debounce_ms = 200

# Função para mostrar o modo no OLED

def mostrar_modos(mensagem_extra=""):
    oled.fill(0)
    oled.text("Modo Ativo:", 0, 0)
    oled.text(modos[modo_ativo], 0, 12)
    if mensagem_extra:
        oled.text(mensagem_extra, 0, 24)  # Mensagem extra logo abaixo do modo ativo
    oled.text("Selecionado:", 0, 32)
    oled.text(modos[modo_selecionado], 0, 44)
    oled.show()
    


# --- Obter data/hora do RTC ---
rtc = RTC()
data = rtc.datetime()  # (ano, mês, dia, dia_da_semana, hora, minuto, segundo, milissegundo)

ano = data[0]
mes = data[1]
dia = data[2]
hora_utc = data[4]
minuto = data[5]
segundo = data[6]

# --- Localização ---
fuso_horario = -3  # UTC-3 (Campinas)
hora_local = (hora_utc + fuso_horario) % 24
latitude = -22.9
longitude = -47.1



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

# Anexa aos pinos GP17 e GP16
servox.attach(16)
servoy.attach(17)

# --- Funções astronômicas ---

def graus_para_horas(angulo): return angulo / 15.0
def limitar_angulo(angulo): return angulo % 360

def julian_date(ano, mes, dia, hora=0, minuto=0, segundo=0):
    if mes <= 2:
        ano -= 1
        mes += 12
    A = ano // 100
    B = 2 - A + (A // 4)
    JD = int(365.25 * (ano + 4716)) + int(30.6001 * (mes + 1)) + dia + B - 1524.5
    frac_dia = (hora + minuto / 60 + segundo / 3600) / 24
    return JD + frac_dia

def tempo_sideral_local(jd, longitude):
    T = (jd - 2451545.0) / 36525
    TS0 = 280.46061837 + 360.98564736629 * (jd - 2451545) + 0.000387933 * T**2 - (T**3) / 38710000
    TS_gmt = limitar_angulo(TS0)
    return limitar_angulo(TS_gmt + longitude)

def ra_dec_para_alt_az(ra_horas, dec_graus, jd, latitude, longitude):
    ra_graus = ra_horas * 15.0
    TS_local = tempo_sideral_local(jd, longitude)
    HA = limitar_angulo(TS_local - ra_graus)
    HA_rad = math.radians(HA)
    dec_rad = math.radians(dec_graus)
    lat_rad = math.radians(latitude)

    sin_alt = math.sin(dec_rad) * math.sin(lat_rad) + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(HA_rad)
    alt = math.asin(sin_alt)

    cos_az = (math.sin(dec_rad) - math.sin(alt) * math.sin(lat_rad)) / (math.cos(alt) * math.cos(lat_rad))
    cos_az = min(1.0, max(-1.0, cos_az))
    az = math.acos(cos_az)
    if math.sin(HA_rad) > 0:
        az = 2 * math.pi - az

    return math.degrees(alt), math.degrees(az)

def dia_do_ano_com_fracao(ano, mes, dia, hora, minuto=0, segundo=0):
    meses_dias = [31,28,31,30,31,30,31,31,30,31,30,31]
    if ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0):
        meses_dias[1] = 29
    soma = sum(meses_dias[:mes-1]) + dia - 1
    frac = (hora + minuto / 60 + segundo / 3600) / 24
    return soma + frac + 1

# --- Efemérides simplificadas ---

def posicao_sol(dia_do_ano):
    L = limitar_angulo(280.46 + 0.9856474 * dia_do_ano)
    g = limitar_angulo(357.528 + 0.9856003 * dia_do_ano)
    lambda_s = limitar_angulo(L + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g)))
    epsilon = math.radians(23.44)
    dec = math.asin(math.sin(epsilon) * math.sin(math.radians(lambda_s)))
    ra = math.atan2(math.cos(epsilon) * math.sin(math.radians(lambda_s)), math.cos(math.radians(lambda_s)))
    if ra < 0:
        ra += 2 * math.pi
    return graus_para_horas(math.degrees(ra)), math.degrees(dec)

def posicao_marte(dia_do_ano):
    N = limitar_angulo(49.5574 + 2.11081E-5 * dia_do_ano)
    w = limitar_angulo(286.5016 + 2.92961E-5 * dia_do_ano)
    a = 1.523688
    e = 0.093405
    M = limitar_angulo(18.6021 + 0.5240207766 * dia_do_ano)
    E = math.radians(M)
    for _ in range(5):
        E -= (E - e * math.sin(E) - math.radians(M)) / (1 - e * math.cos(E))
    E = math.degrees(E)
    x = a * (math.cos(math.radians(E)) - e)
    y = a * math.sqrt(1 - e * e) * math.sin(math.radians(E))
    v = math.degrees(math.atan2(y, x))
    lon = limitar_angulo(v + w)
    epsilon = math.radians(23.44)
    dec = math.asin(math.sin(epsilon) * math.sin(math.radians(lon)))
    ra = math.atan2(math.cos(epsilon) * math.sin(math.radians(lon)), math.cos(math.radians(lon)))
    if ra < 0:
        ra += 2 * math.pi
    return graus_para_horas(math.degrees(ra)), math.degrees(dec)

def posicao_lua(dia_do_ano):
    L = limitar_angulo(218.32 + 13.176396 * dia_do_ano)
    M = limitar_angulo(134.9 + 13.064993 * dia_do_ano)
    lambda_m = limitar_angulo(L + 6.289 * math.sin(math.radians(M)))
    epsilon = math.radians(23.44)
    dec = math.asin(math.sin(epsilon) * math.sin(math.radians(lambda_m)))
    ra = math.atan2(math.cos(epsilon) * math.sin(math.radians(lambda_m)), math.cos(math.radians(lambda_m)))
    if ra < 0:
        ra += 2 * math.pi
    return graus_para_horas(math.degrees(ra)), math.degrees(dec)

# Mostrar o modo inicial
mostrar_modos()

while True:
        

        #calculo das coordenadas
        az_corrigido = 0
        alt_corrigido = 0
        jd = julian_date(ano, mes, dia, hora_utc, minuto, segundo)
        dia_fracionado = dia_do_ano_com_fracao(ano, mes, dia, hora_utc, minuto, segundo)

        vrx_value = adc_vrx.read_u16()  # Lê joystick X
        vry_value = adc_vry.read_u16()  # Lê joystick Y

        acender_led_joystick(vrx_value, posx, posy)  # Atualiza LED com brilho proporcional
        utime.sleep(0.1)  # Pequeno delay para estabilidade
       #---------------------------------------------------------------- 
        estado_a = button_a.value()
        estado_b = button_b.value()
        
        
        tempo_agora = utime.ticks_ms()

        # Leitura botão A
        estado_a = button_a.value()
        if estado_a == 0 and ultimo_estado_a == 1 and utime.ticks_diff(tempo_agora, ultimo_tempo_a) > debounce_ms:
            modo_selecionado = (modo_selecionado + 1) % len(modos)
            mostrar_modos()
            ultimo_tempo_a = tempo_agora
        ultimo_estado_a = estado_a

        # Leitura botão B
        estado_b = button_b.value()
        if estado_b == 0 and ultimo_estado_b == 1 and utime.ticks_diff(tempo_agora, ultimo_tempo_b) > debounce_ms:
            modo_ativo = modo_selecionado
            mostrar_modos()
            ultimo_tempo_b = tempo_agora
        ultimo_estado_b = estado_b

        utime.sleep_ms(100)
        #-----------------------------------------------------------
        if modo_ativo == 1:
            ra_sol, dec_sol = posicao_sol(dia_fracionado)
            alt, az = ra_dec_para_alt_az(ra_sol, dec_sol, jd, latitude, longitude)
            print (alt,az)
            if 180 < 360 - az < 360:
                az_corrigido = (360 - az) - 180
                alt_corrigido = 180 - alt
            elif 360 - az < 180:
                az_corrigido = 360 - az
                alt_corrigido = alt
                
            servox.write(az_corrigido)
            servoy.write(alt_corrigido)            
            mensagem = ""
            if alt < 0:
                servox.write(0)
                servoy.write(0) 
                mensagem = "Abaixo do horizonte"
                mostrar_modos(mensagem)
        if modo_ativo == 2:
            ra_lua, dec_lua = posicao_lua(dia_fracionado)
            alt, az = ra_dec_para_alt_az(ra_lua, dec_lua, jd, latitude, longitude)
            print (alt,az)

            if 180 < 360 - az < 360:
                az_corrigido = (360 - az) - 180
                alt_corrigido = 180 - alt
            elif 360 - az < 180:
                az_corrigido = 360 - az
                alt_corrigido = alt
                
            servox.write(az_corrigido)
            servoy.write(alt_corrigido)       
            mensagem = ""
            if alt < 0:
                servox.write(0)
                servoy.write(0)                 
                mensagem = "Abaixo do horizonte"
                mostrar_modos(mensagem)
        if modo_ativo == 3:
            ra_marte, dec_marte = posicao_marte(dia_fracionado)
            alt, az = ra_dec_para_alt_az(ra_marte, dec_marte, jd, latitude, longitude)
            print (alt,az)
            if 180 < 360 - az < 360:
                az_corrigido = (360 - az) - 180
                alt_corrigido = 180 - alt
            elif 360 - az < 180:
                az_corrigido = 360 - az
                alt_corrigido = alt
                
            servox.write(az_corrigido)
            servoy.write(alt_corrigido)       
                
            mensagem = ""
            if alt < 0:
                servox.write(0)
                servoy.write(0) 
                mensagem = "Abaixo do horizonte"
                mostrar_modos(mensagem)
            
        
            
        #----------------------------------------------
        if modo_ativo ==0:
 
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
                    angulo_y = posx*180/4
                    servox.write(angulo_x)
                    servoy.write(angulo_y)
                    print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                    
                else:
                    posx=4
                    utime.sleep(0.2)
                    apagar_todos()
                    print (vry_value)
                    print ("posicao Y:",posx)
                    angulo_y = posx*180/4
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
                    angulo_y = posx*180/4
                    servox.write(angulo_x)
                    servoy.write(angulo_y)
                    print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                    
                else:
                    posx = 0
                    utime.sleep(0.2)
                    apagar_todos()
                    print (vry_value)
                    print ("posicao Y:",posx)
                    angulo_y = posx*180/4
                    servox.write(angulo_x)
                    servoy.write(angulo_y)
                    print("angulo x:", angulo_x, "| angulo y:", angulo_y)
                    
        if uart.any():
            try:
                line = uart.readline().decode('utf-8').strip()
                processar_linha(line)
            except:
                pass
        time.sleep(0.1)
