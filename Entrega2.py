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
ALUMNO_ESQUEMA = {
    'id': 'id',
    'campos': [ # (etiqueta de campo, campo o ruta de campo, tipo de campo)
        ('nombre', 'nombre', 'string'), 
        ('apellido', 'apellido', 'string'),
        ('dirección', 'direccion', 'direccion'),
        ('email', 'email', 'email'),
        ('celular', 'telefono.celular', 'numero'),
        ('fijo', 'telefono.fijo', 'numero'),
    ]
}

LIBRO_ESQUEMA = {
    'id': 'id',
    'campos': [ # (etiqueta de campo, campo o ruta de campo, tipo de campo)
        ('título', 'titulo', 'string'),
        ('autores', 'autores', 'autores'),
        ('género', 'genero', 'string'),
        ('editorial', 'editorial', 'string'),
        ('costo', 'costoGarantia', 'numero'),
    ]
}

# ----------------------------------------------------------------------------------------------
# FUNCIONES
# ----------------------------------------------------------------------------------------------
def esEmailValido(_dato):
    """
    Valida si una cadena cumple el formato de email, con la estructura 'usuario@dominio.extensión'.

    Parámetros:
        _dato (str): Cadena a validar como email.

    Retorno:
        bool: True si cumple, False en caso contrario o excepción.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        pat = (
            r"^[A-Za-z0-9_.+-]+"   # Usuario: letras, números y caracteres . _ + -
            r"@"                   # Símbolo @ obligatorio
            r"[A-Za-z0-9-]+\."     # Dominio: letras, números, guiones y punto
            r"[A-Za-z]{2,}$"       # Extensión: al menos 2 letras al final
        )
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
        bool: True si puede convertirse a entero, False en caso contrario o excepción.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        int(_dato) # Intentamos conversión a int
        return True
    except (ValueError): # Si falla, no es válido
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
        bool: True si cumple el patrón, False en caso contrario o excepción.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        patron = (
            r"^[A-Za-z]"   # Una letra inicial (A-Z o a-z)
            r"\d+$"        # Uno o más dígitos          
        )
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
        bool: True si coincide con el patrón de fecha y hora, False en caso contrario o excepción.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False

        patron = (
            r"^\d{4}\."                       # Año (4 números) + punto
            r"(0[1-9]|1[0-2])\."              # Mes (01-12) + punto
            r"(0[1-9]|[12]\d|3[01]) "         # Día (01-31) + espacio
            r"([01]\d|2[0-3]):"               # Hora (00-23) + ':'
            r"[0-5]\d:"                       # Minuto (00-59) + ':'
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
        bool: True si cumple, False en caso contrario o excepción.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        patron = (
            r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\.]+"          # Primer bloque: letras, números y punto
            r"(?: [A-Za-zÁÉÍÓÚáéíóúÑñ0-9\.]+)*$"    # Bloques opcionales: espacio + letras, números y punto
        )
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
        bool: True si hay entre 1 y 3 cadenas de letras válidas separadas por comas, False en 
        caso contrario o excepción.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        patrón = (
            r'^[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+'                 # Nombre del primer autor (obligatorio): al menos una letra
            r'(?:\s+[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+)*'          # Posibles espacios + segundos nombres o apellidos
            r'(?:\s*,\s*'                               # Coma y espacios opcionales
            r'[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+'                  # Nombre del siguiente autor (opcional)
            r'(?:\s+[A-Za-zÁÉÍÓÚáéíóúÜüÑñ]+)*)'         # Posibles espacios + segundos nombres o apellidos
            r'{0,2}$'                                   # Bloque opcional: máximo 2 repeticiones. Total: 3 autores (1 obligatorio + 2 opcionales)
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
        bool: True si cumple, False en caso contrario o excepción.
    """
    try:
        if _dato is None or _dato.strip() == "":
            return False
        
        patron = (
            r"^[A-Za-zÁÉÍÓÚáéíóúÑñ]+"           # Al menos una letra válida al inicio
            r"(?:\s+[A-Za-zÁÉÍÓÚáéíóúÑñ]+)*$"     # Bloques opcionales separados por espacios
        )
        
        return re.match(patron, _dato) is not None
    except Exception as e:
        print(f"Error inesperado en la validación de string: {e}")
        return False

