# EA801 LED Pixel Art

## Autores
- *Lucas Eduardo de Lima Vascon* - RA: 147005
- *Fernando Henrique Velame Nicchio* - RA: 197003

## Sobre o Projeto
Este projeto consiste em criar um catálogo interativo de quatro imagens em estilo pixel art, exibido exclusivamente na matriz de LEDs de uma placa BitDogLab. A interação é feita através de dois botões:

- *Botão A*: Volta à imagem anterior.
- *Botão B*: Avança para a próxima imagem do catálogo.

## Características Principais
- *Matriz de LEDs 5x5* (25 LEDs) usando WS2812B (NeoPixel)
- *4 imagens pré-definidas* armazenadas no código
- *Navegação interativa* usando dois botões
- *Feedback sonoro* ao trocar de imagem
- *Mapeamento correto* das coordenadas físicas dos LEDs

## Hardware Necessário
- *Raspberry Pi Pico*
- *Matriz de LEDs 5x5 WS2812B (NeoPixel)*
- *2 botões* para navegação
- *Buzzer passivo ou ativo*
- *Resistores* de pull-up/pull-down conforme necessário
- *Fonte de alimentação* adequada para os LEDs

## Configuração dos Pinos

| Componente       | Pino GPIO |
|-----------------|-----------|
| Matriz de LEDs  | 7         |
| Botão A (anterior) | 5       |
| Botão B (próximo) | 6       |
| Buzzer         | 21        |

## Estrutura do Código

### Bibliotecas Utilizadas
- pico/stdlib.h: Funções básicas do Raspberry Pi Pico
- hardware/pio.h: Controle do PIO para comunicação com os LEDs
- hardware/clocks.h: Controle de clock
- hardware/gpio.h: Controle de GPIO para botões e buzzer
- ws2818b.pio.h: Programa PIO para controle dos LEDs WS2812B

## Funcionamento
- Pressionar *Botão B* avança a matriz de LEDs para a próxima imagem no catálogo, ciclando entre quatro opções.
- Pressionar *Botão A* retorna à imagem anterior no catálogo.
- Sempre que um dos botões é pressionado, o buzzer emite um som de clique como feedback auditivo.
- O sistema permite navegação cíclica: ao pressionar *B* na última imagem, volta para a primeira; ao pressionar *A* na primeira imagem, retorna à última.

## Imagens do Catálogo
As quatro imagens que compõem o catálogo de pixel art são:

### Coelho (Rabbit)
*Imagem projetada:*  
![Coelho Projetado](https://i.ibb.co/2Q3Nm47/image.png)  

*Imagem na placa:*  
![Coelho na Placa](https://i.ibb.co/v6Qz09B0/Imagem-do-Whats-App-de-2025-04-12-s-21-14-47-7a277970.jpg)

### Lobo (Wolf)
*Imagem projetada:*  
![Lobo Projetado](https://i.ibb.co/BHBXrjhh/image.png)  

*Imagem na placa:*  
![Lobo na Placa](https://i.ibb.co/xqRVDsqL/Imagem-do-Whats-App-de-2025-04-12-s-21-14-47-7af28234.jpg)

###  Coração (Heart)
*Imagem projetada:*  
![Coração Projetado](https://i.ibb.co/2H4gp7V/image.png)  

*Imagem na placa:*  
![Coração na Placa](https://i.ibb.co/whT6nrbk/Imagem-do-Whats-App-de-2025-04-12-s-21-14-47-a54c974c.jpg)

### Pokebola (Pokeball)
*Imagem projetada:*  
![Pokebola Projetada](https://i.ibb.co/3yHb9f9y/image.png)  

*Imagem na placa:*  
![Pokebola na Placa](https://i.ibb.co/21g0w7Gg/Imagem-do-Whats-App-de-2025-04-12-s-21-14-47-bd40efc6.jpg)

## Demonstração do Funcionamento
Aqui está um vídeo demonstrando o funcionamento do projeto, mostrando como as imagens são alternadas na matriz de LEDs:

[![Vídeo de Funcionamento](https://img.youtube.com/vi/jns0QhwUgDM/0.jpg)](https://www.youtube.com/shorts/jns0QhwUgDM?feature=share)
