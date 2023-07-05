var uploadedImage;
var upscaledImage;

function updateUploadStatus() {
    var fileInput = document.getElementById('file');
    var uploadStatus = document.querySelector('.upload-status');
    var uploadButtons = document.getElementById('upload-buttons');

    if (fileInput.files.length > 0) {
        var fileSize = fileInput.files[0].size / 1024 / 1024; // size in MB
        uploadStatus.textContent = 'Photo has been uploaded. ' + fileSize.toFixed(2) + ' MB';

        var reader = new FileReader();

        reader.onload = function (e) {
            uploadedImage = new Image();
            uploadedImage.onload = function () {
                var imageContainer = document.getElementById('image-container');
                imageContainer.innerHTML = '';
                imageContainer.appendChild(uploadedImage);

                document.getElementById('uploaded-column').style.display = 'none';
                document.getElementById('upscaled-column').style.display = 'none';
                uploadButtons.style.display = 'block';
                document.getElementById('download-button').style.display = 'none';
            };

            uploadedImage.src = e.target.result;
        };

        reader.readAsDataURL(fileInput.files[0]);
    } else {
        uploadStatus.textContent = '';
        uploadButtons.style.display = 'none';
        document.getElementById('download-button').style.display = 'none';
    }
}


function upscaleImage() {
    if (uploadedImage) {
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');

        exec(`python ${__dirname}/../../edsr_main.py ${uploadedImage}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return;
            }
            console.log(`stdout: ${stdout}`);
            console.error(`stderr: ${stderr}`);

            upscaled = new Image();
            upscaled.src = stdout.trim();
            upscaled.onload = () => {
                canvas.width = upscaled.width * 2;
                canvas.height = upscaled.height * 2;

                ctx.drawImage(upscaled, 0, 0, canvas.width, canvas.height);

                var imageContainer = document.getElementById('image-container');
                imageContainer.innerHTML = '';
                imageContainer.appendChild(canvas);

                upscaledImage = canvas.toDataURL();

                document.getElementById('upload-buttons').style.display = 'none';
                document.getElementById('download-button').style.display = 'block';
                document.getElementById('uploaded-column').style.display = 'grid';
                document.getElementById('upscaled-column').style.display = 'grid';

                var uploadedImageContainer = document.getElementById('uploaded-image-container');
                uploadedImageContainer.innerHTML = '';
                uploadedImageContainer.appendChild(uploadedImage);

                var upscaledImageContainer = document.getElementById('upscaled-image-container');
                upscaledImageContainer.innerHTML = '';
                upscaledImageContainer.appendChild(canvas);
            };
        });
    }
}


/*function upscaleImage() {
    if (uploadedImage) {
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');

        canvas.width = uploadedImage.width * 3;
        canvas.height = uploadedImage.height * 3;

        ctx.drawImage(uploadedImage, 0, 0, canvas.width, canvas.height);

        var imageContainer = document.getElementById('image-container');
        imageContainer.innerHTML = '';
        imageContainer.appendChild(canvas);

        upscaledImage = canvas.toDataURL();

        document.getElementById('upload-buttons').style.display = 'none';
        document.getElementById('download-button').style.display = 'block';
        document.getElementById('uploaded-column').style.display = 'grid';
        document.getElementById('upscaled-column').style.display = 'grid';

        var uploadedImageContainer = document.getElementById('uploaded-image-container');
        uploadedImageContainer.innerHTML = '';
        uploadedImageContainer.appendChild(uploadedImage);

        var upscaledImageContainer = document.getElementById('upscaled-image-container');
        upscaledImageContainer.innerHTML = '';
        upscaledImageContainer.appendChild(canvas);
    }
}*/

function downloadImage() {
    if (upscaledImage) {
        var link = document.createElement('a');
        link.download = 'upscaled-image.png';
        link.href = upscaledImage;
        link.click();
    }
}
