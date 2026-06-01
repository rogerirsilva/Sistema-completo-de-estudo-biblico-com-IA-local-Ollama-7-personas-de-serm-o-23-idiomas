import json, subprocess, os

SOURCES = ["translations", "tauri-launcher/python_app/translations"]

# English values (what the fallback shows)
EN_VALUES = {
    "labels": {
        "app_title": "Bible Study with AI",
        "settings": "Settings",
        "page_subtitle": "Exegesis, Sermons (7 Personas), Devotional and Theological Chat locally with Ollama."
    },
    "messages": {
        "support_title": "Support the project",
        "api_online": "API online at http://localhost:8000"
    }
}

# First add these to all language files (later steps will translate)
# 'pt' already has Portuguese values - keep them
PT_VALUES = {
    "labels": {
        "app_title": "B\u00edblia de Estudos com IA",
        "settings": "Configura\u00e7\u00f5es",
        "page_subtitle": "Exegese, Serm\u00f5es (7 Personas), Devocional e Chat teol\u00f3gico local com Ollama."
    },
    "messages": {
        "support_title": "Apoie o projeto",
        "api_online": "API online em http://localhost:8000"
    }
}

def call_ollama(prompt, model="llama3.1:8b"):
    p = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"num_predict": 1024, "temperature": 0.1}})
    r = subprocess.run(["curl", "-s", "-X", "POST", "http://localhost:11434/api/generate", "-d", p], capture_output=True, text=True, timeout=180)
    resp = json.loads(r.stdout)
    return resp.get("response", "").strip()

def parse_json(text):
    if not text: return None
    start = text.find("{")
    if start < 0: return None
    depth = in_str = esc = 0
    for i, c in enumerate(text[start:], start):
        if esc: esc = 0; continue
        if c == "\\": esc = 1
        elif c == "\"": in_str = not in_str
        elif not in_str:
            if c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try: return json.loads(text[start:i+1])
                    except: return None
    return None

def translate_batch(lang_name):
    """Translate all 5 strings at once"""
    prompt = (
        f"Translate these JSON strings from English to {lang_name}.\n"
        f"Return ONLY a JSON object with the same structure, no markdown.\n\n"
        f'{json.dumps(EN_VALUES, indent=2, ensure_ascii=False)}'
    )
    resp = call_ollama(prompt)
    return parse_json(resp)

def translate_one(text, lang_name):
    """Translate a single string"""
    prompt = f"Translate this to {lang_name}. Return only the translation: {text}"
    resp = call_ollama(prompt)
    return resp.strip().strip('"').strip("'").strip()

# Languages to process (all except pt which already has values)
LANG_NAMES = {
    "ar": "Arabic", "de": "German", "el": "Greek", "en": "English",
    "eo": "Esperanto", "es": "Spanish", "fa": "Persian", "fi": "Finnish",
    "fr": "French", "hi": "Hindi", "id": "Indonesian", "it": "Italian",
    "ja": "Japanese", "ko": "Korean", "pl": "Polish", "ro": "Romanian",
    "ru": "Russian", "sw": "Swahili", "th": "Thai", "tr": "Turkish",
    "vi": "Vietnamese", "zh": "Chinese (Simplified)"
}

for code, name in LANG_NAMES.items():
    print(f"\n=== {name} ({code}) ===")

    if code == "en":
        # Use English values directly
        values = EN_VALUES
    elif code == "pt":
        values = PT_VALUES
    else:
        # Try batch translation
        result = translate_batch(name)
        if result and "labels" in result and "messages" in result:
            labels = result.get("labels", {})
            messages = result.get("messages", {})
            if all(k in labels for k in ["app_title", "settings", "page_subtitle"]) and \
               all(k in messages for k in ["support_title", "api_online"]):
                values = result
                print(f"  Batch OK")
            else:
                result = None

        if not result:
            # Per-key fallback
            print(f"  Batch failed, per-key...")
            values = {
                "labels": {},
                "messages": {}
            }
            for k in ["app_title", "settings", "page_subtitle"]:
                val = translate_one(EN_VALUES["labels"][k], name)
                values["labels"][k] = val or EN_VALUES["labels"][k]
            for k in ["support_title", "api_online"]:
                val = translate_one(EN_VALUES["messages"][k], name)
                values["messages"][k] = val or EN_VALUES["messages"][k]

    # Update both directories
    for src in SOURCES:
        fpath = os.path.join(src, f"{code}.json")
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["labels"]["app_title"] = values["labels"]["app_title"]
        data["labels"]["settings"] = values["labels"]["settings"]
        data["labels"]["page_subtitle"] = values["labels"]["page_subtitle"]
        data["messages"]["support_title"] = values["messages"]["support_title"]
        data["messages"]["api_online"] = values["messages"]["api_online"]
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Updated")

print("\nAll done!")
