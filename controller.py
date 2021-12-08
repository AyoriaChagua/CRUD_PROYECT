from db import get_connection_db
from datetime import datetime


def insert_shoes(brand_id, image, price):
     cur = get_connection_db()
     with cur.cursor() as cursor:
        cursor.execute('INSERT INTO shoes (brand_id, image, price) VALUES(%s, %s,%s)', ( brand_id, image, price))  
     cur.commit()
     cur.close()
     

def insert_model_has_sizes(model_id, size_id):
    cur = get_connection_db()
    with cur.cursor() as cursor:
        cursor.execute('INSERT INTO  models_has_size (models_id, size_id) VALUES(%s, %s)', (model_id, size_id))  
    cur.commit()
    cur.close()


def get_shoe_edit(id):
    connection = get_connection_db()
    data = [] 
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM shoes WHERE id= %s", (id))
        data = cursor.fetchall()
    return data

def get_shoes():
    connection = get_connection_db()
    shoes = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT s.id, s.price, s.image, b.name FROM shoes s INNER JOIN brand b ON s.brand_id = b.id")
        shoes = cursor.fetchall()
    connection.close()
    return shoes

def get_brands():
    connection = get_connection_db()
    brands = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM brand")
        brands = cursor.fetchall()
    connection.close()
    return brands

def get_models(id_brand):
    connection = get_connection_db()
    brands = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM models where brand_id=%s", (id_brand))
        brands = cursor.fetchall()
    return brands


def get_size():
    connection = get_connection_db()
    size = []
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM size")
        size = cursor.fetchall()
    connection.close()
    return size

def format_an_image(image):
    
    now = datetime.now()
    tiempo = now.strftime("%Y%H%M%S")
    if image.filename != '':
            nuevoNombreImagen =  tiempo + image.filename
            image.save("uploads/" + nuevoNombreImagen)
            return nuevoNombreImagen


def delete_an_image(id):
    cur = get_connection_db()
    with cur.cursor() as cursor:
            cursor.execute("SELECT image FROM shoes WHERE id = %s", id)
            fila = cursor.fetchall()
            return fila 
    
def delete_shoe(id):
    cur = get_connection_db()
    with cur.cursor() as cursor:
        cursor.execute("DELETE FROM shoes WHERE id={0}" .format(id))
        cur.commit()


def upload_an_image(image, id):
    cur = get_connection_db()
    with cur.cursor() as cursor:
        
        if image.filename != '':
            nuevoNombreImagen = format_an_image(image)
            cursor.execute("SELECT image FROM shoes WHERE id = %s", id)
            cursor.execute("UPDATE shoes SET image = %s  WHERE id = %s", (nuevoNombreImagen, id))
            cur.commit()
            fila = cursor.fetchall()
            return fila

def get_shoe_edit(id):
    connection = get_connection_db()
    data = [] 
    with connection.cursor() as cursor:
        cursor.execute("SELECT id ,  price, image FROM shoes WHERE id = %s", (id))
        data = cursor.fetchall()
    return data


def update_shoe(id, price):
    cur = get_connection_db()
    with cur.cursor() as cursor:
        cursor.execute("UPDATE shoes SET price = %s  WHERE id = %s", (price, id))
        cur.commit()