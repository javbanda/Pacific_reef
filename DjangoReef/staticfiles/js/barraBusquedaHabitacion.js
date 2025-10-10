document.addEventListener('DOMContentLoaded', function() {
    const checkinPicker = flatpickr("#checkin", {
        locale: "es",
        minDate: "today",
        dateFormat: "d-m-Y",
        altInput: true,
        altFormat: "j F Y",
        monthSelectorType: "static",
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 0) {
                const nextDay = new Date(selectedDates[0]);
                nextDay.setDate(nextDay.getDate() + 1);
                checkoutPicker.set("minDate", nextDay);
                
                if (checkoutPicker.selectedDates[0] && checkoutPicker.selectedDates[0] <= selectedDates[0]) {
                    checkoutPicker.clear();
                }
            }
        },
        onReady: function(selectedDates, dateStr, instance) {
            instance.calendarContainer.classList.add('custom-calendar');
        }
    });

    const checkoutPicker = flatpickr("#checkout", {
        locale: "es",
        minDate: "today",
        dateFormat: "d-m-Y",
        altInput: true,
        altFormat: "j F Y",
        monthSelectorType: "static",
        onReady: function(selectedDates, dateStr, instance) {
            instance.calendarContainer.classList.add('custom-calendar');
        }
    });

    let adultsCount = 1;
    let childrenCount = 0;
    let roomsCount = 1;

    const guestsDropdown = document.getElementById('guestsDropdown');
    const guestsModal = document.getElementById('guestsModal');
    const guestsText = document.getElementById('guestsText');
    const adultsCountElement = document.getElementById('adultsCount');
    const childrenCountElement = document.getElementById('childrenCount');
    const roomsCountElement = document.getElementById('roomsCount');

    document.getElementById('increaseAdults').addEventListener('click', () => updateGuests('adults', 1));
    document.getElementById('decreaseAdults').addEventListener('click', () => updateGuests('adults', -1));
    document.getElementById('increaseChildren').addEventListener('click', () => updateGuests('children', 1));
    document.getElementById('decreaseChildren').addEventListener('click', () => updateGuests('children', -1));
    document.getElementById('increaseRooms').addEventListener('click', () => updateGuests('rooms', 1));
    document.getElementById('decreaseRooms').addEventListener('click', () => updateGuests('rooms', -1));

    guestsDropdown.addEventListener('click', function(e) {
        e.stopPropagation();
        guestsModal.classList.toggle('show');
    });

    document.getElementById('applyGuests').addEventListener('click', function() {
        updateGuestsText();
        guestsModal.classList.remove('show');
    });

    document.addEventListener('click', function(e) {
        if (!guestsDropdown.contains(e.target) && !guestsModal.contains(e.target)) {
            guestsModal.classList.remove('show');
        }
    });

    guestsModal.addEventListener('click', function(e) {
        e.stopPropagation();
    });

    function updateGuests(type, change) {
        switch(type) {
            case 'adults':
                adultsCount = Math.max(1, adultsCount + change);
                adultsCountElement.textContent = adultsCount;
                break;
            case 'children':
                childrenCount = Math.max(0, childrenCount + change);
                childrenCountElement.textContent = childrenCount;
                break;
            case 'rooms':
                const newRoomsCount = Math.max(1, roomsCount + change);
                
                const minAdultsRequired = newRoomsCount;
                if (adultsCount < minAdultsRequired) {
                    adultsCount = minAdultsRequired;
                    adultsCountElement.textContent = adultsCount;
                }
                
                roomsCount = newRoomsCount;
                roomsCountElement.textContent = roomsCount;
                break;
        }
        
        updateButtonsState();
        updateGuestsText();
    }

    function updateGuestsText() {
        const adultsText = `${adultsCount} adulto${adultsCount !== 1 ? 's' : ''}`;
        const childrenText = childrenCount > 0 ? `, ${childrenCount} niño${childrenCount !== 1 ? 's' : ''}` : '';
        const roomsText = `, ${roomsCount} habitación${roomsCount !== 1 ? 'es' : ''}`;
        
        guestsText.textContent = adultsText + childrenText + roomsText;
    }

    function updateButtonsState() {
        const decreaseAdultsBtn = document.getElementById('decreaseAdults');
        const decreaseChildrenBtn = document.getElementById('decreaseChildren');
        const decreaseRoomsBtn = document.getElementById('decreaseRooms');
        const increaseAdultsBtn = document.getElementById('increaseAdults');
        const increaseChildrenBtn = document.getElementById('increaseChildren');
        const increaseRoomsBtn = document.getElementById('increaseRooms');

        decreaseAdultsBtn.disabled = adultsCount <= 1;
        decreaseChildrenBtn.disabled = childrenCount <= 0;
        decreaseRoomsBtn.disabled = roomsCount <= 1;

        const maxGuestsPerRoom = 4;
        const maxTotalGuests = roomsCount * maxGuestsPerRoom;
        const currentTotalGuests = adultsCount + childrenCount;
        const maxRooms = 5;

        increaseAdultsBtn.disabled = currentTotalGuests >= maxTotalGuests;
        increaseChildrenBtn.disabled = currentTotalGuests >= maxTotalGuests;
        increaseRoomsBtn.disabled = roomsCount >= maxRooms;

        const disabledButtons = document.querySelectorAll('.guest-btn:disabled');
        const enabledButtons = document.querySelectorAll('.guest-btn:not(:disabled)');
        
        disabledButtons.forEach(btn => {
            btn.style.opacity = '0.5';
            btn.style.cursor = 'not-allowed';
        });
        
        enabledButtons.forEach(btn => {
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
        });
    }

    document.getElementById('booking-form').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const checkin = document.getElementById('checkin').value;
        const checkout = document.getElementById('checkout').value;
        
        if (!checkin || !checkout) {
            showAlert('Por favor, selecciona las fechas de check-in y check-out', 'error');
            return;
        }

        if (adultsCount === 0) {
            showAlert('Debe haber al menos 1 adulto', 'error');
            return;
        }

        const checkinDate = checkinPicker.selectedDates[0];
        const checkoutDate = checkoutPicker.selectedDates[0];
        
        if (!checkinDate || !checkoutDate) {
            showAlert('Por favor, selecciona fechas válidas', 'error');
            return;
        }

        const nights = Math.ceil((checkoutDate - checkinDate) / (1000 * 60 * 60 * 24));

        if (nights <= 0) {
            showAlert('La fecha de check-out debe ser posterior al check-in', 'error');
            return;
        }

        const searchParams = new URLSearchParams({
            checkin: checkin,
            checkout: checkout,
            adults: adultsCount,
            children: childrenCount,
            rooms: roomsCount,
            nights: nights
        });

        showAlert('¡Búsqueda realizada con éxito! Redirigiendo...', 'success');
        
        setTimeout(() => {
            window.location.href = `/reserva/?${searchParams.toString()}`;
        }, 1500);
    });

    function showAlert(message, type) {
        const existingAlert = document.querySelector('.booking-alert');
        if (existingAlert) {
            existingAlert.remove();
        }

        const alert = document.createElement('div');
        alert.className = `booking-alert alert-${type}`;
        alert.textContent = message;
        alert.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            max-width: 300px;
        `;

        if (type === 'error') {
            alert.style.background = '#e53e3e';
        } else {
            alert.style.background = '#38a169';
        }

        document.body.appendChild(alert);

        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 4000);
    }

    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        .custom-calendar {
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
    `;
    document.head.appendChild(style);

    updateButtonsState();
    updateGuestsText();
    
    console.log('Sistema de reservas inicializado correctamente');
});