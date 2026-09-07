# Guia para el equipo - Bot de Telegram (Tarea #3, IA1)

Esta guia es para el resto del equipo: como levantar el bot en su propia
maquina para probarlo, y una base generica para subirlo a la nube sin
importar que proveedor decidan usar (AWS, GCP, Azure, Render, Railway,
un VPS, etc.). El detalle "oficial" para la entrega (comandos,
integrantes, etc.) esta en `README.md`; este archivo es un complemento
practico paso a paso.

## 1. Que necesitan instalado

- **Python 3.10 o superior** (revisen con `python --version`). Si tienen
  Python 3.14 y al correr el bot les sale un error de
  `RuntimeError: There is no current event loop`, no es nada suyo: ya
  esta resuelto en `bot.py` (Python 3.14 cambio como maneja el event
  loop de asyncio y la libreria del bot todavia esperaba el
  comportamiento viejo).
- **Git**, para clonar/actualizar el repositorio.
- Una cuenta de **Telegram** (para hablar con BotFather y con el bot).

## 2. Obtener su propio token de prueba (opcional pero recomendado)

Cada quien puede tener su propio bot de pruebas mientras desarrolla, para
no chocar entre si mismos:

1. Abran Telegram y busquen `@BotFather` (el oficial, tiene el check azul).
2. Envien `/newbot`.
3. Pongan un nombre visible (el que quieran) y un username unico que
   termine en `bot` (ej. `tunombre_ia1_tarea3_bot`).
4. BotFather les da un token con formato `numeros:letras_y_numeros`.
   Cópienlo, es su credencial - no lo compartan ni lo suban a GitHub.
5. Para hablarle a SU bot (no a BotFather), abran el link que BotFather
   les da (`t.me/su_username_bot`) o busquen ese username en Telegram, y
   denle **Start**.

El bot que ya quedo funcionando y que se entregara es
`G10_ia1_tarea3_bot` (link en la seccion 8 del `README.md`); usar uno
propio es solo para probar cambios sin pisarse entre integrantes antes
de fusionar a la rama principal.

## 3. Clonar y preparar el entorno local

```powershell
git clone https://github.com/Oswaldo052001/IA1_2026S2_Tareas_A.git
cd IA1_2026S2_Tareas_A/Tarea#3

python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
# source venv/bin/activate      # Linux / Mac

pip install -r requirements.txt

copy .env.example .env          # Windows
# cp .env.example .env          # Linux / Mac
```

Abran el `.env` con cualquier editor y reemplacen la linea por su token
real:

```
TELEGRAM_TOKEN=su_token_de_botfather_aqui
```

El `.env` esta en `.gitignore`: nunca se sube al repo. Solo se sube
`.env.example` (sin token real), que ya esta en el repositorio.

## 4. Ejecutar el bot localmente

```powershell
python bot.py
```

Si carga bien, la consola se queda mostrando algo como:

```
... INFO ... Bot iniciado. Esperando mensajes...
```

Eso es normal, significa que quedo escuchando. Mientras esa terminal
siga abierta, abran el chat con su bot en Telegram y prueben, por
ejemplo:

```
/hola
/menu
/calcular 4 + 5
/tabla 7
/convertir 10 km mi
/aleatorio 1 100
/integrantes
/calcular abc + 5      -> deberia responder con el mensaje de error, sin tumbar el bot
```

Para detenerlo, `Ctrl+C` en esa misma terminal.

## 5. Base para desplegar en la nube (independiente del proveedor)

Este bot usa **long polling** (`app.run_polling()`), o sea que el
proceso de Python tiene que quedar corriendo de forma continua y con
salida a internet hacia `api.telegram.org`. Eso significa que, sin
importar la nube que elijan, necesitan un servicio que:

1. **Mantenga un proceso vivo 24/7** (no algo que se "duerma" o se
   apague solo despues de responder una peticion, como si fuera un
   endpoint HTTP sin trafico). Ejemplos que SI sirven: una VM/instancia
   siempre encendida (EC2, Compute Engine, un droplet, un VPS), un
   contenedor con politica de reinicio (ECS/Fargate, un "worker" de
   Render/Railway/Fly.io), o un servicio systemd en un servidor propio.
   Ejemplos que NO sirven tal cual (estan pensados para
   peticion-respuesta, no para procesos de fondo persistentes): AWS
   Lambda o Google Cloud Functions puros, o Cloud Run con
   "scale to zero" sin ajustar (necesitaria adaptarse a webhooks en vez
   de polling, que es mas trabajo).
2. **Reciba `TELEGRAM_TOKEN` como variable de entorno/secreto de la
   plataforma**, nunca escrito en el codigo ni copiado dentro de una
   imagen o build publico.
3. **Se reinicie solo si el proceso se cae** (crash, reinicio del
   servidor, etc.), para no perder puntos si el auxiliar prueba el bot
   y resulta que se habia caido.

### Opcion recomendada: Docker (funciona igual en cualquier nube)

Ya dejamos un `Dockerfile` y un `.dockerignore` en esta misma carpeta.
Cualquier nube que acepte contenedores (AWS, GCP, Azure, Railway,
Render, Fly.io, un VPS con Docker instalado, etc.) puede correr esta
imagen sin cambiarle nada:

```bash
docker build -t sa-p7-bot-ia1 .
docker run -d --restart unless-stopped \
  -e TELEGRAM_TOKEN=su_token_real \
  --name bot-ia1-tarea3 \
  sa-p7-bot-ia1
```

- `--restart unless-stopped` hace que Docker reinicie el contenedor solo
  si se cae o si el servidor se reinicia.
- El token se pasa con `-e`, nunca queda dentro de la imagen.
- Quien vaya a desplegar solo necesita adaptar este mismo comando (o el
  Dockerfile) a la interfaz de la nube que elijan: por ejemplo, en la
  mayoria de plataformas esto se traduce en "subir la imagen" o
  "conectar el repo" + configurar `TELEGRAM_TOKEN` en su seccion de
  variables de entorno/secrets, sin tocar el codigo del bot.

### Checklist antes de dar por hecho el despliegue

- [ ] El proceso queda corriendo de forma **continua**, no solo al
      momento de desplegarlo.
- [ ] `TELEGRAM_TOKEN` esta configurado como variable de entorno en la
      plataforma elegida (no en el codigo, no en un archivo subido a
      GitHub).
- [ ] Probaron `/hola` y un par de comandos mas contra el bot ya
      desplegado (no solo en local).
- [ ] Confirmaron que sigue respondiendo despues de un rato (para
      descartar que la plataforma lo "duerma" por inactividad).
- [ ] Actualizaron la seccion 5 del `README.md` con que nube usaron y
      los pasos exactos que siguieron, para que quede documentado.

## 6. Recordatorios importantes de la rubrica

- Si el bot no esta disponible o no responde durante el fin de semana de
  calificacion, la tarea vale 0 sin importar que tan bien este el
  codigo - por eso el checklist de arriba importa tanto.
- Si el `TELEGRAM_TOKEN` queda expuesto en GitHub (en el codigo o en un
  commit), hay un descuento del 30%. Si accidentalmente lo suben,
  avisen al grupo para regenerarlo de inmediato en BotFather
  (`/mybots` -> el bot -> *API Token* -> *Revoke current token*).
- Todo el codigo de esta tarea debe quedar dentro de la carpeta
  `Tarea#3` de este mismo repositorio (el mismo usado para la Tarea 2).
