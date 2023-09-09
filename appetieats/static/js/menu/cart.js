function incrementQty(incrementButton) {
    console.log(incrementButton)
    const qtyGroup = incrementButton.closest(".qty-group");
    const quantityInput = qtyGroup.querySelector(".qty-input");

    const currentValue = parseInt(quantityInput.value);

    if (!isNaN(currentValue) && currentValue >= 0) {
        quantityInput.value = currentValue + 1;
    }
    else {
        quantityInput.value = 1;
    }
}

function decrementQty(decrementButton) {
    const qtyGroup = decrementButton.closest(".qty-group");
    const quantityInput = qtyGroup.querySelector(".qty-input");

    const currentValue = parseInt(quantityInput.value);

    if (!isNaN(currentValue) && currentValue > 1) {
        quantityInput.value = currentValue - 1;
    }
    else {
        quantityInput.value = 1;
    }
}
