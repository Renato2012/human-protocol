#!/usr/bin/python
# coding=UTF-8

import socket

# Renato Araújo
# 06/06/2017
#
# PROTOCOLO HUMANO - Cliente TCP após estabelecer comunicação com servidor (usando o Protocolo "Boa Tarde")
# requisita o horário local do servidor. 
#

# IP e Porta do servidor.
HOST="127.0.0.1"
PORT=33000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

#print "Para sair use CTRL-X\n"
print "\t|#|---------------------------------------------|#|"
print "\t|#| PROTOCOLO SAUDAÇÃO ---- Cliente em execução |#|"
print "\t|#|---------------------------------------------|#|\n"

print "Digite: Boa Tarde"
msg = raw_input()
first_msg = msg

print "\nout --> " + msg    # 1º Boa Tarde
tcp.send(msg)

saudacao = False

while msg != '\x18':
    if not msg: break

    msg_recebida = tcp.recv(1024)
    print "in <-- " + msg_recebida

    if msg_recebida == "Boa Tarde":
        msg = "Horas"
        print "out --> " + msg
        tcp.send(msg)
        saudacao = bool

    elif saudacao == bool and msg_recebida != "Boa Tarde" :
        print "out --> Obrigado"
        tcp.send("Obrigado")
        msg = '\x18'    # Sair

    elif msg_recebida == "NACK" :	# Resposta NACK, não houve cumprimento da saudação. 
        print "WARNING: Resposta NACK, Protocolo Saudação não entende " + "[" + first_msg + "]"
        print "Tente novamente: "
        msg = raw_input()
        tcp.send(msg) 

    #else:
    #   print "exit"
    #   msg = '\x18'	# sair

print "Comunicação concluida!"
tcp.close()

