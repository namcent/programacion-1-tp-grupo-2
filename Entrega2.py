"""
-----------------------------------------------------------------------------------------------
Título: DESARROLLO PYTHON POR EQUIPO - VERSIÓN 2.0 - ENTREGA 2
Fecha: 07/07/2025
Autor: Equipo 02

Descripción: Una biblioteca de una organización educativa necesita el desarrollo de una
aplicación para informatizar la gestión de préstamos de libros a sus alumnos. Cada libro tiene
un costo de garantía de préstamo diario.

Pendientes:
-----------------------------------------------------------------------------------------------
"""

# ----------------------------------------------------------------------------------------------
# MÓDULOS
# ----------------------------------------------------------------------------------------------
from datetime import datetime
import json
import re

ALUMNOS_ARCHIVO = "alumnos.json"
LIBROS_ARCHIVO = "libros.json"
PRESTAMOS_ARCHIVO = "prestamos.json"


# ----------------------------------------------------------------------------------------------
# FUNCIONES
# ----------------------------------------------------------------------------------------------
def esEmailValido(_dato):
    """
    Valida si una cadena cumple el formato de email.

    Parámetros:
        _dato (str): Cadena a validar como email.

    Retorno:
        bool: True si cumple, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        pat = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pat, _dato) is not None
    except Exception as e:
        print(f"Error inesperado en la validación de email: {e}")
        return False

def esNumeroValido(_dato):
    """
    Valida si una cadena es un número entero.

    Parámetros:
        _dato (str): Cadena a validar como número.

    Retorno:
        bool: True si puede convertirse a entero, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        int(_dato)
        return True
    except (ValueError):
        return False
    except Exception as e:
        print(f"Error inesperado en la validación de número: {e}")
        return False

def esIdValido(_dato):
    """
    Valida que una cadena empiece con una letra (mayúscula o minúscula) seguida de al menos un dígito.

    Parámetros:
        _dato (str): Cadena a validar como ID.

    Retorno:
        bool: True si cumple el patrón, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        patron = r"^[A-Za-z]\d+$"
        return re.match(patron, _dato) is not None
    except Exception as e:
        print(f"Error inesperado en la validación de ID: {e}")
        return False

def esIdPrestamoValido(_dato):
    """
    Valida que una cadena tenga formato 'YYYY.MM.DD HH:MM:SS'.

    Parámetros:
        _dato (str): Cadena a validar como ID de préstamo.

    Retorno:
        bool: True si coincide con el patrón de fecha y hora, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False

        patron = (
            r"^\d{4}\."                       # Año
            r"(0[1-9]|1[0-2])\."              # Mes
            r"(0[1-9]|[12]\d|3[01]) "         # Día
            r"([01]\d|2[0-3]):"               # Hora
            r"[0-5]\d:"                       # Minuto
            r"[0-5]\d$"                       # Segundo
        )
        return re.match(patron, _dato) is not None
    except Exception as e:
        print(f"Error inesperado en la validación de ID de préstamo: {e}")
        return False

def esDireccionValida(_dato):
    """
    Valida que una dirección solo contenga letras, números, puntos y espacios.

    Parámetros:
        _dato (str): Cadena a validar como dirección.

    Retorno:
        bool: True si cumple, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\.]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñ0-9\.]+)*$"
        return re.match(patron, _dato) is not None
    except Exception as e:
        print(f"Error inesperado en la validación de dirección: {e}")
        return False

def sonAutoresValidos(_dato):
    """
    Valida que una cadena contenga letras (hasta tres) separados por comas.

    Parámetros:
        _dato (str): Cadena a validar.

    Retorno:
        bool: True si hay entre 1 y 3 cadenas de letras válidas separadas por comas, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        patrón = (
            r'^[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+'
            r'(?:\s+[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+)*'
            r'(?:\s*,\s*[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+'
            r'(?:\s+[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+)*)*$'
        )
        return re.match(patrón, _dato) is not None
    except Exception as e:
        print(f"Error inesperado en la validación de autores: {e}")
        return False

