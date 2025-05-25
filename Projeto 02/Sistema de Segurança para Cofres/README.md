<h1 style="color:white; font-size:30px; text-align:center;">Sistema de Segurança para Cofres</h1>

<p align="center">
    <img src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto2/imagens/cofre.jpg"
    alt="Figura 1">
    ><br>
    <em>Figura 1 - Cofre eletrônico <em>
</p>

<p style="color:white; font-size:20px; text-align:left;">
    Neste projeto foi desenvolvido o protótipo de um cofre eletrônico por meio da placa BitDogLab. Além dos recursos existente na placa, foram usados também os seguintes periféricos:
    <ul style="color:white; font-size:20px";>
    <li>Teclado Matricial 4x3</li>
    <li>Servo Motor</li>
    <li>Chave fim de curso</li>
    <li>Acelerômetro MPU-6050</li>
    </ul>
</p>
<h2 style="color:white; font-size:25px; text-align:left;">Metodologia </h2>
<p style="color:white; font-size:20px; text-align:left;">
    Esse projeto visou a implementação de periféricos externos à placa BitDogLab, os quais apresentam diferentes protocolos de comunicação. Enquanto o teclado matricial utiliza a comunicação paralela, o servo motor e o acelerômetro MPU-6050 fazem uso da comunicação serial I2C. Além do uso dos periféricos, o projeto também contou com a utilização dos 2 núcleos da Raspberry para divisão de tarefas, de forma que um núcleo foi usado exclusivamente para o controle do display OLED, enquanto o outro foi usado para as demais tarefas. O projeto foi desenvolvido em linguagem de programação Micropyton.     
    Devido a limitações no fornecimento de componentes, a chave de fim de curso foi substituída por um botão, que apresenta o mesmo funcionamento.
</p>
<p style="color:white; font-size:20px; text-align:left;">
    O fluxograma da execução do projeto está descrito na imagem abaixo:
</p>

<p align="center">
    <img 
    src="https://github.com/JCARNEIROX/EA801/blob/main/Projeto2/imagens/Fluxograma.jpg"
    alt = "Figura 2">
    ><br>
    <em>Figura 2 - Fluxograma do Projeto.<em>
</p>


<p style="color:white; font-size:20px; text-align:left;">
    O acelerômetro está acoplado ao motor que emula a fechadura de forma a monitorar a posição do mesmo. Desta forma, o sistema consegue indicar caso a fechadura apresente mau funcionamento. No caso da fechadura não abrir, o acelerômetro indica que a mesma se encontra ainda na posição fechada e o sistema apresenta no display OLED uma mensagem solicitando a manutenção do cofre. O mesmo ocorre caso a fechadura esteja aberta e não feche ao comando do sistema.
</p>

<h2 style="color:white; font-size:25px; text-align:left;">Resultados </h2>

<p style="color:white; font-size:20px; text-align:left;">
    A implementação das etapas anteriormente descritas pode ser visualizada nas imagens abaixo. A figura 3 apresenta a visão geral do projeto.  
</p>

<p align="center">
  <img 
    src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/visao_geral.jpg" 
    alt="Figura 3"
  ><br>
  <em>Figura 3 - Implementação completa do projeto.</em>
</p>

<p style="color:white; font-size:20px; text-align:left;">
    As imagens a seguir mostram as telas durante o uso do cofre e os possíveis erros que o mesmo pode apresentar 
</p>

<div align="center">
  <table>
    <!-- Linha 1 -->
    <tr>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/senha_padrao.jpg"
            alt="Figura 4"
            width="300" height="300"
          >
          <figcaption><strong>Figura 4.</strong></figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/nova_senha.jpg"
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
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/senha_atualizada.jpg"
            alt="Figura 6"
            width="300" height="300"
          >
          <figcaption><strong>Figura 6.</strong> </figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/insira_senha.jpg"
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
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/senha_correta.jpg"
            alt="Figura 8"
            width="300" height="300"
          >
          <figcaption><strong>Figura 8.</strong></figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/senha_incorreta.jpg"
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
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/sist_bloqueado.jpg"
            alt="Figura 10"
            width="300" height="300"
          >
          <figcaption><strong>Figura 10.</strong> </figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/trav_fechado.jpg"
            alt="Figura 11"
            width="300" height="300"
          >
          <figcaption><strong>Figura 11.</strong> </figcaption>
        </figure>
      </td>
    </tr>
    <!-- Linha 5 -->
    <tr>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/trav_aberta.jpg"
            alt="Figura 12"
            width="300" height="300"
          >
          <figcaption><strong>Figura 12.</strong> </figcaption>
        </figure>
      </td>
      <td>
        <figure style="margin:0; text-align:center;">
          <img
            src="https://github.com/JCARNEIROX/EA801/raw/main/Projeto2/imagens/aguardando_fech.jpg"
            alt="Figura 13"
            width="300" height="300"
          >
          <figcaption><strong>Figura 13.</strong> </figcaption>
        </figure>
      </td>
    </tr>
  </table>
</div>


<h2 style="color:white; font-size:25px; text-align:left;">Instruções de utilização</h2>
<p style="color:white; font-size:20px; text-align:left;">
    As instruções de configuração da sua placa pode ser encontrada no repositório do projeto  <a href="https://github.com/BitDogLab/BitDogLab" target="_blank">BitDogLab</a>, após feita as configurações caso esteja utilizando o VSCode pode carregar os arquivos <b>.py</b> localizados no diretório do <a href="https://github.com/JCARNEIROX/EA801/blob/main/Projeto2" target="_blank">Projeto2</a> na memória da placa <b>Raspberry Pi Pico </b>. Caso surja um erro durante o carregamento de um dos arquivos devido ao <i>import</i> do módulo <a href="https://github.com/JCARNEIROX/EA801/blob/main/Projeto2/ssd1306.py" target="_blank">ssd1306.py</a> faça também o upload do mesmo.
</p>

<p style="color:white; font-size:20px; text-align:left;">
    Conheça mais sobre o projeto e também sobre os componentes da placa, assim como tenha acesso a cursos e tutoriais com códigos em <a href="https://bitdoglab.webcontent.website/" target="_blank">BitDogLab.org</a>
</p>

<h2 style="color:white; font-size:25px; text-align:left;">Referências do Projeto</h2>
<p style="color:white; font-size:20px; text-align:left;">
    M. G. Straub, “Cofre Arduino Projeto para Controle de Acesso com Senha,” Blog Usinainfo, Oct. 15, 2019.
</p>
<p style="color:white; font-size:20px; text-align:left;">
    <a href="https://www.usinainfo.com.br/blog/cofre-arduino-projeto-para-controle-de-acesso-com-senha/?srsltid=AfmBOopagn4NP2jyIW6z99NdNhB9W6G1ilY008_0AgjTOs6b9P-nSh1c " target="_blank">Cofre Arduino Projeto para Controle de Acesso com Senha</a>
</p>

<h2 style="color:white; font-size:25px; text-align:left;">Autores</h2>
<p style="color:white; font-size:20px; text-align:left;">
    João Victor Gomes Carneiro <b>RA:</b> 239738<br>
    Gustavo Elias da Silva <b>RA:</b> 236236<br>
    <b> Faculdade de Engenharia Elétrica e Computação (FEEC) </b>
</p>
