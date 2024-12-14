document.addEventListener("DOMContentLoaded", () => {
    // Cargar el token de localStorage
    const token = localStorage.getItem('token');
    if (!token) {
        // Si no existe un token, se redirige a la página de login
        window.location.href = "login.html";
    } else {
        loadCategories(); // Cargar las categorías cuando la página se carga
    }

    // Añadir evento al formulario para registrar una nueva categoría
    document.getElementById('registerCategoryForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir el comportamiento por defecto del formulario
        registerCategory(); // Llamar a la función para registrar la categoría
    });

    // Añadir evento al formulario para registrar una nueva categoría
    document.getElementById('updateCategoryForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir el comportamiento por defecto del formulario
        updateCategory(); // Llamar a la función para registrar la categoría
    });
});

// Se cargan globalmente los datos de usuario
const token = localStorage.getItem('token');
const user_id = localStorage.getItem('id');

const username = localStorage.getItem('username');
document.getElementById("Welcome_username").innerHTML = username;

// Función para cargar las categorías en el desplegable
function loadCategories() {
    fetch(`http://localhost:5000/user/${user_id}/categories`, {
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
            li.textContent = `${category.name}: ${category.descripcion}`; // Asumiendo que también tienes una descripción
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
function registerCategory() {
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

    fetch(`http://localhost:5000/user/${user_id}/categories`, {
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
        loadCategories(); // Recargar las categorías para reflejar el cambio
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
function updateCategory() {
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

    fetch(`http://localhost:5000/user/${user_id}/categories/${category_id}`, {
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
        loadCategories(); // Recargar las categorías para reflejar el cambio
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