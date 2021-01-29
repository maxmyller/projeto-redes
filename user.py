# TRABALHO SEGUNDA UNIDADE
# Alunos: Maxmyller Carvalho / Isaias Lucena

# A classe 'User' representa o usuário em seus atributos / métodos.

class User(object):
	ip = None # ip da conexão
	port = None # porta usada na conexão
	socket = None # mantém o socket em comunicação entre cliente / servidor
	nome_usuario = None # nome de usuário a ser exibido

	# Construtor
	def __init__(self, ip, port, socket):
		self.ip = ip
		self.port = port
		self.socket = socket

	# Método 'send' envia uma mensagem para o usuário atual usando seu socket
	def send(self, mensagem):		
		# Verifica se "mensagem" é uma string ou bytes
		canonical_type = type(mensagem)
		# Dependendo do tipo de conteúdo, adequa na variável 'dados'
		dados = bytes(mensagem, 'utf-8') if canonical_type is str else mensagem

		try:
			self.socket.send(dados)
		except:
			self.socket.close()