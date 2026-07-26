from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Type


class ValuationError(Exception):
    """Raised when valuation cannot be calculated."""


@dataclass
class Equity:
    symbol: str
    name: str
    valuation_model: str
    data: dict


class ValuationModel(ABC):
    """Base class for all valuation models."""

    @abstractmethod
    def calculate(self, equity: Equity) -> float:
        """Calculate fair value per share."""
        raise NotImplementedError

    def _get_float(self, equity: Equity, field_name: str) -> float:
        value = equity.data.get(field_name)

        if value is None or value == "":
            raise ValuationError(
                f"Missing required field '{field_name}' for {equity.symbol}"
            )

        try:
            return float(value)
        except ValueError as exc:
            raise ValuationError(
                f"Invalid numeric value for '{field_name}' in {equity.symbol}: {value}"
            ) from exc


class PriceEarningsModel(ValuationModel):
    """
    Price/Earnings valuation model.

    Formula:
        Fair Value = EPS x PE Multiple
    """

    def calculate(self, equity: Equity) -> float:
        eps = self._get_float(equity, "eps")
        pe_multiple = self._get_float(equity, "pe_multiple")

        return eps * pe_multiple


class DividendDiscountModel(ValuationModel):
    """
    Gordon Growth Dividend Discount Model.

    Formula:
        Fair Value = Dividend x (1 + Growth Rate) / (Required Return - Growth Rate)
    """

    def calculate(self, equity: Equity) -> float:
        dividend = self._get_float(equity, "dividend")
        required_return = self._get_float(equity, "required_return")
        growth_rate = self._get_float(equity, "growth_rate")

        if required_return <= growth_rate:
            raise ValuationError(
                f"Required return must be greater than growth rate for {equity.symbol}"
            )

        return dividend * (1 + growth_rate) / (required_return - growth_rate)


class DiscountedCashFlowModel(ValuationModel):
    """
    Simple one-stage DCF valuation model.

    Formula:
        Enterprise Value = FCF x (1 + Growth Rate) / (Discount Rate - Terminal Growth Rate)
        Equity Value = Enterprise Value - Net Debt
        Fair Value Per Share = Equity Value / Shares Outstanding
    """

    def calculate(self, equity: Equity) -> float:
        free_cash_flow = self._get_float(equity, "free_cash_flow")
        growth_rate = self._get_float(equity, "growth_rate")
        discount_rate = self._get_float(equity, "discount_rate")
        terminal_growth_rate = self._get_float(equity, "terminal_growth_rate")
        shares_outstanding = self._get_float(equity, "shares_outstanding")
        net_debt = self._get_float(equity, "net_debt")

        if discount_rate <= terminal_growth_rate:
            raise ValuationError(
                f"Discount rate must be greater than terminal growth rate for {equity.symbol}"
            )

        if shares_outstanding <= 0:
            raise ValuationError(
                f"Shares outstanding must be greater than zero for {equity.symbol}"
            )

        enterprise_value = (
            free_cash_flow
            * (1 + growth_rate)
            / (discount_rate - terminal_growth_rate)
        )

        equity_value = enterprise_value - net_debt

        return equity_value / shares_outstanding


VALUATION_MODELS: Dict[str, Type[ValuationModel]] = {
    "pe": PriceEarningsModel,
    "ddm": DividendDiscountModel,
    "dcf": DiscountedCashFlowModel,
}