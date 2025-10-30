
def validate_percentage(tax_percentage: float | None) -> bool:
    if tax_percentage is not None and (tax_percentage < 0 or tax_percentage > 100):
        return False
    return True
