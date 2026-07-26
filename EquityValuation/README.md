# Equity Valuation Project

This project reads equity details from a CSV file, assigns each equity to a valuation model, and outputs an estimated fair value per share.

## Supported valuation models

| Model | Name | Required CSV fields |
|---|---|---|
| `pe` | Price/Earnings Model | `eps`, `pe_multiple` |
| `ddm` | Dividend Discount Model | `dividend`, `required_return`, `growth_rate` |
| `dcf` | Discounted Cash Flow Model | `free_cash_flow`, `growth_rate`, `discount_rate`, `terminal_growth_rate`, `shares_outstanding`, `net_debt` |

## Run the project

Create and activate a virtual environment:
