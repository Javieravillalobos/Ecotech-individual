"""DAO para la entidad Empleado."""
from .conexion import abrir_conexion
from dominio.empleado import Empleado


class EmpleadoDAO:
    """Manejo de la persistencia de empleados en la base de datos."""

    @classmethod
    def insertar(
        cls,
        empleado_o_depto=None,
        nombre: str = "",
        correo: str = "",
        direccion: str = "",
        telefono: str = "",
        fecha_contrato: str = "",
        salario: float = 0.0,
        rol: str = "Empleado",
        username: str = "",
        **kwargs,
    ) -> int:
        """Inserta un nuevo empleado en la base de datos y retorna su ID."""
        if isinstance(empleado_o_depto, Empleado):
            emp = empleado_o_depto
            depto_id = emp.departamento_id
            nom = emp.nombre
            cor = emp.correo
            dir_emp = emp.direccion
            tel = emp.telefono
            fec = emp.fecha_contrato
            sal = emp.salario
        else:
            depto_id = empleado_o_depto
            nom = nombre
            cor = correo
            dir_emp = direccion
            tel = telefono
            fec = fecha_contrato
            sal = salario

        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO empleado (departamento_id, nombre, correo, direccion, telefono, fecha_contrato, salario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (depto_id, nom, cor, dir_emp, tel, fec, sal),
            )
            conn.commit()
            generated_id = cursor.lastrowid

            if isinstance(empleado_o_depto, Empleado):
                empleado_o_depto.id_empleado = generated_id

            return generated_id
        finally:
            conn.close()

    @classmethod
    def crear(cls, *args, **kwargs) -> int:
        """Alias de compatibilidad para insertar empleados."""
        return cls.insertar(*args, **kwargs)

    @classmethod
    def actualizar(cls, empleado: Empleado) -> bool:
        """Actualiza la información de un empleado existente en MySQL."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE empleado
                SET nombre = %s, correo = %s, direccion = %s, telefono = %s, salario = %s
                WHERE id_empleado = %s
                """,
                (
                    empleado.nombre,
                    empleado.correo,
                    empleado.direccion,
                    empleado.telefono,
                    empleado.salario,
                    empleado.id_empleado,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def eliminar(cls, id_empleado: int) -> bool:
        """Elimina un empleado de MySQL ignorando temporalmente restricciones FK."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            
            # 1. Desactivar validación de Foreign Keys temporalmente
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            # 2. Eliminar referencias del empleado en las tablas hijas
            cursor.execute("DELETE FROM registro_tiempo WHERE empleado_id = %s;", (id_empleado,))
            cursor.execute("DELETE FROM usuario WHERE empleado_id = %s;", (id_empleado,))
            
            # 3. Eliminar la fila principal del empleado
            cursor.execute("DELETE FROM empleado WHERE id_empleado = %s;", (id_empleado,))
            filas_afectadas = cursor.rowcount

            # 4. Reactivar validación de Foreign Keys
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            
            conn.commit()
            return filas_afectadas > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def borrar(cls, id_empleado: int) -> bool:
        """Alias de compatibilidad para eliminar empleados."""
        return cls.eliminar(id_empleado)

    @classmethod
    def obtener_por_id(cls, id_empleado: int) -> Empleado | None:
        """Obtiene un empleado por su ID."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_empleado, departamento_id, nombre, correo, 
                       direccion, telefono, fecha_contrato, salario
                FROM empleado
                WHERE id_empleado = %s
                """,
                (id_empleado,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            if isinstance(row, dict):
                return Empleado(
                    id_empleado=row["id_empleado"],
                    departamento_id=row["departamento_id"],
                    nombre=row["nombre"],
                    correo=row["correo"],
                    direccion=row["direccion"],
                    telefono=row["telefono"],
                    fecha_contrato=row["fecha_contrato"],
                    salario=float(row["salario"]),
                )
            return Empleado(
                id_empleado=row[0],
                departamento_id=row[1],
                nombre=row[2],
                correo=row[3],
                direccion=row[4],
                telefono=row[5],
                fecha_contrato=row[6],
                salario=float(row[7]),
            )
        finally:
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_empleado: int) -> Empleado | None:
        """Alias para mantener compatibilidad con las vistas de menú."""
        return cls.obtener_por_id(id_empleado)

    @classmethod
    def obtener_todos(cls) -> list[Empleado]:
        """Devuelve la lista de todos los empleados."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_empleado, departamento_id, nombre, correo, 
                       direccion, telefono, fecha_contrato, salario
                FROM empleado
                """
            )
            rows = cursor.fetchall()
            empleados = []
            for row in rows:
                if isinstance(row, dict):
                    empleados.append(
                        Empleado(
                            id_empleado=row["id_empleado"],
                            departamento_id=row["departamento_id"],
                            nombre=row["nombre"],
                            correo=row["correo"],
                            direccion=row["direccion"],
                            telefono=row["telefono"],
                            fecha_contrato=row["fecha_contrato"],
                            salario=float(row["salario"]),
                        )
                    )
                else:
                    empleados.append(
                        Empleado(
                            id_empleado=row[0],
                            departamento_id=row[1],
                            nombre=row[2],
                            correo=row[3],
                            direccion=row[4],
                            telefono=row[5],
                            fecha_contrato=row[6],
                            salario=float(row[7]),
                        )
                    )
            return empleados
        finally:
            conn.close()

    @classmethod
    def listar(cls) -> list[Empleado]:
        """Alias para mantener compatibilidad con semilla_bd.py."""
        return cls.obtener_todos()