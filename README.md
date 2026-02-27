# omega_calendar_project
A high-performance production calendar engine for Python. 
Seamlessly syncs Civil and Fiscal timeframes with O(1) complexity and priority-based extra working days override.⚙️ Production Calendar OmegaO motor definitivo para gestão de janelas de produção e calendários fiscais.Diferente de bibliotecas de calendário convencionais, a Production Calendar Omega foi desenhada para ambientes industriais e ERPs onde o "mês de produção" não coincide com o calendário civil. Graças à lógica de segurança dinâmica, ela aceita qualquer dia de corte (1-31) e se ajusta automaticamente para meses curtos (como Fevereiro).🚀 Destaques (DNA Ômega)Cálculo de Período Fiscal: Conversão instantânea de datas civis para meses de produção com start_day dinâmico.Resiliência de Calendário: Suporte a cortes no dia 29, 30 ou 31 com normalização automática para o último dia do mês (Anti-Crash).Precedência de Operação: Suporte a feriados e Dias Extras (horas extras ou feriados trabalhados com prioridade absoluta).Arquitetura Multi-Contrato: Instancie múltiplos calendários com regras e feriados distintos no mesmo processo.Performance O(1): Busca de datas otimizada via Hashing Sets.📦 InstalaçãoBashpip install production-calendar-omega
🛠️ Como Usar1. Configuração Básica e Período FiscalNa versão 3.0.0, o start_day é um argumento obrigatório para garantir clareza entre diferentes contratos.Pythonfrom datetime import date
from production_calendar import ProductionCalendar

# Inicializar o motor (opcionalmente com feriados)
motor = ProductionCalendar(holidays=[date(2024, 12, 25)])

# Determinar o período fiscal (Ex: Corte todo dia 26)
periodo = motor.get_fiscal_period(date(2024, 2, 27), start_day=26)

print(f"Label: {periodo.label}")         # Mar/24 Fiscal
print(f"Início: {periodo.start_date}")   # 2024-01-26
print(f"Fim: {periodo.end_date}")         # 2024-02-25
print(f"Duração: {periodo.total_days}")   # 31 dias
2. Dias Extras (Override de Produção)Se a fábrica vai rodar num feriado ou domingo, use o extra_working_days para anular a regra padrão.Python# O Natal será dia de produção normal neste contrato
motor = ProductionCalendar(extra_working_days=[date(2024, 12, 25)])

# Retornará True mesmo sendo feriado/domingo
print(motor.is_working_day(date(2024, 12, 25))) 
3. Gerando um Roadmap de ContratoGere rapidamente os meses fiscais para um período estendido:Python# Gerar 6 meses de calendário a partir de hoje com corte dia 16
roadmap = motor.generate_contract_calendar(date.today(), months=6, start_day=16)

for label, p in roadmap.items():
    print(f"{label}: {p.start_date} até {p.end_date}")
📐 Estrutura de Dados FiscalPeriodO retorno de get_fiscal_period é uma instância imutável:AtributoTipoDescriçãomonthintMês fiscal resultante (1-12)yearintAno fiscal resultantestart_datedateData civil de início da janelaend_datedateData civil de término da janelalabelstrIdentificador amigável (ex: "Jan/24 Fiscal")total_daysintContagem de dias corridos na janela⚖️ LicençaDistribuído sob a licença MIT. Veja LICENSE para mais informações.
