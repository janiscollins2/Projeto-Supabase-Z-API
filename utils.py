import re

def normalize_phone(phone: str, default_country_code="55"):
    
    if not phone:
        return None
    digits = re.sub(r"\D", "", phone)
    if len(digits) <= 11:  
        digits = default_country_code + digits
    return digits
