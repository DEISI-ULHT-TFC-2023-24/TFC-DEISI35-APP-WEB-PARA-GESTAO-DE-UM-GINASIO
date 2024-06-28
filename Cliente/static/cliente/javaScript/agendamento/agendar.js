document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        dateClick: function(info) {
            const appointmentDate = document.getElementById('appointment-date');
            appointmentDate.value = info.dateStr;
        },
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        editable: true,
        events: [],  // placeholder for events if needed
        validRange: function(nowDate) {
            return {
                start: nowDate,
                end: new Date(nowDate.getFullYear() + 1, nowDate.getMonth(), nowDate.getDate())
            };
        },
        select: function(info) {
            if (isInvalidDate(info.start)) {
                alert('Data fora do horário de funcionamento.');
                return;
            }
            const appointmentDate = document.getElementById('appointment-date');
            const appointmentTime = document.getElementById('appointment-time');
            appointmentDate.value = info.startStr.split('T')[0];
            appointmentTime.value = info.startStr.split('T')[1] || '';
        },
        businessHours: [
            {
                daysOfWeek: [1, 2, 3, 4, 5], // Segunda a sexta
                startTime: '07:00',
                endTime: '21:30'
            },
            {
                daysOfWeek: [6], // Sábado
                startTime: '09:00',
                endTime: '13:00'
            }
        ],
        selectConstraint: "businessHours"
    });
    calendar.render();

    const appointmentForm = document.getElementById('appointment-form');
    const appointmentName = document.getElementById('appointment-name');
    const appointmentType = document.getElementById('appointment-type');
    const appointmentDate = document.getElementById('appointment-date');
    const appointmentTime = document.getElementById('appointment-time');
    const appointmentNote = document.getElementById('appointment-note');
    const appointmentEmail = document.getElementById('appointment-email');
    const appointmentContact = document.getElementById('appointment-contact');
    const cancelButton = document.getElementById('cancel-button');
    const scheduleButton = document.getElementById('schedule-button');
    const cancelModal = new bootstrap.Modal(document.getElementById('cancelModal'));
    const confirmModal = new bootstrap.Modal(document.getElementById('confirmModal'));
    const summaryContent = document.getElementById('summary-content');

    // Função para obter o CSRF token (se necessário)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    function getSummary() {
        return `
            <strong>Nome:</strong> ${appointmentName.value}<br>
            <strong>Tipo de Visita:</strong> ${appointmentType.value}<br>
            <strong>Data:</strong> ${appointmentDate.value}<br>
            <strong>Hora:</strong> ${appointmentTime.value}<br>
            <strong>Nota:</strong> ${appointmentNote.value || 'N/A'}<br>
            <strong>Email:</strong> ${appointmentEmail.value}<br>
            <strong>Contato:</strong> ${appointmentContact.value}
        `;
    }

    function isInvalidDate(date) {
        const day = date.getUTCDay();
        const hour = date.getUTCHours();
        const minute = date.getUTCMinutes();

        if (day === 0) return true; // Sunday
        if (day >= 1 && day <= 5) { // Monday to Friday
            if (hour < 7 || (hour >= 21 && minute > 30)) return true;
        }
        if (day === 6) { // Saturday
            if (hour < 9 || hour >= 13) return true;
        }
        return false;
    }

    function sendAppointment() {
        const agendamento = {
            nome: appointmentName.value,
            tipo: appointmentType.value,
            data: appointmentDate.value,
            hora: appointmentTime.value,
            email: appointmentEmail.value,
            contato: appointmentContact.value,
            nota: appointmentNote.value || ''
        };

        fetch('/api/agendamentos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(agendamento)
        })
        .then(response => response.json())
        .then(data => {
            if (data.detail) {
                alert(data.detail);
            } else {
                alert('Agendamento realizado com sucesso.');
                window.location.href = '/';
            }
        })
        .catch(error => console.error('Erro:', error));
    }

    cancelButton.addEventListener('click', () => {
        cancelModal.show();
    });

    document.getElementById('confirm-cancel').addEventListener('click', () => {
        cancelModal.hide();
        alert('Agendamento cancelado.');
        window.location.href = '/';
    });

    scheduleButton.addEventListener('click', () => {
        if (appointmentForm.checkValidity()) {
            summaryContent.innerHTML = getSummary();
            confirmModal.show();
        } else {
            appointmentForm.reportValidity();
        }
    });

    document.getElementById('confirm-schedule').addEventListener('click', () => {
        confirmModal.hide();
        sendAppointment();
    });
});
