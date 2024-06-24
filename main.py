from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aaron0412'
app.config['MYSQL_DB'] = 'system'
mysql = MySQL(app)

@app.route('/api/customers/<int:id>') #GET por defecto
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, firstname, lastname, email, phone, address FROM customers WHERE id =' + str(id))
    data = cur.fetchall()                   #el fetchall trae toda la info, que pudimos haberlo hecho desde la consulta pero da igual
    for row in data:
        return jsonify({
            'id':row[0],
            'firstname':row[1],
            'lastname':row[2],
            'email':row[3],
            'phone': row[4],
            'address': row[5]
        })


@app.route('/api/customers') #GET por defecto
@cross_origin()
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, firstname, lastname, email, phone, address FROM customers')
    data = cur.fetchall()                   #el fetchall trae toda la info, que pudimos haberlo hecho desde la consulta pero da igual
    result = []
    for row in data:
        content = {
                'id':row[0],
                'firstname':row[1],
                'lastname':row[2],
                'email':row[3],
                'phone': row[4],
                'address': row[5]
             }
        result.append(content)
    return jsonify(result)

@app.route('/api/customers', methods=['POST'])
@cross_origin()
def saveUpdateCustomer():
    if 'id' in request.json:
        updateCustomer()
    else:
        saveCustomer()
    return 'ok'

#@app.route('/customers', methods=['POST'])#aqui le indicamos el tipode d ato de la solicitud como otro argumento
def saveCustomer():
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO `customers` (`id`, `firstname`, `lastname`, `email`, `phone`, `address`) VALUES (NULL, %s, %s, %s, %s, %s);",
                (request.json['firstname'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address']))
    mysql.connection.commit()
    return 'Cliente guardado'

#@app.route('/customers', methods=['PUT'])#aqui le indicamos el tipode d ato de la solicitud como otro argumento
def updateCustomer():
    cur = mysql.connection.cursor()
    cur.execute("UPDATE `customers` SET `firstname` = %s,"
                " `lastname` = %s,"
                " `email` = %s,"
                " `phone` = %s,"
                " `address` = %s WHERE `customers`.`id` = %s;",
                (request.json['firstname'], request.json['lastname'], request.json['email'], request.json['phone'], request.json['address'], request.json['id']))
    mysql.connection.commit()
    return 'Cliente actualizado'

@app.route('/api/customers/<int:id>', methods=['DELETE'])#aqui le indicamos el tipode d ato de la solicitud como otro argumento y hay que indicarle el id del cliente a eliminar, si no se lo indicamos eliminaria todos los clientes
@cross_origin()
def removeCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM `customers` WHERE `customers`.`id` = " + str(id) +";")
    mysql.connection.commit()
    return 'Cliente eliminado'


@app.route('/')#esto es una decoracion que nos saldra cuando estemos en la ruta que le digamos, si le decimos solo / sera la main por defecto
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/<path:path>')#este '<path:path>' va a permitir aceptar cualquier ruta
@cross_origin()
def publicFiles(path):#esta funcio puede ser cualquier nombre, recibira la ruta como parametro
    return render_template(path)#y al cargar, cargara la ruta

if __name__ == '__main__':
    app.run(None, 3000,True)