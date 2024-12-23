document.addEventListener("DOMContentLoaded", () => {
    // Cargar el token de localStorage y verificar autenticación
    const token = localStorage.getItem('token');
    const user_id = localStorage.getItem('id');
    const username = localStorage.getItem('username');

    if (!token) {
        // Si no existe un token, se redirige a la página de login
        window.location.href = "login.html";
    } else {
        document.getElementById("username").innerHTML = username;
        // Si existe un token, se ejecutan las siguientes acciones       
        loadProducts(user_id, token); // Cargar productos en el dropdown
        loadProductsInStock(user_id, token);        
        checkLowStock(user_id, token); // Se ejecuta checkLowStock solo si hay token
    }
});

function loadProducts(user_id, token) {
    fetch(apiURL + `/user/${user_id}/products`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) throw new Error(result.error);
        populateProductLists(result.data);
    })
    .catch(error => showMessage(error.message, 'error'));
}

function populateProductLists(products) {
    const productSelect = document.getElementById('productId');
    if (productSelect) {
        productSelect.innerHTML = '<option value="">Seleccione un producto</option>'; // Opción inicial

        if (Array.isArray(products) && products.length > 0) {
            products.forEach(product => {
                const option = document.createElement('option');
                option.value = product.id;
                option.textContent = product.name;
                productSelect.appendChild(option);
            });
        } else {
            console.log("No hay productos disponibles o no se cargaron correctamente.");
        }
    } else {
        console.log("No se encontró el elemento de selección de productos.");
    }
}

function loadProductsInStock(user_id, token) {
    fetch(apiURL + `/user/${user_id}/stock`, {  
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) throw new Error(result.error);

        populateStockProducts(result);  // Pasa los datos directamente
    })
    .catch(error => showMessage(error.message, 'error', 'StockListMessage'));
}

function populateStockProducts(stock) {
    const stockListElement = document.getElementById('stockList');
    if (stockListElement) {
        stockListElement.innerHTML = '';  // Limpiar la lista existente

        if (Array.isArray(stock) && stock.length > 0) {
            stock.forEach(item => {
                const listItem = document.createElement('li');
                listItem.textContent = `${item.product_id}, ${item.product_name}, ${item.quantity} unidades`;
                stockListElement.appendChild(listItem);
            });
        } else {
            stockListElement.innerHTML = '<li>No hay productos en stock</li>';
        }
    }
}

function checkLowStock(user_id, token) {
    const notificationIcon = document.getElementById('notification-icon');
    const lowStockSection = document.getElementById('lowStockSection');
    const lowStockList = document.getElementById('lowStockList');

    if (!lowStockList || !lowStockSection) {
        console.log("No se encontraron los elementos de la lista o sección de stock bajo.");
        return;
    }

    fetch(apiURL + `/user/${user_id}/stock/low`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) throw new Error(result.error);

        const products = result.data;
        lowStockList.innerHTML = ''; // Limpiar la lista antes de llenarla

        if (Array.isArray(products) && products.length > 0) {
            products.forEach(product => {
                const listItem = document.createElement('li');
                listItem.textContent = `ID: ${product.product_id}, Nombre: ${product.product_name}, Cantidad: ${product.quantity}`;
                lowStockList.appendChild(listItem);
            });
            if (notificationIcon) {
                notificationIcon.classList.add('alert'); // Agregar clase para destacar la campanita
            }
            lowStockSection.style.display = 'block'; // Mostrar la sección
        } else {
            if (notificationIcon) {
                notificationIcon.classList.remove('alert'); // Eliminar la clase si no hay stock bajo
            }
            lowStockSection.style.display = 'none'; // Ocultar la sección si no hay productos con bajo stock
            showMessage('No hay productos con stock bajo.', 'success');
        }
        
    })
    .catch(error => handleFetchError(error));
}

function updateStock() {
    const productSelect = document.getElementById('productId');
    const product_id = productSelect.value; 
    const product_name = productSelect.options[productSelect.selectedIndex].text;    
    const newQuantity = document.getElementById('newQuantity').value;
    const user_id = localStorage.getItem('id');
    const token = localStorage.getItem('token');

    if (!product_id || !newQuantity) {
        showMessage('Por favor, complete todos los campos.', 'error');
        return;
    }

    if (!confirm(`¿Está seguro que desea actualizar el producto "${product_name}" (ID :${product_id}) a una cantidad de ${newQuantity} unidades?`)) {
        return;
    }

    startSpinner();

    fetch(apiURL + `/user/${user_id}/stock/${product_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify({ quantity: Number(newQuantity) })
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) throw new Error(result.error);
        showMessage(result.message, 'success');
    })
    .catch(error => handleFetchError(error))
    .finally(() => stopSpinner());
    loadProducts(user_id, token); // Cargar productos en el dropdown
    loadProductsInStock(user_id, token);
    checkLowStock(user_id, token); // Recargar la lista de productos con bajo stock
    document.getElementById('newQuantity').value = ''; // Reiniciar el valor del input de cantidad
}

function handleFetchError(error) {
    const errorMessage = error.message === "Failed to fetch" 
        ? "No se pudo conectar con el servidor. Verifique su conexión o intente más tarde."
        : error.message || "Error al cargar los servicios";
    showMessage(errorMessage, 'error');
}

function showMessage(text, type) {
    const messageElement = document.getElementById('updateStockMessage');
    if (messageElement) {
        messageElement.textContent = text;
        messageElement.style.color = type === 'error' ? 'red' : 'green';
    } else {
        console.log("No se encontró el elemento para mostrar el mensaje.");
    }
}

function startSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = 'inline-block';
    }
}

function stopSpinner() {
    const spinner = document.getElementById('loading-spinner');
    if (spinner) {
        spinner.style.display = 'none';
    }
}

function userLogout() {
    localStorage.clear();
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
