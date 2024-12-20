document.addEventListener("DOMContentLoaded", () => {
    // Cargar el token de localStorage y verificar autenticación
    const token = localStorage.getItem('token');
    const user_id = localStorage.getItem('id');
    const username = localStorage.getItem('username');

    if (!token) {
        // Si no existe un token, se redirige a la página de login
        window.location.href = "login.html";
    } else {
        document.getElementById("Welcome_username").innerHTML = username;       
        // Event listeners para los botones de los modales
        const openModalInventarioButton = document.querySelector('[onclick="openModal(\'modalInventario\')"]');
        if (openModalInventarioButton) {
            openModalInventarioButton.addEventListener('click', () => {
                fetchInventory(user_id, token);
            });
        }

        const openModalBajoStockButton = document.querySelector('[onclick="openModal(\'modalBajoStock\')"]');
        if (openModalBajoStockButton) {
            openModalBajoStockButton.addEventListener('click', () => {
                fetchLowStock(user_id, token);
            });
        }

        const openModalListaOrdenesButton = document.querySelector('[onclick="openModal(\'modalListaOrdenes\')"]');
        if (openModalListaOrdenesButton) {
            openModalListaOrdenesButton.addEventListener('click', () => {
                fetchPurchaseOrders(user_id, token);
            });
        }
    }
});

function fetchInventory(user_id, token) {
    fetch(`${apiURL}/user/${user_id}/stock`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al obtener el inventario.');
        }
        return response.json();
    })
    .then(result => {
        populateInventoryList(result);
    })
    .catch(error => {
        handleFetchError(error, 'modal-inventario-lista');
    });
}

function populateInventoryList(stock) {
    const inventoryList = document.getElementById('modal-inventario-lista');
    inventoryList.innerHTML = '';

    if (Array.isArray(stock) && stock.length > 0) {
        stock.forEach(item => {
            const listItem = document.createElement('li');
            listItem.textContent = `${item.product_name}, ${item.quantity} unidades`;
            inventoryList.appendChild(listItem);
        });
    } else {
        inventoryList.innerHTML = '<li>No hay productos en el inventario.</li>';
    }
}

// Función para obtener los productos con bajo stock
function fetchLowStock(user_id, token) {
    fetch(`${apiURL}/user/${user_id}/stock/low`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al obtener los productos con bajo stock.');
        }
        return response.json();
    })
    .then(result => {
        populateLowStockList(result.data);
    })
    .catch(error => {
        handleFetchError(error, 'modal-bajo-stock-lista');
    });
}

// Función para separar la lógica de llenado de la lista de bajo stock
function populateLowStockList(products) {
    const lowStockList = document.getElementById('modal-bajo-stock-lista');
    lowStockList.innerHTML = '';

    if (Array.isArray(products) && products.length > 0) {
        products.forEach(product => {
            const listItem = document.createElement('li');
            listItem.textContent = `ID: ${product.product_id}, Nombre: ${product.product_name}, Cantidad: ${product.quantity}`;
            lowStockList.appendChild(listItem);
        });
    } else {
        lowStockList.innerHTML = '<li>No hay productos con bajo stock.</li>';
    }
}

// Función para obtener y mostrar la lista de órdenes
function fetchPurchaseOrders(user_id, token) {
    // Corregido: Eliminado fetchfetch y se usan user_id y token del contexto
    fetch(`${apiURL}/user/${user_id}/orders`, {
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
        if (!Array.isArray(result.data)) {
            throw new Error('La respuesta no es un arreglo de órdenes.');
        }
        renderPurchaseOrders(result.data);
    })
    .catch(error => {
        handleFetchError(error, 'modal-lista-ordenes-lista');
    });
}

// Función para renderizar las órdenes de compra en el modal
function renderPurchaseOrders(orders) {
    const ordersList = document.getElementById('modal-lista-ordenes-lista');
    ordersList.innerHTML = '';

    if (orders.length > 0) {
        orders.forEach(order => {
            const listItem = document.createElement('li');

            // Formatear la fecha de orden
            const orderDate = new Date(order.order_date);
            const formattedOrderDate = orderDate.toLocaleDateString('es-ES', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });

            // Formatear la fecha de recepción (si existe)
            let formattedReceivedDate = 'Pendiente';
            if (order.received_date) {
                const receivedDate = new Date(order.received_date);
                formattedReceivedDate = receivedDate.toLocaleDateString('es-ES', {
                    day: '2-digit',
                    month: '2-digit',
                    year: 'numeric'
                });
            }

            listItem.innerHTML = `
                ID: ${order.id}<br>
                Fecha de Orden: ${formattedOrderDate}<br>
                Fecha de Recepción: ${formattedReceivedDate}<br>
                Estado: ${order.status}
            `;
            ordersList.appendChild(listItem);
        });
    } else {
        const listItem = document.createElement('li');
        listItem.textContent = 'No hay órdenes de compra registradas.';
        ordersList.appendChild(listItem);
    }
}

// Función para manejar errores de fetch
function handleFetchError(error, modalListId) {
    console.error('Error:', error);
    const listElement = document.getElementById(modalListId);
    if (listElement) {
        listElement.innerHTML = '';
        const errorItem = document.createElement('li');
        errorItem.textContent = `Error: ${error.message}`;
        listElement.appendChild(errorItem);
    }
}

// Funciones de accesibilidad y manejo del sidenav (estas deberían estar en common.js)
const openSidebarButton = document.getElementById('openSidebar');
const closeSidebarButton = document.getElementById('closeSidebar');
const sidebar = document.getElementById('sidebar');

if (openSidebarButton && closeSidebarButton && sidebar) {
    openSidebarButton.addEventListener('click', () => {
        sidebar.setAttribute('aria-hidden', 'false');
        sidebar.classList.add('visible');
    });

    closeSidebarButton.addEventListener('click', () => {
        sidebar.setAttribute('aria-hidden', 'true');
        sidebar.classList.remove('visible');
    });

    const navLinks = sidebar.querySelectorAll('nav ul li a');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            sidebar.setAttribute('aria-hidden', 'true');
            sidebar.classList.remove('visible');
        });
    });
}

// Funciones para abrir y cerrar modales (estas deberían estar en common.js)
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "block";
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "none";
    }
}

window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = "none";
    }
}

// Función de cierre de sesión (userLogout) - debe estar en common.js
function userLogout() {
    // Eliminar token y user_id del localStorage
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');

    // Redirigir al usuario a la página de login
    window.location.href = 'login.html';
}