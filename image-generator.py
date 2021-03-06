from PIL import Image, ImageDraw
import numpy as np
import copy
import math

def alpha_channel_slice(array: np):
    (width, heigth, channels) = np.shape()
    return array[1:2:5]

def create_white_image(width, height, rgba_color=None):
    rgba_array = np.zeros((height, width, 4))
    if rgba_color is not None:
        # Fill with color
        ()

    rgba_array = np.array(rgba_array, dtype=np.uint8)
    return Image.fromarray(rgba_array)

def hex_rgb(hex_color: str):
    if hex_color.startswith('#'):
        hex_color = hex_color[1:]
    elif hex_color.startswith('0x'):
        hex_color = hex_color[2:]
    
    assert 6 == len(hex_color)

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)

assert hex_rgb('FF0033') == (255, 0, 51)

def hexarr_rgbarr(arr: list):
    return list(map(lambda c: hex_rgb(c), arr))

def main():

    black = (0,0,0)
    gray = (127,127,127)
    white = (255,255,255)
    red = (255,0,0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    cyan = (0, 255, 255)
    magenta = (255, 0, 255)
    yellow = (255, 255, 0)

    retro_palette = [ black, gray, white, red, green, blue, cyan, magenta, yellow ]

    sunset_palette = hexarr_rgbarr(['442c1b', '542715', '712f13', '8f3a14', '090504', 'c67b3f', 'e34410', 'e46418', 'f19329', 'f5b145', 'fcf0a3'])
    forrest_palette = hexarr_rgbarr([ '2b3443', '343446', '343c4a', '545b5c', '59665b', '5d666d', '646b60', '687763', '78846a', '7c9469', '879670', '97a578' ])
    grassland_palette = hexarr_rgbarr(['1c2d25', '29471a', '3d5227', '5e8069', '60861c', '6b8649', '6c8ba0', '7f9b22', '96aa2e', 'adc645', 'd4d21b', 'e5edf4'])
    lemon_candy_palette = hexarr_rgbarr(['ffd88e', 'ff8100', 'ffa100', 'ffb400', 'ffce00', 'ffe26a', 'ffeea5'])

    colors = grassland_palette

    raster_width = 250
    raster_heigth = 250

    block_width = 2
    block_heigth = 2

    image_width = raster_width * block_width
    image_heigth = raster_heigth * block_heigth

    draw_start_x = int (-1 * (raster_width / 2))
    draw_end_x = int(raster_width / 2)

    draw_start_y = int (-1 * (raster_width / 2))
    draw_end_y = int(raster_width / 2)

    coin = np.random.randint(0,2)
    random = int(np.random.normal(10 + (coin * np.random.normal(50, 1, 1)[0]), 20, 1)[0])


    frames = []
    for step in range(100, -1, -1):

        image = create_white_image(image_width, image_heigth)
        draw = ImageDraw.Draw(image)

        for x in range(0, raster_width):
            for y in range(0, raster_heigth):
                
                corruption = {
                    'distribution': 'uniform',
                    'factor': 45
                }

                if corruption['distribution'] == 'uniform':
                    random = np.random.randint(0,corruption['factor'])
                elif corruption['distribution'] == 'normal':
                    coin = np.random.randint(0,2)
                    random = int(np.random.normal(corruption['factor'], 10, 1)[0])

                # rasterkorrigiert
                o_x = abs(x - (raster_width / 2))
                o_y = abs(y - (raster_heigth / 2))

                shift = 10

                r = -1+int(math.sqrt(o_x**math.log((o_y+o_x*1.8+1)**1.1)+(o_y+o_x)**((step/10)+0.5))*-1.2) % 256 - int(random * o_x/40 + o_x/8 + o_y/6)
                g = -90+int(math.sqrt(o_x**math.log((o_y+o_x*1.85+1)**1.1)+(o_y+o_x)**((step/10)+0.5))*-1.2) % 256 - int(random * o_x/35 + o_y)
                b = -80+int(math.sqrt(o_x**math.log((o_y+o_x*1.6+1)**1.11)+(o_y+o_x)**((step/10)+0.50001))*-1.2) % 256 - int(random * o_x/70 + o_x*o_y/100)

                color = (r, g, b)

                draw.rectangle(
                    (x * block_width,
                    y * block_heigth,
                    (x + 1) * block_width,
                    (y + 1) * block_heigth),
                    fill=color)
        frames.append(image)

    frames[0].save('animation.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)
    #image.save('./generated-image.png')

if __name__ == "__main__":
    main()