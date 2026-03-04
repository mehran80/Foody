function addToCart(element) {
  const url = element.getAttribute('data-url');
  fetch(url, {
    method: 'POST',
    headers: {
      'x-requested-with': 'XMLHttpRequest',
      'X-CSRFToken': CSRF_TOKEN,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({}) // You can include additional data if needed
  })
  .then(response =>{
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    const badge = document.getElementById('cart_badge');
    if (badge && data.cart_quantity !== undefined) {
      badge.innerText = data.cart_quantity;
    }
    badge.classList.remove('d-none');
  })
  .catch(error => {
    console.error('Error adding to cart:', error);
  });
}

document.addEventListener('DOMContentLoaded', function() {
  const updateButtons = document.querySelectorAll('.update-cart-btn');
    updateButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-id');
            const action = this.getAttribute('data-action');
            const url = this.getAttribute('data-url');

            fetch(url, {
                method: 'POST',
                headers: {
                    'x-requested-with': 'XMLHttpRequest',
                    'X-CSRFToken': CSRF_TOKEN,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ product_id: productId, 'action': action })
            })
            .then(response => response.json())
            .then(data => {
                // Update quantity display
                const qtyInput = document.getElementById(`qty-${productId}`);
                if (qtyInput) {
                    qtyInput.value = data.cart_quantity;
                }
                // Update item total price display
                const itemTotal = document.getElementById(`item-total-${productId}`);
                if (itemTotal) {
                    itemTotal.innerText = `$${data.total_price}`;
                }
                // Update cart total price display
                const cartSubtotal = document.getElementById('cart-subtotal');
                if (cartSubtotal) {
                    cartSubtotal.innerText = `$${data.cart_total_price}`;
                }
            })
            .catch(error => {
                console.error('Error updating cart:', error);
            });
        });
    });
});