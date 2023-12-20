async function takeData() {
    const URL = window.location.pathname +  '/data';

    const response = await fetch(URL);
    const data = await response.json();

    return data;
}

async function init() {
    const data = await takeData();

    buildOpening(data);
}

function buildOpening(data) {
    const container = document.querySelector('#opening-container')
    container.innerHTML = data[0]
    let html = '';
    for (const day of data) {
        html += buildDay(day.day_of_week, day.open, day.opening_time, day.closing_time);
    }
    container.innerHTML = html;
}

function buildDay(dayName, isOpen, openTime, closeTime) {
    if (isOpen === false) {
        openTime = 'closed';
        closeTime = 'closed';
    }
    const html = `
        <div class="d-flex justify-content-between mb-1">
            <h6>${dayName}</h6>
            <div class="d-flex w-50 justify-content-around">
                <h6>${openTime}</h6>
                <h6>-</h6>
                <h6>${closeTime}</h6>
            </div>
        </div>
        `
    return html;
}

init();
