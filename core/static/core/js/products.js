function filterProducts(category, element) {
    // Remove 'active' class from all buttons
    const buttons = document.querySelectorAll('#category-tab .btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    // Add 'active' class to the clicked button
    element.classList.add('active');
    // Get all product items
    const products = document.querySelectorAll('.product-items');
    products.forEach(product => {
        const rawCategory = product.getAttribute('data-category');
        const productCategory = rawCategory ? rawCategory.toLowerCase() : '';
        if (category === 'all' || productCategory.includes(category)) {
            product.style.display = 'block';
        } else {
            product.style.display = 'none';
        }
    });
}