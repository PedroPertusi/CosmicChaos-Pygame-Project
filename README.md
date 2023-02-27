# Cosmic Chaos
### Feito por Pedro Pertusi

# 1. Como executar o jogo?

1. É necessário instalar versão 3.10 ou superior do Python. [Instruções caso necessário!](https://www.youtube.com/watch?v=pDBnCDuL-dc&vl=pt);
2. Neste repositório será necessário clonar o repositório através do terminal usando o comando: *git clone -link* ou baixar o arquivo .zip;
4. Com o terminal aberto na pasta utilize o comando *pip install -r requirements.txt* para instalar tudo necessário para rodar o jogo;
5. Após isso, novamente na pasta baixada/clonada execute o comando python Main.py ou use o botão de executar se disponível.

# 2. Como jogar?

O seu objetivo em Cosmic Chaos é usar seu canhão para destruir os satélites
1. Utilize o ponteiro do mosue para atirar na direção desejada;
2. Você terá 3 tentativas por fase;
3. Quando calculando a rota de seu disparo é importante levar em conta que os planetas possuem gravidade e ao passar por eles seu tiro sofre distorçoes em sua trajetória, *USE ESSA INFORMAÇÃO AO SEU FAVOR*;

# 3. A Física de Cosmic Chaos

Nosso jogo conta com o uso de alguns conceitos da Física, como a Mecânica, Cinemática e Gravitação Universal, para auxilar não só nos movimentos presentes no jogo mas também . Como base para o cálculo dos disparos usamos a formula da distância (d = √((x2 - x1)² + (y2 - y1)²) e também algumas outras como é o caso das formulas do Mov. Uniformemente Variado como: (V = V0 + a * t) e (S = S0 + V0 * t + (a * t^2)/2)
Além disso é implementando em cima dos disparos é a formula da gravidade (g = (G * M) / d²) Onde g é a aceleração gravitacional, M é a massa do corpo central , d é a distância entre o objeto em questão e o centro do corpo central, e G é a constante gravitacional.

# 4.O JOGO
![alt-text](https://github.com/PedroPertusi/CosmicChaos-Pygame-Project/blob/main/Assets/gameplay.gif)
