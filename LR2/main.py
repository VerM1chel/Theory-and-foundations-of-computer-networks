from math import log


def hemming_encoding(data, base2list):
    for i in range(len(data)):
        checkSum = 0
        if i in base2list:  # если данный индекс -- одна из степеней двойки (контрольный бит)
            for j in range(i, len(data), 2 * (i + 1)):
                checkSum += sum([1 for elem in data[j:j + (i + 1)] if elem == 1])  # подсчитываем 1 в интервале N от текущего бита и добавляем сумму к контрольному биту
            if checkSum % 2 == 0:
                data[i] = 0
            else:
                data[i] = 1
    return data

def base2(data):
    base2list = []
    for i in range(len(data)):
        if log(i + 1, 2) % 1 == 0:
            base2list.append(i)
    return base2list

def ruin_message(data, idx):
    for i in range(len(data)):
        if i == idx:
            if data[i] == 0:
                data[i] = 1
            else:
                data[i] = 0


def func_chunks_generators(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]




def main():
    # ПОЛУЧЕНИЕ ДАННЫХ
    data = input()
    data = ' '.join(format(ord(x), 'b') for x in data)
    data = data.split(' ')
    for i in range(len(data)):      # каждому символу должно соответствовать 8 бит, дописываем 0 в начале, если не так
        while len(data[i]) < 8:
            data[i] = '0'+data[i]
    data = ''.join(data)
    print(data)

    data = list(map(int, data))
    k = 0
    i = 0
    while i < len(data):
        if i == 2**k-1:
            data.insert(i, 0)
            k += 1
        i += 1

    base2list = base2(data)
    data = hemming_encoding(data, base2list)
    print(f'encoded data{data}')

    # ДАННЫЕ ЗАКОДИРОВАНЫ
    # ГЕНЕРИРУЕМ ОШИБКУ
    data_recieved = data.copy()
    ruin_message(data_recieved, 5)
    print(f'ruined data {data_recieved}')

    # ЗАНОВО ВЫЧИСЛЯЕМ КОНТРОЛЬНЫЕ БИТЫ, ЧТОБЫ ПОНЯТЬ ГДЕ ОШИБКА
    for i in base2list:
        data_recieved[i] = 0
    data_recieved = hemming_encoding(data_recieved, base2list)

    err_idx = 0
    for i in base2list:      # если данный индекс -- одна из степеней двойки (контрольный бит)
        if data_recieved[i] != data[i]:     # если контрольные биты не совпадают
            err_idx += i+1

    if data_recieved[err_idx-1] == 0:
        data_recieved[err_idx-1] = 1
    else:
        data_recieved[err_idx-1] = 0
    data_recieved = hemming_encoding(data_recieved, base2list)

    print(f'fixed data  {data_recieved}')
    i = len(data_recieved)
    while i >= 0:
        if i in base2list:  # если данный индекс -- одна из степеней двойки (контрольный бит)
            data_recieved.pop(i)
        i -= 1

    data_recieved = list(func_chunks_generators(data_recieved, 8))
    i = 0
    while i < len(data_recieved):
        data_recieved[i] = ''.join(map(str, data_recieved[i]))
        data_recieved[i] = chr(int(data_recieved[i], 2))
        i += 1

    print(data_recieved)
    data_recieved = ''.join(data_recieved)
    print(data_recieved)

if __name__ == '__main__':
    main()
