"""営業DM用：お店のスマホLP（390px幅）を組み立てて、DMに添付する画像（01〜05.jpg）を書き出す。
使い方: python3 tools/dm_lp.py <shop.json> <hero.html> <出力フォルダ>
  shop.json : 1店分のデータ（形式は templates/dm_lp_sample.json）。確かめた事実だけを入れ、分からない所は [ ] にする。
  hero.html : トップ案（Design）のスマホ1画面目の中身（<div style="width:390px;height:844px">…</div>）。
フォントは初回に tools/dm_fonts.py が /tmp/dm_fonts に取ってくる。
"""
import json, sys, os, html, subprocess
from playwright.sync_api import sync_playwright

BASE = os.path.dirname(os.path.abspath(__file__))
FD = '/tmp/dm_fonts'
if not os.path.exists(os.path.join(FD, 'fonts.css')):
    import subprocess; subprocess.run([sys.executable, os.path.join(BASE, 'dm_fonts.py')], check=True)
FONTS = open(os.path.join(FD, 'fonts.css')).read()
E = html.escape

def sec(t, inner, bg=None):
    return f'<section style="padding:44px 24px;{"background:"+bg+";" if bg else ""}">{inner}</section>'

def head(t, label, h):
    return (f'<p class="lb">{E(label)}</p>'
            f'<h2 class="h2">{h}</h2>')

def build(s):
    t = s['theme']
    out = []
    # 1. hero（既存のトップ案）
    out.append(f'<div class="hero">{open(s["_hero"]).read()}</div>')
    c = s['concept']
    out.append(sec(t, head(t, c.get('label', 'CONCEPT'), c['h']) +
        f'<p class="p">{c["p"]}</p>'
        f'<div class="ph" style="height:220px;margin-top:22px">{E(c["ph"])}</div>'))
    # 2. こだわり
    cards = ''.join(f'<div class="card"><span class="no">0{i+1}</span><h3 class="h3">{E(a)}</h3><p class="p sm">{b}</p></div>'
                    for i, (a, b) in enumerate(s['features']))
    out.append(sec(t, head(t, 'POINT', s.get('featuresH', E(s['name']) + 'のこだわり')) + f'<div class="cards">{cards}</div>', t['bg2']))
    # 3. メニュー
    m = s['menu']
    rows = ''.join(f'<div class="row"><span>{E(a)}</span><span class="pr">{E(b)}</span></div>' for a, b in m['items'])
    out.append(sec(t, head(t, 'MENU', m.get('h', 'メニューと料金')) +
        f'<div class="list">{rows}</div><p class="note">{E(m.get("note", "※ 料金・時間は仮のものです。"))}</p>'))
    # 4. 流れ
    st = ''.join(f'<div class="step"><span class="sn">STEP {i+1}</span><div><h3 class="h3">{E(a)}</h3><p class="p sm">{b}</p></div></div>'
                 for i, (a, b) in enumerate(s['flow']))
    out.append(sec(t, head(t, 'FLOW', s.get('flowH', 'ご予約の流れ')) + f'<div class="steps">{st}</div>', t['bg2']))
    # 5. お知らせ
    nw = ''.join(f'<div class="news"><span class="dt">{E(d)}</span><span>{E(x)}</span></div>' for d, x in s['news'])
    out.append(sec(t, head(t, 'NEWS', 'お知らせ') + f'<div class="list">{nw}</div>'
        '<p class="note">※ 季節のお知らせや営業日の変更を、このように日付つきで載せられます。</p>'))
    # 6. よくある質問
    fq = ''.join(f'<div class="qa"><p class="q"><b>Q</b>{E(q)}</p><p class="a"><b>A</b>{a}</p></div>' for q, a in s['faq'])
    out.append(sec(t, head(t, 'FAQ', 'よくあるご質問') + f'<div class="faq">{fq}</div>', t['bg2']))
    # 7. アクセス
    ac = ''.join(f'<div class="row ac"><span class="k">{E(k)}</span><span>{v}</span></div>' for k, v in s['access'])
    out.append(sec(t, head(t, 'ACCESS', 'アクセス・営業時間') +
        '<div class="ph" style="height:180px;margin-bottom:18px">[ 地図 ]</div>' + f'<div class="list">{ac}</div>'))
    # 8. CTA
    ct = s['cta']
    out.append(f'<section class="cta"><h2 class="h2" style="color:#fff">{ct["h"]}</h2><p class="p" style="color:rgba(255,255,255,.88)">{ct["p"]}</p>'
               f'<a class="b1">{E(ct["b1"])}</a>' + (f'<a class="b2">{E(ct["b2"])}</a>' if ct.get('b2') else '') + '</section>')
    out.append(f'<footer><div class="logo">{s["logo"]}</div><p>ご提案用イメージ（写真・文章・料金は仮のものです）<br>制作：ICHIMAI.</p></footer>')
    css = f"""{FONTS}
body{{margin:0;background:{t['bg']};color:{t['ink']};font-family:{t['bf']};-webkit-font-smoothing:antialiased}}
a{{color:inherit;text-decoration:none}} *{{box-sizing:border-box}}
.page{{width:390px}} section{{position:relative}}
.lb{{margin:0 0 8px;font-size:11px;letter-spacing:.22em;color:{t['accent']};font-weight:700}}
.h2{{margin:0 0 16px;font-family:{t['hf']};font-weight:{t['hw']};font-size:24px;line-height:1.5;color:{t['ink']}}}
.h3{{margin:0 0 6px;font-family:{t.get('h3f',t['hf'])};font-weight:{t.get('h3w',t['hw'])};font-size:17px;line-height:1.5}}
.p{{margin:0;font-size:14px;line-height:1.9;color:{t['sub']}}} .p.sm{{font-size:13px;line-height:1.8}}
.ph{{border-radius:{t['r']};background:{t['soft']};display:flex;align-items:center;justify-content:center;font-size:12px;color:{t['sub']}}}
.cards{{display:flex;flex-direction:column;gap:12px}}
.card{{background:{t['card']};border-radius:{t['r']};padding:20px 20px 18px}}
.no{{display:block;font-family:{t['hf']};font-size:13px;color:{t['accent']};margin-bottom:6px;letter-spacing:.1em}}
.list{{border-top:1px solid {t['line']}}}
.row{{display:flex;justify-content:space-between;gap:16px;padding:14px 2px;border-bottom:1px solid {t['line']};font-size:14px;line-height:1.6}}
.row .pr{{white-space:nowrap;color:{t['accent']};font-weight:700}}
.row.ac{{justify-content:flex-start}} .row .k{{flex:0 0 72px;color:{t['sub']};font-size:12px;padding-top:2px}}
.note{{margin:12px 0 0;font-size:11px;color:{t['sub']}}}
.steps{{display:flex;flex-direction:column;gap:14px}}
.step{{display:flex;gap:14px;background:{t['card']};border-radius:{t['r']};padding:18px}}
.sn{{flex:0 0 auto;font-size:10px;letter-spacing:.12em;color:#fff;background:{t['accent']};border-radius:999px;padding:4px 9px;height:fit-content;margin-top:3px}}
.news{{display:flex;gap:14px;padding:14px 2px;border-bottom:1px solid {t['line']};font-size:14px}}
.dt{{flex:0 0 auto;color:{t['sub']};font-size:12px;padding-top:2px}}
.faq{{display:flex;flex-direction:column;gap:12px}}
.qa{{background:{t['card']};border-radius:{t['r']};padding:18px}}
.q,.a{{margin:0;display:flex;gap:10px;font-size:14px;line-height:1.75}} .q{{font-weight:700;margin-bottom:8px}} .a{{color:{t['sub']};font-size:13px}}
.q b,.a b{{flex:0 0 auto;font-family:{t['hf']};color:{t['accent']}}} .a b{{color:{t['sub']}}}
.cta{{background:{t['accent']};padding:48px 24px;display:flex;flex-direction:column;gap:12px}}
.cta .h2{{margin:0}} .cta .p{{margin-bottom:10px}}
.b1,.b2{{display:block;text-align:center;border-radius:{t['br']};padding:16px;font-size:15px;font-weight:700}}
.b1{{background:#fff;color:{t['accent']}}} .b2{{border:1.5px solid rgba(255,255,255,.9);color:#fff}}
footer{{padding:36px 24px 30px;text-align:center}} footer .logo{{margin-bottom:12px}}
footer p{{margin:0;font-size:10px;line-height:1.8;color:{t['sub']}}}
"""
    return f"<!doctype html><html lang='ja'><head><meta charset='utf-8'><style>{css}</style></head><body><div class='page'>{''.join(out)}</div></body></html>"

