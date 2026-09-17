from PIL import Image, ImageDraw
import math

CREME=(242,234,217); PRETO=(5,5,5); SEPIA=(110,98,83)
Wd,Ht=1080,1350
TEAR_Y=1096   # onde a folha rasga

base=Image.new("RGB",(Wd,Ht),CREME)
d=ImageDraw.Draw(base,"RGBA")

# grade de pontos 38px (padrao do campo VEGA)
for y in range(19,Ht,38):
    for x in range(19,Wd,38):
        d.ellipse((x-1.4,y-1.4,x+1.4,y+1.4), fill=SEPIA+(58,))

# luz quente vinda do alto-esquerdo (colhida do post 11)
luz=Image.new("RGBA",(Wd,Ht),(0,0,0,0)); dl=ImageDraw.Draw(luz)
for i in range(120,0,-1):
    r=i*14
    a=int(52*(1-i/120)**1.6)
    dl.ellipse((-460-r*0.25,-560-r*0.25,-460+r,-560+r), fill=(255,255,244,a))
base=Image.alpha_composite(base.convert("RGBA"),luz).convert("RGB")

# rasgo: tira vertical do post 11, girada para virar borda inferior
tira=Image.open(f"{__import__('os').path.dirname(__file__)}/assets/rasgo.png").convert("RGB")
tira=tira.rotate(90,expand=True)           # 1350 x 140
frat=537-518                                # fratura dentro da tira
tira=tira.crop((150,0,1230,44))


from PIL import Image as _I
msk=_I.new("L",tira.size,255); mp=msk.load()
for yy in range(tira.size[1]):
    v = 0 if yy < frat-16 else min(255, int(255*(yy-(frat-16))/10))
    for xx in range(tira.size[0]): mp[xx,yy]=v
base.paste(tira,(0,TEAR_Y-frat),msk)

# campo Preto Cine sob a folha rasgada
d=ImageDraw.Draw(base)
d.rectangle((0,TEAR_Y+12,Wd,Ht), fill=PRETO)
# fibra: o preto nao encosta na fratura, deixa o esgarcado aparecer
base.save(f"{__import__('os').path.dirname(__file__)}/assets/fundo.png")
print("fundo.png pronto", base.size, "rasgo em y=",TEAR_Y)
