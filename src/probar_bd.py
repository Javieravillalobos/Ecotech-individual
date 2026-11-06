from persistencia.conexion import abrir_conexion

conn = abrir_conexion()
cursor = conn.cursor()
cursor.execute("DESCRIBE empleado;")
for col in cursor.fetchall():
    print(col)
conn.close()    