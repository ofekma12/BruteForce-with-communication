from socket import *
import time
import BruteForce
import threading
import pygame 

def play_sound():
    file_path = "matdor.wav"
    pygame.init()
    sound = pygame.mixer.Sound(file_path)
    sound.play()
    pygame.time.wait(int(sound.get_length() * 1000))
    pygame.quit()

def blocking(soc, end):
    '''
    while not end:
        answer1 = soc.recv(1024).decode('utf-8')
        if answer1 == 'end':
            end = True
    '''    

def com(soc, end):
    while not end:
        answer  = soc.recv(1024).decode()
        print(answer)
        if answer[:6]=='start:':
            time.sleep(0.1)
            soc.send('ok'.encode())
            time.sleep(1)
            print("got data from server")
            inputs = answer.split(',')
            start = inputs[0][6:]
            stop = inputs[1][5:]
            MD5 = inputs[2][4:]
            start_list = [chr for chr in start]
            password = BruteForce.BruteForce(start, stop, MD5,6)
            if password!='password was not found':
                answer = 'success:'
                answer += password
                soc.send(answer.encode('utf-8'))
                answer  = soc.recv(1024).decode('utf-8')     
                time.sleep(0.1)
                print("message from server: "+answer)
                print(password)
                if answer!='ok':
                    break
                time2 = soc.recv(1024).decode()
                time2 = time2.split(':')
                uni_time = time2[-1]
                print(uni_time)
                while int(time.time()) < int(uni_time):
                    print(int(time.time()))
                    time.sleep(0.1)
                play_sound()

            else:
                answer = 'failed:next'
                soc.send(answer.encode('utf-8'))
                print("password was sent to server")
                time.sleep(0.1)
            print(password)

            
    soc.close()

def main(soc, end):
    threads = []
    t1 = threading.Thread(target = com, args = (soc,end))
    threads.append(t1)
    for t in threads:
        t.start()
    print("started threads")

if __name__ =='__main__':
    main()