import os
import telebot
import lmstudio as lms
from dotenv import load_dotenv
from core.processador import processar_pdf_com_modelo
from core.processador import remove_thinking_tags


#Esse codigo usa modelo gemma e docling para processar pdfs enviados por telegram e responder com os dados extraidos.
#O modelo é configurado para ser usado com o servidor API do lmstudio.
#O código inclui tratamento de mensagens de texto, fotos e documentos PDF, respondendo de acordo com o tipo de conteúdo recebido.


load_dotenv()
SERVER_API_HOST = os.getenv("SERVER_API_HOST")
CHAVE_TELEGRAM = os.getenv("CHAVE_TELEGRAM")
USUARIOS_AUTORIZADOS = [int(os.getenv("USUARIO_1"))]
lms.configure_default_client(SERVER_API_HOST)

modelo = "google/gemma-4-e2b"
prompito = "voce é um robo e diz bib e bop no fim da frase."

model = lms.llm(modelo)
print(f"Modelo {modelo} carregado com sucesso.", flush=True)
bot = telebot.TeleBot(CHAVE_TELEGRAM)
chat = lms.Chat()
chat.add_system_prompt(prompito)


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


@bot.message_handler(content_types=['photo'])
@auditorada
def receptor_foto(message):
    try:
        
        bot.send_chat_action(message.chat.id, 'typing')

        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        os.makedirs('photos', exist_ok=True)

        local_file_path = os.path.join('photos', f"file_{message.photo[-1].file_id}.jpg")
        with open(local_file_path, 'wb') as f:
                f.write(downloaded_file)

        
        image_handle = lms.prepare_image(local_file_path)
        bot.send_message(message.chat.id, "Imagem recebida:")

        bot.send_chat_action(message.chat.id, 'typing')

        RESPOSTA_SIM_NOTA = '1'
        RESPOSTA_NAO_NOTA = '0'

        verific_image = model.respond(f"verifique se a imagem é uma nota fiscal, responda apenas com '{RESPOSTA_SIM_NOTA}' ou '{RESPOSTA_NAO_NOTA}'. {RESPOSTA_SIM_NOTA} para sim, {RESPOSTA_NAO_NOTA} para nao.", images=[image_handle])


        if verific_image.strip() == RESPOSTA_SIM_NOTA:
            bot.send_message(message.chat.id, "Imagem reconhecida como nota fiscal. Processando...")
            resposta_do_conversor = processar_pdf_com_modelo(local_file_path, model)
            bot.reply_to(message, resposta_do_conversor)

        elif verific_image.strip() == RESPOSTA_NAO_NOTA:
            chat.add_user_message("descreva essa imagem", images=[image_handle])
            resposta = model.respond(chat)
            resposta = remove_thinking_tags(resposta)
            chat.add_assistant_response(resposta)

        else:
            resposta = "Não foi possível determinar o tipo da imagem. Por favor, envie uma nota fiscal ou uma foto clara do produto."

        

        bot.reply_to(message, resposta)

    except Exception as e:
        print(f"Erro ao processar foto: {e}")
        bot.reply_to(message, "Erro ao processar a imagem.")


@bot.message_handler(content_types=['document'])
@auditorada
def receptor_pdf(message):
    try:
        
        bot.send_chat_action(message.chat.id, 'typing')

        if message.document.mime_type == 'application/pdf':
            bot.send_chat_action(message.chat.id, 'upload_document')

            print(f"PDF recebido: {message.document.file_name}")
            
            os.makedirs('documents', exist_ok=True)
            local_file_path = os.path.join('documents', f"file_{message.document.file_id}.pdf")


            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            file_name = message.document.file_name or f"arquivo_{message.document.file_id}.pdf"
            with open(local_file_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            resposta_do_conversor = processar_pdf_com_modelo(local_file_path, model)


            print(f"Arquivo PDF convertido: {file_name}")
            print(f"Resposta do conversor: {resposta_do_conversor}...")

            
            bot.reply_to(message, resposta_do_conversor)
            
        else:
            bot.reply_to(message, "Por favor, envie apenas arquivos PDF.")

    except Exception as e:
        print(f"Erro ao processar PDF: {e}")
        bot.reply_to(message, "Erro ao processar documento.")


@bot.message_handler(func=lambda message: True)
@auditorada
def resp_llm(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')

        chat.add_user_message(message.text)     
        resposta = model.respond(chat)
        resposta = remove_thinking_tags(resposta)
        chat.add_assistant_response(resposta)
        bot.reply_to(message, resposta)

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        bot.reply_to(message, f"Erro ao processar a mensagem: {e}")





bot.polling()