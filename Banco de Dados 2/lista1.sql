--01-Nomes das Agências com depósitos (nome pode aparecer repetido)

SELECT nome_agencia from agencia a  ;

--02-Nomes das Agências com depósitos (nome sem repetição)

SELECT DISTINCT nome_agencia  FROM deposito;

--03-Nomes de Clientes com depósitos e empréstimos ao mesmo tempo;

select DISTINCT nome_cliente  FROM deposito d  
intersect 
SELECT distinct nome_cliente  FROM emprestimo e 

--04-Nomes de Clientes com depósitos e empréstimos ao mesmo tempo na agência PUC;

SELECT DISTINCT nome_cliente FROM deposito d  WHERE nome_agencia= 'PUC' 
intersect 
SELECT DISTINCT nome_cliente FROM emprestimo WHERE nome_agencia = 'PUC'

--Alternativa2 para incluir a condição uma única vez
SELECT DISTINCT nome_cliente FROM  
	(	SELECT DISTINCT nome_cliente, nome_agencia FROM deposito d 
		intersect 
		select DISTINCT nome_cliente, nome_agencia FROM emprestimo
	) AS relatorio
WHERE relatorio.nome_agencia = 'PUC'

--Alternativa3 para usar outro operador (IN)
SELECT DISTINCT nome_cliente FROM deposito WHERE nome_agencia= 'PUC'
AND nome_cliente IN (SELECT DISTINCT nome_cliente FROM emprestimo WHERE nome_agencia='PUC')

--05-Nomes de Clientes com depósitos, mas sem empréstimos na agência PUC;

SELECT nome_cliente FROM deposito WHERE nome_agencia ='PUC'  
except 
SELECT nome_cliente from emprestimo e  WHERE nome_agencia='PUC'

SELECT DISTINCT nome_cliente from deposito WHERE nome_agencia='PUC' 
AND nome_cliente NOT IN (SELECT DISTINCT nome_cliente  FROM emprestimo WHERE nome_agencia='PUC');

--06-Clientes que possuem depósitos ou empréstimos na agencia da PUC

SELECT DISTINCT nome_cliente from deposito d where nome_agencia ='PUC'
UNION
SELECT DISTINCT nome_cliente FROM emprestimo WHERE nome_agencia='PUC'

--07-Nomes de Clientes de Uberlândia

SELECT nome_cliente
FROM Cliente
WHERE cidade_cliente = 'Uberlândia'

--08-Nomes de clientes que tem 'Santos' no nome

SELECT nome_cliente from cliente c 
WHERE nome_cliente LIKE '%Santos%'

--09-Nomes de clientes que tem terminam com 'Souza' ou 'Sousa'

SELECT nome_cliente
FROM cliente
WHERE nome_cliente like '%Sou_a';

--10-Total de depósitos para cada nome de cliente

SELECT nome_cliente, sum(1)
FROM deposito GROUP BY nome_cliente;

--11-Nomes de clientes e depósitos que estão entre 
--R$ 3.000,00 e R$ 4.000,00

SELECT nome_cliente, saldo_deposito
FROM deposito 
WHERE saldo_deposito >= 3000 
AND  saldo_deposito <= 4000

SELECT nome_cliente, saldo_deposito
FROM deposito 
WHERE saldo_deposito BETWEEN 3000 and 4000

--12-Nomes de clientes e a soma de depósitos de cada nome, 
--quando a soma for maior que R$ 5.000,00

SELECT nome_cliente, sum(saldo_deposito)
FROM deposito GROUP BY nome_cliente
HAVING sum(saldo_deposito) > 5000

--13-Nomes de clientes e a soma de depósitos de cada nome,
--quando a soma estiver entre R$ 1.000,00 e R$ 4.000,00,
--em ordem pela soma

SELECT nome_cliente, sum(saldo_deposito)
FROM deposito group by nome_cliente 
HAVING sum(saldo_deposito) BETWEEN 1000 AND 4000
ORDER BY sum(saldo_deposito)


--14-Nomes de clientes e a soma de depósitos de cada nome,
--quando a soma estiver maior do que a média de depósitos,
--em ordem pela soma

SELECT nome_cliente, sum(saldo_deposito)
FROM deposito GROUP BY nome_cliente
HAVING sum(saldo_deposito) > avg(saldo_deposito)
ORDER BY sum(saldo_deposito)

--15-Faça uma listagem da soma de depósitos feitos
--por cada cliente em cada agência. Ordene o resultado
--pelo nome do cliente e depois pelo nome da agência.

SELECT nome_agencia, nome_cliente, sum(saldo_deposito)
FROM deposito 
GROUP BY nome_cliente, nome_agencia 
ORDER BY nome_cliente, nome_agencia

--16- Selecione os nomes dos clientes e a soma de depósitos
--feitos por eles em cada agência que foram maiores que todos
--os depósitos efetuados na agência 'Pampulha'.

--Conjunto1:
SELECT nome_cliente, nome_agencia, sum(saldo_deposito) 
FROM deposito GROUP BY nome_cliente, nome_agencia 

--Conjunto2: 
SELECT sum(saldo_deposito) FROM deposito 
WHERE nome_agencia ='Pampulha' GROUP BY nome_agencia

--Conjunto1 HAVING sum > ALL Conjunto2
SELECT nome_cliente, nome_agencia, sum(saldo_deposito) 
FROM deposito GROUP BY nome_cliente, nome_agencia 
HAVING sum(saldo_deposito) > ALL
(SELECT sum(saldo_deposito) FROM deposito 
WHERE nome_agencia ='Pampulha' GROUP BY nome_agencia);
