document.addEventListener("DOMContentLoaded", () => {
    // Cargar el token de localStorage
    const token = localStorage.getItem('token');
    if (token){
        const username = localStorage.getItem('username'); 
        document.getElementById("username").innerHTML = username;
    }
    else{
        // Si no existe un token, se redirige a la página de login
        window.location.href = "login.html";
    }
});

// Se cargan globalmente los datos de usuario
const token = localStorage.getItem('token');
const id_user = localStorage.getItem('id');
const username = localStorage.getItem('username'); 

var userCategories = []
var userServices = []

function showMessage(text, type){
    // Elemento para mostrar mensajes al usuario
    const messageElement = document.getElementById("message");
    messageElement.classList.remove('error', 'success', 'info');

    // Mostrar un mensaje de carga
    messageElement.innerHTML = text;

    // type : 'info' | 'success' | 'error'
    messageElement.classList.add(type); 
}

function userLogout(){
    // Borrar los datos del almacenamiento local
    localStorage.removeItem('token');
    localStorage.removeItem('id');
    localStorage.removeItem('username');

    // Redigir a la página de login, a index, o la que corresponda
    window.location.href = "login.html";
}

function loadServicesByUser(){
    showMessage("Cargando sus servicios...", 'info'); 
    
    // Configuración de la solicitud
    const requestOptions = {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            "x-access-token": token
        }
    };

    // Realizar la solicitud de creación de usuario
    fetch(`${apiURL}/user/${id_user}/service`, requestOptions)
        .then(response => handleResponse(response))
        .then(response => {
            // Servicios cargados correctamente
            console.log(response)

            userServices =  response;
            const servicesTableBody = document.querySelector('#services-table tbody');
            servicesTableBody.innerHTML = '';
            userServices.forEach(service => {
                const row = document.createElement('tr');
                row.id = `${service.id}`;
                row.innerHTML = `
                    <td>${service.nombre}</td>
                    <td>${service.precio}</td>
                    <td>${service.descripcion}</td>
                    <td>${service.categoria}</td>
                    <td>
                        <button class="action-btn" onclick="editService(${service.id})">Editar</button>
                        <button class="action-btn delete-btn" onclick="deleteService(${service.id})">Eliminar</button>
                        <button class="action-btn details-btn" onclick="viewService(${service.id})">Detalles</button>
                    </td>
                `;
                servicesTableBody.appendChild(row);
            });
            showMessage("Servicios cargados correctamente",'success');            
        })
        .catch(error => {
            // Hubo algún error, ya sea en respueta de la API o error de conexión
            if (error.message === "Failed to fetch") {
                showMessage("No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.", 'error');
            } else {
                let text = error.message || "Error al cargar los servicios";
                showMessage(text, 'error');
            }
        })
        .finally(() => {
            // 
        });
    
}

function loadCategoriesByUser(){
    showMessage("Cargando categorias de servicios...", 'info');
    // Configuración de la solicitud
    const requestOptions = {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            "x-access-token": token
        }
    };

    // Realizar la solicitud de creación de usuario
    fetch(`${apiURL}/user/${id_user}/category`, requestOptions)
        .then(response => handleResponse(response))
        .then(response => {
            // Categorías cargadas correctamente
            console.log(response)

            // AQUI LA CARGA DE VALORES EN EL SELECTOR
            userCategories = response;
            const categorySelect = document.getElementById('service-category');
            categorySelect.innerHTML = '';
            userCategories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.nombre;
                categorySelect.appendChild(option);
            });

            showMessage("Categorías cargados correctamente", 'success');
        })
        .catch(error => {
            // Hubo algún error, ya sea en respueta de la API o error de conexión
            if (error.message === "Failed to fetch") {
                showMessage("No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.", 'error');
            } else {
                let text = error.message || "Error al cargar las categorias";
                showMessage(text, 'error');
            }
        })
        .finally(() => {
            // 
        });
}


loadCategoriesByUser();
loadServicesByUser();


// funcion para deshabilitar botones durante la edición o carga, sólo se activa el correspondiente
function disableButtons(){
    const buttons = document.getElementsByTagName('button');
    console.log(buttons);
    for (let i=0; i < buttons.length; i++){
        buttons[i].disabled = true;
    }
}
// funcion para habilitar botones al finalizar la edición o carga
function enableButtons(){
    const buttons = document.getElementsByTagName('button');
    console.log(buttons);
    for (let i=0; i < buttons.length; i++){
        buttons[i].disabled = false;
    }
}
function editService(id){
    disableButtons();
    var row = document.getElementById(id);
    for (let i = 0; i < 3; i++){
        row.children[i].contentEditable = true;
        row.children[i].classList.toggle('on-edit');
    }
    const selector = document.createElement('select');
    userCategories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id;
        option.textContent = category.nombre;
        selector.appendChild(option);
    });
    
    const tdata = row.children[3];
    tdata.innerHTML = '';
    tdata.appendChild(selector);

    row.children[4].innerHTML = `
        <td>
            <button class="action-btn" onclick="saveService(${id})">Guardar</button>
            <button class="action-btn" onclick="cancelEdit(${id})">Cancelar</button>
        </td>
    `;
}

