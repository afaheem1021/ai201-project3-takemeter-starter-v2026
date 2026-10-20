import json, sys, html, re, urllib.request, random
ids = sys.argv[1:]
out = []
def clean(t):
    t = re.sub(r'<p>', '\n\n', t or '')
    t = re.sub(r'<a href="([^"]*)"[^>]*>.*?</a>', lambda m: html.unescape(m.group(1)), t)
    t = re.sub(r'<[^>]+>', '', t)
    return html.unescape(t).strip()
def walk(node, story, depth):
    for c in node.get('children', []):
        if c.get('type') == 'comment' and c.get('text'):
            out.append({'id': c['id'], 'story': story, 'depth': depth, 'author': c.get('author'), 'text': clean(c['text'])})
        walk(c, story, depth + 1)
for sid in ids:
    d = json.load(urllib.request.urlopen(f'https://hn.algolia.com/api/v1/items/{sid}'))
    walk(d, d['title'], 0)
json.dump(out, open('comments.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(out))
