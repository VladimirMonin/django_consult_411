document.addEventListener('DOMContentLoaded', function() {
    const masterSelect = document.querySelector('#id_master');
    const servicesSelect = document.querySelector('#id_services');

    if (masterSelect && servicesSelect) {
        masterSelect.addEventListener('change', function() {
            const masterId = this.value;
            if (masterId) {
                fetch(`/ajax/get-master-services/?master_id=${masterId}`)
                    .then(response => response.json())
                    .then(data => {
                        servicesSelect.innerHTML = ''; // Очищаем список услуг
                        if (data.services) {
                            data.services.forEach(service => {
                                const option = document.createElement('option');
                                option.value = service.id;
                                option.textContent = service.name;
                                servicesSelect.appendChild(option);
                            });
                        }
                    })
                    .catch(error => console.error('Ошибка при загрузке услуг:', error));
            } else {
                servicesSelect.innerHTML = ''; // Очищаем, если мастер не выбран
            }
        });

        // Вызываем событие change при загрузке страницы, чтобы подгрузить услуги для мастера, выбранного по умолчанию
        masterSelect.dispatchEvent(new Event('change'));
    }
});
