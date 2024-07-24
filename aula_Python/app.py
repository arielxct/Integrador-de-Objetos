from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'aula01'
app.secret_key = 'mysecretkey'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# ----------------------REGISTRO DE USUARIOS ---------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        role = request.form.get('role', 'user')  # Puedes obtener esto del formulario o asignarlo manualmente
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)", (username, email, password, role))
        mysql.connection.commit()
        cur.close()
        
        flash('Usted se ha registrado satisfactoriamente!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# ------------------- LOGIN --------------------------------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
        
        if result > 0:
            data = cur.fetchone()
            password = data[3]  # La contraseña está en el cuarto campo (índice 3)
            role = data[4]  # El rol está en el quinto campo (índice 4)
            
            if bcrypt.check_password_hash(password, password_candidate):
                session['logged_in'] = True
                session['username'] = username
                session['role'] = role
                
                flash('Usted ha iniciado sesión correctamente', 'success')
                
                if role == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('index'))
            else:
                flash('Password inválido', 'danger')
        else:
            flash('No se encuentra el usuario', 'danger')
        
        cur.close()
    
    return render_template('login.html')

# -----------------------  HOME ------------------------


@app.route('/home')
def home():
    if 'logged_in' in session:
        return render_template('home.html', username=session['username'])
    else:
        flash('Please log in first', 'danger')
        return redirect(url_for('index'))
        # return redirect(url_for('login'))
        
# --------------- LOGOUT ----------------------------

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# --------------------- INDEX ---------------------------------
@app.route('/index')
def index():
     if 'logged_in' in session:
        return render_template('index.html', username=session['username'])
     else:
        flash('Please log in first', 'danger')
        return redirect(url_for('index'))
    
     # return render_template('index.html')

# if __name__ == '__main__':
#     app.run(debug=True)
# ------------------ ADMIN -----------------------------

@app.route('/admin')
def admin():
     if 'logged_in' in session:
        return render_template('admin.html', username=session['username'])
     else:
        flash('Please log in first', 'danger')
        return redirect(url_for('index'))

# MMMMMMMMMMMMMMMMMMMMMMMM ALUMNOS MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
# --------- buscador ---------------
@app.route('/buscador')
def buscador():
    cur = mysql.connection.cursor()
   
   
    cur.execute('SELECT alumnos.dni, alumnos.nombre, alumnos.apellido, direccion.id, direccion.calle, direccion.numero, educacion.id_educacion, educacion.educacionMax FROM alumnos INNER JOIN  direccion ON alumnos.direccion = direccion.id INNER JOIN  educacion ON alumnos.educacion = educacion.id_educacion ORDER BY  alumnos.dni;')
    datos = cur.fetchall()

   # flash('Listado de Alumnos')
    return render_template('buscador.html', datos = datos)
   


# --------- listar ---------------
@app.route('/listar')
def listar():
    cur = mysql.connection.cursor()
   #  cur.execute('select * from usuario')
   
    cur.execute('SELECT alumnos.dni, alumnos.nombre, alumnos.apellido, direccion.id, direccion.calle, direccion.numero, educacion.id_educacion, educacion.educacionMax FROM alumnos INNER JOIN  direccion ON alumnos.direccion = direccion.id INNER JOIN  educacion ON alumnos.educacion = educacion.id_educacion ORDER BY  alumnos.dni;')
    datos = cur.fetchall()

    flash('Listado de Alumnos')
    
    return render_template('listar.html', datos = datos)

# -------------agregar -----------------------
@app.route('/agregar', methods=['POST','GET'])
def agregar():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        
        cur.execute('select * from alumnos')
        datosAl = cur.fetchall()
        
        cur.execute('select * from direccion')
        datos = cur.fetchall()
        
        cur.execute('select * from educacion')
        datosEduc = cur.fetchall()
        
        flash('Alumnos Agragado')
        return render_template('agregar.html', alumnos =datosAl, direccion = datos, educacion = datosEduc) 
        
      
    elif request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        educacion = request.form['educacion']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO alumnos (dni, nombre, apellido, direccion, educacion) VALUES (%s, %s, %s, %s, %s)', (dni, nombre, apellido, direccion, educacion))
        cur.connection.commit()
        return  redirect(url_for('listar'))
    
    
 
