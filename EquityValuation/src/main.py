import csv
from pathlib import Path
from typing import List

from valuation_models import (
    Equity,
    ValuationError,
    ValuationModel,
    VALUATION_MODELS,
)


class EquityValuationApp:
    def __init__(self, csv_file_path: Path):
        self.csv_file_path = csv_file_path

    def read_equities(self) -> List[Equity]:
        equities: List[Equity] = []

        if not self.csv_file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_file_path}")

        with self.csv_file_path.open(mode="r", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)

            required_columns = {"symbol", "name", "valuation_model"}
            missing_columns = required_columns - set(reader.fieldnames or [])

            if missing_columns:
                raise ValueError(
                    f"Missing required columns in CSV: {', '.join(missing_columns)}"
                )

            for row in reader:
                symbol = row["symbol"].strip()
                name = row["name"].strip()
                valuation_model = row["valuation_model"].strip().lower()

                equity = Equity(
                    symbol=symbol,
                    name=name,
                    valuation_model=valuation_model,
                    data=row,
                )

                equities.append(equity)

        return equities

    def get_valuation_model(self, model_name: str) -> ValuationModel:
        model_class = VALUATION_MODELS.get(model_name)

        if model_class is None:
            available_models = ", ".join(VALUATION_MODELS.keys())
            raise ValueError(
                f"Unknown valuation model '{model_name}'. "
                f"Available models: {available_models}"
            )

        return model_class()

    def value_equity(self, equity: Equity) -> float:
        model = self.get_valuation_model(equity.valuation_model)
        return model.calculate(equity)

    def run(self) -> None:
        equities = self.read_equities()

        print("Equity Valuation Results")
        print("-" * 80)
        print(f"{'Symbol':<10} {'Name':<25} {'Model':<10} {'Fair Value':>15}")
        print("-" * 80)

        for equity in equities:
            try:
                fair_value = self.value_equity(equity)

                print(
                    f"{equity.symbol:<10} "
                    f"{equity.name:<25} "
                    f"{equity.valuation_model:<10} "
                    f"{fair_value:>15.2f}"
                )

            except ValuationError as exc:
                print(
                    f"{equity.symbol:<10} "
                    f"{equity.name:<25} "
                    f"{equity.valuation_model:<10} "
                    f"ERROR: {exc}"
                )


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    csv_file = project_root / "data" / "equity_details.csv"

    app = EquityValuationApp(csv_file)
    app.run()