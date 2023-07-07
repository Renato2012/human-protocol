#!/usr/bin/python
#coding=UTF-8

import threading
import socket
from time import strftime   #get hour minute second

# Renato Araújo
# 06/06/2017
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
        print ("\n\nConectado por " + str(self.client) + "\n")
        while True:
            msg = self.con.recv(1024)
            if not msg: break
            
            print ("in <-- ", self.client, msg)

            if msg == "Boa Tarde":
                print ("out --> Saudacao: " + str(msg))
                self.con.send(msg)
                self.saudacao = bool

            elif self.saudacao == bool and msg == "Horas":
                hour = strftime("%H:%M:%S")
                print ("out --> Hora: " + str(hour))
                self.con.send(hour)

            elif msg == "Obrigado":
                #print "out --> " + msg
                print ("Comunicacao concluida!")
                break	# sai do laço, finaliza comunicação com cliente

            else:
                print ("Error: Par nao estabeleceu fase SAUDACAO")
                #break	# sai do laço
                #
                print ("WARNING: Aguardando estabelecimento da saudacao")
                self.con.send("NACK")

        print ("Finalizando conexao do cliente " + str(self.client) + "\n")
        self.con.close()
        
# coding the socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# IP do servidor ('' pode responder em todas as NIC disponíveis no servidor) e porta (33000).
orig = ('', 33000)
tcp.bind(orig)
tcp.listen(50)


print ("\t|#|----------------------------------------------|#|")
print ("\t|#| PROTOCOLO SAUDACAO ---- Servidor em execucao |#|")
print ("\t|#|----------------------------------------------|#|\n")


while True:
    con, client = tcp.accept()
    thread = TCPServer(con, client)
    thread.start()
