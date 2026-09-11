"""
Tarea #3 - Bot de Telegram (IA1 - Seccion A - 2S2026)
Oswaldo Antonio Choc Cuteres - 201901844

Bot interactivo de Telegram construido con python-telegram-bot.
Responde a comandos con parametros, muestra un menu con botones
inline y valida las entradas del usuario sin detener el proceso
ante errores.

Requiere la variable de entorno TELEGRAM_TOKEN (ver .env.example).
"""

import os
import random
import logging
import asyncio
from datetime import datetime

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Datos del grupo (actualizar cuando se sumen mas integrantes)
# ---------------------------------------------------------------------------
INTEGRANTES = [
    ("Brando Ivan Munoz Debroy", "201700890"),
    ("Geovanni Eduardo Nufio Illescas", "201901444"),
    ("Oswaldo Antonio Choc Cuteres", "201901844"),
    ("Kelly Zuceth Gutierrez Velasquez", "201901457"),
    ("Luis Eduardo Monroy Perez", "201800918"),
]

CONTACTO = (
    "Contacto del grupo\n"
    "Correo: 3014167370101@ingenieria.usac.edu.gt\n"
    "Curso: Inteligencia Artificial 1 - Seccion A - 2S2026"
)

UNIDADES_A_METROS = {
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
    "ft": 0.3048,
}

COMANDOS_INFO = {
    "/hola": "Saluda al usuario usando su nombre de Telegram.",
    "/hora": "Muestra la fecha y hora actual del servidor.",
    "/contacto": "Muestra la informacion de contacto del grupo.",
    "/integrantes": "Muestra nombre y carnet de los integrantes.",
    "/ayuda": "Muestra esta lista de comandos.",
    "/menu": "Muestra un menu interactivo con botones.",
    "/calcular <n1> <op> <n2>": "Suma, resta, multiplica o divide dos numeros. Ej: /calcular 4 + 5",
    "/tabla <numero>": "Muestra la tabla de multiplicar del 1 al 10. Ej: /tabla 7",
    "/convertir <cantidad> <origen> <destino>": "Convierte entre cm, m, km, mi, ft. Ej: /convertir 10 km mi",
    "/aleatorio <min> <max>": "Genera un entero aleatorio entre min y max. Ej: /aleatorio 1 100",
}


def _texto_ayuda() -> str:
    lineas = ["Comandos disponibles:\n"]
    for comando, descripcion in COMANDOS_INFO.items():
        lineas.append(f"{comando} - {descripcion}")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Comandos basicos
# ---------------------------------------------------------------------------
async def cmd_hola(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name or "amigo/a"
    await update.message.reply_text(f"Hola, {nombre}! Bienvenido/a al bot de la Tarea 3 de IA1.")

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name or "amigo/a"
    await update.message.reply_text(
        f"Hola, {nombre}! Soy el bot de la Tarea 3 de IA1.\n\n" + _texto_ayuda()
    )

async def cmd_hora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ahora = datetime.now().strftime("%A %d de %B de %Y, %H:%M:%S")
    await update.message.reply_text(f"Fecha y hora actual: {ahora}")


async def cmd_contacto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CONTACTO)


async def cmd_integrantes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lineas = ["Integrantes del grupo:\n"]
    for nombre, carnet in INTEGRANTES:
        lineas.append(f"- {nombre} ({carnet})")
    await update.message.reply_text("\n".join(lineas))


async def cmd_ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(_texto_ayuda())


# ---------------------------------------------------------------------------
# Menu interactivo
# ---------------------------------------------------------------------------
def _teclado_menu() -> InlineKeyboardMarkup:
    botones = [
        [InlineKeyboardButton("Saludo", callback_data="menu_hola"),
         InlineKeyboardButton("Hora", callback_data="menu_hora")],
        [InlineKeyboardButton("Contacto", callback_data="menu_contacto"),
         InlineKeyboardButton("Integrantes", callback_data="menu_integrantes")],
        [InlineKeyboardButton("Calculadora", callback_data="menu_calcular"),
         InlineKeyboardButton("Tabla", callback_data="menu_tabla")],
        [InlineKeyboardButton("Convertir", callback_data="menu_convertir"),
         InlineKeyboardButton("Aleatorio", callback_data="menu_aleatorio")],
        [InlineKeyboardButton("Ayuda completa", callback_data="menu_ayuda")],
    ]
    return InlineKeyboardMarkup(botones)


async def cmd_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Menu principal - elige una opcion:",
        reply_markup=_teclado_menu(),
    )


async def on_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    opcion = query.data

    if opcion == "menu_hola":
        nombre = query.from_user.first_name or "amigo/a"
        texto = f"Hola, {nombre}!"
    elif opcion == "menu_hora":
        texto = f"{datetime.now().strftime('%A %d de %B de %Y, %H:%M:%S')}"
    elif opcion == "menu_contacto":
        texto = CONTACTO
    elif opcion == "menu_integrantes":
        texto = "\n".join(f"- {n} ({c})" for n, c in INTEGRANTES)
    elif opcion == "menu_ayuda":
        texto = _texto_ayuda()
    elif opcion == "menu_calcular":
        texto = "Uso: /calcular <numero1> <operador> <numero2>\nEj: /calcular 8 / 2\nOperadores validos: + - * /"
    elif opcion == "menu_tabla":
        texto = "Uso: /tabla <numero>\nEj: /tabla 7"
    elif opcion == "menu_convertir":
        texto = "Uso: /convertir <cantidad> <origen> <destino>\nEj: /convertir 10 km mi\nUnidades: cm, m, km, mi, ft"
    elif opcion == "menu_aleatorio":
        texto = "Uso: /aleatorio <min> <max>\nEj: /aleatorio 1 100"
    else:
        texto = "Opcion no reconocida."

    await query.edit_message_text(texto, reply_markup=_teclado_menu())