#-------------obtener para EDITAR--------------------
@app.route('/obtener/<id>')
def obtener(id):
  
         cur = mysql.connection.cursor()
         cur.execute('select * from alumnos where dni = %s' % (id))
         alumno = cur.fetchall()
        
        
 # ------agrego codigo -------------    
         curDir = mysql.connection.cursor()
         curDir.execute('select * from direccion')
         datosDir = curDir.fetchall()

         curMiDir = mysql.connection.cursor()
         curMiDir.execute('select alumnos.direccion, direccion.calle, direccion.numero from alumnos,direccion where direccion.id = alumnos.direccion and alumnos.dni = %s' % (id))
         datoMiDir = curMiDir.fetchall()

   
 # ------educacion ------------- 
         curEduc = mysql.connection.cursor()
         curEduc.execute('select * from educacion')
         datosEduc = curEduc.fetchall()
         
         curMiEduc = mysql.connection.cursor()
         curMiEduc.execute('select alumnos.educacion, educacion.id_educacion, educacion.educacionMax from alumnos,educacion where educacion.id_educacion = alumnos.educacion and alumnos.dni = %s' % (id))
         datoMiEduc = curMiEduc.fetchall()
        
         return render_template('editar.html', alumnos = alumno[0], direccion = datosDir, educacion = datosEduc,lacalle = datoMiDir,laEduca = datoMiEduc )
# ----------- actualizar -----------------
# codigo nuevo <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@app.route('/actualizar/<dni>', methods=['POST'])
def actualizar(dni):
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        educacion = request.form['educacion']

        

        #  UPDATE 
        update_query = """
        UPDATE `alumnos`
        SET `nombre` = '{0}', `apellido` = '{1}', `direccion` = '{2}', `educacion` = '{3}'
        WHERE `alumnos`.`dni` = %s
        """

        # Formato de  values
        updated_values = [nombre, apellido, direccion, educacion]

        # Ejecuto query 
        cur = mysql.connection.cursor()
        cur.execute(update_query.format(*updated_values), (dni,))

        # Commit 
        
        cur.connection.commit()

        # ============================
        affected_rows = cur.rowcount
        if affected_rows > 0:
            print(f"\nSe actualizó el alumnos con DNI {dni}")
            return redirect(url_for('listar'))
        else:
            print(f"\nNo se encontró el alumnos con DNI {dni}")
            return redirect(url_for('listar'))

   

     
# -------------eliminar - OK -----------------------
@app.route('/eliminar/<string:dni>')
def eliminar(dni):
     
       cur = mysql.connection.cursor()
       cur.execute('delete from alumnos where dni = {0}'.format (dni))
       cur.connection.commit()
       return redirect(url_for('listar'))
   
# --------- Buscar por DNI---------------
@app.route('/buscarDni', methods=['POST'])
def buscarDni():
    dni =request.form['dni']
    cur = mysql.connection.cursor()
    cur.execute('SELECT  alumnos.dni, alumnos.nombre, alumnos.apellido, direccion.id, direccion.calle, direccion.numero, educacion.id_educacion, educacion.educacionMax FROM alumnos INNER JOIN  direccion ON alumnos.direccion = direccion.id INNER JOIN  educacion ON alumnos.educacion = educacion.id_educacion  where dni LIKE "%%%s%%"' % (dni))
    
    datos = cur.fetchall()
    
    if datos:
        flash('Resultado de la busqueda')
    else:
        flash('No hay resultados para su busqueda')
    return render_template('buscador.html', datos = datos)

# --------- Buscar por Nombre---------------
@app.route('/buscarNombre', methods=['POST'])
def buscar():
    nombre =request.form['nombre']
    cur = mysql.connection.cursor()
    
    cur.execute('SELECT  alumnos.dni, alumnos.nombre, alumnos.apellido, direccion.id, direccion.calle, direccion.numero, educacion.id_educacion, educacion.educacionMax FROM alumnos INNER JOIN  direccion ON alumnos.direccion = direccion.id INNER JOIN  educacion ON alumnos.educacion = educacion.id_educacion  where nombre LIKE "%%%s%%"' % (nombre))
   
    datos = cur.fetchall()
    
    if datos:
        flash('Resultado de la busqueda')
    else:
        flash('No hay resultados para su busqueda')
    return render_template('buscador.html', datos = datos)
  # --------- Buscar por Apellido---------------
@app.route('/buscarApellido', methods=['POST'])
def buscarApellido():
    apellido =request.form['apellido']
    cur = mysql.connection.cursor()
   
    cur.execute('SELECT  alumnos.dni, alumnos.nombre, alumnos.apellido, direccion.id, direccion.calle, direccion.numero, educacion.id_educacion, educacion.educacionMax FROM alumnos INNER JOIN  direccion ON alumnos.direccion = direccion.id INNER JOIN  educacion ON alumnos.educacion = educacion.id_educacion where apellido LIKE "%%%s%%"' % (apellido))
   
    datos = cur.fetchall()
    
    if datos:
        flash('Resultado de la busqueda')
    else:
        flash('No hay resultados para su busqueda')
    return render_template('buscador.html', datos = datos) 


