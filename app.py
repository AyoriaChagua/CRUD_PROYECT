from flask import Flask, render_template, request,redirect, url_for, flash, send_from_directory
from controller import *
from werkzeug.utils import redirect
import os 


app = Flask(__name__, template_folder = 'templates')

CARPETA = os.path.join('uploads')

app.config['CARPETA'] = CARPETA
app.secret_key = 'mysecretkey'


@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'], nombreFoto)


@app.route('/')
def index():
    shoes  = get_shoes()
    return render_template('index.html', shoes = shoes)

@app.route('/main')
def main():
    shoes  = get_shoes()
    return render_template('main.html', shoes = shoes)


@app.route('/insert')
def create():
    brands  = get_brands()
    size = get_size()
    brands_id = request.args.get('brands_id')
    models = [] if brands_id is None else get_models(brands_id)
    return render_template('insert.html', brands = brands, size = size,brands_id= brands_id, models = models)

@app.route('/add', methods=['POST'])
def add_shoes():
    if request.method == 'POST':
        brand_id = request.form['brands_id']
        model_id = request.form['model']
        price = request.form['price']
        image = request.files['image'] 
        size_id = request.form['size']
        nuevoNombreImagen = format_an_image(image)
        insert_shoes(brand_id, nuevoNombreImagen,price)
        insert_model_has_sizes(model_id, size_id)
        flash('Shoes addes successfully')
        return redirect('/insert')

@app.route('/delete/<string:id>')
def delete_shoes(id):
    fila = delete_an_image(id)
    os.remove(os.path.join(app.config['CARPETA'], fila[0][0]))
    delete_shoe(id)
    
    flash('Shoes removed successfully')
    return redirect('/')


@app.route('/edit/<id>')
def edit_shoes(id):
    data = get_shoe_edit(id)
    
    return render_template('edit_shoes.html', data = data[0])


@app.route('/update/<id>', methods=['POST'])
def update_shoes(id):
    if request.method == 'POST':
        price = request.form['price'] 
        image = request.files['image']
        image_ant = request.form['image_ant']
        fila = upload_an_image(image, id)
        if fila != None:
            os.remove(os.path.join(app.config['CARPETA'], image_ant))
            update_shoe(id,price)
 
        else:
            
            update_shoe(id, price)

        flash('Shoes updated Successfully')
        return redirect(url_for('edit_shoes', id = id))



if __name__ == '__main__':
    app.run(port=3000, debug=True)