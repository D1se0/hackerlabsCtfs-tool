#!/bin/bash

# Verificar si el script se está ejecutando como root
if [ "$(id -u)" -ne "0" ]; then
    echo "Este script debe ejecutarse como root."
    exit 1
fi

# Actualizar la lista de paquetes
echo "Actualizando la lista de paquetes..."
apt-get update

# Instalar pip3 si no está instalado
if ! command -v pip3 &> /dev/null; then
    echo "pip3 no está instalado. Instalando pip3..."
    apt-get install -y python3-pip
fi

# Instalar las dependencias necesarias
echo "Instalando dependencias..."
pip3 install -r requirements.txt

# Crear un enlace simbólico en /usr/bin/
if [ -f "hackerlabsCtfs.py" ]; then
    echo "Creando enlace simbólico en /usr/bin/"
    ln -sf "$(realpath hackerlabsCtfs.py)" /usr/bin/hackerlabsCtfs
else
    echo "El archivo hackerlabsCtfs.py no se encuentra en el directorio."
    exit 1
fi

# Ejecutar el comando para mostrar la ayuda
echo "Ejecutando 'hackerlabsCtfs -h' para mostrar la ayuda..."
hackerlabsCtfs -h

# Mensaje de finalización
echo "La instalación se completó exitosamente."
