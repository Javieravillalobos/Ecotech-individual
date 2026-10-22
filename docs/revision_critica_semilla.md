# Revisión crítica: semilla de datos EcoTech

## Objetivo
Complementar `crear_bd.py` con `semilla_bd.py` para disponer de datos de prueba relacionados y poder ejecutar el proceso más de una vez sin duplicar los datos de demostración.

## Fuente y material revisado
- Código del proyecto EcoTech entregado: `src/persistencia/crear_bd.py`, los DAO de departamento, empleado, proyecto y registro de tiempo, las clases de dominio y el esquema SQL.
- Instrucción de la actividad: completar departamentos, empleados, gerentes y proyectos; crear `RegistroTiempo` con referencias válidas; ejecutar dos veces y comparar cantidades.
- Propuesta asistida por IA: crear una semilla idempotente que use los DAO disponibles, valide las relaciones antes de registrar horas y muestre conteos al terminar.

## Propuesta aplicada
Se agregó `src/persistencia/semilla_bd.py` sin reemplazar ni reorganizar la estructura del proyecto. El script:
1. Reutiliza `DepartamentoDAO`, `EmpleadoDAO`, `ProyectoDAO` y `RegistroTiempoDAO`.
2. Crea departamentos de ejemplo.
3. Crea empleados de demostración y marca dos como `Gerente` mediante el campo `rol`, porque el esquema actual no tiene una tabla ni una relación específica de gerente por departamento.
4. Crea proyectos y asigna empleados existentes a ellos.
5. Inserta registros de tiempo solo cuando encuentra el empleado y el proyecto correspondientes.
6. Comprueba si ya existen los registros de demostración antes de insertarlos otra vez y muestra los totales de las tablas.

## Revisión crítica y decisión propia
La IA ayudó a proponer la estructura de la semilla, pero no tomé la propuesta como correcta automáticamente. La contrasté con las columnas reales del esquema y los métodos que efectivamente existen en los DAO. Por ejemplo, el proyecto guarda el rol como texto y no cuenta con una entidad Gerente separada; por eso la semilla usa `rol = 'Gerente'` y no inventa una tabla nueva. También se respetaron las claves foráneas de `registro_tiempo`: primero se crean los departamentos, empleados y proyectos, y después se registran las horas.

La decisión fue mantener la arquitectura actual y agregar un archivo nuevo en persistencia, en vez de modificar el menú o duplicar las operaciones SQL que ya están implementadas en los DAO. La idempotencia se resolvió comprobando nombres de departamentos/proyectos, username/correo, asignaciones y la combinación de datos del registro de tiempo. Esto permite repetir la ejecución sin volver a insertar los mismos datos de demostración.

Una limitación importante es que el modelo actual no relaciona formalmente un gerente con un departamento. El rol indica que una persona es gerente, pero no garantiza que sea el gerente de un departamento concreto. Para representar esa regla de negocio de forma completa se necesitaría una relación adicional en el modelo y en la base de datos; no la agregué porque la instrucción pide mantener la estructura existente.

Otra limitación es que los DAO de empleados no ofrecen una búsqueda específica por username o correo, por lo que la semilla consulta esas columnas para evitar duplicados y luego usa los DAO para las inserciones. A futuro sería mejor incorporar esos métodos al DAO y mantener toda la lógica de persistencia encapsulada allí. La detección de duplicados de registros de tiempo usa una combinación de empleado, proyecto, fecha, horas y descripción; si se quisieran permitir dos tareas idénticas el mismo día, habría que definir una regla de negocio más precisa.

Las credenciales incluidas son únicamente de demostración y no deben reutilizarse en producción. La contraseña se entrega al modelo `Empleado`, que ya genera un hash PBKDF2 antes de persistirlo. Antes de presentar la entrega, se deben ejecutar los dos ensayos en la misma base de datos y registrar las salidas reales; no se deben afirmar resultados que no se hayan comprobado.

## Instrucciones para ejecutar
Desde una terminal, ubicarse en la carpeta `src` del proyecto. Configurar `.env` para usar la misma base de datos en ambas ejecuciones.

```powershell
# 1. Crear las tablas (no borra las tablas existentes)
python -m persistencia.crear_bd

# 2. Primera ejecución de la semilla
python -m persistencia.semilla_bd

# 3. Segunda ejecución, sin borrar ni recrear la base
python -m persistencia.semilla_bd
```

## Comparación esperada
En una base vacía, la primera ejecución inserta los datos de demostración. La segunda debe mostrar `0` empleados, proyectos, asignaciones y registros de tiempo insertados en esa ejecución, y los totales deben mantenerse iguales. Si la base ya tenía datos, los totales iniciales pueden ser mayores; lo importante es comparar la salida real de ambas ejecuciones y confirmar que la segunda no duplica los datos de la semilla.

| Entidad | Cantidad de demostración prevista |
|---|---:|
| Departamentos | 3 |
| Empleados (incluye 2 gerentes por rol) | 4 |
| Proyectos | 2 |
| Asignaciones proyecto-empleado | 4 |
| Registros de tiempo | 4 |

Las cantidades anteriores describen los datos de demostración, no necesariamente los totales de una base que ya contenga información.

## Evidencia para completar después de ejecutar
- Primera ejecución: pegar aquí la salida real de la consola.
- Segunda ejecución: pegar aquí la salida real de la consola.
- Comparación: indicar los totales antes/después y confirmar si permanecieron iguales.

## Resultados comprobados en una base SQLite de prueba limpia

Se ejecutó `crear_bd` y luego `semilla_bd` dos veces usando una base temporal independiente del archivo entregado.

**Ejecución 1**
- Departamentos totales: 3
- Usuarios totales: 4
- Empleados totales: 4
- Proyectos totales: 2
- Asignaciones proyecto-empleado: 4
- Registros de tiempo totales: 4
- Insertados en esta ejecución: 4 empleados, 2 proyectos, 4 asignaciones y 4 registros de tiempo.

**Ejecución 2**
- Departamentos totales: 3
- Usuarios totales: 4
- Empleados totales: 4
- Proyectos totales: 2
- Asignaciones proyecto-empleado: 4
- Registros de tiempo totales: 4
- Insertados en esta ejecución: 0 empleados, 0 proyectos, 0 asignaciones y 0 registros de tiempo.

**Conclusión de la prueba:** en SQLite, las cantidades se mantuvieron iguales entre las dos ejecuciones y la segunda ejecución no insertó nuevamente los datos de demostración. También se ejecutaron las pruebas automáticas existentes: 8 pruebas finalizaron correctamente. La compatibilidad con MariaDB/MySQL debe verificarse en un servidor real antes de afirmar que se probó ese motor.
