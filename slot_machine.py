import random

items = ['gpu', 'cpu', 'mbd', 'ram']
description = {"gpu": 50, "cpu": 30, "mbd": 20, "ram": 15}
spin_count = random.randint(3, 5)


def spin():
    global spin_count
    spin_count += random.randint(1, 3)
    item_zero = random.choice(items)
    item_first = random.choice(items)
    item_second = random.choice(items)
    if item_zero == item_first == item_second or\
            spin_count in range(random.randint(1, 25), random.randint(1, 25) + 11):
        if spin_count > 25:
            spin_count = random.randint(1, 3)
        else:
            spin_count += 2
        return [item_zero,
                item_zero,
                item_zero], description[item_zero], f'Вы выиграли {description[item_zero]} монет!'
    return [item_zero,
            item_first,
            item_second], 0, "Вы проиграли!"
