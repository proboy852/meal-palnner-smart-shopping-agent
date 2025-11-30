from tools.price_lookup import price_lookup
import pandas as pd

class PriceOptimizerAgent:
    def evaluate(self, shopping_list):
        rows = []
        total = 0

        for item, qty in shopping_list.items():
            p = price_lookup(item)
            est = p["price"] * (qty / 100 if qty > 10 else 1)

            rows.append({
                "item": item,
                "qty": qty,
                "unit_price": p["price"],
                "store": p["store"],
                "est_cost": round(est, 2)
            })

            total += est

        return {
            "items": rows,
            "total_est": round(total, 2),
            "table": pd.DataFrame(rows)
        }
