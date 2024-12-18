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

// Llenar la lista de productos
function populateProductLists(products) {
    const productSelect = document.getElementById('productSelect');
    productSelect.innerHTML = '<option value="">Seleccione un producto</option>';

    if (!products.length) {
        productSelect.innerHTML = '<option>No hay productos disponibles</option>';
        return;
    }

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
            document.getElementById('supplier-id').innerHTML = '<option value="">Seleccione un producto primero</option>';
        }
    });
}

// Cargar productos asociados a un proveedor específico
function loadProducts(supplierId = null) {
    const productSelect = document.getElementById('productSelect');
    productSelect.innerHTML = '<option value="">Cargando...</option>';

    let url = apiURL + `/user/${user_id}/products`;
    if (supplierId) {
        url += `?supplier_id=${supplierId}`; // Filtrar por proveedor si existe el parámetro
    }

    fetch(url, {
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
    .catch(error => {
        console.error('Error al cargar productos:', error);
        productSelect.innerHTML = '<option>Error al cargar productos</option>';
    });
}

// Cargar proveedores
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
        supplierDropdown.innerHTML = '<option value="">-- Seleccione un proveedor --</option>';

        if (Array.isArray(data) && data.length > 0) {
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

    // Eliminamos este evento change:
    // supplierDropdown.addEventListener('change', () => { ... });
}

// Función para cargar proveedores por producto seleccionado
function loadSuppliersByProduct(productId) {
    const supplierSelect = document.getElementById('supplier-id');
    supplierSelect.innerHTML = '<option value="">Cargando...</option>';

    fetch(apiURL + `/user/${user_id}/products/${productId}/supplier`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => {
                throw new Error(err.message || "Error desconocido del servidor.");
            });
        }
        return response.json();
    })
    .then(suppliers => {
        supplierSelect.innerHTML = '<option value="">Seleccione un proveedor</option>'; // Limpiar opciones

        if (Array.isArray(suppliers) && suppliers.length > 0) {
            suppliers.forEach(supplier => {
                const option = document.createElement('option');
                option.value = supplier.id;
                option.textContent = `${supplier.name_supplier} (ID: ${supplier.id})`;
                supplierSelect.appendChild(option);
            });
        } else {
            supplierSelect.innerHTML = '<option value="">No hay proveedores para este producto</option>';
        }
    })
    .catch(error => {
        console.error('Error al cargar proveedores:', error);
        supplierSelect.innerHTML = '<option value="">Error al cargar proveedores</option>';
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
        fetchPurchaseOrders();
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

// Función para mostrar la ventana modal con los detalles de la orden
function showOrderDetails(order) {
    const modal = document.getElementById('orderModal');
    const modalContent = document.getElementById('modal-order-details');
    modalContent.innerHTML = ''; // Limpiar contenido anterior

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

    modalContent.innerHTML = orderInfo;
    modal.style.display = 'block'; // Mostrar la ventana modal
}

// Función para cerrar la ventana modal
document.getElementById('closeModal').addEventListener('click', () => {
    document.getElementById('orderModal').style.display = 'none';
});

function renderPurchaseOrders(orders) {
    const orderListContainer = document.getElementById('order-list');
    orderListContainer.innerHTML = '';

    if (orders.length === 0) {
        orderListContainer.innerHTML = '<p>No hay órdenes de compra registradas.</p>';
        return;
    }

    orders.forEach(order => {
        const orderElement = document.createElement('div');
        orderElement.className = 'order';

        // Determinar si los botones deben estar habilitados o no basado en order.status
        const isPending = order.status === 'pending';
        const confirmButtonDisabledAttribute = isPending ? '' : 'disabled';
        const deleteButtonDisabledAttribute = isPending ? '' : 'disabled'; // Aplicar la misma lógica al botón Eliminar

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
                    deleteOrder(order.id).then(() => {
                        fetchPurchaseOrders(); // Actualiza la lista después de eliminar
                    }).catch(error => {
                        console.error('Error al eliminar la orden:', error);
                        alert('No se pudo eliminar la orden. Intenta de nuevo.');
                    });
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
                    confirmOrder(order.id).then(() => {
                        fetchPurchaseOrders(); // Actualiza la lista después de confirmar
                    }).catch(error => {
                        console.error('Error al confirmar la orden:', error);
                        alert('No se pudo confirmar la orden. Intenta de nuevo.');
                    });
                }
            } else {
                alert('Solo las órdenes pendientes pueden ser confirmadas.');
            }
        });
    });
}


// Function to delete an order
function deleteOrder(orderId) {
    if (!user_id || !token) {
        alert('No estás autenticado para eliminar órdenes.');
        return;
    }

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
                throw new Error(errorData.message || 'Error al eliminar la orden'); // Usa el mensaje de la API o un mensaje genérico si no hay mensaje
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        fetchPurchaseOrders();
    })
    .catch(error => {
        console.error('Error:', error);
        alert(error.message || 'No se pudo eliminar la orden.'); // Muestra el mensaje de error específico o un mensaje genérico
    });
}

function confirmOrder(orderId) {
    return new Promise((resolve, reject) => {
        if (!user_id || !token) {
            reject('No estás autenticado para confirmar órdenes.');
            return;
        }

        fetch(apiURL + `/user/${user_id}/orders/${orderId}`, {
            method: 'PUT',
            headers: {
                'x-access-token': token // Ya no incluimos 'Content-Type': 'application/json'
            },
            body: null // Enviamos body como null
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.message || 'Error al confirmar la orden');
                });
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            resolve();
        })
        .catch(error => {
            console.error('Error:', error);
            reject(error.message || 'No se pudo confirmar la orden.');
        });
    });
}