let priceInput = document.getElementById('price');

// Define a standard value for price field
priceInput.value = '$ 0.00';

// Format the field price when reload page
let price = priceInput.value;
price = price.replace(/\D/g, '');
price = `$ ` + (price / 100).toFixed(2)
priceInput.value = price;

priceInput.addEventListener('input', function(event) {
    let price = event.target.value;

    price = price.replace(/\D/g, '');
    price = `$ ` + (price / 100).toFixed(2)

    event.target.value = price;
});

function valuePriceField(price) {
    let priceInput = document.getElementById('price');
    price = (price).toFixed(2);
    priceInput.value = `$ ${price}`;
}