def validarDato(_dato, _etiqueta, _validacion):
    """
    Pide al usuario un dato hasta que pase la validación indicada.

    Parámetros:
        _dato (str): Valor inicial ingresado.
        _etiqueta (str): Nombre para el mensaje de error (ej. "email", "id").
        _validacion (str): Tipo de validación ("email", "numero", "id", "idPrestamo", "direccion", 
        "autores" o por defecto "string").

    Retorno:
        str: Valor validado y formateado (strip/upper) que cumple la validación o cadena vacía en 
        caso de excepción.
    """
    try:
        # Selección del validador en base al tipo solicitado
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

        # Mientras la función de validación devuelva False, volvemos a pedir el dato
        while not validador(dato):
            dato = input(f"Error. Por favor ingrese un/a/os {_etiqueta} válido/a/s: ").strip()
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
        None: Si hay un error al abrir o parsear el archivo.
    """
    try:
        archivo = open(_direccion, mode="r", encoding="utf-8")
        diccionario = json.load(archivo)
        archivo.close()
        return diccionario
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None

def escribirArchivo(_direccion, _diccionario):
    """
    Escribe un diccionario en un archivo JSON.

    Parámetros:
        _direccion (str): Ruta del archivo JSON.
        _diccionario (dict): Diccionario a escribir.
    
    Retorno:
        None: Se escribe el archivo JSON y devuelve None. En caso de error al abrir o parsear 
        el archivo, lo informa y devuelve None.
    """
    try:
        archivo = open(_direccion, mode="w", encoding="utf-8")
        json.dump(_diccionario, archivo, ensure_ascii=False, indent=4)
        archivo.close()
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)

def pedirYValidarId(_diccionario, _etiqueta, _validarExistente, _validacion):
    """
    Solicita un ID y valida su existencia o inexistencia según lo que se ingrese como parámetro.

    Parámetros:
        _diccionario (dict): Diccionario donde buscar la existencia o inexistencia de un valor.
        _etiqueta (str): Nombre para el mensaje de error (ej. "alumno", "libro").
        _validarExistente (bool): True si el ID debe existir y estar activo, False si debe ser nuevo.
        _validacion (str): Tipo de validación para el ID ("id" o "idPrestamo").

    Retorno:
        str|None: ID validado (en mayúsculas) o None si el usuario ingresa '0' para volver o se captura 
        una excepción.
    """
    try:
        entrada = validarDato(input(f"Ingrese el ID del {_etiqueta}: "), "id", _validacion).strip().upper()

        # Caso id préstamo: chequeo de 'fechaFinalizacion' para saber si sigue activo
        if _validacion == "idPrestamo" and _validarExistente:
            valido = False
            while not valido:
                if entrada == "0": # Opción de volver
                    return None
                
                if entrada not in _diccionario: # Chequeo existencia del id
                    print("Error: el ID de préstamo no existe.")
                else:
                    prestamo = _diccionario[entrada]
                    if prestamo["fechaFinalizacion"] != "":  # Chequeo si está activo
                        print("Error: el préstamo ya fue finalizado.")
                    else:
                        valido = True # fechaFinalizacion == "" (todavía activo)

                if not valido:
                    entrada = validarDato(
                        input("Por favor ingrese un ID de préstamo válido (0 para volver): "),
                        "préstamo",
                        "idPrestamo"
                    ).strip().upper()
            return entrada
        
        # Caso id alumno/libro: chequeo de campo 'activo'
        if _validarExistente and _validacion != "idPrestamo":
            while entrada not in _diccionario or not _diccionario[entrada]["activo"]:
                print(f"Error: el ID del {_etiqueta} no existe o está inactivo.")
                entrada = input(f"Por favor, ingrese el ID del {_etiqueta} (0 para volver): ").strip().upper()
                if entrada == "0": # Opción de volver
                    return None
                else:
                    entrada = validarDato(entrada, "id", _validacion).upper()

            return entrada
        else:
            # Caso creación de nuevo id: chequeo de no existencia previa
            while entrada in _diccionario:
                print(f"Error: el ID del {_etiqueta} que ingresó ya existe.")
                entrada = input(f"Por favor ingrese un nuevo ID del {_etiqueta} (0 para volver): ").strip().upper()
                if entrada == "0": # Opción de volver
                    return None
                else:
                    entrada = validarDato(entrada, "id", _validacion).upper()

            return entrada
    except Exception as e:
        print(f"Error inesperado en el pedido y validación de ID: {e}")
        return None
    
def obtenerValor(_etiqueta, _tipoDato):
    """
    Pide al usuario el valor correspondiente a un campo y lo valida según su tipo de dato.

    Parámetros:
        _etiqueta (str): Nombre del campo a solicitar (ej. "autores", "costo", etc.).
        _tipoDato (str): Tipo de validación a aplicar ("autores", "numero", "string", "email", "direccion", etc.).

    Retorno:
        dict|int|str|None: 
            - Si el campo es "autores", devuelve un diccionario con las claves "autor1", "autor2" y "autor3".  
            - Si el tipo de dato es "numero", devuelve un entero.  
            - Para otros tipos, devuelve la cadena validada.
            - Si se captura una excepción lo informa y devuelve None.
    """
    try:
        if _etiqueta == "autores":
            autores = validarDato(input("\nIngresar autores (separados por coma, máx 3): ").strip(), "autores", "autores")
            autoresCortados = [
                parte.strip() for parte in autores.split(",") if parte.strip() # Separa la cadena de autores por coma y elimina los espacios en blanco al ppio y al final
            ]
            autoresRellenados = (autoresCortados + ["", "", ""])[:3] # Rellena con 3 cadenas vacías y aplica un slice para solo obtener 3 elementos
            return {
                "autor1": autoresRellenados[0], # Completa el diccionario con cada uno de los elementos
                "autor2": autoresRellenados[1],
                "autor3": autoresRellenados[2],
            }

        if _tipoDato == "numero":
            mensaje = "Ingresar costo de garantía ($): " if _etiqueta == "costo" else f"Ingresar {_etiqueta}: "
            entrada = validarDato(input(mensaje), _etiqueta, "numero")
            return int(entrada)

        # Valida el resto de los tipos de datos (string, email, dirección, etc.)
        mensaje = f"Ingresar {_etiqueta}: "
        entrada = validarDato(input(mensaje), _etiqueta, _tipoDato)
        return entrada
    except Exception as e:
        print(f"Error inesperado al obtener valor: {e}")
        return None

def asignarValorEnRegistro(_registro, _campo, _valor):
    """
    Asigna un valor a un registro, creando diccionarios anidados si el campo incluye puntos.

    Parámetros:
        _registro (dict): Diccionario donde se guardará el valor.
        _campo (str): Ruta del campo, que puede incluir niveles separados por ".".
        _valor: Valor a asignar en el registro.

    Retorno:
        None: Se modifica el diccionario y devuelve None. Si se captura una excepción lo informa 
        y devuelve None.
    """
    try:
        if "." in _campo: # Caso de ruta anidada
            partes = _campo.split(".") # Separa la ruta por punto
            nodo = _registro
            for parte in partes[:-1]: # Itera los valores de la ruta sin incluir el último para garantizar que existan
                try:
                    nodo = nodo[parte] # Intenta apuntar al valor de ruta de esa iteración
                except KeyError: # Si el valor no existe lanzará KeyError
                    nodo[parte] = {} # Crea el diccionario anidado para ese valor
                    nodo = nodo[parte] # Apunta a ese valor
            nodo[partes[-1]] = _valor # Asigna el valor a la última clave de la ruta
        else:
            _registro[_campo] = _valor
        return None
    except Exception as e:
        print(f"Error inesperado al asignar valor al registro: {e}")
        return None

def crearRegistro(_ruta, _etiqueta, _esquema):
    """
    Pide datos al usuario según un esquema y crea un nueva registro en el archivo JSON.

    Parámetros:
        _ruta (str): Ruta del archivo JSON donde se guardaran los registros.
        _etiqueta (str): Nombre del registro para mensajes (ej. "alumno", "libro", etc.).
        _esquema (dict): Estructura que define el campo ID y la lista de campos que se pediran.
    
    Retorno:
        None: Se crea el registro, se guarda sobre el archivo JSON y devuelve None. Si el usuario 
        ingresa '0' para volver o se captura una excepción se informa y devuelve None.
    """
    try:
        diccionario = cargarArchivo(_ruta)

        # Pide y valida el id
        idValidador = _esquema['id']
        id = pedirYValidarId(diccionario, _etiqueta, False, idValidador)
        if id is None:
            return None

        # Crea el registro con el flag activo True
        registro = {'activo': True}

        # Construye el mapa donde vuelca el esquema con el formato: etiqueta -> (campoReal, tipoDato)
        opciones = {
            etiqueta: (campoReal, tipoDato)
            for etiqueta, campoReal, tipoDato in _esquema['campos']
        }

        # Para cada campo del esquema pide el valor y lo asigna
        for etiqueta, (campoReal, tipoDato) in opciones.items():
            valor = obtenerValor(etiqueta, tipoDato)
            asignarValorEnRegistro(registro, campoReal, valor)

        # En el caso de alumno inicializa las infracciones en 0
        if _etiqueta == "alumno":
            registro["infracciones"] = 0

        # Asigna el registro correspondiente al id en el diccionario
        diccionario[id] = registro
        
        escribirArchivo(_ruta, diccionario)

        print(f"{_etiqueta.capitalize()} {id} registrado correctamente.")
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al crear registro: {e}")
        return None

def modificarRegistro(_ruta, _etiqueta, _esquema):
    """
    Pide un campo y un nuevo valor para modificar un registro existente en el archivo JSON.

    Parámetros:
        _ruta (str): Ruta del archivo JSON donde se guardaran los registros.
        _etiqueta (str): Nombre del registro para mensajes (ej. "alumno", "libro", etc.).
        _esquema (dict): Estructura que define el campo ID y la lista de campos disponibles para modificar.
    
    Retorno:
        None: Se modifica el registro, se guarda sobre el archivo JSON y devuelve None. Si el usuario 
        ingresa '0' para volver o se captura una excepción se informa y devuelve None.
    """
    try:
        diccionario = cargarArchivo(_ruta)

        # Pide y valida el id
        idValidador = _esquema['id']
        id = pedirYValidarId(diccionario, _etiqueta, True, idValidador)
        if id is None:
            return None

        # Construye el mapa donde vuelca el esquema con el formato: etiqueta -> (campoReal, tipoDato)
        opciones = {
            etiqueta: (campoReal, tipoDato)
            for etiqueta, campoReal, tipoDato in _esquema["campos"]
        }

        # Muestra menú de campos modificables
        print("\nCampos disponibles para modificar:")
        for etiqueta in opciones:
            print(f"- {etiqueta}")

        # Pide y valida la selección
        etiquetaSeleccionada = validarDato(
            input("\nIngresá el campo a modificar (respetando tildes): ").strip().lower(),
            "campo",
            "string"
        )
        while etiquetaSeleccionada not in opciones:
            etiquetaSeleccionada = validarDato(
                input("Error. Por favor ingrese un campo disponible de la lista: ").strip().lower(),
                "campo",
                "string"
            )

        # Obtiene la ruta y el tipo de dato del campo seleccionado
        campoReal, tipoDato = opciones[etiquetaSeleccionada]
        
        # Pide el valor y lo asigna
        valor = obtenerValor(etiquetaSeleccionada, tipoDato)
        asignarValorEnRegistro(diccionario[id], campoReal, valor)

        escribirArchivo(_ruta, diccionario)

        print(f"\n{_etiqueta.capitalize()} {id} modificado correctamente.")
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al modificar registro: {e}")
        return None

def inactivarRegistro(_ruta, _etiqueta, _esquema):
    """
    Marca como inactiva un registro existente guardando su campo "activo" en False.

    Parámetros:
        _ruta (str): Ruta del archivo JSON donde se guardaran los registros.
        _etiqueta (str): Nombre del registro para mensajes (ej. "alumno", "libro", etc.).
        _esquema (dict): Estructura que define el campo ID del registro.
    
    Retorno:
        None: Se inactiva el registro, se guarda sobre el archivo JSON y devuelve None. Si el usuario 
        ingresa '0' para volver o se captura una excepción se informa y devuelve None.
    """
    try:
        diccionario = cargarArchivo(_ruta)

        # Pide y valida el id
        idValidador = _esquema['id']
        id = pedirYValidarId(diccionario, _etiqueta, True, idValidador)
        if id is None:
            return None

        # Sobreescribe el campo 'activo' de ese id en False
        diccionario[id]['activo'] = False

        escribirArchivo(_ruta, diccionario)

        print(f"{_etiqueta.capitalize()} {id} inactivado correctamente.")
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al inactivar registro: {e}")
        return None

def listarRegistros(_ruta, _etiqueta, _esquema):
    """
    Muestra por consola el listado de los registros activos según el esquema.

    Parámetros:
        _ruta (str): Ruta del archivo JSON donde se guardan los registros.
        _etiqueta (str): Nombre del registro para mensajes (ej. "alumno", "libro", etc.).
        _esquema (dict): Estructura que define la lista de campos a mostrar.
    
    Retorno:
        None: Se lista el registro y devuelve None. Si no se encontraron registros activos 
        o se captura una excepción se informa y devuelve None.
    """
    try:
        diccionario = cargarArchivo(_ruta)
        
        # Crea un diccionario que solo contiene elementos con el campo 'activo' en True
        activos = {k:v for k,v in diccionario.items() if v['activo']}

        # Si no hay elementos en el diccionario imprime mensaje de aviso y sale
        if not activos:
            print(f"No se encontraron {_etiqueta}s activos.")
            return None
        
        # Imprime la lista de registros activos
        print(f"\nLISTADO DE {_etiqueta.upper()}S ACTIVOS")
        print("-" * 50)

        for id, registro in activos.items():
            print(f"ID: {id}")

            # Obtiene los valores de cada campo y los imprime
            for etiqueta, campoReal, tipoDato in _esquema['campos']:

                if '.' in campoReal: # Caso de ruta anidada
                    partes = campoReal.split('.') # Separa la ruta por punto
                    nodo = registro
                    for parte in partes: # Itera los valores de la ruta 
                        nodo = nodo[parte] # Apunta al valor de ruta de esa iteración
                    valor = nodo # Asigna el valor de la ruta
                else:  # Caso de clave común
                    valor = registro[campoReal]

                print(f"{etiqueta.upper()}: {valor}")

            print("-" * 50)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al listar registros: {e}")
        return None

def formatearInformes(_diccionario, _anio, _titulo, _esDinero=False):
    """
    Formatea un informe anual en forma de tabla con columnas mensuales.

    Parámetros:
        _diccionario (dict): Diccionario donde las claves son los nombres y los valores son listas con 12 números (uno por mes).
        _anio (int o str): Año del informe.
        _titulo (str): Título centrado que aparecerá en la parte superior del informe.
        _esDinero (bool): Si es True, los valores se muestran con signo '$' y dos decimales.

    Retorno:
        str: Cadena formateada con encabezados, filas alineadas y totales por mes, o cadena vacía en caso de excepción.
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