# MMMMMMMMMMMMM   INSTRUCTORES MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

 
# --------- buscador instructores---------------
@app.route('/buscadorInst')
def buscadorInst():
    cur = mysql.connection.cursor()
   
   
    cur.execute('SELECT instructores.dni, instructores.nombre, instructores.apellido, direccion.id, direccion.calle, direccion.numero, educacioninst.id_educacion, educacioninst.educacionMax FROM instructores INNER JOIN  direccion ON instructores.direccion = direccion.id INNER JOIN  educacioninst ON instructores.educacion = educacioninst.id_educacion ORDER BY  instructores.dni;')
    datosInst = cur.fetchall()

    flash('Listado de Instructores')
    return render_template('buscadorinst.html', datosInst = datosInst)
   


# --------- listar instructores ---------------
@app.route('/listarinst')
def listarinst():
    cur = mysql.connection.cursor()
   
   
    cur.execute('SELECT instructores.dni, instructores.nombre, instructores.apellido, direccion.id, direccion.calle, direccion.numero, educacioninst.id_educacion, educacioninst.educacionMax FROM instructores INNER JOIN  direccion ON instructores.direccion = direccion.id INNER JOIN  educacioninst ON instructores.educacion = educacioninst.id_educacion ORDER BY  instructores.dni;')
    datosInst = cur.fetchall()

    flash('Listado de Instructores')
    
    return render_template('listarinst.html', datosInst = datosInst)

# -------------agregar instructores -----------------------
@app.route('/agregarinst', methods=['POST','GET'])
def agregarInst():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        
        cur.execute('select * from direccion')
        datosInst = cur.fetchall()
        
        cur.execute('select * from educacionInst')
        datosEducInst = cur.fetchall()
        
        flash('instructores Agregado')
        return render_template('agregarinst.html', direccionInst = datosInst, educacionInst = datosEducInst) 
        
      
    elif request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        educacion = request.form['educacion']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO instructores (dni, nombre, apellido, direccion, educacion) VALUES (%s, %s, %s, %s, %s)', (dni, nombre, apellido, direccion, educacion))
        cur.connection.commit()
        return  redirect(url_for('listarinst'))
     

#-------------obtener para EDITAR--------------------
@app.route('/obtenerInst/<id>')
def obtenerinst(id):
  
         cur = mysql.connection.cursor()
         cur.execute('select * from instructores where dni = %s' % (id))
         instructores = cur.fetchall()
        
        
 # ------agrego codigo -------------    
         curDirInst = mysql.connection.cursor()
         curDirInst.execute('select * from direccion')
         datosDirInst = curDirInst.fetchall()

         curMiDirInst = mysql.connection.cursor()
         curMiDirInst.execute('select instructores.direccion, direccion.calle, direccion.numero from instructores,direccion where direccion.id = instructores.direccion and instructores.dni = %s' % (id))
         datoMiDirInst = curMiDirInst.fetchall()

   
 # ------educacion ------------- 
         curEducInst = mysql.connection.cursor()
         curEducInst.execute('select * from educacioninst')
         datosEducInst = curEducInst.fetchall()
         
         curMiEducInst = mysql.connection.cursor()
         curMiEducInst.execute('select instructores.educacion, educacioninst.id_educacion, educacioninst.educacionMax from instructores,educacioninst where educacioninst.id_educacion = instructores.educacion and instructores.dni = %s' % (id))
         datoMiEducInst = curMiEducInst.fetchall()
        
         return render_template('editarinst.html', instructores = instructores[0], direccion = datosDirInst, educacion = datosEducInst,lacalle = datoMiDirInst,laEduca = datoMiEducInst )

# ----------- actualizar -----------------
# codigo nuevo <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@app.route('/actualizarinst/<dni>', methods=['POST'])
def actualizarinst(dni):
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        direccion = request.form['direccion']
        educacion = request.form['educacion']

        

        #  UPDATE 
        update_query = """
        UPDATE `instructores`
        SET `nombre` = '{0}', `apellido` = '{1}', `direccion` = '{2}', `educacion` = '{3}'
        WHERE `instructores`.`dni` = %s
        """

        # Formato de  values
        updated_values = [nombre, apellido, direccion, educacion]

        # Ejecuto query 
        curInst = mysql.connection.cursor()
        curInst.execute(update_query.format(*updated_values), (dni,))

        # Commit 
        
        curInst.connection.commit()

        # ============================
        affected_rows = curInst.rowcount
        if affected_rows > 0:
            print(f"\nSe actualizó el instructor con DNI {dni}")
            return redirect(url_for('listarinst'))
        else:
            print(f"\nNo se encontró el instructor con DNI {dni}")
            return redirect(url_for('listarinst'))

 
     
