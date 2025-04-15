# Projeto EA801 LED Pixel Art

**Autores:**  
- Lucas Eduardo de Lima Vascon, RA: 147005  
- Fernando Henrique Velame Nicchio, RA: 197003  

## Descrição do Projeto  
O projeto consiste em um catálogo interativo de quatro imagens em estilo pixel art, exibido em uma matriz de LEDs 5x5 (WS2812B) da placa BitDogLab. A navegação entre as imagens é feita através de dois botões, com feedback sonoro ao trocar de imagem.

## Características Principais  
- Matriz de LEDs 5x5 (25 LEDs) usando WS2812B (NeoPixel).  
- 4 imagens pré-definidas armazenadas no código.  
- Navegação entre imagens usando dois botões.  
- Feedback sonoro ao trocar de imagem.  
- Mapeamento correto de coordenadas para a disposição física dos LEDs.  

## Hardware Necessário  
- **Raspberry Pi Pico**  
- **Matriz de LEDs 5x5 WS2812B (NeoPixel)**  
- 2 botões para navegação  
- **Buzzer passivo ou ativo**  
- **Resistores de pull-up/pull-down conforme necessário**  
- **Fonte de alimentação adequada para os LEDs**  

## Configuração dos Pinos  
| Componente          | Pino GPIO |  
|---------------------|----------|  
| Matriz de LEDs      | 7        |  
| Botão A (anterior)  | 5        |  
| Botão B (próximo)   | 6        |  
| Buzzer              | 21       |  

## Bibliotecas Utilizadas  
- `pico/stdlib.h`: Funções básicas do Raspberry Pi Pico.  
- `hardware/pio.h`: Controle do PIO para comunicação com os LEDs.  
- `hardware/clocks.h`: Controle de clock.  
- `hardware/gpio.h`: Controle de GPIO para botões e buzzer.  
- `ws2818b.pio.h`: Programa PIO para controle dos LEDs WS2812B.  

## Funcionamento  
1. **Botão B**: Avança para a próxima imagem no catálogo (cicla entre 4 opções).  
2. **Botão A**: Volta para a imagem anterior no catálogo.  
3. **Feedback sonoro**: O buzzer emite um som de clique ao pressionar qualquer botão.  
4. **Ciclo de imagens**: Ao chegar à última imagem e pressionar **B**, volta para a primeira. Pressionar **A** na primeira imagem vai para a última.  

## Imagens do Catálogo  
1. **Coelho (Rabbit)**  
2. **Lobo (Wolf)**  
3. **Coração (Heart)**  
4. **Pokebola (Pokeball)**  

## Vídeo Demonstrativo  
Assista ao funcionamento do projeto [aqui]([https://youtube.com/shorts/QyNCzWLz_c87feature=share]).  
