// Initialize active tab from URL hash
//   document.addEventListener('DOMContentLoaded', function() {
//     const urlParams = new URLSearchParams(window.location.search);
//     const tab = urlParams.get('tab');
//     if (tab) {
//       const tabButton = document.querySelector(`[data-bs-target="#tab-${tab}"]`);
//       if (tabButton) {
//         tabButton.show();
//       }
//     }
//   });

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
    document.body.addEventListener('click', function(event) {
        const buttonEdit = event.target.closest('.update-product-btn');
    
        if (!buttonEdit) return;

        const productId = buttonEdit.dataset.productId;
        const productName = buttonEdit.dataset.productName;
        const productPrice = buttonEdit.dataset.productPrice;
        const productStock = buttonEdit.dataset.productStock;
        const productAvailability = buttonEdit.dataset.productAvailability; // "True" or "False"
        const productImages = buttonEdit.dataset.productImages;
        const productDescription = buttonEdit.dataset.productDescription;
        const editUrl = buttonEdit.dataset.editUrl;
        const discount_percentage = buttonEdit.dataset.discountPercentage;

        // Update the edit modal with product details
        document.getElementById('editProductId').value = productId;
        document.getElementById('editProductName').value = productName;
        document.getElementById('editProductDescription').value = productDescription;
        document.getElementById('editProductPrice').value = productPrice;
        document.getElementById('editProductCategory').value = buttonEdit.dataset.productCategory;
        document.getElementById('editProductStock').value = productStock;
        document.getElementById('editDiscount').value = discount_percentage;
        
        // FIX: Directly assign the string "True" or "False"
        document.getElementById('editProductAvailability').value = productAvailability;

        // Image Preview Logic
        const imgPreview = document.getElementById('editProductImagePreview');
        const fileInput = document.getElementById('editProductImages');
        fileInput.value = ''; // Clear file input
        
        if (productImages && productImages !== "undefined" && productImages !== "") {
            if (!productImages.startsWith('/media/')) {
                imgPreview.src = '/media/' + productImages;
            } else {
                imgPreview.src = productImages;
            }
            imgPreview.style.display = 'block';
        } else {
            imgPreview.style.display = 'none';
        }
        
        // Save URL to the FORM
        document.getElementById('editProductForm').dataset.editUrl = editUrl;

        // FIX: USE 'editProductModal' (THE DIV), NOT 'editProductForm'
        const modalElement = document.getElementById('editProductModal');
        let editModal = bootstrap.Modal.getInstance(modalElement);
        if (!editModal) {
            editModal = new bootstrap.Modal(modalElement);
        }
        editModal.show();
    });

    const editProductForm = document.getElementById('editProductForm');
    if(editProductForm) {
        editProductForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const form = event.target;
            const formData = new FormData(form); 
            const editUrl = form.dataset.editUrl;
            const productId = document.getElementById('editProductId').value;

            fetch(editUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    // NO Content-Type here!
                },
                body: formData 
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    
                    // Update the UI
                    const rowToUpdate = document.getElementById(`product-row-${productId}`);
                    if (rowToUpdate) {
                        const nameCell = rowToUpdate.querySelector('.product-name');
                        const priceCell = rowToUpdate.querySelector('.product-price');
                        const stockCell = rowToUpdate.querySelector('.product-stock');
                        const availabilityCell = rowToUpdate.querySelector('.product-availability');
                        const discountCell = rowToUpdate.querySelector('.discount-percentage');
                        
                        if(nameCell) nameCell.textContent = formData.get('name');
                        if(priceCell) priceCell.textContent = `$${formData.get('price')}`;
                        if(stockCell) stockCell.textContent = `${formData.get('stock')} kg`;
                        if(discountCell) discountCell.textContent = `${formData.get('discount_price')}%`;
                        
                        if(availabilityCell) {
                            const isAvail = formData.get('is_available') === 'True';
                            availabilityCell.innerHTML = isAvail 
                                ? '<span class="badge bg-success">Available</span>' 
                                : '<span class="badge bg-danger">Unavailable</span>';
                        }

                        if (data.new_image_url) {
                            const img = rowToUpdate.querySelector('img');
                            if (img) img.src = data.new_image_url;
                        }
                        
                        // CRITICAL: Update the hidden data attributes on the button so if you click edit again, it has the new data!
                        const btn = rowToUpdate.querySelector('.update-product-btn');
                        if(btn) {
                            btn.dataset.productName = formData.get('name');
                            btn.dataset.productPrice = formData.get('price');
                            btn.dataset.productStock = formData.get('stock');
                            btn.dataset.productDescription = formData.get('description');
                            btn.dataset.productAvailability = formData.get('is_available');
                            btn.dataset.productCategory = formData.get('category');
                            btn.dataset.discountPercentage = formData.get('discount_percentage');
                            if (data.new_image_url) btn.dataset.productImages = data.new_image_url;
                        }
                    }
                    
                    // FIX: USE 'editProductModal' (THE DIV), NOT 'editProductForm'
                    const modalElement = document.getElementById('editProductModal');
                    const editModal = bootstrap.Modal.getInstance(modalElement);
                    if (editModal) {
                        editModal.hide();
                    }
                    
                    alert('Product updated successfully.');
                    
                } else {
                    alert('Error updating product. Please check the form.');
                }
            })
            .catch(error => {
                console.error('Fetch Error:', error);
                alert("A critical error occurred.");
            });
        });
    }
    
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
const editCategoryForm = document.getElementById('editCategoryForm');
if (editCategoryForm) {
    editCategoryForm.addEventListener('submit', function(event) {
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
}