def ingresarAlumno():
    """
    Registra un nuevo alumno. Permite crear un nuevo registro a partir del esquema correspondiente, 
    guardándolo en su archivo JSON.

    Retorno:
        None: Se crea el registro y devuelve None. Si se captura una excepción se informa y devuelve None.
    """
    try:
        crearRegistro(ALUMNOS_ARCHIVO, "alumno", ALUMNO_ESQUEMA)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al ingresar alumno: {e}")
        return None

def modificarAlumno():
    """
    Modifica los datos de un alumno existente. Permite cambiar uno de los campos de un alumno existente 
    identificado por ID.

    Retorno:
        None: Se modifica el registro y devuelve None. Si se captura una excepción se informa y devuelve None.
    """
    try:
        modificarRegistro(ALUMNOS_ARCHIVO, "alumno", ALUMNO_ESQUEMA)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al modificar alumno: {e}")
        return None

def inactivarAlumno():
    """
    Marca como inactivo a un alumno existente (baja lógica) identificado por ID.

    Retorno:
        None: Se inactiva el registro y devuelve None. Si se captura una excepción se informa y devuelve None.
    """
    try:
        inactivarRegistro(ALUMNOS_ARCHIVO, "alumno", ALUMNO_ESQUEMA)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al inactivar alumno: {e}")
        return None

