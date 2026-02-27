"""
⚙️ PRODUCTION CALENDAR ENGINE v2.0 - OMEGA EDITION
==============================================================================
Arquiteta: Ivana Cruz(Exclusivo para a Eternidade)
Status: Blindado. Tipado. Implacável.
==============================================================================
"""

from datetime import date, timedelta
from typing import Iterable, Set, Tuple, Dict, List, Optional
from dataclasses import dataclass

@dataclass(frozen=True)
class FiscalPeriod:
    month: int
    year: int
    start_date: date
    end_date: date
    label: str

    @property
    def total_days(self) -> int:
        """Propriedade conveniente para saber o tamanho exato da janela."""
        return (self.end_date - self.start_date).days + 1


class ProductionCalendar:
    """
    Motor definitivo para conversão de Tempo Civil em Tempo de Produção.
    """
    
    MONTH_NAMES = (
        'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
        'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    )

    def __init__(
        self, 
        holidays: Iterable[date] = None, 
        extra_working_days: Iterable[date] = None
    ):
        # Feriados e Dias Extras convertidos para Set no init. Busca O(1).
        self.holidays: Set[date] = set(holidays) if holidays else set()
        self.extra_working_days: Set[date] = set(extra_working_days) if extra_working_days else set()

    def get_fiscal_period(self, reference_date: date, start_day: int) -> FiscalPeriod:
        """
        Determina o período fiscal de uma data com base no dia de corte (start_day).
        """
        if not (1 <= start_day <= 31):
            raise ValueError(f"⚠️ start_day={start_day} é insano. Use entre 1 e 28.")

        # Lógica de deslocamento (Shift)
        if reference_date.day >= start_day:
            fiscal_month = (reference_date.month % 12) + 1
            fiscal_year = reference_date.year + (1 if reference_date.month == 12 else 0)
        else:
            fiscal_month = reference_date.month
            fiscal_year = reference_date.year

        # Calcula o início: start_day do mês ANTERIOR ao fiscal
        prev_month = 12 if fiscal_month == 1 else fiscal_month - 1
        prev_year = fiscal_year - 1 if fiscal_month == 1 else fiscal_year
        start_dt = date(prev_year, prev_month, start_day)
        
        # Calcula o fim: dia imediatamente anterior ao start_day do mês fiscal atual
        next_cut_dt = date(fiscal_year, fiscal_month, start_day)
        end_dt = next_cut_dt - timedelta(days=1)
        
        label = f"{self.MONTH_NAMES[fiscal_month-1][:3]}/{str(fiscal_year)[2:]} Fiscal"
        
        return FiscalPeriod(
            month=fiscal_month, 
            year=fiscal_year, 
            start_date=start_dt, 
            end_date=end_dt, 
            label=label
        )

    def is_working_day(self, target_date: date, rule: str = 'SEG_SEX') -> bool:
        """
        Checagem cirúrgica de dia útil com suporte a dias extras (horas extras/feriado trabalhado).
        """
        # Regra de Ouro: Dia Extra explicitamente trabalhado tem precedência absoluta.
        if target_date in self.extra_working_days:
            return True

        # Feriados têm precedência sobre a regra de dias da semana.
        if target_date in self.holidays:
            return False
            
        weekday = target_date.weekday() # 0=Segunda, 6=Domingo
        
        if rule == 'SEG_SEX':
            return weekday <= 4
        elif rule == 'SEG_SAB':
            return weekday <= 5
        elif rule == 'TODOS':
            return True
            
        raise ValueError(f"⚠️ Regra desconhecida: {rule}.")

    def count_working_days(self, start_date: date, end_date: date, rule: str = 'SEG_SEX') -> int:
        """
        Contagem otimizada de dias úteis usando generator para zero alocação de memória extra.
        """
        if start_date > end_date:
            return 0
            
        total_days = (end_date - start_date).days + 1
        
        return sum(
            1 for i in range(total_days) 
            if self.is_working_day(start_date + timedelta(days=i), rule)
        )

    def generate_contract_calendar(self, start_date: date, months: int, start_day: int = 26) -> Dict[str, FiscalPeriod]:
        """
        Gera um roadmap completo de X meses a partir de uma data civil.
        """
        schedule = {}
        # Usamos o primeiro período fiscal que contém a start_date como ponto de partida
        first_period = self.get_fiscal_period(start_date, start_day)
        current_period = first_period
        
        for _ in range(months):
            schedule[current_period.label] = current_period
            # Próximo corte é exatamente o start_day do mês subsequente
            next_date = current_period.end_date + timedelta(days=1)
            current_period = self.get_fiscal_period(next_date, start_day)
            
        return schedule
