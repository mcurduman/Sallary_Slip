from stdnum import ro

def validate_national_id(national_id: str, country_code: str) -> bool:
    if country_code == "RO":
        return ro.cnp.is_valid(national_id)
    return False
