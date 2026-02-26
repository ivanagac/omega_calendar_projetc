# omega_calendar_projetc
A high-performance production calendar engine for Python. Seamlessly syncs Civil and Fiscal timeframes (26-25) with O(1) complexity and priority-based extra working days override.


# ⚙️ Production Calendar Omega

[![PyPI version](https://img.shields.io/badge/pypi-v2.0.0-blue.svg)](https://pypi.org/project/production-calendar-omega/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)

**O motor definitivo para gestão de janelas de produção e calendários fiscais.**

Diferente de bibliotecas de calendário convencionais, a *Production Calendar Omega* foi desenhada para ambientes industriais e ERPs onde o "mês de produção" não coincide com o calendário civil. Se o teu Março começa no dia 26 de Fevereiro, esta é a tua biblioteca.

---

## 🚀 Destaques (DNA Ômega)

- **Cálculo de Período Fiscal:** Conversão instantânea de datas civis para meses de produção (ex: janelas de 26 a 25).
- **Precedência de Operação:** Suporte a feriados e **Dias Extras** (horas extras ou feriados trabalhados com prioridade absoluta).
- **Arquitetura Multi-Contrato:** Instancie múltiplos calendários com regras, feriados e dias de corte distintos no mesmo processo.
- **Performance O(1):** Busca de datas otimizada via Hashing Sets.
- **Imutabilidade:** Resultados entregues em `Frozen Dataclasses` para evitar mutações acidentais no pipeline.

## 📦 Instalação

```bash
pip install production-calendar-omega
🛠️ Como Usar
1. Configuração Básica
Ideal para contratos padrão com janelas de fechamento fixas.

Python
from datetime import date
from production_calendar import ProductionCalendar

# Definir feriados do contrato
feriados = [date(2024, 12, 25)]

# Inicializar o motor
motor = ProductionCalendar(holidays=feriados)

# Descobrir a qual mês de produção uma data pertence (Corte dia 26)
periodo = motor.get_fiscal_period(date(2024, 2, 27), start_day=26)

print(f"Label: {periodo.label}")         # Mar/24 Fiscal
print(f"Início: {periodo.start_date}")   # 2024-01-26
print(f"Fim: {periodo.end_date}")         # 2024-02-25
2. Dias Extras (Override de Produção)
Se a fábrica vai rodar num feriado ou domingo, use o extra_working_days.

Python
dias_trabalhados = [date(2024, 12, 25)] # Sim, vamos rodar no Natal!
motor = ProductionCalendar(extra_working_days=dias_trabalhados)

# No Natal, is_working_day retornará True devido à precedência de Dias Extras.
print(motor.is_working_day(date(2024, 12, 25))) # True
3. Contagem de Dias Úteis
Calcule a capacidade produtiva de uma janela fiscal ignorando feriados e fins de semana (a menos que sejam Dias Extras).

Python
periodo = motor.get_fiscal_period(date.today())
dias_uteis = motor.count_working_days(periodo.start_date, periodo.end_date, rule='SEG_SEX')
print(f"Dias produtivos na janela: {dias_uteis}")
📐 Estrutura de Dados FiscalPeriod
O retorno de get_fiscal_period é uma instância de FiscalPeriod:

Atributo	Tipo	Descrição
month	int	Mês fiscal resultante
year	int	Ano fiscal resultante
start_date	date	Data civil de início da janela
end_date	date	Data civil de término da janela
label	str	Identificador formatado (ex: "Jan/24 Fiscal")
total_days	int	Contagem total de dias corridos na janela
⚖️ Licença
Distribuído sob a licença MIT. Veja LICENSE para mais informações.
