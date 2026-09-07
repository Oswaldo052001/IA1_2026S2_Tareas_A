# Imagen base para desplegar el bot en cualquier nube que acepte
# contenedores (AWS, GCP, Azure, Railway, Render, Fly.io, un VPS con
# Docker, etc.). No incluye el token: se inyecta como variable de
# entorno al correr el contenedor (ver GUIA_EQUIPO.md, seccion 5).

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

# TELEGRAM_TOKEN se define en tiempo de ejecucion:
#   docker run -e TELEGRAM_TOKEN=xxxx ...
# o en la seccion de variables de entorno/secrets de la nube elegida.

CMD ["python", "bot.py"]
