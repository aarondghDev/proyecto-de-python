document.addEventListener("DOMContentLoaded", init); //esta linea hace que corra la funcion search() al cargar la pagina
const URL_API = 'http://localhost:3000/api/'

var customers = []

function init() {
    search()
}

async function search() {
    var url = URL_API + 'customers'
    var response = await fetch(url, {
        "method": 'GET',
        "headers": {
            "Content-Type": 'application/json'
        }
    })

    customers = await response.json();

    console.log(customers);// esto nos muestra por consola la base de datos del url que le dijimos

    var html = ''
    for (customer of customers){
        var row = `<tr> 
        <td> ${customer.firstname}</td>
        <td>${customer.lastname}</td>
        <td>${customer.email}</td>
        <td>${customer.phone}</td>
        <td>${customer.address}</td>
        <td>
        <button onclick="remove(${customer.id})" class="btnDelete">Eliminar</button>
        <button onclick="edit(${customer.id})" class="myButton">Editar</button>
        </td>
    </tr> `

    html = html + row
    }
    

    document.querySelector('#customers > tbody').outerHTML = html
}

function edit(id) {
 abrirFormulario()
var customer = customers.find(x => x.id == id)
document.getElementById('txtId').value = customer.id
document.getElementById('txtFirstname').value = customer.firstname
document.getElementById('txtLastname').value = customer.lastname
document.getElementById('txtPhone').value = customer.phone
document.getElementById('txtEmail').value = customer.email
document.getElementById('txtAddress').value = customer.address
}

async function remove(id){
    respuesta = confirm('Estas seguro de eliminarlo?')
    if (respuesta) {
        var url = URL_API + 'customers/' + id
        await fetch(url, {
        "method": 'DELETE',
        "headers": {
            "Content-Type": 'application/json'
        }
    })
    window.location.reload();
    }
}

function clean() {
    document.getElementById('txtId').value = ''
    document.getElementById('txtFirstname').value = ''
    document.getElementById('txtLastname').value = ''
    document.getElementById('txtPhone').value = ''
    document.getElementById('txtEmail').value = ''
    document.getElementById('txtAddress').value = ''
}

async function save(){
    var data = {
        "address": document.getElementById('txtAddress').value,
        "email": document.getElementById('txtEmail').value,
        "firstname": document.getElementById('txtFirstname').value,
        "lastname": document.getElementById('txtLastname').value,
        "phone": document.getElementById('txtPhone').value
    }
    
    var id = document.getElementById('txtId').value
    if (id != '') {
        data.id = id
    }
        var url = URL_API + 'customers'
        await fetch(url, {
        "method": 'POST',
        "body": JSON.stringify(data),
        "headers": {
            "Content-Type": 'application/json'
        }
    })
    window.location.reload();
}

function agregar(){
    clean();
    abrirFormulario();
}

function abrirFormulario() {
    htmlModal = document.getElementById('modal');
    htmlModal.setAttribute('class', 'modale opened');
  }

  function cerrarModal() {
    htmlModal = document.getElementById('modal');
    htmlModal.setAttribute('class', 'modal');
  }



