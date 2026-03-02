import re
import json

def clean_price(price_str):
    #Convert price string like '1 200,00' into float 1200.00
    price_str = price_str.replace(" ", "").replace(",", ".")
    return float(price_str)

def parse_receipt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    #Extract All Prices
    price_pattern = r"\d(?: ?\d)*,\d{2}"
    raw_prices = re.findall(price_pattern, text)

    prices = [clean_price(p) for p in raw_prices]

    #Extract Product Names
    product_pattern = r"\d+\.\n(.+)"
    products = re.findall(product_pattern, text)

    #Extract Total Amount
    total_pattern = r"ИТОГО:\n([\d\s]+,\d{2})"
    total_match = re.search(total_pattern, text)
    total = clean_price(total_match.group(1)) if total_match else 0

    #Extract Date & Time
    datetime_pattern = r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s*\d{2}:\d{2}:\d{2})"
    datetime_match = re.search(datetime_pattern, text)
    datetime = datetime_match.group(1) if datetime_match else None

    #Extract Payment Method
    payment_pattern = r"(Банковская карта|Наличные)"
    payment_match = re.search(payment_pattern, text)
    payment_method = payment_match.group(1) if payment_match else "Не найдено"

    #Create Structured Output
    receipt_data = {
        "products": products,
        "prices": prices,
        "total_amount": total,
        "datetime": datetime,
        "payment_method": payment_method
    }

    return receipt_data

if __name__ == "__main__":
    file_path = "Practice5/raw.txt"
    parsed_data = parse_receipt(file_path)

    print("РАСПАРСЕННЫЙ ЧЕК:\n")
    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))
