// unificar con stock2 donde se uusan los showmensage

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

    // Llamar a checkLowStock automáticamente al cargar la página
    checkLowStock();

});
// Se cargan globalmente los datos de usuario//------------------------------------>consultar con los compañeros si las pasamos globalmente o dentro de cada funcion
//le pasamos lo que requiera
const token = localStorage.getItem('token');
const user_id = localStorage.getItem('id');
const username = localStorage.getItem('username'); 

// Función para verificar el stock bajo y mostrar advertencia
function checkLowStock() {
    const user_id = localStorage.getItem('id');
    const notificationIcon = document.getElementById('notification-icon'); // Obtener el icono de notificación

    fetch(`http://localhost:5000/user/${user_id}/stock/low`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': localStorage.getItem('token') //--->si la definimos globalmente, directamente le pasamos el parametro: x-access-token': token
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            throw new Error(result.error);
        }
        const lowStockList = result.data; 
        if (lowStockList.length > 0) {
            const formattedMessage = lowStockList.map(item => 
                `Producto ID: ${item.product_id}\nNombre: ${item.product_name}\nCantidad: ${item.quantity}\n\n`
            ).join('');
            alert(`Advertencia: Los siguientes productos tienen stock bajo:\n\n${formattedMessage}`);
            if (notificationIcon) {
                notificationIcon.classList.add('alert'); // Usar la clase 'alert'
            }
        } else {
            alert('No hay productos con stock bajo.');
            if (notificationIcon) {
                notificationIcon.classList.remove('alert'); // Usar la clase 'alert'
            }
        }
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


// Función para actualizar el stock de un producto
function updateStock() {
    const product_id = document.getElementById('productId').value;
    const newQuantity = document.getElementById('newQuantity').value;
    const messageElement = document.getElementById('updateStockMessage');

    if (!product_id || !newQuantity) {
        messageElement.textContent = 'Por favor, complete todos los campos.';
        messageElement.style.color = 'red';
        return; 
    }
    // Confirmar la actualización con el usuario
    const confirmUpdate = confirm(`¿Está seguro que desea actualizar el producto ${product_id} a una cantidad de ${newQuantity} unidades?`);
    if (!confirmUpdate) {
        return; // Salir si el usuario cancela
    }

    startSpinner(); // Mostrar el spinner de carga

    const data = {
        quantity: Number(newQuantity) 
    };

    // Enviar la solicitud PUT al servidor
    fetch(`http://localhost:5000/user/${user_id}/stock/${product_id}`, { 
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': localStorage.getItem('token') 
        },
        body: JSON.stringify(data) 
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            throw new Error(result.error); 
        }
        messageElement.textContent = result.message;
        messageElement.style.color = 'green'; 
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
        stopSpinner();
    });
}

// Función para mostrar mensajes de información, error o éxito al usuario
function showMessage(text, type) {
    const messageElement = document.getElementById('updateStockMessage');
    messageElement.textContent = text;
    messageElement.style.color = type === 'error' ? 'red' : 'green';
}

// Funciones auxiliares para mostrar/ocultar el spinner de carga
function startSpinner() {
    document.getElementById('loading-spinner').style.display = 'inline-block';
}

function stopSpinner() {
    document.getElementById('loading-spinner').style.display = 'none';
}

// Función para cerrar la sesión del usuario
function userLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('id');
    localStorage.removeItem('username');
    window.location.href = "login.html"; 
}
