print ("Hello, World")

age = 20
age = int(input("Enter age here: "))
if age >= 20 and age <= 65:
    
    print("You are between the age 18 and 65. You are elligible to vote, vote wisely")

#main assignment
age = int(input("Enter yout age: "))
#Voting
if age >=18:
    print ("You can vote, you are 18 or older.")

else:
    print("You cannot vote yet, wait till you are of age, Why are you rushing!")

#Drinking
age = int(input("Enter your age: "))
if age <= 18:
    print("You are too young to drink, go and sleep")

else:
    print("No drink o, you fit damage your liver, na better update o")

#Senior Discount
if age >= 65:
    age = int(input("Enter your age: "))
    print("You are qualified for Senior discount, relax and enjoy it, it's your right")

elif age <=64:
    print("Please, go and work, e never reach your turn.")

else :
    print("You should be studying o, eh!")


