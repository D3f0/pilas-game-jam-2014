"""
Genera listado HTML de actores
"""

import pilas
import inspect
import re
import os

__all__ = ['listado_actores']

imagen_re = re.compile(r'[\w\/]+\.png')


def es_nombre_clase(nombre):
    if nombre.startswith('_'):
        return False
    if nombre[0] == nombre[0].upper():
        return True
    else:
        return False


def scaar_nombre_imagen_de_codigo(clase):
    codigo = inspect.getsource(clase.__init__)

    match = imagen_re.search(codigo)

    if match:
        imagen = match.group()
        ruta = os.path.dirname(inspect.getfile(clase))
        ruta = os.path.join(ruta, '../data', imagen)

        with open(ruta, "rb") as f:
            data = f.read()
            return data.encode("base64")


def nombre_actores(no_incluir=None):
    if no_incluir:
        no_incluir = map(lambda x: x.lower(), no_incluir)
    else:
        # Algunos que no nos interesan
        no_incluir = ['mapa', 'torreta', 'ejes', 'boton', 'actor', 'menu', 'pausa']

    actor_imagen = {}
    nombre_clases = [nombre for nombre in dir(pilas.actores)
                     if es_nombre_clase(nombre) and nombre.lower() not in no_incluir]
    for nombre in nombre_clases:
        clase = getattr(pilas.actores, nombre)
        imagen = scaar_nombre_imagen_de_codigo(clase)
        if imagen:
            actor_imagen[nombre] = imagen
    return actor_imagen


def listado_actores(no_incluir=None):
    html = ''
    for nombre, ruta in nombre_actores(no_incluir=no_incluir).iteritems():
        html += '<h1>{nombre}</h1><img src="data:image/png;base64,{ruta}"></br>'.format(
            nombre=nombre,
            ruta=ruta)
    return html


if __name__ == "__main__":
    print(listado_actores())
