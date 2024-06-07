def check_car_number(car_number) -> bool:
    alpha = ["А", "В", "Е", "К", "М", "Н", "О", "Р", "С", "Т", "У", "Х"]
    current_number = ""
    if 7 <= len(car_number) <= 9:
        for symbol in car_number:
            if symbol in alpha or symbol.isdigit():
                current_number += symbol

    if current_number == car_number and not current_number.isalpha() and not current_number.isdigit():
        return True
    
    return False

