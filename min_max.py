# for 8 start with max
# list = [2,4,-1,1,5,1,-1,7,-2,-8,0,5,1,6,-3,11]
# n = 16
list = [3,2,6,11,8,10,5,14]
n = 8
# n = int(input("Enter the number of elements in the list: "))
# for i in range(n):
#     list.append(int(input("Enter the element: ")))
turn = 0 if n == 16 else 1
    
while n > 1:
    new_list = []
    if turn == 1:
        for i in range(0, n - 1, 2):
            new_list.append(max(list[i], list[i + 1]))
        list = new_list
    elif turn == 0:
        for i in range(0, n - 1, 2):
            new_list.append(min(list[i], list[i + 1]))
        list = new_list
    n = len(list)
    turn = 1 - turn 
print(list)