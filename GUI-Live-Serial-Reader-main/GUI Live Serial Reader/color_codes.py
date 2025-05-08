import re

def is_hex_color(color_code: str):
    hex_pattern = r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$"
    return bool(re.match(hex_pattern, color_code))