import json

# 1. Загрузка данных
with open(r"C:\Users\Акниет\Desktop\practice_pp2\Practice4\json\sample-data.json", "r") as f:
    data = json.load(f)

# 2. Заголовок таблицы
print("Interface Status")
print("="*80)
print(f"{'DN':50} {'Description':20} {'Speed':6} {'MTU':6}")
print("-"*50, "-"*20, "-"*6, "-"*6)

# 3. Проход по интерфейсам и вывод
for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]
    dn = attrs.get("dn", "")
    descr = attrs.get("descr", "")
    speed = attrs.get("speed", "")
    mtu = attrs.get("mtu", "")
    
    print(f"{dn:50} {descr:20} {speed:6} {mtu:6}")