# ---------------------------------------------------------------------------
# Comandos con parametros y logica
# ---------------------------------------------------------------------------
OPERADORES = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


async def cmd_calcular(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 3:
        await update.message.reply_text(
            "Uso incorrecto.\nFormato: /calcular <numero1> <operador> <numero2>\n"
            "Ej: /calcular 4 + 5\nOperadores validos: + - * /"
        )
        return

    n1_str, operador, n2_str = args

    try:
        n1 = float(n1_str)
        n2 = float(n2_str)
    except ValueError:
        await update.message.reply_text("numero1 y numero2 deben ser numeros validos. Ej: /calcular 4 + 5")
        return

    if operador not in OPERADORES:
        await update.message.reply_text("Operador invalido. Usa uno de: + - * /")
        return

    if operador == "/" and n2 == 0:
        await update.message.reply_text("No se puede dividir entre cero.")
        return

    resultado = OPERADORES[operador](n1, n2)
    await update.message.reply_text(f"Resultado: {n1} {operador} {n2} = {resultado}")


async def cmd_tabla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Uso: /tabla <numero>\nEj: /tabla 7")
        return

    try:
        numero = int(args[0])
    except ValueError:
        await update.message.reply_text("<numero> debe ser un numero entero. Ej: /tabla 7")
        return

    lineas = [f"Tabla del {numero}:"]
    for i in range(1, 11):
        lineas.append(f"{numero} x {i} = {numero * i}")
    await update.message.reply_text("\n".join(lineas))


async def cmd_convertir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 3:
        await update.message.reply_text(
            "Uso: /convertir <cantidad> <unidad_origen> <unidad_destino>\n"
            "Ej: /convertir 10 km mi\nUnidades soportadas: cm, m, km, mi, ft"
        )
        return

    cantidad_str, origen, destino = args
    origen = origen.lower()
    destino = destino.lower()

    try:
        cantidad = float(cantidad_str)
    except ValueError:
        await update.message.reply_text("<cantidad> debe ser un numero valido. Ej: /convertir 10 km mi")
        return

    if origen not in UNIDADES_A_METROS or destino not in UNIDADES_A_METROS:
        await update.message.reply_text("Unidad invalida. Unidades soportadas: cm, m, km, mi, ft")
        return

    metros = cantidad * UNIDADES_A_METROS[origen]
    resultado = metros / UNIDADES_A_METROS[destino]
    await update.message.reply_text(f"{cantidad} {origen} = {resultado:.4f} {destino}")


async def cmd_aleatorio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Uso: /aleatorio <min> <max>\nEj: /aleatorio 1 100")
        return

    try:
        minimo = int(args[0])
        maximo = int(args[1])
    except ValueError:
        await update.message.reply_text("<min> y <max> deben ser numeros enteros. Ej: /aleatorio 1 100")
        return

    if minimo >= maximo:
        await update.message.reply_text("<min> debe ser menor que <max>.")
        return

    numero = random.randint(minimo, maximo)
    await update.message.reply_text(f"Numero aleatorio entre {minimo} y {maximo}: {numero}")


# ---------------------------------------------------------------------------
# Manejo de comandos inexistentes y errores globales
# ---------------------------------------------------------------------------
async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Comando no reconocido. Usa /ayuda para ver la lista de comandos disponibles."
    )


async def manejador_errores(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Excepcion no manejada: %s", context.error, exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "Ocurrio un error al procesar tu solicitud. Intenta de nuevo o revisa /ayuda."
        )


def main():
    if not TELEGRAM_TOKEN:
        raise RuntimeError(
            "No se encontro TELEGRAM_TOKEN. Copia .env.example a .env y coloca tu token."
        )

    # Python 3.14 elimino la creacion automatica de un event loop en el
    # hilo principal cuando no existe uno (antes solo mostraba un aviso).
    # python-telegram-bot 21.x todavia depende de ese comportamiento
    # antiguo internamente, asi que lo creamos manualmente antes de que
    # la libreria lo busque, evitando el RuntimeError al iniciar.
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("hola", cmd_hola))
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("hora", cmd_hora))
    app.add_handler(CommandHandler("contacto", cmd_contacto))
    app.add_handler(CommandHandler("integrantes", cmd_integrantes))
    app.add_handler(CommandHandler("ayuda", cmd_ayuda))
    app.add_handler(CommandHandler("menu", cmd_menu))
    app.add_handler(CommandHandler("calcular", cmd_calcular))
    app.add_handler(CommandHandler("tabla", cmd_tabla))
    app.add_handler(CommandHandler("convertir", cmd_convertir))
    app.add_handler(CommandHandler("aleatorio", cmd_aleatorio))

    app.add_handler(CallbackQueryHandler(on_menu_click))

    # Cualquier /comando no registrado cae aqui (debe ir despues de los CommandHandler)
    app.add_handler(MessageHandler(filters.COMMAND, comando_desconocido))

    app.add_error_handler(manejador_errores)

    logger.info("Bot iniciado. Esperando mensajes...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
