def fn(mylist):
    n = len(mylist)
    for i in range(n-1):
        count = 0
        for j in range(0,n-1-i):
            if mylist[j]>mylist[j+1]:
                mylist[j],mylist[j+1]=mylist[j+1],mylist[j]
                print(mylist)
                count+=1
        if count == 0:
            return mylist

if __name__=="__main__":
    L = [110,5,3,8,44,11,2,50]
    print(L)
    fn(L)
    print(L)

            

