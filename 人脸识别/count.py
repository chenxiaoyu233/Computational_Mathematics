#coding=utf-8
ans = 0
total = 55
for i in range(55):
    line = input()
    line = line.split(' ')
    if line[0] == line[1]:
        ans += 1

print ('{}/{} = {}'.format(ans, total, ans/total))
