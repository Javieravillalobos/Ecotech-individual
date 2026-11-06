"""DAO para la entidad Proyecto."""
from .conexion import abrir_conexion
from dominio.proyecto import Proyecto


class ProyectoDAO:
    """Manejo de la persistencia de proyectos en la base de datos."""

    @classmethod
    def obtener_por_id(cls, id_proyecto: int) -> Proyecto | None:
        """Obtiene un proyecto por su ID."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, NULL AS estado
                FROM proyecto
                WHERE id_proyecto = %s
                """,
                (id_proyecto,),
            )
            row = cursor.fetchone()
            if not row:
                return None

            if isinstance(row, dict):
                return Proyecto(
                    id_proyecto=row["id_proyecto"],
                    nombre=row["nombre"],
                    descripcion=row["descripcion"],
                    fecha_inicio=str(row["fecha_inicio"]),
                    fecha_fin=str(row["fecha_fin"]) if row["fecha_fin"] else None,
                    estado=row["estado"] or "En progreso",
                )
            return Proyecto(
                id_proyecto=row[0],
                nombre=row[1],
                descripcion=row[2],
                fecha_inicio=str(row[3]),
                fecha_fin=str(row[4]) if row[4] else None,
                estado=row[5] or "En progreso",
            )
        finally:
            conn.close()

    @classmethod
    def buscar_por_id(cls, id_proyecto: int) -> Proyecto | None:
        """Alias para mantener compatibilidad con las vistas del menú."""
        return cls.obtener_por_id(id_proyecto)

    @classmethod
    def obtener_todos(cls) -> list[Proyecto]:
        """Devuelve todos los proyectos registrados en el sistema."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id_proyecto, nombre, descripcion, fecha_inicio, fecha_fin, NULL AS estado
                FROM proyecto
                """
            )
            rows = cursor.fetchall()
            proyectos = []
            for row in rows:
                if isinstance(row, dict):
                    proyectos.append(
                        Proyecto(
                            id_proyecto=row["id_proyecto"],
                            nombre=row["nombre"],
                            descripcion=row["descripcion"],
                            fecha_inicio=str(row["fecha_inicio"]),
                            fecha_fin=str(row["fecha_fin"]) if row["fecha_fin"] else None,
                            estado=row["estado"] or "En progreso",
                        )
                    )
                else:
                    proyectos.append(
                        Proyecto(
                            id_proyecto=row[0],
                            nombre=row[1],
                            descripcion=row[2],
                            fecha_inicio=str(row[3]),
                            fecha_fin=str(row[4]) if row[4] else None,
                            estado=row[5] or "En progreso",
                        )
                    )
            return proyectos
        finally:
            conn.close()

    @classmethod
    def listar(cls) -> list[Proyecto]:
        """Alias de compatibilidad para listar proyectos."""
        return cls.obtener_todos()

    @classmethod
    def insertar(
        cls,
        proyecto_o_nombre=None,
        descripcion: str = "",
        fecha_inicio: str = "",
        fecha_fin: str = None,
        estado: str = "En progreso",
        **kwargs,
    ) -> int:
        """Inserta un nuevo proyecto en MySQL."""
        if isinstance(proyecto_o_nombre, Proyecto):
            proy = proyecto_o_nombre
            nom = proy.nombre
            desc = proy.descripcion
            f_ini = proy.fecha_inicio
            f_fin = proy.fecha_fin
        else:
            nom = proyecto_o_nombre
            desc = descripcion
            f_ini = fecha_inicio
            f_fin = fecha_fin

        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO proyecto (nombre, descripcion, fecha_inicio, fecha_fin)
                VALUES (%s, %s, %s, %s)
                """,
                (nom, desc, f_ini, f_fin),
            )
            conn.commit()
            generated_id = cursor.lastrowid
            if isinstance(proyecto_o_nombre, Proyecto):
                proyecto_o_nombre.id_proyecto = generated_id
            return generated_id
        finally:
            conn.close()

    @classmethod
    def crear(cls, *args, **kwargs) -> int:
        """Alias para insertar proyectos."""
        return cls.insertar(*args, **kwargs)

    @classmethod
    def actualizar(cls, proyecto: Proyecto) -> bool:
        """Actualiza un proyecto existente en MySQL."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE proyecto
                SET nombre = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s
                WHERE id_proyecto = %s
                """,
                (
                    proyecto.nombre,
                    proyecto.descripcion,
                    proyecto.fecha_inicio,
                    proyecto.fecha_fin,
                    proyecto.id_proyecto,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()

    @classmethod
    def eliminar(cls, id_proyecto: int) -> bool:
        """Elimina un proyecto y desvincula previamente sus registros asociados."""
        conn = abrir_conexion()
        try:
            cursor = conn.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
            cursor.execute("DELETE FROM registro_tiempo WHERE proyecto_id = %s;", (id_proyecto,))
            cursor.execute("DELETE FROM proyecto WHERE id_proyecto = %s;", (id_proyecto,))
            filas_afectadas = cursor.rowcount
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()
            return filas_afectadas > 0
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def borrar(cls, id_proyecto: int) -> bool:
        """Alias para eliminar proyectos."""
        return cls.eliminar(id_proyecto)