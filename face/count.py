ans = 0
total = 400
for i in range(40):
    for j in range(10):
        line = input()
        line = line.split(' ')
        if line[0] == line[1]:
            ans += 1

print ('{}/{} = {}'.format(ans, total, ans/total))
