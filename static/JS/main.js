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

const form = document.getElementById('image-upload-form');
            const fileInput = document.getElementById('image-file-input');
            const upscaledImageContainer = document.getElementById('upscaled-image-container');

            form.addEventListener('submit', (event) => {
                event.preventDefault();
                const file = fileInput.files[0];
                const reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = () => {
                    const imageData = reader.result.split(',')[1];
                    upscaleImage(imageData);
                };
            });

            function upscaleImage(imageData) {
                const spinner = document.createElement('div');
                spinner.classList.add('spinner');
                upscaledImageContainer.appendChild(spinner);
              
                fetch('/upscale', {
                  method: 'POST',
                  headers: {
                    'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({ image_data: imageData })
                })
                  .then(response => response.json())
                  .then(data => {
                    const upscaledImageData = data.upscaled_image_bytes;
                    const upscaledImage = new Image();
                    upscaledImage.src = 'data:image/jpeg;base64,' + upscaledImageData;
                    upscaledImage.onload = () => {
                      upscaledImageContainer.removeChild(spinner);
                      upscaledImageContainer.appendChild(upscaledImage);
                      document.getElementById('download-button').style.display = 'block';
                    };
                  })
                  .catch(error => {
                    console.error(error);
                    upscaledImageContainer.removeChild(spinner);
                    alert('Failed to upscale image. Please try again.');
                  });
              }

              /**function upscaleImage(imageData) {
                const spinner = document.createElement('div');
                spinner.classList.add('spinner');
                upscaledImageContainer.appendChild(spinner);
            
                fetch('/upscale', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ image_data: imageData })
                })
                .then(response => response.json())
                .then(data => {
                    const upscaledImage = new Image();
                    upscaledImage.src = 'data:image/jpeg;base64,' + data.upscaled_image_data;
                    upscaledImage.onload = () => {
                        upscaledImageContainer.removeChild(spinner);
                        const canvas = document.createElement('canvas');
                        canvas.width = upscaledImage.width;
                        canvas.height = upscaledImage.height;
                        const context = canvas.getContext('2d');
                        context.drawImage(upscaledImage, 0, 0);
                        const upscaledImageData = canvas.toDataURL('image/jpeg');
                        const upscaledImageElement = document.createElement('img');
                        upscaledImageElement.src = upscaledImageData;
                        upscaledImageContainer.appendChild(upscaledImageElement);
                    };
                })
                .catch(error => console.error(error));
            }**/

function downloadImage() {
    if (upscaledImage) {
        const link = document.createElement('a');
        link.download = 'upscaled-image.jpg';
        link.href = upscaledImage.replace(/^data:image\/[^;]+/, 'data:application/octet-stream');
        link.click();
    }
}