def render(shops, ids, outdir):
    os.makedirs(outdir, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg = b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
        for s in shops:
            if ids and s['id'] not in ids: continue
            fn = os.path.join(FD, f'lp_{s["id"]}.html')
            open(fn, 'w').write(build(s))
            pg.goto('file://' + fn); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(700)
            # セクションの区切りで画面ごとにまとめる（1枚の高さは最大 900px）
            tops = pg.evaluate("[...document.querySelector('.page').children].map(e=>[e.offsetTop,e.offsetHeight])")
            H = pg.evaluate("document.querySelector('.page').offsetHeight")
            groups, cur = [], None
            for y, h in tops:
                if cur and cur[0] > 0 and (y + h - cur[0]) <= 1250: cur[1] = y + h
                else:
                    if cur: groups.append(cur)
                    cur = [y, y + h]
            groups.append(cur)
            d = outdir
            for i, (y0, y1) in enumerate(groups):
                png = os.path.join(d, f'{i+1:02d}.png')
                pg.screenshot(path=png, full_page=True, clip={'x': 0, 'y': y0, 'width': 390, 'height': y1 - y0})
                subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', png, '-q:v', '3', png[:-4] + '.jpg'], check=True); os.remove(png)
            print(s['id'], 'slides', len(groups), 'height', H)
        b.close()

if __name__ == '__main__':
    import subprocess
    shop = json.load(open(sys.argv[1])); shop['_hero'] = sys.argv[2]
    shop.setdefault('id', 'shop')
    render([shop], [], sys.argv[3])
