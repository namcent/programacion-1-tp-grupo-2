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
    Valida si una cadena cumple el formato de email, con la estructura usuario@dominio.extensión.

    Parámetros:
        _dato (str): Cadena a validar como email.

    Retorno:
        bool: True si cumple, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        pat = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$" #caracteres válidos (letras, números, _ . + -), @, dominio (letras, números, -), punto literal y sufijo (letras, números, . -)
        return re.match(pat, _dato) is not None
    except Exception as e:
        print(f"Error inesperado en la validación de email: {e}")
        return False

def esNumeroValido(_dato):
    """
    Valida si una cadena es un número entero. No permite vacíos ni caracteres no numéricos.

    Parámetros:
        _dato (str): Cadena a validar como número.

    Retorno:
        bool: True si puede convertirse a entero, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        int(_dato) # Intentamos conversión a int. Si falla, no es válido
        return True
    except (ValueError):
        return False
    except Exception as e:
        print(f"Error inesperado en la validación de número: {e}")
        return False

def esIdValido(_dato):
    """
    Valida que una cadena empiece con una letra (mayúscula o minúscula) seguida de uno o más dígitos.

    Parámetros:
        _dato (str): Cadena a validar como ID.

    Retorno:
        bool: True si cumple el patrón, False en caso contrario.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        patron = r"^[A-Za-z]\d+$" # 1 letra y 1 o más números
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
            r"^\d{4}\."                       # Año (4 números)
            r"(0[1-9]|1[0-2])\."              # Mes (01-12)
            r"(0[1-9]|[12]\d|3[01]) "         # Día (01-31)
            r"([01]\d|2[0-3]):"               # Hora (00-23)
            r"[0-5]\d:"                       # Minuto (00-59)
            r"[0-5]\d$"                       # Segundo (00-59)
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
    
def obtenerValor(_campo, _tipoDato):
    """
    Pide al usuario el valor correspondiente a un campo y lo valida según su tipo de dato.

    Parámetros:
        _campo (str): Etiqueta o nombre del campo a solicitar (p.ej. "autores", "costo", etc.).
        _tipoDato (str): Tipo de validación a aplicar ("autores", "numero", "string", "email", "direccion", etc.).

    Retorno:
        dict|int|str: 
            - Si el campo es "autores", devuelve un diccionario con las claves "autor1", "autor2" y "autor3".  
            - Si el tipo de dato es "numero", devuelve un entero.  
            - Para otros tipos, devuelve la cadena validada.
    """
    if _campo == "autores":
        autores = validarDato(input("\nIngresar autores (separados por coma, máx 3): ").strip(), "autores", "autores")
        autoresCortados = [
            parte.strip() for parte in autores.split(",") if parte.strip()
        ]
        autoresRellenados = (autoresCortados + ["", "", ""])[:3]
        return {
            "autor1": autoresRellenados[0],
            "autor2": autoresRellenados[1],
            "autor3": autoresRellenados[2],
        }

    if _tipoDato == "numero":
        mensaje = "Ingresar costo de garantía ($): " if _campo == "costo" else f"Ingresar {_campo}: "
        entrada = validarDato(input(mensaje), _campo, "numero")
        return int(entrada)

    # resto de tipos (string, email, dirección, etc.)
    mensaje = f"Ingresar {_campo}: "
    entrada = validarDato(input(mensaje), _campo, _tipoDato)
    return entrada

def asignarValorEnRegistro(_registro, _campo, _valor):
    """
    Asigna un valor a un registro, creando diccionarios anidados si el campo incluye puntos.

    Parámetros:
        _registro (dict): Diccionario donde se guardará el valor.
        _campo (str): Ruta del campo, que puede incluir niveles separados por ".".
        _valor: Valor a asignar en el registro.
    """
    if "." in _campo:
        partes = _campo.split(".")
        nodo = _registro
        for parte in partes[:-1]:
            try:
                nodo = nodo[parte]
            except KeyError:
                nodo[parte] = {}
                nodo = nodo[parte]
        nodo[partes[-1]] = _valor
    else:
        _registro[_campo] = _valor

