def calculate_total(_salary, _bonus):
    return _salary + (_salary / 100 * _bonus)


name = 'Antoliy'
salary = 2000
bonus = 20
currency = '$'


total = calculate_total(salary, bonus)
print(f'Name: {name}\nSalary: {salary:.02f}{currency}\nBonus: {bonus}%\nTotal: {total:.02f}\n')

idx = 3
people = [5000, ['asdasd', 'lklklk', 4234], 'hello', 10.34534, 42, 'aaaa', 235, 'bbbbb', 'cccccc', 324]
# print(people[0], people[1], people[3])
# print(people[0], people[1][2], people[3])
# print(people[idx])
# print(people[-1])
# print(people[-2])
# print(people[-3])
# print(people[0:4])
# print(people[0:5:2])
# print(people[0:-1:2])
print(people)
# people.append(9999)
# people.insert(0, -1)
# people.insert(2, 5)
# people.insert(100, 5)
print(people)
people_extra = [54545, 675675, 'sddd']
# print(people + people_extra)
people[0] = 10
print(len(people))

if len(people) > 10:
    people[8] = 555555
else:
    people.append(1111111111)

print(people)
