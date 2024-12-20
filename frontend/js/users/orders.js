document.addEventListener("DOMContentLoaded", () => {
    // Verificar si el usuario está autenticado al cargar la página
    const token = localStorage.getItem('token');
    if (!token) {
         // Redirigir al usuario a la página de login si no hay token
        window.location.href = "login.html";
    } else {
        // Cargar productos, proveedores y órdenes de compra si el usuario está autenticado
        loadProducts();
        loadSuppliers();
        fetchPurchaseOrders();
    }
    // Asociar el evento de submit del formulario a la función registerPurchaseOrder
    document.getElementById('order-form').addEventListener('submit', handleFormSubmission(registerPurchaseOrder));
});

// Función para envolver la función de manejo de eventos del formulario y prevenir el comportamiento por defecto
function handleFormSubmission(callback) {
    return function (event) {
        event.preventDefault(); // Prevenir la recarga de la página al enviar el formulario
        callback(); // Llamar a la función pasada como argumento (ej. registerPurchaseOrder)
    };
}

// Variables globales para almacenar el token, ID de usuario y nombre de usuario
const token = localStorage.getItem('token');
const user_id = localStorage.getItem('id');
const username = localStorage.getItem('username');

// Elementos del DOM para la navegación lateral (sidebar)
const openSidebarButton = document.getElementById('openSidebar');
const closeSidebarButton = document.getElementById('closeSidebar');
const sidebar = document.getElementById('sidebar');

// Evento para abrir la barra lateral
openSidebarButton.addEventListener('click', () => {
    sidebar.setAttribute('aria-hidden', 'false');
    sidebar.classList.add('visible');
});

// Evento para cerrar la barra lateral
closeSidebarButton.addEventListener('click', () => {
    sidebar.setAttribute('aria-hidden', 'true');
    sidebar.classList.remove('visible');
});

// Evento para cerrar la barra lateral al hacer clic en un enlace
const navLinks = sidebar.querySelectorAll('nav ul li a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        sidebar.setAttribute('aria-hidden', 'true');
        sidebar.classList.remove('visible');
    });
});

/**
 * Función para llenar las listas de productos en el formulario.
 * @param {Array} products - Lista de productos a mostrar.
 */
function populateProductLists(products) {
    const productSelect = document.getElementById('productSelect');
    productSelect.innerHTML = '<option value="">Seleccione un producto</option>';
    // Si no hay productos, mostrar un mensaje indicativo
    if (!products.length) {
        productSelect.innerHTML = '<option>No hay productos disponibles</option>';
        return;
    }
    // Llenar la lista de productos con las opciones correspondientes
    products.forEach(product => {
        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = product.name;
        productSelect.appendChild(option);
    });

    // Agregar evento 'change' para cargar proveedores al seleccionar un producto
    productSelect.addEventListener('change', () => {
        const selectedProductId = productSelect.value;
        if (selectedProductId) {
            loadSuppliersByProduct(selectedProductId); // Nueva función para cargar proveedores por producto
        } else {
            // Si no se selecciona un producto, mostrar mensaje
            document.getElementById('supplier-id').innerHTML = '<option value="">Seleccione un producto primero</option>';
        }
    });
}

/**
 * Función para cargar productos desde la API.
 * @param {number|null} supplierId - ID del proveedor para filtrar productos (opcional).
 */
function loadProducts(supplierId = null) {
    const productSelect = document.getElementById('productSelect');
    productSelect.innerHTML = '<option value="">Cargando...</option>';

    // Construir la URL de la API para obtener productos, con filtro opcional por proveedor
    let url = apiURL + `/user/${user_id}/products`;
    if (supplierId) {
        url += `?supplier_id=${supplierId}`; // Filtrar por proveedor si existe el parámetro
    }

    // Realizar la solicitud a la API para obtener productos
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => handleResponse(response)) // Manejar la respuesta de la API
    .then(result => {
        populateProductLists(result.data);// Llenar la lista de productos con la respuesta
    })
    .catch(error => {
        console.error('Error al cargar productos:', error);
        productSelect.innerHTML = '<option>Error al cargar productos</option>'; // Mensaje de error
    });
}

/**
 * Función para cargar proveedores desde la API y mostrarlos en el dropdown.
 */