# -------------eliminar instructores - OK -----------------------
@app.route('/eliminarinst/<string:dni>')
def eliminarinst(dni):
     
       curInst = mysql.connection.cursor()
       curInst.execute('delete from instructores where dni = {0}'.format (dni))
       curInst.connection.commit()
       return redirect(url_for('listarinst'))
   
# --------- Buscar por DNI de instructores---------------
@app.route('/buscarDniInst', methods=['POST'])
def buscarDniInst():
    dni =request.form['dni']
    curInst = mysql.connection.cursor()
   
    curInst.execute('SELECT  instructores.dni, instructores.nombre, instructores.apellido, direccion.id, direccion.calle, direccion.numero, educacioninst.id_educacion, educacioninst.educacionMax FROM instructores INNER JOIN  direccion ON instructores.direccion = direccion.id INNER JOIN  educacioninst ON instructores.educacion = educacioninst.id_educacion  where dni LIKE "%%%s%%"' % (dni))
    
    datosInstDni = curInst.fetchall()
    
    if datosInstDni:
        flash('Resultado de la busqueda de instructores')
    else:
        flash('No hay resultados para la busqueda de instructor')
    return render_template('buscadorinst.html', datosInst = datosInstDni)

# --------- Buscar por Nombre de instructores---------------
@app.route('/buscarNombreInst', methods=['POST'])
def buscarNombreInst():
    nombre =request.form['nombre']
    curInstNombre = mysql.connection.cursor()
   
    curInstNombre.execute('SELECT  instructores.dni, instructores.nombre, instructores.apellido, direccion.id, direccion.calle, direccion.numero, educacioninst.id_educacion, educacioninst.educacionMax FROM instructores INNER JOIN  direccion ON instructores.direccion = direccion.id INNER JOIN  educacioninst ON instructores.educacion = educacioninst.id_educacion  where nombre LIKE "%%%s%%"' % (nombre))
    
    datosInstNombre = curInstNombre.fetchall()
    
    if datosInstNombre:
        flash('Resultado de la busqueda de instructor')
    else:
        flash('No hay resultados para la busqueda de instructor')
    return render_template('buscadorinst.html', datosInst = datosInstNombre)

  # --------- Buscar por Apellido de instructores---------------
@app.route('/buscarApellidoInst', methods=['POST'])
def buscarApellidoInst():
    apellido =request.form['apellido']
    curInstApellido = mysql.connection.cursor()
    
    curInstApellido.execute('SELECT  instructores.dni, instructores.nombre, instructores.apellido, direccion.id, direccion.calle, direccion.numero, educacioninst.id_educacion, educacioninst.educacionMax FROM instructores INNER JOIN  direccion ON instructores.direccion = direccion.id INNER JOIN  educacioninst ON instructores.educacion = educacioninst.id_educacion where apellido LIKE "%%%s%%"' % (apellido))
   
    datosInstApellido = curInstApellido.fetchall()
    
    if datosInstApellido:
        flash('Resultado de la busqueda de instructor')
    else:
        flash('No hay resultados para la busqueda de instructor')
    return render_template('buscadorinst.html', datosInst = datosInstApellido) 



# MMMMMMMMMMMMMMMMM FIN INSTRUCTORES MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

# MMMMMMMMMMMMMMMMM COMIENZO DE CURSOS MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM
@app.route('/buscadorcursos')
def buscadorCursos():
    cur = mysql.connection.cursor()
   
   
    
    cur.execute('SELECT * FROM cursos;')
    datosCursos = cur.fetchall()


    flash('Listado de Cursos')
    return render_template('buscadorcursos.html', datosCursos = datosCursos)
   


# --------- listar cursos ---------------
@app.route('/listarcursos')
def listarcursos():
    cur = mysql.connection.cursor()
   
   
  
    cur.execute('SELECT * FROM cursos;')
    datosCursos = cur.fetchall()

    flash('Listado de Cursos')
    
    return render_template('listarcursos.html', datosCursos = datosCursos)

