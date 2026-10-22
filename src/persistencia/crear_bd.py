"""Creación de tablas para SQLite y MySQL/MariaDB."""
from .conexion import abrir_conexion, motor_actual


ESQUEMA_SQLITE = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_id INTEGER NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS departamento (
    id_depto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS empleado (
    id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL UNIQUE,
    departamento_id INTEGER,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    direccion TEXT NOT NULL DEFAULT '',
    telefono TEXT NOT NULL DEFAULT '',
    fecha_contrato TEXT NOT NULL,
    salario REAL NOT NULL CHECK (salario >= 0),
    rol TEXT NOT NULL DEFAULT 'Empleado',
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (departamento_id)
        REFERENCES departamento(id_depto) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS proyecto (
    id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT NOT NULL DEFAULT '',
    fecha_inicio TEXT NOT NULL DEFAULT '',
    fecha_fin TEXT NOT NULL DEFAULT '',
    CHECK (
        fecha_fin = ''
        OR fecha_inicio = ''
        OR fecha_fin >= fecha_inicio
    )
);

CREATE TABLE IF NOT EXISTS proyecto_empleado (
    proyecto_id INTEGER NOT NULL,
    empleado_id INTEGER NOT NULL,
    PRIMARY KEY (proyecto_id, empleado_id),
    FOREIGN KEY (proyecto_id)
        REFERENCES proyecto(id_proyecto) ON DELETE CASCADE,
    FOREIGN KEY (empleado_id)
        REFERENCES empleado(id_empleado) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS registro_tiempo (
    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
    empleado_id INTEGER NOT NULL,
    proyecto_id INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    horas_trabajadas REAL NOT NULL
        CHECK (horas_trabajadas > 0 AND horas_trabajadas <= 24),
    descripcion_tarea TEXT NOT NULL,
    FOREIGN KEY (empleado_id)
        REFERENCES empleado(id_empleado) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id)
        REFERENCES proyecto(id_proyecto) ON DELETE CASCADE
);
"""


ESQUEMA_MYSQL = """
CREATE TABLE IF NOT EXISTS usuario (
    id INT NOT NULL AUTO_INCREMENT,
    empleado_id INTEGER NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_usuario_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS departamento (
    id_depto INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(150) NOT NULL,
    PRIMARY KEY (id_depto),
    UNIQUE KEY uq_departamento_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS empleado (
    id_empleado INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    departamento_id INT NULL,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(254) NOT NULL,
    direccion VARCHAR(255) NOT NULL DEFAULT '',
    telefono VARCHAR(40) NOT NULL DEFAULT '',
    fecha_contrato VARCHAR(10) NOT NULL,
    salario DECIMAL(12,2) NOT NULL,
    rol VARCHAR(80) NOT NULL DEFAULT 'Empleado',
    PRIMARY KEY (id_empleado),
    UNIQUE KEY uq_empleado_usuario (usuario_id),
    UNIQUE KEY uq_empleado_correo (correo),
    CONSTRAINT fk_empleado_usuario
        FOREIGN KEY (usuario_id)
        REFERENCES usuario(id),
    CONSTRAINT fk_empleado_departamento
        FOREIGN KEY (departamento_id)
        REFERENCES departamento(id_depto)
        ON DELETE SET NULL,
    CONSTRAINT chk_empleado_salario CHECK (salario >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS proyecto (
    id_proyecto INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT NOT NULL,
    fecha_inicio VARCHAR(10) NOT NULL DEFAULT '',
    fecha_fin VARCHAR(10) NOT NULL DEFAULT '',
    PRIMARY KEY (id_proyecto),
    CONSTRAINT chk_proyecto_fechas CHECK (
        fecha_fin = ''
        OR fecha_inicio = ''
        OR fecha_fin >= fecha_inicio
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS proyecto_empleado (
    proyecto_id INT NOT NULL,
    empleado_id INT NOT NULL,
    PRIMARY KEY (proyecto_id, empleado_id),
    CONSTRAINT fk_pe_proyecto
        FOREIGN KEY (proyecto_id)
        REFERENCES proyecto(id_proyecto)
        ON DELETE CASCADE,
    CONSTRAINT fk_pe_empleado
        FOREIGN KEY (empleado_id)
        REFERENCES empleado(id_empleado)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS registro_tiempo (
    id_registro INT NOT NULL AUTO_INCREMENT,
    empleado_id INT NOT NULL,
    proyecto_id INT NOT NULL,
    fecha VARCHAR(10) NOT NULL,
    horas_trabajadas DECIMAL(5,2) NOT NULL,
    descripcion_tarea VARCHAR(500) NOT NULL,
    PRIMARY KEY (id_registro),
    CONSTRAINT fk_rt_empleado
        FOREIGN KEY (empleado_id)
        REFERENCES empleado(id_empleado)
        ON DELETE CASCADE,
    CONSTRAINT fk_rt_proyecto
        FOREIGN KEY (proyecto_id)
        REFERENCES proyecto(id_proyecto)
        ON DELETE CASCADE,
    CONSTRAINT chk_rt_horas CHECK (
        horas_trabajadas > 0 AND horas_trabajadas <= 24
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""


def crear_tablas():
    """Crea las tablas correspondientes al motor seleccionado."""
    conn = abrir_conexion()

    try:
        motor = motor_actual()

        if motor == "sqlite":
            esquema = ESQUEMA_SQLITE
        elif motor in ("mysql", "mariadb"):
            esquema = ESQUEMA_MYSQL
        else:
            raise ValueError(
                "DB_ENGINE debe ser 'sqlite', 'mysql' o 'mariadb'."
            )

        conn.executescript(esquema)
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada.")