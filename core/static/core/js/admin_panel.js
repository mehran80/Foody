// Initialize active tab from URL hash
  document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const tab = urlParams.get('tab');
    if (tab) {
      const tabButton = document.querySelector(`[data-bs-target="#tab-${tab}"]`);
      if (tabButton) {
        tabButton.show();
      }
    }
  });

// Function to get CSRF token from cookies
// This function retrieves the value of a specified cookie, which is necessary for including the CSRF token in AJAX requests to protect against cross-site request forgery attacks. It checks if the document has cookies, splits them into an array, and iterates through them to find the one that matches the specified name. If found, it decodes and returns the cookie value; otherwise, it returns null.
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Handle product editing
// Listen for clicks on edit buttons, populate the modal with the product's current data, and show the modal

document.addEventListener('DOMContentLoaded', function() {
    const buttonEdit = document.querySelector('.update-product-btn');
    if (!buttonEdit)
        return;
        const productId = buttonEdit.dataset.productId;
        const productName = buttonEdit.dataset.productName;
        const productPrice = buttonEdit.dataset.productPrice;
        const productStock = buttonEdit.dataset.productStock;
        const productAvailability = buttonEdit.dataset.productAvailability;
        const productImages = buttonEdit.dataset.productImages;
        const productDescription = buttonEdit.dataset.productDescription;

        // Update the edit modal with product details
        document.getElementById('editProductId').value = productId;
        document.getElementById('editProductName').value = productName;
        document.getElementById('editProductDescription').value = productDescription;
        document.getElementById('editProductPrice').value = productPrice;
        document.getElementById('editProductImages').value = productImages;
        document.getElementById('editProductCategory').value = buttonEdit.dataset.productCategory;
        document.getElementById('editProductStock').value = productStock;
        document.getElementById('editProductAvailability').checked = productAvailability === 'True';
        
        


        // Show the edit modal
        const editModal = new bootstrap.Modal(document.getElementById('editProductModal'));
        editModal.show();
});

document.getElementById('editProductForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = event.target;
    const productId = document.getElementById('editProductId').value;
    const productName = document.getElementById('editProductName').value;
    const productDescription = document.getElementById('editProductDescription').value;
    const productPrice = document.getElementById('editProductPrice').value;
    const productImages = document.getElementById('editProductImages').value;
    const productCategory = document.getElementById('editProductCategory').value;
    const productStock = document.getElementById('editProductStock').value;
    const productAvailability = document.getElementById('editProductAvailability').checked;
    const editUrl = form.dataset.editUrl;

    fetch(editUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: productName,
            description: productDescription,
            images: productImages,
            price: productPrice,
            category: productCategory,
            stock: productStock,
            is_available: productAvailability })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const rowToUpdate = document.getElementById(`product-row-${productId}`);
            if (rowToUpdate) {
                const cells = rowToUpdate.querySelectorAll('td');
                cells[1].textContent = productName;
                cells[2].textContent = `$${productPrice}`;
                cells[3].textContent = `${productStock} kg`;
                cells[4].innerHTML = productAvailability ? '<span class="badge bg-success">Available</span>' : '<span class="badge bg-danger">Unavailable</span>';
            }
            alert('Product updated successfully.');
        } else {
            alert('Error updating product: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("A critical error occurred. Check the console (F12) for details.");
    });
});

// Handle product deletion
// Listen for clicks on delete buttons, show confirmation dialog, send AJAX request to delete product, and update UI based on response
// When a delete button is clicked, show a confirmation dialog, send an AJAX request to delete the product, and update the UI based on the response
// Listen for clicks on delete buttons, show confirmation dialog, send AJAX request to delete product, and update UI based on response
document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const activeTab = urlParams.get('tab');
    if (activeTab) {
        const tabButton = document.querySelector(`[data-bs-target="#${activeTab}"]`);
        if (tabButton) {
            const tab = new bootstrap.Tab(tabButton);
            tab.show();
        }
    }

        document.body.addEventListener('click', function(event) {
        const deleteButton = event.target.closest('.delete-product-btn');
        if (!deleteButton) {
            return;
        }
        const productId = deleteButton.dataset.productId;
        const deleteUrl = deleteButton.dataset.deleteUrl;
        if (confirm('Are you sure you want to delete this product?')) {
            fetch(deleteUrl, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Server responded with an error!');
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    const rowToRemove = document.getElementById(`product-row-${productId}`);
                    if (rowToRemove) {
                        rowToRemove.remove();
                    }
                    alert('Product deleted successfully.');
                } else {
                    alert('Error from server: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("A critical error occurred. Check the console (F12) for details.");
            });
        }
    });
});

