with open('fixer_original.py') as f:
    l = f.read().split('\n')[:8]


main = l[-1]

aux = l[:-1]
aux = [x.split(' = ') for x in aux]

for f in aux[::-1]:
    if len(f) != 2:
        raise Exception('wrong')
    name = f[0]
    body = f[1]
    main = main.replace(name, body)

print(main)