# -------------agregar cursos -----------------------
@app.route('/agregarcursos', methods=['POST','GET'])
def agregarCursos():
    if request.method == 'GET':
        
        cur = mysql.connection.cursor()
        cur.execute('select * from cursos')
        datosCursos = cur.fetchall()
        
         # ------agrego codigo id de cursadas-------------    
        curCursos = mysql.connection.cursor()
        curCursos.execute('SELECT (MAX(codigo)+1) AS max_codigo_curso FROM cursos')
        datosMaxCurso = curCursos.fetchall()
        # ----------------------------------------
        flash('Curso Agregado')
        return render_template('agregarcursos.html', datosCursos = datosCursos, datosMaxCurso =  datosMaxCurso) 
        
      
    elif request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO cursos (codigo, nombre, descripcion) VALUES (%s, %s, %s)', (codigo, nombre, descripcion))
        cur.connection.commit()
        return  redirect(url_for('listarcursos'))
     

#-------------obtener para EDITAR--------------------
@app.route('/obtenercursos/<codigo>')
def obtenerCursos(codigo):
  
         cur = mysql.connection.cursor()
         cur.execute('select * from cursos where codigo = %s' % (codigo))
         cursos = cur.fetchall()
        
        
 # ------agrego codigo -------------    
         curCursos = mysql.connection.cursor()
         curCursos.execute('select * from cursos')
         datosCursos = curCursos.fetchall()

        

   
 # ------educacion ------------- 
        
         
         return render_template('editarcursos.html', cursos = cursos[0], datosCursos = datosCursos)
        
        
# ----------- actualizar -----------------
# codigo nuevo <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@app.route('/actualizarcursos/<codigo>', methods=['POST'])
def actualizarCursos(codigo):
    if request.method == 'POST':
        codigo = request.form['codigo']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        

        

        #  UPDATE 
        update_query = """
        UPDATE `cursos`
        SET `nombre` = '{0}', `descripcion` = '{1}'
        WHERE `cursos`.`codigo` = %s
        """

        # Formato de  values
        updated_values = [nombre, descripcion]

        # Ejecuto query 
        curCursos = mysql.connection.cursor()
        curCursos.execute(update_query.format(*updated_values), (codigo,))

        # Commit 
        
        curCursos.connection.commit()

        # ============================
        affected_rows = curCursos.rowcount
        if affected_rows > 0:
            print(f"\nSe actualizó el curso con el codigo: {codigo}")
            return redirect(url_for('listarcursos'))
        else:
            print(f"\nNo se encontró el curso con el codigo {codigo}")
            return redirect(url_for('listarcursos'))

 
     
# -------------eliminar cursos -----------------------
@app.route('/eliminarcursos/<string:codigo>')
def eliminarCursos(codigo):
     
       curInst = mysql.connection.cursor()
       curInst.execute('delete from cursos where codigo = {0}'.format (codigo))
       curInst.connection.commit()
       return redirect(url_for('listarcursos'))
   
# --------- Buscar por Codigo el curso ---------------
@app.route('/buscarCursos', methods=['POST'])
def buscarCursos():
    codigo =request.form['codigo']
    curCurso = mysql.connection.cursor()
   
    curCurso.execute('SELECT  * from cursos  where codigo LIKE "%%%s%%"' % (codigo))
    
    datosCursos = curCurso.fetchall()
    
    if datosCursos:
        flash('Resultado de la busqueda de Cursos')
    else:
        flash('No hay resultados para la busqueda de Cursos')
    return render_template('buscadorcursos.html', datosCursos = datosCursos)

# --------- Buscar por Nombre de Cursos---------------
@app.route('/buscarNombreCursos', methods=['POST'])
def buscarNombreCursos():
    nombre =request.form['nombre']
    curCursosNombre = mysql.connection.cursor()
   
    curCursosNombre.execute('SELECT  * FROM cursos  where nombre LIKE "%%%s%%"' % (nombre))
    
    datosCursosNombre = curCursosNombre.fetchall()
    
    if datosCursosNombre:
        flash('Resultado de la busqueda de Cursos')
    else:
        flash('No hay resultados para la busqueda de Cursos')
    return render_template('buscadorcursos.html', datosCursos = datosCursosNombre)

  # --------- Buscar Cursos por Descripcion---------------