def esStringValido(_dato):
    """
    Valida que una cadena solo contenga letras (incluye tildes y ñ) y espacios.

    Parámetros:
        _dato (str): Cadena a validar.

    Retorno:
        bool: True si cumple, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ]+(?: [A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$"
        return re.match(patron, _dato) is not None
    except Exception as e:
        print(f"Error inesperado en la validación de string: {e}")
        return False

def validarDato(_dato, _tipo, _validacion):
    """
    Pide al usuario un dato hasta que pase la validación indicada.

    Parámetros:
        _dato (str): Valor inicial ingresado.
        _tipo (str): Nombre para el mensaje de error (p.ej. "email", "id").
        _validacion (str): Tipo de validación ("email", "numero", "id", "idPrestamo", "direccion", "autores" o por defecto "string").

    Retorno:
        str: Valor validado y formateado (strip/upper) que cumple la validación.
    """
    try:
        if _validacion == "email":
            validador = esEmailValido
        elif _validacion == "numero":
            validador = esNumeroValido
        elif _validacion == "id":
            validador = esIdValido
        elif _validacion == "idPrestamo":
            validador = esIdPrestamoValido
        elif _validacion == "direccion":
            validador = esDireccionValida
        elif _validacion == "autores":
            validador = sonAutoresValidos
        else:
            validador = esStringValido

        dato = _dato.strip()

        while not validador(dato):
            dato = input(f"Error. Por favor ingrese un/a/os {_tipo} válido/a/s: ").strip()
        return dato
    except Exception as e:
        print(f"Error inesperado en la validación del dato: {e}")
        return ""

def cargarArchivo(_direccion):
    """
    Carga un archivo JSON y devuelve su contenido como diccionario.

    Parámetros:
        _direccion (str): Ruta del archivo JSON.

    Retorno:
        dict: Contenido del JSON.
    """
    try:
        archivo = open(_direccion, mode="r", encoding="utf-8")
        diccionario = json.load(archivo)
        archivo.close()
        return diccionario
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)

def escribirArchivo(_direccion, _diccionario):
    """
    Escribe un diccionario en un archivo JSON.

    Parámetros:
        _direccion (str): Ruta del archivo JSON.
        _diccionario (dict): Diccionario a escribir.

    Retorno:
        None
    """
    try:
        archivo = open(_direccion, mode="w", encoding="utf-8")
        json.dump(_diccionario, archivo, ensure_ascii=False, indent=4)
        archivo.close()
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)

def pedirYValidarId(_diccionario, _tipo, _validarExistente, _validacion):
    """
    Solicita un ID y valida su existencia o inexistencia según lo que se ingrese como parámetro.

    Parámetros:
        _diccionario (dict): Diccionario donde buscar la existencia o inexistencia de un valor.
        _tipo (str): Nombre para el mensaje de error (p.ej. "alumno", "libro").
        _validarExistente (bool): True si el ID debe existir y estar activo, False si debe ser nuevo.
        _validacion (str): Tipo de validación para el ID ("id" o "idPrestamo").

    Retorno:
        str/None: ID validado (en mayúsculas) o None si el usuario ingresa '0' para volver.
    """
    try:
        id = validarDato(input(f"Ingrese el ID del {_tipo}: "), "id", _validacion).strip().upper()
            
        if _validarExistente:
            while id not in _diccionario or not _diccionario[id]["activo"]:
                print(f"Error: el ID del {_tipo} no existe o está inactivo.")
                entrada = input(f"Por favor, ingrese el ID del {_tipo} (0 para volver): ").strip().upper()
                if entrada == "0":
                    return
                else:
                    id = validarDato(entrada, "id", _validacion).upper()

            return id
        else:
            while id in _diccionario:
                print(f"Error: el ID del {_tipo} que ingresó ya existe.")
                entrada = input(f"Por favor ingrese un nuevo ID del {_tipo} (0 para volver): ").strip().upper()
                if entrada == "0":
                    return
                else:
                    id = validarDato(entrada, "id", _validacion).upper()

            return id
    except Exception as e:
        print(f"Error inesperado en el pedido y validación de ID: {e}")
        return ""


def ingresarAlumno():
    """
    Registra un nuevo alumno. Solicita sus datos, lo registra en el archivo JSON y confirma su 
    creación.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        idAlumno = pedirYValidarId(alumnos, "alumno", False, "id")
        if idAlumno is None:
            return

        nombre = validarDato(input("Ingresar el nombre: "), "nombre", "string")
        apellido = validarDato(input("Ingresar el apellido: "), "apellido", "string")
        direccion = validarDato(input("Ingresar la direccion: "), "direccion", "direccion")
        email = validarDato(input("Ingresar el email: "), "email", "email")
        celular = int(validarDato(input("Ingresar el teléfono celular: "), "celular", "numero"))
        fijo = int(validarDato(input("Ingresar el teléfono fijo: "), "fijo", "numero"))

        alumnos[idAlumno] = {
            "activo": True,
            "nombre": nombre,
            "apellido": apellido,
            "direccion": direccion,
            "email": email,
            "telefono": {
                "celular": celular,
                "fijo": fijo,
            },
            "infracciones": 0,
        }
        escribirArchivo(ALUMNOS_ARCHIVO, alumnos)
        print(f"Alumno {idAlumno} registrado correctamente.")
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al ingresar alumno: {e}")


def modificarAlumno():
    """
    Modifica los datos de un alumno existente. Permite cambiar uno de los campos de un alumno existente 
    identificado por ID.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        idAlumno = pedirYValidarId(alumnos, "alumno", True, "id")
        if idAlumno is None:
            return

        print("\nCampos disponibles para modificar: nombre, apellido, email, direccion, celular, fijo")
        campo = input("Ingresá el campo a modificar: ").strip().lower()

        while campo not in alumnos[idAlumno] and campo not in alumnos[idAlumno]["telefono"]:
            print("Error: campo inválido")
            entradaCampo = input("Por favor ingrese el campo a modificar o 0 para volver: ").strip().lower()
            if entradaCampo == "0":
                return
            campo = entradaCampo

        if campo == "email":
            validacion = "email"
        elif campo in ("celular", "fijo"):
            validacion = "numero"
        elif campo == "direccion":
            validacion = "direccion"
        else:
            validacion = "string"
    
        nuevoValor = validarDato(input(f"Nuevo valor para {campo}: "), campo, validacion)

        if campo in ("celular", "fijo"):
            alumnos[idAlumno]["telefono"][campo] = int(nuevoValor)
        else:
            alumnos[idAlumno][campo] = nuevoValor

        escribirArchivo(ALUMNOS_ARCHIVO, alumnos)
        print(f"Modificación del campo {campo} exitosa")

    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al modificar alumno: {e}")


def inactivarAlumno():
    """
    Marca como inactivo a un alumno existente (baja lógica) identificado por ID.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        idAlumno = pedirYValidarId(alumnos, "alumno", True, "id")
        if idAlumno is None:
            return

        alumnos[idAlumno]["activo"] = False
        escribirArchivo(ALUMNOS_ARCHIVO, alumnos)
        print(f"Alumno {idAlumno} inactivado")

    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al inactivar alumno: {e}")


