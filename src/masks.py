from .logger import create_logger

logger = create_logger(__name__, "masks.log")


def get_mask_card_number(card_number: str) -> str:
    """
    Создаёт маску для номера карты приводя к типу: 'XXXX XX** **** XXXX'
    :param card_number: номер карты
    :return: маска карты
    """
    logger.info("Старт функции get_mask_card_number")
    logger.debug(f"Получены данные: {card_number}")

    number_int = int(card_number)
    if number_int < 0:
        logger.error("Ошибка данных: Номер отрицательный")
        raise ValueError("Номер не может быть отрицательным")

    if len(card_number) != 16:
        logger.error("Ошибка данных: Не соответствующая длина номера")
        raise ValueError(f"Длина номера должна быть 16 цифр {card_number}")

    mask_format = "{0} {1}** **** {2}"
    number_list = [card_number[:4], card_number[4:6], card_number[-4:]]
    mask_card = mask_format.format(*number_list)

    logger.debug(f"Результат: {mask_card}")
    logger.info("Функция завершена успешно")
    return mask_card


def get_mask_account(account_number: str) -> str:
    """
    Создаёт маску для номера банковского счёта приводя к типу: '**XXXX'
    :param account_number: номер банковского счёта
    :return: маска счёта
    """
    logger.info("Старт функции get_mask_account")
    logger.debug(f"Получен номер: {account_number}")

    number_int = int(account_number)
    if number_int < 0:
        logger.error("Ошибка данных: Номер отрицательный")
        raise ValueError("Номер не может быть отрицательным")

    if len(account_number) != 20:
        logger.error(f"Ошибка данных: Не верная длина номера: {account_number}")
        raise ValueError("Длина номера должна быть 20 цифр")

    mask_number = f"**{account_number[-4:]}"

    logger.debug(f"Результат: {mask_number}")
    logger.info("Функция завершена успешно")
    return mask_number
