document.addEventListener("DOMContentLoaded", function () {
  const masterSelect = document.querySelector("#id_master");
  const servicesSelect = document.querySelector("#id_services");

  // Функция для получения CSRF токена из cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");

  if (masterSelect && servicesSelect) {
    const updateServices = () => {
      const masterId = masterSelect.value;
      if (masterId) {
        fetch("/ajax/get-master-services/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({ master_id: masterId }),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Данные о мастере:", data);
            servicesSelect.innerHTML = ""; // Очищаем список услуг
            if (data.services) {
              console.log("Полученные услуги:", data.services);
              data.services.forEach((service) => {
                const option = document.createElement("option");
                option.value = service.id;
                option.textContent = service.name;
                servicesSelect.appendChild(option);
              });
            }
          })
          .catch((error) => console.error("Ошибка при загрузке услуг:", error));
      } else {
        servicesSelect.innerHTML = ""; // Очищаем, если мастер не выбран
      }
    };

    masterSelect.addEventListener("change", updateServices);
    // Вызываем функцию при загрузке страницы
    updateServices();
  }

  const toastElList = document.querySelectorAll(".toast");
  const toastList = [...toastElList].map((toastEl) => {
    const toast = new bootstrap.Toast(toastEl, {
      delay: 5000, // 5 секунд
    });
    toast.show();
    return toast;
  });
});
