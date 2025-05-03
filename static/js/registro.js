document.addEventListener('DOMContentLoaded', function() {
    const roleInputs = document.querySelectorAll('input[name="role"]');
    const notificationsGroup = document.querySelectorAll('.notifications-group');
    const codigoAutenticacion = document.getElementById('codigo-autenticacion');

    function toggleNotifications(role) {
        notificationsGroup.forEach(group => {
            group.style.display = role === 'BIBLIOTECARIO' ? 'none' : 'block';
        });
        codigoAutenticacion.style.display = role === 'BIBLIOTECARIO' ? 'block' : 'none';
    }

    roleInputs.forEach(input => {
        input.addEventListener('change', function() {
            toggleNotifications(this.value);
        });
    });

    // Establecer estado inicial
    const selectedRole = document.querySelector('input[name="role"]:checked');
    if (selectedRole) {
        toggleNotifications(selectedRole.value);
    }
});