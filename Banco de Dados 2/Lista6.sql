update conta set saldo_conta=0;
--PRIMEIRO CONFERIMOS COMO EST· A SITUAÁ„O DAS CONTAS
select * from conta;

--EXECUTAMOS OUTRA CONFERENCIA PARA VER COMO SER„O OS RETORNOS DA PESQUISA
select getliquido(numero_conta, nome_agencia) from conta

--DEPOIS ATUALIZAMOS ...
update conta set saldo_conta=getliquido(numero_conta, nome_cliente);

--... E CONFERINDO DE NOVO:

select * from conta where nome_agencia = 'PUC';

--A DEFINI«√O DA FUN«√O GETLIQUIDO

CREATE OR REPLACE FUNCTION getliquido(p_numero_conta integer, p_nome_agencia character varying, p_nome_cliente character varying)
  RETURNS float AS
$BODY$
DECLARE
    saldo_liquido float;
    soma_deposito float;
    soma_emprestimo float;
    cursor_relatorio CURSOR FOR SELECT SUM(D.SALDO_DEPOSITO) AS TOTAL_DEP, 
		SUM(E.VALOR_EMPRESTIMO) AS TOTAL_EMP
		FROM CONTA AS C NATURAL left OUTER JOIN 
		(EMPRESTIMO AS E NATURAL full join DEPOSITO AS D)
	WHERE C.NOME_CLIENTE=p_nome_cliente 
	AND C.NOME_AGENCIA=p_nome_agencia 
	AND C.NUMERO_CONTA=p_numero_conta
	GROUP BY C.NOME_CLIENTE, C.NOME_AGENCIA, C.NUMERO_CONTA;
BEGIN
    OPEN cursor_relatorio;
        saldo_liquido=0;    
        FETCH cursor_relatorio INTO soma_deposito, soma_emprestimo;
        --RAISE NOTICE 'O valor de DEP È % e EMP È %', soma_deposito, soma_emprestimo;
        IF FOUND THEN 
	    IF soma_deposito IS NULL then soma_deposito=0; END IF;
	    IF soma_emprestimo IS NULL then soma_emprestimo=0; END IF;
            saldo_liquido = soma_deposito - soma_emprestimo ;
        END IF;
    CLOSE cursor_relatorio;
    RETURN saldo_liquido;
END
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;
ALTER FUNCTION getliquido(integer, character varying, character varying)
  OWNER TO postgres;

 create role postgres