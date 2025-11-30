def human_friendly_list(shopping_dict):
    """
    Convert {'tomato':150, 'spaghetti':400} -> a readable list of lines
    """
    lines = []
    for item, qty in shopping_dict.items():
        # if qty is 0 skip
        if qty <= 0:
            continue
        # convert grams to 'units' if large
        if qty >= 1000:
            qty_str = f"{qty/1000:.1f} kg"
        elif qty >= 100:
            qty_str = f"{qty} g"
        else:
            qty_str = f"{qty} g"
        lines.append(f"- {item}: {qty_str}")
    return "\n".join(lines)
