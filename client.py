#!/usr/bin/python
#coding=UTF-8

import socket

# Renato Araújo
# 06/06/2017
# 09/07/2023 Update to Python 3.
# Changes print"" to print(""); raw_input() to input() and encode() 'send messages' and decode() 'receive messages'.
# https://stackoverflow.com/a/49362435
#
# PROTOCOLO HUMANO - Cliente TCP após estabelecer comunicação com servidor (usando o Protocolo "Boa Tarde")
# requisita o horário local do servidor.
#

# IP e Porta do servidor.
HOST = "127.0.0.1"
PORT = 33000

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)

#print("Para sair use CTRL-X\n)"
print("\t|#|---------------------------------------------|#|")
print("\t|#| PROTOCOLO SAUDAÇÃO ---- Cliente em execução |#|")
print("\t|#|---------------------------------------------|#|\n")

print("Digite: Boa Tarde")
msg = input()
msg_byte = msg.encode() # encode string to byte.

print("\nout --> " + msg)    # 1º Boa Tarde
tcp.send(msg_byte)

saudacao = False

while msg != '\x18':
    if not msg: break

    msg_recebida_byte = tcp.recv(1024)
    msg_recebida = msg_recebida_byte.decode() # decode byte to string.
    print("in <-- " + msg_recebida)

    if msg_recebida == "Boa Tarde":
        msg = "Horas?"
        print("out --> " + msg)
        tcp.send(msg.encode())
        saudacao = True

    elif saudacao and msg_recebida != "Boa Tarde":
        print("out --> Obrigado")
        msg = "Obrigado"
        tcp.send(msg.encode())
        msg = '\x18'    # Sair

    elif msg_recebida == "NACK": # Resposta NACK, não houve cumprimento da saudação.
        print("WARNING: Resposta NACK, Protocolo Saudação não entende " + "[" + msg + "]")
        #print("Tente novamente: ")
        msg = input("Tente novamente: ")
        tcp.send(msg.encode())

    #else:
    #   print("exit")
    #   msg = '\x18'	# sair

print("Comunicação concluida!")
tcp.close()
