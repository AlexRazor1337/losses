import requests, re
from lxml import html


def parse_data(data):
    parsed = re.findall("\D+\d*.*?", data)
    parsed = [element.strip() for element in parsed]

    army_index = [idx for idx, s in enumerate(parsed) if 'Особовий склад' in s][0]
    army_joined = ' '.join(parsed[army_index:]).replace(' ,', ',')

    return parsed[:army_index] + [army_joined]


def load_data(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    data = tree.xpath('//ul[@class="see-also"]/li[@class="gold"][1]/div[@class="casualties"]/div/ul/li//text()[not(parent::small)]')
    date = tree.xpath('//ul[@class="see-also"]/li[@class="gold"][1]/span[@class="black"]/text()')[0]
    return ''.join(data).replace('\xa0', ' '), date


def main():
    URL = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
    data, date = load_data(URL)
    data = parse_data(data)
    print(data)

if __name__ == "__main__":
    main()
