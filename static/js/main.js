document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Animación suave para mensajes de alerta con mejor estilo
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        alert.style.transition = 'all 0.3s ease-in-out';
        alert.style.transform = 'translateY(0)';
        alert.style.opacity = '1';
        
        setTimeout(function() {
            alert.style.transform = 'translateY(-20px)';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 3000);
    });

    // Mejorar la interactividad de las tarjetas de libros con efectos modernos
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        card.style.transition = 'all 0.3s ease-in-out';
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 5px 15px rgba(0,0,0,0.2)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });
    });

    // Inicializar los modales de Bootstrap con animación mejorada
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        new bootstrap.Modal(modal);
        modal.addEventListener('show.bs.modal', function() {
            this.style.animation = 'fadeIn 0.3s';
        });
    });

    // La lógica del campo CdA se maneja en registro.html

    // Añadir efecto de hover a los botones
    var buttons = document.querySelectorAll('.btn');
    buttons.forEach(function(button) {
        button.style.transition = 'all 0.2s ease-in-out';
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Añadir animación suave al scroll
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId !== '#') {
                document.querySelector(targetId).scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Añadir estilos CSS para las animaciones
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .modal.show {
        animation: fadeIn 0.3s;
    }

    .card {
        transition: all 0.3s ease-in-out;
    }

    .btn {
        transition: all 0.2s ease-in-out;
    }
`;
document.head.appendChild(style);