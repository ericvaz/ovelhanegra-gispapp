#!/usr/bin/env python3
"""Generate the SEO 'sample questions by category' pages from the question bank.

Usage: python3 tools/gen-question-pages.py   (run from repo root)
Writes GISPApp/questions/index.html and GISPApp/questions/<slug>/index.html.
Deterministic: the same 5 sample questions per category every run (seeded),
so pages don't churn between deploys.
"""
import json, re, html, random, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
Q = json.load(open(ROOT / "GISPApp/practice/data/questions.json"))
OUT = ROOT / "GISPApp/questions"
BASE = "https://ovelhanegra.io/GISPApp"
DOMAINS = ["Conceptual Foundations","Geospatial Data Fundamentals","Cartography & Visualization","Data Acquisitions","Data Manipulation","Analytical Methods","Database Design & Management","Application Development","Systems Design & Management","Professional Practice"]
BLURB = {
 "Conceptual Foundations": "the nature of geographic information: scale, spatial relationships, Tobler's first law, MAUP, levels of measurement, field versus object views, and how GIS represents the world",
 "Geospatial Data Fundamentals": "vector and raster models, topology, datums and projections as applied to data, metadata standards, data quality and formats",
 "Cartography & Visualization": "map design, symbology and visual variables, classification, colour, labeling, generalization, thematic map types and web maps",
 "Data Acquisitions": "remote sensing, GNSS, surveying, photogrammetry, lidar, digitizing, field collection and acquiring third-party data",
 "Data Manipulation": "editing, topology cleaning, geoprocessing for data preparation, reprojection, format conversion, resampling, joins, QA/QC and automation",
 "Analytical Methods": "overlay, proximity, network analysis, interpolation, terrain analysis, spatial statistics, suitability modelling and map algebra",
 "Database Design & Management": "the relational model, normalization, SQL and spatial SQL, spatial databases, indexes, transactions, versioning and data integrity",
 "Application Development": "scripting and automation, web mapping, OGC services, REST APIs, the software lifecycle, version control, testing and security",
 "Systems Design & Management": "needs assessment, architecture, capacity planning, implementation, governance, cost-benefit, procurement and system maintenance",
 "Professional Practice": "ethics and the GISCI Code of Ethics, certification and licensure, liability, copyright and data licensing, privacy and professional communication",
}
slug = lambda d: re.sub(r"[^a-z0-9]+", "-", d.lower().replace("&", "and")).strip("-")
e = html.escape
today = datetime.date.today().isoformat()

HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}">
<meta name="apple-itunes-app" content="app-id=6785084756">
<meta property="og:type" content="article"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="https://ovelhanegra.io/GISPApp/img/og.png">
<link rel="icon" href="../../img/icon.png">
<script type="application/ld+json">{ld}</script>
<style>
:root{{--blue:#1560c8;--blue2:#0ea5a4;--ink:#111827;--sub:#5b6472;--line:#e8ebf1;--soft:#f4f8fd}}
*{{box-sizing:border-box;margin:0;padding:0}}body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);line-height:1.6;-webkit-font-smoothing:antialiased}}
a{{color:var(--blue);text-decoration:none}}.in{{max-width:780px;margin:0 auto;padding:0 20px}}
nav{{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0}}nav .in{{display:flex;justify-content:space-between;align-items:center;height:60px}}
.brand{{display:flex;align-items:center;gap:10px;font-weight:800;color:var(--ink)}}.brand img{{width:30px;height:30px;border-radius:8px}}
.btn{{display:inline-block;background:var(--blue);color:#fff;border-radius:12px;padding:10px 16px;font-weight:700}}.btn.ghost{{background:#fff;color:var(--ink);border:1px solid var(--line)}}
main{{padding:36px 0 60px}}h1{{font-size:2rem;line-height:1.15;letter-spacing:-.02em}}h2{{font-size:1.25rem;margin:26px 0 8px}}.lead{{color:var(--sub);font-size:1.08rem;margin:12px 0 20px}}
.q{{border:1px solid var(--line);border-radius:16px;padding:18px 20px;margin:16px 0;background:#fff}}.q .m{{font-size:.8rem;color:var(--sub);font-weight:600;letter-spacing:.03em;text-transform:uppercase}}
.q h3{{font-size:1.05rem;margin:6px 0 10px;line-height:1.45}}.q ol{{list-style:upper-alpha;padding-left:26px}}.q li{{margin:4px 0}}
details{{margin-top:10px;background:var(--soft);border-radius:10px;padding:10px 12px}}summary{{cursor:pointer;font-weight:700;color:var(--blue)}}details p{{margin-top:8px}}
.cta{{background:linear-gradient(160deg,#eaf3ff,#f3fbfa);border:1px solid var(--line);border-radius:16px;padding:22px;margin:30px 0}}.cta .row{{display:flex;gap:12px;flex-wrap:wrap;margin-top:12px}}
.cats{{columns:2;gap:18px}}.cats a{{display:block;padding:6px 0}}@media(max-width:600px){{.cats{{columns:1}}}}
footer{{border-top:1px solid var(--line);color:var(--sub);font-size:.85rem;padding:30px 20px 50px;text-align:center}}footer a{{margin:0 8px}}
</style></head><body>
<nav><div class="in"><a class="brand" href="../../"><img src="../../img/icon.png" alt="">GISP Prep</a><div><a class="btn ghost" href="../../practice/">Practice online</a> <a class="btn" href="https://apps.apple.com/us/app/gisp-prep-gis-exam-practice/id6785084756">iPhone app</a></div></div></nav>
<main><div class="in">"""
FOOT = """</div></main>
<footer><a href="../../">GISP Prep</a> · <a href="../../gisp-exam-study-guide/">Study guide</a> · <a href="../../practice/">Practice online</a> · <a href="../">All categories</a> · <a href="https://ovelhanegra.io/">Ovelha Negra</a><p style="margin-top:8px">Independent study aid, not affiliated with or endorsed by the GIS Certification Institute (GISCI).</p></footer>
</body></html>"""

def qblock(q, n):
    opts = "".join(f"<li>{e(o)}</li>" for o in q["options"])
    return f"""<article class="q"><div class="m">Question {n} · {e(q['difficulty'])} · {e(q['type'])}</div><h3>{e(q['question'])}</h3><ol>{opts}</ol>
<details><summary>Show answer and explanation</summary><p><b>Answer: {"ABCD"[q['correctIndex']]}.</b> {e(q['explanation'])}</p></details></article>"""

def cta(d):
    return f"""<div class="cta"><b>Want the other {len([x for x in Q if x['domain']==d])-5} {e(d)} questions?</b><p style="color:var(--sub);margin-top:4px">All 400 questions are free to practice in your browser or in the iPhone app. Timed mock exams, analytics and the full flashcard library are a one-time unlock — no subscription.</p>
<div class="row"><a class="btn" href="../../practice/">Practice online, free</a><a class="btn ghost" href="https://apps.apple.com/us/app/gisp-prep-gis-exam-practice/id6785084756">Get the iPhone app</a><a class="btn ghost" href="../../gisp-exam-study-guide/">Read the study guide</a></div></div>"""

index_items = []
for d in DOMAINS:
    s = slug(d); url = f"{BASE}/questions/{s}/"
    rnd = random.Random(s)
    pool = [q for q in Q if q["domain"] == d]
    # 5 samples: 2 easy, 2 medium, 1 hard where possible
    pick = []
    for lv, k in (("Easy", 2), ("Medium", 2), ("Hard", 1)):
        c = [q for q in pool if q["difficulty"] == lv]; rnd.shuffle(c); pick += c[:k]
    title = f"{d}: GISP Practice Questions (with answers) | GISP Prep"
    desc = f"Five free GISP exam practice questions on {d} with answers and explanations, from a bank of 400 covering all ten GISCI knowledge categories. Practice online or on iPhone."
    ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q["question"],"acceptedAnswer":{"@type":"Answer","text":f"{q['options'][q['correctIndex']]}. {q['explanation']}"}} for q in pick]})
    body = f"""<p style="color:var(--sub);font-weight:700;letter-spacing:.04em;text-transform:uppercase;font-size:.8rem">GISCI knowledge category {DOMAINS.index(d)+1} of 10</p>
<h1>{e(d)}: GISP practice questions</h1>
<p class="lead">{e(d)} on the GISP exam covers {e(BLURB[d])}. Here are five sample questions from our bank of {len(pool)} on this category, each with the answer and a short explanation.</p>
{''.join(qblock(q, i+1) for i, q in enumerate(pick))}
{cta(d)}
<h2>What this category tests</h2>
<p>{e(d)} is one of the ten knowledge categories in the official GISCI exam blueprint. Questions are vendor-neutral: they test concepts and professional judgement rather than the menus of one software package, and they come as conceptual, application, scenario and data-interpretation items. Expect the exam to mix easy recall with harder scenario questions where you must choose the best course of action.</p>
<h2>Other categories</h2><div class="cats">{''.join(f'<a href="../{slug(x)}/">{e(x)}</a>' for x in DOMAINS if x != d)}</div>
<p style="margin-top:22px"><a href="../../gisp-exam-study-guide/">How to study for the GISP exam: a complete guide →</a></p>"""
    (OUT / s).mkdir(parents=True, exist_ok=True)
    (OUT / s / "index.html").write_text(HEAD.format(title=e(title), desc=e(desc), url=url, ld=ld) + body + FOOT)
    index_items.append((d, s, len(pool), BLURB[d]))

# index page
url = f"{BASE}/questions/"
title = "GISP Practice Questions by Category — Free Samples with Answers | GISP Prep"
desc = "Free GISP exam practice questions for each of the ten GISCI knowledge categories, with answers and explanations. From a 400-question bank you can practice online or on iPhone."
ld = json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":title,"url":url,"hasPart":[{"@type":"WebPage","name":f"{d}: GISP practice questions","url":f"{BASE}/questions/{s}/"} for d,s,_,_ in index_items]})
items = "".join(f'<article class="q"><h3 style="margin:0 0 4px"><a href="{s}/">{e(d)}</a></h3><p style="color:var(--sub)">{e(b)}. <b>{n} questions</b> in the bank; five free samples on the page.</p></article>' for d,s,n,b in index_items)
body = f"""<h1>GISP practice questions by category</h1>
<p class="lead">The GISCI exam blueprint has ten knowledge categories. Each page below gives five free sample questions with answers and explanations, drawn from our bank of {len(Q)}. Practice the whole bank free online or in the iPhone app.</p>
{items}
{cta(DOMAINS[0]).replace(f"Want the other {len([x for x in Q if x['domain']==DOMAINS[0]])-5} {e(DOMAINS[0])} questions?", "Ready to practice all 400?")}"""
(OUT / "index.html").write_text(HEAD.replace('href="../../', 'href="../').format(title=e(title), desc=e(desc), url=url, ld=ld).replace('href="../practice/"','href="../practice/"') + body.replace('href="../../','href="../') + FOOT.replace('href="../../','href="../').replace('<a href="../">All categories</a> · ',''))
print("wrote", len(index_items), "category pages + index to", OUT)
