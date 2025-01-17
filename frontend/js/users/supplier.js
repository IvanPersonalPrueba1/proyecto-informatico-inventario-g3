document.addEventListener("DOMContentLoaded", () => {
    // Cargar el token de localStorage y verificar autenticación
    const token = localStorage.getItem('token');
    const user_id = localStorage.getItem('id');

    if (token) {
        // Cargar productos en stock en el desplegable
        loadProducts(user_id, token);

        // Cargar proveedores en el desplegable
        loadSuppliers(user_id, token);

        loadProductsSelect(user_id, token);

        // Configurar el evento de clic para el botón de registrar proveedor
        const registerSupplierBtn = document.getElementById('registerSupplierBtn');
        if (registerSupplierBtn) {
            registerSupplierBtn.addEventListener('click', () => registerSupplier(user_id, token)); 
        } else {
            console.error("Elemento con ID 'registerSupplierBtn' no encontrado");
        }

        // Configurar el evento de clic para el botón de vincular proveedor
        const linkSupplierBtn = document.getElementById('linkSupplierBtn');
        if (linkSupplierBtn) {
            linkSupplierBtn.addEventListener('click', () => linkProductToSupplier(user_id, token));
        } else {
            console.error("Elemento con ID 'linkSupplierBtn' no encontrado");
        }

        // Configurar el evento de clic para el botón de consultar proveedores
        const getSuppliersBtn = document.getElementById('getSuppliersBtn');
        if (getSuppliersBtn) {
            getSuppliersBtn.addEventListener('click', () => getSuppliersByProduct(user_id, token)); 
        } else {
            console.error("Elemento con ID 'getSuppliersBtn' no encontrado");
        }
    } else {
        // Redirigir al login si no hay token
        window.location.href = "login.html";
    }
});

const username = localStorage.getItem('username');
document.getElementById("Welcome_username").innerHTML = username;


// Mostrar mensajes al usuario
function showMessage(text, type) {
    const messageElement = document.getElementById("message");
    if (messageElement) {
        messageElement.classList.remove('error', 'success', 'info');
        messageElement.innerHTML = text;
        messageElement.classList.add(type);
    }
}

// Cargar productos en el dropdown
function loadProducts(user_id, token) {
    const productDropdown = document.getElementById('product_id');

    fetch(apiURL + `/user/${user_id}/stock`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (Array.isArray(data) && data.length > 0) {
            productDropdown.innerHTML = '';

            // Agregar opción predeterminada
            const defaultOption = document.createElement('option');
            defaultOption.textContent = '-- Seleccione un producto --';
            defaultOption.value = '';
            productDropdown.appendChild(defaultOption);

            data.forEach(product => {
                const option = document.createElement('option');
                option.value = product.product_id;
                option.textContent = `${product.product_name} (ID: ${product.product_id})`; // Muestra ambos valores
                productDropdown.appendChild(option);
            });
        } else {
            productDropdown.innerHTML = '<option>No hay productos disponibles</option>';
        }
    })
    .catch(error => {
        console.error('Error cargando productos:', error);
        productDropdown.innerHTML = '<option>Error cargando productos</option>';
    });
}

// Cargar proveedores en el dropdown
function loadSuppliers(user_id, token) {
    const supplierDropdown = document.getElementById('supplier_id');
    fetch(apiURL + `/user/${user_id}/suppliers`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => response.json())
    .then(data => {
        if (Array.isArray(data) && data.length > 0) {
            supplierDropdown.innerHTML = '';

            // Agregar opción predeterminada
            const defaultOption = document.createElement('option');
            defaultOption.textContent = '-- Seleccione un proveedor --';
            defaultOption.value = '';
            supplierDropdown.appendChild(defaultOption);

            // Cargar proveedores en el dropdown
            data.forEach(supplier => {
                const option = document.createElement('option');
                option.value = supplier.id;
                option.textContent = `${supplier.name_supplier} (ID: ${supplier.id})`;
                supplierDropdown.appendChild(option);
            });
        } else {
            supplierDropdown.innerHTML = '<option>No hay proveedores disponibles</option>';
        }
    })
    .catch(error => {
        console.error('Error cargando proveedores:', error);
        supplierDropdown.innerHTML = '<option>Error cargando proveedores</option>';
    });
}

// Función para registrar un nuevo proveedor
function registerSupplier(user_id, token) {
    const name_supplier = document.getElementById('name_supplier').value;
    const phone = document.getElementById('phone').value;
    const mail = document.getElementById('mail').value;
    const messageElement = document.getElementById('registerSupplierMessage');

    if (!name_supplier || !phone || !mail) {
        messageElement.textContent = 'Por favor, complete todos los campos.';
        messageElement.style.color = 'red';
        return; 
    }

    const data = {
        name_supplier,
        phone,
        mail
    };

    fetch(apiURL + `/user/${user_id}/supplier`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            // Si la respuesta no es OK, analizar el cuerpo de la respuesta para obtener el error
            return response.json().then(data => { 
                throw new Error(data.message); // Lanza un error con el mensaje del backend
            });
        }
        return response.json();
    })
    .then(result => {
        if (result.error) {
            throw new Error(result.error);
        }
        messageElement.textContent = 'Proveedor registrado exitosamente';
        messageElement.style.color = 'green';

        // Recargar proveedores en el dropdown
        loadSuppliers(user_id, token);
    })
    .catch(error => {
        messageElement.textContent = `Error: ${error.message}`;
        messageElement.style.color = 'red';
    });
}

