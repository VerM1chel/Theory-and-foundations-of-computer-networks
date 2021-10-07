import serial
import threading, sys


class Worker(threading.Thread):

    def __init__(self, num_thread):
        # вызываем конструктор базового класса
        super().__init__()
        # определяем аргументы собственного класса
        self.num_thread = num_thread

    def run(self):
        while(1):
            sp.send(str.encode(input()))





class SerPort(serial.SerialBase):
    def __init__(self, name, baudrate):
        self.name = name
        try:
            self.serialPort = serial.Serial(self.name)
            self.serialPort.baudrate = baudrate

            self.esc = hex(29)  # 1Dh
            self.flag = hex(10)  # 0Ah
            self.fcs = hex(11)  # 0Bh

            print(f'Port {self.name} was successfully connected')
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            if (self.serialPort):
                checkSum = sum(data).to_bytes(2, byteorder='big')  # ввод был в байтах, подсчитываем сумму и конвертируем в 2 байта
                k =  sum(data)
                for i, byte in enumerate(data):
                    if (byte == self.flag or byte == self.fcs): # Если встретили бит, совпадающий значением с флагом начала или конца
                        for j in range(i + 1, len(data)):
                            data[j + 1] = data[j]  # Сдвиг на 1 вправо
                        data[i + 1] += hex(2)  # То изменяем этот байт
                        data[i] = self.esc  # Вставка esc-последовательности
                message = self.flag.encode() + data + self.fcs.encode() + checkSum
                self.serialPort.write(message)
        except IOError as ioe:
            print(f"Port {self.name} can't send data")

    def receive(self):
        data = ''
        try:
            message = self.serialPort.read(self.serialPort.inWaiting())

            flag = message[0:3].decode()  # Получаем флаг (0xa)
            end_idx = message.find(b'0xb')
            if (end_idx != -1):
                fcs = message[end_idx: end_idx + 3].decode()  # Получаем конец пакета (0xb)
            else:
                fcs = -1
            if (flag == self.flag and fcs == self.fcs):  # Если мы получили пакет полностью
                maybeData = message[3:end_idx]  # Получаем то, что должно соответствовать нашим данным
                for i, byte in enumerate(maybeData):
                    if (byte == self.esc):
                        maybeData[i + 1] -= hex(2)  # Когда отравляли, то увеличивали на 2, теперь уменьшаем
                        for j in range(i + 1, len(maybeData)):
                            maybeData[j] = maybeData[j - 1]  # Сдвиг на 1 влево
                checkSum = int.from_bytes(message[end_idx + 3:], "big")  # конвертируем контрольную сумму из байтов обратно в число (в байтовом представлении будет примерно \x01\xb3
                if (sum(maybeData) == checkSum):
                    data = maybeData
                else:
                    print('Transmission error')
                    return ''
            else:
                print('Transmission error')
                return ''
        except IOError as ioe:
            print(f"Port {self.name} can't read data")
        return data


    def inWaiting(self):
        k = 0
        if self.serialPort.inWaiting():
            k = 1
        return self.serialPort.inWaiting()

    def setBaud(self, baudrate):
        self.serialPort.baudrate = baudrate

    def getBaud(self):
        return self.serialPort.baudrate

    def showBaud(self):
        print(f'Now baud is {sp.getBaud()}')



sp = SerPort('COM1', 9600)
print(f'Now baud is {sp.getBaud()}')

th = Worker(1)
th.start()


while(1):
    if sp.inWaiting():
        rec_data = sp.receive()
        if ('set baud' in str(rec_data)):
            speed = rec_data.split()[2]
            if (speed.isdigit()):
                if int(speed)>0:
                    sp.setBaud(speed)
                print(f'Now baud is {sp.getBaud()}')
            else:
                print(rec_data)
        elif (rec_data=='show baud'):
            sp.showBaud()
        elif (rec_data=='disconnect'):
            sp.send('disconnect'.encode('utf-8'))
            sys.exit()
        else:
            print(rec_data)
