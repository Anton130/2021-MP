import socket # библиотека для обмена сокетами
import threading
import queue
import sys # библиотека для работы с системными функциями
import random # библиотека для работы с рандомом
import os # библиотека для работы с операционной системой


#Client Code - Код клиента:
def ReceiveData(sock):
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            print(data.decode('utf-8'))
        except:
            pass

def RunClient(serverIP): # функция запуска клиента(от IP сервера)
    host = socket.gethostbyname(socket.gethostname())
    port = random.randint(6000,10000) # берём рандомный порт
    print('Client IP->'+str(host)+' Port->'+str(port)) # пишем хост и порт на клиент
    server = (str(serverIP),5000) # IP сервера и порт=5000
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # создаём объект для обмена сокетами
    s.bind((host,port)) #
    
    name = input('Please write your name here: ') # вводим своё имя для идентификации
    if name == '': # если имя - пустая строка, то:
        name = 'Guest'+str(random.randint(1000,9999)) # имя - гость №... рандом
        print('Your name is:'+name) # Печатаем: Ваше имя ...
    s.sendto(name.encode('utf-8'),server) # Отправляем имя на сервер
    threading.Thread(target=ReceiveData,args=(s,)).start()
    while True: # бесконечный цикл
        data = input() # информация - входная с клавиатуры
        if data == 'qqq': # Если информация = qqq, то завершаем цикл
            break
        elif data=='': # Если информация = пустой строке, то продолжаем цикл
            continue
        data = '['+name+']' + '->'+ data # информация = [имя] -> информация
        s.sendto(data.encode('utf-8'),server) # отправляем информацию на сервер
    s.sendto(data.encode('utf-8'),server)# отправляем информацию на сервер при выходе(qqq)
    s.close()# закрываем объект обмена
    os._exit(0) # выходим из клиента
#Client Code Ends Here - Код клиента заканчивается здесь


#Server Code
def RecvData(sock,recvPackets):
    while True:
        data,addr = sock.recvfrom(1024)
        recvPackets.put((data,addr))

def RunServer():
    host = socket.gethostbyname(socket.gethostname()) #берём ip адрес с системы
    port = 5000
    print('Server hosting on IP-> '+str(host))
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.bind((host,port))
    clients = set()
    recvPackets = queue.Queue()

    print('Server Running...')

    threading.Thread(target=RecvData,args=(s,recvPackets)).start()

    run_server = True
    while run_server:
        while not recvPackets.empty():
            data,addr = recvPackets.get()
            if addr not in clients:
                clients.add(addr)
                continue
            #clients.add(addr)
            data = data.decode('utf-8')
            if data.endswith('qqq'):
                clients.remove(addr)
                continue
            if data.endswith('quit'):
                run_server = False
                break
            print(str(addr)+data)
            for c in clients:
                if c!=addr:
                    s.sendto(data.encode('utf-8'),c)

    s.close()
#Serevr Code Ends Here

if __name__ == '__main__':
    if len(sys.argv)==1:
        RunServer()
    elif len(sys.argv)==2:
        RunClient(sys.argv[1])
    else:
        print('Run Serevr:-> python Chat.py')
        print('Run Client:-> python Chat.py <ServerIP>')