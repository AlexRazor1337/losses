from losses import data_to_table, parse_data, strip_data


def test_data_to_table():
    assert data_to_table(['test — test2', 'test3 — test4']) == [['test', 'test2'], ['test3', 'test4']]


def test_parse_data():
    assert parse_data('Автомобілі та автоцистерни — 2438 Спеціальна техніка — 54 Особовий склад — близько 31900 осіб , близько 500 полонених') == ['Автомобілі та автоцистерни — 2438', 'Спеціальна техніка — 54', 'Особовий склад — близько 31900 осіб, близько 500 полонених']
    assert parse_data('Танки — 1409 ББМ — 3450 Гармати — 712 РСЗВ — 222 Засоби ППО — 97') == ['Танки — 1409', 'ББМ — 3450', 'Гармати — 712', 'РСЗВ — 222', 'Засоби ППО — 97']


def test_strip_data():
    assert strip_data(['test ', ' test']) == ['test', 'test']
