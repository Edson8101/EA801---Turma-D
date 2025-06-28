# 🤖 GirassolBot: Robô Seguidor de Luz

![Badge Status](https://img.shields.io/badge/Status-Concluído-success)
![MicroPython](https://img.shields.io/badge/MicroPython-1.19-blue)

Este projeto implementa um robô autônomo seguidor de luz, baseado em sensores de luminosidade BH1750, um display OLED e controle de motores com o driver HW-166. O sistema é programado em MicroPython para detectar a fonte de luz mais intensa e mover-se em sua direção.

---

## 🔄 Histórico do Projeto

O projeto original utilizava **dois sensores BH1750** para medir a iluminação à esquerda e à direita do robô. A lógica era simples: mover-se na direção com maior intensidade luminosa, com base na **diferença entre as medições dos dois sensores**.

No entanto, durante os testes, **um dos sensores apresentou mau funcionamento**, resultando em leituras inconsistentes. Para contornar o problema e garantir o funcionamento do robô, o projeto foi **modificado**:

- O código agora **detecta falhas de leitura** e atua de forma segura.
- Em caso de valores de luz muito baixos ou ausência de leitura, o robô **para automaticamente**.

Essa modificação garantiu a robustez do sistema mesmo com falhas de hardware.

---

## 📸 Demonstração

<img src="images/IMG_20250626_162245706.jpg" width="400">
<img src="images/IMG_20250626_162250723.jpg" width="400">
<img src="images/IMG_20250626_162400869.jpg" width="400">
[![Assista a explicação no YouTube](https://img.youtube.com/vi/ID_DO_VIDEO/hqdefault.jpg)]([https://www.youtube.com/watch?v=ID_DO_VIDEO](https://youtube.com/shorts/RmvDgT72ZjM?feature=share))
[![Assista em ação no YouTube](https://img.youtube.com/vi/ID_DO_VIDEO/hqdefault.jpg)]([https://www.youtube.com/watch?v=ID_DO_VIDEO](https://youtube.com/shorts/DCyMCFHWLeQ?feature=share))

---

## 📦 Componentes Utilizados

- Microcontrolador compatível com MicroPython (ex: Raspberry Pi Pico)
- 2x Sensores de luminosidade **BH1750** (apenas 1 em uso funcional)
- Display OLED 128x64 (I2C)
- Driver de motores **HW-166**
- 2x Motores DC
- 2x Botões (controle de estado e inversão)
- Fios jumpers e fonte de alimentação apropriada

---

## ⚙️ Funcionalidades

- Leitura de luminosidade via I2C
- Exibição de status no display OLED
- Controle de dois motores DC com PWM
- Botão A: liga/desliga o robô
- Botão B: inverte a direção dos motores
- Movimento baseado na fonte de luz mais forte
- Parada automática em ambientes escuros ou falha de sensor

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
    Ligado --> Parado : Ambiente escuro ou erro de leitura

    Frente --> Ligado
    Esquerda --> Ligado
    Direita --> Ligado
    Parado --> Ligado
