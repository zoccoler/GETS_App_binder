# GETS_App: Aplicação Web para Análise Temporal de Dados do GETS (com mybinder)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zoccoler/GETS_App_binder/HEAD)

## Índice

[Descrição Geral](#geral)

[Utilização](#utilizacao)

[Financiamento](#financiamento)

[Licença](#licenca)

## Descrição Geral

Aplicação web para visualização inteligente de dados de equipamentos hospitalares e serviços relacionados do sistema de Gestão de Tecnologia para a Saúde (GETS), desenvolvido pelo Laboratório Nacional para Gerenciamento de Tecnologia em Saúde (LNGTS).

Utiliza as tabelas geradas pelo GETS para produção de gráficos interativos e gera modelos de séries temporais otimizados para construção de linhas de tendência em relação à manutenção de equipamentos médico-hospitalares.

Neste repositório, nós fornecemos os códigos-fonte para rodar a aplicação localmente pela plataforma como serviço Docker (Docker, Inc.).

## Utilização

1. Compactar tabelas em arquivo ".zip":
  - Utilize um software de compressão de arquivos, como o [WinRAR](https://www.win-rar.com/) para compactar as tabelas do GETS (ou uma pasta contendo as tabelas) num único arquivo ".zip".
  - **Importante**: a aplicação não aceita ".rar", deve ser ".zip";
2. Carregar repositório no Mybinder:
  - Clique na tag [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/zoccoler/GETS_App_binder/HEAD) e aguarde a criação do ambiente;
  - Após certo tempo, a interface do Jupyter notebook deve aparecer.
3. Fazer o upload das tabelas:
  - Clique na pasta "data" para abrí-la (veja figura abaixo);
![load1](/figuras/load1.png)
  - Clique no botão "Upload" (mostrado em vermelho na figura abaixo) e selecione o arquivo ".zip" contendo todas as tabelas;
![load2](/figuras/load2.png)
  - Clique no botão azul de "Upload" (destacado em vermelho na figura abaixo). Em seguida retorne ao diretório raíz clicando no ícone da pasta destacado em verde na figura abaixo.
![load3](/figuras/load3.png)
4. Abrir o código principal:
  - Clique sobre o arquivo entitulado "Interface_temporal_GETS.ipynb";
  - O código deve abrir numa nova aba/janela como ilustrado abaixo;
![voila1](/figuras/voila1.png)
5. Abrir a interface pelo Voilà:
  - Clique no botão Voilà;
  - A interface principal da aplicação vai abrir numa nova aba/janela (veja figura abaixo).
![interface1](/figuras/interface1.png)
6. Clique no botão "Carregar Tabelas". Se alguma tabela estiver faltando, você será informado com uma mensagem abaixo do botão.
  - **Observação**: após o carregamento das tabelas, o arquivo ".zip" é deletado do ambiente virtual do binder.
7. Selecione um ou mais equipamentos pelo campo "Equipamento";
8. Selecione uma data inicial de análise pelo campo "Data Inicial";
9. Selecione uma data final de análise pelo campo "Dara Final";
10. Pronto! O gráfico deve ser apresentado no centro da tela.
**Observação**:  Os aquivos de saída que você salvar serão armazenados na pasta “gets_app/data” e deverão ser baixados dest pasta antes de fechar as abas da aplicação. Para isso, é necessário selecionar os arquivos (assinalar as checkboxes) e clicar no botão Download (como ilustrado abaixo).
![save_binder](/figuras/save_binder.png)

A aplicação contém 3 abas: Quantidade, Custo e Duração.

### Quantidade

Mostra a quantidade total do(s) equipamento(s) ativo(s) (curva azul) e disponíveis (curva laranja). A diferença entre as duas curvas corresponde à quantidade de equipamentos em manutenção corretiva.
A opção mostrar linhad e tendência abre novos campos para construção de uma linha de tendência a partir de uma data selecionada e pela duração escolhida (em semanas).
GETS_App automaticamente busca o melhor modelo de séries temporais (ARIMA, ARIMA com sazonalidade trimestral e Suavização Exponencial) usando como dados de treinamento todos os valores anteriores à data da previsão.

### Custo

Mostra os custos totais mensias (em R$) do(s) equipamento(s) selecionado(s), divididos em custos com materiais (barras verde-escuras) e custos com serviços externos (barras verde-claras).
As barras são interativas, clicar nelas gera um mini-gráfico à esquerda com os custos do mês selecionado ao longo de outros anos.
Os valores já são mostrados corrigidos pela inflação caso a tabela de IPCA tenha sido carregada. Do contrário, são mostrados valores não-corrigidos.

### Duração

Mostra as medianas das durações (em horas) das ordens de serviço (OS) do(s) equipamento(s) selecionado(s) (barras roxas).

## Financiamento

Este projeto foi financiado pelo [CNPq](http://www.cnpq.br/).

## Linceça

MIT License

Copyright (c) 2021 Centro de Engenharia Biomédica (CEB) - Universidade Estadual de Campinas (UNICAMP)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