function cancelEdit(){
    loadServicesByUser();    
    enableButtons();
}


function saveService(id_service){
    showMessage('Guardando cambios...', 'info');
    
    // Obtener los valores
    const row = document.getElementById(id_service);

    //const nombreCategoria = row.children[3].textContent;
    //const id_categoria = userCategories.filter(cat => cat.nombre == nombreCategoria)[0].id;
    const selector = row.querySelector('select'); 
    const id_categoria = selector.value;

    const data = {
        nombre : row.children[0].textContent,
        precio: Number(row.children[1].textContent),
        descripcion: row.children[2].textContent,
        id_categoria:id_categoria
    }

    console.log("nuevos valores=", data)
    // Configuración de la solicitud
    const requestOptions = {
        method: 'PUT',
        headers: {
            "Content-Type": "application/json",
            "x-access-token": token
        },
        body: JSON.stringify(data)
    };

    // Realizar la solicitud de creación de servicio
    fetch(`${apiURL}/user/${id_user}/service/${id_service}`, requestOptions)
        .then(response => handleResponse(response))
        .then(response => {
            // Cambios guardados correctamente
            console.log(response)
            showMessage("Servicio creado correctamente", 'success');
            loadServicesByUser();           
        })
        .catch(error => {
            // Hubo algún error, ya sea en respueta de la API o error de conexión
            if (error.message === "Failed to fetch") {
                showMessage("No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.", 'error');
            } else {
                let text = error.message || "Error al guardar los cambios";
                showMessage(text, 'error');
            }
        })
        .finally(() => {
            enableButtons(); 
        });
}

function deleteService(id_service){      
    // Confirmacion para eliminar
    if (!confirm("Está seguro..?")){  
        return
    }

    showMessage("Eliminando servicio...", 'info');    
    
    // Configuración de la solicitud
    const requestOptions = {
        method: 'DELETE',
        headers: {
            "Content-Type": "application/json",
            "x-access-token": token
        }
    };

    // Realizar la solicitud de eliminacion de un servicio
    fetch(`${apiURL}/user/${id_user}/service/${id_service}`, requestOptions)
        .then(response => handleResponse(response))
        .then(response => {
            // Cambios guardados correctamente
            console.log(response)
            showMessage("Servicio borrado correctamente...", 'success')
            loadServicesByUser();           
        })
        .catch(error => {
            // Hubo algún error, ya sea en respueta de la API o error de conexión
            if (error.message === "Failed to fetch") {
                showMessage("No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.", 'error');
            } else {
                let text = error.message || "Error al borrar el servicio";
                showMessage(text, 'error');
            }
        })
        .finally(() => {
            // 
        });
}

function addService(){
    showMessage("Agregando nuevo servicio...", 'info');
    
    // Obtener los valores
    const name = document.getElementById('service-name').value;
    const price = document.getElementById('service-price').value;
    const description = document.getElementById('service-description').value;
    const category = document.getElementById('service-category').value;

    // Controlar los valores
    if ((name =="") || (price < 0) || (description == "") ){
        showMessage("Debe completar todos los campos", 'error');
        return
    }
    const data = {
        nombre : name,
        precio: Number(price),
        descripcion: description,
        id_categoria: Number(category)
    }

    // Configuración de la solicitud
    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "x-access-token": token
        },
        body: JSON.stringify(data)
    };

    // Realizar la solicitud de creación de servicio
    fetch(`${apiURL}/user/${id_user}/service`, requestOptions)
        .then(response => handleResponse(response))
        .then(response => {
            // Servicio agregado correctamente
            console.log(response)
            showMessage("Servicio agregado correctamente", 'success');
            loadServicesByUser();           
        })
        .catch(error => {
            // Hubo algún error, ya sea en respueta de la API o error de conexión
            if (error.message === "Failed to fetch") {
                showMessage("No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.", 'error');
            } else {
                let text = error.message || "Error al agregar el servicio";
                showMessage(text, 'error');
            }
        })
        .finally(() => {
            enableButtons(); 
        });
}