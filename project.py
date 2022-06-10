import requests, re
from lxml import html
from tabulate import tabulate


def print_table(headers, data):
    print(tabulate(data, headers, tablefmt='grid'))


def data_to_table(data):
    return [row.split(' — ') for row in data]


def strip_data(data):
    return [element.strip() for element in data]


def parse_data(data):
    parsed = strip_data(re.findall("\D+\d*.*?", data))

    try:
        army_index = [idx for idx, s in enumerate(parsed) if 'Особовий склад' in s][0]
        army_joined = ' '.join(parsed[army_index:]).replace(' ,', ',')

        return parsed[:army_index] + [army_joined]

    except IndexError:
        return parsed


def load_data(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    data = tree.xpath('//ul[@class="see-also"]/li[@class="gold"][1]/div[@class="casualties"]/div/ul/li//text()[not(parent::small)]')
    date = tree.xpath('//ul[@class="see-also"]/li[@class="gold"][1]/span[@class="black"]/text()')[0]
    return ''.join(data).replace('\xa0', ' '), date


def main():
    URL = 'https://index.minfin.com.ua/ua/russian-invading/casualties/'
    data, date = load_data(URL)
    data = data_to_table(parse_data(data))

    headers = ['Category', f'Amount of losses ({date})']
    print_table(headers, data)


if __name__ == "__main__":
    main()
