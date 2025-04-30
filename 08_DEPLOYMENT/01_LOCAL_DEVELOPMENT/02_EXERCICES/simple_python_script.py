import random as ran
import numpy as np

def create_random_groups(name_list, nb_groups) :

    ran.shuffle(name_list)

    return np.array_split(name_list, nb_groups)
    
names = []

nb_names = int(input("How many people in total ? "))

nb_groups = int(input("How many groups would you like to form ? "))

user_input = True

for i in range(nb_names) :
    names.append(input("Enter a name : "))

for group in create_random_groups(names, nb_groups) :
    print(group)

print("test")