import json
langs = ["fi","id","el","eo","hi","fa","pl","ro","sw","th","tr","nl","no","cs","hu","uk"]
for code in langs:
    try:
        d = json.load(open(f"translations/{code}.json", encoding="utf-8"))
        print(f"{code}: title={d['labels']['app_title'][:50]}")
    except:
        pass
