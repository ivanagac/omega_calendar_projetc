#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ PRODUCTION CALENDAR ENGINE v3.0 - OMEGA EVOLUTION
==============================================================================
Arquiteta: Ivana Cruz(Exclusivo para a Eternidade)
Status: Anti-Erro. Dinâmico. Aceita até 31 dias.
==============================================================================
"""

import calendar
from datetime import date, timedelta
from typing import Iterable, Set, Dict
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
        """Retorna o tamanho exato da janela em dias corridos."""
        return (self.end_date - self.start_date).days + 1


class ProductionCalendar:
    """
    Motor definitivo para conversão de Tempo Civil em Tempo de Produção.
    Suporta dias de corte dinâmicos (1 a 31) com ajuste automático para meses curtos.
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
        # Busca O(1) para feriados e dias de bônus produtivo.
        self.holidays: Set[date] = set(holidays) if holidays else set()
        self.extra_working_days: Set[date] = set(extra_working_days) if extra_working_days else set()

    def _safe_date(self, year: int, month: int, day: int) -> date:
        """Ajusta o dia solicitado para o último dia disponível do mês se necessário."""
        last_day = calendar.monthrange(year, month)[1]
        return date(year, month, min(day, last_day))

    def get_fiscal_period(self, reference_date: date, start_day: int) -> FiscalPeriod:
        """
        Calcula o período fiscal com base em um start_day obrigatório.
        Aceita start_day até 31, normalizando para o fim do mês quando necessário.
        """
        if not (1 <= start_day <= 31):
            raise ValueError(f"⚠️ start_day={start_day} é inválido. Use entre 1 e 31.")

        # Lógica de Decisão: A data atual já pertence ao próximo mês fiscal?
        # Para fins de comparação, usamos a mesma lógica de ajuste seguro.
        last_day_ref = calendar.monthrange(reference_date.year, reference_date.month)[1]
        effective_start = min(start_day, last_day_ref)

        if reference_date.day >= effective_start:
            fiscal_month = (reference_date.month % 12) + 1
            fiscal_year = reference_date.year + (1 if reference_date.month == 12 else 0)
        else:
            fiscal_month = reference_date.month
            fiscal_year = reference_date.year

        # Cálculo do Início: Dia de corte no mês anterior ao fiscal
        prev_m = 12 if fiscal_month == 1 else fiscal_month - 1
        prev_y = fiscal_year - 1 if fiscal_month == 1 else fiscal_year
        start_dt = self._safe_date(prev_y, prev_m, start_day)
        
        # Cálculo do Fim: Dia anterior ao próximo corte fiscal
        next_cut_dt = self._safe_date(fiscal_year, fiscal_month, start_day)
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
        """Precedência: Dia Extra > Feriado > Regra de Semana."""
        if target_date in self.extra_working_days:
            return True
        if target_date in self.holidays:
            return False
            
        weekday = target_date.weekday()
        if rule == 'SEG_SEX':
            return weekday <= 4
        elif rule == 'SEG_SAB':
            return weekday <= 5
        elif rule == 'TODOS':
            return True
        raise ValueError(f"⚠️ Regra desconhecida: {rule}.")

    def count_working_days(self, start_date: date, end_date: date, rule: str = 'SEG_SEX') -> int:
        """Conta dias produtivos no intervalo."""
        if start_date > end_date:
            return 0
        total_days = (end_date - start_date).days + 1
        return sum(1 for i in range(total_days) if self.is_working_day(start_date + timedelta(days=i), rule))

    def generate_contract_calendar(self, start_date: date, months: int, start_day: int) -> Dict[str, FiscalPeriod]:
        """Gera sequência de meses fiscais sem acumular erros de data."""
        schedule = {}
        current_ref = start_date
        
        for _ in range(months):
            period = self.get_fiscal_period(current_ref, start_day)
            schedule[period.label] = period
            # Salta para o dia seguinte ao fim da janela para pegar o próximo ciclo
            current_ref = period.end_date + timedelta(days=1)
            
        return schedule