# TRABALHO SEGUNDA UNIDADE
# Alunos: Maxmyller Carvalho / Isaias Lucena

# A classe ChatServer é o servidor do chat. 

from socket import *
import threading 
from user import *
 
HOST = '127.0.0.1'      
PORT = 5000             

class ChatServer:
	# Iniciando socket
	sock=socket(AF_INET, SOCK_STREAM)
	# Guarda os usuários conectados
	usuarios_conectados = []
	
	def __init__(self):
		self.sock.bind((HOST, PORT)) # Vincula na PORTA o HOST definidos acima
		
	# Retorna o valor da string antes do argumento
	def retorna_requisicao_antes(self, requisicao_str):
		return requisicao_str[requisicao_str.find(':') + 1 : requisicao_str.find('(')]
		
	# Retorna o valor da string passada como argumento
	def retorna_requisicao_interior(self, requisicao_str):
		return requisicao_str[requisicao_str.find('(') + 1 : requisicao_str.find(')')]

	# Executa o procedimento para desconectar adequadamente um usuário
	def desconectar_usuario(self, user):
		# Fecha o socket dedicado ao usuário e deleta do vetor o usuário que sai da conversa
		user.socket.close()
		self.usuarios_conectados.remove(user)

		# Envio de mensagem para os usuários presentes quem acabou de sair
		usuario_saiu = "%s saiu..."%user.nome_usuario
		print(usuario_saiu) # Imprime no servidor
		for u in self.usuarios_conectados: # Imprime nos usuários
			u.send(bytes(usuario_saiu, 'utf-8'))
		
	# Lista de usuários no servidor, imprimindo nome de usuário, ip e porta
	def lista_conectados(self,user_list):
		for u in self.usuarios_conectados:
			user_list = "< %s|%s:|%s >"%(u.nome_usuario,u.ip,u.port)
			print(user_list)
			

	# Manipula/verifica os clientes às suas necessidades interpretando
	# as solicitações continuamente e enviando de volta a resposta apropriada
	def manipula(self, client_socket, addr):
		# Cria um novo usuário através da classe 'User' e adiciona-o na lista de usuários conectados
		usuario_atual = User(addr[0], addr[1], client_socket)
		self.usuarios_conectados.append(usuario_atual)

		while True:
			dados = usuario_atual.socket.recv(1024) # Recebe informações do usuário atual
			msg = str(dados, 'utf-8') # Converte de bytes para string
			requisicao = self.retorna_requisicao_antes(msg) # Definindo o prefixo da solicitação

			# Se o usuário quiser definir / alterar seu nome,
			# obtenha o conteúdo dentro do parêntese para ser o novo_nome_usuario.
			if requisicao == "nome": 
				novo_nome_usuario = self.retorna_requisicao_interior(msg)				
				# Verifica se o 'nome_usuario' escolhido já existe
				nome_usuario_existe = next((x for x in self.usuarios_conectados if x.nome_usuario == novo_nome_usuario), None) is not None
				# Se existir, envia uma mensagem ao usuário para que ele possa tentar novamente
				if nome_usuario_existe:
					existente_nome_usuario = "Esse nickname ja existe"
					print(existente_nome_usuario) # Imprime a frase no servidor
					usuario_atual.send(existente_nome_usuario) # Envia a frase para o usuário em questão
					
				# Caso o 'nome_usuario' escolhido não existir:
				else:
					# Se 'usuario_atual' não recebeu um 'nome_usuario', acabou de entrar no chat.
					# Caso contrário, alterou seu 'nome_usuario', informando com uma mensagem.
					if usuario_atual.nome_usuario is None:
						mensagem = "%s entrou..."%novo_nome_usuario
					else: 
						mensagem = "%s agora é %s"%(usuario_atual.nome_usuario, novo_nome_usuario)
					
					# Transforma o string em bytes, para que ela possa ser enviada aos usuários
					dados = mensagem
					# Defina o 'novo_nome_usuario' para o 'usuario_atual'
					usuario_atual.nome_usuario = novo_nome_usuario

					
			# Se o usuário não definir seu 'nome_usuario', não faz nada
			elif usuario_atual.nome_usuario == None: 
				continue
			
			elif requisicao == "lista":
				#Listagem dos usuários conectados no momento
				self.lista_conectados(usuario_atual)
				continue
				
			elif requisicao == "sair": 
			# Sair/desconectar do servidor
					self.desconectar_usuario(usuario_atual)
					break
					
			else:
				# Cria a string de mensagem, no formato: 'nome_usuario escreveu: mensagem'
				dados = "%s escreveu: %s"%(usuario_atual.nome_usuario, str(dados, 'utf-8'))

			# Imprime a mensagem no servidor
			print(dados)
			
			# E imprime também nos usuários
			for user in self.usuarios_conectados:
				user.send(dados)
								
	
	# Aceita as conexões de clientes e cria um thread individual para cada um que foi estabelecido
	def aceitar_conexoes(self):
		while True:
			client_socket,addr = self.sock.accept()
			client_socket_thread = threading.Thread(target = self.manipula, args = (client_socket, addr))
			client_socket_thread.daemon = True
			client_socket_thread.start()

	# Inicia o socket do servidor
	def run(self):
		self.sock.listen(1)

		# Cria uma thread secundária para aceitar conexões dos clientes conectados
		prompt_thread = threading.Thread(target = self.aceitar_conexoes)
		prompt_thread.daemon = True
		prompt_thread.start()

		# Imprime o status do servidor
		print("Servidor aceitando conexões...")

		while True:
			
			# Aceitando solicitações no servidor
			command = input()
			
			if command[: command.find('(')] == "lista":
				self.lista_conectados(usuario_atual)

			elif command[: command.find('(')] == "sair":
				break

			else:
				print("Erro: esse comando nao é reconhecido pelo sistema")


if __name__ == "__main__":
	server = ChatServer()
	server.run()
 