def listarAlumnos():
    """
    Imprime por consola el listado de alumnos activos y sus datos.

    Retorno:
        None: Se listan los registros y devuelve None. Si se captura una excepción se informa y devuelve None.
    """
    try:
        esquema = {
            'id': ALUMNO_ESQUEMA['id'],
            'campos': ALUMNO_ESQUEMA['campos'] + [
                ('infracciones', 'infracciones', 'numero')
            ]
        }
        listarRegistros(ALUMNOS_ARCHIVO, "alumno", esquema)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al listar alumnos: {e}")
        return None

def ingresarLibro():
    """
    Registra un nuevo libro. Permite crear un nuevo registro a partir del esquema correspondiente, 
    guardándolo en su archivo JSON.

    Retorno:
        None: Se crea el registro y devuelve None. Si se captura una excepción se informa y devuelve None.
    """
    try:
        crearRegistro(LIBROS_ARCHIVO, "libro", LIBRO_ESQUEMA)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al ingresar libro: {e}")
        return None

def modificarLibro():
    """
    Modifica los datos de un libro existente. Permite cambiar uno de los campos de un libro existente 
    identificado por ID.

    Retorno:
        None: Se modifica el registro y devuelve None. Si se captura una excepción se informa y devuelve None.
    """
    try:
        modificarRegistro(LIBROS_ARCHIVO, "libro", LIBRO_ESQUEMA)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al modificar libro: {e}")
        return None