// Función para vincular un producto a un proveedor
function linkProductToSupplier(user_id, token) {
    const supplier_id = document.getElementById('supplier_id').value;
    const product_id = document.getElementById('product_id').value;
    const messageElement = document.getElementById('linkSupplierMessage'); 

    if (!supplier_id || !product_id) {
        messageElement.textContent = 'Por favor, seleccione un proveedor y un producto.';
        messageElement.style.color = 'red';
        return; 
    }

    fetch(apiURL + `/user/${user_id}/suppliers/${supplier_id}/products/${product_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => {
        if (!response.ok) {
            // Si la respuesta no es OK, analizar el cuerpo de la respuesta para obtener el error
            return response.json().then(data => { 
                throw new Error(data.message); // Lanza un error con el mensaje del backend
            });
        }
        return response.json();
    })
    .then(result => {
        if (result.error) {
            throw new Error(result.error); // Si el servidor devuelve un error en el cuerpo de la respuesta
        }
        messageElement.textContent = 'Producto vinculado al proveedor exitosamente';
        messageElement.style.color = 'green';
    })
    .catch(error => {
        // Si se captura un error, mostramos el mensaje adecuado
        messageElement.textContent = `Error: ${error.message}`;
        messageElement.style.color = 'red';
    });
}

// Función para consultar proveedores por producto
function getSuppliersByProduct(user_id, token) {
    const product_id = document.getElementById('consult_product_id').value;
    const messageElement = document.getElementById('suppliersListMessage');
    const suppliersTableBody = document.querySelector('#suppliersTable tbody');
    const modal = document.getElementById('supplierModal');

    // Limpiar mensajes previos
    messageElement.textContent = '';
    messageElement.style.color = '';

    if (!product_id) {
        messageElement.textContent = 'Por favor, ingrese el ID del producto.';
        messageElement.style.color = 'red';
        return;
    }

    fetch(apiURL + `/user/${user_id}/products/${product_id}/supplier`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => {
        if (!response.ok) {
            // Capturar errores enviados desde el backend
            return response.json().then(err => {
                throw new Error(err.message || "Error desconocido del servidor.");
            });
        }
        return response.json();
    })
    .then(data => {
        suppliersTableBody.innerHTML = ''; // Limpiar la tabla de proveedores

        // Verificar si hay proveedores
        if (Array.isArray(data) && data.length > 0) {
            data.forEach(supplier => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${supplier.id}</td>
                    <td>${supplier.name_supplier}</td>
                    <td>${supplier.phone}</td>
                    <td>${supplier.mail}</td>
                `;
                suppliersTableBody.appendChild(row);
            });
        } else {
            const row = document.createElement('tr');
            row.innerHTML = `<td colspan="4">No se encontraron proveedores para este producto.</td>`;
            suppliersTableBody.appendChild(row);
        }

        // Mostrar el modal con los proveedores
        modal.style.display = 'block';
    })
    .catch(error => {
        // Mostrar errores del backend
        messageElement.textContent = error.message;
        messageElement.style.color = 'red';
    });
}

// Cerrar el modal cuando se haga clic en la 'x'
document.getElementById('closeModal').addEventListener('click', () => {
    const modal = document.getElementById('supplierModal');
    modal.style.display = 'none';
});

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

function populateProductLists(products) {
    const productSelect = document.getElementById('consult_product_id');

    productSelect.innerHTML = '';

    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = product.name;
        productSelect.appendChild(option);
    });
}


 //Carga los productos del usuario en el select 'consult_product_id'.
function loadProductsSelect(user_id, token) {
    // Realiza una petición GET a la API para obtener la lista de productos del usuario.
    fetch(apiURL + `/user/${user_id}/products`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json', // Indica que la petición es de tipo JSON.
            'x-access-token': token // Incluye el token de autenticación en la cabecera.
        }
    })
    .then(response => handleResponse(response)) // Llama a la función handleResponse para gestionar la respuesta.
    .then(result => {
        // Si la respuesta es exitosa, llama a la función populateProductSelect para llenar el select.
        // result.data contiene la lista de productos.
        populateProductSelect(result.data);
    })
    .catch(error => showMessage(error.message, 'error', 'ProductListMessage')); // Captura cualquier error y muestra un mensaje.
}


//Llena el select 'consult_product_id' con la lista de productos proporcionada.
function populateProductSelect(products) {
    // Obtiene la referencia al elemento select con id 'consult_product_id'.
    const productSelect = document.getElementById('consult_product_id');

    // Limpia el contenido actual del select (elimina cualquier opción existente).
    productSelect.innerHTML = '';

    // Crea la opción predeterminada '-- Seleccione un producto --'.
    const defaultOption = document.createElement('option');
    defaultOption.textContent = '-- Seleccione un producto --'; // Texto que se muestra al usuario.
    defaultOption.value = ''; // Valor vacío para la opción por defecto.
    productSelect.appendChild(defaultOption); // Agrega la opción por defecto al select.

    // Itera sobre cada producto en la lista de productos.
    products.forEach(product => {
        // Crea un nuevo elemento 'option' para cada producto.
        const option = document.createElement('option');
        option.value = product.id; // Establece el valor de la opción como el ID del producto.
        option.textContent = product.name; // Establece el texto de la opción como el nombre del producto.
        productSelect.appendChild(option); // Agrega la opción del producto al select.
    });
}

// Función para cerrar la sesión del usuario
function userLogout() {
    localStorage.clear(); // Limpia todos los datos del almacenamiento
    window.location.href = "login.html";
}