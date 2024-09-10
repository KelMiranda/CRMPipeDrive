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
    && rm -rf /var/lib/apt/lists/*

# Instalar el controlador ODBC 17 para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Exponer el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando para ejecutar tu aplicación Flask
CMD ["python", "app.py"]