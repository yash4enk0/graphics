from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_test_texture():
    img = Image.new('RGB', (512, 512), color=(200, 200, 200))
    draw = ImageDraw.Draw(img)

    colors = [
        (255, 220, 180),
        (180, 50, 50),
        (200, 100, 100),
        (255, 240, 200),
    ]
    
    draw.rectangle([0, 0, 255, 255], fill=colors[0])
    draw.rectangle([256, 0, 511, 255], fill=colors[1])
    draw.rectangle([0, 256, 255, 511], fill=colors[2])
    draw.rectangle([256, 256, 511, 511], fill=colors[3])
    
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 25)
    except:
        font = ImageFont.load_default()
    
    labels = [
        (1, 10, 10),    (2, 220, 10),    (3, 270, 10),     (4, 470, 10),
        (5, 10, 210),   (6, 220, 210),   (7, 270, 210),    (9, 470, 210),
        (9, 10, 270),   (10, 215, 270),  (11, 265, 270),   (12, 465, 270),
        (13, 10, 470),  (14, 215, 470),  (15, 265, 470),   (16, 465, 470),
    ]
    
    for num, x, y in labels:
        draw.text((x+2, y+2), str(num), fill=(0, 0, 0), font=font)
        draw.text((x, y), str(num), fill=(255, 255, 255), font=font)
    
    img.save('media/texture.bmp')

def create_wood_textures():
    light_wood = Image.new('RGB', (256, 256))
    pixels = light_wood.load()
    
    for i in range(256):
        for j in range(256):
            base = 210 - (np.sin(i * 0.05) * 15)
            r = int(base)
            g = int(base - 30)
            b = int(base - 70)
            pixels[i, j] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    light_wood.save('media/1.bmp')

    dark_wood = Image.new('RGB', (256, 256))
    pixels = dark_wood.load()
    
    for i in range(256):
        for j in range(256):
            base = 101 - (np.sin(i * 0.05) * 10)
            r = int(base)
            g = int(base - 34)
            b = int(base - 68)
            pixels[i, j] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
    
    dark_wood.save('media/2.bmp')

def create_2x2_checkerboard():
    try:
        light = Image.open('media/1.bmp')
        dark = Image.open('media/2.bmp')
    except:
        light = Image.new('RGB', (256, 256), color=(210, 180, 140))
        dark = Image.new('RGB', (256, 256), color=(101, 67, 33))
    
    checkerboard = Image.new('RGB', (512, 512))
    
    checkerboard.paste(dark, (0, 0))
    checkerboard.paste(light, (256, 0))
    checkerboard.paste(light, (0, 256))
    checkerboard.paste(dark, (256, 256))
    
    checkerboard.save('media/2x2.bmp')

def create_spiral_pattern():
    img = Image.new('RGB', (512, 512))
    pixels = img.load()
    
    for i in range(512):
        for j in range(512):
            x = (i - 256) / 512 * 8
            y = (j - 256) / 512 * 8
            
            r = np.sqrt(x*x + y*y)
            
            if x != 0:
                fi = np.arctan(y / x)
            else:
                fi = np.pi / 2
            
            value = abs(np.cos(8 * fi - r))
            
            if (value % 1.0) < 0.75:
                pixels[i, j] = (255, 255, 0)
            else:
                pixels[i, j] = (0, 0, 255)
    
    img.save('media/pattern.bmp')

def main():
    create_test_texture()
    create_wood_textures()
    create_2x2_checkerboard()
    create_spiral_pattern()


if __name__ == "__main__":
    main()