# Usar una imagen base oficial de Python 3.11.4
FROM python:3.11.4-slim

# Instalar las dependencias del sistema necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    curl \
    apt-transport-https \
    gnupg2 \
    unixodbc-dev \
    ca-certificates \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Instalar el controlador ODBC 17 para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Desactivar el buffering de Python
ENV PYTHONUNBUFFERED=1

# Crear un enlace simbólico de 'python' a 'python3'
RUN ln -s /usr/local/bin/python3 /usr/bin/python

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Crear un archivo cron job que ejecute el script una vez al día
RUN echo "0 0 * * * python /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/mycron

# Dar permisos de ejecución al archivo cron
RUN chmod 0644 /etc/cron.d/mycron

# Aplicar el cron job
RUN crontab /etc/cron.d/mycron

# Crear un archivo de log para el cron job
RUN touch /var/log/cron.log

# Comando para ejecutar cron y mantener el contenedor en ejecución
CMD ["sh", "-c", "cron && tail -f /var/log/cron.log"]
