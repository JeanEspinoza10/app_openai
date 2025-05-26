# Usa una imagen base oficial de Python
FROM python:3.12-slim

RUN apt-get update && apt-get install -y git libgl1 && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app
RUN git clone --depth 1 https://github.com/ultralytics/yolov5.git

# Copia los archivos de dependencias y del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu aplicación
COPY ./app/ .

# Comando por defecto para ejecutar la aplicación
CMD ["python", "main.py"]