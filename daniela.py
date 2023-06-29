from flask import Flask, request, render_template
#from chatbot import get_response
from flask_cors import CORS
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import spacy

# Configurar el objeto para escribir en un archivo de registro
history='history.log'
context_file='context.txt'

# Crear la aplicación Flask
app = Flask(__name__)
CORS(app)
# Carga el modelo de idioma en español de Spacy
nlp = spacy.load('es_core_news_sm')

# Crea una instancia de ChatBot con el adaptador de Spacy para español
chatbot = ChatBot('Daniela', lang_adapter='chatterbot.lang.SpaCyAdapter',
                   spacy_language=nlp, storage_adapter='chatterbot.storage.SQLStorageAdapter', database_uri='sqlite:///db.sqlite3')


# Entrenar con corpus de preguntas y respuestas en español
corpus_trainer = ChatterBotCorpusTrainer(chatbot)
corpus_trainer.train('./corpus/spanish')

trainer = ListTrainer(chatbot)

def_list = [
    "Hola",
    "Hola, soy Daniela ¿en qué puedo ayudarte?",
    "¿Cómo estás?",
    "Estoy bien, gracias. ¿Y tú?",
    "Estoy mal",
    "Lo siento mucho. ¿Puedo ayudarte en algo?",
    "Como te llamas",
    "Mi nombre es Daniela"
    ]

# Lee el archivo de texto y crea una lista de conversaciones
with open(context_file, 'r') as file:
    convers = file.readlines()
    
# Crea un objeto ListTrainer y entrena al bot con las conversaciones
trainer = ListTrainer(chatbot)
trainer.train(convers)
trainer.train(def_list)


@app.route('/')
def home():
    # Leer el archivo de registro y obtener las conversaciones
    with open(history, 'r') as f:
        history_data = f.readlines()
    # Pasar las conversaciones a la plantilla HTML
    return render_template('index.html', history = history_data)

# Ruta para el inicio de la conversación
@app.route('/get')
def chatbot_response():
    # Obtener la pregunta del usuario
    user_input = request.args.get('msg')
    # Obtener la respuesta del chatbot
    chatbot_response = chatbot.get_response(user_input)
    # Escribir la conversación en el archivo de registro
    with open(history, 'a') as f:
        f.write('<p><b>&gt;&gt;</b> ' + user_input + '</p>\n')
        f.write('<p><b>&gt; ' + str(chatbot_response) + '</b></p>\n')
    # Devolver la respuesta del chatbot como texto
    temp_response = str(chatbot_response)
    return temp_response

@app.route('/clear')
def clear_context():
        # Abrir el archivo de historial en modo escritura
    with open(history, "w") as temp:
        # Escribir una cadena vacía en el archivo
        temp.write("")
    # Borrar el contexto de ChatterBot
    #chatbot.storage.drop()
    return ""

# Ruta para aprender de la interacción y guardar la conversación en la base de datos
@app.route('/feedback')
def do_feedback():
    # Aprender de la cadena de texto proporcionada
    # Obtener la pregunta del usuario
    user_input = request.args.get('msg')
    temp_question = request.args.get('tmp')
    with open(context_file, 'a') as f:
        f.write('Q: ' + temp_question + '\n')
        f.write('A: ' + user_input)
    # Lee el archivo de texto y crea una lista de conversaciones
    with open(context_file, 'r') as file:
        convers = file.readlines()
    trainer.train(convers)
    return ""


# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)