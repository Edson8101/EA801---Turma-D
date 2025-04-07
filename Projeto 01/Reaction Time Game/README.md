<h1 style="color:white; font-size:30px; text-align:center;">Reaction Time Game</h1>

<div align="center">
    <img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/imagens/farol.jpg">
</div></div>

<p style="color:white; font-size:20px; text-align:left;">
    Este jogo foi inspirado nas corridas de fórmula 1 e provas de arrancadas popularmente conhecidas. Neste tipo de esporte os pilotos dos carros precisam estar atentos aos faróis para dar a largada e iniciar a corrida. Neste esporte geralmente os faróis possuem o layout como da imagem acima e a contagem para partida se inicia na horizontal ascendendo cada luz vermelha, a partida é autorizada quando todas as luzes se apagam.
</p>
<p style="color:white; font-size:20px; text-align:left;">
    O <b>Reaction Time Game</b> vem para simular na placa <a href="https://github.com/BitDogLab/BitDogLab" target="_blank">BitDogLab</a> esta etapa inicial presente nos esportes de automobilismo, o jogo visa propor uma disputa entre dois jogadores para ver qual possui melhor tempo de reação. Para este fim foram utilizados os seguintes periféricos presente na placa:
</p>
<ul style="color:white; font-size:20px";>
    <li>Matriz de LEDs</li>
    <li>Display OLED</li>
    <li>Botões A e B</li>
    <li>BBuzzer</li>
</ul>
<p style="color:white; font-size:20px; text-align:left;">
    A linguagem de programação utilizada foi o Micropython e foi usado o <a href="https://code.visualstudio.com/" target="_blank">Visual Studio Code</a> (VSCode) como ambiente de edição dos códigos assim como a extensão <a href="https://github.com/paulober/MicroPico" target="_blank">MicroPico</a> para permitir a interface entre computador e microntrolador.  
</p>
<h2 style="color:white; font-size:25px; text-align:left;">Fluxo do código</h2>
<p style="color:white; font-size:20px; text-align:left;">
    O Script <a href="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/main.py" target="_blank">main.py</a> segue a dinâmica descrita de acordo com o fluxograma da imagem à seguir:
</p>
<div align="center">
    <img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/imagens/Fluxograma.jpg">
</div></div>
<p style="color:white; font-size:20px; text-align:left;">
    Os jogadores podem permanecer jogando e caso queiram reiniciar os placares basta pressionar o botão reset contido na placa!
</p>
<h2 style="color:white; font-size:25px; text-align:left;">Imagens da Implementação na Placa</h2>
<div align="center">
    <table>
        <tr>
            <td><img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/imagens/frente.jpg" width="300" height="300"></td>
            <td><img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/imagens/inicio.jpg" width="300" height="300"></td>
        </tr>
        <tr>
            <td><img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/imagens/start.jpg" width="300" height="300"></td>
            <td><img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/imagens/start.jpg" width="300" height="300"></td>
        </tr>
    </table>
</div>
<p style="color:white; font-size:20px; text-align:left;">
    A imagem acima mostra os estados que se passam durante o jogo na placa. A seguir tem-se um gif de uma simulação de uma jogada por um dos jogadores.
</p>
<div align="center">
    <img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/imagens/gif.gif" width="600" height="600">
</div></div>
<h2 style="color:white; font-size:25px; text-align:left;">Instruções de utilização</h2>

<p style="color:white; font-size:20px; text-align:left;">
    As instruções de configuração da sua placa pode ser encontrada no repositório do projeto  <a href="https://github.com/BitDogLab/BitDogLab" target="_blank">BitDogLab</a>, após feita as configurações caso esteja utilizando o VSCode pode carregar os arquivos <a href="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/main.py" target="_blank">main.py</a> e <a href="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/interface.py" target="_blank">interface.py</a> na memória da placa <b>Raspberry Pi Pico </b>. Caso surja um erro durante o carregamento de um dos arquivos devido ao <i>import</i> do módulo <a href="https://github.com/JCARNEIROX/EA801/blob/main/Projeto1/ssd1306.py" target="_blank">ssd1306.py</a> faça também o upload do mesmo.
</p>

<p style="color:white; font-size:30px; text-align:left;">
    <b>Tudo pronto! Agora é só ver quem é mais ágil!</b>
</p>

<p style="color:white; font-size:20px; text-align:left;">
    Conheça mais sobre o projeto e também conheça mais sobre os compnentes da placa assim como tenha acesso a cursos e tutoriais com códigos em <a href="https://bitdoglab.webcontent.website/" target="_blank">BitDogLab.org</a>
</p>