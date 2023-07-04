var uploadedImage;
var upscaledImage;

function updateUploadStatus() {
    var fileInput = document.getElementById('file');
    var uploadStatus = document.querySelector('.upload-status');

    if (fileInput.files.length > 0) {
        var fileSize = fileInput.files[0].size / 1024 / 1024; // size in MB
        uploadStatus.textContent = 'Photo has been uploaded. ' + fileSize.toFixed(2) + ' MB';

        var reader = new FileReader();

        reader.onload = function(e) {
            uploadedImage = new Image();
            uploadedImage.onload = function() {
                var imageContainer = document.getElementById('image-container');
                imageContainer.innerHTML = '';
                imageContainer.appendChild(uploadedImage);
            };

            uploadedImage.src = e.target.result;
        };

        reader.readAsDataURL(fileInput.files[0]);
    } else {
        uploadStatus.textContent = '';
    }
}

function upscaleImage() {
    if (uploadedImage) {
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');

        // Upscale the image 2x
        canvas.width = uploadedImage.width * 2;
        canvas.height = uploadedImage.height * 2;

        ctx.drawImage(uploadedImage, 0, 0, canvas.width, canvas.height);

        var imageContainer = document.getElementById('image-container');
        imageContainer.innerHTML = '';
        imageContainer.appendChild(canvas);

        upscaledImage = canvas.toDataURL();
    }
}

function downloadImage() {
    if (upscaledImage) {
        var link = document.createElement('a');
        link.download = 'upscaled-image.png';
        link.href = upscaledImage;
        link.click();
    }
}