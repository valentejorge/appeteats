var canvas = $("#canvas"),
    context = canvas.get(0).getContext("2d"),
    $form = $('#product-form'),
    image = $('#image-form');

$('#image').on('change', function() {
    if (this.files && this.files[0]) {
        if (this.files[0].type.match(/^image\//)) {
            var reader = new FileReader();
            reader.onload = function(evt) {
                var img = new Image();
                img.onload = function() {
                    console.log(canvas)
                    console.log(image)
                    canvas[0].style.display = "block";
                    image[0].style.display = "block";
                    context.canvas.height = img.height;
                    context.canvas.width = img.width;
                    context.drawImage(img, 0, 0);
                    if (canvas.data('cropper')) {
                        canvas.cropper('destroy');
                    }
                    var cropper = canvas.cropper({
                        aspectRatio: 1 / 1
                    });
                };
                img.src = evt.target.result;
            };
            reader.readAsDataURL(this.files[0]);
        } else {
            alert("Invalid file type! Please select an image file.");
        }
    } else {
        alert('No file(s) selected.');
    }
});

document.querySelector('#product-form').addEventListener('submit', function(event) {
    event.preventDefault();
    if (canvas) {
        var croppedImageDataURL = canvas.cropper('getCroppedCanvas').toDataURL("image/png");
        var croppedImageBlob = dataURLToBlob(croppedImageDataURL);

        let croppedInput = document.createElement('input');
        croppedInput.type = 'file';
        croppedInput.name = 'crop-img';
        croppedInput.id = 'crop-img';

        const file = new File([croppedImageBlob], 'image.png')

        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);

        croppedInput.files = dataTransfer.files;

        event.target.appendChild(croppedInput);

        // let oldInput = document.querySelector('#img')
        // oldInput.remove()

        event.target.submit();
    };
});

// Function to convert URL data in a blob
function dataURLToBlob(dataURL) {
    var parts = dataURL.split(';base64,');
    var contentType = parts[0].split(':')[1];
    var byteCharacters = atob(parts[1]);
    var byteArrays = [];

    for (var i = 0; i < byteCharacters.length; i++) {
        byteArrays.push(byteCharacters.charCodeAt(i));
    }

    var blob = new Blob([new Uint8Array(byteArrays)], { type: contentType });
    return blob;
}
