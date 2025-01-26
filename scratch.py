li = ['one', 'two', 'three', "bug"]
li_b = ['four', 'five']

# print(li)

# first = li.pop(0)
# li_b.append(first)
# li_c = li + li_b
#
# print(li_b)

# def whatever(li):
#     l = li.pop(0)
#
# print(whatever(li))

# print(li[:2])

for n in range(0):
    print("house")


def funco_pop_one(var_ctr=0):
    print(var_ctr)
    user_input = input("? ")

    if user_input == "moo":
        funco_pop_two(var_ctr)
        # var_ctr += 1

    print(f"Exit f1 {var_ctr}")

def funco_pop_two(var_ctr=0):
    print(var_ctr)
    user_input = input("? ")

    if user_input == "foo":
        var_ctr += 1
        funco_pop_one(var_ctr)

    print(f"Exit f2 {var_ctr}")

funco_pop_one()

# fp 0
#     fp 1
#         fp 2

# exit f2 1
# exit f1 1
# exit f2 1
# exit f1 0