function showPage(buttonName) {
    const pages = document.querySelectorAll(`[name="page"]`)

    pages.forEach((page) => {
        page.classList.remove('active');
    });

    const page = document.querySelector(`#${buttonName}`)
    page.classList.add('active');
}

function changePageState() {
    const path = window.location.hash;

    const page = path.split('?')[0].slice(1)

    const item = path.split('?')[1];


    if (!page && !item || page && !item) {
       hideProductDetails();
       hideCategoryDetails();
    }

    if (item) {
        const itemArray = item.split('=')

        const subpage = {
            item: itemArray[0],
            id: itemArray[1]
        }

        if (subpage.item === 'category_id') {
            try {
                showCategory(parseInt(subpage.id));
                hideProductDetails();
            }
            catch(_err) {
                window.location.hash = 'menu'
            }
        }
        if (subpage.item === 'product_id') {
            try {
                showProductDetails(parseInt(subpage.id))
            }
            catch(_err) {
                window.location.hash = 'menu'
            }
        }
    }

    console.log(`page is ${page}`)
    if (page) {
        showPage(page)
    }

}

window.addEventListener("hashchange", changePageState);
document.addEventListener("DOMContentLoaded", changePageState);
