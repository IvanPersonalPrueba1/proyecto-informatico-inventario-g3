document.addEventListener('DOMContentLoaded', () => {
    const openBtn = document.getElementById('openSidebar');
    const closeBtn = document.getElementById('closeSidebar');
    const sidebar = document.getElementById('sidebar');

    // Abrir el sidebar
    openBtn.addEventListener('click', () => {
        sidebar.classList.add('open');
    });

    // Cerrar el sidebar
    closeBtn.addEventListener('click', () => {
        sidebar.classList.remove('open');
    });
});

// Función para cerrar la sesión del usuario
function userLogout() {
    localStorage.clear(); // Limpia todos los datos del almacenamiento
    window.location.href = "login.html";
}

const username = localStorage.getItem('username');
document.getElementById("Welcome_username").innerHTML = username;