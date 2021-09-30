from flask import Flask, request
from flask import render_template, request, redirect
from flaskext.mysql import MySQL
from datetime import datetime
import os

app=Flask(__name__)

mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sistema_empleados'
app.config['MYSQL_DATABASE_PORT']=3306
mysql.init_app(app)

Carpeta = os.path.join('Uploads')
app.config['Carpeta']=Carpeta

@app.route("/")
def index():
    sql=' SELECT * FROM empleados;'
    #sql='INSERT INTO personal (id_persona, nombres, apellidos, Correo, Telefono, Imagen) VALUES ("0987654321", "Estefania", "Sicouret Benites", "estefania.sicouret123456@gmail.com", "0995555555", "foto.jpg");'
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    empleados=cursor.fetchall()
    print(empleados)
    conn.commit()
    return render_template('personal/index.html', empleados=empleados)

@app.route('/destroy/<id_persona>')
def destroy(id_persona):
    conn=mysql.connect()
    cursor=conn.cursor()
    
    cursor.execute("Select im_persona FROM empleados WHERE id_persona=%s",id_persona)
    fila=cursor.fetchall()
    os.remove(os.path.join(app.config['Carpeta'], fila[0][0]))    
    
    cursor.execute("DELETE FROM empleados WHERE id_persona=%s", id_persona)
    conn.commit()
    return redirect('/')

@app.route('/edit/<id_persona>')
def edit(id_persona):
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("select * from empleados WHERE id_persona=%s", (id_persona))
    empleados=cursor.fetchall()
    conn.commit()
    print(empleados)
    return render_template('personal/editar.html', empleados=empleados)

@app.route('/actualizar', methods=['POST'])
def actualizar():

    _nombre=request.form['txtnombre']
    _apellido=request.form['txtapellido']
    _correo=request.form['txtcorreo']    
    _cedula=request.form['txtcedula']
    #_telefono=request.form['txttelefono']
    _imagen=request.files['txtimagen']
    
    sql='update empleados set nombres=%s, apellidos=%s, correo=%s where id_persona=%s ;'
    
    datos=(_cedula,_nombre,_apellido,_correo)
    conn=mysql.connect()
    cursor=conn.cursor()
    
    ahora=datetime.now()
    tiempo=ahora.strftime("%Y%H%M%S")

    if _imagen.filename!='':
        nuevoNombreImagen=tiempo+_imagen.filename
        _imagen.save("uploads/"+nuevoNombreImagen)
        cursor.execute("Select im_persona FROM empleados WHERE id_persona=%s", _cedula)
        fila=cursor.fetchall()
        os.remove(os.path.join(app.config['Carpeta'], fila[0][0]))
        cursor.execute("Update empleados SET im_persona=%s WHERE id_persona=%s", (nuevoNombreImagen, _cedula))
    
    cursor.execute(sql,datos)
    conn.commit()
    
    return redirect('/')

@app.route('/creacion')
def creacion():
    return render_template('personal/creacion.html')


@app.route('/store', methods=['POST'])
def almacenamiento():
    _cedula=request.form['txtcedula']
    _nombre=request.form['txtnombre']
    _apellido=request.form['txtapellido']
    _correo=request.form['txtcorreo']
    #_telefono=request.form['txttelefono']
    _imagen=request.files['txtimagen']
    
    ahora=datetime.now()
    tiempo=ahora.strftime("%Y%H%M%S")
    
    if _imagen.filename!='':
        nuevoNombreImagen=tiempo+_imagen.filename
        _imagen.save("uploads/"+nuevoNombreImagen)
    
    datos=(_cedula,_nombre,_apellido,_correo,nuevoNombreImagen)
    
    #sql=' SELECT * FROM personal;'
    sql='INSERT INTO empleados (id_persona, nombres, apellidos, correo, im_persona) VALUES (%s, %s, %s, %s, %s);'
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return render_template('personal/index.html')
    return

if __name__ == '__main__':
    app.run(debug=True)