def listarAlumnos():
    """
    Imprime por consola el listado de alumnos activos y sus datos.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)

        if not alumnos:
            print("No hay alumnos registrados.")

        print("\nLISTADO DE ALUMNOS ACTIVOS")
        print("-" * 50)

        alumnosActivos = 0

        for idAlumno, datos in alumnos.items():
            if datos["activo"]:
                alumnosActivos += 1

                print(f"ID: {idAlumno}")
                print(f"NOMBRE: {datos['nombre']} {datos['apellido']}")
                print(f"DIRECCIÓN: {datos['direccion']}")
                print(f"EMAIL: {datos['email']}")
                print(
                    f"TELÉFONO: Cel: {datos['telefono']['celular']} | Fijo: {datos['telefono']['fijo']}"
                )
                print(f"ESTADO: {'Activo' if datos['activo'] else 'Inactivo'}")
                print(f"INFRACCIONES: {datos['infracciones']}")
                print("-" * 50)

        if alumnosActivos == 0:
            print("No hay alumnos activos registrados.")
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al listar alumnos: {e}")


def ingresarLibro():
    """
    Registra un nuevo libro. Solicita los datos del nuevo libro, lo registra en el JSON y confirma su creación.
    """
    try:
        libros = cargarArchivo(LIBROS_ARCHIVO)
        idLibro = pedirYValidarId(libros, "libro", False, "id")
        if idLibro is None:
            return

        titulo = validarDato(input("Ingresar el título: "), "título", "string")

        autores = validarDato(input("Autores (separados por coma, máx 3): ").strip(), "autores", "autores")
        autoresCortados = [
            parte.strip() for parte in autores.split(",") if parte.strip()
        ]
        autoresRellenados = (autoresCortados + ["", "", ""])[:3]
        dictAutores = {
            "autor1": autoresRellenados[0],
            "autor2": autoresRellenados[1],
            "autor3": autoresRellenados[2],
        }

        genero = validarDato(input("Ingresar el género: "), "género", "string")
        editorial = validarDato(input("Ingresar la editorial: "), "editorial", "string")
        costo = int(validarDato(input("Ingresar el costo de garantía en $: "), "costo", "numero"))

        libros[idLibro] = {
            "titulo": titulo,
            "autores": dictAutores,
            "activo": True,
            "genero": genero,
            "editorial": editorial,
            "costoGarantia": costo,
        }

        escribirArchivo(LIBROS_ARCHIVO, libros)
        print("Libro ingresado correctamente.")
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al ingresar libro: {e}")


def modificarLibro():
    """
    Modifica los datos de un libro existente. Permite cambiar uno de los campos de un libro existente 
    identificado por ID.
    """
    try:
        libros = cargarArchivo(LIBROS_ARCHIVO)
        idLibro = pedirYValidarId(libros, "libro", True, "id")
        if idLibro is None:
            return

        print("\nCampos disponibles para modificar: titulo, autores, genero, editorial, costo")
        campo = validarDato(input("Ingresá el campo a modificar: ").strip().lower(), "campo", "string")
        if campo == "costo":
            campo = "costoGarantia"

        while campo not in libros[idLibro]:
            print("Error: campo inválido")
            entradaCampo = validarDato(input("Por favor ingrese el campo a modificar o 0 para volver: ").strip().lower(), "campo", "string")
            if entradaCampo == "0":
                return
            campo = entradaCampo

        if campo == "autores":
            autores = validarDato(input("Nuevo valor para autores (separados por coma, máx 3): ").strip(), "autores", "autores")
            autoresCortados = [
                parte.strip() for parte in autores.split(",") if parte.strip()
            ]
            autoresRellenados = (autoresCortados + ["", "", ""])[:3]
            nuevoValor = {
                "autor1": autoresRellenados[0],
                "autor2": autoresRellenados[1],
                "autor3": autoresRellenados[2],
            }
        else:
            if campo == "costoGarantia":
                validacion = "numero"
            else:
                validacion = "string"

            nuevoValor = validarDato(input(f"Nuevo valor para {campo}: "), campo, validacion)

            if campo == "costoGarantia":
                nuevoValor = int(nuevoValor)

        libros[idLibro][campo] = nuevoValor

        escribirArchivo(LIBROS_ARCHIVO, libros)
        print(f"Modificación del campo {campo} exitosa")
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al modificar libro: {e}")


def inactivarLibro():
    """
    Marca como inactivo a un libro existente (baja lógica) identificado por ID.
    """
    try:
        libros = cargarArchivo(LIBROS_ARCHIVO)
        idLibro = pedirYValidarId(libros, "libro", True, "id")
        if idLibro is None:
            return

        libros[idLibro]["activo"] = False
        escribirArchivo(LIBROS_ARCHIVO, libros)
        print(f"Libro {idLibro} marcado como inactivo.")

    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al inactivar libro: {e}")


def listarLibros():
    """
    Imprime por consola el listado completo de libros y sus datos.
    """
    try:
        libros = cargarArchivo(LIBROS_ARCHIVO)
        if not libros:
            print("No hay libros registrados.")

        librosActivos = 0

        print("\nLISTADO DE LIBROS")
        print("-" * 50)

        for idLibro, datos in libros.items():
            if datos["activo"]:
                librosActivos += 1
                print(f"ID: {idLibro}")
                print(f"TÍTULO: {datos['titulo']}")
                print(
                    f"AUTORES: {datos['autores']['autor1']} , {datos['autores']['autor2']} , {datos['autores']['autor3']}"
                )
                print(f"GÉNERO: {datos['genero']}")
                print(f"COSTO: {datos['costoGarantia']}")
                print(f"ESTADO: {'Activo' if datos['activo'] else 'Inactivo'}")
                print("-" * 50)

        if librosActivos == 0:
            print("No hay libros activos registrados.")
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al listar libros: {e}")


def registrarPrestamo():
    """
    Registra un nuevo préstamo con ID automático de fecha/hora para alumno y libro válidos y lo 
    agrega al archivo préstamos.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        idAlumno = pedirYValidarId(alumnos, "alumno", True, "id")
        if idAlumno is None:
            return
        
        idLibro = pedirYValidarId(libros, "libro", True, "id")
        if idLibro is None:
            return

        idPrestamo = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        fechaInicio = datetime.now()

        prestamos[idPrestamo] = {
            "idPrestamo": idPrestamo,
            "idAlumno": idAlumno,
            "idLibro": idLibro,
            "cantidadDias": 0,
            "fechaInicio": fechaInicio.strftime("%Y-%m-%d"),
            "fechaFinalizacion": "",
            "estadoDevolucionCorrecto": False,
        }
        escribirArchivo(PRESTAMOS_ARCHIVO, prestamos)
        print(f"Préstamo con ID: {idPrestamo} registrado exitosamente.")
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al registrar préstamo: {e}")


