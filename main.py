import os
import telebot
import lmstudio as lms
from dotenv import load_dotenv
from processador import processar_pdf_com_modelo


#esse codigo usa modelo gemma para poder ver imagens
#possui o comando /photo para receber imagens

load_dotenv() #ok
SERVER_API_HOST = os.getenv("SERVER_API_HOST")
CHAVE_TELEGRAM = os.getenv("CHAVE_TELEGRAM")
USUARIOS_AUTORIZADOS = [int(os.getenv("USUARIO_LUIZ"))]  # IDs dos usuários autorizados a usar o bot
lms.configure_default_client(SERVER_API_HOST)

modelo = "google/gemma-3-4b"
prompito = "voce é um robo e diz bib e bop no fim da frase."

model = lms.llm(modelo)
print(f"Modelo {modelo} carregado com sucesso.", flush=True)
bot = telebot.TeleBot(CHAVE_TELEGRAM)
chat = lms.Chat()
chat.add_system_prompt(prompito)

# Decorador para verificar autorização
def auditorada(func):
    """Decorador para verificar se o usuário está autorizado"""
    def wrapper(message):
        if not message.from_user.id in USUARIOS_AUTORIZADOS:
            bot.reply_to(message, "❌ Você não tem permissão para usar este bot.")
            return
        return func(message)
    return wrapper


@bot.message_handler(commands=['start', 'help'])
@auditorada
def send_welcome(message):
    bot.reply_to(message, "Welcome! I'm your bot.")

# Este é o manipulador de mensagens que "escuta" por imagens
@bot.message_handler(content_types=['photo'])
@auditorada
def receptor_photo(message):
    try:
        # Envia indicador de digitação
        bot.send_chat_action(message.chat.id, 'typing')

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # Criar diretório photos se não existir
        os.makedirs('photos', exist_ok=True)

        local_file_path = os.path.join('photos', f"file_{message.photo[-1].file_id}.jpg")
        with open(local_file_path, 'wb') as f:
                f.write(downloaded_file)

        # Agora usar o caminho do arquivo local
        image_handle = lms.prepare_image(local_file_path)
        bot.send_message(message.chat.id, "Imagem recebida:")


        # Envia indicador de digitação
        bot.send_chat_action(message.chat.id, 'typing')
        # Adiciona a imagem ao chat
        chat.add_user_message("descreva essa imagem", images=[image_handle])

        resposta = model.respond(chat)  
        chat.add_assistant_response(resposta)

        bot.reply_to(message, resposta)
    except Exception as e:
        print(f"Erro ao processar foto: {e}")
        bot.reply_to(message, "Erro ao processar a imagem.")

# Filtro para arquivos PDF
@bot.message_handler(content_types=['document'])
@auditorada
def receptor_pdf(message):
    # Verifica se o arquivo é um PDF
    if message.document.mime_type == 'application/pdf':
        bot.send_chat_action(message.chat.id, 'upload_document')

        print(f"PDF recebido: {message.document.file_name}")
        
        # Criar diretório documents se não existir
        os.makedirs('documents', exist_ok=True)
        local_file_path = os.path.join('documents', f"file_{message.document.file_id}.pdf")


        # Baixa o arquivo
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Salva o arquivo localmente
        file_name = message.document.file_name or f"arquivo_{message.document.file_id}.pdf"
        with open(local_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        resposta_do_conversor = processar_pdf_com_modelo(local_file_path, model)


        print(f"Arquivo PDF convertido: {file_name}")
        print(f"Resposta do conversor: {resposta_do_conversor}...")  # Imprime os primeiros 200 caracteres da resposta

        
        bot.reply_to(message, resposta_do_conversor)
        
    else:
        bot.reply_to(message, "Por favor, envie apenas arquivos PDF.")

#aqui que o llm responde as mensagens de texto
@bot.message_handler(func=lambda message: True)
@auditorada
def resp_llm(message):
    try:
        # Envia indicador de digitação
        bot.send_chat_action(message.chat.id, 'typing')

        chat.add_user_message(message.text)  # adiciona a mensagem do usuário ao chat
        # usando o chat para manter o contexto      
        resposta = model.respond(chat)  
        chat.add_assistant_response(resposta)  # adiciona a resposta do assistente
        bot.reply_to(message, resposta)
    except Exception as e:
        bot.reply_to(message, f"Erro ao processar a mensagem: {e}")





bot.polling()