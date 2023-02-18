class Category:

  def __init__(self, name):
    self.name = name
    self.total = 0.00
    self.ledger = []

  def __repr__(self):
    out = f"{self.name:*^30}\n"

    for i in self.ledger:
      out += f"{i['description'][0:23]:23}{i['amount']:>7.2f}\n"

    out += f"Total: {self.total:.2f}"
    return out

  def deposit(self, amount, *description):
    self.total += amount
    description = description[0] if description else ""
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, *description):
    can_withdraw = self.check_funds(amount)

    description = description[0] if description else ""

    if can_withdraw:
      self.total -= amount
      self.ledger.append({"amount": -amount, "description": description})

    return can_withdraw

  def get_balance(self):
    return self.total

  def transfer(self, amount, instance):

    can_transfer = self.check_funds(amount)

    if can_transfer:

      self.withdraw(amount, f"Transfer to {instance.name}")
      instance.deposit(amount, f"Transfer from {self.name}")

    return can_transfer

  def check_funds(self, amount):

    if amount > self.total:
      return False

    return True


food = Category("food")
entertainment = Category("Entertainment")
food.deposit(100, "Something")
food.transfer(25, entertainment)
food.withdraw(20, "beans")
print(food.ledger)
print(food.get_balance())
print(entertainment.ledger)
print(entertainment.get_balance())
print(food)


def create_spend_chart(categories):
  s = "Percentage spent by category\n"

  total = 0.0
  cats = {}
  for cat in categories:
    cat_total = 0.0

    for item in cat.ledger:
      amount = item['amount']
      if amount < 0:
        total += amount
        cat_total += amount

    cats[cat.name] = abs(cat_total)

  total = abs(total)

  for key, value in cats.items():
    percent = (value / total) * 100
    cats[key] = percent
  

  for i in range(100, -1, -10):
    s += f"{str(i) + '|' :>4}"
    for val in cats.values():
      if val >= i:
        s += " o "
      else:
        s += "   "
    s += " \n"

  Length = len(cats.items())
  s += f"    {(Length*3+1) * '-'}\n"
  
  descriptions = list(map(lambda category: category.name, categories))
  max_length = max(map(lambda description: len(description), descriptions))
  descriptions = list(map(lambda description: description.ljust(max_length), descriptions))
  for x in zip(*descriptions):
      s += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"
     
  return s.rstrip("\n")

create_spend_chart([food, entertainment])