def crearEntidad(_ruta, _tipo, _esquema):
    """
    Pide datos al usuario según un esquema y crea una nueva entidad en el archivo JSON.

    Parámetros:
        _ruta (str): Ruta del archivo JSON donde se guardaran las entidades.
        _tipo (str): Nombre de la entidad para mensajes (ej. "alumno", "libro", etc.).
        _esquema (dict): Estructura que define el campo ID y la lista de campos que se pediran.
    """
    diccionario = cargarArchivo(_ruta)

    idValidador = _esquema['id']
    id = pedirYValidarId(diccionario, _tipo, False, idValidador) # pedirYValidarId(alumnos, "alumno", True, "id")
    if id is None:
        return

    # Preparar el registro con el flag activo
    registro = {'activo': True}
    # Construir mapa etiqueta → (campoReal, tipoDato)
    opciones = {
        etiqueta: (campoReal, tipoDato)
        for etiqueta, campoReal, tipoDato in _esquema['campos']
    }

    # Para cada campo del esquema, pedimos valor y lo asignamos
    for etiqueta, (campoReal, tipoDato) in opciones.items():
        valor = obtenerValor(etiqueta, tipoDato)
        # si el campo real era "costo", obtenerValor ya lo pidió con etiqueta "costo"
        asignarValorEnRegistro(registro, campoReal, valor)

    # En caso de alumno, inicializar infracciones a 0
    if _tipo == "alumno":
        registro["infracciones"] = 0

    # Insertar y guardar
    diccionario[id] = registro

    escribirArchivo(_ruta, diccionario)
    print(f"{_tipo.capitalize()} {id} registrado correctamente.")


def modificarEntidad(_ruta, _tipo, _esquema):
    """
    Pide un campo y un nuevo valor para modificar una entidad existente en el archivo JSON.

    Parámetros:
        _ruta (str): Ruta del archivo JSON donde se guardaran las entidades.
        _tipo (str): Nombre de la entidad para mensajes (ej. "alumno", "libro", etc.).
        _esquema (dict): Estructura que define el campo ID y la lista de campos disponibles para modificar.
    """
    diccionario = cargarArchivo(_ruta)

    idValidador = _esquema['id']
    id = pedirYValidarId(diccionario, _tipo, True, idValidador) # pedirYValidarId(alumnos, "alumno", True, "id")
    if id is None:
        return

    # Construir mapa etiqueta → (campoReal, tipoDato)
    opciones = {
        etiqueta: (campoReal, tipoDato)
        for etiqueta, campoReal, tipoDato in _esquema["campos"]
    }

    print(f"opciones: {opciones}")

    # Mostrar menú de campos
    print("\nCampos disponibles para modificar:")
    for etiqueta in opciones:
        print(f"- {etiqueta}")

    # Leer elección
    etiquetaSeleccionada = validarDato(
        input("\nIngresá el campo a modificar: ").strip().lower(),
        "campo",
        "string"
    )
    while etiquetaSeleccionada not in opciones:
        etiquetaSeleccionada = validarDato(
            input("Error. Por favor ingrese un campo disponible de la lista: ").strip().lower(),
            "campo",
            "string"
        )

    # Obtener ruta real y tipo, pedir valor y asignar
    campoReal, tipoDato = opciones[etiquetaSeleccionada]
    valor = obtenerValor(etiquetaSeleccionada, tipoDato)

    asignarValorEnRegistro(diccionario[id], campoReal, valor)

    escribirArchivo(_ruta, diccionario)
    print(f"\n{_tipo.capitalize()} {id} modificado correctamente.")


def inactivarEntidad(_ruta, _tipo, _esquema):
    """
    Marca como inactiva una entidad existente guardando su campo "activo" en False.

    Parámetros:
        _ruta (str): Ruta del archivo JSON donde se guardaran las entidades.
        _tipo (str): Nombre de la entidad para mensajes (ej. "alumno", "libro", etc.).
        _esquema (dict): Estructura que define el campo ID de la entidad.
    """
    diccionario = cargarArchivo(_ruta)

    idValidador = _esquema['id']
    id = pedirYValidarId(diccionario, _tipo, True, idValidador) # pedirYValidarId(alumnos, "alumno", True, "id")
    if id is None:
            return

    diccionario[id]['activo'] = False
    escribirArchivo(_ruta, diccionario)
    print(f"{_tipo.capitalize()} {id} inactivado correctamente.")

def listarEntidades(_ruta, _tipo, _esquema):
    """
    Muestra por consola el listado de las entidades activas según el esquema.

    Parámetros:
        _ruta (str): Ruta del archivo JSON donde se guardan las entidades.
        _tipo (str): Nombre de la entidad para mensajes (ej. "alumno", "libro", etc.).
        _esquema (dict): Estructura que define la lista de campos a mostrar.
    """
    diccionario = cargarArchivo(_ruta)
    
    activos = {k:v for k,v in diccionario.items() if v['activo']}

    if not activos:
        print(f"No se encontraron {_tipo}s activos.")
        return
    
    print(f"\nLISTADO DE {_tipo.upper()}S ACTIVOS")
    print("-" * 50)

    for id, registro in activos.items():
        print(f"ID: {id}")
        for etiqueta, campoReal, tipoDato in _esquema['campos']:
            if '.' in campoReal:
                partes = campoReal.split('.')
                nodo = registro
                for parte in partes:
                    nodo = nodo[parte]
                valor = nodo

            else:
                valor = registro[campoReal]
            print(f"{etiqueta.upper()}: {valor}")
        print("-" * 50)

