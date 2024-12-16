document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = "login.html";
    } else {
        loadProducts();
        loadSuppliers();
        fetchPurchaseOrders();
    }
    document.getElementById('order-form').addEventListener('submit', handleFormSubmission(registerPurchaseOrder));
});

function handleFormSubmission(callback) {
    return function (event) {
        event.preventDefault();
        callback();
    };
}

// Variables globales
const token = localStorage.getItem('token');
const user_id = localStorage.getItem('id');
const username = localStorage.getItem('username');

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
    const productSelect = document.getElementById('productSelect');
    productSelect.innerHTML = '<option value="">Seleccione un producto </option>';

    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = product.name;
        productSelect.appendChild(option);
    });
}

function loadProducts() {
    fetch(apiURL + `/user/${user_id}/products`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => handleResponse(response))
    .then(result => {
        populateProductLists(result.data);
    })
    .catch(error => showMessage(error.message, 'error', 'OrderListMessage'));
}

function loadSuppliers() {
    const supplierDropdown = document.getElementById('supplier-id');
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

function showMessage(text, type, elementId) {
    const messageElement = document.getElementById(elementId);
    messageElement.textContent = text;
    messageElement.style.color = type === 'success' ? 'green' : 'red';
}

function collectProductData() {
    const supplier = document.getElementById('supplier-id').value;
    const product_id = document.getElementById('productSelect').value;
    const quantity = parseInt(document.getElementById('total-quantity').value, 10);

    // Validación de campos requeridos
    if (!supplier || !product_id || isNaN(quantity)) {
        showMessage('Por favor, complete todos los campos.', 'error', `OrderRegisterMessage`);
        return null;
    }
    const products = [{ product_id, quantity }]; // Array de objetos con los datos del producto
    return { products };
}

function registerPurchaseOrder() {
    const data = collectProductData();
    if (!data) return; // Si hay datos inválidos, sale

    fetch(apiURL + `/user/${user_id}/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify(data)  // Asegúrate de que esto es un JSON válido
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar la orden');
        }
        return response.json();
    })
    .then(responseData => {
        showMessage('orden registrada exitosamente.', 'success', 'OrderRegisterMessage');
        document.getElementById('order-form').reset();
        loadProducts(); // Llama a la función para actualizar la lista de productos
    })
    .catch(error => {
        showMessage(error.message, 'error', 'OrderRegisterMessage');
    });
}

function fetchPurchaseOrders() {
    fetch(apiURL + `/user/${user_id}/orders`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token // Asegúrate de pasar el token del usuario para la autenticación
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al obtener las órdenes de compra.');
        }
        return response.json();
    })
    .then(result => { // Cambiamos de 'orders' a 'result' para reflejar el objeto completo
        console.log(result); // Verificar el contenido de la respuesta
        // Verifica si la propiedad 'data' es un arreglo
        if (!Array.isArray(result.data)) {
            throw new Error('La respuesta no es un arreglo de órdenes.');
        }
        renderPurchaseOrders(result.data); // Renderiza las órdenes en la interfaz
    })
    .catch(error => {
        showMessage(`Error: ${error.message}`, 'error', 'OrderListMessage');
    });
}

function renderPurchaseOrders(orders) {
    const orderListContainer = document.getElementById('order-list'); // Asumiendo que tienes un contenedor para órdenes
    orderListContainer.innerHTML = ''; // Limpia las órdenes existentes

    if (orders.length === 0) {
        orderListContainer.innerHTML = '<p>No hay órdenes de compra registradas.</p>';
        return;
    }

    orders.forEach(order => {
        const orderElement = document.createElement('div');
        orderElement.className = 'order';

        const orderInfo = `
            <div>
                <strong>ID:</strong> ${order.id}<br>
                <strong>Fecha de Orden:</strong> ${order.order_date}<br>
                <strong>Fecha de Recepción:</strong> ${order.received_date || 'Pendiente'}<br>
                <strong>Estado:</strong> ${order.status}<br>
                <strong>Productos:</strong>
                <ul>
                    ${order.products.map(product => `
                        <li>Producto ID: ${product.product_id}, Cantidad: ${product.quantity}</li>
                    `).join('')}
                </ul>
            </div>
        `;

        orderElement.innerHTML = orderInfo;
        orderListContainer.appendChild(orderElement);
    });
}
