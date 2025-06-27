"""
-----------------------------------------------------------------------------------------------
Título: DESARROLLO PYTHON POR EQUIPO - VERSIÓN 1.0 - ENTREGA 1
Fecha: 02/06/2025
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


# ----------------------------------------------------------------------------------------------
# FUNCIONES
# ----------------------------------------------------------------------------------------------
def ingresarAlumno(_alumnos):
    """
    Registra un nuevo alumno en el diccionario de alumnos.

    Parámetros:
        _alumnos (dict): Diccionario de alumnos (clave: idAlumno).

    Retorno:
        _alumnos (dict): Diccionario de alumnos actualizado con la nueva entrada.
    """
    idAlumno = input("Ingresá el ID del alumno: ").strip()
    if idAlumno in _alumnos:
        print("Error: el ID del alumno ya existe")
        return _alumnos

    _alumnos[idAlumno] = {
        "activo": True,
        "nombre": input("Nombre: ").strip(),
        "apellido": input("Apellido: ").strip(),
        "direccion": input("Dirección: ").strip(),
        "email": input("Email: ").strip(),
        "telefono": {
            "celular": int(input("Teléfono celular: ")),
            "fijo": int(input("Teléfono fijo: ")),
        },
        "infracciones": 0,
    }
    print(f"Alumno {idAlumno} registrado correctamente.")
    return _alumnos


def modificarAlumno(_alumnos):
    """
    Modifica los datos básicos de un alumno existente.

    Parámetros:
        _alumnos (dict): Diccionario de alumnos (clave: idAlumno).

    Retorno:
        _alumnos (dict): Diccionario de alumnos con los cambios aplicados
        (o sin cambios si el ID no se encontró).
    """
    idAlumno = input("ID del alumno a modificar: ")
    if idAlumno not in _alumnos:
        print("Error: el alumno no fue encontrado")
        return _alumnos

    print("\nCampos disponibles para modificar: nombre, apellido, email, direccion")
    campo = input("Ingresá el campo a modificar: ")
    if campo in _alumnos[idAlumno]:
        _alumnos[idAlumno][campo] = input(f"Nuevo valor para {campo}: ")
        print(f"Modificación del campo {campo} exitosa")
    else:
        print("Campo invalido")
    return _alumnos


def inactivarAlumno(_alumnos):
    """
    Inactiva (baja lógica) a un alumno a partir de su ID.

    Parámetros:
        _alumnos (dict): Diccionario de alumnos (clave: idAlumno).

    Retorno:
        _alumnos (dict): Diccionario de alumnos con el estado del alumno
        actualizado a inactivo si el ID existe.
    """
    idAlumno = input("ID del alumno a inactivar: ")
    if idAlumno in _alumnos:
        _alumnos[idAlumno]["activo"] = False
        print(f"Alumno {idAlumno} inactivado")
    else:
        print("Error: el ID del alumno no existe")
    return _alumnos


def listarAlumnos(_alumnos):
    """
    Muestra el listado de alumnos activos y sus datos.

    Parámetros:
        _alumnos (dict): Diccionario de alumnos (clave: idAlumno).

    Retorno:
        _alumnos (dict): El mismo diccionario recibido, sin modificar.
    """
    if not _alumnos:
        print("No hay alumnos registrados.")
        return _alumnos

    print("\nLISTADO DE ALUMNOS ACTIVOS")
    print("-" * 50)

    alumnosActivos = 0

    for idAlumno, datos in _alumnos.items():
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

    return _alumnos


def ingresarLibro(_libros):
    """
    Registra un nuevo libro en el diccionario de libros.

    Parámetros:
        _libros (dict): Diccionario de libros (clave: idLibro).

    Retorno:
        _libros (dict): Diccionario de libros actualizado con la nueva entrada.
    """
    idlibro = input("ID del libro: ")
    if idlibro in _libros:
        print("El libro ya existe.")
        return _libros
    titulo = input("Título: ")

    autores = input("Autores (separados por coma, máx 3): ").strip()
    autoresCortados = [parte.strip() for parte in autores.split(",") if parte.strip()]
    autoresRellenados = (autoresCortados + ["", "", ""])[:3]
    dictAutores = {
        "autor1": autoresRellenados[0],
        "autor2": autoresRellenados[1],
        "autor3": autoresRellenados[2],
    }

    genero = input("Genero: ")
    editorial = input("Editorial: ")
    costo = int(input("Costo de garantía ($): "))
    _libros[idlibro] = {
        "titulo": titulo,
        "autores": dictAutores,
        "activo": True,
        "genero": genero,
        "editorial": editorial,
        "costoGarantia": costo,
    }
    print("Libro ingresado correctamente.")
    return _libros


def modificarLibro(_libros):
    """
    Modifica los datos básicos de un libro existente.

    Parámetros:
        _libros (dict): Diccionario de libros (clave: idLibro).

    Retorno:
        _libros (dict): Diccionario de libros con los cambios aplicados
        (o sin cambios si el ID no se encontró).
    """
    idlibro = input("ID del libro a modificar: ")
    if idlibro not in _libros:
        print("Libro no encontrado.")
        return _libros

    titulo = input("Nuevo título: ")

    autores = input("Nuevo/s autor/es (separados por coma, máx 3): ").strip()
    autoresCortados = [parte.strip() for parte in autores.split(",") if parte.strip()]
    autoresRellenados = (autoresCortados + ["", "", ""])[:3]
    dictAutores = {
        "autor1": autoresRellenados[0],
        "autor2": autoresRellenados[1],
        "autor3": autoresRellenados[2],
    }

    genero = input("Nuevo genero: ")
    editorial = input("Nueva editorial: ")
    costo = int(input("Nuevo costo de garantía ($): "))

    _libros[idlibro]["titulo"] = titulo
    _libros[idlibro]["autores"] = dictAutores
    _libros[idlibro]["genero"] = genero
    _libros[idlibro]["editorial"] = editorial
    _libros[idlibro]["costoGarantia"] = costo

    print("Libro modificado correctamente.")
    return _libros


def listarLibros(_libros):
    """
    Muestra el listado completo de libros y sus datos.

    Parámetros:
        _libros (dict): Diccionario de libros (clave: idLibro).

    Retorno:
        _libros (dict): El mismo diccionario recibido, sin modificar.
    """
    if not _libros:
        print("No hay libros registrados.")
        return _libros

    librosActivos = 0

    print("\nLISTADO DE LIBROS")
    print("-" * 50)

    for idLibro, datos in _libros.items():
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

    return _libros


def marcarInactivo(_libros):
    """
    Marca un libro como inactivo (baja lógica) a partir de su ID.

    Parámetros:
        _libros (dict): Diccionario de libros (clave: idLibro).

    Retorno:
        _libros (dict): Diccionario de libros con el estado del libro
        actualizado a inactivo si el ID existe.
    """
    idlibro = input("ID del libro a marcar como inactivo: ")
    if idlibro in _libros:
        _libros[idlibro]["activo"] = False
        print("Libro marcado como inactivo.")
    else:
        print("Libro no encontrado.")
    return _libros


def registrarPrestamo(_alumnos, _libros, _prestamos):
    """
    Registra un nuevo préstamo y lo agrega al diccionario de préstamos.

    Parámetros:
        _alumnos (dict): Diccionario de alumnos (clave: idAlumno, valor: datos del alumno).
        _libros (dict): Diccionario de libros  (clave: idLibro,  valor: datos del libro).
        _prestamos (dict): Diccionario de préstamos (clave: idPrestamo).

    Retorno:
        _prestamos (dict): Diccionario de préstamos actualizado con la nueva operación.
    """
    idAlumno = input("Ingrese el ID del alumno (ej. A1003): ").strip()
    idLibro = input("Ingrese el ID del libro  (ej. L1007): ").strip()

    if idAlumno not in _alumnos or not _alumnos[idAlumno]["activo"]:
        print("El alumno no existe o está inactivo.")
        return _prestamos

    if idLibro not in _libros or not _libros[idLibro]["activo"]:
        print("El libro no existe o no está disponible.")
        return _prestamos

    idPrestamo = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
    fechaInicio = datetime.now()

    _prestamos[idPrestamo] = {
        "idPrestamo": idPrestamo,
        "idAlumno": idAlumno,
        "idLibro": idLibro,
        "cantidadDias": 0,
        "fechaInicio": fechaInicio.strftime("%Y-%m-%d"),
        "fechaFinalizacion": "",
        "estadoDevolucionCorrecto": False,
    }

    print(f"Préstamo registrado con ID: {idPrestamo}")

    return _prestamos


def finalizarPrestamo(_alumnos, _libros, _prestamos):
    """
    Finaliza un préstamo, registra la devolución, calcula el monto y actualiza infracciones.

    Parámetros:
        _alumnos (dict): Diccionario de alumnos (clave: idAlumno, valor: datos del alumno).
        _libros (dict): Diccionario de libros  (clave: idLibro,  valor: datos del libro).
        _prestamos (dict): Diccionario de préstamos (clave: idPrestamo).

    Retorno:
        _prestamos (dict): Diccionario de préstamos con los datos del préstamo cerrado.
        _alumnos (dict): Diccionario de alumnos (modificado si se suma infracción).
    """
    idPrestamo = input(
        "Ingrese el ID del préstamo (0 para volver al menú anterior): "
    ).strip()

    while idPrestamo not in _prestamos and idPrestamo != "0":
        print("El préstamo no existe.")
        reintento = (
            input("Ingrese 'r' para reintentar o '0' para volver: ").strip().lower()
        )
        if reintento == "0":
            return _prestamos, _alumnos
        idPrestamo = input("Ingrese nuevamente el ID del préstamo: ").strip()

    if idPrestamo == "0":
        return _prestamos, _alumnos

    prestamo = _prestamos[idPrestamo]

    fechaInicio = datetime.strptime(prestamo["fechaInicio"], "%Y-%m-%d")
    fechaFin = datetime.now()

    diasPrestamo = (fechaFin - fechaInicio).days
    if diasPrestamo == 0:
        diasPrestamo = 1

    idLibro = prestamo["idLibro"]

    costoDiario = _libros[idLibro]["costoGarantia"]
    montoTotal = costoDiario * diasPrestamo

    prestamo["fechaFinalizacion"] = fechaFin.strftime("%Y-%m-%d")
    prestamo["cantidadDias"] = diasPrestamo

    devolucion = (
        input("¿La devolución es correcta? (s = sí / n = no): ").strip().lower()
    )

    while devolucion not in ("s", "n"):
        print("Error. Ingrese 's' o 'n'.")
        devolucion = (
            input("¿La devolución es correcta? (s = sí / n = no): ").strip().lower()
        )

    devolucionCorrecta = devolucion == "s"

    if not devolucionCorrecta:
        idAlumno = prestamo["idAlumno"]
        _alumnos[idAlumno]["infracciones"] += 1
        print("Se añadió 1 infracción al alumno.")

    print(f"\nPréstamo finalizado correctamente.")
    print(f"Días prestados: {diasPrestamo}")
    print(f"Costo por día : {costoDiario}")
    print(f"Total a pagar : {montoTotal}\n")

    return _prestamos, _alumnos


def resumenMensual(_prestamos, _alumnos, _libros, _anio, _mes):
    """
    Genera un resumen de los préstamos realizados en un mes específico.

    Parámetros:
        _prestamos (dict): Diccionario de préstamos (clave: idPrestamo, valor: datos del préstamo).
        _alumnos (dict): Diccionario de alumnos (clave: idAlumno, valor: datos del alumno).
        _libros (dict): Diccionario de libros  (clave: idLibro,  valor: datos del libro).
        _anio (int): Año del cual se desea obtener el resumen.
        _mes (int): Mes (1 a 12) del cual se desea obtener el resumen.

    Retorno:
        str: texto formateado con el resumen mensual de préstamos realizados en un mes.
    """
    salida = []
    salida.append(f"Listado de reservas del mes {_mes}/{_anio}")
    salida.append(f"{'Fecha/Hora':<35}{'Alumno':<35}{'Libro':<35}")
    salida.append("-" * 105)

    for clave, prestamo in _prestamos.items():
        fecha = prestamo["fechaInicio"]
        if fecha.startswith(f"{_anio}-{str(_mes).zfill(2)}"):
            fechaHora = clave
            idAlumno = prestamo["idAlumno"]
            nombreAlumno = _alumnos.get(idAlumno, {}).get("nombre", f"Alumno {idAlumno}")
            idLibro = prestamo["idLibro"]
            tituloLibro = _libros.get(idLibro, {}).get("titulo", f"Libro {idLibro}")
            salida.append(f"{fechaHora:<35}{nombreAlumno:<35}{tituloLibro:<35}")

    return "\n".join(salida)


def resumenAnualPorLibroCantidad(_prestamos, _anio, _libros):
    """
    Genera un resumen anual con la cantidad de préstamos por libro.

    Parámetros:
        _prestamos (dict): Diccionario de préstamos (clave: idPrestamo, valor: datos del préstamo).
        _anio (int): Año para el cual se desea generar el resumen.
        _libros (dict): Diccionario de préstamos (clave: idLibro, valor: datos del libro).

    Retorno:
        str: texto formateado con las reservas mensuales de libros.
    """
    resumen = {idLibro: [0] * 12 for idLibro in _libros.keys()}

    for prestamo in _prestamos.values():
        fecha = prestamo["fechaInicio"]
        if fecha.startswith(str(_anio)):
            mes = int(fecha[5:7])
            libro = prestamo["idLibro"]
            if libro in resumen:
                resumen[libro][mes - 1] += 1

    resumenPorTitulo = {
        _libros.get(idLibro, {}).get("titulo", f"Libro {idLibro}"): valores
        for idLibro, valores in resumen.items()
    }

    return formateoInformes(
        resumenPorTitulo,
        _anio,
        "Resumen Anual de Reservas por Libro (Cantidades)"
    )


def resumenAnualPorLibroPesos(_prestamos, _libros, _anio):
    """
    Genera un resumen anual del dinero en garantía movido por libro.

    Parámetros:
        _prestamos (dict): Diccionario de préstamos (clave: idPrestamo, valor: datos del préstamo).
        _libros (dict): Diccionario con información de libros (clave: idLibro, valor: datos del libro).
        _anio (int): Año para el cual se desea generar el resumen.

    Retorno:
        str: texto formateado con el monto acumulado mensualmente por libro.
    """
    resumen = {}

    for prestamo in _prestamos.values():
        fecha = prestamo["fechaInicio"]
        if fecha.startswith(str(_anio)):
            mes = int(fecha[5:7]) - 1
            idLibro = prestamo["idLibro"]
            nombreLibro = _libros.get(idLibro, {}).get("titulo", f"Libro {idLibro}")
            costo = _libros.get(idLibro, {}).get("costoGarantia", 0)

            if nombreLibro not in resumen:
                resumen[nombreLibro] = [0] * 12
            resumen[nombreLibro][mes] += costo

    return formateoInformes(
        resumen,
        _anio,
        "Resumen Anual de Reservas por Libro (Pesos)",
        _esDinero=True
    )

def resumenAnualDevolucionesIncorrectas(_prestamos, _anio):
    """
    Genera el resumen anual de devoluciones incorrectas por mes.

    Parámetros:
        prestamos (dict): diccionario de préstamos.
        anio (int): año a filtrar.

    Retorno:
        str: texto formateado con devoluciones incorrectas por mes.
    """
    meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
             "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]

    incorrectasPorMes = []
    for mes in range(1, 13):
        count = 0
        for prestamo in _prestamos.values():
            fecha = prestamo["fechaInicio"]
            if fecha.startswith(f"{_anio}-{str(mes).zfill(2)}"):
                if not prestamo.get("estadoDevolucionCorrecto", True):
                    count += 1
        incorrectasPorMes.append(count)

    anchoTotal = 160
    salida = []
    salida.append("-" * anchoTotal)
    salida.append("Resumen anual de reservas con devolución incorrecta".center(anchoTotal))
    salida.append("-" * anchoTotal)

    encabezado = "MESES".ljust(15)
    for m in meses:
        encabezado += f"{m}.{str(_anio)[-2:]}".center(12)
    salida.append(encabezado)

    salida.append("-" * anchoTotal)

    fila = "Devol.Incorrect".ljust(15)
    for val in incorrectasPorMes:
        fila += f"{val}".center(12)
    salida.append(fila)

    salida.append("-" * anchoTotal)

    return "\n".join(salida)


def formateoInformes(_diccionario, _anio, _titulo, _esDinero=False):
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

    _anio = int(_anio)
    anchoNombre = 50
    anchoMes = 10
    totalColumnas = anchoNombre + (12 * anchoMes)

    meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
             "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]

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


# ----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
# ----------------------------------------------------------------------------------------------
def main():
    # -------------------------------------------------
    # Inicialización de variables
    # ----------------------------------------------------------------------------------------------
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
                    alumnos = ingresarAlumno(alumnos)

                elif opcionSubmenu == "2":  # Opción 2 del submenú
                    alumnos = modificarAlumno(alumnos)

                elif opcionSubmenu == "3":  # Opción 3 del submenú
                    alumnos = inactivarAlumno(alumnos)

                elif opcionSubmenu == "4":  # Opción 4 del submenú
                    listarAlumnos(alumnos)

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
                    libros = ingresarLibro(libros)

                elif opcionSubmenu == "2":  # Opción 2 del submenú
                    libros = modificarLibro(libros)

                elif opcionSubmenu == "3":  # Opción 3 del submenú
                    libros = marcarInactivo(libros)

                elif opcionSubmenu == "4":  # Opción 4 del submenú
                    listarLibros(libros)

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
                    prestamos = registrarPrestamo(alumnos, libros, prestamos)

                elif opcionSubmenu == "2":  # Opción 2 del submenú
                    prestamos, alumnos = finalizarPrestamo(alumnos, libros, prestamos)

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
                    anio = int(input("Ingrese el año (formato AAAA): "))
                    mes = int(input("Ingrese el mes (1-12): "))
                    print(resumenMensual(prestamos, alumnos, libros, anio, mes))

                elif opcionSubmenu == "2":  # Opción 2 del submenú
                    anio = input("Ingrese el año (AAAA): ")
                    print(resumenAnualPorLibroCantidad(prestamos, anio, libros))

                elif opcionSubmenu == "3":  # Opción 3 del submenú
                    anio = int(input("Ingrese el año (formato AAAA): "))
                    print(resumenAnualPorLibroPesos(prestamos, libros, anio))

                elif opcionSubmenu == "4":  # Opción 4 del submenú
                    anio = int(input("Ingrese el año (formato AAAA): "))
                    print(resumenAnualDevolucionesIncorrectas(prestamos, anio))

                    input("\nPresione ENTER para volver al menú.")
                    print("\n\n")

        if (
            opcionSubmenu != "0"
        ):  # Pausa entre opciones. No la realiza si se vuelve de un submenú
            input("\nPresione ENTER para volver al menú.")
            print("\n\n")


# Punto de entrada al programa
main()
