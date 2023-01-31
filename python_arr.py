my_arr = []
my_arr.insert(0,('1','0'))
my_arr.insert(0,('2','1'))
my_arr.pop()
my_arr.insert(0,('3','1'))
my_arr.insert(0,('4','0'))
print(len(my_arr))
cnt = 0

def miised_blocks(a_arr):
    cnt = 0
    for x,y in a_arr:
        if y == '1':
            cnt = cnt +1
    return cnt


if __name__ == "__main__": 
    print(miised_blocks(my_arr));

