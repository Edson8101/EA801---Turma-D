#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/clocks.h"
#include "hardware/gpio.h"
#include "ws2818b.pio.h"

// Definições de pinos
#define LED_COUNT 25
#define LED_PIN 7
#define BUTTON_A_PIN 5  // Botão para imagem anterior
#define BUTTON_B_PIN 6  // Botão para próxima imagem
#define BUZZER_PIN 21

// Definição de pixel GRB
typedef struct {
    uint8_t G, R, B;
} pixel_t;

// Buffer de pixels
pixel_t leds[LED_COUNT];

// Variáveis PIO
PIO np_pio;
uint sm;

// Protótipos de função
void npInit(uint pin);
void npSetLED(uint index, uint8_t r, uint8_t g, uint8_t b);
void npClear();
void npWrite();
int getIndex(int x, int y);
void playSound();
void showImage(int imageIndex);

// Definição das 4 imagens (matrizes 5x5 de RGB)
const uint8_t IMAGES[4][5][5][3] = {
    // Imagem 1 - Lobo
    {
        {{0, 0, 0}, {100, 100, 100}, {100, 100, 100}, {100, 100, 100}, {0, 0, 0}},
        {{100, 100, 100}, {100, 100, 100}, {0, 0, 0}, {100, 100, 100}, {100, 100, 100}},
        {{158, 151, 151}, {0, 0, 0}, {158, 151, 151}, {0, 0, 0}, {158, 151, 151}},
        {{158, 151, 151}, {158, 151, 151}, {158, 151, 151}, {158, 151, 151}, {158, 151, 151}},
        {{158, 151, 151}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {158, 151, 151}}
    },
    // Imagem 2 - Pokebola
    {
        {{225, 225, 225}, {225, 225, 225}, {225, 225, 225}, {225, 225, 225}, {225, 225, 225}},
        {{225, 225, 225}, {225, 225, 225}, {225, 225, 225}, {225, 225, 225}, {225, 225, 225}},
        {{225, 0, 0}, {225, 0, 0}, {225, 225, 225}, {225, 0, 0}, {225, 0, 0}},
        {{225, 0, 0}, {225, 0, 0}, {225, 0, 0}, {225, 0, 0}, {225, 0, 0}},
        {{225, 0, 0}, {225, 0, 0}, {225, 0, 0}, {225, 0, 0}, {225, 0, 0}}
    },
    // Imagem 3 - Coração
    {
        {{0, 0, 0}, {0, 0, 0}, {100, 0, 0}, {0, 0, 0}, {0, 0, 0}},
        {{0, 0, 0}, {100, 0, 0}, {100, 0, 0}, {100, 0, 0}, {0, 0, 0}},
        {{100, 0, 0}, {100, 0, 0}, {100, 0, 0}, {100, 0, 0}, {100, 0, 0}},
        {{100, 0, 0}, {100, 0, 0}, {100, 0, 0}, {100, 0, 0}, {100, 0, 0}},
        {{0, 0, 0}, {100, 0, 0}, {0, 0, 0}, {100, 0, 0}, {0, 0, 0}}
    },
    // Imagem 4 - Smile
    {
        {{100, 100, 100}, {100, 100, 100}, {137, 137, 137}, {100, 100, 100}, {100, 100, 100}},
        {{100, 100, 100}, {0, 0, 0}, {100, 100, 100}, {0, 0, 0}, {100, 100, 100}},
        {{100, 100, 100}, {100, 100, 100}, {100, 100, 100}, {100, 100, 100}, {100, 100, 100}},
        {{100, 100, 100}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {100, 100, 100}},
        {{100, 100, 100}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {100, 100, 100}}
    }
};

/**
 * Inicializa a máquina PIO para controle da matriz de LEDs.
 */
void npInit(uint pin) {
    uint offset = pio_add_program(pio0, &ws2818b_program);
    np_pio = pio0;

    sm = pio_claim_unused_sm(np_pio, false);
    if (sm < 0) {
        np_pio = pio1;
        sm = pio_claim_unused_sm(np_pio, true);
    }

    ws2818b_program_init(np_pio, sm, offset, pin, 800000.f);
    npClear();
}

