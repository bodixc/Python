import bitstring
print("*.*.*.*.*.*Множення чисел з плаваючою точкою*.*.*.*.*.*")
X1 = float(input("Введіть 1-ше число: "))
X2 = float(input("Введіть 2-ге число: "))
round_indexs = []
for x in [X1, X2]:
    if '.' in str(x):
        round_index = len(str(x)[str(x).index('.')+1:])
    else:
        round_index = str(x)[str(x).index('e')+2:]
        if round_index[0] == '0':
            round_index = round_index[1:]
        round_index = int(round_index)
    round_indexs.append(round_index)
round_index = round_indexs[0] + round_indexs[1]
res = ''
print('\nПеревірка чисел:')
if 0 in [X1, X2]:
    print(' - Один з множників дорівнює нулю')
    print(' - Встановлюємо результат у нуль')
    res = 0
elif X1 > 2**127 or X2 > 2**127:
    print(f' - Один з множників більше допустимого значення: {2**127}')
    print(' - Встановлюємо результат у inf')
    res = 'inf'
else:
    print(' - Пройдена перевірка')
    print('\nПідготовка чисел:')
    bin_X1 = bitstring.BitArray(float=X1, length=32).bin
    print(' - Переводимо 1-ше число в стандарт IEEE-754 (32-bit): ' + bin_X1)
    bin_X2 = bitstring.BitArray(float=X2, length=32).bin
    print(' - Переводимо 2-ге число в стандарт IEEE-754 (32-bit): ' + bin_X2)
    print('\nВстановлення знаку результату:')
    sign_X1 = int(bin_X1[0])
    print(f' - Знак 1-го числа = {sign_X1}' )
    sign_X2 = int(bin_X2[0])
    print(f' - Знак 2-го числа = {sign_X2}' )

    sign = sign_X1 ^ sign_X2

    print(f' - Знак результату: {sign_X1} xor {sign_X2} = {sign}' )

    print('\nОбрахування мантиси результату:')
    mantissa_X1 = int('1' + bin_X1[9:], 2)
    print(f' - Мантиса 1-го числа: 1.{bin_X1[9:]}')
    mantissa_X2 = int('1' + bin_X2[9:], 2)
    print(f' - Мантиса 2-го числа: 1.{bin_X2[9:]}')
    mantissa = bin(mantissa_X1 * mantissa_X2)[2:]
    print(f' - Перемножуємо мантиси між собою: {mantissa[:-46]}.{mantissa[-46:]}')
    print(f' - Нормалізуємо мантису результату: {mantissa[0]}.{mantissa[1:]}')
    mantissa_exponent = len(mantissa) - 47
    print(f' - Експонента мантиси результату: {mantissa_exponent}')
    mantissa = mantissa[1:24]
    print(' - Беремо за значення мантиси результату 23 старші біти: ' + mantissa)

    print('\nОбрахування значення експоненти:')
    exponent_X1 = int(bin_X1[1:9], 2)
    print(f' - Експонента 1-го числа: {bin_X1[1:9]}')
    exponent_X2 = int(bin_X2[1:9], 2)
    print(f' - Експонента 2-го числа: {bin_X2[1:9]}')
    exponent = exponent_X1 + exponent_X2 - 127 + mantissa_exponent
    bin_exponent = '0' * (8 - len(bin(exponent)[bin(exponent).index('b')+1:])) + bin(exponent)[bin(exponent).index('b')+1:]
    print(' - Обраховуємо значення експоненти результату: ' + bin_exponent)
    if exponent < 0:
        print(' - Екпонента переповнена за мінімальне допустиме значення')
        print(' - Встановлюємо результат у нуль')
        res = 0
    else:
        bin_number = str(sign) + bin_exponent + mantissa
        print('\nРезультат числа у форматі IEEE-754 (32-bit): ' + bin_number)
        number = bitstring.BitArray('0b' + bin_number).float
        res = round(number, round_index)
        print('Переводимо число у формат з плаваючою точкою: ' + str(res))
print(f'\nРезультат множення: {X1} * {X2} = {res}')