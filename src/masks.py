from .logger import create_logger

logger = create_logger(__name__, 'masks.log')


def get_mask_card_number(card_number: int) -> str:
    """
    Создаёт маску для номера карты приводя к типу: 'XXXX XX** **** XXXX'
    :param card_number: номер карты
    :return: маска карты
    """
    logger.info("Старт функции get_mask_card_number")
    logger.debug(f"Получены данные: {card_number}")

    number_str = str(card_number)
    if card_number < 0:
        logger.error("Ошибка данных: Номер отрицательный")
        raise ValueError("Номер не может быть отрицательным")

    if len(number_str) != 16:
        logger.error("Ошибка данных: Не соответствующая длина номера")
        raise ValueError("Длина номера должна быть 16 цифр")

    mask_format = "{0} {1}** **** {2}"
    number_list = [number_str[:4], number_str[4:6], number_str[-4:]]
    mask_card = mask_format.format(*number_list)

    logger.debug(f"Результат: {mask_card}")
    logger.info("Функция завершена успешно")
    return mask_card


def get_mask_account(account_number: int) -> str:
    """
    Создаёт маску для номера бонковского счёта приводя к типу: '**XXXX'
    :param account_number: номер банковского счёта
    :return: маска счёта
    """
    logger.info("Старт функции get_mask_account")
    logger.debug(f"Получен номер: {account_number}")

    if account_number < 0:
        logger.error("Ошибка данных: Номер отрицательный")
        raise ValueError("Номер не может быть отрицательным")

    number_str = str(account_number)
    if len(number_str) != 16:
        logger.error("Ошибка данных: Не верная длина номера")
        raise ValueError("Длина номера должна быть 16 цифр")

    mask_number = f"**{number_str[-4:]}"

    logger.debug(f"Результат: {mask_number}")
    logger.info("Функция завершена успешно")
    return mask_number
