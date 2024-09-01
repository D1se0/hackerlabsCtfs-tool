#!/bin/python3
# Autor: d1se0

import argparse
import random
import requests
from bs4 import BeautifulSoup
import os
from colorama import init, Fore, Style

# Inicializar colores
init(autoreset=True)

# Definición de colores
COLOR_AZUL = Fore.BLUE
COLOR_VERDE = Fore.GREEN
COLOR_NARANJA = Fore.YELLOW
COLOR_ROJO = Fore.RED
COLOR_BLANCO = Fore.WHITE
COLOR_RESET = Style.RESET_ALL
COLOR_VERDE_HACKER = Fore.GREEN
COLOR_VERDE_OSC = Fore.LIGHTGREEN_EX
COLOR_CYAN_SECCION = Fore.CYAN
COLOR_AMARILLO_IMPORTANTE = Fore.YELLOW
COLOR_VERDE_EXITO = Fore.LIGHTGREEN_EX

# Archivo para almacenar máquinas completadas
ARCHIVO_MAQUINAS_COMPLETADAS = "hackers_hechas.txt"
URL_BASE = 'https://d1se0.github.io/hackerlabs/'
URL_ENLACES_DESCARGA = "https://raw.githubusercontent.com/D1se0/hackerlabsCtfs-tool/main/enlaces_descarga.txt"

# Banners personalizados con tonalidades verdes
BANNERS_PERSONALIZADOS = [
    '''
    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ ██╗      █████╗ ██████╗ ███████╗     
    ██║ ██╔╝██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝    
    █████╔╝ ███████║██║     █████╔╝ █████╗  ██████╔╝██║     ███████║██████╔╝███████╗    
    ██╔═██╗ ██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗██║     ██╔══██║██╔══██╗╚════██║    
    ██║  ██╗██║  ██║╚██████╗██║  ██╗███████╗██║  ██║███████╗██║  ██║██████╔╝███████║    
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝ 
          by @d1se0
	    v2.0
    ''',
    f'    Visita nuestra web para más recursos: {URL_BASE} \n',
    f'    ¡Aprende más en https://d1se0.github.io/hackerlabs/guia_del_hacking_page/guia_del_hacking.html! \n'
]

# Niveles de dificultad
NIVELES_DIFICULTAD = ['Muy Facil', 'Facil', 'Medio', 'Dificil']

# Función para desactivar los colores
def desactivar_colores():
    global COLOR_AZUL, COLOR_VERDE, COLOR_NARANJA, COLOR_ROJO, COLOR_BLANCO, COLOR_RESET, COLOR_CYAN_SECCION, COLOR_AMARILLO_IMPORTANTE, COLOR_VERDE_EXITO
    COLOR_AZUL = COLOR_VERDE = COLOR_NARANJA = COLOR_ROJO = COLOR_BLANCO = COLOR_RESET = COLOR_CYAN_SECCION = COLOR_AMARILLO_IMPORTANTE = COLOR_VERDE_EXITO = ''

