# Tarea #3 - Bot de Telegram (Python + API de Telegram)

**Universidad de San Carlos de Guatemala - Facultad de Ingenieria**
**Inteligencia Artificial 1 - Seccion A - Segundo Semestre 2026**

## 1. Integrantes

| Nombre | Carnet | Porcentaje (%) |
|---|---|---|
| Brando Ivan Munoz Debroy | 201700890 | 20 |
| Geovanni Eduardo Nufio Illescas | 201901444 | 20 |
| Oswaldo Antonio Choc Cuteres | 201901844 | 20 |
| Kelly Zuceth Gutierrez Velasquez | 201901457 | 20 |
| Luis Eduardo Monroy Perez | 201800918 | 20 |

## 2. Descripcion del bot

Bot interactivo de Telegram construido con **Python** y la libreria
`python-telegram-bot` (que consume la API oficial de Telegram). Permite
interaccion mediante comandos, recibe parametros, valida entradas
invalidas o incompletas sin detenerse, y cuenta con un menu interactivo
mediante botones inline.

## 3. Comandos implementados

| Comando | Descripcion |
|---|---|
| `/hola` | Saluda al usuario utilizando su nombre de Telegram. |
| `/hora` | Muestra la fecha y hora actual obtenida dinamicamente. |
| `/contacto` | Muestra la informacion de contacto definida por el grupo. |
| `/integrantes` | Muestra el nombre y carnet de los integrantes del grupo. |
| `/ayuda` | Muestra la lista de comandos disponibles y su descripcion. |
| `/menu` | Muestra un menu interactivo con botones de Telegram. |
| `/calcular <numero1> <operador> <numero2>` | Suma, resta, multiplica o divide dos numeros. Valida tipos, operador y division entre cero. Ej: `/calcular 4 + 5` |
| `/tabla <numero>` | Muestra la tabla de multiplicar del numero, del 1 al 10. Ej: `/tabla 7` |
| `/convertir <cantidad> <unidad_origen> <unidad_destino>` | Convierte unidades de longitud entre cm, m, km, mi y ft. Ej: `/convertir 10 km mi` |
| `/aleatorio <min> <max>` | Genera un numero entero aleatorio entre min y max (min debe ser menor que max). Ej: `/aleatorio 1 100` |

Cualquier comando no reconocido, o un comando con parametros invalidos o
incompletos, responde con un mensaje de error y, cuando aplica, el
formato correcto de uso, sin detener el bot.

## 4. Como instalar y ejecutar (local)

### Requisitos previos

- Python 3.10 o superior.
- Un token de bot generado con **BotFather** en Telegram.

### 4.1 Configuracion

```bash
cd "Tarea#3"
python -m venv venv

# Windows
venv\Scripts\Activate.ps1
# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Editar .env y colocar el TELEGRAM_TOKEN real (nunca subir este archivo)
```

### 4.2 Ejecucion

```bash
python bot.py
```

El bot queda escuchando mediante *long polling*; para probarlo, abrir el
chat o grupo de Telegram donde este agregado y enviar cualquiera de los
comandos de la seccion 3.

## 5. Despliegue en la nube (PENDIENTE)

El bot funciona igual en local que en la nube: la logica de los
comandos es independiente de donde corra el proceso, lo unico que
cambia es donde queda alojado para que se mantenga activo 24/7 durante
el periodo de calificacion.

**Esta parte queda pendiente a proposito** para que el resto del grupo
decida la nube a utilizar y se encargue del despliegue (se evaluo AWS
como una opcion, pero queda abierto a lo que el grupo prefiera). Una
vez desplegado, actualizar esta seccion con:

- Plataforma utilizada y breve justificacion.
- Pasos de despliegue (o link a un script/documento con el detalle).
- Como se configura el `TELEGRAM_TOKEN` como variable de entorno en ese
  entorno (sin exponerlo en el codigo ni en el repositorio).

## 6. Reparto de trabajo

| Integrante | Aporte |
|---|---|
| Oswaldo Antonio Choc Cuteres | Desarrollo completo de la logica del bot: los 10 comandos obligatorios, validaciones de entrada, manejo de errores/comandos inexistentes y menu interactivo con botones. |
| Brando Ivan Munoz Debroy, Geovanni Eduardo Nufio Illescas, Kelly Zuceth Gutierrez Velasquez, Luis Eduardo Monroy Perez | Despliegue en la nube (pendiente, ver seccion 5). |

> Distribucion acordada por el grupo: 20% para cada integrante.

## 7. Estructura de entrega en el repositorio

```
IA1_2026S2_Tareas_A/
└── Tarea#3/
    ├── bot.py
    ├── requirements.txt
    ├── .env.example
    ├── .gitignore
    └── README.md
```

## 8. Link del bot / chat de Telegram

Bot de pruebas: https://t.me/G10_ia1_tarea3_bot (username: `G10_ia1_tarea3_bot`)
