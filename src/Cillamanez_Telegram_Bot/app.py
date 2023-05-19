from decouple import config #Importamos la libreria decouple para poder leer las variables de entorno
import telebot #Importamos la libreria de telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply#Importamos la libreria de ReplyKeyboardMarkup
from Constellations_runner import constellations
from Constellations import plot_stars 
from RR_runner import RR_SHOW
import sympy as sp
import re
import os

#Variables de entorno
TOKEN = config('TOKEN')

commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    'menu'        : 'Shows the main menu options',
}

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

#Creamos el bot
bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener

#Creamos el comando /start
@bot.message_handler(commands=['start'])
def cmd_start(message):
    """Da la bienvenida al usuario"""
    bot.reply_to(message, "Hola, bienvenido al bot de Cillamanez. Usa el comando /menu para ver las opciones disponibles")


@bot.message_handler(commands=['menú', 'menu'])
def main_menu(message):
   clear_cache()
   markup = InlineKeyboardMarkup(row_width=1)
   b1 = InlineKeyboardButton("Estrellas y Constelaciones", callback_data="constellations")
   b2 = InlineKeyboardButton("Relaciones de Recurrencia.", callback_data="RR")
   b3 = InlineKeyboardButton("Cerrar", callback_data="close")
   markup.add(b1, b2, b3)
   bot.send_message(message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)

#Creamos el comando /info
@bot.message_handler(commands=['info'])
def cmd_info(message):
    """Muestra informacion del bot"""
    bot.reply_to(message, "Este bot fue creado por Cillamanez")

# help page
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

def cmd_constellations_menu(message):
   markup = InlineKeyboardMarkup(row_width=1)
   b1 = InlineKeyboardButton("Graficar todas las estrellas.", callback_data="1.1")
   b2 = InlineKeyboardButton("Graficar todas las estrellas y una constellación", callback_data="1.2")
   b3 = InlineKeyboardButton("Graficar todas las estrellas y todas las constellaciones", callback_data="1.3")
   b4 = InlineKeyboardButton("Volver", callback_data="volver")
   markup.add(b1, b2, b3, b4)
   bot.send_message(message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)

def cmd_constellations_sub_menu(message):
    markup = InlineKeyboardMarkup(row_width=1)
    b1 = InlineKeyboardButton("Boyero", callback_data="Boyero")
    b2 = InlineKeyboardButton("Casiopea", callback_data="Casiopea")
    b3 = InlineKeyboardButton("Cazo", callback_data="Cazo")
    b4 = InlineKeyboardButton("Cygnet", callback_data="Cygnet")
    b5 = InlineKeyboardButton("Geminis", callback_data="Geminis")
    b6 = InlineKeyboardButton("Hydra", callback_data="Hydra")
    b7 = InlineKeyboardButton("Osa Mayor", callback_data="Osa Mayor")
    b8 = InlineKeyboardButton("Osa Menor", callback_data="Osa Menor")
    b9 = InlineKeyboardButton("Volver", callback_data="volver")
    markup.add(b1, b2, b3, b4, b5, b6, b7, b8, b9)
    bot.send_message(message.chat.id, "Selecciona una constelación:", reply_markup=markup)

RR = {}

def cmd_grado_rr(message):
    """Pregunta el grado de la relación de recurrencia"""
    msg = bot.send_message(message.chat.id, "¿Cuál es el grado de la relación de recurrencia?")
    bot.register_next_step_handler(message, cmd_coeficientes_rr)
    

def cmd_coeficientes_rr(message):
    """Pregunta los coeficientes de la relación de recurrencia"""
    ##Si el usuario no responde con un número, se le vuelve a preguntar
    if not message.text.isdigit():
        msg = bot.send_message(message.chat.id, "Error: Ingresa un número. \n¿Cuál es el grado de la relación de recurrencia?")
        bot.register_next_step_handler(msg, cmd_coeficientes_rr)
    else:
        RR[message.chat.id]={}
        RR[message.chat.id]['grado'] = message.text
        RR[message.chat.id]['coeficientes'] = []
        RR[message.chat.id]['condiciones_iniciales'] = []
        RR[message.chat.id]['i'] = int(message.text)
        RR[message.chat.id]['i2'] = int(message.text)
        bot.send_message(message.chat.id, f"Dime el coeficiente de f(n - {RR[message.chat.id]['i']}):")
        bot.register_next_step_handler(message, save_coeficientes_rr)

def save_coeficientes_rr(message):
    if not message.text.isdigit():
        indice_coeficiente = RR[message.chat.id]['i']
        msg = bot.send_message(message.chat.id, f"Error: Ingresa un número. Dime el coeficiente de f(n - {indice_coeficiente} ):")
        bot.register_next_step_handler(msg, save_coeficientes_rr)
    else:
        if RR[message.chat.id]['i']>0:
            RR[message.chat.id]['i'] = RR[message.chat.id]['i']-1
            indice_coeficiente = RR[message.chat.id]['i']

        RR[message.chat.id]['coeficientes'].append(int(message.text))

        if RR[message.chat.id]['i'] == 0:
            bot.send_message(message.chat.id,  f"Dime el valor de f({RR[message.chat.id]['i2']-1}):")
            bot.register_next_step_handler(message, save_condiciones_iniciales_rr)
        else:
            bot.send_message(message.chat.id, f"Dime el coeficiente de f(n - {indice_coeficiente}):")
            bot.register_next_step_handler(message, save_coeficientes_rr)

def cmd_condiciones_iniciales_rr(message):
    """Pregunta las condiciones iniciales de la relación de recurrencia"""
    bot.register_next_step_handler(message, guardar_datos)