# Leer el archivo de máquinas completadas
def leer_maquinas_completadas(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        return set()
    with open(nombre_archivo, "r") as file:
        return set(line.strip().lower() for line in file)

# Escribir una máquina como completada
def escribir_maquina_completada(nombre_archivo, nombre_maquina):
    with open(nombre_archivo, "a") as file:
        file.write(nombre_maquina.lower() + "\n")

# Leer enlaces de descarga desde una URL
def leer_enlaces_desde_url(url):
    enlaces = {}
    try:
        response = requests.get(url)
        response.raise_for_status()  # Esto lanzará un error si la respuesta no es 200
        contenido = response.text
        for linea in contenido.splitlines():
            if '=' in linea:
                nombre, enlace = map(str.strip, linea.split('=', 1))
                enlaces[nombre.lower()] = enlace
    except requests.exceptions.RequestException as e:
        print(f"{COLOR_ROJO}[x] Error al obtener los enlaces desde la URL: {e}{COLOR_RESET}")
    return enlaces

# Obtener datos de la web
def obtener_maquinas_disponibles():
    response = requests.get(URL_BASE)
    if response.status_code != 200:
        print(f"{COLOR_ROJO}[x] Error al acceder a la página: {response.status_code}{COLOR_RESET}")
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# Extraer los nombres de las máquinas de los botones
def extraer_nombres_maquinas(soup):
    botones = soup.find_all('button', {'data-machine': True})
    nombres = [boton['data-machine'].strip().lower() for boton in botones]
    return nombres

# Procesar la lista de máquinas desde el HTML
def procesar_maquinas(soup, enlaces_descarga):
    lista_maquinas = []
    items = soup.find_all("div", class_="item")
    
    for item in items:
        # Extraer el nombre de la máquina
        nombre = item.find('span', class_='item-title').get_text(strip=True).lower() if item.find('span', class_='item-title') else 'N/A'
        
        # Extraer la dificultad desde las clases del div
        clases = item.get('class', [])
        dificultad = next((clase for clase in clases if clase in ['muy-facil', 'facil', 'medio', 'dificil']), 'Desconocida')
        dificultad = dificultad.replace('-', ' ').title()  # Ajustar el formato
        
        # Extraer el creador desde el atributo 'data-author'
        creador = item.get('data-author', 'N/A').lower()
        
        # Extraer el tamaño
        tamano = item.find('span', class_='size').get_text(strip=True) if item.find('span', class_='size') else 'N/A'
        
        # Obtener el enlace de descarga desde el diccionario, basado en nombres extraídos
        enlace_descarga = enlaces_descarga.get(nombre, 'N/A')
        
        lista_maquinas.append((nombre, dificultad, enlace_descarga, tamano, creador))
    return lista_maquinas

# Mostrar banner de bienvenida
def mostrar_banner():
    for banner in BANNERS_PERSONALIZADOS:
        print(f'{COLOR_VERDE_HACKER}{banner}{COLOR_RESET}')

# Mostrar información detallada de una máquina con color para la dificultad y marcar como "Hecha" si ya fue completada
def mostrar_info_maquina(maquina, maquinas_completadas):
    dificultad = maquina[1].title()
    if dificultad == 'Muy Facil':
        color_dificultad = COLOR_AZUL
    elif dificultad == 'Facil':
        color_dificultad = COLOR_VERDE
    elif dificultad == 'Medio':
        color_dificultad = COLOR_NARANJA
    elif dificultad == 'Dificil':
        color_dificultad = COLOR_ROJO
    else:
        color_dificultad = COLOR_BLANCO  # Fallback color if difficulty is not recognized

    completada = "✔ Hecha" if maquina[0] in maquinas_completadas else ""
    
    print(f"{COLOR_CYAN_SECCION}Nombre:{COLOR_RESET} {maquina[0].title()} {COLOR_VERDE_OSC}{completada}{COLOR_RESET}")
    print(f"{color_dificultad}Dificultad:{COLOR_RESET} {dificultad}")
    print(f"{COLOR_BLANCO}Tamaño de descarga:{COLOR_RESET} {maquina[3]}")
    print(f"{COLOR_BLANCO}Link de descarga:{COLOR_RESET} {maquina[2]}")
    print(f"{COLOR_CYAN_SECCION}Creador:{COLOR_RESET} {maquina[4].title()}")
    print()

# Listar máquinas disponibles filtradas por dificultad y creador, marcando las completadas
def listar_maquinas_filtradas(maquinas, maquinas_completadas, dificultad=None, creador=None):
    if dificultad:
        dificultad_filtrada = dificultad.title()  # Asegurarse de que la dificultad esté en formato de título
        if dificultad_filtrada == 'Muy Facil':
            color_dificultad = COLOR_AZUL
        elif dificultad_filtrada == 'Facil':
            color_dificultad = COLOR_VERDE
        elif dificultad_filtrada == 'Medio':
            color_dificultad = COLOR_NARANJA
        elif dificultad_filtrada == 'Dificil':
            color_dificultad = COLOR_ROJO
        else:
            color_dificultad = COLOR_BLANCO  # Fallback color if difficulty is not recognized
        
        maquinas_filtradas = [maquina for maquina in maquinas if maquina[1] == dificultad_filtrada]
    elif creador:
        creador_filtrado = creador.strip().lower()
        maquinas_filtradas = [maquina for maquina in maquinas if maquina[4].strip() == creador_filtrado]
    else:
        maquinas_filtradas = maquinas

    total_maquinas = len(maquinas_filtradas)
    if total_maquinas == 0:
        print(f"{COLOR_ROJO}[x] No se encontraron máquinas con los filtros especificados.{COLOR_RESET}")
        return

    for maquina in maquinas_filtradas:
        mostrar_info_maquina(maquina, maquinas_completadas)
    
    print(f"{COLOR_VERDE}Total de máquinas mostradas: {total_maquinas}{COLOR_RESET}")

# Mostrar una máquina aleatoria que no esté completada
def mostrar_maquina_aleatoria(maquinas, maquinas_completadas, dificultad=None, creador=None):
    maquinas_filtradas = [maquina for maquina in maquinas if (not dificultad or maquina[1] == dificultad) and (not creador or maquina[4] == creador.lower())]
    maquinas_filtradas = [maquina for maquina in maquinas_filtradas if maquina[0] not in maquinas_completadas]  # Excluir completadas
    
    if maquinas_filtradas:
        maquina_aleatoria = random.choice(maquinas_filtradas)
        mostrar_info_maquina(maquina_aleatoria, maquinas_completadas)
    else:
        print(f"{COLOR_ROJO}[x] No se encontraron máquinas con los filtros especificados o todas las máquinas están completadas.{COLOR_RESET}")

# Manejo de argumentos
def manejar_argumentos(args, maquinas, maquinas_completadas):
    if args.finish:
        nombre_maquina = args.finish.lower()
        if nombre_maquina in [maquina[0] for maquina in maquinas]:
            escribir_maquina_completada(ARCHIVO_MAQUINAS_COMPLETADAS, nombre_maquina)
            print(f"{COLOR_VERDE_EXITO}[✓] Máquina '{nombre_maquina}' marcada como completada.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}[x] Máquina '{nombre_maquina}' no encontrada entre las disponibles.{COLOR_RESET}")
        return

    if args.list_machines_finish:
        print(f"{COLOR_VERDE}Máquinas completadas:{COLOR_RESET}")
        for nombre in sorted(maquinas_completadas):
            print(f" - {nombre.title()}")
        return

    if args.name:
        nombre_maquina = args.name.lower()
        maquina = next((maquina for maquina in maquinas if maquina[0] == nombre_maquina), None)
        if maquina:
            mostrar_info_maquina(maquina, maquinas_completadas)
        else:
            print(f"{COLOR_ROJO}[x] No se encontró ninguna máquina con el nombre '{args.name}'.{COLOR_RESET}")
        return

    if args.aleatoria:
        dificultad_filtrada = args.dificultad.title() if args.dificultad else None
        creador_filtrado = args.creador.lower() if args.creador else None
        mostrar_maquina_aleatoria(maquinas, maquinas_completadas, dificultad=dificultad_filtrada, creador=creador_filtrado)
        return

    listar_maquinas_filtradas(maquinas, maquinas_completadas, args.dificultad, args.creador)

# Programa principal
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script para filtrar y listar máquinas desde la web de hackerlabs.es")
    parser.add_argument('-d', '--dificultad', choices=[nivel.lower() for nivel in NIVELES_DIFICULTAD], help='Filtra máquinas por dificultad.')
    parser.add_argument('-c', '--creador', type=str, help='Filtra máquinas por creador.')
    parser.add_argument('-a', '--aleatoria', action='store_true', help='Muestra una máquina aleatoria según los filtros dados.')
    parser.add_argument('-f', '--finish', type=str, help='Marca una máquina como finalizada.')
    parser.add_argument('-l', '--list-machines-finish', action='store_true', help='Lista las máquinas marcadas como finalizadas.')
    parser.add_argument('-n', '--name', type=str, help='Muestra la máquina con el nombre especificado.')
    parser.add_argument('--no-colores', action='store_true', help='Desactiva el uso de colores en la salida.')

    args = parser.parse_args()

    if args.no_colores:
        desactivar_colores()

    mostrar_banner()
    maquinas_completadas = leer_maquinas_completadas(ARCHIVO_MAQUINAS_COMPLETADAS)
    
    # Leer enlaces desde URL
    enlaces_descarga = leer_enlaces_desde_url(URL_ENLACES_DESCARGA)
    
    # Obtener HTML y enlaces
    soup = obtener_maquinas_disponibles()
    if soup:
        maquinas = procesar_maquinas(soup, enlaces_descarga)
        manejar_argumentos(args, maquinas, maquinas_completadas)
    else:
        print(f"{COLOR_ROJO}[x] No se pudieron obtener las máquinas disponibles desde la web.{COLOR_RESET}")