@app.route('/buscarDescripcionCursos', methods=['POST'])
def buscarDescripcionCursos():
    descripcion =request.form['descripcion']
    curCursosDesc = mysql.connection.cursor()
    
    curCursosDesc.execute('SELECT  * FROM cursos  where descripcion LIKE "%%%s%%"' % (descripcion))
   
    datosCursosDesc = curCursosDesc.fetchall()
    
    if datosCursosDesc:
        flash('Resultado de la busqueda de Cursos')
    else:
        flash('No hay resultados para la busqueda de Cursos')
    return render_template('buscadorcursos.html', datosCursos = datosCursosDesc) 


# MMMMMMMMMMMMMMMMM FIN CURSOS MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM

# XXXXXXXXXXXXXXXXXXXXXXX COMIENZO DE CURSADA xxxxxxxxxxxxxxxxxxxxx
@app.route('/buscadorcursada')
def buscadorcursada():
    cur = mysql.connection.cursor()
   
   
   
    cur.execute('SELECT * FROM cursada;')
    datosCursada = cur.fetchall()


    flash('Listado de Cursadas')
    return render_template('buscadorcursada.html', datosCursada = datosCursada)
   



# ------------- LISTAR CURSADA CON ORDENAMIENTO ---------------------------------

@app.route('/listarcursada')
def listarcursada():
    order_by = request.args.get('order_by', 'cursada.id_cursada')  # Obtener el parámetro de orden o usar por defecto 'cursada.id_cursada'
    cur = mysql.connection.cursor()
   
    query = f'''
        SELECT 
            cursada.id_cursada, 
            cursos.codigo, 
            cursos.nombre AS curso_nombre,
            instructores.dni AS instructor_dni, 
            instructores.nombre AS instructor_nombre, 
            instructores.apellido AS instructor_apellido, 
            alumnos.dni AS alumno_dni, 
            alumnos.nombre AS alumno_nombre, 
            alumnos.apellido AS alumno_apellido 
        FROM 
            cursada 
        JOIN 
            cursos ON cursada.curso = cursos.codigo 
        JOIN 
           instructores ON cursada.instructor = instructores.dni 
        JOIN 
            alumnos ON cursada.alumnos = alumnos.dni 
        ORDER BY 
            {order_by};

    '''
    
    cur.execute(query)
    datosCursada = cur.fetchall()

    flash('Listado de Cursadas')
    
    return render_template('listarcursada.html', datosCursada=datosCursada, order_by=order_by)





# -------------agregar cursada -----------------------
@app.route('/agregarcursada', methods=['POST','GET'])
def agregarCursada():
    if request.method == 'GET':
        
        cur = mysql.connection.cursor()
        cur.execute('select * from cursada')
        cursada = cur.fetchall()
        
        
       # ------agrego codigo id de cursadas-------------    
        curCursos = mysql.connection.cursor()
        curCursos.execute('SELECT (MAX(id_cursada)+1) AS max_id_cursada FROM cursada')
        datosMaxCursada = curCursos.fetchall()
# --------------cursos -----nuevo ---------
        curCurso = mysql.connection.cursor()
        curCurso.execute('select * from cursos')
        curCurso = curCurso.fetchall()


# --------------instructor -----nuevo ---------
        curInst = mysql.connection.cursor()
        curInst.execute('select * from instructores')
        curInst = curInst.fetchall()
        
# -------------alumno ----------nuevo ---------
        curAlumno = mysql.connection.cursor()
        curAlumno.execute('select  *  from alumnos')
        curAlumno = curAlumno.fetchall() 
        
# -------------alumno ----------nuevo ---------
        curMensajes = mysql.connection.cursor()
        curMensajes.execute('select * from mensajes where id_mensaje = 1')
        curMensajes = curMensajes.fetchall() 
        
       
        
        flash('Cursada Agregada')
        
        return render_template('agregarcursada.html',cursada = cursada, datoMaxId = datosMaxCursada,elcurso = curCurso, instructor = curInst, alumno =  curAlumno, mensaje =  curMensajes)
      
      # *************envio datosCursada a la vista ****************  
      
    elif request.method == 'POST':
        id_cursada = request.form['id_cursada']
        curso = request.form['curso']
        instructor = request.form['instructor']
        alumnos = request.form['alumnos']
        
        
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO cursada (id_cursada, curso, instructor, alumnos) VALUES (%s, %s, %s, %s)', (id_cursada, curso, instructor, alumnos))
        

        cur.connection.commit()
        return  redirect(url_for('listarcursada'))
     

#-------------obtener para EDITAR CURSADA --------------------
@app.route('/obtenercursada/<id_cursada>')
def obtenercursada(id_cursada):
  
         cur = mysql.connection.cursor()
         cur.execute('select * from cursada where id_cursada = %s' % (id_cursada))
         cursada = cur.fetchall()
        
        
 # ------agrego codigo -------------    
         curCursos = mysql.connection.cursor()
         curCursos.execute('select * from cursada')
         datosCursada = curCursos.fetchall()
