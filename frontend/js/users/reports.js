// Función para cerrar la sesión del usuario
function userLogout() {
    localStorage.clear(); // Limpia todos los datos del almacenamiento
    window.location.href = "login.html";
}

// Verifica si el usuario está autenticado
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = "login.html";
    } else {
        const username = localStorage.getItem('username');
        document.getElementById("username").textContent = username; // Asegúrate de que el ID coincida
    }
});

