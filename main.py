from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

# Abrir a foto do usuário
foto = Image.open("dados/foto_usuario.jpg").convert("RGB")

# 1. Transformar em preto e branco
foto_pb = foto.convert("L")

# 2. Adicionar “traços” ou textura envelhecida (efeito amassado)
# Criar ruído simples
largura, altura = foto_pb.size
ruido = np.random.randint(0, 50, (altura, largura), dtype='uint8')
imagem_ruido = Image.fromarray(ruido, 'L')

# Misturar ruído com a foto
foto_textura = Image.blend(foto_pb, imagem_ruido, alpha=0.2)

# 3. Suavizar levemente e dar efeito antigo
foto_final = foto_textura.filter(ImageFilter.GaussianBlur(radius=1))
foto_final = ImageEnhance.Contrast(foto_final).enhance(1.2)

# Salvar a imagem processada
foto_final.save("dados/foto_envelhecida.jpg")
print("Imagem processada e salva em dados/foto_envelhecida.jpg")