def inactivarLibro():
    """
    Marca como inactivo a un libro existente (baja lógica) identificado por ID.

    Retorno:
        None: Se inactiva el registro y devuelve None. Si se captura una excepción se informa y devuelve None.
    """
    try:
        inactivarRegistro(LIBROS_ARCHIVO, "libro", LIBRO_ESQUEMA)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al inactivar libro: {e}")
        return None

def listarLibros():
    """
    Imprime por consola el listado de libros activos y sus datos.

    Retorno:
        None: Se listan los registros y devuelve None. Si se captura una excepción se informa y devuelve None.
    """
    try:
        base = [
            etiqueta for etiqueta in LIBRO_ESQUEMA['campos']
            if etiqueta[0] != 'autores'
        ]

        autores = [
            ('Autor 1', 'autores.autor1', 'string'),
            ('Autor 2', 'autores.autor2', 'string'),
            ('Autor 3', 'autores.autor3', 'string'),
        ]

        esquema = {
            'id': LIBRO_ESQUEMA['id'],
            'campos': base + autores
        }

        listarRegistros(LIBROS_ARCHIVO, "libro", esquema)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al listar libros: {e}")
        return None

def registrarPrestamo():
    """
    Registra un nuevo préstamo con ID automático de fecha/hora para alumno y libro válidos y lo 
    agrega al archivo JSON correspondiente.

    Retorno:
        None: Se crea el registro, se guarda sobre el archivo JSON y devuelve None. Si el usuario 
        ingresa '0' para volver o se captura una excepción se informa y devuelve None.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        # Pide y valida el id del alumno
        idAlumno = pedirYValidarId(alumnos, "alumno", True, "id")
        if idAlumno is None:
            return None

        # Pide y valida el id del libro
        idLibro = pedirYValidarId(libros, "libro", True, "id")
        if idLibro is None:
            return None

        # Genera el id del préstamo y la fecha de inicio
        idPrestamo = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        fechaInicio = datetime.now()

        # Completa los campos del nuevo registro de préstamo
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
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al registrar préstamo: {e}")
        return None

def finalizarPrestamo():
    """
    Finaliza un préstamo, registra la devolución, calcula el monto y actualiza infracciones. 
    Guarda los datos actualizados en los archivos JSON correspondientes.

    Retorno:
        None: Se modifican los registros, se guardan sobre los archivos JSON, se informa y 
        devuelve None. Si el usuario ingresa '0' para volver o se captura una excepción se informa 
        y devuelve None.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        # Pide y valida el id del préstamo
        idPrestamo = pedirYValidarId(prestamos, "préstamo", True, "idPrestamo")
        if idPrestamo is None:
            return None

        prestamo = prestamos[idPrestamo]

        # Convierte la fecha de inicio al formato "YYYY-MM-DD"
        fechaInicio = datetime.strptime(prestamo["fechaInicio"], "%Y-%m-%d")

        # Asigna la fecha de finalización al día y horario actual
        fechaFin = datetime.now()

        # Calcula los días de préstamo (1 por defecto)
        diasPrestamo = (fechaFin - fechaInicio).days
        if diasPrestamo == 0:
            diasPrestamo = 1

        # Calula el monto total (costo diario del libro * días de préstamo)
        idLibro = prestamo["idLibro"]
        costoDiario = libros[idLibro]["costoGarantia"]
        montoTotal = costoDiario * diasPrestamo

        # Asigna los valores de fecha de finalización y cantidad de días al registro del préstamo
        prestamo["fechaFinalizacion"] = fechaFin.strftime("%Y-%m-%d")
        prestamo["cantidadDias"] = diasPrestamo

        # Pregunta y valida si la devolución fue correcta
        devolucion = validarDato(input("¿La devolución es correcta? (s = sí / n = no): ").strip().lower(), "respuesta", "string")
        while devolucion not in ("s", "n"):
            print("Error. Ingrese 's' o 'n'.")
            devolucion = validarDato(input("¿La devolución es correcta? (s = sí / n = no): ").strip().lower(), "respuesta", "string")

        devolucionCorrecta = devolucion == "s"

        # Si la devolución no fue correcta suma una infracción al alumno
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

        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al finalizar préstamo: {e}")
        return None

