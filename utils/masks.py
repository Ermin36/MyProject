#functions

def get_mask_card_number(card_number:int)->str:
    """
    Создаёт маску для номера карты приводя к типу: 'XXXX XX** **** XXXX'
    :param card_number: номер карты
    :return: маска карты
    """
    number_str = str(card_number)
    if card_number < 0:
        raise ValueError('Номер не может быть отрицательным')

    if len(number_str) != 16:
        raise ValueError('Длина номера должна быть 16 цифр')

    mask_format = '{0} {1}** **** {2}'
    number_list = [number_str[:4],number_str[4:6],number_str[-4:]]
    mask_card = mask_format.format(*number_list)

    return mask_card


def get_mask_account(account_number:int)->str:
    """
    Создаёт маску для номера бонковского счёта приводя к типу: '**XXXX'
    :param account_number: номер банковского счёта
    :return: маска счёта
    """
    if account_number <0:
        raise ValueError('Номер не может быть отрицательным')

    number_str = str(account_number)
    if len(number_str) != 16:
        raise ValueError('Длина номера должна быть 16 цифр')

    mask_number = f'**{number_str[-4:]}'
    return mask_number