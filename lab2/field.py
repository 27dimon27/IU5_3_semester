def field(items, *args):
    assert len(args) > 0, "Необходимо передать хотя бы одно поле."
    for item in items:
        if len(args) == 1:
            value = item.get(args[0])
            if value:
                yield value
        else:
            result = {}
            for key in args:
                value = item.get(key)
                if value:
                    result[key] = value
            if result:
                yield result


goods = [{'title': 'Ковер', 'price': 2000, 'color': 'green'},
    {'title': 'Диван для отдыха', 'color': 'black'}]

print(list(field(goods, 'title')))
print(list(field(goods, 'title', 'price')))
print(list(field(goods, 'title', 'price', 'color')))