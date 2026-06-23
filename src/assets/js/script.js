document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        themeSystem: 'standard',
        // Aqui o calendário busca os dados automaticamente
        events: '../data/eventos.json' 
    });
    calendar.render();
});

