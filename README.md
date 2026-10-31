# Transaction Settlement Orchestrator

O **Transaction Settlement Orchestrator** é um painel corporativo focado em conciliação financeira assíncrona, inteligência de dados e segurança transacional. O sistema foi desenvolvido para gerenciar e monitorar grandes fluxos de operações de venda em canais de liquidação rápida como PIX e TED, integrando regras rígidas de compliance e prevenção a fraudes em tempo real.

---

## 🛠️ Funcionalidades e Regras do Motor de Risco

O sistema conta com um motor de risco avançado integrado diretamente ao fluxo de dados, aplicando travas de segurança automáticas antes da liquidação final e garantindo propriedades ACID na memória operacional:

*   **Validação de Consistência Estrutural:** Identifica e rejeita imediatamente dados nulos, CPFs em branco ou valores inconsistentes (menores ou iguais a zero).
*   **Regra 1 — Limite Operacional por Transação:** Bloqueio automático de segurança para qualquer transação unitária que exceda o valor de **R$ 10.000,00**.
*   **Regra 2 — Anti-Spam e Repetição Rápida (Travas de Concorrência):** Mecanismo de defesa que impede ataques de repetição rápida ou transações duplicadas feitas pelo mesmo CPF e com o mesmo valor em um intervalo menor que **60 segundos**.
*   **Regra 3 — Trava de Risco Noturno:** Compliance de segurança bancária que restringe operações de alto valor realizadas entre **22:00 e 06:00**, limitando o teto operacional para o máximo de **R$ 1.000,00** por transação durante a madrugada.
*   **Auditoria de Logs em Tempo Real:** Sistema estruturado de monitoramento com sinalização visual instantânea, separando conciliações aprovadas e tentativas fraudulentas bloqueadas.

---

## 🎨 Design e Interface

A aplicação adota uma **paleta de cores corporativa neutra**, focando na seriedade, usabilidade e leitura rápida de métricas de alta gerência (Faturamento Liquidado, Sucessos e Impedimentos):
*   **Fundo e Estrutura:** Tons neutros e limpos (`#F9F8F6` e `#FFFFFF`), garantindo excelente contraste tanto em ambientes claros quanto em dispositivos configurados no Modo Escuro.
*   **Métricas de Risco:** Indicadores e bordas funcionais utilizando tons sóbrios de verde (`#6B8E23`) para operações legítimas e vermelho (`#CD5C5C`) para sinalizar fraudes e rejeições.

---

## 💻 Tecnologias Utilizadas

*   **HTML5** (Estruturação semântica da aplicação)
*   **CSS3** (Estilização responsiva e componentes modulares inline)
*   **JavaScript (Vanilla JS)** (Lógica do motor de risco, manipulação otimizada do DOM e processamento assíncrono em memória)

---

## 🚀 Como Executar o Projeto

1. Clone o repositório para o seu ambiente local:
   ```bash
   git clone https://github.com
   ```
2. Abra o arquivo `index.html` em qualquer navegador ou acesse diretamente através do link público do ambiente:
   *   [Transaction Settlement Orchestrator no GitHub Pages](https://github.io)
