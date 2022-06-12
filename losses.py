import requests, re, json, sys
from lxml import html
from tabulate import tabulate

import PIL.ImageEnhance as ImageEnhance
import PIL.Image as Image
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont


def tint_image(img, factor):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def draw_text_on_image(data, date, background_path, font_path, font_size, header_font_size, header_text, text_color='white', header_color='yellow'):
    HEADER_TEXT = header_text % date
    HEADER_COLOR = header_color  # TODO make it configurable
    HIGHLIGHT_COLOR = (255, 40, 0)
    TINT_AMOUNT = 0.35
    TEXT_COLOR = text_color

    img = tint_image(Image.open(background_path), TINT_AMOUNT)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, font_size)
    header_font = ImageFont.truetype(font_path, header_font_size)

    center_x, center_y = img.size[0] / 2, img.size[1] / 2
    start_y = center_y - ((len(data) + 1) * font_size) / 2

    draw.text(
        (center_x - draw.textsize(HEADER_TEXT, font=header_font)[0] / 2, start_y - 3 * header_font_size),
        HEADER_TEXT,
        font=header_font,
        align='center',
        fill=HEADER_COLOR
    )
    # iterate over data and draw each line of text
    for i, line in enumerate(data):
        text_width = draw.textsize(line[0], font=font)[0]
        draw.text(
            (center_x - text_width - 10, start_y + i * font_size),
            line[0] + ':',
            font=font,
            align='right',
            fill=TEXT_COLOR
        )

        if ', ' in line[1]:
            for j, sub_line in enumerate(line[1].split(', ')):
                draw.text(
                    (center_x + 10, start_y + i * font_size + j * font_size),
                    sub_line.split('(+')[0],
                    font=font,
                    align='left',
                    fill=TEXT_COLOR
                )
                if '(+' in sub_line:
                    draw.text(
                        (center_x + 10 + draw.textsize(sub_line.split('(+')[0], font=font)[0], start_y + i * font_size + j * font_size),
                        '(+' + sub_line.split('(+')[1],
                        font=font,
                        align='left',
                        fill=HIGHLIGHT_COLOR
                    )
        else:
            draw.text(
                (center_x + 10, start_y + i * font_size),
                line[1].split('(+')[0],
                font=font,
                align='left',
                fill=TEXT_COLOR
            )
            if '(+' in line[1]:
                draw.text(
                    (center_x + 10 + draw.textsize(line[1].split('(+')[0], font=font)[0], start_y + i * font_size),
                    '(+' + line[1].split('(+')[-1],
                    font=font,
                    align='left',
                    fill=HIGHLIGHT_COLOR
                )

    img.save('./result.jpg')


def print_table(headers, data):
    print(tabulate(data, headers, tablefmt='grid'))


def data_to_table(data):
    return [row.split(' — ') for row in data]


def strip_data(data):
    return [element.strip() for element in data if element.strip()]


def parse_data(data):
    result = re.findall('\D+\d*.*?[\s\(.?\d+\)]?', data)
    for i in range(len(result)):
        if '(+' in result[i]:
            result[i - 1] += result[i]
            result[i] = ''

    parsed = strip_data(result)

    try:
        army_index = [idx for idx, s in enumerate(parsed) if 'Особовий склад' in s][0]
        army_joined = ' '.join(parsed[army_index:]).replace(' ,', ',')

        return parsed[:army_index] + [army_joined]

    except IndexError:
        return parsed


def load_data(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    data = tree.xpath('//ul[@class="see-also"]/li[@class="gold"][1]/div[@class="casualties"]/div/ul/li//text()')
    date = tree.xpath('//ul[@class="see-also"]/li[@class="gold"][1]/span[@class="black"]/text()')[0]
    return ''.join(data).replace('\xa0', ' '), date


def main():
    URL = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
    data, date = load_data(URL)
    data = data_to_table(parse_data(data))

    # check if there is and argument and it is true
    if len(sys.argv) > 1 and sys.argv[1] == '-i':
        try:
            with open('./config.json', encoding='utf8') as config_file:
                config = json.load(config_file)
                draw_text_on_image(data, date, **config)
        except FileNotFoundError:
            print('Config file not found, creating new.')
            # create config.json file
            with open('./config.json', 'w', encoding='utf8') as config_file:
                json.dump(
                    {
                        'background_path': './resources/image.jpeg',
                        'font_path': './resources/font.ttf',
                        'font_size': 30,
                        'header_font_size': 46,
                        'header_text': 'Протягом 24.02-%s\n орієнтовані втрати противника склали:',
                        'text_color': 'white',
                        'header_color': 'yellow'
                    },
                    config_file,
                    indent=4,
                    ensure_ascii=False,
                )

    else:
        print_table(['Category', f'Amount of losses ({date})'], data)


if __name__ == '__main__':
    main()