function loadSuppliers() {
    const supplierDropdown = document.getElementById('supplier-id');

    // Realizar la solicitud a la API para obtener proveedores
    fetch(apiURL + `/user/${user_id}/suppliers`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => response.json()) // Convertir la respuesta a JSON
    .then(data => {
        supplierDropdown.innerHTML = '<option value="">-- Seleccione un proveedor --</option>'; // Opción por defecto

        // Si hay proveedores, llenar el dropdown con las opciones correspondientes
        if (Array.isArray(data) && data.length > 0) {
            data.forEach(supplier => {
                const option = document.createElement('option');
                option.value = supplier.id;
                option.textContent = `${supplier.name_supplier} (ID: ${supplier.id})`;
                supplierDropdown.appendChild(option);
            });
        } else {
            supplierDropdown.innerHTML = '<option>No hay proveedores disponibles</option>'; // Mensaje si no hay proveedores
        }
    })
    .catch(error => {
        console.error('Error cargando proveedores:', error);
        supplierDropdown.innerHTML = '<option>Error cargando proveedores</option>'; // Mensaje de error
    });
}

/**
 * Función para cargar proveedores asociados a un producto específico desde la API.
 * @param {number} productId - ID del producto para el cual se cargarán los proveedores.
 */
function loadSuppliersByProduct(productId) {
    const supplierSelect = document.getElementById('supplier-id');
    supplierSelect.innerHTML = '<option value="">Cargando...</option>'; // Mensaje de carga

    // Realizar la solicitud a la API para obtener proveedores de un producto específico
    fetch(apiURL + `/user/${user_id}/products/${productId}/supplier`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => {
        // Manejar errores de respuesta no exitosa
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message || "Error desconocido del servidor.");
            });
        }
        return response.json();
    })
    .then(suppliers => {
        supplierSelect.innerHTML = '<option value="">Seleccione un proveedor</option>'; // Limpiar opciones existentes

        // Llenar el dropdown de proveedores con los proveedores asociados al producto
        if (Array.isArray(suppliers) && suppliers.length > 0) {
            suppliers.forEach(supplier => {
                const option = document.createElement('option');
                option.value = supplier.id;
                option.textContent = `${supplier.name_supplier} (ID: ${supplier.id})`;
                supplierSelect.appendChild(option);
            });
        } else {
            supplierSelect.innerHTML = '<option value="">No hay proveedores para este producto</option>'; // Mensaje si no hay proveedores
        }
    })
    .catch(error => {
        console.error('Error al cargar proveedores:', error);
        supplierSelect.innerHTML = '<option value="">Error al cargar proveedores</option>'; // Mensaje de error
    });
}

/**
 * Función para mostrar un mensaje al usuario.
 * @param {string} text - Texto del mensaje.
 * @param {string} type - Tipo de mensaje ('success' o 'error').
 * @param {string} elementId - ID del elemento HTML donde se mostrará el mensaje.
 */
function showMessage(text, type, elementId) {
    const messageElement = document.getElementById(elementId);
    messageElement.textContent = text;
    messageElement.style.color = type === 'success' ? 'green' : 'red'; // Color verde para éxito, rojo para error
}


/**
 * Función para recopilar los datos del producto seleccionado en el formulario.
 * @returns {{products: Array<{product_id: number, quantity: number}>}|null} - Objeto con los datos del producto o null si hay campos incompletos.
 */
function collectProductData() {
    const supplier = document.getElementById('supplier-id').value;
    const product_id = document.getElementById('productSelect').value;
    const quantity = parseInt(document.getElementById('total-quantity').value, 10);

    // Validación de campos requeridos
    if (!supplier || !product_id || isNaN(quantity)) {
        showMessage('Por favor, complete todos los campos.', 'error', `OrderRegisterMessage`);
        return null;
    }
    // Crear un array de objetos con los datos del producto
    const products = [{ product_id, quantity }];
    return { products };
}

/**
 * Función para registrar una nueva orden de compra.
 */
