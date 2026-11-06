"""Script de creación e inicialización de tablas en la base de datos."""
from .conexion import abrir_conexion, obtener_motor


def crear_tablas():
    """Crea la estructura de tablas necesaria para EcoTech si no existe."""
    motor = obtener_motor()

    if motor == "sqlite":
        sentencias = [
            """
            CREATE TABLE IF NOT EXISTS departamento (
                id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                presupuesto REAL DEFAULT 0.00,
                gerente_id INTEGER NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS empleado (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                departamento_id INTEGER NULL,
                nombre TEXT NOT NULL,
                correo TEXT UNIQUE NOT NULL,
                direccion TEXT,
                telefono TEXT,
                fecha_contrato TEXT NOT NULL,
                salario REAL NOT NULL,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id_departamento) ON DELETE SET NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                rol TEXT DEFAULT 'Empleado',
                FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS proyecto (
                id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha_inicio TEXT NOT NULL,
                fecha_fin TEXT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS proyecto_empleado (
                proyecto_id INTEGER NOT NULL,
                empleado_id INTEGER NOT NULL,
                PRIMARY KEY (proyecto_id, empleado_id),
                FOREIGN KEY (proyecto_id) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS registro_tiempo (
                id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                empleado_id INTEGER NOT NULL,
                proyecto_id INTEGER NOT NULL,
                horas_trabajadas REAL NOT NULL,
                fecha TEXT NOT NULL,
                descripcion_tarea TEXT,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado) ON DELETE CASCADE,
                FOREIGN KEY (proyecto_id) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS indicador_api (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fuente TEXT NOT NULL,
                codigo TEXT NOT NULL,
                fecha TEXT NOT NULL,
                valor REAL NOT NULL,
                UNIQUE (fuente, codigo, fecha)
            );
            """,
        ]
    else:
        # Estructura Nativa para MySQL
        sentencias = [
            "SET FOREIGN_KEY_CHECKS = 0;",
            """
            CREATE TABLE IF NOT EXISTS departamento (
                id_departamento INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                presupuesto DECIMAL(12, 2) DEFAULT 0.00,
                gerente_id INT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS empleado (
                id_empleado INT AUTO_INCREMENT PRIMARY KEY,
                departamento_id INT NULL,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(100) UNIQUE NOT NULL,
                direccion VARCHAR(255),
                telefono VARCHAR(20),
                fecha_contrato DATE NOT NULL,
                salario DECIMAL(10, 2) NOT NULL,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id_departamento) ON DELETE SET NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                empleado_id INT UNIQUE NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                rol ENUM('Empleado', 'Administrador') DEFAULT 'Empleado',
                FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS proyecto (
                id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                fecha_inicio DATE NOT NULL,
                fecha_fin DATE NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS proyecto_empleado (
                proyecto_id INT NOT NULL,
                empleado_id INT NOT NULL,
                PRIMARY KEY (proyecto_id, empleado_id),
                FOREIGN KEY (proyecto_id) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS registro_tiempo (
                id_registro INT AUTO_INCREMENT PRIMARY KEY,
                empleado_id INT NOT NULL,
                proyecto_id INT NOT NULL,
                horas_trabajadas DECIMAL(5, 2) NOT NULL,
                fecha DATE NOT NULL,
                descripcion_tarea TEXT,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado) ON DELETE CASCADE,
                FOREIGN KEY (proyecto_id) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS indicador_api (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fuente VARCHAR(100) NOT NULL,
                codigo VARCHAR(50) NOT NULL,
                fecha DATE NOT NULL,
                valor DECIMAL(18, 6) NOT NULL,
                UNIQUE KEY uq_indicador_api (fuente, codigo, fecha)
            );
            """,
            "SET FOREIGN_KEY_CHECKS = 1;",
        ]

    conn = abrir_conexion()
    try:
        cursor = conn.cursor()
        for sentencia in sentencias:
            sentencia_limpia = sentencia.strip()
            if sentencia_limpia:
                cursor.execute(sentencia_limpia)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


if __name__ == "__main__":
    crear_tablas()