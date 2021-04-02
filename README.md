# GETS_App: Aplicação Web para Análise Temporal de Dados do GETS (with mybinder)
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

1. 
1. Carregue/copie as tabelas do GETS (imagens de como obtê-las são mostradas no final desta página) na pasta local escolhida no passo 4 da instalação;
2. Clique no botão "Carregar Tabelas". Se alguma tabela estiver faltando, você será informado com uma mensagem abaixo do botão.
3. Selecione um ou mais equipamentos pelo campo "Equipamento";
4. Selecione uma data inicial de análise pelo campo "Data Inicial";
5. Selecione uma data final de análise pelo campo "Dara Final";
6. Pronto! O gráfico deve ser apresentado no centro da tela.

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

## Licença de Software

This program is a free software. You can redistribute and/or modify it under the terms of the [GNU General Public License v3.0](https://github.com/leoelias-unicamp/modals/blob/master/LICENSE) as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
