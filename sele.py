f = open('demo.txt', 'r', encoding='utf-8')

for i in f:
    ads = f"'{i}',"
    ad = f"'{i}',".split()
    add = ad[0]+ad[1]
    print(add)
    f = open('demo_one.txt', 'a', encoding='utf-8')
    f.writelines(str(add) + '\n')
    f.close()
