--Funções de agregação:

--Encontre a soma total de depósitos para cada cliente

select nome_cliente, sum(saldo_deposito) 
from deposito
group by nome_cliente 

--Encontre a soma total de depósitos para cada cliente 
--e ordene pela ordem descendente dos depósitos

select nome_cliente, sum(saldo_deposito) 
from deposito
group by nome_cliente
order by  sum(saldo_deposito) desc

--Conte quantos depósitos realizou cada cliente

select nome_cliente, count(numero_deposito) 
from deposito
group by nome_cliente

--Conte quantos depósitos realizou cada cliente e ordene 
--pelo ordem descendente da quantidade e depositos

select nome_cliente, count(numero_deposito)
from deposito
group by nome_cliente
order by count(1) desc

--Encontre a soma total de depósitos para cada cliente,
--e também a quantidade de depósitos. Mostre o resultado
--ordenado primeiro pela ordem ascendente da quantidade de depósitos
--e depois pela soma total descendente de depósitos de cada cliente

select nome_cliente, sum(saldo_deposito), count(1) 
from deposito
group by nome_cliente 
order by count(1) asc, sum(saldo_deposito) desc

--Encontre o número de depositantes em cada agência
select nome_agencia, count(nome_cliente)
from deposito
group by nome_agencia 

--Mas a cláusula anterior está errada porque um cliente
--pode fazer mais de um depósito por agencia. Veja:
select nome_agencia, nome_cliente, count(nome_cliente)
from deposito group by nome_agencia , nome_cliente  

--Solução:
select nome_agencia, count( distinct nome_cliente)
from deposito
group by nome_agencia 

--Encontre o saldo médio de depósitos de cada agência

select nome_agencia, avg(saldo_deposito)
from 
group by nome_agencia

--Encontre o saldo médio de depósitos de cada agência
--mas mostre apenas as agencias e saldo médio que forem
--maiores do que R$ 1.200,00

select nome_agencia, avg(saldo_deposito)
from deposito
group by nome_agencia
having avg(saldo_deposito) > 1200

--Selecione o valor do maior depósito

select max(saldo_deposito)
from deposito

--Selecione o valor do maior, da média e do menor depósito

select max(saldo_deposito), avg(saldo_deposito), min(saldo_deposito)
from deposito

--Selecione o valor do maior, da média 
--e do menor depósito, todos por agencia

select nome_agencia, max(saldo_deposito), 
avg(saldo_deposito), min(saldo_deposito)
from deposito
group by nome_agencia 


--Selecione o nome do cliente que fez o maior deposito

select nome_cliente, saldo_deposito
from deposito
where saldo_deposito = (select max(saldo_deposito) from deposito)


