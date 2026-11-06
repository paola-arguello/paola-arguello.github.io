import sys, csv, re
from bs4 import BeautifulSoup
soup = BeautifulSoup(open(sys.argv[1], encoding="utf-8"), "html.parser")
t = lambda el: re.sub(r"\s+", " ", el.get_text(" ", strip=True)) if el else ""
rows, seen = [], set()
for item in soup.select(".product-grid-item"):
    pid = item.get("data-product-id")
    if pid in seen: continue
    seen.add(pid)
    m = re.findall(r"\$\d+\.\d{2}", t(item.select_one(".grid-product__price--current")))
    rows.append({"sauce_name": t(item.select_one(".grid-product__title")),
                 "price": float(m[-1][1:]) if m else "",
                 "vendor": t(item.select_one(".grid-product__vendor"))})
with open(sys.argv[2], "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["sauce_name","price","vendor"]); w.writeheader(); w.writerows(rows)
print(len(rows))
for r in rows: print(f"| {r['sauce_name']} | ${r['price']:.2f} | {r['vendor']} |")