// Handle tab navigation and category deletion
// Listen for clicks on tab buttons to update URL hash and show the corresponding tab
// Listen for clicks on delete buttons, show confirmation dialog, send AJAX request to delete category, and update UI based on response
// When a tab button is clicked, update the URL hash and show the corresponding tab
// When a delete button is clicked, show a confirmation dialog, send an AJAX request to delete the category, and update the UI based on the response
// Listen for clicks on tab buttons to update URL hash and show the corresponding tab

document.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const activeTab = urlParams.get('tab');

    if (activeTab) {
        const tabButton = document.querySelector(`[data-bs-target="#${activeTab}"]`);
        
        if (tabButton) {
            const tab = new bootstrap.Tab(tabButton);
            tab.show();
        }
    }

    document.body.addEventListener('click', function(event) {
        
        const deleteButton = event.target.closest('.delete-category-btn');
        
        if (!deleteButton) {
            return;
        }
        
        const categoryId = deleteButton.dataset.categoryId;
        const deleteUrl = deleteButton.dataset.deleteUrl;

        if (confirm('Are you sure you want to delete this category?')) {
            fetch(deleteUrl, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) { 
                    throw new Error('Server responded with an error! Status: ' + response.status);
                }
                return response.json();
            })
            .then(data => {
                if (data.status === 'success') {
                    const rowToRemove = document.getElementById(`category-row-${categoryId}`);
                    if (rowToRemove) {
                        rowToRemove.remove();
                    }
                    alert('Category deleted successfully.');
                } else {
                    alert('Error from server: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert("A critical error occurred. Check the console (F12) for details.");
            });
        }
    });
});

// Handle category editing
// Listen for clicks on edit buttons
// When an edit button is clicked, populate the modal with the category's current data and show the modal
// Listen for form submission in the modal, send an AJAX request to update the category, and update the UI accordingly

document.body.addEventListener('click', function(event) {
    const updateButton = event.target.closest('.update-category-btn');
    if (!updateButton) {
        return;
    }
    const categoryId = updateButton.dataset.categoryId;
    const categoryName = updateButton.dataset.categoryName;
    const editUrl = updateButton.dataset.editUrl;

    document.getElementById('editCategoryId').value = categoryId;
    document.getElementById('editCategoryName').value = categoryName;

    document.getElementById('editCategoryForm').dataset.editUrl = editUrl;
    
    const editModal = new bootstrap.Modal(document.getElementById('editCategoryModal'));
    editModal.show();
});

// Handle form submission for editing category
// When the form is submitted, prevent default behavior, send an AJAX request to update the category, and update the UI based on the response
// Listen for form submission in the edit category modal
// When the form is submitted, prevent default behavior, send an AJAX request to update the category, and update the UI based on the response

document.getElementById('editCategoryForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const form = event.target;
    const categoryId = document.getElementById('editCategoryId').value;
    const newName = document.getElementById('editCategoryName').value;
    const editUrl = form.dataset.editUrl;
    fetch(editUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: newName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const rowToUpdate = document.getElementById(`category-row-${categoryId}`);
            if (rowToUpdate) {
                const nameCell = rowToUpdate.querySelector('.category-name');
                console.log("Found Row:", rowToUpdate); // Debugging
                if (nameCell) {
                    nameCell.textContent = newName;
                }
                const editBtn = rowToUpdate.querySelector('.update-category-btn');
                if (editBtn) {
                    editBtn.dataset.categoryName = newName;
                }
            }

            if (document.activeElement) {
                document.activeElement.blur();
            }
            const editModal = bootstrap.Modal.getInstance(document.getElementById('editCategoryModal'));
            editModal.hide();
        } else {
            alert('Error updating category: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("A critical error occurred. Check the console (F12) for details.");
    });
});