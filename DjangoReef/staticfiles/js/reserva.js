const roomsData = [
    {
        id: 1,
        name: "Habitación Individual",
        category: "turista",
        type: "individual",
        description: "Ideal para viajeros solos, con todas las comodidades esenciales.",
        price: 45000,
        capacity: 1,
        images: [
            "/static/img/habitaciones/hindiv1.jpg",
            "/static/img/habitaciones/hindiv2.jpg",
            "/static/img/habitaciones/baño.jpg"
        ],
        features: [
            "Cama individual premium",
            "Baño privado con ducha",
            "TV LED 32\" con cable",
            "WiFi gratuito",
            "Aire acondicionado"
        ],
        available: 8
    },
    {
        id: 2,
        name: "Habitación Doble",
        category: "turista",
        type: "doble",
        description: "Perfecta para parejas, con espacio cómodo y confortable.",
        price: 65000,
        capacity: 2,
        images: [
            "/static/img/habitaciones/hdoble1.jpg",
            "/static/img/habitaciones/hdoble2.jpg",
            "/static/img/habitaciones/baño.jpg"
        ],
        features: [
            "Cama doble queen o 2 individuales",
            "Baño privado con ducha panorámica",
            "TV LED 40\" Smart TV",
            "Mini nevera",
            "WiFi high speed"
        ],
        available: 12
    },
    {
        id: 3,
        name: "Habitación Familiar",
        category: "turista",
        type: "familiar",
        description: "Amplio espacio para familias, diseñado para su comodidad.",
        price: 85000,
        capacity: 4,
        images: [
            "/static/img/habitaciones/hfamiliar1.jpg",
            "/static/img/habitaciones/hfamiliar2.jpg",
            "/static/img/habitaciones/baño.jpg"
        ],
        features: [
            "2 camas dobles full size",
            "Baño con bañera/ducha",
            "TV LED 43\" Smart TV",
            "Sofá cama adicional",
            "Espacio amplio familiar"
        ],
        available: 10
    },
    {
        id: 4,
        name: "Suite Doble Premium",
        category: "premium",
        type: "doble",
        description: "Elegancia y sofisticación con vista al mar. Experimenta el lujo contemporáneo en un espacio diseñado para el descanso y la desconexión total.",
        price: 120000,
        capacity: 4,
        images: [
            "/static/img/habitaciones/sdoblep1.jpg",
            "/static/img/habitaciones/sdoblep2.jpg",
            "/static/img/habitaciones/sdoblep3.jpg"
        ],
        features: [
            "Cama king size premium",
            "Baño de lujo con jacuzzi",
            "TV LED 55\" 4K Smart TV",
            "Balcón privado con vista al mar",
            "Minibar surtido",
            "Nespresso coffee machine"
        ],
        available: 4
    },
    {
        id: 5,
        name: "Suite Familiar Premium",
        category: "premium",
        type: "familiar",
        description: "Ideal para disfrutar en familia, con espacios amplios y luminosos. El escenario perfecto para vacaciones memorables, donde cada miembro encuentra su espacio de confort y lujo.",
        price: 160000,
        capacity: 4,
        images: [
            "/static/img/habitaciones/sfamiliarp1.jpg",
            "/static/img/habitaciones/sfamiliarp2.jpg",
            "/static/img/habitaciones/sfamiliarp3.jpg"
        ],
        features: [
            "Cama king size premium",
            "Baño de lujo con jacuzzi",
            "TV LED 55\" 4K Smart TV",
            "Balcón privado con vista al mar",
            "Minibar surtido",
            "Nespresso coffee machine"
        ],
        available: 4
    }
];

document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const checkin = urlParams.get('checkin');
    const checkout = urlParams.get('checkout');
    const adults = urlParams.get('adults');
    const children = urlParams.get('children');
    const rooms = urlParams.get('rooms');

    displaySearchSummary(checkin, checkout, adults, children, rooms);

    loadAvailableRooms(checkin, checkout, adults, children);

    setupFilters();
});

function displaySearchSummary(checkin, checkout, adults, children, rooms) {
    const searchDetails = document.getElementById('searchDetails');

    if (!searchDetails) {
        console.error('Elemento searchDetails no encontrado');
        return;
    }

    const totalGuests = parseInt(adults || 1) + parseInt(children || 0);

    let html = `
        <div class="row">
            <div class="col-sm-3">
                <strong>Check-in:</strong><br>
                ${checkin ? formatDate(checkin) : 'No seleccionado'}
            </div>
            <div class="col-sm-3">
                <strong>Check-out:</strong><br>
                ${checkout ? formatDate(checkout) : 'No seleccionado'}
            </div>
            <div class="col-sm-3">
                <strong>Huéspedes:</strong><br>
                ${totalGuests} persona${totalGuests !== 1 ? 's' : ''}
            </div>
            <div class="col-sm-3">
                <strong>Habitaciones:</strong><br>
                ${rooms || 1}
            </div>
        </div>
    `;

    searchDetails.innerHTML = html;
}