void npSetLED(uint index, uint8_t r, uint8_t g, uint8_t b) {
    leds[index].R = r;
    leds[index].G = g;
    leds[index].B = b;
}

void npClear() {
    for (uint i = 0; i < LED_COUNT; ++i)
        npSetLED(i, 0, 0, 0);
}

void npWrite() {
    for (uint i = 0; i < LED_COUNT; ++i) {
        pio_sm_put_blocking(np_pio, sm, leds[i].G);
        pio_sm_put_blocking(np_pio, sm, leds[i].R);
        pio_sm_put_blocking(np_pio, sm, leds[i].B);
    }
    sleep_us(100);
}

/**
 * Função para mapear coordenadas (x,y) para o índice do LED
 */
int getIndex(int x, int y) {
    y = 4 - y;  // Inverte a coordenada y para orientação correta
    
    if (y % 2 == 0) {
        return y * 5 + x;
    } else {
        return y * 5 + (4 - x);
    }
}

/**
 * Efeito sonoro mais animado (bipe curto com dois tons)
 */
void playSound() {
    // Primeiro tom (mais agudo)
    for(int i = 0; i < 5; i++) {
        gpio_put(BUZZER_PIN, 1);
        sleep_us(500);
        gpio_put(BUZZER_PIN, 0);
        sleep_us(500);
    }
    
    // Pequena pausa
    sleep_ms(20);
    
    // Segundo tom (mais grave)
    for(int i = 0; i < 3; i++) {
        gpio_put(BUZZER_PIN, 1);
        sleep_us(1000);
        gpio_put(BUZZER_PIN, 0);
        sleep_us(1000);
    }
}

void showImage(int imageIndex) {
    if (imageIndex < 0) imageIndex = 3;  // Volta para última imagem
    if (imageIndex >= 4) imageIndex = 0; // Volta para primeira imagem
    
    for(int y = 0; y < 5; y++) {
        for(int x = 0; x < 5; x++) {
            int posicao = getIndex(x, y);
            npSetLED(posicao, 
                    IMAGES[imageIndex][y][x][0], 
                    IMAGES[imageIndex][y][x][1], 
                    IMAGES[imageIndex][y][x][2]);
        }
    }
    npWrite();
}

int main() {
    stdio_init_all();

    // Inicializa matriz de LEDs
    npInit(LED_PIN);
    
    // Inicializa botões
    gpio_init(BUTTON_A_PIN);
    gpio_set_dir(BUTTON_A_PIN, GPIO_IN);
    gpio_pull_up(BUTTON_A_PIN);
    
    gpio_init(BUTTON_B_PIN);
    gpio_set_dir(BUTTON_B_PIN, GPIO_IN);
    gpio_pull_up(BUTTON_B_PIN);
    
    // Inicializa buzzer
    gpio_init(BUZZER_PIN);
    gpio_set_dir(BUZZER_PIN, GPIO_OUT);
    gpio_put(BUZZER_PIN, 0);

    int current_image = 0;
    bool button_a_was_pressed = false;
    bool button_b_was_pressed = false;

    // Exibe a primeira imagem inicialmente
    showImage(current_image);

    while(true) {
        // Verifica se o botão A (imagem anterior) foi pressionado
        bool button_a_pressed = !gpio_get(BUTTON_A_PIN);
        if (button_a_pressed && !button_a_was_pressed) {
            current_image = (current_image - 1) % 4;
            playSound();
            showImage(current_image);
            sleep_ms(50);
        }
        button_a_was_pressed = button_a_pressed;

        // Verifica se o botão B (próxima imagem) foi pressionado
        bool button_b_pressed = !gpio_get(BUTTON_B_PIN);
        if (button_b_pressed && !button_b_was_pressed) {
            current_image = (current_image + 1) % 4;
            playSound();
            showImage(current_image);
            sleep_ms(50);
        }
        button_b_was_pressed = button_b_pressed;

        sleep_ms(10);
    }

    return 0;
}