# Marketplace_Distribuido

<p align="center">

<h4 align="center" > Universidade Estadual de Feira de Santana </h4>
<h4 align="center" >  TEC502 - Concorrência e Conectividade  </h4>
</p>


- Esse projeto foi desenvolvido por: 
    
  	- [Lucas Gabriel da Silva Lima Reis](https://github.com/lucasxgb), 
	- [Silas Silva Costa](https://github.com/silas-silva)
	
- Avaliado por: 
	- [Antonio Augusto Teixeira Ribeiro Coutinho](https://linkedin.com/in/antonio-augusto-teixeira-ribeiro-coutinho-03a3217)

## Introdução

- Visando expandir seus negócios a loja Saldão dos Computadores está utilizando diferentes marketplaces em sua interface. Porém o grande problema enfrentado pela mesma é que por cada marketplace utilizado possuir a própria base de dados, acaba gerando problemas de controles de estoque, uma vez que poderão ser vendidos produtos a mais que os disponíveis no estoque.
- Para resolução desse conflito, foi criado o consórcio de marketplaces que facilitaria o controle de estoque. Foi solicitado a uma equipe especializada em sistemas distribuídos para implementação desta solução, utilizando implementação baseada em sistemas distribuídos, baseando-se em requisitos pré-estabelecidos. como: cadastro de produtos em apenas um marketplace, transações
atômicas sobre os itens do carrinhos, controle de vendas, entre outros.
- Este relatório tem como objetivo principal mostrar como foi o processo de desenvolvimento do sistema, expondo principalmente o algoritmo de sistemas distribuídos que foi utilizado na
tentativa de resolver o problema apresentado, essas informações serão apresentadas na seção



## Para executar o sistema:
- Torna-se necessário:
    - `Instalar fastapi`: pip install fastapi
    - `Instalar uvicorn`: pip install uvicorn
    - `Instalar request`: pip install requests

 - Para ligar os servidores: 
    - `mark01`: python -m uvicorn mark01:app --reload --port=4000
    - `mark02`: python -m uvicorn mark01:app --reload --port=5000
    - `mark02`: python -m uvicorn mark01:app --reload --port=8000
# 

- O sistema é constituído pelas telas e funcionalidades:
	![Listagem vazia](https://github.com/lucasxgb/Marketplace_Distribuido/blob/main/View/images/tela1vazia.png)
	- `Listagem de informações na tela`: Todas os itens do marketplace são listados quando a tela está vazia e é clicado no botão de busca.


	![Listagem de item específico](https://github.com/lucasxgb/Marketplace_Distribuido/blob/main/View/images/tela1.png)
	- `Listagem de informações especifica`: Todas os itens do marketplace que tem nome semelhante ao pesquisado são exibidos na tela.


	![Produto específico](https://github.com/lucasxgb/Marketplace_Distribuido/blob/main/View/images/tela2.png)
	- `Ver produto`: Ao clicar em um produto você é redirecionado para tela do produto específico, onde pode inserir o mesmo no carrinho de compras passando seu nome e clicando no botão adicionar carrinho.


	![Cadastro de itens](https://github.com/lucasxgb/Marketplace_Distribuido/blob/main/View/images/telaAdicionar.png)
	- `Cadastro`: Ao clicar no sinal de + no menu você pode ir para tela de cadastro de itens no banco de dados em um determinado marketplace, passando suas informações.


	![Carrinho](https://github.com/lucasxgb/Marketplace_Distribuido/blob/main/View/images/tela3.png)
	- `Carrinho`: Carrinho de compras onde você passa o nome do usuário e pode finalizar a sua compra, onde é retirado os dados do seu carrinho no banco de dados, e reduzida a quantidade de itens no carrinho.



## Resultados e Conclusões:
O desenvolvimento do código foi um sucesso na maior parte do problema, pois, conseguimos implementar toda a parte de cliente (frontend), e boa parte do servidor, o sistema foi terminado permitindo que os clientes realizassem todas as funcionalidades que poderiamos abordar por meio da API, que permitiu realizar
o controle e o tratamento de dados, visto que para realizar uma compra os servidores deveriam se comunicar entre si, e também as ações que eram executadas em servidor único, não precisando
de comunicação entre os demais.

Tivemos problema com a implementação do algoritmo de eleição, onde conseguimos implementar a lógica do algoritmo de eleição para a escolha do coordenador, porém por questões técnicas, tivemos problemas ao fazer a comunicação na parte do algoritmo de eleição, uma vez que os servidores não conseguiam enviar mensagens entre si. O problema encontrado foram nas requisições.
