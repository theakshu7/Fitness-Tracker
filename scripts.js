$(document).ready(function() {
    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        var formData = new FormData(this);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            success: function(data) {
                // Fetch the latest images and update the gallery
                fetchImages();
                // Reset the form
                $('#upload-form')[0].reset();
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });

    function fetchImages() {
        $.get('/images', function(data) {
            $('.timeline').html('');
            data.images.forEach(function(image, index) {
                var timelineItem = `
                    <div class="timeline-item">
                        <div class="timeline-img">
                            <img src="/file/${image.filename}" alt="Progress Photo">
                        </div>
                        <div class="timeline-content">
                            <h3>${image.upload_date_str}</h3>
                        </div>
                    </div>
                `;
                $('.timeline').append(timelineItem);
            });
        });
    }

    // Initial fetch of images
    fetchImages();
});