# --------------cursos -----nuevo ---------
         curCurso = mysql.connection.cursor()
         curCurso.execute('select * from cursos')
         curCurso = curCurso.fetchall()


# --------------instructor -----nuevo ---------
         curInst = mysql.connection.cursor()
         curInst.execute('select * from instructores')
         curInst = curInst.fetchall()
        
# -------------alumno ----------nuevo ---------
         curAlumno = mysql.connection.cursor()
         curAlumno.execute('select  *  from alumnos')
         curAlumno = curAlumno.fetchall()

 # ------ datos del curso segun id_cursada ------------- 
         curDatoCurso = mysql.connection.cursor()
         curDatoCurso.execute('select cursos.codigo, cursos.nombre  from cursos, cursada  where cursos.codigo= cursada.curso and  cursada.id_cursada = %s' % (id_cursada))
         curDatoCurso  = curDatoCurso .fetchall()
         
# ------ datos del alumno  segin id_cursada  ------------- 
         curDatosAlumno = mysql.connection.cursor()
         curDatosAlumno.execute('select alumnos.dni, alumnos.nombre, alumnos.apellido  from alumnos,cursada  where alumnos.dni= cursada.alumnos and  cursada.id_cursada = %s' % (id_cursada))
         curDatosAlumno = curDatosAlumno.fetchall()
         
# ------ datos del instructor segin id:cursada  ------------- 
         
         curDatosInst = mysql.connection.cursor()
         curDatosInst.execute('select instructores.dni, instructores.nombre, instructores.apellido  from instructores,cursada  where instructores.dni= cursada.instructor and  cursada.id_cursada = %s' % (id_cursada))
         curDatosInst = curDatosInst.fetchall()
         
         
        # solo instructor
         return render_template('editarcursada.html', cursada = cursada[0], datoscursada = datosCursada,elcurso = curCurso, instructor = curInst, alumno =  curAlumno, datosInst = curDatosInst, datosAlum = curDatosAlumno, datoCurso = curDatoCurso)
       
# ----------- actualizar -----------------
# codigo nuevo <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@app.route('/actualizarcursada/<id_cursada>', methods=['POST'])
def actualizarcursada(id_cursada):
    if request.method == 'POST':
        
        id_cursada = request.form['id_cursada']
        curso = request.form['curso']
        instructor = request.form['instructor']
        alumnos = request.form['alumnos']   
        
        
        update_query = """
         UPDATE `cursada`
         SET `curso` = \'{0}\', `instructor` = \'{1}\', `alumnos` = \'{2}\' 
         WHERE `cursada`.`id_cursada` = %s
        """
         
       

        # Formato de  values
        updated_values = [curso, instructor, alumnos]

        # Ejecuto query 
        curCursada = mysql.connection.cursor()
        curCursada.execute(update_query.format(*updated_values), (id_cursada,))

        # Commit 
        
        curCursada.connection.commit()

        # ============================
        affected_rows = curCursada.rowcount
        if affected_rows > 0:
            print(f"\nSe actualizó la cursada con el codigo: {id_cursada}")
            return redirect(url_for('listarcursada'))
        else:
            print(f"\nNo se encontró la cursada con el codigo {id_cursada}")
            return redirect(url_for('listarcursada'))

 
     
# -------------eliminar cursada -----------------------
@app.route('/eliminarcursada/<string:id_cursada>')
def eliminarcursada(id_cursada):
     
       curCursada = mysql.connection.cursor()
       curCursada.execute('delete from cursada where id_cursada = {0}'.format (id_cursada))
       curCursada.connection.commit()
       return redirect(url_for('listarcursada'))
   
# --------- Buscar por id_cursada de la cursada ---------------
@app.route('/buscarcursada', methods=['POST'])
def buscarcursada():
    id_cursada =request.form['id_cursada']
    curCursadaId = mysql.connection.cursor()
   
    curCursadaId.execute('SELECT  * from cursada  where id_cursada LIKE "%%%s%%"' % (id_cursada))
    
    datosCursada = curCursadaId.fetchall()
    
    if datosCursada:
        flash('Resultado de la busqueda de Cursada')
    else:
        flash('No hay resultados para la busqueda de Cursasda')
    return render_template('buscadorcursada.html', datosCursada = datosCursada)

