import re

def is_hex_color(color_code: str):
    hex_pattern = r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$"
    return bool(re.match(hex_pattern, color_code))

def is_rgb_color(color_code: str):
    rgb_pattern = r"^\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$"
    return bool(re.match(rgb_pattern, color_code))