import json, random, re
c = json.load(open('comments.json', encoding='utf-8'))
seen = set(); keep = []
for x in c:
    t = x['text']
    if not (40 <= len(t) <= 900) or t in seen: continue
    seen.add(t); keep.append(x)
random.seed(2026)
random.shuffle(keep)
ev = re.compile(r'https?://|according to|the article says|\bper\b the|\b\d{2,}(\.\d+)?\s?(%|percent|million|billion|ms|GB|MB|years)|\b(19|20)\d\d\b', re.I)
xp = re.compile(r"\b(I've|I have|I worked|I work|at my (job|company|work)|in my experience|we (had|use|used|run|ran)|my (wife|husband|dad|mom|team|company|doctor|dentist)|when I was|I used to)\b", re.I)
used = set(); pool = []
def take(items, n, src):
    for x in items:
        if n == 0: break
        if x['id'] in used: continue
        used.add(x['id']); pool.append({**x, 'src': src}); n -= 1
take(keep, 140, 'random')
take([x for x in keep if ev.search(x['text'])], 70, 'kw-evidence')
take([x for x in keep if xp.search(x['text'])], 70, 'kw-experience')
json.dump(pool, open('pool.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(pool))