def finalizarPrestamo():
    """
    Finaliza un préstamo, registra la devolución, calcula el monto y actualiza infracciones. 
    Guarda los datos actualizados en los archivos correspondientes.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        idPrestamo = pedirYValidarId(prestamos, "préstamo", True, "idPrestamo")
        if idPrestamo is None:
            return

        prestamo = prestamos[idPrestamo]

        fechaInicio = datetime.strptime(prestamo["fechaInicio"], "%Y-%m-%d")
        fechaFin = datetime.now()

        diasPrestamo = (fechaFin - fechaInicio).days
        if diasPrestamo == 0:
            diasPrestamo = 1

        idLibro = prestamo["idLibro"]

        costoDiario = libros[idLibro]["costoGarantia"]
        montoTotal = costoDiario * diasPrestamo

        prestamo["fechaFinalizacion"] = fechaFin.strftime("%Y-%m-%d")
        prestamo["cantidadDias"] = diasPrestamo

        devolucion = validarDato(input("¿La devolución es correcta? (s = sí / n = no): ").strip().lower(), "respuesta", "string")

        while devolucion not in ("s", "n"):
            print("Error. Ingrese 's' o 'n'.")
            devolucion = validarDato(input("¿La devolución es correcta? (s = sí / n = no): ").strip().lower(), "respuesta", "string")

        devolucionCorrecta = devolucion == "s"

        if not devolucionCorrecta:
            idAlumno = prestamo["idAlumno"]
            alumnos[idAlumno]["infracciones"] += 1
            escribirArchivo(ALUMNOS_ARCHIVO, alumnos)
            print("Se añadió 1 infracción al alumno.")

        escribirArchivo(ALUMNOS_ARCHIVO, alumnos)
        escribirArchivo(PRESTAMOS_ARCHIVO, prestamos)

        print(f"\nPréstamo finalizado correctamente.")
        print(f"Días prestados: {diasPrestamo}")
        print(f"Costo por día : {costoDiario}")
        print(f"Total a pagar : {montoTotal}\n")
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al finalizar préstamo: {e}")


def imprimirResumenMensual():
    """
    Solicita un año y mes e imprime por consola el listado de préstamos iniciados en ese periodo.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        anio = int(validarDato(input("Ingrese el año (formato AAAA): "),"año", "numero"))
        mes = int(validarDato(input("Ingrese el mes (1-12): "), "mes", "numero"))

        salida = []
        salida.append(f"Listado de reservas del mes {mes}/{anio}")
        salida.append(f"{'Fecha/Hora':<35}{'Alumno':<35}{'Libro':<35}")
        salida.append("-" * 105)

        for clave, prestamo in prestamos.items():
            fecha = prestamo["fechaInicio"]
            if fecha.startswith(f"{anio}-{str(mes).zfill(2)}"):
                fechaHora = clave
                idAlumno = prestamo["idAlumno"]
                nombreAlumno = alumnos.get(idAlumno, {}).get(
                    "nombre", f"Alumno {idAlumno}"
                )
                idLibro = prestamo["idLibro"]
                tituloLibro = libros.get(idLibro, {}).get("titulo", f"Libro {idLibro}")
                salida.append(f"{fechaHora:<35}{nombreAlumno:<35}{tituloLibro:<35}")

        print("\n".join(salida))
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al imprimir resumen mensual: {e}")