function registerPurchaseOrder() {
    const data = collectProductData();
    if (!data) return; // Si hay datos inválidos, retorna

    fetch(apiURL + `/user/${user_id}/orders`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify(data)  
    })
    .then(response => {
        if (!response.ok) {
            // Intenta obtener un mensaje de error más específico del servidor
            throw new Error('Error al registrar la orden');
        }
        return response.json();
    })
    .then(responseData => {
        // Mostrar mensaje de éxito y limpiar el formulario
        showMessage('orden registrada exitosamente.', 'success', 'OrderRegisterMessage');
        document.getElementById('order-form').reset();
        loadProducts(); // Recargar la lista de productos
        fetchPurchaseOrders();// Recargar la lista de órdenes de compra
    })
    .catch(error => {
        // Mostrar mensaje de error
        showMessage(error.message, 'error', 'OrderRegisterMessage');
    });
}

/**
 * Función para obtener y mostrar las órdenes de compra del usuario.
 */
function fetchPurchaseOrders() {
    // Realizar la solicitud a la API para obtener las órdenes de compra
    fetch(apiURL + `/user/${user_id}/orders`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token 
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al obtener las órdenes de compra.');
        }
        return response.json();
    })
    .then(result => {
        // Si la respuesta no es un array, lanzar un error 
        if (!Array.isArray(result.data)) {
            throw new Error('La respuesta no es un arreglo de órdenes.');
        }
        renderPurchaseOrders(result.data); // Renderiza las órdenes en la interfaz
    })
    .catch(error => {
        showMessage(`Error: ${error.message}`, 'error', 'OrderListMessage');
    });
}

/**
 * Función para mostrar una ventana modal con los detalles de una orden específica.
 * @param {Object} order - Objeto que representa la orden de compra.
 */
function showOrderDetails(order) {
    const modal = document.getElementById('orderModal');
    const modalContent = document.getElementById('modal-order-details');
    modalContent.innerHTML = ''; // Limpiar contenido anterior

    // Formatear la fecha de la orden para mostrarla en formato DD/MM/YYYY
    const orderDate = new Date(order.order_date);
    const formattedOrderDate = orderDate.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });

    // Formatear la fecha de recepción (si existe), o mostrar 'Sin Confirmar'
    let formattedReceivedDate = 'Sin Confirmar';
    if (order.received_date) {
        const receivedDate = new Date(order.received_date);
        formattedReceivedDate = receivedDate.toLocaleDateString('es-ES', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric'
        });
    }

    // Construir el contenido HTML con los detalles de la orden
    const orderInfo = `
        <div>
            <strong>ID:</strong> ${order.id}<br>
            <strong>Fecha de Orden:</strong> ${formattedOrderDate}<br>
            <strong>Fecha de Recepción:</strong> ${formattedReceivedDate}<br>
            <strong>Estado:</strong> ${order.status}<br>
            <strong>Productos:</strong>
            <ul>
                ${order.products.map(product => `
                    <li>Producto ID: ${product.product_id}, Cantidad: ${product.quantity}</li>
                `).join('')}
            </ul>
        </div>
    `;

    modalContent.innerHTML = orderInfo;
    modal.style.display = 'block'; // Mostrar la ventana modal
}

// Evento para cerrar la ventana modal al hacer clic en el botón de cerrar
document.getElementById('closeModal').addEventListener('click', () => {
    document.getElementById('orderModal').style.display = 'none';
});


/**
 * Función para renderizar las órdenes de compra en la interfaz de usuario.
 * @param {Array} orders - Lista de órdenes de compra a renderizar.
 */
