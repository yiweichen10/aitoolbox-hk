import json
import re

zh_pattern = re.compile(r'[\u4e00-\u9fa5]+')
found = set()

def scan(obj):
    if isinstance(obj, str):
        found.update(zh_pattern.findall(obj))
    elif isinstance(obj, list):
        for i in obj:
            scan(i)
    elif isinstance(obj, dict):
        for v in obj.values():
            scan(v)

file_path = r'C:\Users\27040\WorkBuddy\20260321092139\seo-site-en\data\tools_en.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

scan(data)
for item in sorted(list(found)):
    print(item)
