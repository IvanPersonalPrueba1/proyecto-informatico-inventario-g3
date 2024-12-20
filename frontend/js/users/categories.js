document.addEventListener("DOMContentLoaded", () => {
    // Cargar el token de localStorage
    const token = localStorage.getItem('token');
    const user_id = localStorage.getItem('id');
    if (!token) {
        // Si no existe un token, se redirige a la página de login
        window.location.href = "login.html";
    } else {
        loadCategories(user_id, token); // Cargar las categorías cuando la página se carga
    }

    // Añadir evento al formulario para registrar una nueva categoría
    document.getElementById('registerCategoryForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir el comportamiento por defecto del formulario
        registerCategory(user_id, token); // Llamar a la función para registrar la categoría
    });

    // Añadir evento al formulario para registrar una nueva categoría
    document.getElementById('updateCategoryForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir el comportamiento por defecto del formulario
        updateCategory(user_id, token); // Llamar a la función para registrar la categoría
    });
});

const username = localStorage.getItem('username');
document.getElementById("Welcome_username").innerHTML = username;

// Función para cargar las categorías en el desplegable
function loadCategories(user_id, token) {
    fetch(apiURL + `/user/${user_id}/categories`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            throw new Error(result.error);
        }

        const categoryList = document.getElementById('category-list');
        const categorySelect = document.getElementById('category_id'); // Referencia al select
        categoryList.innerHTML = ''; // Limpiar la lista anterior
        categorySelect.innerHTML = ''; // Limpiar el select anterior

        result.data.forEach(category => {
            // Crear un elemento de lista
            const li = document.createElement('li');
            li.textContent = `${category.name}: ${category.descripcion}`;
            categoryList.appendChild(li);

            // Crear una opción para el select
            const option = document.createElement('option');
            option.value = category.id; // Usar el id de la categoría como valor
            option.textContent = category.name; // Nombre de la categoría como texto
            categorySelect.appendChild(option);
        });
    })
    .catch(error => {
        showMessage(error.message || "Error al cargar las categorías", 'error', 'registerCategoryMessage');
    });
}

// Función para registrar una nueva categoría
function registerCategory(user_id, token) {
    const name = document.getElementById('name_category').value;
    const description = document.getElementById('description').value;

    if (!name || !description) {
        showMessage('Por favor, complete todos los campos.', 'error', 'registerCategoryMessage');
        return;
    }

    const data = {
        name: name,
        descripcion: description
    };

    fetch(apiURL + `/user/${user_id}/categories`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            throw new Error(result.error);
        }
        showMessage('Categoría creada exitosamente', 'success', 'registerCategoryMessage');
        document.getElementById('registerCategoryForm').reset(); // Reiniciar el formulario
        loadCategories(user_id,token); // Recargar las categorías para reflejar el cambio
    })
    .catch(error => {
        if (error.message === "Failed to fetch") {
            showMessage("No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.", 'error', 'registerCategoryMessage');
        } else {
            showMessage(error.message || "Error al crear la categoría", 'error', 'registerCategoryMessage');
        }
    });
}


// Función para modificar una categoría existente
function updateCategory(user_id, token) {
    const category_id = document.getElementById('category_id').value;
    const new_name = document.getElementById('new_name_category').value;
    const new_description = document.getElementById('new_description').value;

    if (!category_id || !new_name || !new_description) {
        showMessage('Por favor, complete todos los campos.', 'error', 'updateCategoryMessage');
        return;
    }

    const data = {
        name: new_name,
        descripcion: new_description
    };

    fetch(apiURL + `/user/${user_id}/categories/${category_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            throw new Error(result.error);
        }
        showMessage('Categoría actualizada exitosamente', 'success', 'updateCategoryMessage');
        document.getElementById('updateCategoryForm').reset(); // Reiniciar el formulario
        loadCategories(user_id, token); // Recargar las categorías para reflejar el cambio
    })
    .catch(error => {
        if (error.message === "Failed to fetch") {
            showMessage("No se pudo conectar con el servidor. Verifique su conexión o intente más tarde.", 'error', 'updateCategoryMessage');
        } else {
            showMessage(error.message || "Error al actualizar la categoría", 'error', 'updateCategoryMessage');
        }
    });
}

// Función para mostrar mensajes de información, error o éxito al usuario
function showMessage(text, type, elementId) {
    const messageElement = document.getElementById(elementId);
    messageElement.textContent = text;
    if (type === 'error') {
        messageElement.style.color = 'red';
    } else if (type === 'success') {
        messageElement.style.color = 'green';
    } else if (type === 'warning') {
        messageElement.style.color = 'orange';
    }
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
    localStorage.clear(); // Limpia todos los datos del almacenamiento
    window.location.href = "login.html";
}

// Accesibilidad y funcionalidad del sidenav
const openSidebarButton = document.getElementById('openSidebar');
const closeSidebarButton = document.getElementById('closeSidebar');
const sidebar = document.getElementById('sidebar');

// Al abrir el sidenav
openSidebarButton.addEventListener('click', () => {
    sidebar.setAttribute('aria-hidden', 'false');
    sidebar.classList.add('visible');
});

// Al cerrar el sidenav
closeSidebarButton.addEventListener('click', () => {
    sidebar.setAttribute('aria-hidden', 'true');
    sidebar.classList.remove('visible');
});

// Cierra el sidenav al hacer clic en un enlace
const navLinks = sidebar.querySelectorAll('nav ul li a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        sidebar.setAttribute('aria-hidden', 'true');
        sidebar.classList.remove('visible');
    });
});
