# TRABALHO SEGUNDA UNIDADE
# Alunos: Maxmyller Carvalho / Isaias Lucena


# A classe ChatClient representa o lado do cliente de uma conexão TCP em um chat.
# Contém uma thread principal que é responsável por receber os dados do servidor enquanto os dados escritos pelo usuário para
# esse mesmo servidor usa uma segundo thread, que foi chamado aqui de 'user_thread'.

from socket import *
import threading
 
HOST = '127.0.0.1'
PORT = 5000

class ClientChat:
	sock=socket(AF_INET, SOCK_STREAM)
	
	def mensagem_enviada(self):
		while True:
			self.sock.send(bytes(input(""), 'utf-8'))
	
	def __init__(self):
		# Pede ao usuário para informar um nickname
		nickname = input("Digite seu nickname: ")
		
		# Escreve o nome do usuário e o envia para o servidor
		if nickname:
			mensagem = "nome(%s)"%nickname
			self.sock.connect((HOST, PORT))
			self.sock.send(bytes(mensagem, 'utf-8'))

			# Thread criado abaixo para escrever pro servidor 
			user_thread = threading.Thread(target = self.mensagem_enviada)
			user_thread.daemon = True
			user_thread.start()			
			
			while True:
				# Recebendo a mensagem
				dados = self.sock.recv(1024)

				if not dados: break

				# Imprimindo as mensagens nos clientes conectados
				print(str(dados, 'utf-8'))
				
client = ClientChat()
