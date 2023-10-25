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
        buildDashboard(data);
    }
}

function buildDashboard(data) {
    for (const item in data) {
        let html = '';

        const page = document.querySelector(`#${item}`)

        for (const order of data[item]) {
            html += cardConstructor(order);
        }

        page.innerHTML = html;
    }

}

function cardConstructor(order) {
    let html = '';
    html += buildCardTop(order.id, order.customer_name, order.customer_address, order.customer_reference)

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
    html += buildCardFooter(order.id, order.status);

    /*
    const a = document.querySelector('#processing');
    console.log(a)
    a.innerHTML = html;
    */
    return html;
}

function buildCardTop(id, name, address, reference) {
    let html = '';
    html += `
        <div class="order-card mb-3">
            <div class="d-flex justify-content-center align-items-center p-2" style="background-color: #ea0000; color: #fff; border-radius: 10px 10px 0 0;">
                <span class="material-icons">tag</span>
                <h6 class="mb-0">
                    000${id}
                </h6>
            </div>
            <div class="list-group-item" style="background-color: transparent;">
                <div class="d-flex justify-content-center align-items-center mb-1">
                    <span class="material-icons">person</span>
                    <h6 class="mb-0">
                        ${name}
                    </h6>
                </div>
            <div class="d-flex justify-content-center align-items-start">
            <span class="material-icons">location_on</span>
                <h6 class="mb-0">
                    ${address}
                </h6>
            </div>
            <div class="d-flex justify-content-center align-items-start mb-1">
                <h6 class="mb-0">
                    ${reference} 
                </h6>
            </div>
        </div>
    `
    return html;

}

function buildProductsList(items) {
    let html = ''
    for (const item of items) {
        html += `
            <ul class="list-group">
                <li class="list-group-item cart-list">
                    <div class="d-flex align-items-center justify-content-start w-50">
                        <img src="/static/cache/${item.image_path}" class="cart-img" style="max-width: 30px;">
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

function buildCardFooter(id, status) {
    let html = '';
    switch(status) {
        case 'processing':
            html = `
                <form action="/admin/dashboard" method="post">
                    <input name="id" type="hidden" value="${id}">
                    <input name="status" type="hidden" value="${status}">
                    <input name="operation" type="hidden" value="next">
                    <button type="submit" class="d-flex align-items-center justify-content-end std-button p-1 bottom-button">
                        <span class="">Next Step</span>
                        <span class="material-icons nav_icons">chevron_right</span>
                    </button>
                </form>
            </div>
            `
            return html;
        case 'cooking':
            html = `
                <div class="d-flex w-100">
                    <form class="w-50" action="/admin/dashboard" method="post">
                        <input name="id" type="hidden" value="${id}">
                        <input name="status" type="hidden" value="${status}">
                        <input name="operation" type="hidden" value="previous">
                        <button type="submit" class="d-flex align-items-center justify-content-start std-button p-1 bottom-button left">
                            <span class="material-icons nav_icons">chevron_left</span>
                            <span class="">Previous Step</span>
                        </button>
                    </form>
                    <form class="w-50" action="/admin/dashboard" method="post">
                        <input name="id" type="hidden" value="${id}">
                        <input name="status" type="hidden" value="${status}">
                        <input name="operation" type="hidden" value="next">
                        <button type="submit" class="d-flex align-items-center justify-content-end std-button p-1 bottom-button right">
                            <span class="">Next Step</span>
                            <span class="material-icons nav_icons">chevron_right</span>
                        </button>
                    </form>
                </div>
            </div>
            `
            return html;
        case 'done':
            html = `
                <form action="/admin/dashboard" method="post">
                    <input name="id" type="hidden" value="${id}">
                    <input name="status" type="hidden" value="${status}">
                    <input name="operation" type="hidden" value="previous">
                    <button type="submit" class="d-flex align-items-center justify-content-start std-button p-1 bottom-button">
                        <span class="material-icons nav_icons">chevron_left</span>
                        <span class="">Previous Step</span>
                    </button>
                </form>
            </div>

            `
            return html;
    }
}

init();
