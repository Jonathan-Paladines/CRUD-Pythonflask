from flask import Flask, request
from flask import render_template, request
from flaskext.mysql import MySQL
from datetime import datetime

app=Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='crud-empleados'
app.config['MYSQL_DATABASE_PORT']=3310
mysql.init_app(app)

@app.route("/")
def index():
    sql=' SELECT * FROM personal;'
    #sql='INSERT INTO personal (id_persona, nombres, apellidos, Correo, Telefono, Imagen) VALUES ("0987654321", "Estefania", "Sicouret Benites", "estefania.sicouret123456@gmail.com", "0995555555", "foto.jpg");'
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return render_template('personal/index.html')

@app.route('/creacion')
def creacion():
    return render_template('personal/creacion.html')

@app.route('/store', methods=['POST'])
def almacenamiento():
    _cedula=request.form['txtcedula']
    _nombre=request.form['txtnombre']
    _apellido=request.form['txtapellido']
    _correo=request.form['txtcorreo']
    _telefono=request.form['txttelefono']
    _imagen=request.files['txtimagen']
    
    ahora=datetime.now()
    tiempo=now.strftime("%Y%H%M%S")
    
    if _imagen.filename!='':
        nuevoNombreImagen=tiempo+_imagen.filename
        _imagen.save("uploads/"+nuevoNombreImagen)
    
    datos=(_cedula,_nombre,_apellido,_correo,_telefono,nuevoNombreImagen)
    
    #sql=' SELECT * FROM personal;'
    sql='INSERT INTO personal (id_persona, nombres, apellidos, Correo, Telefono, Imagen) VALUES (%s, %s, %s, %s, %s, %s);'
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('personal/index.html')
    return

if __name__ == '__main__':
    app.run(debug=True)