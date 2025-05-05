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

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias Python (incluyendo dnspython compatible)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY . .

# Comando por defecto para ejecutar el servidor Flask con socketio + eventlet
CMD ["python", "run.py"]
