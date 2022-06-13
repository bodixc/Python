print('******Множення. Множник в правій частині регістру******')

multiplicand_1 = ''
multiplicand_2 = ''
nums = []
for i in range(2):
    num = input(f'{i + 1}-й множник: ')
    nums.append(num)
    num = bin(int(num))
    if int(num, base=2) < (-2 ** 31) or int(num, base=2) > (2 ** 31 - 1):
        raise ValueError(f'Переповнення регістру!\nМножник більше допустимих значень [{-2 ** 31}; {2 ** 31 - 1}]')
    if num[0] == '-':
        num = '0' * (35 - len(num)) + num[3:]
        additional_code = '1'
        for b in num[1:]:
            if b == '0':
                additional_code += '1'
            else:
                additional_code += '0'
        additional_code = bin(int(additional_code, base=2) + 1)[2:]
        if i == 0:
            multiplicand_1 = additional_code
        else:
            multiplicand_2 = additional_code
        print(f' - Перетворюємо у доповняльний код: {additional_code}')
    else:
        num = '0' * (34 - len(num)) + num[2:]
        print(f' - Перетворюємо в прямий код: {num}')
        if i == 0:
            multiplicand_1 = num
        else:
            multiplicand_2 = num

print('\nПідготовка регістрів')
Multiplicand = multiplicand_1
Adder = Multiplicand + '0' * 32
print(' - Записуємо значення 1-го множника в регістр Multiplicand = ' + Multiplicand)
Result = '0' * 32 + multiplicand_2
print(' - Записуємо значення 2-го множника в праву частину регістру Result = ' + Result)

for i in range(32):
    print(f'\nІтерація {i + 1}:')
    print(' - Result = ' + Result)
    if Result[-1] == '1':
        print(' - Молодший біт регістру Result = 1:')
        print('    + Додаємо вміст регістру Multiplicand до лівої частини регістру Result')
        res = bin(int(Adder, base=2) + int(Result, base=2))[2:]
        Result = '0' * (64 - len(res)) + res
    else:
        print(' - Молодший біт регістру Result = 0:')
        print('    - Пропускаємо додавання')
    print(' - Result = ' + Result)
    print(' - Зсуваємо регістр Result вправо на 1 біт')
    Result = '0' + Result[:-1]
Result = Result[-32:]

if multiplicand_1[0] != multiplicand_2[0]:
    direct_code = ''
    for b in Result:
        if b == '0':
            direct_code += '1'
        else:
            direct_code += '0'
    direct_code = bin(int(direct_code, base=2) + 1)
    Result = - int(direct_code, base=2)
    print(f'\nМножники мають різні знаки: \n - Перетворюємо результат у прямий код: {direct_code[2:]}')
else:
    print(f'\nМножники мають однакові знаки \n - Результат уже у прямому коді')
    Result = int(Result, base=2)
Error = ''
if Result != int(nums[0]) * int(nums[1]):
    Error = '\nРегістр результату переповнений! Результат помилковий'
print(Error)
print(f'Результат множення: {nums[0]} * {nums[1]} = {Result}')