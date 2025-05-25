### Referência: https://github.com/canalBrincandoComIdeias/Q0977/

from machine import Pin
from machine import PWM

class Servo:
    
    # Construtor
    def __init__(self):
        self.FREQ = 50
        self.pulse_min = 2000 # 0º ~ 0.61 ms
        self.pulse_max = 7800 # 180º ~ 2.38 ms
        self.duty = self.pulse_min + (self.pulse_max - self.pulse_min) 
    
    # Configura o pino e inicia o PWM
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
