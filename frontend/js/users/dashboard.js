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

function getProductsByUser(){
    const token = localStorage.getItem('token');
    const id = localStorage.getItem('id');
    if ((token) && (id)){
        console.log("Cargando productos");

        // Elemento para mostrar mensajes al usuario
        const messageElement = document.getElementById("message");
        messageElement.classList.remove('error', 'success');

        // Elementos para mostrar una animación de carga sobre el botón del formulario
        const submitBtn = document.getElementById('load-products-btn');
        const spinner = document.getElementById('loading-spinner');

        // Mostrar un mensaje de carga
        messageElement.innerHTML = "Cargando sus productos...";
        // Mostrar el spinner y desactivar el botón mientras se procesa la solicitud
        spinner.style.display = 'inline-block';
        submitBtn.disabled = true;

        // Configuración de la solicitud
        const requestOptions = {
            method: 'GET',
            headers: {
                "Content-Type": "application/json",
                "x-access-token": token
            }
        };

        // Realizar la solicitud de creación de usuario
        fetch(`${apiURL}/user/${id}/product`, requestOptions)
            .then(response => handleResponse(response))
            .then(response => {
                // Productos cargados correctamente
                console.log(response)
                messageElement.innerHTML = "Productos cargados correctamente";
                messageElement.classList.add('success');            
            })
            .catch(error => {
                // Hubo algún error, ya sea en respueta de la API o error de conexión
                if (error.message === "Failed to fetch") {
                    messageElement.innerHTML = "No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.";
                } 
                else if (error.message === "Signature has expired"){
                    alert("Su sesión ha expirado, debe volver a ingresar");
                    window.location.href = "login.html"
                }
                else {
                    messageElement.innerHTML = error.message || "Error al cargar los productos";
                }
                messageElement.classList.add('error');
                messageElement.classList.add('error');
            })
            .finally(() => {
                // Ocultar el spinner y activar el botón nuevamente
                spinner.style.display = 'none';
                submitBtn.disabled = false;
            });
        }
}