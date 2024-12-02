# ICI224 
# Tarea 02: Consultar Fabricantes de tarjetas de red
# Profesor: Omar Salinas 

# Integrantes: 
# Ricardo Silva, ricardo.silvap@alumnos.uv.cl
# Joaquin Martinez, joaquin.martinez@alumnos.uv.cl
# Alonso Vera, alonso.vera@alumnos.uv.cl


import getopt
import sys
import time
from json import loads
from http import client


RESPUESTA_FABRICANTE = "MAC address: {mac}\nFabricante: {vendor}\nTiempo de respuesta: {time}ms\n"
RESPUESTA_NO_ENCONTRADO = "MAC address: {mac}\nFabricante: Not found\nTiempo de respuesta: {time}ms\n"
AYUDA = """Uso: python OUILookup.py --mac <MAC> | --arp | [--help]
--mac: MAC a consultar. Ejemplo: aa:bb:cc:00:00:00.
--arp: Muestra los fabricantes de los hosts disponibles en la tabla ARP.
--help: Muestra este mensaje de ayuda y termina."""

#Extrae el proveedor a través de la API utilizando la dirección MAC
def consultar_fabricante_mac(mac: str) -> dict:
    inicio = time.time()  # Medir el tiempo de inicio
    conn = client.HTTPSConnection("api.maclookup.app")
    conn.request("GET", "/v2/macs/" + mac)
    respuesta = conn.getresponse()
    fin = time.time()  # Tiempo de fin
    tiempo_transcurrido = round((fin - inicio) * 1000, 3)  # De lo que se encarga esta sección es de calcular el tiempo en milisegundos
    
    if respuesta.status == 200:
        data = loads(respuesta.read())
        fabricante = data.get("company")  # Extraer el nombre del proveedor de la información recibida
        # Introducimos la clave "company" para verificar si existe. de lo contrario, deberá retornar "Not Found"
        if not fabricante:
            return {"fabricante": "Not found", "tiempo(ms)": tiempo_transcurrido}
        return {"fabricante": fabricante, "tiempo(ms)": tiempo_transcurrido}
    else:
        return {"fabricante": "Not found", "tiempo(ms)": tiempo_transcurrido}

# Función principal para manejar los parámetros de entrada
def main(argv):
    # mostrar ayuda si no se entrega ningún argumento 
    if len(argv) == 0:
        print(AYUDA)
        sys.exit(2)

    try:
        opts, args = getopt.getopt(argv, "", ["mac=", "arp", "help"])
    except getopt.GetoptError:
        print(AYUDA)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--mac":
            # Consultar la API siempre
            resultado_api = consultar_fabricante_mac(arg)
            if resultado_api["fabricante"] != "Not found":
                print(RESPUESTA_FABRICANTE.format(mac=arg, vendor=resultado_api["fabricante"], time=resultado_api["tiempo(ms)"]))
            else:
                print(RESPUESTA_NO_ENCONTRADO.format(mac=arg, time=resultado_api["tiempo(ms)"]))
        elif opt == "--arp":
            print("La opción --arp no está disponible, siempre se consulta la API.")
        elif opt == "--help":
            # Mostrar la ayuda
            print(AYUDA)
        else:
            print("Opción no válida. Use --help para ver las opciones.")
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])   
    ###                   
  ####
############
##########################
################