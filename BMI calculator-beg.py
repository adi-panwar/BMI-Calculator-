print("==--Panfar Simple MBI Calculator--==")

weight = float(input("Enter your weight in kg: "))
height = float(input("Enter your height in cm: "))

height =  height/100 
bmi= weight/height**2
print("your bmi (body mass index) is: " , round(bmi, 2))

if bmi < 18.5:
    print("oops , You are underweight. -- you need to eat more neutrients food ")
elif 18.5<= bmi < 25:
    print("yeeeeeeee , you are Normal.  -- good keep it up ")
elif 25<= bmi <30 :
    print("cheeee , you are overweight. -- do exersize ")
else :
    print("OMG , you are obese.  -- go to doctor and concern upon it.")
     
           