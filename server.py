#!/usr/bin/python
# coding=UTF-8

import threading
import socket
from time import strftime  # get hour minute second

# Renato Araújo
# 06/06/2017
# 09/07/2023 Update to Python 3.
# Changes print"" to print(""); raw_input() to input() and encode() 'send messages' and decode() 'receive messages'.
# https://stackoverflow.com/a/49362435
#
# PROTOCOLO HUMANO - Servidor TCP com thread aceita até 50 conexões de clientes simultaneamente.
# Ao receber uma conexão, se esta cumpre a fase de saudação "Boa Tarde",
# então servidor está apto a informar seu horário local.

class TCPServer(threading.Thread):
    def __init__(self, con, client):
        threading.Thread.__init__(self)
        self.con = con
        self.client = client
        self.saudacao = False

    def run(self):
        print("\n\nConectado por " + str(self.client) + "\n")
        while True:
            msg_byte = self.con.recv(1024)
            msg = msg_byte.decode() # decode byte to string
            if not msg: break

            print("in <-- ", self.client, msg)

            if msg == "Boa Tarde":
                print("out --> Saudação: " + str(msg))
                self.con.send(msg_byte)
                self.saudacao = True

            elif self.saudacao and msg == "Horas?":
                hour = strftime("%H:%M:%S")
                print("out --> Hora: " + str(hour))
                self.con.send(hour.encode()) # encode string to byte.

            elif msg == "Obrigado":
                # print("out --> " + msg)
                print("Comunicação concluida!")
                break  # sai do laço, finaliza comunicação com cliente

            else:
                print("Error: Par não estabeleceu fase SAUDAÇÃO")
                # break	# sai do laço
                #
                print("WARNING: Aguardando estabelecimento da saudação")
                nack = "NACK"
                self.con.send(nack.encode()) # encode string to byte.

        print("Finalizando conexão do cliente " + str(self.client) + "\n")
        self.con.close()


# coding the socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IP do servidor ('' pode responder em todas as NIC disponíveis no servidor) e porta (33000).
orig = ('', 33000)
tcp.bind(orig)
tcp.listen(50)

print("\t|#|----------------------------------------------|#|")
print("\t|#| PROTOCOLO SAUDAÇÃO ---- Servidor em execução |#|")
print("\t|#|----------------------------------------------|#|\n")

while True:
    con, client = tcp.accept()
    thread = TCPServer(con, client)
    thread.start()
