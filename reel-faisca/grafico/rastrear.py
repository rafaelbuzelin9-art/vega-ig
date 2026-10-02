"""Rastreia o celular quadro a quadro e grava o quadrilátero da tela por quadro.

Uso: python3 rastrear.py <cena> <video> <quadro_ref> x0,y0 x1,y1 x2,y2 x3,y3 [t_ini t_fim]
Saída: quads-<cena>.js com window.QUADS = [[[x,y],...4], ...] (um por quadro).
Método: registro direto de cada quadro contra o quadro de referência (ECC, movimento afim)
sobre imagem de bordas, com máscara numa coroa em volta da tela; inicializa cada quadro com o
resultado do vizinho (sem acumular erro, porque o alvo é sempre a referência). Fora de
[t_ini, t_fim] a tela não aparece, então copia o quadro mais próximo.
"""
import sys, json, cv2, numpy as np

cena, video, qref = sys.argv[1], sys.argv[2], int(sys.argv[3])
Q = np.array([[float(v) for v in p.split(',')] for p in sys.argv[4:8]], dtype=np.float32)
t_ini = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0
t_fim = float(sys.argv[9]) if len(sys.argv) > 9 else 1e9
FPS = 24

cap = cv2.VideoCapture(video)
frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY))
n = len(frames); H, W = frames[0].shape

def bordas(g):
    g = cv2.GaussianBlur(g, (5, 5), 0)
    sx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3); sy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    m = cv2.magnitude(sx, sy)
    m = cv2.GaussianBlur(m, (7, 7), 0)
    return (m / (m.max() + 1e-6)).astype(np.float32)

poly = Q.reshape(-1, 1, 2).astype(np.int32)
m_in = np.zeros((H, W), np.uint8); cv2.fillPoly(m_in, [poly], 255)
k_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
k_big = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (61, 61))
mask = (cv2.dilate(m_in, k_big) & ~cv2.dilate(m_in, k_small)).astype(np.uint8)

ref = bordas(frames[qref])
crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1e-5)
i0, i1 = max(0, int(t_ini * FPS)), min(n - 1, int(t_fim * FPS))

warps = [None] * n; cc = [0.0] * n
warps[qref] = np.eye(2, 3, dtype=np.float32); cc[qref] = 1.0
for direcao in (1, -1):
    w = np.eye(2, 3, dtype=np.float32); i = qref
    while i0 <= i + direcao <= i1:
        j = i + direcao
        cur = bordas(frames[j])
        try:
            c, w2 = cv2.findTransformECC(ref, cur, w.copy(), cv2.MOTION_AFFINE, crit, mask, 5)
            w = w2; cc[j] = float(c)
        except cv2.error:
            cc[j] = 0.0  # mantém o warp anterior
        warps[j] = w.copy()
        i = j

quads = []
ultimo = None
for i in range(n):
    w = warps[i]
    if w is None:
        w = warps[i0] if i < i0 else warps[i1]
    q = cv2.transform(Q.reshape(-1, 1, 2), w).reshape(-1, 2)
    quads.append(q)
arr = np.array(quads, dtype=np.float32)
sm = arr.copy()
for i in range(n):
    a, b = max(0, i - 1), min(n, i + 2)
    sm[i] = np.median(arr[a:b], axis=0)
desl = np.linalg.norm(sm - Q[None], axis=2).max(axis=1)
usados = [cc[i] for i in range(i0, i1 + 1)]
print(f'{cena}: {n} quadros; faixa {i0}-{i1}; correlação ECC min/med {min(usados):.2f}/{float(np.median(usados)):.2f}; falhas {sum(1 for c in usados if c == 0.0)}')
print(f'deslocamento máx. em relação à ref: {desl[i0:i1+1].max():.1f} px (quadro {int(i0 + desl[i0:i1+1].argmax())})')
with open(f'quads-{cena}.js', 'w') as f:
    f.write('window.QUADS=' + json.dumps([[[round(float(x), 2), round(float(y), 2)] for x, y in q] for q in sm]) + ';')
print('gravado', f'quads-{cena}.js')
