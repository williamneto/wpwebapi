 CAMADAS

1) webapp - serve a API
   	. recebe requisições e processa
   	. inicia o whatsapp driver e envia comandos
   	. devolve retorno
2) whatsapp driver - faz operações no whatsapp
   	. recebe comandos da API e executa
   	. registra operações
   	. devolve retorno
3) model
   	. usuários
     	- nome
      	- chave de acesso
   	. operações
      	- usuário
      	- tipo - ADD ou VIEW
      

DEFINIÇÕES

1) requisições - todas requerem chave de acesso (?user)
	. solicitação de login - ?user=XXX
      - /start_login/
		. retorna QRCode
      * Até um minuto e meio de espera por requisição
      * Quando a seção está salva e não necessita leitura
      * do qrcode, espera de 40s aproximadamente
	. confirmação de login - ?user=XXX
      - /confirm_login /
		. retorna se o QRCode foi lido
	. visualizar chats - ?user=XXX
      - /get_chats/
		. retorna chats - mensagens lidas e não lidas
      - /chat/<id>/
      . retorna um chat e suas mensagens
      * apenas as 21 últimas mensagens
      * necessario implementar backp de mensagens
      * não baixa videos
      * mesma mídia baixada diversas vezes em arquivos diferentes
	. envio de mensagem - ?user=XXX&number=XXX&message=XXX
      - /send_message
		- abre um chat e envia mensagem
	. criação de grupos
      - /create_group
2) comandos
3) operações