def imprimirResumenMensual():
    """
    Solicita un año y mes e imprime por consola el listado de préstamos iniciados en ese periodo.

    Retorno:
        None: Se imprime el resumen y devuelve None. Si se captura una excepción se informa y 
        devuelve None.
    """
    try:
        alumnos = cargarArchivo(ALUMNOS_ARCHIVO)
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        # Pide y valida el año y mes a imprimir
        anio = int(validarDato(input("Ingrese el año (formato AAAA): "),"año", "numero"))
        mes = int(validarDato(input("Ingrese el mes (1-12): "), "mes", "numero"))

        # Prepara encabezados
        salida = []
        salida.append(f"Listado de reservas del mes {mes}/{anio}")
        salida.append(f"{'Fecha/Hora':<35}{'Alumno':<35}{'Libro':<35}")
        salida.append("-" * 105)

        # Filtra y formatea los préstamos
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

        # Imprime los préstamos formateados
        print("\n".join(salida))
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al imprimir resumen mensual: {e}")
        return None

def imprimirResumenAnualPorLibroCantidad():
    """
    Solicita un año e imprime por consola cuántos préstamos tuvo cada libro mes a mes.

    Retorno:
        None: Se imprime el resumen y devuelve None. Si se captura una excepción se informa y 
        devuelve None.
    """
    try:
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        # Pide y valida el año a imprimir
        anio = int(validarDato(input("Ingrese el año (formato AAAA): "),"año", "numero"))

        # Crea un diccionario con una lista de 12 ceros (uno por cada mes) para cada libro
        resumen = {idLibro: [0] * 12 for idLibro in libros.keys()}

        # Cuenta los préstamos por mes, filtrados por año
        for prestamo in prestamos.values():
            fecha = prestamo["fechaInicio"]
            if fecha.startswith(str(anio)):
                mes = int(fecha[5:7])  # Extrae el mes
                libro = prestamo["idLibro"]
                if libro in resumen:
                    resumen[libro][mes - 1] += 1
        
        # Genera el resumen por título de libro
        resumenPorTitulo = {
            libros.get(idLibro, {}).get("titulo", f"Libro {idLibro}"): valores
            for idLibro, valores in resumen.items()
        }

        # Formatea el resumen para generar la tabla con cantidades y la imprime
        informe = formatearInformes(resumenPorTitulo, anio, "Resumen Anual de Reservas por Libro (Cantidades)")
        print(informe)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al imprimir resumen anual de reservas por libro: {e}")
        return None

