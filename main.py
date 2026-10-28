import pymupdf
import re
from decimal import Decimal

doc = pymupdf.open(r"C:\Users\hhuser\Downloads\bank.pdf")

date_pattern = r"\d{2}\.\d{2}\.\d{4}" # Через паттерн даты и времени будем искать транзакции в этом файле
time_pattern = r"\d{2}:\d{2}"
transactions = [] # Внешний спикок операций
for page_num in range(doc.page_count):
    page = doc.load_page(page_num) # Загружаем страницы из PDF
    text = page.get_text() # Достаём из страниц текст
    lines = text.splitlines() # Из текста берём строки
    for index, line in enumerate(lines):
        date_match = re.fullmatch(date_pattern, line)
        if date_match:
            if index + 4 < len(lines): # Проверяем наличие нужных нам строк
                next_index = index + 1
                transaction = {"date": None, # Создаём внутренний словарь для каждой транзакции
                               "time": None,
                               "category": None,
                               "amount": None,
                               "balance": None,
                               "type": None}
                if re.fullmatch(time_pattern, lines[next_index]):
                    transaction["date"] = lines[index] # Извлекаем нужные нам категории
                    transaction["time"] = lines[index + 1]
                    transaction["category"] = lines[index + 2]
                    transaction["amount"] = lines[index + 3]
                    transaction["balance"] = lines[index + 4]
                    transaction["amount"] = transaction["amount"].replace("\xa0", "") # Убираем пробел
                    transaction["amount"] = transaction["amount"].replace(",", ".") # Меняем запятую на точку
                    if transaction["amount"].startswith("+"): # Проверяем тип операции, операции с плюсом - доходы, без знака - расходы
                        transaction["type"] = "income"
                    else:
                        transaction["type"] = "expense"
                    transaction["amount"] = Decimal(transaction["amount"]) # Преобразуем строку в decimal для денежных вычислений
                    transaction["amount"] = int(transaction["amount"] * 100) # Переводим из рублей в копейки, т.к. SQL не работает с decimal
                    transaction["balance"] = transaction["balance"].replace("\xa0", "")
                    transaction["balance"] = transaction["balance"].replace(",", ".")
                    transaction["balance"] = Decimal(transaction["balance"])
                    transaction["balance"] = int(transaction["balance"] * 100)
                    transactions.append(transaction) # Добавляем каждую транзакцию во внешний список
print(len(transactions))
print(transactions[11])