document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('participants-container');
    const addButton = document.getElementById('add-participant');
    const totalFormsInput = document.getElementById('id_participants-TOTAL_FORMS');

    if (!container || !addButton || !totalFormsInput) {
        return;
    }

    const emptyRow = container.querySelector('.participant-row');
    if (!emptyRow) {
        return;
    }

  const updateLabels = () => {
        container.querySelectorAll('.participant-row').forEach((row, index) => {
            const input = row.querySelector('input[type="email"]');
            const label = row.querySelector('label');
            if (!input || !label) {
                return;
            }

            const fieldId = `id_participants-${index}-email`;
            input.name = `participants-${index}-email`;
            input.id = fieldId;
            label.setAttribute('for', fieldId);

            if (input.value) {
                label.classList.add('active');
            }
        });
    };

    addButton.addEventListener('click', () => {
        const index = parseInt(totalFormsInput.value, 10);
        const row = emptyRow.cloneNode(true);

        const input = row.querySelector('input[type="email"]');
        const label = row.querySelector('label');
        const helper = row.querySelector('.helper-text');

        if (input) {
            input.value = '';
            input.name = `participants-${index}-email`;
            input.id = `id_participants-${index}-email`;
        }

        if (label) {
            label.setAttribute('for', `id_participants-${index}-email`);
            label.classList.remove('active');
        }

        if (helper) {
            helper.remove();
        }

        container.appendChild(row);
        totalFormsInput.value = index + 1;

        if (typeof M !== 'undefined' && M.updateTextFields) {
            M.updateTextFields();
        }
    });

    updateLabels();
});
