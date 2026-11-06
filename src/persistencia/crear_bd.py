"""Script de creación e inicialización de tablas en la base de datos."""
from .conexion import abrir_conexion


def crear_tablas():
    """Crea la estructura de tablas necesaria para EcoTech si no existe."""
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
        CREATE TABLE IF NOT EXISTS registro_tiempo (
            id_registro INT AUTO_INCREMENT PRIMARY KEY,
            empleado_id INT NOT NULL,
            proyecto_id INT NOT NULL,
            horas DECIMAL(5, 2) NOT NULL,
            fecha DATE NOT NULL,
            descripcion TEXT,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id_empleado) ON DELETE CASCADE,
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
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