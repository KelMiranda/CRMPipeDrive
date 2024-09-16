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
    # Dependencias para Node.js
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar el controlador ODBC 17 para SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalar Node.js y npm
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el archivo package.json y package-lock.json para instalar dependencias de Node.js (incluyendo Tailwind)
COPY package*.json ./

# Instalar las dependencias de Node.js (Tailwind CSS y otras necesarias)
RUN npm install

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Compilar Tailwind CSS (compilación de tu archivo de entrada)
RUN npm run build

# Exponer el puerto en el que correrá la aplicación Flask
EXPOSE 5000

# Comando para ejecutar tu aplicación Flask
CMD ["python", "app.py"]
