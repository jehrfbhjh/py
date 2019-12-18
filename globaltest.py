global num
num = 1
def fun():
     global num
     num = 123
     print(num)
def fun1():
    global num
    num = num +1
    print(num)
fun()
print(num)
fun1()