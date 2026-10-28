import pymupdf
import re

doc = pymupdf.open(r"C:\Users\hhuser\Downloads\bank.pdf")

date_pattern = r"\d{2}\.\d{2}\.\d{4}"
time_pattern = r"\d{2}:\d{2}"
for page_num in range(doc.page_count):
    page = doc.load_page(page_num)
    text = page.get_text()
    lines = text.splitlines()
    for index, line in enumerate(lines):
        date_match = re.fullmatch(date_pattern, line)
        if date_match:
            if index + 4 < len(lines):
                next_index = index + 1
                transaction = {"date": None,
                               "time": None,
                               "category": None,
                               "amount": None,
                               "balance": None}
                if re.fullmatch(time_pattern, lines[next_index]):
                    transaction["date"] = lines[index]
                    transaction["time"] = lines[index + 1]
                    transaction["category"] = lines[index + 2]
                    transaction["amount"] = lines[index + 3]
                    transaction["balance"] = lines[index + 4]
                    print(transaction)