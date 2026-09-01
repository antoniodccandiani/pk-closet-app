"""
PK Closet - Compositor de Artes
Estilo travado: delicado, logo oficial, tipografia limpa
"""

from __future__ import annotations
from datetime import date
from pathlib import Path
from typing import Optional
import random
import math

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
OUTPUT = ROOT / "output"
OUTPUT.mkdir(exist_ok=True)

LOGO_PATH = ASSETS / "logo_oficial.png"

FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def richer_delicate_bg(seed: int = 42) -> Image.Image:
    random.seed(seed)
    w, h = 1080, 1920
    base = Image.new("RGB", (w, h))
    pixels = base.load()
    for y in range(h):
        t = y / h
        r = int(252 - 8 * t)
        g = int(247 - 10 * t)
        b = int(242 - 9 * t)
        for x in range(w):
            noise = random.randint(-3, 3)
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    palette = [
        (236, 208, 200, 55), (245, 222, 215, 40), (228, 195, 188, 48),
        (250, 232, 225, 35), (220, 185, 178, 42), (242, 218, 210, 38),
    ]

    for i in range(18):
        r = random.randint(140, 480)
        x = random.randint(-150, 1200)
        y = random.randint(-200, 2100)
        c = random.choice(palette)
        rx = r + random.randint(-40, 80)
        ry = r + random.randint(-60, 40)
        draw.ellipse([x - rx, y - ry, x + rx, y + ry], fill=c)

    for i in range(5):
        points = []
        y_base = random.randint(200, 1600)
        for x in range(0, 1080, 40):
            y = y_base + int(80 * math.sin(x / 180 + i)) + random.randint(-20, 20)
            points.append((x, y))
        if len(points) > 2:
            draw.line(points, fill=(235, 205, 198, 28), width=random.randint(40, 90))

    for i in range(7):
        r = random.randint(100, 250)
        x = random.randint(50, 1030)
        y = random.randint(100, 1800)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 250, 247, 22))

    composed = Image.alpha_composite(base.convert("RGBA"), overlay)
    composed = composed.filter(ImageFilter.GaussianBlur(radius=35))
    composed = composed.filter(ImageFilter.GaussianBlur(radius=25))
    composed = composed.convert("RGB")

    noise = Image.new("RGB", (w, h))
    npx = noise.load()
    for y in range(h):
        for x in range(w):
            v = random.randint(-6, 6)
            npx[x, y] = (128 + v, 128 + v, 128 + v)
    noise = noise.filter(ImageFilter.GaussianBlur(radius=1.5))
    composed = Image.blend(composed, noise, 0.04)

    enhancer = ImageEnhance.Color(composed)
    composed = enhancer.enhance(1.06)
    enhancer = ImageEnhance.Contrast(composed)
    composed = enhancer.enhance(1.04)
    enhancer = ImageEnhance.Brightness(composed)
    composed = enhancer.enhance(1.02)
    return composed


def _paste_logo(im: Image.Image, size: int = 236, y: int = 160) -> None:
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((size, size), Image.Resampling.LANCZOS)
    x = (1080 - size) // 2
    im.paste(logo, (x, y), logo)


