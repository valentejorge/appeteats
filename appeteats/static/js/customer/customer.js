async function takeData() {
    const URL = window.location.pathname + '/data';
    const response = await fetch(URL);
    const data = await response.json();

    return data;
}

async function init() {
    const data = await takeData();

    if (data) {
        console.log(data);
        buildCustomerView(data);
    }
}

function buildCustomerView(data) {
    for (const _item in data) {
        let html = '';

        const div = document.querySelector('#orders');
        for (const order of data) {
            html += cardConstructor(order);
        }

        div.innerHTML = html;
    }
}

function cardConstructor(order) {
    let html = '';
    html += buildCardTop(order.status)

    html += buildProductsList(order.items)

    html += `
        <li class="list-group-item order-footer">
            <h6 class="p-title mb-0 total-text">Total: </h6>
            <div class="price-section">
                <h6 class="mb-0">$</h6>
                <h6 class="mb-0">${order.total_price.toFixed(2)}</h6>
            </div>
        </li>
    `
    html += '</div>'

    return html;
}

function buildCardTop(status) {
    let html = '';
    html += `
        <div class="order-card shadow">
            <div class="d-flex justify-content-center align-items-center order-header text-center mt-4">
                <h6 class="mb-0">
                    ${status.charAt(0).toUpperCase() + status.slice(1)}
                </h6>
    `
    html += buildStatus(status)

    html += `</div>`
    return html;
}

function buildStatus(status) {
    switch(status) {
        case 'processing':
            return `<div class="spinner spinner-border spinner-border-sm" role="status"></div>`
        case 'cooking':
            return `<div class="spinner spinner-grow spinner-grow-sm" role="status"></div>`
        case 'done':
            return `<span class="spinner material-icons nav-icons text-success">check</span>`
    }
}


function buildProductsList(items) {
    let html = ''
    for (const item of items) {
        html += `
            <ul class="list-group">
                <li class="list-group-item cart-list">
                    <div class="d-flex align-items-center justify-content-start w-50">
                        <img src="/static/cache/${item.image_path}" class="cart-img">
                        <h6 class="p-title mb-0">${item.product_name}</h6>
                    </div>
                    <div>
                        x
                    </div>
                    <input type="number" class="qty-input text-center" value="${item.quantity}" disabled>
                    <div>
                        =
                    </div>
                    <div class="price-section">
                        <h6 class="mb-0">$</h6>
                        <h6 class="mb-0">${item.sub_total}</h6>
                    </div>
                </li>
            </ul>
        `
    }
    return html;
}

init();
