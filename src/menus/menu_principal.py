"""Módulo para el menú principal y control de navegación de EcoTech."""
import getpass
import sys

from persistencia.conexion import motor_actual
from persistencia.crear_bd import crear_tablas
from persistencia.semilla_bd import cargar_semilla
from servicios.autenticacion import autenticar
from servicios.gestion_empleados import listar_todos_los_empleados
from servicios.indicadores import consultar_indicador_dolar, obtener_historial_local
from servicios.mi_cuenta import mis_registros_de_tiempo, ver_mi_ficha

# Importar submenús existentes del proyecto
from .menu_departamento import menu_departamentos
from .menu_empleado import menu_empleados
from .menu_proyecto import menu_proyectos
from .menu_registro_tiempo import menu_registros


def solicitar_login() -> dict | None:
    """Solicita credenciales de acceso al usuario."""
    print("\n" + "=" * 40)
    print("      INICIO DE SESIÓN - ECOTECH      ")
    print("=" * 40)
    usuario = input("Usuario: ").strip()
    clave = getpass.getpass("Contraseña: ").strip()

    sesion = autenticar(usuario, clave)
    if sesion is None:
        print("\n❌ Error: Credenciales incorrectas.")
        return None

    print(f"\n✅ Bienvenid@, {sesion['nombre_usuario']}! (Rol: {sesion['rol'].upper()})")
    return sesion


def menu_privado(sesion: dict) -> bool:
    """
    Despliega las opciones del sistema según el rol del usuario autenticado.
    Retorna True para cerrar sesión y volver al login, o False para salir.
    """
    while True:
        print("\n" + "=" * 45)
        print(f" ECOTECH - MENÚ ({sesion['nombre_usuario'].upper()} | {sesion['rol'].upper()})")
        print("=" * 45)
        print("1. Mi Ficha (Datos propios)")
        print("2. Mis Registros de Tiempo")
        print("3. Consultar Indicador Económico (API Dólar)")
        print("4. Ver Historial de Indicadores (BD Local)")

        # Opciones administrativas avanzadas (visibles solo para admin)
        if sesion["rol"] == "admin":
            print("-" * 45)
            print("5. [ADMIN] Gestión de Empleados")
            print("6. [ADMIN] Gestión de Departamentos")
            print("7. [ADMIN] Gestión de Proyectos")
            print("8. [ADMIN] Gestión General de Tiempos")

        print("-" * 45)
        print("9. Cerrar Sesión")
        print("0. Salir de la Aplicación")
        print("=" * 45)

        opcion = input("Seleccione una opción: ").strip()

        # Acciones para todos los usuarios (Datos propios y API)
        if opcion == "1":
            try:
                emp = ver_mi_ficha(sesion)
                print(f"\n📌 FICHA DE EMPLEADO:\n  {emp}")
            except Exception as err:
                print(f"\n❌ Error: {err}")

        elif opcion == "2":
            try:
                registros = mis_registros_de_tiempo(sesion)
                print(f"\n⏱️ MIS REGISTROS DE TIEMPO ({len(registros)}):")
                for r in registros:
                    print(f"  - {r}")
            except Exception as err:
                print(f"\n❌ Error: {err}")

        elif opcion == "3":
            print("\nConsultando servicio externo API...")
            res = consultar_indicador_dolar(sesion)
            if res["exito"]:
                print(f"\n✅ {res['indicador']}")
                print(f"   Origen: {res['origen']}")
            else:
                print(f"\n❌ {res['mensaje']}")

        elif opcion == "4":
            try:
                historial = obtener_historial_local(sesion)
                print(f"\n📜 HISTORIAL EN BD LOCAL ({len(historial)} registros):")
                for h in historial:
                    print(f"  - {h}")
            except Exception as err:
                print(f"\n❌ Error: {err}")

        # Acciones protegidas para Administrador
        elif opcion == "5" and sesion["rol"] == "admin":
            menu_empleados()

        elif opcion == "6" and sesion["rol"] == "admin":
            menu_departamentos()

        elif opcion == "7" and sesion["rol"] == "admin":
            menu_proyectos()

        elif opcion == "8" and sesion["rol"] == "admin":
            menu_registros()

        elif opcion == "9":
            print("\n🔒 Sesión cerrada correctamente.")
            return True  # Cierra sesión y retorna a la pantalla de login

        elif opcion == "0":
            print("\n👋 ¡Hasta luego!")
            return False  # Finaliza la aplicación

        else:
            print("\n⚠️ Opción no válida o no autorizada para su rol.")


def menu_principal():
    """Inicializa la base de datos, ejecuta la semilla y controla el bucle de sesión."""
    # 1. Crear tablas y poblar datos iniciales
    crear_tablas()
    cargar_semilla()

    try:
        print(f"\nBase de datos conectada exitosamente ({motor_actual().upper()})")
    except Exception as exc:
        print(f"No se pudo inicializar la base de datos: {exc}")
        if motor_actual() == "mysql":
            print("Revisa que MySQL/WampServer esté iniciado y que las credenciales de .env sean correctas.")
        return

    # 2. Bucle de autenticación
    while True:
        sesion = solicitar_login()
        if sesion is None:
            reintentar = input("\n¿Desea reintentar el ingreso? (S/N): ").strip().upper()
            if reintentar != "S":
                print("\n👋 ¡Hasta luego!")
                sys.exit(0)
            continue

        continuar = menu_privado(sesion)
        if not continuar:
            sys.exit(0)