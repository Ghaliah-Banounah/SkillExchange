(() => {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault()
                event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
    })
})()

// Preview uploaded image
function previewImage(event) {
    var input = event.target;
    var image = document.getElementById('preview');
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            image.src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

// Tabs in profile
document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".tab-button");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach((tab) => {
        tab.addEventListener("click", function () {
            tabs.forEach((t) => t.classList.remove("active"));
            contents.forEach((c) => c.classList.remove("active"));

            this.classList.add("active");
            document.getElementById(this.dataset.tab).classList.add("active");
        });
    });
});

// Set min date to today and use Date Range Picker
$('input[name="scheduled_at"]').daterangepicker({
    locale: {
        format: 'YYYY-MM-DD'
    },
    minDate: new Date(),
});


// Delete Chat from Direct Messages for Chats app
function confirmDelete() {
    return confirm("Are You sure you want delete this chat ?");
}

// Function to display the name of the selected file for Chats app
function displayFileName() {
    var fileInput = document.getElementById('file-upload');
    var fileNameDisplay = document.getElementById('file-name-display');
    if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = fileInput.files[0].name;
    } else {
         fileNameDisplay.textContent = '';
        }
    }
// This function is called when the page is fully loaded for Chats app
window.onload = function() {
    var chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

//Disable the alerts in Chats app
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('chat-page');
});

//remove footer margin top for Chats app
document.addEventListener('DOMContentLoaded', function() {
if (window.location.pathname.includes('/chats/chat/')) {
   var footer = document.querySelector('footer');
   footer.classList.remove('mt-5');
   }
});
