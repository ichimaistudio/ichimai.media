"""営業DM用LPのフォント（Google Fonts の OFL フォント）を /tmp/dm_fonts に取得し fonts.css を作る。"""
import subprocess,urllib.parse,os
D='/tmp/dm_fonts'; os.makedirs(D,exist_ok=True); os.chdir(D); os.makedirs('fonts',exist_ok=True)
L={'Zen Kaku Gothic New':('zenkakugothicnew',['ZenKakuGothicNew-Regular.ttf:400','ZenKakuGothicNew-Medium.ttf:500','ZenKakuGothicNew-Bold.ttf:700']),
'Noto Serif JP':('notoserifjp',['NotoSerifJP[wght].ttf:200 900']),
'Italiana':('italiana',['Italiana-Regular.ttf:400']),
'Zen Maru Gothic':('zenmarugothic',['ZenMaruGothic-Regular.ttf:400','ZenMaruGothic-Medium.ttf:500','ZenMaruGothic-Bold.ttf:700','ZenMaruGothic-Black.ttf:900']),
'Quicksand':('quicksand',['Quicksand[wght].ttf:300 700']),
'Noto Sans JP':('notosansjp',['NotoSansJP[wght].ttf:100 900']),
'Cormorant Garamond':('cormorantgaramond',['CormorantGaramond[wght].ttf:300 700','CormorantGaramond-Italic[wght].ttf:300 700:i']),
'Shippori Mincho':('shipporimincho',['ShipporiMincho-Regular.ttf:400','ShipporiMincho-Medium.ttf:500','ShipporiMincho-SemiBold.ttf:600','ShipporiMincho-Bold.ttf:700','ShipporiMincho-ExtraBold.ttf:800']),
'DM Serif Display':('dmserifdisplay',['DMSerifDisplay-Regular.ttf:400']),
'Playfair Display':('playfairdisplay',['PlayfairDisplay[wght].ttf:400 900']),
'M PLUS 1p':('mplus1p',['MPLUS1p-Regular.ttf:400','MPLUS1p-Medium.ttf:500','MPLUS1p-Bold.ttf:700']),
'Marcellus':('marcellus',['Marcellus-Regular.ttf:400']),
'Dela Gothic One':('delagothicone',['DelaGothicOne-Regular.ttf:400']),
'Zen Kaku Gothic Antique':('zenkakugothicantique',['ZenKakuGothicAntique-Regular.ttf:400','ZenKakuGothicAntique-Medium.ttf:500','ZenKakuGothicAntique-Bold.ttf:700'])}
css=[]
for fam,(d,files) in L.items():
    for f in files:
        parts=f.split(':'); n=parts[0]; w=parts[1]; it=len(parts)>2
        p='fonts/'+n
        if not os.path.exists(p) or os.path.getsize(p)<1000:
            code=subprocess.run(['curl','-sSL','-o',p,'-w','%{http_code}','https://raw.githubusercontent.com/google/fonts/main/ofl/'+d+'/'+urllib.parse.quote(n)],capture_output=True,text=True).stdout
            if code!='200': print('MISS',n,code); os.remove(p) if os.path.exists(p) else None; continue
        css.append(f"@font-face{{font-family:'{fam}';src:url('file://{D}/fonts/{urllib.parse.quote(n)}');font-weight:{w};font-style:{'italic' if it else 'normal'}}}")
open('fonts.css','w').write('\n'.join(css)); print(len(css),'faces')
