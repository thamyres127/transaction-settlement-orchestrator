let faturamentoTotal = 0.0;
let transacoesAprovadas = 0;
let fraudesBloqueadas = 0;
let historicoTransacoes = [];

const form = document.getElementById('form-transacao');
const inputCpf = document.getElementById('input-cpf');
const inputValor = document.getElementById('input-valor');
const inputTipo = document.getElementById('input-tipo');

const metricFaturamento = document.getElementById('metric-faturamento');
const metricAprovadas = document.getElementById('metric-aprovadas');
const metricFraudes = document.getElementById('metric-fraudes');
const painelLogs = document.getElementById('painel-logs');
const logVazio = document.getElementById('log-vazio');

form.addEventListener('submit', function(e) {
    e.preventDefault();

    const cpfInformado = inputCpf.value.trim();
    const valorInformado = parseFloat(inputValor.value);
    const tipoInformado = inputTipo.value;
    const timestampAtual = Date.now() / 1000;

    if (!cpfInformado || isNaN(valorInformado) || valorInformado <= 0) {
        adicionarLog('REJEITADA', 'Dados inconsistentes ou nulos', cpfInformado, valorInformado, tipoInformado);
        incrementarFraude();
        return;
    }

    // REGRA 1: Limite Operacional por Transação [explicit_memory_claims]
    if (valorInformado > 10000.00) {
        adicionarLog('REJEITADA', 'Transação excede o limite operacional de segurança', cpfInformado, valorInformado, tipoInformado);
        incrementarFraude();
        return;
    }

    // REGRA 2: Bloqueio de Repetição Rápida [explicit_memory_claims]
    const tentativaDuplicada = historicoTransacoes.find(function(tx) {
        return tx.cpf === cpfInformado && 
               tx.valor === valorInformado && 
               (timestampAtual - tx.timestamp) < 60;
    });
    if (tentativaDuplicada) {
        adicionarLog('REJEITADA', 'Transação bloqueada por repetição rápida suspeita', cpfInformado, valorInformado, tipoInformado);
        incrementarFraude();
        return;
    }

    // REGRA 3: Trava de Horário Noturno [explicit_memory_claims]
    const horaAtual = new Date().getHours();
    if ((horaAtual >= 22 || horaAtual < 6) && valorInformado > 1000.00) {
        adicionarLog('REJEITADA', 'Limite noturno excedido para o horário (Máx: R$ 1000.00)', cpfInformado, valorInformado, tipoInformado);
        incrementarFraude();
        return;
    }

    // LIQUIDAÇÃO CONCLUÍDA COM SUCESSO [explicit_memory_claims]
    const idGerado = 'TX-' + Math.floor(timestampAtual) + '-' + cpfInformado.substring(0, 3);
    
    historicoTransacoes.unshift({
        cpf: cpfInformado,
        valor: valorInformado,
        timestamp: timestampAtual
    });

    transacoesAprovadas++;
    faturamentoTotal += valorInformado;
    
    metricAprovadas.textContent = transacoesAprovadas;
    metricFaturamento.textContent = 'R$ ' + faturamentoTotal.toFixed(2);

    adicionarLog('APROVADA', 'Liquidação realizada com sucesso e saldo conciliado', cpfInformado, valorInformado, tipoInformado, idGerado);

    inputCpf.value = '';
    inputValor.value = '';
});

function incrementarFraude() {
    fraudesBloqueadas++;
    metricFraudes.textContent = fraudesBloqueadas;
}

function adicionarLog(status, motivo, cpf, valor, tipo, id = '') {
    if (logVazio) {
        logVazio.style.display = 'none';
    }

    const logId = id ? id : 'ERR-' + Date.now();
    const corBorda = status === 'APROVADA' ? '#6B8E23' : '#CD5C5C';
    const corTextoMotivo = status === 'APROVADA' ? '#6B8E23' : '#CD5C5C';

    const elementoLog = document.createElement('div');
    elementoLog.className = 'log-item';
    elementoLog.style.borderLeft = '5px solid ' + corBorda;

    elementoLog.innerHTML = 
        '<strong>[' + status + ']</strong> ' + logId + '<br />' +
        '<span style="color: #666;">CPF: ' + cpf + ' | Valor: R$ ' + valor.toFixed(2) + ' | Canal: ' + tipo + '</span><br />' +
        '<small style="color: ' + corTextoMotivo + '; font-weight: bold;">Motivo: ' + motivo + '</small>';

    painelLogs.insertBefore(elementoLog, painelLogs.firstChild);
}