def imprimirResumenAnualPorLibroCantidad():
    """
    Solicita un año e imprime por consola cuántos préstamos tuvo cada libro mes a mes.
    """
    try:
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        anio = int(validarDato(input("Ingrese el año (formato AAAA): "),"año", "numero"))

        resumen = {idLibro: [0] * 12 for idLibro in libros.keys()}

        for prestamo in prestamos.values():
            fecha = prestamo["fechaInicio"]
            if fecha.startswith(str(anio)):
                mes = int(fecha[5:7])
                libro = prestamo["idLibro"]
                if libro in resumen:
                    resumen[libro][mes - 1] += 1

        resumenPorTitulo = {
            libros.get(idLibro, {}).get("titulo", f"Libro {idLibro}"): valores
            for idLibro, valores in resumen.items()
        }

        informe = formatearInformes(resumenPorTitulo, anio, "Resumen Anual de Reservas por Libro (Cantidades)")
        print(informe)
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al imprimir resumen anual de reservas por libro: {e}")


def imprimirResumenAnualPorLibroPesos():
    """
    Solicita un año e imprime por consola el resumen anual del dinero en garantía movido por libro.
    """
    try:
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)
        
        anio = int(validarDato(input("Ingrese el año (formato AAAA): "),"año", "numero"))

        resumen = {}

        for prestamo in prestamos.values():
            fecha = prestamo["fechaInicio"]
            if fecha.startswith(str(anio)):
                mes = int(fecha[5:7]) - 1
                idLibro = prestamo["idLibro"]
                nombreLibro = libros.get(idLibro, {}).get("titulo", f"Libro {idLibro}")
                costo = libros.get(idLibro, {}).get("costoGarantia", 0)

                if nombreLibro not in resumen:
                    resumen[nombreLibro] = [0] * 12
                resumen[nombreLibro][mes] += costo

        informe = formatearInformes(resumen, anio, "Resumen Anual de Reservas por Libro (Pesos)", _esDinero=True)
        print(informe)
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al imprimir resumen anual por libro: {e}")


def imprimirResumenAnualDevolucionesIncorrectas():
    """
    Solicita un año e imprime por consola el resumen anual de devoluciones incorrectas por mes.
    """
    try:
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)
        
        anio = int(validarDato(input("Ingrese el año (formato AAAA): "),"año", "numero"))

        meses = [
            "ENE",
            "FEB",
            "MAR",
            "ABR",
            "MAY",
            "JUN",
            "JUL",
            "AGO",
            "SEP",
            "OCT",
            "NOV",
            "DIC",
        ]

        incorrectasPorMes = []
        for mes in range(1, 13):
            count = 0
            for prestamo in prestamos.values():
                fecha = prestamo["fechaInicio"]
                if fecha.startswith(f"{anio}-{str(mes).zfill(2)}"):
                    if not prestamo.get("estadoDevolucionCorrecto", True):
                        count += 1
            incorrectasPorMes.append(count)

        anchoTotal = 160
        salida = []
        salida.append("-" * anchoTotal)
        salida.append(
            "Resumen anual de reservas con devolución incorrecta".center(anchoTotal)
        )
        salida.append("-" * anchoTotal)

        encabezado = "MESES".ljust(15)
        for m in meses:
            encabezado += f"{m}.{str(anio)[-2:]}".center(12)
        salida.append(encabezado)

        salida.append("-" * anchoTotal)

        fila = "Devol.Incorrect".ljust(15)
        for val in incorrectasPorMes:
            fila += f"{val}".center(12)
        salida.append(fila)

        salida.append("-" * anchoTotal)

        print("\n".join(salida))
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al imprimir resumen anual de devoluciones incorrectas: {e}")


def formatearInformes(_diccionario, _anio, _titulo, _esDinero=False):
    """
    Formatea un informe anual en forma de tabla con columnas mensuales.

    Parámetros:
        _diccionario (dict): Diccionario donde las claves son los nombres y los valores son listas con 12 números (uno por mes).
        _anio (int o str): Año del informe.
        _titulo (str): Título centrado que aparecerá en la parte superior del informe.
        _esDinero (bool): Si es True, los valores se muestran con signo '$' y dos decimales.

    Retorno:
        str: Cadena formateada con encabezados, filas alineadas y totales por mes.
    """
    try:
        _anio = int(_anio)
        anchoNombre = 50
        anchoMes = 10
        totalColumnas = anchoNombre + (12 * anchoMes)

        meses = [
            "ENE",
            "FEB",
            "MAR",
            "ABR",
            "MAY",
            "JUN",
            "JUL",
            "AGO",
            "SEP",
            "OCT",
            "NOV",
            "DIC",
        ]

        salida = []
        salida.append("-" * totalColumnas)
        salida.append(_titulo.center(totalColumnas))
        salida.append("-" * totalColumnas)

        encabezado = f"{'Libros':<{anchoNombre}}"
        for mes in meses:
            encabezado += f"{mes}.{_anio % 100:02d}".rjust(anchoMes)
        salida.append(encabezado)
        salida.append("-" * totalColumnas)

        for libro, valores in _diccionario.items():
            fila = f"{libro:<{anchoNombre}}"
            for val in valores:
                if val == 0:
                    fila += f"{'':>{anchoMes}}"
                else:
                    fila += f"{'$' + format(val, '.2f'):>{anchoMes}}" if _esDinero else f"{val:>{anchoMes}}"
            salida.append(fila)

        salida.append("-" * totalColumnas)
        return "\n".join(salida)
    except Exception as e:
        print(f"Error inesperado al formatear informe: {e}")
        return ""

