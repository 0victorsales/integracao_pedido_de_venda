## integracao_pedido_ok_omie-FOGO_SELVAGEM 
## Inicialização



O programa é execultado no piperdream com um trigger



## Ferramentas

- Python
- piperdream
- Omie - Sistema de gestão financeira do cliente
- Pedido OK 


## Bibliotecas

1. datetime: Biblioteca integrada do Python para manipulação de datas e horas. Usada para converter formatos de data.
2. requests: Realizar solicitações HTTP, permitindo interações com servidores web, APIs e comunicação na internet.
3. re: Biblioteca integrada do Python usado para trabalhar com expressões regulares.
4. json: Biblioteca integrada do Python usado para converter dados em formato JSON em Python.



## Links importantes

Documentação Pedido Ok - [Pedido Ok API Docs](https://docs.api.pedidook.com.br/)
Documentação Omie - [Omie API Docs](https://developer.omie.com.br/service-list/)

## integracao_pedido_ok_omie-FOGO_SELVAGEM 

## Introdução

Esse projeto tem como objetivo integrar os sistemas Pedido Ok e Omie. Ele faz a inclusão dos pedidos do Pedido Ok no Omie.



## Descrição do ambiente técnico

- Gera pedido de venda no Omie
- Verifica se cliente do pedido já tem cadastro no Omie
- Caso o cliente não tenha cadastro no Omie ele será incluido 

### Descrição do Sistema

O sistema é composto por um backend que realiza chamadas de API no ERP Pedido Ok, possibilitando a geração de pedidos de venda no ERP Omie.

### Carregamento de dados
No início do processo, o código utiliza a biblioteca "datetime" para criar uma variável que obtém a data atual e adiciona dois meses a ela. Essa variável é posteriormente utilizada no momento da geração do pedido no OMIE, preenchendo o campo "data_previsao".

Em seguida, o código realiza chamadas às APIs para obter dados dos clientes do PEDIDO OK, clientes do OMIE, produtos do PEDIDO OK, produtos do OMIE, vendedores do PEDIDO OK, vendedores do OMIE e códigos de pagamento do OMIE. Para cada uma dessas chamadas, o código cria um dicionário para armazenar os dados obtidos. Esses dicionários são utilizados posteriormente para processar e incluir os pedidos no OMIE.

### Verificação da situação do pedido
Na segunda parte do projeto, a função "adc_dados_cliente_dicionario" recebe um JSON contendo os pedidos do sistema PEDIDO OK. Em seguida, verifica se a situação do pedido é "Pendente". Caso o pedido atenda a essa condição, o código inicia o processo de criação de um dicionário que irá selecionar e obter os dados necessários que foram carregados previamente no início do programa. Esses dados, presentes nos dicionários criados, são essenciais para realizar o processo de inclusão dos pedidos no sistema OMIE.

### Verificação do cliente
Na terceira parte, o código realiza uma análise para verificar se o cliente associado ao pedido está cadastrado no sistema OMIE. Utilizando o CNPJ do cliente como parâmetro, o código usa o método get na função "dic_clientes_omie", e tenta obter o "código cliente OMIE" e armazenar esse valor na variável chamada "codigo_cliente_omie". Caso não seja possível obter o valor, a variável receberá o valor "None".

Em seguida, é aplicada uma condição para verificar se o valor da variável "codigo_cliente_omie" é igual a "None". Se essa condição for verdadeira, o código chamará a função "cadastrar_clientes". Essa função tem como objetivo cadastrar o cliente no sistema OMIE, recebendo como parâmetro um dicionário contendo os dados do cliente a ser cadastrado.

### Adiconando dados no dicionário
Na quarta parte, a função "adc_dados_cliente_dicionario" é responsável por adicionar os dados necessários vindos do pedido de venda do sistema PEDIDO OK no dicionário chamado "dicionario_pedido". Em seguida, utilizando a informação "condicao_pagamento" do pedido de venda, a função utiliza um método "get" para obter o código de pagamento do OMIE, chamando a função "descobrir_cod_pagamento".

Após isso, o dicionário é incrementado com os dados dos produtos do OMIE e dos clientes do PEDIDO OK. Posteriormente, esse dicionário é adicionado à lista chamada "lista_dicionario_pedidos", a qual conterá os dados necessários para a inclusão dos pedidos no OMIE, consolidando as informações para o processo de integração.


### Inclusão do pedido no Omie
Na quinta parte, por meio de um loop "for", a função "incluir_pedido" é encarregada de inserir o pedido de venda no OMIE. Essa função recebe como parâmetro um dicionário que contém todos os dados necessários para a geração do pedido de venda. Através dessa operação, o código realiza a integração do pedido no OMIE, utilizando os dados previamente preparados para a inclusão bem-sucedida do pedido de venda.

### Objetivo do sistema
O objetivo desse sistema é promover a integração entre os ERPs Pedido Ok e Omie, possibilitando a geração de pedidos de venda no sistema Omie com base nos pedidos originados do Pedido Ok.

### Requisitos
- Haver pedido de venda com situação "Pendente"
- Cliente está cadastrado no Omie




