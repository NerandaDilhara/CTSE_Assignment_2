import json, re

task3_str = """
```json
{
  "paper_title": "Test Title",
  "objectives": ["Obj1"],
  "methodology": "Method1",
  "findings": ["Find1"],
  "limitations": ["Lim1"],
  "research_gaps": ["Gap1"],
  "future_work": ["Fut1"]
}
```
"""

try:
    json_match = re.search(r'```json\n(.*?)\n```', task3_str, re.DOTALL)
    if json_match:
        data = json.loads(json_match.group(1))
    else:
        start = task3_str.find('{')
        end = task3_str.rfind('}')
        if start != -1 and end != -1:
            data = json.loads(task3_str[start:end+1])
        else:
            data = json.loads(task3_str)
    print("Parsed data:", data)
except Exception as e:
    print("Error:", e)
