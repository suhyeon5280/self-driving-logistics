import turtle

import random as r

co=['red','pink','skyblue','blue','orange','green']

tu=turtle.Turtle()

sn=turtle.Screen()

sn.setup(300,300)

for n in range(40):

    tu=turtle.Turtle()

    tu.shape('turtle')

    tu.penup()

    x,y=r.randint(-200,200),r.randint(-200,200)

    tu.color(co[r.randint(0,5)],co[r.randint(0,5)])   #앞에가 테두리 뒤에가 색

    tu.goto(x,y)

print("개강싫어,,")