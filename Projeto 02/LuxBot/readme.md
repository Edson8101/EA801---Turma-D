# Robô Seguidor de Luz Autônomo(LuxBot)

![Badge Status](https://img.shields.io/badge/Status-Concluído-success)
![MicroPython](https://img.shields.io/badge/MicroPython-1.19-blue)
![Licença](https://img.shields.io/badge/Licença-MIT-green)

Projeto de um robô autônomo que utiliza sensores de luz (BH1750) para mapear ambientes, identificar a direção de maior luminosidade e seguir a fonte de luz de forma dinâmica.

---

## 📌 Proposta
Desenvolver um sistema embarcado capaz de:
1. Realizar conferencia enre os sensores para medição da intensidade luminosa.
2. Posicionar-se na direção de **maior luminosidade**.
3. Seguir a fonte de luz até que a intensidade diminua **10%**.
4. Reiniciar o ciclo automaticamente, adaptando-se a mudanças no ambiente.

**Aplicações:** Robótica educacional, automação residencial, estudos de eficiência energética.

---

## 🧰 Materiais
| Componente               | Descrição                                                                 |
|--------------------------|---------------------------------------------------------------------------|
| BitDogLab (RPi Pico)     | Placa controladora baseada no Raspberry Pi Pico.                         |
| 2x Sensor BH1750            | Sensor digital de luminosidade (I2C, 1-65535 lux).                       |
| Driver L298N             | Driver para controle de motores DC com PWM.                              |
| 2x Motores DC + Rodas    | Motores de 5-9V com caixa de redução para locomoção.                     |
| Tela OLED 128x64 (I2C)   | Display para exibição de dados em tempo real.                            |
| Bateria 9V               | Fonte de alimentação portátil para motores e eletrônicos.                |

---

## 🛠️ Estrutura do Projeto
### Hardware
1. **Sensoriamento:**
   - **BH1750:** Conectado via I2C (GP0: SDA, GP1: SCL).
2. **Atuação:**
   - **Motores DC:** Controlados pelo driver L298N (GP2-GP7 para direção e PWM).
3. **Interface:**
   - **OLED:** Compartilha o barramento I2C com o BH1750.

### Software
- Arquivo main.py
