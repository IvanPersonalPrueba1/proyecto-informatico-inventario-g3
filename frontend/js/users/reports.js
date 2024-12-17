// Función para cerrar la sesión del usuario
function userLogout() {
    localStorage.clear(); // Limpia todos los datos del almacenamiento
    window.location.href = "login.html";
}

// Verifica si el usuario está autenticado
document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = "login.html";
    } else {
        const username = localStorage.getItem('username');
        document.getElementById("Welcome_username").textContent = username; // Asegúrate de que el ID coincida
    }

    // Llamar a las funciones para cargar los reportes al cargar la página
    loadPurchasesSummary();
    loadTopSuppliers();
    loadTopProducts();
    loadTotalExpenses();
});

// Función para cargar el resumen de compras
function loadPurchasesSummary() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const userId = localStorage.getItem('userId'); // Asegúrate de que el ID de usuario esté en el almacenamiento local

    if (startDate && endDate) {
        fetch(apiURL + `/user/${userId}/reports/summary?start_date=${startDate}&end_date=${endDate}`)
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
    const userId = localStorage.getItem('userId');

    fetch(apiURL + `/user/${userId}/reports/top-suppliers`)
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
    const userId = localStorage.getItem('userId');

    fetch(apiURL + `/user/${userId}/reports/top-products`)
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
    const userId = localStorage.getItem('userId');

    fetch(apiURL + `/user/${userId}/reports/total-expenses`)
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