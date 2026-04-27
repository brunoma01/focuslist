const dueInput = document.getElementById('due_date');

function openModal() {
    document.getElementById('confirmModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('confirmModal').style.display = 'none';
}

function startEdit(button) {
    document.querySelectorAll('.edit-form:not(.hidden)').forEach(form => {
        cancelEdit(form);
    });

    const li = button.closest('li');

    const title = li.querySelector('.task-title');
    const form = li.querySelector('.edit-form');

    title.classList.add('hidden');
    form.classList.remove('hidden');

    const input = form.querySelector('input');
    input.focus();
    input.select();
}

function cancelEdit(form) {
    const li = form.closest('li');

    const title = li.querySelector('.task-title');
    const input = form.querySelector('input');

    input.value = title.innerText;

    form.classList.add('hidden');
    title.classList.remove('hidden');

    input.blur();
}

document.addEventListener('click', function(event) {
    const modal = document.getElementById('confirmModal');

    if (event.target === modal) {
        modal.style.display = "none";
    }
});

document.querySelectorAll('.toast').forEach((toast) => {
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);

    setTimeout(() => {
        toast.classList.remove('show');
        toast.remove();
    }, 2500);
});

document.addEventListener('click', function(e) {
    const editingForms = document.querySelectorAll('.edit-form');

    editingForms.forEach(form => {
        if (!form.classList.contains('hidden')) {

            const li = form.closest('li');

            if (!li.contains(e.target)) {
                cancelEdit(form);
            }
        }
    });
});

document.querySelectorAll('.edit-input').forEach(input => {
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            this.form.submit();
        }

        if (e.key === 'Escape') {
            cancelEdit(this.closest('form'));
        }
    });
});

if (dueInput) {
    dueInput.addEventListener('click', function() {
        if (this.showPicker) {
            this.showPicker();
        }
    });
}