# --------- Buscar por Nombre de Curso---------------
@app.route('/buscarNombreCursada', methods=['POST'])
def buscarNombreCursada():
    curso =request.form['curso']
    curCursosNombre = mysql.connection.cursor()
   
    curCursosNombre.execute('SELECT  * FROM cursada  where curso LIKE "%%%s%%"' % (curso))
    
    datosCursadaCurso = curCursosNombre.fetchall()
    
    if datosCursadaCurso:
        flash('Resultado de la busqueda de Cursada por curso')
    else:
        flash('No hay resultados para la busqueda de Cursos')
    return render_template('buscadorcursada.html', datosCursada = datosCursadaCurso)

  # --------- Buscar Cursada por Instructor---------------
@app.route('/buscarInstructorCursada', methods=['POST'])
def buscarInstructorCursada():
    instructor =request.form['instructor']
    curCursadaInstructor = mysql.connection.cursor()
    
    curCursadaInstructor.execute('SELECT  * FROM cursada  where instructor LIKE "%%%s%%"' % (instructor))
   
    datosCursadaInst = curCursadaInstructor.fetchall()
    
    if datosCursadaInst:
        flash('Resultado de la busqueda de Cursada por instructor')
    else:
        flash('No hay resultados para la busqueda de Cursada por instructor')
    return render_template('buscadorcursada.html', datosCursada = datosCursadaInst) 
 
 # --------- Buscar Cursada por Alumno---------------
@app.route('/buscarAlumnoCursada', methods=['POST'])
def buscarAlumnoCursada():
    alumnos =request.form['alumnos']
    curCursadaAlumnos = mysql.connection.cursor()
    
    curCursadaAlumnos.execute('SELECT  * FROM cursada  where alumnos LIKE "%%%s%%"' % (alumnos))
   
    datosCursadaAl = curCursadaAlumnos.fetchall()
    
    if datosCursadaAl:
        flash('Resultado de la busqueda de Cursada por Alumno')
    else:
        flash('No hay resultados para la busqueda de Cursada por Alumno')
    return render_template('buscadorcursada.html', datosCursada = datosCursadaAl) 

# MMMMMMMMMMMMMMMMM FIN CURSOS MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM


# XXXXXXXXXXXXXXXXXXXX comienzo de usuarios xxxxxxxxxxxxxxxxxxxxxxxxx

# XXXXXXXXXXXXXXXX Listado de Usuarios XXXXXXXXXXXXXXXXXXXXXX
@app.route('/listarusuarios')
def listarusuarios():
    sort_by = request.args.get('sort_by', 'id')
    valid_columns = ['id', 'username', 'email', 'role']
    if sort_by not in valid_columns:
        sort_by = 'id'
    
    cur = mysql.connection.cursor()
    query = f'SELECT * FROM users ORDER BY {sort_by}'
    cur.execute(query)
    datos = cur.fetchall()
    cur.close()
    
    flash('Listado de Usuarios')
    return render_template('listarusuarios.html', datos_usuarios=datos)

# ---------------------Buscar Usuario --------------------------
@app.route('/buscarusuario', methods=['POST'])
def buscarusuario():
    search_query = request.form['search_query']
    cur = mysql.connection.cursor()
    query = """
    SELECT * FROM users 
    WHERE id = %s OR username LIKE %s OR email LIKE %s OR role LIKE %s
    """
    cur.execute(query, (search_query, f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
    resultados = cur.fetchall()
    cur.close()
    if resultados:
        return render_template('listarusuarios.html', datos_usuarios=resultados)
    else:
        flash('No se encontraron usuarios con los criterios de búsqueda.', 'danger')
        return redirect(url_for('listarusuarios'))
# ---------------------Obtener Usuario --------------------------

@app.route('/obtenerusuario/<id>')
def obtenerusuario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE id = %s', [id])
    usuario = cur.fetchone()
    cur.close()
    return render_template('editarusuario.html', usuario=usuario)

# ---------------------Actualizar  Usuario --------------------------

@app.route('/actualizarusuario/<id>', methods=['POST'])
def actualizarusuario(id):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE users
            SET username = %s, email = %s, password = %s, role = %s
            WHERE id = %s
        """, (username, email, password, role, id))
        mysql.connection.commit()
        cur.close()

        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('listarusuarios'))
    
# ---------------------Eliminar Usuario --------------------------

@app.route('/eliminarusuario/<string:id>')
def eliminarusuario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE id = %s', [id])
    mysql.connection.commit()
    cur.close()
    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('listarusuarios'))




# ------------------------
if __name__ == '__main__':
    app.run(port=3000,debug=True)
