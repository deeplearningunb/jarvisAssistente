# jarvisAssistente
Assistente virtual Jarvis para linux

# Ideia

## Qual o problema que o Jarvis vem para solucionar?
A falta de bons assistentes virtuais para as máquina desktop linux com base nas
distribuições debian. 

## O que é o jarvis?   
É um assistente virtual que contém uma rede neural que serve para identificar
e classificar o que o usuário falou com seus comandos internos da ferramenta e
assim executar tarefas relacionadas ao que foi dito.

## Quem é o usuário do Jarvis?   
O usuário do jarvis são as pessoas que desejam ter um assistente virtual dentro
de distribuições como ubuntu, pop-os, etc. Distribuições base debian que não possuem
assistente virtuais dentro de sua plataforma.


# Equipe

## Quais talentos a equipe precisa?   
Para um bom desenvolvimento a equipe necessita de ter:
* Desenvolvedores pleno ou junior de python que saibam sobre tratamento
 de voz com python;
* Desenvolvedores pleno ou junior que saibam trabalhar com redes neurais e dados;
* Desenvolvedores que saibam colocar uma solução em produção;
* Product Manager para entender e arquitetar o que o produto deveria ter e fazer;

## Quem é o líder da equipe?
* Líder da equipe é a única pessoa que está nela: Victor Hugo Dias Coelho;

## Regras de conduta
1. Toda branch tem que ter uma issue associada;
2. Todo problema tem que ser descrito através de uma issue;
3. A branch tem que ter como prefixo o número da issue e como título um preve
resumo ou o título completo da issue;
4. Só serão aceitos PRs cuja o CI estiver passando e que estiver com a menos 1
aprovação de uma pessoa diferente da que realizou a mudança;(Isso não vale para a equipe de 1 pessoa só)
5. O card no kanban tem que ser devidamente movimentado conforme sua execução;

## Quantas pessoas essa equipe tem?
* Apenas 1: Victor Hugo Dias Coelho

# Planejamento
## Objetivo
Ter uma ferramenta utilizável com uma solução se utilizando de redes neurais com
tarefas simples. Essas tarefas são:   
* Controle de volume;
* Controle de multimídia das músicas;
* Execução de músicas do spotify;
* Abri programas;
* Fechar programas;
* Realizar pesquisas no google;
* Sair do jarvis;

## Metas
Conseguir pelo menos 90% dos comandos descritos anteriormente funcionando da maneira
correta com a classificação do comando realizado;

## Tarefas
Toda as tarefas estão descritas no quadro do kanban relacioando a esse projeto
no zenhub;

## Recursos necessários
* Máquina com pelo menos 4 gb de ram;
* Máquina que tenha microfone a alto falantes;
* Máquina com spotify instalado para realização dos comandos no mesmo;
* Máquina com acesso a internete para fazer as pesquisas do google;
* Máquina com sistema operacional com kernel linux e distribuições base debian;
* Espaço 100 mb de espaço em disco;
* Máquina tem que ter python e pip instalados;

## Riscos do projeto
* Por haver só um indivíduo qualquer problema de saúde para causar o não desenvolvimento do produto
* Caso o dado de comandos não seja encontrado ou não consiga ser feito não será
possível treinar a rede;
* Caso o tempo não seja suficiente dentro do cronograma;

## Cronograma
|Tarefa|Tempo|
|---|---|
|Realização da base line do produto|04/05/2022|
|Realização da documentação e do vídeo de apresentação do produto|05/05/2022|

## Membros/Stakeholders
* Victor Hugo Dias Coelho

# Observações
* Além dos pacotes que estão nos requirements os usuários precisam instalar
outros pacotes via apt-get.

`sudo apt-get install qdbus-qt5 espeak python3-pyaudio dbus`

# Como rodar o sistema;
Para rodar o sistema tem que ter instalado todos os requisitos que tem no arquivo
requerements.txt dentro da pasta source:

`pip3 install -r requerements.txt`

Para executar o jarvis basta digitar `python3 src/jarvis.py`. Após o jarvis falar
bem vindo. Você pode começar a se comunicar com ele.
