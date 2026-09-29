# GitHub issue'larındaki işaret kutularını okuyup durum.json'a yazar.
import json, re, subprocess, os, datetime
repo = os.environ.get("REPO", "chaseitego-ops/remble-takvim")
out = subprocess.run(["gh", "api", "--paginate", f"repos/{repo}/issues?state=all&per_page=100"],
                     capture_output=True, text=True, check=True).stdout
issues = json.loads(out.replace("][", ","))
days = {}
for it in issues:
    body = it.get("body") or ""
    m = re.search(r"<!-- gun:(\d{4}-\d{2}-\d{2}) -->", body)
    if not m:
        continue
    days[m.group(1)] = [c != " " for c in re.findall(r"^- \[( |x|X)\]", body, re.M)]
data = {"days": dict(sorted(days.items()))}
old = {}
if os.path.exists("durum.json"):
    with open("durum.json", encoding="utf-8") as f:
        old = json.load(f)
if old.get("days") != data["days"]:
    data["at"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    with open("durum.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("durum.json güncellendi")
else:
    print("değişiklik yok")
