// static/js/script.js

const categorySelect = document.getElementById('category');
const otherBox = document.getElementById('otherBox');
const otherInput = document.getElementById('otherInput');
const form = document.getElementById('maintenanceForm');
const progressFill = document.getElementById('progressFill');
const submitBtn = document.getElementById('submitBtn');
const responseMessage = document.getElementById('responseMessage');

// ---------- CATEGORY LOGIC ----------
categorySelect.addEventListener('change', () => {
    if (categorySelect.value === 'Other') {
        otherBox.classList.remove('hidden');
        otherInput.required = true;
    } else {
        otherBox.classList.add('hidden');
        otherInput.required = false;
        otherInput.value = '';
    }
    updateProgressBar();
});

// ---------- PROGRESS BAR ----------
function updateProgressBar() {
    const requiredFields = form.querySelectorAll(
        'input[required], select[required], textarea[required]'
    );

    let filled = 0;

    requiredFields.forEach(field => {
        if (field.type === 'radio') {
            if (form.querySelector(`input[name="${field.name}"]:checked`)) {
                filled++;
            }
        } else if (field.value.trim() !== '') {
            filled++;
        }
    });

    const progress = (filled / requiredFields.length) * 100;
    progressFill.style.width = `${progress}%`;
}

form.addEventListener('input', updateProgressBar);
form.addEventListener('change', updateProgressBar);

// ---------- DEFAULT DATE ----------
const issueDate = document.querySelector('input[name="issue_date"]');
issueDate.value = new Date().toISOString().split('T')[0];

// ---------- FORM SUBMIT ----------
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        phone: formData.get('phone'),
        block: formData.get('block'),
        floor: formData.get('floor'),
        room_no: formData.get('room_no'),
        category: formData.get('category'),
        other_detail: formData.get('other_detail') || '',
        priority: formData.get('priority'),
        issue_date: formData.get('issue_date'),
        description: formData.get('description')
    };

    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';

    try {
        const response = await fetch('/api/maintenance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.message || 'Submission failed');
        }

        // SUCCESS UI
        responseMessage.classList.remove('hidden');
        form.style.display = 'none';
        document.getElementById('ticketId').textContent = result.ticket_id;

        const submitAnother = document.createElement('button');
        submitAnother.type = 'button';
        submitAnother.textContent = 'Submit Another Report';
        submitAnother.className = 'button';

        submitAnother.onclick = () => {
            form.reset();
            form.style.display = 'block';
            responseMessage.classList.add('hidden');
            progressFill.style.width = '0%';
            otherBox.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Report';
            submitAnother.remove();
        };

        responseMessage.appendChild(submitAnother);

    } catch (error) {
        console.error(error);
        alert('Submission failed. Please try again.');
        submitBtn.disabled = false;
        submitBtn.textContent = 'Submit Report';
    }
});

console.log('Campus Maintenance Portal loaded ✔');

