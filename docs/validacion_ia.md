# Validación del uso de Inteligencia Artificial

## 1. Uso de la IA

Utilizamos la inteligencia artificial como apoyo para resolver dudas puntuales, revisar la organización de algunos archivos y detectar aspectos que convenía mejorarla herramienta no reemplaza la revisión del código ni las pruebas del programa

## 2. Criterios de revisión

Revisamos que las clases de dominio estuvieran separadas de la persistencia y de los menús, que las consultas enviaran los datos mediante parámetros, que se mantuvieran las relaciones entre las tablas y que las contraseñas no se guardaran como texto plano.

## 3. Cambios realizados después de la revisión

- Separaramos las opciones de consola en archivos dentro de src/menus/ para mantener main.py como punto de entrada y coordinación
- Añadímos la selección del motor de base de datos mediante DB_ENGINE en el archivo .env.
- Mantuvimos SQLite como configuración inicial y añadí la opción de conexión a MySQL con mysql-connector-python
- Añadímos la creación de tablas para ambos motores y un script para crear la base de datos MySQL.
- Incorporamos opciones de búsqueda y actualización en el menú de registros de tiempo.

## 4. Pruebas realizadas durante la revisión

- La compilación de los archivos Python terminó sin errores.
- Las seis pruebas automáticas de dominio terminaron con resultado OK.
- Se realizó una prueba de integración con SQLite para crear, consultar, actualizar y eliminar datos relacionados de empleados, departamentos, proyectos y registros de tiempo.
- Se inició main.py con SQLite y se comprobó que muestra el menú principal y permite salir correctamente.

La conexión a un servidor MySQL real  se verificó cambiando y editando el contenido de .env y conectandolo a wampserver

## 5. Decisiones tomadas

Se mantuvo SQLite como opción predeterminada porque permite ejecutar el sistema localmente sin configurar un servidor se añadió la compatibilidad de código con MySQL para poder seleccionarlo mediante .env cuando exista una instancia disponible

Las sugerencias se utilizaron como apoyo y se revisaron mediante compilación y pruebas
