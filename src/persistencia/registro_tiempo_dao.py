"""
DAO para la entidad RegistroTiempo."""
from contextlib import closing

from .conexion import abrir_conexion, marcador_sql
from dominio.registro_tiempo import RegistroTiempo


class RegistroTiempoDAO:
    """Manejo de la persistencia de registros de tiempo en la base de datos."""

    @classmethod
    def insertar(
        cls,
        registro_o_empleado_id=None,
        proyecto_id: int = None,
        fecha: str = "",
        horas_trabajadas: float = 0.0,
        descripcion_tarea: str = "",
    ) -> int:
        """Inserta un nuevo registro de tiempo aceptando un objeto RegistroTiempo o argumentos individuales."""
        if isinstance(registro_o_empleado_id, RegistroTiempo):
            reg = registro_o_empleado_id
            emp_id = reg.empleado_id
            proy_id = reg.proyecto_id
            fec = reg.fecha
            hrs = reg.horas_trabajadas
            desc = reg.descripcion_tarea
        else:
            emp_id = registro_o_empleado_id
            proy_id = proyecto_id
            fec = fecha
            hrs = horas_trabajadas
            desc = descripcion_tarea

        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO registro_tiempo (empleado_id, proyecto_id, fecha, horas_trabajadas, descripcion_tarea)
                VALUES (%s, %s, %s, %s, %s)
                """.replace("%s", marcador_sql()),
                (emp_id, proy_id, fec, hrs, desc),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()

    @classmethod
    def crear(cls, *args, **kwargs) -> int:
        """Alias de compatibilidad para insertar registros."""
        return cls.insertar(*args, **kwargs)

    @classmethod
    def obtener_por_id(cls, id_registro: int) -> RegistroTiempo | None:
        """Obtiene un registro de tiempo por su ID."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_registro, empleado_id, proyecto_id, fecha, 
                       horas_trabajadas, descripcion_tarea
                FROM registro_tiempo
                WHERE id_registro = %s
                """.replace("%s", marcador_sql()),
                (id_registro,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            if hasattr(row, "keys"):
                return RegistroTiempo(
                    id_registro=row["id_registro"],
                    empleado_id=row["empleado_id"],
                    proyecto_id=row["proyecto_id"],
                    fecha=row["fecha"],
                    horas_trabajadas=float(row["horas_trabajadas"]),
                    descripcion_tarea=row["descripcion_tarea"],
                )
            return RegistroTiempo(
                id_registro=row[0],
                empleado_id=row[1],
                proyecto_id=row[2],
                fecha=row[3],
                horas_trabajadas=float(row[4]),
                descripcion_tarea=row[5],
            )
        finally:
            conn.close()


    @classmethod
    def obtener_por_empleado(cls, empleado_id: int) -> list[RegistroTiempo]:
        """Obtiene todos los registros de tiempo de un empleado."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_registro, empleado_id, proyecto_id, fecha, 
                       horas_trabajadas, descripcion_tarea
                FROM registro_tiempo
                WHERE empleado_id = %s
                """.replace("%s", marcador_sql()),
                (empleado_id,),
            )
            rows = cursor.fetchall()
            registros = []
            for row in rows:
                if hasattr(row, "keys"):
                    registros.append(
                        RegistroTiempo(
                            id_registro=row["id_registro"],
                            empleado_id=row["empleado_id"],
                            proyecto_id=row["proyecto_id"],
                            fecha=row["fecha"],
                            horas_trabajadas=float(row["horas_trabajadas"]),
                            descripcion_tarea=row["descripcion_tarea"],
                        )
                    )
                else:
                    registros.append(
                        RegistroTiempo(
                            id_registro=row[0],
                            empleado_id=row[1],
                            proyecto_id=row[2],
                            fecha=row[3],
                            horas_trabajadas=float(row[4]),
                            descripcion_tarea=row[5],
                        )
                    )
            return registros
        finally:
            conn.close()

    @classmethod
    def listar_por_empleado(cls, empleado_id: int) -> list[RegistroTiempo]:
        """Alias para compatibilidad con las vistas del menú."""
        return cls.obtener_por_empleado(empleado_id)

    @classmethod
    def obtener_todos(cls) -> list[RegistroTiempo]:
        """Devuelve todos los registros de tiempo en el sistema."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_registro, empleado_id, proyecto_id, fecha, 
                       horas_trabajadas, descripcion_tarea
                FROM registro_tiempo
                """
            )
            rows = cursor.fetchall()
            registros = []
            for row in rows:
                if hasattr(row, "keys"):
                    registros.append(
                        RegistroTiempo(
                            id_registro=row["id_registro"],
                            empleado_id=row["empleado_id"],
                            proyecto_id=row["proyecto_id"],
                            fecha=row["fecha"],
                            horas_trabajadas=float(row["horas_trabajadas"]),
                            descripcion_tarea=row["descripcion_tarea"],
                        )
                    )
                else:
                    registros.append(
                        RegistroTiempo(
                            id_registro=row[0],
                            empleado_id=row[1],
                            proyecto_id=row[2],
                            fecha=row[3],
                            horas_trabajadas=float(row[4]),
                            descripcion_tarea=row[5],
                        )
                    )
            return registros
        finally:
            conn.close()

    @classmethod
    def listar(cls) -> list[RegistroTiempo]:
        """Alias para compatibilidad con vistas de administración y semilla."""
        return cls.obtener_todos()

    @classmethod
    def eliminar(cls, id_registro: int) -> bool:
        """Elimina un registro de tiempo por su ID de la base de datos."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM registro_tiempo WHERE id_registro = {marcador_sql()}",
                (id_registro,),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def borrar(cls, id_registro: int) -> bool:
        """Alias de compatibilidad para la opción de eliminación."""
        return cls.eliminar(id_registro)

    @classmethod
    def actualizar(cls, id_registro: int, empleado_id: int, proyecto_id: int, fecha: str, horas: float, descripcion: str) -> bool:
        conn = abrir_conexion()
        p = marcador_sql()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute(f"UPDATE registro_tiempo SET empleado_id={p}, proyecto_id={p}, fecha={p}, horas_trabajadas={p}, descripcion_tarea={p} WHERE id_registro={p}", (empleado_id, proyecto_id, fecha, horas, descripcion, id_registro))
                cambiado = cursor.rowcount > 0
            conn.commit()
            return cambiado
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
