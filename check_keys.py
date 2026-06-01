import json

keys = [
    ("app_title", "labels"),
    ("settings", "labels"),
    ("page_subtitle", "labels"),
    ("support_title", "messages"),
    ("api_online", "messages"),
]
langs = ["en","pt","es","fr","ja","ko","zh","de","it","ar","ru","vi"]

print(f"{'code':<5} {'key':<20} value")
print("-"*65)
for code in langs:
    d = json.load(open(f"translations/{code}.json", encoding="utf-8"))
    for k, section in keys:
        val = d[section][k]
        print(f"{code:<5} {k:<20} {val[:50]}")
    print()
