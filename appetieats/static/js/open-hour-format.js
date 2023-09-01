function formatTimeInput(input) {
    let cleanedInput = input.replace(/[^\d]/g, '');

    if (cleanedInput.length >= 3) {
        let hours = cleanedInput.slice(0, 2);
        let minutes = cleanedInput.slice(2, 4);
        if (hours > 23) {
            hours = 00;
        }
        if (minutes > 59) {
            minutes = 00;
        }
        return `${hours}:${minutes}`;
    }

    return cleanedInput;
}

function handleTimeInput(inputElement) {
    const currentValue = inputElement.value;

    const formattedValue = formatTimeInput(currentValue);

    inputElement.value = formattedValue;
}

const timeInputs = document.querySelectorAll('.time');
console.log(timeInputs)
timeInputs.forEach((input) => {
    input.addEventListener('input', () => handleTimeInput(input));
});
