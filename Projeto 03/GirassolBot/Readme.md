# 🤖 Robô Seguidor de Luz com BH1750, OLED e Driver HW-166

Este projeto implementa um robô autônomo seguidor de luz, baseado em sensores de luminosidade BH1750, um display OLED e controle de motores com o driver HW-166. O sistema é programado em MicroPython para detectar diferenças de luz ambiente e se mover em direção à fonte mais iluminada.

---

## 📸 Demonstração

> _Adicione aqui imagens e um vídeo do robô funcionando._

---

## 📦 Componentes Utilizados

- Microcontrolador compatível com MicroPython (ex: Raspberry Pi Pico)
- 2x Sensores de luminosidade **BH1750**
- Display OLED 128x64 (I2C)
- Driver de motores **HW-166**
- 2x Motores DC
- 2x Botões (controle de estado e inversão)
- Fios jumpers e fonte de alimentação apropriada

---

## ⚙️ Funcionalidades

- Leitura de luminosidade dos sensores BH1750 via I2C
- Exibição de mensagens no display OLED
- Controle de dois motores DC via PWM
- Botão A: liga/desliga o robô
- Botão B: inverte a direção dos motores
- Movimento baseado em detecção da fonte de luz mais intensa
- Parada automática em ambientes escuros

---

## 🧠 Máquina de Estados

```mermaid
stateDiagram-v2
    [*] --> Desligado

    Desligado --> Ligado : Botão A pressionado
    Ligado --> Desligado : Botão A pressionado

    Ligado --> Frente : Luz esquerda ≈ Luz direita
    Ligado --> Esquerda : Luz esquerda > Luz direita + THRESHOLD
    Ligado --> Direita : Luz direita > Luz esquerda + THRESHOLD
    Ligado --> Parado : Ambiente escuro

    Frente --> Ligado
    Esquerda --> Ligado
    Direita --> Ligado
    Parado --> Ligado
