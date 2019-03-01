
#冒泡排序的代码实现原理
def fn(mylist):
    n = len(mylist)
    for i in range(n-1,0,-1):
        for j in range(0,i):
            if mylist[j] > mylist[j+1]:
                mylist[j],mylist[j+1] = mylist[j+1],mylist[j]
    return mylist


L = [55,22,44,11,99,66,33]
n =fn(L)
print(n)
