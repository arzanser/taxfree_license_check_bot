from bot.text import *

def merge_dict_mosreg(car_license_dict, carier_license_dict) -> dict:
    data_frame = {
        "Статус:": "",
        "Перевозчик (наименование ЮЛ или ИП):": "",
        "ОГРН / ОГРНИП:": "",
        "ИНН:": "",
        "Марка автомобиля:": "",
        "Модель автомобиля:": "",
        "Государственный регистрационный номер:": "",
        "Номер реестровой записи в региональном реестре легкового такси:": "",
        "Номер реестровой записи в региональном реестре перевозчиков легковым такси:": "",
        "Дата предоставления разрешения:": "",
        "Срок действия разрешения:": "",
        "Внесено в разрешение перевозчика:": ""
        }

    if car_license_dict !=  MESSAGES["ERROR_CAR_LICENSE"] or carier_license_dict != MESSAGES["ERROR_CARIER_LICENSE"]:
        check_status = car_license_dict.pop("Внесено в разрешение перевозчика:")
        
        for key, value in car_license_dict.items():
            if key in data_frame:
                data_frame[key] = value

        for key, value in carier_license_dict.items():
            if key in data_frame and key != "Статус:":
                data_frame[key] = value

        if check_status.strip().isdigit():
            data_frame["Внесено в разрешение перевозчика:"] = "✅ "
        else:
            data_frame["Внесено в разрешение перевозчика:"] = "❌ "

        return data_frame

    else:
        return car_license_dict | carier_license_dict


def merge_dict_mosru(car_license_dict, carier_license_dict) -> dict:
    data_frame = {
        "Статус": "",
        "Фамилия, Имя, Отчество индивидуального предпринимателя или физического лица": "",
        "Полное наименование юридического лица": "",
        "ОГРН / ОГРНИП": "",
        "ИНН": "",
        "Марка транспортного средства": "",
        "Модель транспортного средства": "",
        "Государственный регистрационный номер транспортного средства": "",
        "Номер записи в региональном реестре легковых такси, содержащий сведения о легковом такси": "",
        "Номер записи в региональном реестре перевозчиков легковым такси, содержащий сведения о перевозчике": "",
        "Дата внесения записи в региональный реестр перевозчиков легковым такси": "",
        "Дата окончания срока действия разрешения": "",
        "Внесено в разрешение перевозчика:": "",
    }

    if car_license_dict == {}: car_license_dict = MESSAGES["ERROR_CAR_LICENSE"]
    if carier_license_dict == {}: carier_license_dict = MESSAGES["ERROR_CARIER_LICENSE"]
    
    if car_license_dict != MESSAGES["ERROR_CAR_LICENSE"] or carier_license_dict != MESSAGES["ERROR_CARIER_LICENSE"]:
        for key, value in car_license_dict.items():
            if key in data_frame:
                data_frame[key] = value

        for key, value in carier_license_dict.items():
            if key in data_frame:
                data_frame[key] = value

            if key == "Номера записей в региональном реестре легковых такси города Москвы, содержащих сведения о легковых такси, используемых перевозчиком легковым такси для осуществления перевозок пассажиров и багажа легковым такси:" or carier_license_dict == MESSAGES["ERROR_CARIER_LICENSE"]:
                if car_license_dict["Государственный регистрационный номер транспортного средства"] in value.split():
                    data_frame["Внесено в разрешение перевозчика:"] = "✅ "
                else:
                    data_frame["Внесено в разрешение перевозчика:"] = "❌ " 

        return data_frame
    else:
        return car_license_dict | carier_license_dict


def print_license_data(data) -> str:
    license = ""
    for key, value in data.items():
        license += f"{key} - {value}\n\n"
    return license