def save_condiciones_iniciales_rr(message):
    if not message.text.isdigit():
        indice_condicion = RR[message.chat.id]['i2']
        msg = bot.send_message(message.chat.id, f"Error: Ingresa un número. Dime el valor de f({indice_condicion-1}):")
        bot.register_next_step_handler(msg, save_condiciones_iniciales_rr)
    else:
        if RR[message.chat.id]['i2']>0:
            RR[message.chat.id]['i2'] = RR[message.chat.id]['i2']-1
            indice_condicion = RR[message.chat.id]['i2']
        
        RR[message.chat.id]['condiciones_iniciales'].append(int(message.text))
        if RR[message.chat.id]['i2'] == 0:
            bot.send_message(message.chat.id, f"Ingrese la función g(n): ")
            bot.register_next_step_handler(message, save_funcion_rr)
        else:
            bot.send_message(message.chat.id, f"Dime el valor de f({RR[message.chat.id]['i2']-1}):")
            bot.register_next_step_handler(message, save_condiciones_iniciales_rr)



def save_funcion_rr(message):
    regex = r"^[nN\d\W]*$" #Expresión regular para validar la función
    if re.match(regex, message.text):
        try:
            g_n = sp.sympify(message.text)
            RR[message.chat.id]['funcion'] = g_n
            markup = InlineKeyboardMarkup(row_width=1)
            b1 = InlineKeyboardButton("Mostrar resultado", callback_data="show_result")
            b2 = InlineKeyboardButton("Cancelar", callback_data="cancel")
            markup.add(b1, b2)
            bot.send_message(message.chat.id, "Desea imprimir los resultados?", reply_markup=markup)
        except (sp.SympifyError, ValueError):
            msg = bot.send_message(message.chat.id, "Error: Ingresa una función válida. \nIngrese la función g(n): ")
            bot.register_next_step_handler(msg, save_funcion_rr)
    else:
        msg = bot.send_message(message.chat.id, "Error: Ingresa una función válida. \nIngrese la función g(n): ")
        bot.register_next_step_handler(msg, save_funcion_rr)
        

def guardar_datos(message):
    """Guarda los datos de la relación de recurrencia"""
    texto = 'Datos introducidos por el usuario: \n'
    texto += 'Grado: ' + RR[message.chat.id]['grado'] + '\n'
    for i in range(len(RR[message.chat.id]['coeficientes'])):
        texto += 'Coeficiente de f(n - ' + str(i) + '): ' + str(RR[message.chat.id]['coeficientes'][i]) + '\n'
    for i in range(len(RR[message.chat.id]['condiciones_iniciales'])):
        texto += 'Valor de f(' + str(i) + '): ' + str(RR[message.chat.id]['condiciones_iniciales'][i]) + '\n'
    bot.send_message(message.chat.id, texto, parse_mode='HTML')
    del RR[message.chat.id]

def clear_cache():
    dir = 'generated_images'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    dir2 = 'temps'
    for f in os.listdir(dir2):
        os.remove(os.path.join(dir2, f))

@bot.callback_query_handler(func=lambda x: True)
def respuesta_botones_inline(call):
    """Gestion las acciones de los botones callback_data"""
    cid = call.from_user.id
    mid = call.message.id
    if call.data == "close":
        bot.delete_message(cid, mid)
    elif call.data == "volver" or call.data == "cancel":
        bot.delete_message(cid, mid)
        main_menu(call.message)
    elif call.data == "constellations":
        bot.delete_message(cid, mid)
        cmd_constellations_menu(call.message)
    elif call.data == "RR":
        bot.delete_message(cid, mid)
        cmd_grado_rr(call.message)
    elif call.data == "show_result":
        bot.delete_message(cid, mid)
        RR_SHOW(RR[call.message.chat.id]['grado'], RR[call.message.chat.id]['coeficientes'], RR[call.message.chat.id]['condiciones_iniciales'], RR[call.message.chat.id]['funcion'])
        foto1 = open(r'generated_images/formula1.png', 'rb')
        bot.send_photo(cid, foto1, "Formula con coeficientes no resueltos: ")

        foto2 = open(r'generated_images/formula2.png', 'rb')
        bot.send_photo(cid, foto2, "Formula con coeficientes resueltos: ")
        del RR[call.message.chat.id]
    elif call.data == "1.1":
        bot.delete_message(cid, mid)
        constellations(1)
        foto = open('generated_images\constellations.jpg', 'rb')
        bot.send_photo(cid, foto, "Imagen de todas las estrellas")
    elif call.data == "1.2":
        bot.delete_message(cid, mid)
        cmd_constellations_sub_menu(call.message)
    elif call.data == "1.3":
        bot.delete_message(cid, mid)
        constellations(3)
        foto = open('generated_images\constellations.jpg', 'rb')
        bot.send_photo(cid, foto, "Imagen de todas las estrellas y todas las constelaciones")
    elif call.data in plot_stars.Constellations_path:
        bot.delete_message(cid, mid)
        constellations(2, call.data)
        foto = open('generated_images\constellations.jpg', 'rb')
        bot.send_photo(cid, foto, "Imagen de todas las estrellas y la constelación " + call.data)


def bot_start():
    """Bucle principal del bot"""
    bot.infinity_polling()

if __name__ == '__main__':
    print("El bot se esta ejecutando")
    #Creamos el hilo del bot
    #bot_thread = threading.Thread(name = "thread_bot", target=bot_start)
    #bot_thread.start()
    bot.infinity_polling()