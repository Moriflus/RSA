import random

"""
Алгоритм Евклида для нахождения НОД(a, b)
"""
def EvklidNOD(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b

"""
Расширенный алгоритм Евклида
"""
def gcdExtended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcdExtended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

"""
Нахождение обратного элемента по модулю
"""
def InvElement(m, a):
    gcd, x, y = gcdExtended(a, m)
    return (x % m + m) % m

"""
Проверка является ли число простым или составным
"""
def isPrime(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n

"""
Генерация больших простых чисел "p" и "q"
"""
def PQgen():
    while True:
        p = random.randint(1, 10000000)
        if isPrime(p) == 1:
            break
    while True:
        q = random.randint(1, 10000000)
        if isPrime(q) == 1:
            break
    return p, q

"""
Нахождение числа "e" (экспонента зашифрования)
"""
def eChoose(FunEyler, N):
    e = 2
    while e < FunEyler:
        if EvklidNOD(e, FunEyler) == 1 and EvklidNOD(e, N) == 1:
            return e
        e += 1

"""
Генерация публичного и приватного ключей
"""
def keyGenerator(p, q):
    N = p * q
    FunEyler = (p - 1) * (q - 1)
    lock = [eChoose(FunEyler, N), N]

    unlock = [InvElement(FunEyler, lock[0]), N]
    return lock, unlock

"""
Шифрование сообщения
"""
def encryption(data, lock):
    out = ''
    for char in data:
        out += chr(((ord(char) ** lock[0]) % lock[1]) % 1114111)
    return out

"""
Дешифрование сообщения
"""
def decryption(data, unlock):
    out = ''
    for char in data:
        out += chr(((ord(char) ** unlock[0]) % unlock[1]) % 1114111)
    return out

"""
Консольная программа
"""
print('Шифрование и дешифрование методом "RSA"')
PQ = input('1 - Сгенерировать "p" и "q"\n2 - Ввести вручную\nВаш выбор: ')
if PQ == '1':
    PQ = PQgen()
    p = PQ[0]
    q = PQ[1]
    keys = keyGenerator(p, q)
    lock = keys[0]
    unlock = keys[1]
    print('Ваш публичный ключ: ' + str(lock[0]) + ' ' + str(lock[1]))
    print('Ваш приватный ключ: ' + str(unlock[0]) + ' ' + str(unlock[1]))

else:
    p = int(input('p: '))
    while isPrime(p) != 1:
        p = int(input('Повторите ввод "p": '))
    q = int(input('q: '))
    while isPrime(q) != 1:
        q = int(input('Повторите ввод "q": '))
    keys = keyGenerator(p, q)
    lock = keys[0]
    unlock = keys[1]
    print('Ваш публичный ключ: ' + str(lock[0]) + ' ' + str(lock[1]))
    print('Ваш приватный ключ: ' + str(unlock[0]) + ' ' + str(unlock[1]))


action = input('Выберите следующее действие:\n1 - Шифрование текста по публичному ключу\n2 - Дешифрование текста по приватному ключу\n3 - Сохранить ключи\nВаш выбор: ')
if action == '1':
    selfornot = input('1 - Указать файл с текстом для шифрования \n2 - Ввести вручную\n')
    if selfornot == '1':
        inp = input('Введите название файла: ')
        file = open(inp, 'r', encoding='utf-8')
        mydata = file.readline()
        file.close()
        result = encryption(mydata, lock)
        file = open('result', 'w', encoding='utf-8')
        file.write(result)
        file.close()
        print(result + '\nРезультат также записан в файл "result"!')
    elif selfornot == '2':
        inp = input('Введите текст: ')
        result = encryption(inp, lock)
        file = open('result', 'w', encoding='utf-8')
        file.write(result)
        file.close()
        print(result + '\nРезультат также записан в файл "result"!')
    else:
        print('Выбрана несуществующая опция!')
elif action == '2':
    selfornot = input('1 - Указать файл с текстом для дешифрования \n2 - Ввести вручную\n')
    if selfornot == '1':
        inp = input('Введите название файла: ')
        file = open(inp, 'r', encoding='utf-8')
        secretdata = file.readline()
        file.close()
        unlock = list(map(int, input('Приватный ключ: ').split()))
        result = decryption(secretdata, unlock)
        file = open('result', 'w', encoding='utf-8')
        file.write(result)
        file.close()
        print(result + '\nРезультат также записан в файл "result"!')
    elif selfornot == '2':
        inp = input('Введите текст: ')
        unlock = list(map(int, input('Приватный ключ: ').split()))
        result = decryption(inp, unlock)
        file = open('result', 'w', encoding='utf-8')
        file.write(result)
        file.close()
        print(result + '\nРезультат также записан в файл "result"!')
    else:
        print('Выбрана несуществующая опция!')
else:
    file = open('result', 'w', encoding='utf-8')
    file.write('Ваш публичный ключ: ' + str(lock[0]) + ' ' + str(lock[1]))
    file.write('\n')
    file.write('Ваш приватный ключ: ' + str(unlock[0]) + ' ' + str(unlock[1]))
    file.close()
    print('Ключи успешно записаны в файл "result"!')
