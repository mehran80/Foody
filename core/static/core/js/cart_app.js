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
                const grandTotal = document.getElementById('cart-grandtotal');
                if (grandTotal) {
                  grandTotal.innerText = `$${data.cart_total_price}`;
                }
            })
            .catch(error => {
                console.error('Error updating cart:', error);
            });
        });
    });
});


document.addEventListener('DOMContentLoaded', function(){
  var stripe = Stripe('pk_test_51T7hscKqozwVdadCOTLel7DGqbrIyuEbFq7qlspyT0RNUQDSJKBjA30xT04boi8i3tWX5FLUxzNw97lgbXdao42B00X8EevnSV');
  var elements = stripe.elements();

  var style = { base: { fontSize: '16px', color: '#32325d' } };
  var card = elements.create('card', {style: style});
  card.mount('#card-element');

  var codRadio = document.getElementById('payCOD')
  var cardRadio = document.getElementById('payCard')
  var stripeBox = document.getElementById('stripe-card-box')

  function togglePaymentBox(){
    if (cardRadio.checked){
      stripeBox.style.display = 'block'
    }
    else{
      stripeBox.style.display = 'none'
    }
  }
  if(cardRadio && codRadio){
    cardRadio.addEventListener('change', togglePaymentBox);
    codRadio.addEventListener('change', togglePaymentBox);

    togglePaymentBox();
  }
  else{
    console.error("CRITICAL: Radio buttons not found by JS!");
  }


  var form = document.querySelector('#checkout-form');
  if(form){
    form.addEventListener('submit', function(event){
      if (codRadio.checked){
        return;
      }

      event.preventDefault();
      var submitBtn = document.querySelector('button[type="submit"]');
      submitBtn.disabled = true;
      submitBtn.innerText = "Processing..."

      stripe.createToken(card).then(function(result){
        if(result.error){
          var errorElement = document.getElementById('card-errors');
          errorElement.textContent = result.error.message;
          document.querySelector('button[type="submit"]').disabled = false;
        }
        else{
          document.getElementById('stripeToken').value = result.token.id;
          form.submit();
        }
      });
    });
  }
  else{
    console.error("CRITICAL: Form with id='checkout-form' not found!");
  }
});

document.addEventListener('DOMContentLoaded', function(){
  
  const savedAddressRadios = document.querySelectorAll('.saved-address-radio');
  const newAddressRadio = document.getElementById('use-new-address-radio');
  const newAddressForm = document.getElementById('new-address-form');

  function toggleNewForm(){
    if (!newAddressForm) return; 

    if (!newAddressRadio) {
        newAddressForm.style.display = 'block';
        return; 
    }


    if(newAddressRadio.checked){
      newAddressForm.style.display = 'block';
    } else {
      newAddressForm.style.display = 'none';
    }
  }


  if (newAddressRadio) {
      newAddressRadio.addEventListener('change', toggleNewForm);

      if (savedAddressRadios && savedAddressRadios.length > 0) {
          savedAddressRadios.forEach(radio => {
              radio.addEventListener('change', toggleNewForm);
          });
      }
  }

  toggleNewForm();

});