def ingresarAlumno():
    """
    Registra un nuevo alumno. Solicita sus datos, lo registra en el archivo JSON y confirma su 
    creación.
    """
    try:
        esquema = {
            'id': 'id',
            'campos': [
                ('nombre', 'nombre', 'string'),
                ('apellido', 'apellido', 'string'),
                ('dirección', 'direccion', 'direccion'),
                ('email', 'email', 'email'),
                ('celular', 'telefono.celular', 'numero'),
                ('fijo', 'telefono.fijo', 'numero')
            ]
        }
        crearEntidad(ALUMNOS_ARCHIVO, "alumno", esquema)

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
        esquema = {
            'id': 'id',
            'campos': [
                ('nombre', 'nombre', 'string'),
                ('apellido', 'apellido', 'string'),
                ('dirección', 'direccion', 'direccion'),
                ('email', 'email', 'email'),
                ('celular', 'telefono.celular', 'numero'),
                ('fijo', 'telefono.fijo', 'numero')
            ]
        }
        modificarEntidad(ALUMNOS_ARCHIVO, "alumno", esquema)

    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al modificar alumno: {e}")


def inactivarAlumno():
    """
    Marca como inactivo a un alumno existente (baja lógica) identificado por ID.
    """
    try:
        esquema = {
            'id': 'id',
            'campos': [
                ('nombre', 'nombre', 'string'),
                ('apellido', 'apellido', 'string'),
                ('dirección', 'direccion', 'direccion'),
                ('email', 'email', 'email'),
                ('celular', 'telefono.celular', 'numero'),
                ('fijo', 'telefono.fijo', 'numero')
            ]
        }
        inactivarEntidad(ALUMNOS_ARCHIVO, "alumno", esquema)

    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al inactivar alumno: {e}")


def listarAlumnos():
    """
    Imprime por consola el listado de alumnos activos y sus datos.
    """
    try:
        esquema = {
            'id': 'id', #idPrestamo
            'campos': [
                ('nombre', 'nombre', 'string'),
                ('apellido', 'apellido', 'string'),
                ('dirección', 'direccion', 'direccion'),
                ('email', 'email', 'email'),
                ('teléfono celular', 'telefono.celular', 'numero'),
                ('teléfono fijo', 'telefono.fijo', 'numero'),
                ('infracciones', 'infracciones','numero')
            ]
        }
        listarEntidades(ALUMNOS_ARCHIVO, "alumno", esquema)

    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al listar alumnos: {e}")


def ingresarLibro():
    """
    Registra un nuevo libro. Solicita los datos del nuevo libro, lo registra en el JSON y confirma su creación.
    """
    try:
        esquema = {
            'id': 'id', #idPrestamo
            'campos': [
                ('título', 'titulo', 'string'),
                ('autores','autores', 'autores'),
                ('género', 'genero', 'string'),
                ('editorial', 'editorial', 'string'),
                ('costo', 'costoGarantia', 'numero')
            ]
        }
        crearEntidad(LIBROS_ARCHIVO, "libro", esquema)

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
        esquema = {
            'id': 'id', #idPrestamo
            'campos': [
                ('título', 'titulo', 'string'),
                ('autores','autores', 'autores'),
                ('género', 'genero', 'string'),
                ('editorial', 'editorial', 'string'),
                ('costo', 'costoGarantia', 'numero')
            ]
        }
        modificarEntidad(LIBROS_ARCHIVO, "libro", esquema)

    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al modificar libro: {e}")


def inactivarLibro():
    """
    Marca como inactivo a un libro existente (baja lógica) identificado por ID.
    """
    try:
        esquema = {
            'id': 'id', #idPrestamo
            'campos': [
                ('título', 'titulo', 'string'),
                ('autores','autores', 'autores'),
                ('género', 'genero', 'string'),
                ('editorial', 'editorial', 'string'),
                ('costo', 'costoGarantia', 'numero')
            ]
        }
        inactivarEntidad(LIBROS_ARCHIVO, "libro", esquema)

    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
    except Exception as e:
        print(f"Error inesperado al inactivar libro: {e}")


def listarLibros():
    """
    Imprime por consola el listado de libros activos y sus datos.
    """
    try:
        esquema = {
            'id': 'id',
            'campos': [
                ('tÍtulo', 'titulo','string'),
                ('autor 1', 'autores.autor1', 'autores'),
                ('autor 2', 'autores.autor2', 'autores'),
                ('autor 3', 'autores.autor3', 'autores'),
                ('género', 'genero', 'string'),
                ('editorial', 'editorial', 'string'),
                ('costo de garantía', 'costoGarantia', 'numero')
            ]
        }
        listarEntidades(LIBROS_ARCHIVO, "libro", esquema)

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
                    print("[3] Eliminar alumno")
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
