ans = 0
total = 400
for i in range(40):
    for j in range(10):
        line1 = input()
        line2 = input()
        line1 = line1.split(',')
        st = line1[0][9:]
        if st == line2 :
            ans += 1
        print(st, line2)

print ('{}/{} = {}'.format(ans, total, ans/total))