function renderPurchaseOrders(orders) {
    const orderListContainer = document.getElementById('order-list');
    orderListContainer.innerHTML = ''; // Limpiar la lista de órdenes

    // Si no hay órdenes, mostrar un mensaje indicativo
    if (orders.length === 0) {
        orderListContainer.innerHTML = '<p>No hay órdenes de compra registradas.</p>';
        return;
    }

    // Iterar sobre cada orden para crear su representación en la interfaz
    orders.forEach(order => {
        const orderElement = document.createElement('div');
        orderElement.className = 'order';

        // Determinar si los botones deben estar habilitados o no basado en order.status
        const isPending = order.status === 'pending';
        const confirmButtonDisabledAttribute = isPending ? '' : 'disabled';
        const deleteButtonDisabledAttribute = isPending ? '' : 'disabled'; // Aplicar la misma lógica al botón Eliminar

        // Construir el HTML para cada orden con la información y los botones de acción
        const orderInfo = `
            <strong>ID:</strong> ${order.id}
            <strong>Estado:</strong> ${order.status}
            <button class="view-details-btn" data-order-id="${order.id}">Ver Detalles</button>
            <button class="delete-order-btn" data-order-id="${order.id}" ${deleteButtonDisabledAttribute}>Eliminar Orden</button>
            <button class="confirm-order-btn" data-order-id="${order.id}" ${confirmButtonDisabledAttribute}>Confirmar</button>`;

        orderElement.innerHTML = orderInfo;
        orderListContainer.appendChild(orderElement);

        // Evento para el botón "Ver Detalles"
        const viewDetailsButton = orderElement.querySelector('.view-details-btn');
        viewDetailsButton.addEventListener('click', () => {
            showOrderDetails(order);
        });

        // Evento para el botón "Eliminar Orden"
        const deleteButton = orderElement.querySelector('.delete-order-btn');
        deleteButton.addEventListener('click', () => {
            // Verificar si el estado es "pending" antes de proceder
            if (order.status === 'pending') {
                if (confirm('¿Estás seguro de que deseas eliminar esta orden?')) {
                    deleteOrder(order.id); // Llama a la función directamente
                }
            } else {
                alert('Solo las órdenes pendientes pueden ser eliminadas.');
            }
        });

        // Evento para el botón "Confirmar"
        const confirmButton = orderElement.querySelector('.confirm-order-btn');
        confirmButton.addEventListener('click', () => {
            // Verificar si el estado es "pending" antes de proceder
            if (order.status === 'pending') {
                if (confirm('¿Estás seguro de que deseas confirmar esta orden?')) {
                    confirmOrder(order.id); // Llama a la función directamente
                }
            } else {
                alert('Solo las órdenes pendientes pueden ser confirmadas.');
            }
        });
    });
    }



/**
 * Función para eliminar una orden de compra por su ID.
 * @param {number} orderId - ID de la orden a eliminar.
 */
function deleteOrder(orderId) {
    clearMessage('OrderRegisterMessage'); // Limpia cualquier mensaje previo

    fetch(apiURL + `/user/${user_id}/orders/${orderId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => {
        if (!response.ok) {
            // Leer el cuerpo de la respuesta para obtener el mensaje de error específico
            return response.json().then(errorData => {
                throw new Error(errorData.message || 'Error al eliminar la orden');
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        fetchPurchaseOrders(); // Actualiza la lista después de eliminar
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message || 'No se pudo eliminar la orden.');
    });
}


/**
 * Función para confirmar una orden de compra por su ID.
 * Actualiza la fecha de recepción de la orden a la fecha actual.
 * @param {number} orderId - ID de la orden a confirmar.
 */
function confirmOrder(orderId) {
    clearMessage('OrderRegisterMessage'); // Limpia cualquier mensaje previo

    // Obtener la fecha actual en formato YYYY-MM-DD
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];

    // Realizar la solicitud a la API para confirmar la orden
    fetch(apiURL + `/user/${user_id}/orders/${orderId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify({ received_date: formattedDate }) // Enviar la fecha en formato YYYY-MM-DD
    })
    .then(response => {
        // Si la respuesta no es exitosa, intentar obtener el mensaje de error
        if (!response.ok) {
            return response.text().then(text => {
                // Intentar parsear como JSON, si falla usar el texto plano
                try {
                    const errorData = JSON.parse(text);
                    throw new Error(errorData.error || 'Error al confirmar la orden');
                } catch (e) {
                    throw new Error(text || 'Error al confirmar la orden');
                }
            });
        }
        return response.json(); // Si es exitosa, parsear como JSON
    })
    .then(data => {
        // Mostrar mensaje de éxito
        alert(data.message);
        fetchPurchaseOrders(); // Actualizar la lista de órdenes de compra
    })
    .catch(error => {
        // Mostrar mensaje de error
        console.error('Error:', error);
        alert(error.message || 'No se pudo confirmar la orden.');
    });
}

/**
 * Función para limpiar el contenido de un elemento de mensaje en la interfaz.
 * @param {string} elementId - ID del elemento HTML que contiene el mensaje.
 */
function clearMessage(elementId) {
    const messageElement = document.getElementById(elementId);
    if (messageElement) {
        messageElement.textContent = ''; // Limpia el contenido del mensaje
    }
}
