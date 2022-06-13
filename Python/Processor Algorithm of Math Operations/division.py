import bitstring

nums = []
print('///////////////////////////Ділення як є///////////////////////////')
num1 = int(input('Ділене: '))
if num1 < (-2 ** 63) or num1 > (2 ** 63 - 1):
    raise ValueError(f'Переповнення регістру!\nДілене більше допустимих значень [{-2 ** 63}; {2 ** 63 - 1}]')
nums.append(num1)
if num1 < 0: num1 = ~num1 + 1
Divident = bitstring.BitArray(int=num1, length=64).bin
print(' - Перетворюємо в прямий код: ' + Divident)
num2 = int(input('Дільник: '))
if num2 == 0:
    raise ZeroDivisionError('На нуль ділити не можна!')
if num2 < (-2 ** 63) or num2 > (2 ** 63 - 1):
    raise ValueError(f'Переповнення регістру!\nДілене більше допустимих значень [{-2 ** 63}; {2 ** 63 - 1}]')
nums.append(num2)
if num2 < 0: num2 = ~num2 + 1
Divisor = bitstring.BitArray(int=num2, length=64).bin
print(' - Перетворюємо в прямий код: ' + Divisor)
print('\nПідготовка регістрів')
Remainder = Divident
print(' - Записуємо значення діленого в регістр Remainder = ' + Remainder)
print(' - Записуємо значення дільника в регістр Divisor = ' + Divisor)
shift = len(bin(num1)) - len(bin(num2))
if shift < 0: shift = -1
Divisor += '0' * shift
print(
    ' - Зсуваємо значення дільника в регістрі Divisor в  вліво, щоб старший значущий біт був на рівні з діленим ' + Divisor)
Quotient = '0' * 32
for i in range(shift + 1):
    print(f'\nІтерація {i + 1}:')
    Remainder = bitstring.BitArray(int=int(Remainder, base=2), length=64).bin
    print(' - Remainder = ' + Remainder)
    Divisor = bitstring.BitArray(int=int(Divisor, base=2), length=64).bin
    print(' - Divisor = ' + Divisor)
    if int(Remainder, base=2) >= int(Divisor, base=2):
        print(' - Значення регістру Remainder більше за значення регістру Divisor:')
        Quotient += '1'
        print('    + Встановлюємо молодший біт = 1 регістру Quotient: ' + Quotient[-32:])
        Remainder = bitstring.BitArray(int=(int(Remainder, base=2) - int(Divisor, base=2)), length=64).bin
        print('    + Віднімаємо значення регістру Divisor від регістру Remainder')
    else:
        print(' - Значення регістру Remainder менше за значення регістру Divisor:')
        Quotient += '0'
        print('    - Встановлюємо молодший біт = 0 регістру Quotient:' + Quotient[-32:])
        print('    - Пропускаємо віднімання')
    print(' - Зсуваємо регістр  Quotient вправо на 1 біт')
    Divisor = bitstring.BitArray(int=(int(Divisor, base=2) >> 1), length=64).bin
    print(' - Зсуваємо регістр Divisor вправо на 1 біт')

Remainder = int(Remainder, base=2)
Quotient = bin(int(Quotient, base=2))[2:]
if len(Quotient) > 32:
    print('\nСталось переповнення регістру частки Qutient. Результат є помилковим математично!')
elif Quotient == '':
    Quotient = '0'
Quotient = int(Quotient[-32:], base=2)
if nums[0] < 0 or nums[1] < 0:
    Remainder = - Remainder
if (nums[0] > 0 and nums[1] < 0) or (nums[0] < 0 and nums[1] > 0):
    Quotient = - Quotient

print(f'Результат ділення: {nums[0]} / {nums[1]} = {Quotient}. Залишок: {Remainder}')