def create_bom_dia(frase: str, cta: str = "Siga @pkclosetrp") -> Path:
    bg = richer_delicate_bg(seed=random.randint(1, 9999))
    im = bg.convert("RGBA")
    draw = ImageDraw.Draw(im)

    _paste_logo(im, size=236, y=160)

    # Título
    titulo = "Bom dia"
    font_t = get_font(FONT_SERIF, 66)
    bb = draw.textbbox((0, 0), titulo, font=font_t)
    tw = bb[2] - bb[0]
    draw.text(((1080 - tw) // 2, 520), titulo, font=font_t, fill=(48, 36, 32))

    # Frase
    font_m = get_font(FONT_REG, 32)
    words = frase.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0, 0), test, font=font_m)[2] < 820:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)

    y = 625
    for line in lines:
        bb = draw.textbbox((0, 0), line, font=font_m)
        tw = bb[2] - bb[0]
        draw.text(((1080 - tw) // 2, y), line, font=font_m, fill=(52, 40, 36))
        y += 46

    y += 18
    draw.line([(340, y), (740, y)], fill=(180, 145, 140), width=1)

    # Elemento sutil
    mid_y = 980
    s = 7
    cx = 540
    draw.polygon([(cx, mid_y - s), (cx + s, mid_y), (cx, mid_y + s), (cx - s, mid_y)], fill=(185, 150, 145))
    draw.line([(290, mid_y), (500, mid_y)], fill=(200, 170, 165), width=1)
    draw.line([(580, mid_y), (790, mid_y)], fill=(200, 170, 165), width=1)

    # CTA
    font_c = get_font(FONT_REG, 26)
    bb = draw.textbbox((0, 0), cta, font=font_c)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    bw, bh = tw + 90, th + 34
    bx = (1080 - bw) // 2
    by = 1320
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=26, fill=(196, 149, 149))
    draw.text((bx + (bw - tw) // 2, by + (bh - th) // 2 - 1), cta, font=font_c, fill=(255, 255, 255))

    # Data
    data_str = date.today().strftime("%d/%m/%Y")
    font_d = get_font(FONT_REG, 18)
    bb = draw.textbbox((0, 0), data_str, font=font_d)
    tw = bb[2] - bb[0]
    draw.text(((1080 - tw) // 2, 1760), data_str, font=font_d, fill=(150, 130, 120))

    final = im.convert("RGB")
    out_name = f"PK_BomDia_{date.today().isoformat()}.png"
    out_path = OUTPUT / out_name
    final.save(out_path, "PNG", optimize=True)
    return out_path


def create_funcionamento(
    data_obj: date,
    horario: str,
    mensagem: str = "Estamos de portas abertas para te receber com carinho. Venha nos visitar e se sentir especial.",
    cta: str = "Te esperamos na loja",
) -> Path:
    bg = richer_delicate_bg(seed=random.randint(1, 9999))
    im = bg.convert("RGBA")
    draw = ImageDraw.Draw(im)

    _paste_logo(im, size=228, y=140)

    dias = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira",
            "Sexta-feira", "Sábado", "Domingo"]
    dia_semana = dias[data_obj.weekday()]
    data_str = data_obj.strftime("%d/%m/%Y")

    # Título
    titulo = "Funcionamento"
    font_t = get_font(FONT_SERIF, 50)
    bb = draw.textbbox((0, 0), titulo, font=font_t)
    tw = bb[2] - bb[0]
    draw.text(((1080 - tw) // 2, 410), titulo, font=font_t, fill=(48, 36, 32))

    # Data
    info = f"{dia_semana}, {data_str}"
    font_info = get_font(FONT_REG, 27)
    bb = draw.textbbox((0, 0), info, font=font_info)
    tw = bb[2] - bb[0]
    draw.text(((1080 - tw) // 2, 485), info, font=font_info, fill=(95, 75, 70))

    draw.line([(370, 540), (710, 540)], fill=(180, 145, 140), width=1)

    # Horário
    font_h = get_font(FONT_BOLD, 44)
    bb = draw.textbbox((0, 0), horario, font=font_h)
    tw = bb[2] - bb[0]
    draw.text(((1080 - tw) // 2, 585), horario, font=font_h, fill=(48, 36, 32))

    # Mensagem
    font_m = get_font(FONT_REG, 29)
    words = mensagem.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textbbox((0, 0), test, font=font_m)[2] < 820:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)

    y = 690
    for line in lines:
        bb = draw.textbbox((0, 0), line, font=font_m)
        tw = bb[2] - bb[0]
        draw.text(((1080 - tw) // 2, y), line, font=font_m, fill=(55, 42, 38))
        y += 43

    # Endereço
    font_end = get_font(FONT_REG, 23)
    end1 = "Rua Henrique Dumont, 748 — Jardim Paulista"
    end2 = "Em frente ao Supermercado Savegnago"
    bb = draw.textbbox((0, 0), end1, font=font_end)
    tw = bb[2] - bb[0]
    draw.text(((1080 - tw) // 2, 880), end1, font=font_end, fill=(110, 90, 85))
    bb = draw.textbbox((0, 0), end2, font=font_end)
    tw = bb[2] - bb[0]
    draw.text(((1080 - tw) // 2, 920), end2, font=font_end, fill=(110, 90, 85))

    # Elemento sutil
    mid_y = 1060
    s = 7
    cx = 540
    draw.polygon([(cx, mid_y - s), (cx + s, mid_y), (cx, mid_y + s), (cx - s, mid_y)], fill=(185, 150, 145))
    draw.line([(310, mid_y), (510, mid_y)], fill=(200, 170, 165), width=1)
    draw.line([(570, mid_y), (770, mid_y)], fill=(200, 170, 165), width=1)

    # CTA
    font_c = get_font(FONT_REG, 26)
    bb = draw.textbbox((0, 0), cta, font=font_c)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    bw, bh = tw + 90, th + 34
    bx = (1080 - bw) // 2
    by = 1240
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=26, fill=(196, 149, 149))
    draw.text((bx + (bw - tw) // 2, by + (bh - th) // 2 - 1), cta, font=font_c, fill=(255, 255, 255))

    final = im.convert("RGB")
    out_name = f"PK_Funcionamento_{data_obj.isoformat()}.png"
    out_path = OUTPUT / out_name
    final.save(out_path, "PNG", optimize=True)
    return out_path


def gerar_legenda_produto(nome_peca: str, cores: str = "", preco: str = "") -> str:
    """
    Gera legenda curta, humanizada, com desejo de compra.
    Máximo 5 hashtags. Foco em viralizar pelo Brasil.
    """
    aberturas = [
        f"Essa {nome_peca.lower()} foi feita para te deixar confiante.",
        f"Quando você veste essa {nome_peca.lower()}, o dia muda de figura.",
        f"Tem peça que abraça o corpo e a autoestima ao mesmo tempo.",
        f"Se você procura se sentir especial sem esforço, essa é a peça.",
        f"A gente criou essa {nome_peca.lower()} pensando em você se olhando no espelho e sorrindo.",
    ]

    desejo = [
        "Leve, delicada e com aquele caimento que valoriza.",
        "Perfeita para o dia a dia e para os momentos em que você quer se sentir mais você.",
        "O tipo de peça que você coloca e já recebe elogio.",
        "Conforto e elegância no mesmo look.",
        "Feita para mulheres que gostam de se sentir bonitas de verdade.",
    ]

    fechamento = [
        "Disponível para todo o Brasil. Chama no direct ou visita a loja.",
        "Enviamos para todo o Brasil. Te esperamos.",
        "Compre online ou venha nos visitar em Ribeirão Preto.",
        "Parcelamos em até 10x sem juros. Enviamos para todo o Brasil.",
    ]

    hashtags = [
        "#PKCloset",
        "#ModaFeminina",
        "#LookDoDia",
        "#ModaBrasil",
        "#EstiloFeminino",
    ]

    legenda = f"{random.choice(aberturas)} {random.choice(desejo)}"
    if cores:
        legenda += f" Disponível em {cores}."
    if preco:
        legenda += f" Por {preco}."
    legenda += f" {random.choice(fechamento)}"
    legenda += "\n\n" + " ".join(hashtags)

    return legenda


def gerar_legenda_produto(nome_peca: str, cores: str = "", preco: str = "") -> str:
    """
    Legenda curta, humanizada, com desejo de compra e potencial de viralização.
    Exatamente 5 hashtags. Foco em todo o Brasil.
    """
    import random

    aberturas = [
        f"Essa {nome_peca.lower()} foi feita para o seu corpo e para a sua autoestima.",
        f"Quando você veste essa {nome_peca.lower()}, o dia ganha outro significado.",
        f"Tem peça que abraça, valoriza e te faz se sentir mais você.",
        f"Se você quer se sentir especial sem esforço, essa é a peça.",
        f"A gente pensou em você se olhando no espelho e sorrindo de verdade.",
        f"Essa {nome_peca.lower()} não é só roupa. É a sensação de estar bem.",
    ]

    desejo = [
        "Caimento que valoriza, tecido que abraça e aquele toque de delicadeza que faz diferença.",
        "Leve, elegante e com o conforto que a gente ama no dia a dia.",
        "O tipo de peça que você coloca e já recebe elogio.",
        "Perfeita para quem gosta de se sentir bonita de verdade, sem exagero.",
        "Feita para mulheres que querem se olhar no espelho e gostar do que veem.",
    ]

    fechamento = [
        "Enviamos para todo o Brasil. Chama no direct.",
        "Disponível para todo o Brasil. Te esperamos na loja ou online.",
        "Parcelamos em até 10x sem juros. Envio para todo o Brasil.",
        "Compre online ou visite a loja em Ribeirão Preto. Enviamos para o Brasil todo.",
    ]

    # Hashtags fixas e estratégicas (máximo 5)
    hashtags = "#PKCloset #ModaFeminina #LookDoDia #ModaBrasil #EstiloFeminino"

    legenda = f"{random.choice(aberturas)} {random.choice(desejo)}"
    if cores:
        legenda += f" Disponível em {cores}."
    if preco:
        legenda += f" Por {preco}."
    legenda += f" {random.choice(fechamento)}"
    legenda += f"\n\n{hashtags}"
    return legenda


def create_produto(
    foto_path: Path,
    nome: str,
    cores: str = "",
    grade: str = "",
    preco: str = None,
    formato: str = "story",  # story | post
) -> Path:
    """
    Compõe arte de produto com a foto ORIGINAL intacta.
    Nunca redesenha, recolore ou altera a peça.
    """
    from PIL import Image, ImageDraw, ImageFont
    import random
    from datetime import date

    if formato == "story":
        W, H = 1080, 1920
        foto_max_h = int(H * 0.48)
        logo_size = 200
        logo_y = 110
    else:
        W, H = 1080, 1350
        foto_max_h = int(H * 0.50)
        logo_size = 180
        logo_y = 80

    bg = richer_delicate_bg(seed=random.randint(1, 9999))
    if formato == "post":
        bg = bg.crop((0, 0, 1080, 1350))
    im = bg.convert("RGBA")
    draw = ImageDraw.Draw(im)

    # Logo oficial
    logo = Image.open(LOGO_PATH).convert("RGBA")
    logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    lx = (W - logo_size) // 2
    im.paste(logo, (lx, logo_y), logo)

    # Foto do produto — INTACTA
    foto = Image.open(foto_path).convert("RGBA")
    # Redimensiona proporcionalmente sem cortar a peça
    fw, fh = foto.size
    ratio = min((W * 0.78) / fw, foto_max_h / fh)
    new_w = int(fw * ratio)
    new_h = int(fh * ratio)
    foto = foto.resize((new_w, new_h), Image.Resampling.LANCZOS)

    foto_x = (W - new_w) // 2
    foto_y = logo_y + logo_size + 40
    im.paste(foto, (foto_x, foto_y), foto if foto.mode == "RGBA" else None)

    # Textos abaixo da foto
    y_text = foto_y + new_h + 50

    # Nome da peça
    font_nome = get_font(FONT_SERIF, 36)
    bb = draw.textbbox((0, 0), nome, font=font_nome)
    tw = bb[2] - bb[0]
    draw.text(((W - tw) // 2, y_text), nome, font=font_nome, fill=(48, 36, 32))
    y_text += 50

    # Cores + Grade
    info_parts = []
    if cores:
        info_parts.append(cores)
    if grade:
        info_parts.append(f"Grade: {grade}")
    if info_parts:
        info = "  •  ".join(info_parts)
        font_info = get_font(FONT_REG, 24)
        bb = draw.textbbox((0, 0), info, font=font_info)
        tw = bb[2] - bb[0]
        draw.text(((W - tw) // 2, y_text), info, font=font_info, fill=(90, 70, 65))
        y_text += 40

    # Preço
    if preco:
        font_preco = get_font(FONT_BOLD, 32)
        bb = draw.textbbox((0, 0), preco, font=font_preco)
        tw = bb[2] - bb[0]
        draw.text(((W - tw) // 2, y_text), preco, font=font_preco, fill=(48, 36, 32))
        y_text += 50

    # CTA
    cta = "Chama no direct"
    font_c = get_font(FONT_REG, 24)
    bb = draw.textbbox((0, 0), cta, font=font_c)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]
    bw, bh = tw + 80, th + 28
    bx = (W - bw) // 2
    by = min(y_text + 30, H - 120)
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=22, fill=(196, 149, 149))
    draw.text((bx + (bw - tw) // 2, by + (bh - th) // 2 - 1), cta, font=font_c, fill=(255, 255, 255))

    final = im.convert("RGB")
    suffix = "Story" if formato == "story" else "Post"
    out_name = f"PK_Produto_{nome.replace(' ', '_')[:30]}_{suffix}.png"
    out_path = OUTPUT / out_name
    final.save(out_path, "PNG", optimize=True)
    return out_path


def create_produto_modelo_virtual(
    nome: str,
    cores: str = "",
    grade: str = "",
    preco: str = None,
    formato: str = "story",
    descricao_peca: str = "",
) -> Path:
    """
    Gera arte conceitual com modelo virtual.
    IMPORTANTE: resultado é simulação, não reprodução fiel da peça.
    """
    # Esta função é um placeholder estrutural.
    # A geração real da imagem da modelo é feita no app via Grok Imagine
    # e depois composta com logo + textos.
    # Por enquanto retorna None para o app tratar o fluxo de geração.
    return None
