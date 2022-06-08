--A DEFINIÇÃO DA FUNÇÃO GETLIQUIDO
CREATE OR REPLACE FUNCTION getliquido(p_numero_conta integer, p_nome_agencia character varying, p_nome_cliente character varying)
  RETURNS float AS
$BODY$
DECLARE
    saldo_liquido float;
    soma_deposito float;
   
    cursor_relatorio CURSOR FOR SELECT SUM(D.SALDO_DEPOSITO) AS TOTAL_DEP, 
		SUM(E.VALOR_EMPRESTIMO) AS TOTAL_EMP
		FROM CONTA AS C  LEFT OUTER JOIN 
		(EMPRESTIMO AS E NATURAL  DEPOSITO AS D)
	WHERE C.NOME_CLIENTE=p_nome_cliente AND C.NOME_AGENCIA=p_nome_agencia AND C.NUMERO_CONTA=p_numero_conta
	GROUP BY C.NOME_CLIENTE, C.NOME_AGENCIA, C.NUMERO_CONTA;
BEGIN
    
    OPEN cursor_relatorio;
            
        FETCH cursor_relatorio INTO soma_deposito, soma_emprestimo;
        --RAISE NOTICE 'O valor de DEP é % e EMP é %', soma_deposito, soma_emprestimo;
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
  OWNER TO aluno;









--DEFINININDO A FUNÇÃO A SER ACIONADA POR TRIGGER (GATILHO)
CREATE OR REPLACE FUNCTION Atualizar_Ativos_F1()
  RETURNS trigger AS
$BODY$
DECLARE
	l_ativo_agencia float;
	l_nome_agencia character varying;	
	cursor_relatorio CURSOR FOR SELECT NOME_AGENCIA, SUM(SALDO_CONTA) 
		FROM CONTA GROUP BY ;
BEGIN
   RAISE NOTICE 'FUNÇÃO QUE NÃO RECEBE ARGUMENTOS';
   OPEN cursor_relatorio;
	LOOP
		FETCH cursor_relatorio INTO l_ativo_agencia;
		IF FOUND THEN
			IF l_ativo_agencia IS NULL THEN l_ativo_agencia=0; END IF;
			UPDATE AGENCIA SET ATIVO_AGENCIA = l_ativo_agencia where NOME_AGENCIA = l_nome_agencia;
		END IF;
		IF NOT FOUND THEN EXIT; END IF;
	END LOOP;
   CLOSE cursor_relatorio;
   RETURN NULL;
END
$BODY$
  LANGUAGE plpgsql VOLATILE COST 100;
ALTER FUNCTION Atualizar_Ativos_F1() OWNER TO postgres;









--CRIANDO O GATILHO

-- DROP TRIGGER trigger_atualiza_ativos_f2 ON conta;

CREATE TRIGGER TRIGGER_Atualiza_Ativos_F1 
AFTER ON CONTA 
FOR EACH STATEMENT EXECUTE PROCEDURE Atualizar_Ativos_F1();





























--INICIALMENTE OS ATIVOS DA AGENCIA ESTÃO COM VALOR ZERO

UPDATE AGENCIA SET ATIVO_AGENCIA = 0;

SELECT * FROM AGENCIA

SELECT * FROM CONTA




















--AO ATUALIZARMOS OS SALDOS DAS CONTAS, DISPARAMOS A ATUALIZAÇÃO DOS ATIVOS DAS AGÊNCIAS
UPDATE CONTA SET SALDO_CONTA=GETLIQUIDO(NUMERO_CONTA, NOME_AGENCIA, NOME_CLIENTE);



























--DEFINININDO A NOVA FUNÇÃO A SER ACIONADA POR TRIGGER (GATILHO)
CREATE OR REPLACE FUNCTION Atualizar_Ativos_F2()
  RETURNS trigger AS
$BODY$
DECLARE
	l_ativo_agencia float;
	l_nome_agencia character varying;	
	cursor_relatorio CURSOR FOR SELECT NOME_AGENCIA, SUM(SALDO_CONTA) 
		FROM CONTA ;
BEGIN
	RAISE NOTICE 'FUNÇÃO QUE RECEBE ARGUMENTO %', TG_ARGV[0];
   OPEN cursor_relatorio;
	LOOP
		FETCH cursor_relatorio INTO l_nome_agencia;
		IF  THEN
			IF l_ativo_agencia IS NULL THEN l_ativo_agencia=0; END IF;
			UPDATE SET ATIVO_AGENCIA = l_ativo_agencia where NOME_AGENCIA = l_nome_agencia;
		END IF;
		IF NOT FOUND THEN EXIT; END IF;
	END LOOP;
   CLOSE cursor_relatorio;
   RETURN NULL;
END
$BODY$
  LANGUAGE plpgsql VOLATILE COST 100;
ALTER FUNCTION Atualizar_Ativos_F2() OWNER TO postgres;





















--CRIANDO UMA VARIAÇÃO DO GATILHO
-- DROP TRIGGER trigger_atualiza_ativos_f1 ON conta;
CREATE TRIGGER TRIGGER_Atualiza_Ativos_F2
AFTER UPDATE 
FOR EACH EXECUTE PROCEDURE Atualizar_Ativos_F2('CONSTANTE');

























--INICIALMENTE OS ATIVOS DA AGENCIA ESTÃO COM VALOR ZERO
UPDATE AGENCIA SET ATIVO_AGENCIA = 0;

SELECT * FROM AGENCIA

SELECT * FROM CONTA































--AO ATUALIZARMOS OS SALDOS DAS CONTAS, DISPARAMOS A ATUALIZAÇÃO DOS ATIVOS DAS AGÊNCIAS
UPDATE CONTA SET SALDO_CONTA=GETLIQUIDO(NUMERO_CONTA, NOME_AGENCIA, NOME_CLIENTE);
