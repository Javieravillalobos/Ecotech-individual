"""DAO para la persistencia de indicadores económicos en la base de datos."""
from contextlib import closing

from dominio.indicador import Indicador
from persistencia.conexion import abrir_conexion, motor_actual


class IndicadorDAO:
    @staticmethod
    def guardar(indicador: Indicador) -> bool:
        """Guarda un indicador en la BD. Si ya existe (fuente, codigo, fecha), no lo duplica."""
        conn = abrir_conexion()
        try:
            with closing(conn.cursor()) as cursor:
                motor = motor_actual()
                placeholder = "%s" if motor in ("mysql", "mariadb") else "?"
                
                sql = f"""
                    INSERT INTO indicador_api (fuente, codigo, fecha, valor)
                    VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder})
                """
                if motor in ("mysql", "mariadb"):
                    sql += " ON DUPLICATE KEY UPDATE valor = VALUES(valor)"
                else:
                    sql += " ON CONFLICT(fuente, codigo, fecha) DO UPDATE SET valor = excluded.valor"

                cursor.execute(sql, (
                    indicador.fuente,
                    getattr(indicador, "codigo", "dolar"),
                    indicador.fecha,
                    float(indicador.valor)
                ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al guardar indicador en BD: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def obtener_ultimo() -> Indicador | None:
        """Obtiene el último indicador almacenado para el respaldo offline."""
        conn = abrir_conexion()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    SELECT fuente, codigo, fecha, valor 
                    FROM indicador_api 
                    ORDER BY fecha DESC, id DESC 
                    LIMIT 1
                """)
                fila = cursor.fetchone()
                if fila:
                    if isinstance(fila, (tuple, list)):
                        return Indicador(fecha=str(fila[2]), valor=float(fila[3]), fuente=str(fila[0]))
                    return Indicador(fecha=str(fila["fecha"]), valor=float(fila["valor"]), fuente=str(fila["fuente"]))
                return None
        finally:
            conn.close()

    @staticmethod
    def listar_historial() -> list[dict]:
        """Obtiene todo el historial registrado en la base de datos local."""
        conn = abrir_conexion()
        try:
            with closing(conn.cursor()) as cursor:
                cursor.execute("""
                    SELECT fuente, codigo, fecha, valor 
                    FROM indicador_api 
                    ORDER BY fecha DESC
                """)
                filas = cursor.fetchall()
                
                historial = []
                for f in filas:
                    if isinstance(f, (tuple, list)):
                        historial.append({"fuente": f[0], "codigo": f[1], "fecha": str(f[2]), "valor": float(f[3])})
                    else:
                        historial.append({"fuente": f["fuente"], "codigo": f["codigo"], "fecha": str(f["fecha"]), "valor": float(f["valor"])})
                return historial
        finally:
            conn.close()