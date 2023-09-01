const everyday = document.querySelector("#everyday")
const weekdays = document.querySelector("#weekdays");
const everydayInput = document.querySelector("#everyday-input")

function toggleWeekdayVisibility() {
    if (everyday.checked) {
        weekdays.classList.add('hide-important')
        everydayInput.classList.remove('hide-important');

    } else {
        weekdays.classList.remove('hide-important')
        everydayInput.classList.add('hide-important');
    }
}



toggleWeekdayVisibility();

everyday.addEventListener('change', toggleWeekdayVisibility);
