def calculate_total():
    return salary + (salary / 100 * bonus)


def calculate_total2(_salary, _bonus):
    return _salary + (_salary / 100 * _bonus)


name = 'Antoliy'
salary = 2000
bonus = 20
currency = '$'
total = calculate_total()

# print(name, salary, bonus)

template = 'Name: {0}\nSalary: {1}{3}\nBonus: {2}%\nTotal: {4}\n'
out = template.format(name, salary, bonus, currency, total)
# print(out)

template2 = 'Name: {name}\nSalary: {salary:.02f}{currency}\nBonus: {bonus}%\nTotal: {total:.02f}\n'
out2 = template2.format(
    name=name, salary=salary, bonus=bonus,
    currency=currency, total=total,
)
# print(out2)

# print(f'Name: {name}\nSalary: {salary:.02f}{currency}\nBonus: {bonus}%\nTotal: {total:.02f}\n')

print(total)
print(calculate_total(), '\n')
bonus += 10 #  30

print(total)
print(calculate_total(), '\n')
bonus -= 15 # 15

print(total)
print(calculate_total(), '\n')


total = calculate_total()
# print(f'Name: {name}\nSalary: {salary:.02f}{currency}\nBonus: {bonus}%\nTotal: {total:.02f}\n')


total = calculate_total2(salary, bonus)
print(f'Name: {name}\nSalary: {salary:.02f}{currency}\nBonus: {bonus}%\nTotal: {total:.02f}\n')
