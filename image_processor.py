from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import os

def envelhecer_foto(caminho_entrada, caminho_saida):
    foto = Image.open(caminho_entrada).convert("RGB")

    # Preto e branco
    foto_pb = foto.convert("L")

    # Ruído (efeito antigo)
    largura, altura = foto_pb.size
    ruido = np.random.randint(0, 50, (altura, largura), dtype='uint8')
    imagem_ruido = Image.fromarray(ruido, 'L')

    foto_textura = Image.blend(foto_pb, imagem_ruido, alpha=0.2)

    # Suavização e contraste
    foto_final = foto_textura.filter(ImageFilter.GaussianBlur(radius=1))
    foto_final = ImageEnhance.Contrast(foto_final).enhance(1.2)

    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    foto_final.save(caminho_saida)

    return caminho_saida
