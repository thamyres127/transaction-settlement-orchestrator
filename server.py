import json
import time
from datetime import datetime

# ==========================================
# 1. BASE DE DADOS SIMULADA (PERSISTÊNCIA)
# ==========================================
# Estrutura relacional em memória para simular o banco de dados de liquidação
banco_dados = {
    "transacoes_liquidadas": [],
    "tentativas_fraude": []
}

# ==========================================
# 2. MOTOR DE RISCO E CONCILIAÇÃO (BACK-END)
# ==========================================
def processar_liquidacao(transacao_json):
    """
    Processa e liquida transações aplicando regras estritas de risco.
    Retorna o status da operação e a justificativa.
    """
    try:
        dados = json.loads(transacao_json)
    except json.JSONDecodeError:
        return {"status": "REJEITADA", "motivo": "Erro de comunicação: JSON corrompido"}

    # Extração e higienização inicial de dados básicos
    cpf = dados.get("cpf", "").strip()
    valor = dados.get("valor", 0.0)
    tipo = dados.get("tipo", "PIX").upper()
    timestamp = dados.get("timestamp", time.time())

    # Higienização: Bloqueia campos essenciais nulos ou inconsistentes
    if not cpf or valor <= 0:
        registro_erro = {"cpf": cpf, "valor": valor, "tipo": tipo, "timestamp": timestamp, "motivo": "Dados inconsistentes ou nulos"}
        banco_dados["tentativas_fraude"].append(registro_erro)
        return {"status": "REJEITADA", "motivo": "Dados inconsistentes ou nulos"}

    # --- REGRAS DE NEGÓCIO E ANTIFRAUDE ---
    
    # REGRA 1: Limite Operacional por Transação (Prevenção de Perdas Massivas)
    if valor > 10000.00:
        registro_fraude = {"cpf": cpf, "valor": valor, "tipo": tipo, "timestamp": timestamp, "motivo": "Valor acima do limite operacional permitido"}
        banco_dados["tentativas_fraude"].append(registro_fraude)
        return {"status": "REJEITADA", "motivo": "Transação excede o limite operacional de segurança"}

    # REGRA 2: Bloqueio de Repetição Rápida (Anti-Spam / Ataque de Força Bruta de Saldo)
    # Verifica se o mesmo CPF tentou o mesmo valor nos últimos 60 segundos
    for t in banco_dados["transacoes_liquidadas"] + banco_dados["tentativas_fraude"]:
        if t["cpf"] == cpf and t["valor"] == valor:
            tempo_decorrido = timestamp - t["timestamp"]
            if tempo_decorrido < 60:
                registro_fraude = {"cpf": cpf, "valor": valor, "tipo": tipo, "timestamp": timestamp, "motivo": "Multiplas tentativas com mesmo valor em curto intervalo"}
                banco_dados["tentativas_fraude"].append(registro_fraude)
                return {"status": "REJEITADA", "motivo": "Transação bloqueada por repetição rápida suspeita"}

    # REGRA 3: Trava de Segurança de Horário Noturno de Alta Criticidade
    # Restrição estrita de valor máximo para transações entre 22h e 06h
    hora_atual = datetime.fromtimestamp(timestamp).hour
    if (hora_atual >= 22 or hora_atual < 6) and valor > 1000.00:
        registro_fraude = {"cpf": cpf, "valor": valor, "tipo": tipo, "timestamp": timestamp, "motivo": "Transação noturna acima do limite de segurança"}
        banco_dados["tentativas_fraude"].append(registro_fraude)
        return {"status": "REJEITADA", "motivo": "Limite noturno excedido para o horário (Máx: R$ 1000.00)"}

    # SE PASSAR POR TODAS AS TRAVAS: Liquidação Concluída com Sucesso
    registro_sucesso = {
        "id_transacao": f"TX-{int(timestamp)}-{cpf[:3]}",
        "cpf": cpf,
        "valor": valor,
        "tipo": tipo,
        "timestamp": timestamp,
        "data_liquidacao": datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    }
    banco_dados["transacoes_liquidadas"].append(registro_sucesso)
    return {"status": "APROVADA", "motivo": "Liquidação realizada com sucesso e saldo conciliado"}


# ==========================================
# 3. SUÍTE DE TESTES UNITÁRIOS AUTOMATIZADOS
# ==========================================
def executar_testes_sistema():
    """
    Executa testes automatizados para garantir a resiliência matemática e lógica do back-end.
    """
    print("🧪 INICIANDO TESTES AUTOMATIZADOS DO MOTOR DE LIQUIDAÇÃO...\n")
    ts_base = time.time()

    # Cenário 1: Transação Válida Padrão
    tx_valida = json.dumps({"cpf": "12345678901", "valor": 250.50, "tipo": "Pix", "timestamp": ts_base})
    res1 = processar_liquidacao(tx_valida)
    assert res1["status"] == "APROVADA", "Falha no Cenário 1: Deveria aprovar transação normal."
    print("✅ Teste 1: Transação normal aprovada e saldo conciliado com sucesso.")

    # Cenário 2: Bloqueio de Valor Abusivo (Regra 1)
    tx_abusiva = json.dumps({"cpf": "98765432100", "valor": 15000.00, "tipo": "TED", "timestamp": ts_base})
    res2 = processar_liquidacao(tx_abusiva)
    assert res2["status"] == "REJEITADA" and "limite operacional" in res2["motivo"], "Falha no Cenário 2."
    print("✅ Teste 2: Travamento de valor abusivo acima do limite operacional funcionou.")

    # Cenário 3: Bloqueio de Repetição Rápida (Regra 2)
    tx_repetida = json.dumps({"cpf": "12345678901", "valor": 250.50, "tipo": "Pix", "timestamp": ts_base + 10})
    res3 = processar_liquidacao(tx_repetida)
    assert res3["status"] == "REJEITADA" and "repetição" in res3["motivo"], "Falha no Cenário 3."
    print("✅ Teste 3: Proteção contra transações repetidas em curto intervalo validada.")

    # Cenário 4: Limite Noturno (Regra 3)
    # Forçando timestamp para o horário das 23:00h
    ts_noturno = datetime.now().replace(hour=23, minute=0, second=0).timestamp()
    tx_noturna = json.dumps({"cpf": "45678912300", "valor": 1200.00, "tipo": "Pix", "timestamp": ts_noturno})
    res4 = processar_liquidacao(tx_noturna)
    assert res4["status"] == "REJEITADA" and "noturno" in res4["motivo"], "Falha no Cenário 4."
    print("✅ Teste 4: Trava de faturamento noturno de alta criticidade funcionou.")

    print("\n🎉 TODOS OS TESTES PASSARAM COM SUCESSO! MOTOR BLINDADO CONTRA QUEBRAS.")

# Executa os testes automaticamente ao rodar o arquivo
if __name__ == "__main__":
    executar_testes_sistema()
