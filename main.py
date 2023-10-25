import fastapi
import mysql.connector
from pydantic import BaseModel

app = fastapi.FastAPI()

class Contacto(BaseModel):
    email: str
    nombre: str
    telefono: str

# Crear la conexión a la base de datos
conn = mysql.connector.connect(
    user='r8j7aq906amihnto',
    password='ceandy13kb8mepit',
    host='jhdjjtqo9w5bzq2t.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    port='3306',
    database='jjyuzlldzo267aht'
)

@app.get("/")
def inicio():
    return {'Developer by': 'Patricio Vargas f:'}

# Rutas para las operaciones CRUD

@app.post("/contactos")
async def crear_contacto(contacto: Contacto):
    """Crea un nuevo contacto."""
    # Insertar el contacto en la base de datos y responder con un mensaje
    c = conn.cursor()
    add_data = (
        'INSERT INTO contactos (email, nombre, telefono) VALUES (%s, %s, %s)',
        (contacto.email, contacto.nombre, contacto.telefono)
    )
    c.execute(*add_data)
    conn.commit()
    return contacto

@app.get("/contactos")
async def obtener_contactos():
    """Obtiene todos los contactos."""
    # Consultar todos los contactos de la base de datos y enviarlos en un JSON
    c = conn.cursor()
    c.execute('SELECT * FROM contactos;')
    response = []
    for row in c:
        contacto = {"email": row[0], "nombre": row[1], "telefono": row[2]}
        response.append(contacto)
    return response

@app.get("/contactos/{email}")
async def obtener_contacto(email: str):
    """Obtiene un contacto por su email."""
    # Consultar el contacto por su email
    c = conn.cursor()
    c.execute('SELECT * FROM contactos WHERE email = %s', (email,))
    contacto = None
    for row in c:
        contacto = {"email": row[0], "nombre": row[1], "telefono": row[2]}
    return contacto

@app.put("/contactos/{email}")
async def actualizar_contacto(email: str, contacto: Contacto):
    """Actualiza un contacto."""
    c = conn.cursor()
    c.execute(
        'UPDATE contactos SET nombre = %s, telefono = %s WHERE email = %s',
        (contacto.nombre, contacto.telefono, email)
    )
    conn.commit()
    return contacto

@app.delete("/contactos/{email}")
async def eliminar_contacto(email: str):
    """Elimina un contacto."""
    # Eliminar el contacto de la base de datos
    c = conn.cursor()
    c.execute('DELETE FROM contactos WHERE email = %s', (email,))
    conn.commit()
    return {"mensaje": "Contacto eliminado"}
