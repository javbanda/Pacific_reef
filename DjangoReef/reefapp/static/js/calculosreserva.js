function inicializarCalculosReserva(precioBase) {
    console.log('🎯 Iniciando cálculos de reserva...');
    
    const checkinInput = document.getElementById('fecha_checkin');
    const checkoutInput = document.getElementById('fecha_checkout');
    
    if (!checkinInput || !checkoutInput) {
        console.log('⏹️ No es página de reserva');
        return;
    }
    
    console.log('✅ Configurando cálculos para reserva');
    
    function calcularReserva() {
        if (!checkinInput.value || !checkoutInput.value) {
            resetearCalculos();
            return;
        }
        
        const inicio = new Date(checkinInput.value);
        const fin = new Date(checkoutInput.value);
        
        if (isNaN(inicio) || isNaN(fin) || inicio >= fin) {
            resetearCalculos();
            return;
        }
        
        const diffTiempo = fin - inicio;
        const dias = Math.ceil(diffTiempo / (1000 * 60 * 60 * 24));
        
        const subtotal = precioBase * dias;
        const impuestos = subtotal * 0.19;
        const servicio = 5000;
        const totalEstadia = subtotal + impuestos + servicio;
        const pagoReserva = totalEstadia * 0.3;
        const saldoPendiente = totalEstadia * 0.7;
        
        function formatoMoneda(monto) {
            return '$' + Math.round(monto).toLocaleString('es-CL');
        }
        
        try {
            document.getElementById('noches-count').textContent = dias + ' noche' + (dias !== 1 ? 's' : '');
            document.getElementById('subtotal-estadia').textContent = formatoMoneda(subtotal);
            document.getElementById('impuestos').textContent = formatoMoneda(impuestos);
            document.getElementById('total-estadia').textContent = formatoMoneda(totalEstadia);
            document.getElementById('pago-reserva').textContent = formatoMoneda(pagoReserva);
            document.getElementById('saldo-pendiente').textContent = formatoMoneda(saldoPendiente);
            document.getElementById('total-pagar').textContent = formatoMoneda(pagoReserva);
            document.getElementById('pago-reserva-text').textContent = formatoMoneda(pagoReserva);
            document.getElementById('saldo-pendiente-text').textContent = formatoMoneda(saldoPendiente);
        } catch (error) {
            console.error('Error actualizando interfaz:', error);
        }
    }
    
    function resetearCalculos() {
        const elementos = [
            'noches-count', 'subtotal-estadia', 'impuestos', 'total-estadia',
            'pago-reserva', 'saldo-pendiente', 'total-pagar',
            'pago-reserva-text', 'saldo-pendiente-text'
        ];
        
        elementos.forEach(id => {
            const elemento = document.getElementById(id);
            if (elemento) {
                if (id === 'noches-count') {
                    elemento.textContent = '0 noches';
                } else {
                    elemento.textContent = '$0';
                }
            }
        });
    }

    checkinInput.addEventListener('change', calcularReserva);
    checkoutInput.addEventListener('change', calcularReserva);
    
    if (checkinInput.value && checkoutInput.value) {
        setTimeout(calcularReserva, 100);
    }
    
    console.log('✅ Sistema de cálculos configurado');
}

document.addEventListener('DOMContentLoaded', function() {
    const datosElemento = document.getElementById('datos-reserva');
    
    if (datosElemento) {
        const precioBase = parseFloat(datosElemento.getAttribute('data-precio'));
        inicializarCalculosReserva(precioBase);
    }
});