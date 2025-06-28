# 🤖 GirassolBot: Robô Seguidor de Luz

![Badge Status](https://img.shields.io/badge/Status-Concluído-success)
![MicroPython](https://img.shields.io/badge/MicroPython-1.19-blue)

Este projeto implementa um robô autônomo seguidor de luz, usando um sensor de luminosidade **BH1750**, um display **OLED 128x64** e controle de motores via driver **HW-166**. A lógica é programada em **MicroPython**.

---

## 🛠️ Projeto Original (followlux.py)

Inicialmente, o projeto utilizava **dois sensores BH1750**, posicionados à esquerda e à direita do robô, com a lógica de seguir a direção com maior luminosidade. No entanto, um dos sensores apresentou defeito, causando leituras inválidas.

Em vez de substituir o sensor, optamos por adaptar o projeto para **funcionar com apenas um BH1750** e implementar um novo comportamento baseado em **giro 360° + limiar de luz**.

O código original está preservado no arquivo `followlux.py` como referência.

---

## ✅ Versão Atual (main.py)

A nova versão do projeto está no arquivo `main.py` e traz as seguintes melhorias:

### ⚙️ Funcionalidades principais:

- **Leitura de luminosidade com 1 BH1750** (via I2C)
- **Display OLED** exibe mensagens de status e valores de luminosidade
- Controle de motores com **driver HW-166**
- **Giro de 360° automático** para buscar direção com maior luminosidade
- **Botão A alterna entre 4 modos:**
  1. **Desligado**
  2. **Seguir luz acima de 100 lux**
  3. **Seguir luz acima de 200 lux**
  4. **Seguir luz acima de 500 lux**
- **Botão B inverte a direção** dos motores

---

## 📸 Demonstração

<img src="imagens/IMG_20250626_162245706.jpg" width="400">
<img src="imagens/IMG_20250626_162250723.jpg" width="400">
<img src="imagens/IMG_20250626_162400869.jpg" width="400">

### Explicando o funcionamento:

[![Assista no YouTube](https://img.youtube.com/vi/RmvDgT72ZjM/hqdefault.jpg)](https://youtube.com/shorts/RmvDgT72ZjM)

### GirassolBot em ação

[![Assista no YouTube](https://img.youtube.com/vi/DCyMCFHWLeQ/hqdefault.jpg)](https://youtube.com/shorts/DCyMCFHWLeQ)

---

## 📦 Componentes Utilizados

- Placa microcontroladora compatível com MicroPython (ex: Raspberry Pi Pico)
- 1x Sensor de luminosidade **BH1750**
- Display OLED 128x64 (I2C)
- Driver de motor **HW-166**
- 2x Motores DC
- 2x Botões (controle de modo e inversão)
- Fios, protoboard e fonte de alimentação

---

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

## 🔄 Máquina de Estados Simplificada

```mermaid
stateDiagram-v2
    [*] --> Desligado

    Desligado --> Seguir100 : Botão A
    Seguir100 --> Seguir200 : Botão A
    Seguir200 --> Seguir500 : Botão A
    Seguir500 --> Desligado : Botão A

    Seguir100 --> Procurando : Luz < 100
    Seguir200 --> Procurando : Luz < 200
    Seguir500 --> Procurando : Luz < 500

    Procurando --> Seguir : Luz >= limiar
    Seguir --> Procurando : Luz < limiar
