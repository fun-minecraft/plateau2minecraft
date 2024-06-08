a = [[1, 2], [2, 3], [3, 4]]

for i in a:
    found = False
    for j in range(2):
        if found:
            break
        if i[j] % 2 == 0:
            found = True
        print(i[j])