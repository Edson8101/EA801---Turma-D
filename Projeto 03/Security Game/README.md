<h1 style="color:white; font-size:30px; text-align:center;">Security Game</h1>

<p align="center">
    <img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto3/imagens/cofre.jpg"
    alt="Figura 1"
    ><br>
</p>

<h3 style="color:white; font-size:20px; text-align:left;">EA801</h3>
<h3 style="color:white; font-size:20px; text-align:left;">Turma D</h3>
<h3 style="color:white; font-size:20px; text-align:left;">Professor Fabiano Fruett</h3>

<h2 style="color:white; font-size:25px; text-align:left;">Alunos</h2>
<ul style="color:white; font-size:20px; text-align:left;">
  <li>Gustavo Elias Da Silva, RA: 236236</li>
  <li>João Victor Gomes Carneiro, RA: 239738</li>
</ul>

<h2 style="color:white; font-size:25px; text-align:left;">Contatos</h2>

<ul style="color:white; font-size:20px; text-align:left;">
  <li><a href="mailto:g236236@dac.unicamp.br">g236236@dac.unicamp.br</a></li>
  <li><a href="mailto:j239738@dac.unicamp.br">j239738@dac.unicamp.br</a></li>
</ul>

<h2 style="color:white; font-size:25px; text-align:left;">Descrição</h2>
<p style="color:white; font-size:20px; text-align:left;">
Este projeto é uma evolução do <a href="https://github.com/JCARNEIROX/EA801/blob/main/Projeto2" target="_blank">Projeto2</a>, que transformou o sistema de segurança em um jogo interativo com a placa <a href="https://github.com/BitDogLab/BitDogLab" target="_blank">BitDogLab</a>. Neste projeto foram implementadas novas estruturas para melhor apresentação do sistema, como a elaboração da estrutura física do cofre em MDF e a elaboração de uma placa de circuito impresso para a conexão e interfaceamento dos periféricos com a placa BitDogLab. Com isso, os componentes presentes neste projeto, além da placa de desenvolvimento da disciplina, foram:</p>
<ul style="color:white; font-size:20px";>
  <li>Teclado Matricial 4×3</li>
  <li>Solenoide 12 V</li>
  <li>Sensor Reed Switch</li>
  <li>Placa de Circuito Impresso (PCB)</li>
  <li>Regulador de tensão 7805</li>
  <li>Circuito ponte H L293D</li>
  <li>Display OLED 128×64</li>
  <li>Diodo 1N4007</li>
  <li>Ímã de neodímio</li>
  <li>Estrutura de MDF para o cofre</li>
</ul>

<h2 style="color:white; font-size:25px; text-align:left;">Metodologia</h2>
<p style="color:white; font-size:20px; text-align:left;">
Esse projeto visou a implementação de periféricos externos à placa BitDogLab, os quais apresentam diferentes protocolos de comunicação. Enquanto o teclado matricial utiliza comunicação paralela, o display OLED utiliza I2C. Além do uso dos periféricos, o projeto contou com a utilização dos dois núcleos da Raspberry Pi para divisão de tarefas: um núcleo foi dedicado exclusivamente ao controle do display OLED, enquanto o outro cuidou das demais funções. O desenvolvimento foi feito em MicroPython.</p>

<p style="color:white; font-size:20px; text-align:left;">
O projeto inicial previa alimentação em 15 V, mas devido à disponibilidade foi usada uma fonte de notebook de 19,5 V. O acionamento da solenóide (fechadura) foi feito com o CI L293D (meia-ponte H), usando duas saídas para fornecer a corrente necessária.
</p>

<p style="color:white; font-size:20px; text-align:left;">
Como a placa BitDogLab requer 5 V, foi usado um regulador 7805 com dissipador para converter os 19,5 V da fonte para 5 V.
</p>

<p style="color:white; font-size:20px; text-align:left;">
Para verificar o fechamento da porta do cofre, usou-se um sensor Reed Switch acionado por um ímã na porta.
</p>

