import json

# Check all 22 non-PT languages for the 5 keys
langs = ["ar","de","el","en","eo","es","fa","fi","fr","hi","id","it","ja","ko","pl","ro","ru","sw","th","tr","vi","zh"]
for code in langs:
    d = json.load(open(f"translations/{code}.json", encoding="utf-8"))
    title = d["labels"]["app_title"]
    settings = d["labels"]["settings"]
    # Quick heuristic: if title contains "Bible" (English) or "Bibl" (Latin-derived but OK for Germanic/Romance),
    # or if it looks like garbage (contains Latin chars for CJK), flag it
    print(f"{code}:")
    print(f"  app_title: {title[:60]}")
    print(f"  settings:  {settings[:40]}")
    print(f"  page_subtitle: {d['labels']['page_subtitle'][:50]}")
    print(f"  support_title: {d['messages']['support_title'][:40]}")
    print(f"  api_online: {d['messages']['api_online'][:50]}")
    print()
