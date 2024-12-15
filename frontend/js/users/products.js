document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = "login.html";
    } else {
        loadCategories(); // Llenar el select de categorías
        loadProducts();
    }

    // Event listeners for form submissions
    document.getElementById('createProductForm').addEventListener('submit', handleFormSubmission(registerProduct));
    document.getElementById('updateProductForm').addEventListener('submit', handleFormSubmission(updateProduct));
    document.getElementById('deleteProductForm').addEventListener('submit', handleFormSubmission(deleteProduct));
    document.getElementById('listProductsByCategoryForm').addEventListener('submit', handleFormSubmission(loadProductsByCategory));
});

// Variables globales
const token = localStorage.getItem('token');
const user_id = localStorage.getItem('id');
const username = localStorage.getItem('username');
let categories = []; // Almacenará las categorías
document.getElementById("Welcome_username").innerHTML = username;


// Funciones principales
function handleFormSubmission(callback) {
    return function (event) {
        event.preventDefault();
        callback();
    };
}

function loadCategories() {
    fetch(apiURL + `/user/${user_id}/categories`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
    })
    .then(response => handleResponse(response))
    .then(result => {
        categories = result.data; // Almacena las categorías en la variable global
        populateCategorySelect(result.data, 'NewProductCategorySelect');
        populateCategorySelect(result.data, 'UpdateProductCategorySelect');
        populateCategorySelect(result.data, 'categorySelectFilter');
    })
    .catch(error => showMessage(error.message, 'error', 'registerProductMessage'));
}

function populateCategorySelect(categories, selectId) {
    const selectElement = document.getElementById(selectId);
    selectElement.innerHTML = '<option value="">Seleccione una categoría</option>'; // Opción inicial

    categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.id; // Asegúrate de usar el ID correcto
        option.textContent = category.name;
        selectElement.appendChild(option);
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
    .catch(error => showMessage(error.message, 'error', 'ProductListMessage'));
}

function registerProduct() {
    const data = collectProductData('create');
    if (!data) return; // Si hay datos inválidos, sale

    fetch(apiURL + `/user/${user_id}/products`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify(data)  // Asegúrate de que esto es un JSON válido
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al registrar el producto');
        }
        return response.json();
    })
    .then(responseData => {
        showMessage('Producto registrado exitosamente.', 'success', 'registerProductMessage');
        document.getElementById('createProductForm').reset();
        loadProducts(); // Llama a la función para actualizar la lista de productos
    })
    .catch(error => {
        showMessage(error.message, 'error', 'registerProductMessage');
    });
}


function updateProduct() {
    const productId = document.getElementById('productSelectUpdate').value;
    const data = collectProductData('update', productId);
    if (!data) return;

    fetch(apiURL + `/user/${user_id}/products/${productId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'x-access-token': token
        },
        body: JSON.stringify(data)
    })
    .then(response => handleResponse(response))
    .then(() => {
        showMessage('Producto actualizado exitosamente.', 'success', 'updateProductMessage');
        document.getElementById('updateProductForm').reset();
        loadProducts();
    })
    .catch(error => showMessage(error.message, 'error', 'updateProductMessage'));
}

function deleteProduct() {
    const productId = document.getElementById('productSelectDelete').value;
    if (!productId) {
        showMessage('Seleccione un producto para eliminar.', 'error', 'deleteProductMessage');
        return;
    }

    fetch(apiURL + `/user/${user_id}/products/${productId}`, {
        method: 'DELETE',
        headers: {
            'x-access-token': token
        }
    })
    .then(response => handleResponse(response))
    .then(() => {
        showMessage('Producto eliminado exitosamente.', 'success', 'deleteProductMessage');
        document.getElementById('deleteProductForm').reset();
        loadProducts();
    })
    .catch(error => showMessage(error.message, 'error', 'deleteProductMessage'));
}

function loadProductsByCategory() {
    const categoryId = document.getElementById('categorySelectFilter').value;
    if (!categoryId) {
        showMessage('Seleccione una categoría.', 'error', 'listProductsByCategoryMessage');
        return;
    }

    fetch(apiURL + `/user/${user_id}/products/${categoryId}`, {
        method: 'GET',
        headers: {
            'x-access-token': token
        }
    })
    .then(response => handleResponse(response))
    .then(result => {
        // Verifica qué contiene `result` aquí
        console.log(result); // Para depuración
        // Asegúrate de que estás pasando la estructura correcta
        populateCategoryProducts(result); // Cambiado de result.data a result
    })
    .catch(error => showMessage(error.message, 'error', 'listProductsByCategoryMessage'));
}


// Helper functions
function handleResponse(response) {
    if (!response.ok) {
        return response.json().then(result => {
            throw new Error(result.error || 'Error inesperado.');
        });
    }
    return response.json();
}

function collectProductData(action, productId) {
    const name = document.getElementById(`${action === 'create' ? 'create' : 'updated'}ProductName`).value.trim();
    const price = parseFloat(document.getElementById(`${action === 'create' ? 'create' : 'updated'}ProductPrice`).value);
    const category_id = document.getElementById(`${action === 'create' ? 'New' : 'Update'}ProductCategorySelect`).value;

    // Asegúrate de que category_id sea null si no se selecciona
    const categoryIdValue = category_id ? parseInt(category_id) : null;

    // Validación de campos requeridos
    if (!name || isNaN(price) || (action === 'update' && !productId)) {
        showMessage('Por favor, complete todos los campos.', 'error', `${action}ProductMessage`);
        return null;
    }

    return { name, price, category_id: categoryIdValue };
}


function populateProductLists(products) {
    const productList = document.getElementById('productList');
    const productSelect = document.getElementById('productSelectUpdate');
    const productSelectDelete = document.getElementById('productSelectDelete');

    productList.innerHTML = '';
    productSelect.innerHTML = '';
    productSelectDelete.innerHTML = '';

    products.forEach(product => {
        const li = document.createElement('li');
        
        // Encuentra el nombre de la categoría usando la ID del producto
        const category = categories.find(cat => cat.id === product.category_id);
        const categoryName = category ? category.name : 'Sin categoría'; // Usa un nombre predeterminado si no se encuentra
      
        // Incluye el ID de la categoría junto con el nombre y el precio
        li.textContent = `${product.name} - ${product.price} - ${categoryName} (ID: ${product.category_id})`;
        productList.appendChild(li);

        const option = document.createElement('option');
        option.value = product.id;
        option.textContent = product.name;
        productSelect.appendChild(option);
        productSelectDelete.appendChild(option.cloneNode(true));
    });
}

function populateCategoryProducts(products) {
    const productList = document.getElementById('productListCategoryFilter');
    productList.innerHTML = '';

    // Verifica que `products` sea un array
    if (!Array.isArray(products) || products.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No products found.';
        productList.appendChild(li);
        return;
    }

    // Recorrer cada producto
    products.forEach(product => {
        console.log(product); // Para depuración

        const li = document.createElement('li');
        const price = parseFloat(product.price).toLocaleString(undefined, { style: 'currency', currency: 'USD' });
        
        li.textContent = `${product.name} - ${price}`;
        li.classList.add('product-item'); // Clase CSS para estilización
        productList.appendChild(li);
    });
}

function showMessage(text, type, elementId) {
    const messageElement = document.getElementById(elementId);
    messageElement.textContent = text;
    messageElement.style.color = type === 'success' ? 'green' : 'red';
}

// Función para cerrar la sesión del usuario
function userLogout() {
    localStorage.clear(); // Limpia todos los datos del almacenamiento
    window.location.href = "login.html";
}