# ----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
# ----------------------------------------------------------------------------------------------
def main():
    # -------------------------------------------------
    # Inicialización de variables
    # ----------------------------------------------------------------------------------------------
    """
    alumnos = {
        "A1001": {
            "activo": True,
            "nombre": "Ana",
            "apellido": "López",
            "direccion": "Calle Falsa 123, CABA",
            "email": "ana@mail.com",
            "telefono": {"celular": 1122334455, "fijo": 47891234},
            "infracciones": 0,
        },
        "A1002": {
            "activo": False,
            "nombre": "Carlos",
            "apellido": "Gómez",
            "direccion": "Av. Libertador 456, CABA",
            "email": "carlos@mail.com",
            "telefono": {"celular": 1155667788, "fijo": 0},
            "infracciones": 2,
        },
        "A1003": {
            "activo": True,
            "nombre": "Luisa",
            "apellido": "Martínez",
            "direccion": "Corrientes 789, CABA",
            "email": "luisa@mail.com",
            "telefono": {"celular": 1199887766, "fijo": 43021987},
            "infracciones": 1,
        },
        "A1004": {
            "activo": True,
            "nombre": "Pedro",
            "apellido": "Díaz",
            "direccion": "Belgrano 101, CABA",
            "email": "pedro@mail.com",
            "telefono": {"celular": 1133445566, "fijo": 45612378},
            "infracciones": 3,
        },
        "A1005": {
            "activo": True,
            "nombre": "Marta",
            "apellido": "Pérez",
            "direccion": "Cabildo 202, CABA",
            "email": "marta@mail.com",
            "telefono": {"celular": 1177889900, "fijo": 0},
            "infracciones": 0,
        },
        "A1006": {
            "activo": False,
            "nombre": "Jorge",
            "apellido": "Rodríguez",
            "direccion": "Scalabrini Ortiz 333, CABA",
            "email": "jorge@mail.com",
            "telefono": {"celular": 1122334455, "fijo": 48235791},
            "infracciones": 1,
        },
        "A1007": {
            "activo": True,
            "nombre": "Sofía",
            "apellido": "Fernández",
            "direccion": "Av. Rivadavia 8500, CABA",
            "email": "sofia@mail.com",
            "telefono": {"celular": 1144221133, "fijo": 0},
            "infracciones": 2,
        },
        "A1008": {
            "activo": True,
            "nombre": "Diego",
            "apellido": "Suárez",
            "direccion": "Av. San Juan 2500, CABA",
            "email": "diego@mail.com",
            "telefono": {"celular": 1188997766, "fijo": 43006789},
            "infracciones": 0,
        },
        "A1009": {
            "activo": True,
            "nombre": "Valeria",
            "apellido": "Prieto",
            "direccion": "José León Suárez 1550, CABA",
            "email": "valeria@mail.com",
            "telefono": {"celular": 1133556688, "fijo": 0},
            "infracciones": 1,
        },
        "A1010": {
            "activo": True,
            "nombre": "Esteban",
            "apellido": "Ramos",
            "direccion": "Av. Las Heras 3400, CABA",
            "email": "esteban@mail.com",
            "telefono": {"celular": 1166442211, "fijo": 47771234},
            "infracciones": 3,
        },
    }

    libros = {
        "L1001": {
            "titulo": "Cien años de soledad",
            "autores": {"autor1": "Gabriel García Márquez", "autor2": "", "autor3": ""},
            "activo": True,
            "genero": "Realismo mágico",
            "editorial": "Sudamericana",
            "costoGarantia": 3200,
        },
        "L1002": {
            "titulo": "1984",
            "autores": {"autor1": "George Orwell", "autor2": "", "autor3": ""},
            "activo": True,
            "genero": "Distopía",
            "editorial": "Secker & Warburg",
            "costoGarantia": 4100,
        },
        "L1003": {
            "titulo": "Orgullo y prejuicio",
            "autores": {"autor1": "Jane Austen", "autor2": "", "autor3": ""},
            "activo": True,
            "genero": "Novela romántica",
            "editorial": "T. Egerton",
            "costoGarantia": 2700,
        },
        "L1004": {
            "titulo": "El nombre de la rosa",
            "autores": {"autor1": "Umberto Eco", "autor2": "", "autor3": ""},
            "activo": True,
            "genero": "Novela histórica",
            "editorial": "Bompiani",
            "costoGarantia": 4800,
        },
        "L1005": {
            "titulo": "Crónica de una muerte anunciada",
            "autores": {"autor1": "Gabriel García Márquez", "autor2": "", "autor3": ""},
            "activo": True,
            "genero": "Novela corta",
            "editorial": "Oveja Negra",
            "costoGarantia": 2500,
        },
        "L1006": {
            "titulo": "El principito",
            "autores": {
                "autor1": "Antoine de Saint-Exupéry",
                "autor2": "",
                "autor3": "",
            },
            "activo": True,
            "genero": "Fábula",
            "editorial": "Reynal & Hitchcock",
            "costoGarantia": 1500,
        },
        "L1007": {
            "titulo": "Los detectives salvajes",
            "autores": {"autor1": "Roberto Bolaño", "autor2": "", "autor3": ""},
            "activo": True,
            "genero": "Novela",
            "editorial": "Anagrama",
            "costoGarantia": 3400,
        },
        "L1008": {
            "titulo": "La sombra del viento",
            "autores": {"autor1": "Carlos Ruiz Zafón", "autor2": "", "autor3": ""},
            "activo": True,
            "genero": "Misterio",
            "editorial": "Planeta",
            "costoGarantia": 3900,
        },
        "L1009": {
            "titulo": "Rayuela",
            "autores": {"autor1": "Julio Cortázar", "autor2": "", "autor3": ""},
            "activo": True,
            "genero": "Novela experimental",
            "editorial": "Sudamericana",
            "costoGarantia": 1800,
        },
        "L1010": {
            "titulo": "El amor en los tiempos del cólera",
            "autores": {"autor1": "Gabriel García Márquez", "autor2": "", "autor3": ""},
            "activo": False,
            "genero": "Novela",
            "editorial": "Oveja Negra",
            "costoGarantia": 3000,
        },
    }

    prestamos = {
        "2025.05.01 09:15:32": {
            "idPrestamo": "2025.05.01 09:15:32",
            "idAlumno": "A1001",
            "idLibro": "L1002",
            "cantidadDias": 14,
            "fechaInicio": "2025-05-01",
            "fechaFinalizacion": "2025-05-15",
            "estadoDevolucionCorrecto": True,
        },
        "2025.05.03 14:07:45": {
            "idPrestamo": "2025.05.03 14:07:45",
            "idAlumno": "A1002",
            "idLibro": "L1005",
            "cantidadDias": 7,
            "fechaInicio": "2025-05-03",
            "fechaFinalizacion": "2025-05-10",
            "estadoDevolucionCorrecto": True,
        },
        "2025.04.20 11:55:12": {
            "idPrestamo": "2025.04.20 11:55:12",
            "idAlumno": "A1003",
            "idLibro": "L1001",
            "cantidadDias": 21,
            "fechaInicio": "2025-04-20",
            "fechaFinalizacion": "2025-05-11",
            "estadoDevolucionCorrecto": False,
        },
        "2025.05.25 16:20:05": {
            "idPrestamo": "2025.05.25 16:20:05",
            "idAlumno": "A1004",
            "idLibro": "L1008",
            "cantidadDias": 10,
            "fechaInicio": "2025-05-25",
            "fechaFinalizacion": "2025-06-04",
            "estadoDevolucionCorrecto": True,
        },
        "2025.04.10 10:40:00": {
            "idPrestamo": "2025.04.10 10:40:00",
            "idAlumno": "A1005",
            "idLibro": "L1004",
            "cantidadDias": 30,
            "fechaInicio": "2025-04-10",
            "fechaFinalizacion": "2025-05-10",
            "estadoDevolucionCorrecto": True,
        },
        "2025.05.18 13:27:18": {
            "idPrestamo": "2025.05.18 13:27:18",
            "idAlumno": "A1006",
            "idLibro": "L1006",
            "cantidadDias": 15,
            "fechaInicio": "2025-05-18",
            "fechaFinalizacion": "2025-06-02",
            "estadoDevolucionCorrecto": False,
        },
        "2025.05.22 08:50:01": {
            "idPrestamo": "2025.05.22 08:50:01",
            "idAlumno": "A1007",
            "idLibro": "L1003",
            "cantidadDias": 12,
            "fechaInicio": "2025-05-22",
            "fechaFinalizacion": "2025-06-03",
            "estadoDevolucionCorrecto": True,
        },
        "2025.05.28 12:12:09": {
            "idPrestamo": "2025.05.28 12:12:09",
            "idAlumno": "A1008",
            "idLibro": "L1009",
            "cantidadDias": 20,
            "fechaInicio": "2025-05-28",
            "fechaFinalizacion": "2025-06-17",
            "estadoDevolucionCorrecto": True,
        },
        "2025.05.30 18:33:44": {
            "idPrestamo": "2025.05.30 18:33:44",
            "idAlumno": "A1009",
            "idLibro": "L1010",
            "cantidadDias": 8,
            "fechaInicio": "2025-05-30",
            "fechaFinalizacion": "2025-06-07",
            "estadoDevolucionCorrecto": False,
        },
        "2025.05.05 15:05:29": {
            "idPrestamo": "2025.05.05 15:05:29",
            "idAlumno": "A1010",
            "idLibro": "L1007",
            "cantidadDias": 25,
            "fechaInicio": "2025-05-05",
            "fechaFinalizacion": "2025-05-30",
            "estadoDevolucionCorrecto": True,
        },
    }
    """

    # ----------------------------------------------------------------------------------------------
    # Bloque de menú
    # ----------------------------------------------------------------------------------------------
    while True:
        while True:
            opciones = 4
            print()
            print("---------------------------")
            print("MENÚ PRINCIPAL")
            print("---------------------------")
            print("[1] Gestión de alumnos")
            print("[2] Gestión de libros")
            print("[3] Gestión de préstamos")
            print("[4] Informes")
            print("---------------------------")
            print("[0] Salir del programa")
            print("---------------------------")
            print()

            opcionSubmenu = ""
            opcionMenuPrincipal = input("Seleccione una opción: ")
            if opcionMenuPrincipal in [
                str(i) for i in range(0, opciones + 1)
            ]:  # Sólo continua si se elije una opcion de menú válida
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcionMenuPrincipal == "0":  # Opción salir del programa
            exit()  # También puede ser sys.exit() para lo cual hay que importar el módulo sys

        elif opcionMenuPrincipal == "1":  # Opción 1 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > GESTIÓN DE ALUMNOS")
                    print("---------------------------")
                    print("[1] Ingresar alumno")
                    print("[2] Modificar alumno")
                    print("[3] Inactivar alumno")
                    print("[4] Listar alumnos")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()

                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [
                        str(i) for i in range(0, opciones + 1)
                    ]:  # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input(
                            "Opción inválida. Presione ENTER para volver a seleccionar."
                        )
                print()

                if opcionSubmenu == "0":  # Opción salir del submenú
                    break  # No sale del programa, sino que vuelve al menú anterior

                elif opcionSubmenu == "1":  # Opción 1 del submenú
                    ingresarAlumno()

                elif opcionSubmenu == "2":  # Opción 2 del submenú
                    modificarAlumno()

                elif opcionSubmenu == "3":  # Opción 3 del submenú
                    inactivarAlumno()

                elif opcionSubmenu == "4":  # Opción 4 del submenú
                    listarAlumnos()

                input("\nPresione ENTER para volver al menú.")  # Pausa entre opciones
                print("\n\n")

        elif opcionMenuPrincipal == "2":  # Opción 2 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > GESTIÓN DE LIBROS")
                    print("---------------------------")
                    print("[1] Ingresar libro")
                    print("[2] Modificar libro")
                    print("[3] Eliminar libros")
                    print("[4] Listado de libros")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")

                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [
                        str(i) for i in range(0, opciones + 1)
                    ]:  # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input(
                            "Opción inválida. Presione ENTER para volver a seleccionar."
                        )
                print()

                if opcionSubmenu == "0":  # Opción salir del submenú
                    break  # No sale del programa, sino que vuelve al menú anterior

                elif opcionSubmenu == "1":  # Opción 1 del submenú
                    ingresarLibro()

                elif opcionSubmenu == "2":  # Opción 2 del submenú
                    modificarLibro()

                elif opcionSubmenu == "3":  # Opción 3 del submenú
                    inactivarLibro()

                elif opcionSubmenu == "4":  # Opción 4 del submenú
                    listarLibros()

                input("\nPresione ENTER para volver al menú.")  # Pausa entre opciones
                print("\n\n")

        elif opcionMenuPrincipal == "3":  # Opción 3 del menú principal
            while True:
                while True:
                    opciones = 2
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > GESTIÓN DE PRÉSTAMOS")
                    print("---------------------------")
                    print("[1] Registro de préstamo")
                    print("[2] Finalización de préstamo")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")

                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [
                        str(i) for i in range(0, opciones + 1)
                    ]:  # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input(
                            "Opción inválida. Presione ENTER para volver a seleccionar."
                        )
                print()

                if opcionSubmenu == "0":  # Opción salir del submenú
                    break  # No sale del programa, sino que vuelve al menú anterior

                elif opcionSubmenu == "1":  # Opción 1 del submenú
                    registrarPrestamo()

                elif opcionSubmenu == "2":  # Opción 2 del submenú
                    finalizarPrestamo()

                input("\nPresione ENTER para volver al menú.")  # Pausa entre opciones
                print("\n\n")

        elif opcionMenuPrincipal == "4":  # Opción 4 del menú principal
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > INFORMES")
                    print("---------------------------")
                    print("[1] Reservas del mes")
                    print("[2] Resumen Anual de Reservas por Libro (Cantidades)")
                    print("[3] Resumen Anual de reservas por Libro (Pesos)")
                    print("[4] Resumen anual de reservas con devolución incorrecta")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()

                    opcionSubmenu = input("Seleccione una opción: ")
                    if opcionSubmenu in [
                        str(i) for i in range(0, opciones + 1)
                    ]:  # Sólo continua si se elije una opcion de menú válida
                        break
                    else:
                        input(
                            "Opción inválida. Presione ENTER para volver a seleccionar."
                        )
                print()

                if opcionSubmenu == "0":  # Opción salir del submenú
                    break  # No sale del programa, sino que vuelve al menú anterior

                elif opcionSubmenu == "1":  # Opción 1 del submenú
                    imprimirResumenMensual()

                elif opcionSubmenu == "2":  # Opción 2 del submenú
                    imprimirResumenAnualPorLibroCantidad()

                elif opcionSubmenu == "3":  # Opción 3 del submenú
                    imprimirResumenAnualPorLibroPesos()

                elif opcionSubmenu == "4":  # Opción 4 del submenú
                    imprimirResumenAnualDevolucionesIncorrectas()

                    input("\nPresione ENTER para volver al menú.")
                    print("\n\n")

        if (
            opcionSubmenu != "0"
        ):  # Pausa entre opciones. No la realiza si se vuelve de un submenú
            input("\nPresione ENTER para volver al menú.")
            print("\n\n")


# Punto de entrada al programa
main()
