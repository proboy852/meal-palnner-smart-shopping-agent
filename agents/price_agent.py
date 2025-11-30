from tools.price_lookup import price_lookup
import pandas as pd

class PriceOptimizerAgent:
    def evaluate(self, shopping_list):
        rows = []
        total = 0.0
        for item, qty in shopping_list.items():
            info = price_lookup(item)
            unit_price = info.get("price", 1.0)
            est = unit_price * (qty/100 if qty > 10 else 1)
            rows.append({
                "item": item, "qty": qty, "unit_price": unit_price,
                "store": info.get("store","MockMart"), "est_cost": round(est,2)
            })
            total += est
        return {"items": rows, "total_est": round(total,2), "table": pd.DataFrame(rows)}