function formatDate(dateString) {
    if (!dateString) return 'Fecha no válida';

    try {
        const [day, month, year] = dateString.split('-');
        const date = new Date(year, month - 1, day);

        if (isNaN(date.getTime())) {
            return dateString;
        }

        const options = { day: 'numeric', month: 'long', year: 'numeric' };
        return date.toLocaleDateString('es-ES', options);
    } catch (error) {
        console.error('Error formateando fecha:', error);
        return dateString;
    }
}

function getRoomTypeDisplay(tipo) {
    const typeMap = {
        'individual': 'Individual',
        'doble': 'Doble',
        'familiar': 'Familiar',
        'suite': 'Suite Premium',
        'suiteD': 'Suite Doble',
        'suiteF': 'Suite Familiar'
    };
    return typeMap[tipo] || tipo.charAt(0).toUpperCase() + tipo.slice(1);
}

function getRoomCategoryDisplay(categoria, tipo) {
    if (categoria === 'Premium') {
        return 'Premium';
    }
    return getRoomTypeDisplay(tipo);
}

async function loadAvailableRooms(checkin, checkout, adults, children) {
    try {
        let apiUrl = '/api/habitaciones-disponibles/';
        const params = new URLSearchParams();

        if (checkin) params.append('checkin', checkin);
        if (checkout) params.append('checkout', checkout);
        if (adults) params.append('adultos', adults);
        if (children) params.append('ninos', children);

        if (params.toString()) {
            apiUrl += '?' + params.toString();
        }

        console.log('🔍 Solicitando habitaciones desde:', apiUrl); // Debug

        const response = await fetch(apiUrl);

        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }

        const roomsData = await response.json();
        console.log('✅ Habitaciones recibidas:', roomsData); // Debug

        if (roomsData.error) {
            throw new Error(roomsData.error);
        }

        displayRooms(roomsData);

    } catch (error) {
        console.error('❌ Error cargando habitaciones:', error);

        const container = document.getElementById('roomsContainer');
        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle"></i>
                    <strong>Error al cargar habitaciones:</strong><br>
                    ${error.message}
                    <br><small>Se mostrarán habitaciones de ejemplo.</small>
                </div>
            `;
        }

        loadSampleRooms();
    }
}

function loadSampleRooms() {
    const sampleRooms = [
        {
            id: 1,
            numero: '101',
            categoria: 'Turista',
            tipo: 'individual',
            precio: 45000,
            capacidad: '1 adulto',
            descripcion: 'Habitación individual económica, ideal para viajeros solos'
        },
        {
            id: 2,
            numero: '102',
            categoria: 'Turista',
            tipo: 'doble',
            precio: 65000,
            capacidad: '2 adultos',
            descripcion: 'Habitación doble para parejas, con cama queen size'
        },
        {
            id: 3,
            numero: '201',
            categoria: 'Premium',
            tipo: 'suite',
            precio: 120000,
            capacidad: '2 adultos',
            descripcion: 'Suite premium con jacuzzi y vista al mar'
        }
    ];

    displayRooms(sampleRooms);
}

function displayRooms(rooms) {
    const container = document.getElementById('roomsContainer');
    const roomCount = document.getElementById('roomCount');

    if (!container) {
        console.error('Elemento roomsContainer no encontrado');
        return;
    }

    if (rooms.length === 0) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-bed fa-3x text-muted mb-3"></i>
                <h4>No se encontraron habitaciones disponibles</h4>
                <p class="text-muted">Intenta modificar tus criterios de búsqueda</p>
                <button class="btn btn-primary mt-3" onclick="window.history.back()">
                    <i class="fas fa-arrow-left me-2"></i>Modificar búsqueda
                </button>
            </div>
        `;
    } else {
        container.innerHTML = rooms.map(room => `
            <div class="card room-card" data-category="${room.categoria.toLowerCase()}" data-type="${room.tipo}" data-price="${room.precio}">
                <div class="row g-0">
                    <div class="col-md-4">
                        <img src="${getRoomImageSrc(room.tipo, room.numero)}" 
     class="card-img-top room-image" 
     alt="${room.descripcion}"
     onerror="handleImageError(this)">
                    </div>
                    <div class="col-md-5">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h5 class="card-title">Habitación ${room.numero} - ${getRoomTypeDisplay(room.tipo)}</h5>
                                <span class="availability-badge">
                                    <i class="fas fa-check"></i> Disponible
                                </span>
                            </div>
                            <p class="card-text text-muted">${room.descripcion}</p>
                            <div class="room-features">
                                <div><i class="fas fa-users"></i> ${room.capacidad}</div>
                                <div><i class="fas fa-star"></i> ${room.categoria}</div>
                                <div><i class="fas fa-building"></i> Piso ${room.numero.charAt(0)}</div>
                                <div><i class="fas fa-wifi"></i> WiFi Gratuito</div>
                                <div><i class="fas fa-tv"></i> TV Cable</div>
                                <div><i class="fas fa-snowflake"></i> Aire Acondicionado</div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="card-body h-100 d-flex flex-column justify-content-between">
                            <div class="price-section">
                                <div class="price-amount">$${room.precio.toLocaleString('es-CL')}</div>
                                <div class="price-period">por noche</div>
                                <small class="text-muted">Impuestos incluidos</small>
                            </div>
                            <button class="btn btn-reserve w-100 mt-3" style="color: #ffffff;" onclick="reserveRoom(${room.id})">
                                <i class="fas fa-calendar-check me-2"></i>Reservar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }

    if (roomCount) {
        roomCount.textContent = `${rooms.length} habitación${rooms.length !== 1 ? 'es' : ''} encontrada${rooms.length !== 1 ? 's' : ''}`;
    }
}

function getRoomImageSrc(tipo, numero) {
    const imageMap = {
        'individual': '/static/img/habitaciones/hindiv1.jpg',
        'doble': '/static/img/habitaciones/hdoble1.jpg',
        'familiar': '/static/img/habitaciones/hfamiliar1.jpg',
        'suiteD': '/static/img/habitaciones/sdoblep1.jpg',
        'suiteF': '/static/img/habitaciones/sfamiliarp1.jpg',
        'suite': '/static/img/habitaciones/sdoblep1.jpg'
    };

    return imageMap[tipo] || '/static/img/habitaciones/default.jpg';
}
function setupFilters() {
    const priceRange = document.getElementById('priceRange');
    const priceRangeValue = document.getElementById('priceRangeValue');

    if (priceRange && priceRangeValue) {
        priceRange.addEventListener('input', function () {
            priceRangeValue.textContent = `$${parseInt(this.value).toLocaleString('es-CL')}`;
        });
    }

    document.querySelectorAll('input[type="checkbox"], #priceRange').forEach(element => {
        element.addEventListener('change', applyFilters);
    });
}

function applyFilters() {
    const categoryTurista = document.getElementById('filterTurista')?.checked ?? true;
    const categoryPremium = document.getElementById('filterPremium')?.checked ?? true;
    const selectedTypes = Array.from(document.querySelectorAll('.room-type:checked')).map(cb => cb.value);
    const maxPrice = parseInt(document.getElementById('priceRange')?.value || 200000);

    const roomCards = document.querySelectorAll('.room-card');
    let visibleCount = 0;

    roomCards.forEach(card => {
        const category = card.getAttribute('data-category');
        const type = card.getAttribute('data-type');
        const price = parseFloat(card.getAttribute('data-price'));

        const categoryMatch =
            (category === 'turista' && categoryTurista) ||
            (category === 'premium' && categoryPremium);

        const typeMatch = selectedTypes.length === 0 || selectedTypes.includes(type);
        const priceMatch = price <= maxPrice;

        const shouldShow = categoryMatch && typeMatch && priceMatch;
        card.style.display = shouldShow ? 'block' : 'none';

        if (shouldShow) visibleCount++;
    });

    const roomCount = document.getElementById('roomCount');
    if (roomCount) {
        roomCount.textContent = `${visibleCount} habitación${visibleCount !== 1 ? 'es' : ''} encontrada${visibleCount !== 1 ? 's' : ''}`;
    }
}

function openImageModal(imageSrc, roomName) {
    const modalImage = document.getElementById('modalImage');
    const modalLabel = document.getElementById('imageModalLabel');

    if (modalImage && modalLabel) {
        modalImage.src = imageSrc;
        modalLabel.textContent = roomName;

        const modalElement = document.getElementById('imageModal');
        if (modalElement && typeof bootstrap !== 'undefined') {
            const modal = new bootstrap.Modal(modalElement);
            modal.show();
        }
    }
}

function reserveRoom(roomId) {
    const urlParams = new URLSearchParams(window.location.search);

    window.location.href = `/reservar/${roomId}/?${urlParams.toString()}`;
}

window.applyFilters = applyFilters;
window.openImageModal = openImageModal;
window.reserveRoom = reserveRoom;
window.formatDate = formatDate;
window.getRoomTypeDisplay = getRoomTypeDisplay;