<p style="color:white; font-size:20px; text-align:left;">
A seguir, detalhes do circuito e suas características de funcionamento.
</p>

<h2 style="color:white; font-size:25px; text-align:left;">Projeto da PCB</h2>

<p style="color:white; font-size:20px; text-align:left;">
Foi desenvolvida uma PCB para compatibilizar os diferentes níveis de tensão: a solenóide opera em 12 V, e a BitDogLab em ≈ 4,3 V (5 V do regulador menos a queda de um diodo em série). O projeto da placa foi feito no KiCad e confeccionado em laboratório.</p>
<p align="center">
    <img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto3/imagens/schematico_kicad.png"
    alt="Figura 1">
    <br>
    <em>Figura 1 - Esquemático da placa de circuito impresso <em>
</p>
<p align="center">
    <img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto3/imagens/PCB_3D.png"
    alt="Figura 1">
    <br>
    <em>Figura 2 - Vista 3D da placa de circuito impresso <em>
</p>


<h2 style="color:white; font-size:25px; text-align:left;">Funcionamento do Jogo</h2>

<p style="color:white; font-size:20px; text-align:left;">O fluxograma de execução está ilustrado abaixo.</p>
<p align="center">
    <img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto3/imagens/fluxograma.png"
    alt="Figura 1">
    <br>
    <em>Figura 3 -Fluxograma do Projeto <em>
</p>

<p style="color:white; font-size:20px; text-align:left;">Implementou-se também um dispositivo de segurança: ao digitar a senha padrão <strong>*801</strong> a qualquer momento em espera de sequência, o cofre libera imediatamente. Ao fechar a porta, o jogo reinicia.</p>

<h2 style="color:white; font-size:25px; text-align:left;">Resultados</h2>
<div align="center">
  <table>
    <!-- Linha 1 -->
    <tr>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto3/imagens/fig4.jpg"
            alt="Figura 4"
            width="300" height="300"
          >
          <figcaption><strong>Figura 4.</strong></figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto3/imagens/fig5.jpg"
            alt="Figura 5"
            width="300" height="300"
          >
          <figcaption><strong>Figura 5.</strong></figcaption>
        </figure>
      </td>
    </tr>
    <!-- Linha 2 -->
    <tr>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto3/imagens/fig6.jpg"
            alt="Figura 6"
            width="300" height="300"
          >
          <figcaption><strong>Figura 6.</strong> </figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto3/imagens/fig7.jpg"
            alt="Figura 7"
            width="300" height="300"
          >
          <figcaption><strong>Figura 7.</strong> </figcaption>
        </figure>
      </td>
    </tr>
    <!-- Linha 3 -->
    <tr>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto3/imagens/fig8.jpg"
            alt="Figura 8"
            width="300" height="300"
          >
          <figcaption><strong>Figura 8.</strong></figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto3/imagens/fig9.jpg"
            alt="Figura 9"
            width="300" height="300"
          >
          <figcaption><strong>Figura 9.</strong> </figcaption>
        </figure>
      </td>
    </tr>
    <!-- Linha 4 -->
    <tr>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto3/imagens/fig10.jpg"
            alt="Figura 10"
            width="300" height="300"
          >
          <figcaption><strong>Figura 10.</strong> </figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto3/imagens/fig11.jpg"
            alt="Figura 11"
            width="300" height="300"
          >
          <figcaption><strong>Figura 11.</strong> </figcaption>
        </figure>
      </td>
    </tr>
  </table>
</div>

<h2 style="color:white; font-size:25px; text-align:left;">Referência de projeto</h2>

<p style="color:white; font-size:18px; text-align:left;">M. G. Straub, “Cofre Arduino Projeto para Controle de Acesso com Senha,” Blog Usinainfo, 15 out 2019. <a href="https://www.usinainfo.com.br/blog/cofre-arduino-projeto-para-controle-de-acesso-com-senha/?srsltid=AfmBOopagn4NP2jyIW6z99NdNhB9W6G1ilY008_0AgjTOs6b9P-nSh1c">Disponível online</a> (acesso em 21 abr 2025).</p>

