// Función para cerrar la sesión del usuario
function userLogout() {
    localStorage.clear(); // Limpia todos los datos del almacenamiento
    window.location.href = "login.html"; // Redirige a la página de login
}

// Obtiene el token y la información del usuario del almacenamiento local
const token = localStorage.getItem('token');
const user_id = localStorage.getItem('id');
const username = localStorage.getItem('username');
document.getElementById("Welcome_username").innerHTML = username;

// Verifica si el usuario está autenticado al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    if (!token) {
        window.location.href = "login.html"; // Redirige si no hay token
    } else {
        document.getElementById("Welcome_username").textContent = username; // Muestra el nombre de usuario
        // Carga los reportes al cargar la página
        loadPurchasesSummary();
        loadTopSuppliers();
        loadTopProducts();
        loadTotalExpenses();
    }
});

// Función para cargar el resumen de compras
function loadPurchasesSummary() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    if (startDate && endDate) {
        fetch(`${apiURL}/user/${user_id}/reports/summary?start_date=${startDate}&end_date=${endDate}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'x-access-token': token // Solo el token es necesario aquí
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud de resumen de compras');
            }
            return response.json();
        })
        .then(data => {
            const purchasesSummaryList = document.getElementById('purchases-summary');
            purchasesSummaryList.innerHTML = ''; // Limpia la lista anterior
            data.data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `${item.order_date} - Proveedor: ${item.supplier_name} - Total: ${item.total_amount}`;
                purchasesSummaryList.appendChild(li);
            });
        })
        .catch(error => {
            console.error(error);
            alert('Error al cargar el resumen de compras');
        });
    }
}

// Función para cargar los principales proveedores
function loadTopSuppliers() {
    fetch(`${apiURL}/user/${user_id}/reports/top-suppliers`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token // Incluye el token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud de principales proveedores');
        }
        return response.json();
    })
    .then(data => {
        const topSuppliersList = document.getElementById('top-suppliers');
        topSuppliersList.innerHTML = ''; // Limpia la lista anterior
        data.data.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `Proveedor: ${item.supplier_name} - Órdenes: ${item.total_orders}`;
            topSuppliersList.appendChild(li);
        });
    })
    .catch(error => {
        console.error(error);
        alert('Error al cargar los principales proveedores');
    });
}

// Función para cargar los productos más comprados
function loadTopProducts() {
    fetch(`${apiURL}/user/${user_id}/reports/top-products`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token // Incluye el token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud de productos más comprados');
        }
        return response.json();
    })
    .then(data => {
        const topProductsList = document.getElementById('top-products');
        topProductsList.innerHTML = ''; // Limpia la lista anterior
        data.data.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `Producto: ${item.product_name} - Cantidad: ${item.total_quantity}`;
            topProductsList.appendChild(li);
        });
    })
    .catch(error => {
        console.error(error);
        alert('Error al cargar los productos más comprados');
    });
}

// Función para cargar los gastos totales por proveedor
function loadTotalExpenses() {
    fetch(`${apiURL}/user/${user_id}/reports/total-expenses`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token // Incluye el token
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud de gastos totales por proveedor');
        }
        return response.json();
    })
    .then(data => {
        const totalExpensesList = document.getElementById('total-expenses');
        totalExpensesList.innerHTML = ''; // Limpia la lista anterior
        data.data.forEach(item => {
            const li = document.createElement('li');
            li.textContent = `Proveedor: ${item.supplier_name} - Total Gastado: ${item.total_spent}`;
            totalExpensesList.appendChild(li);
        });
    })
    .catch(error => {
        console.error(error);
        alert('Error al cargar los gastos totales por proveedor');
    });
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

// Manejo del formulario de generación de resumen de compras
const reportForm = document.getElementById('report-form');
reportForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Previene el envío del formulario
    loadPurchasesSummary(); // Llama a la función para cargar el resumen
});
