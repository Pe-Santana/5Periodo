--PRIMEIRO CONFERIMOS COMO ESTá A SITUAçãO DAS CONTAS
select * from emprestimo where nome_agencia = 'PUC';

--EXECUTAMOS OUTRA CONFERENCIA PARA VER COMO SERãO OS RETORNOS DA PESQUISA
select conta.*, update_valor_emprestimo1(numero_conta, nome_agencia, nome_cliente) from conta where nome_agencia = 'PUC';

--A DEFINIÇÃO DA FUNÇÃO update_valor_emprestimo1
CREATE OR REPLACE FUNCTION update_valor_emprestimo1(	p_numero_conta integer, 
							p_nome_agencia character varying, 
							p_nome_cliente character varying
						)
  RETURNS float AS
$BODY$
DECLARE
    l_valor_emprestimo float;
    l_valor_juros float;
    cursor_relatorio CURSOR FOR SELECT VALOR_EMPRESTIMO, JUROS_EMPRESTIMO
	FROM EMPRESTIMO 
	WHERE NOME_CLIENTE=p_nome_cliente 
	AND NOME_AGENCIA=p_nome_agencia 
	AND NUMERO_CONTA=p_numero_conta;
BEGIN

    open cursor_relatorio;
	FETCH cursor_relatorio INTO l_valor_emprestimo, l_valor_juros;
	IF FOUND THEN 
		l_valor_emprestimo = l_valor_emprestimo * (1+(l_valor_juros)/100);
		UPDATE EMPRESTIMO SET VALOR_EMPRESTIMO = l_valor_emprestimo
	where nome_cliente = p_nome_cliente
	and nome_agencia = p_nome_agencia 
	and numero_conta = p_numero_conta;
	END IF;
    CLOSE cursor_relatorio;
    RETURN l_valor_emprestimo;
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION update_valor_emprestimo1(integer, character varying, character varying)
  OWNER TO aluno;

--Lista as quantidades de emprestimos realizados por cada cliente
 
select nome_cliente, count(1) from emprestimo group by nome_cliente order by count(1) desc

--Lista apenas um deles
select * from emprestimo where nome_cliente = 'Reinaldo Pereira da Silva';

--Agora atualiza apenas os valores de empréstimos desta pessoa
update_valor_emprestimo2('Reinaldo Pereira da Silva');

--A DEFINIÇÃO DO PROCEDIMENTO update_valor_emprestimo2
CREATE OR REPLACE FUNCTION update_valor_emprestimo2(	p_nome_cliente character varying )
  RETURNS void as
$BODY$
DECLARE
	l_valor_emprestimo float;
	l_valor_juros float;
	l_numero_emprestimo integer;
    cursor_relatorio CURSOR FOR VALOR_EMPRESTIMO, JUROS_EMPRESTIMO, NUMERO_EMPRESTIMO
				FROM EMPRESTIMO 
				WHERE NOME_CLIENTE=p_nome_cliente;
BEGIN

   OPEN cursor_relatorio;
	LOOP
		FETCH cursor_relatorio INTO l_valor_emprestimo, l_valor_juros, l_numero_emprestimo;
		IF FOUND THEN 
			UPDATE EMPRESTIMO SET VALOR_EMPRESTIMO = l_valor_emprestimo WHERE 
			NUMERO_EMPRESTIMO=l_numero_emprestimo;
		END IF;
		IF not FOUND THEN EXIT;
		END IF;
	END LOOP;
   CLOSE cursor_relatorio;
   RETURN;
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION update_valor_emprestimo2(character varying)
  OWNER TO postgres;