def imprimirResumenAnualPorLibroPesos():
    """
    Solicita un año e imprime por consola el resumen anual del dinero en garantía movido por libro.

    Retorno:
        None: Se imprime el resumen y devuelve None. Si se captura una excepción se informa y 
        devuelve None.
    """
    try:
        libros = cargarArchivo(LIBROS_ARCHIVO)
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)

        # Pide y valida el año a imprimir
        anio = int(validarDato(input("Ingrese el año (formato AAAA): "),"año", "numero"))

        resumen = {}

        # Construye el resumen de montos
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

        # Formatea el resumen para generar la tabla en pesos y la imprime
        informe = formatearInformes(resumen, anio, "Resumen Anual de Reservas por Libro (Pesos)", _esDinero=True)
        print(informe)
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al imprimir resumen anual por libro: {e}")
        return None

def imprimirResumenAnualDevolucionesIncorrectas():
    """
    Solicita un año e imprime por consola el resumen anual de devoluciones incorrectas por mes.

    Retorno:
        None: Se imprime el resumen y devuelve None. Si se captura una excepción se informa y 
        devuelve None.
    """
    try:
        prestamos = cargarArchivo(PRESTAMOS_ARCHIVO)
        
        # Pide y valida el año a imprimir
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

        # Para cada mes (1–12), cuenta los préstamos cuyo estadoDevolucionCorrecto sea False (por defecto True si falta)
        incorrectasPorMes = []
        for mes in range(1, 13):
            incorrectas = 0
            for prestamo in prestamos.values():
                fecha = prestamo["fechaInicio"]
                if fecha.startswith(f"{anio}-{str(mes).zfill(2)}"):
                    if not prestamo.get("estadoDevolucionCorrecto", True):
                        incorrectas += 1
            incorrectasPorMes.append(incorrectas)

        # Construye la tabla 'salida' manualmente
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

        # Imprime la tabla
        print("\n".join(salida))
        return None
    except (FileNotFoundError, OSError) as detalle:
        print("Error al intentar abrir archivo(s):", detalle)
        return None
    except Exception as e:
        print(f"Error inesperado al imprimir resumen anual de devoluciones incorrectas: {e}")
        return None

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
