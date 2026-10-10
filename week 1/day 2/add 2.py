def add(price,quantity):
    return price*quantity

price=float(input("Enter the price:"))
quantity=float(input("Enter the quantity:"))

print("Your total bill is: ", add(float(price), float(quantity)))