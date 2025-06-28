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

### Fotos do Protótipo
<img src="images/" width="400">
<img src="images/" width="400">
