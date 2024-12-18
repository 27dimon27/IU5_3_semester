let param = document.querySelector('.max-par');
let sum_of_px = 0;

let cards = document.querySelectorAll('.card');
for (let i = 0; i < cards.length; ++i) {
    if (sum_of_px + cards[i].clientWidth >= param.clientWidth) {
        cards[i - 1].classList.add('.last-card-in-row');
        sum_of_px = cards[i].clientWidth;
    }

    cards[i].addEventListener('click', function() {
        let reg_form = document.getElementById('reg-form');
        reg_form.scrollIntoView({ behavior: 'smooth' });
    });
}

let element = document.querySelector('.header');
let back = document.querySelector('.background');
let tg = document.querySelector('.tg');
let ins = document.querySelector('.insta');

document.addEventListener('DOMContentLoaded', function() {

    function detectDeviceType() {
        let userAgent = navigator.userAgent || navigator.vendor || window.opera;
        let deviceType;
        let tg = document.querySelector('.tg');
        let insta = document.querySelector('.insta');

        // Проверка на мобильные устройства
        if (/windows phone/i.test(userAgent)) {
            deviceType = "Смартфон (Windows Phone)";
            // tg.classList.add('tg-phone-landscape');
            // insta.classList.add('insta-phone-landscape');
        } else if (/android/i.test(userAgent)) {
            deviceType = "Смартфон (Android)";
            
        } else if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
            deviceType = "Устройство Apple (iOS)";
            
        } else if (/Macintosh/.test(userAgent) && 'ontouchend' in document) {
            deviceType = "iPadOS устройство";
            
        } else {
            deviceType = "Настольный ПК или другое устройство";
        }

        // Добавить слушатель события изменения ориентации
        window.addEventListener("resize", function() {
            applyStyles(deviceType);
        });

        // Отображение типа устройства на странице
        //alert("Тип устройства: " + deviceType);
        applyStyles(deviceType);
    }
    function getOrientation() {
        return window.matchMedia("(orientation: portrait)").matches ? "portrait" : "landscape";
    }
    function applyStyles(deviceType) {
        let orientation = getOrientation();
        let tg = document.querySelector('.tg');
        let insta = document.querySelector('.insta');

        if (deviceType === "Смартфон (Windows Phone)" || deviceType === "Смартфон (Android)" || deviceType === "Устройство Apple (iOS)" || deviceType === "iPadOS устройство") {
            if (orientation === "landscape") {
                // tg.classList.remove('tg');
                // insta.classList.remove('insta');
                tg.classList.add('tg-phone-landscape');
                insta.classList.add('insta-phone-landscape');
            } else {
                if (tg.classList.contains('tg-phone-landscape')) { tg.classList.remove('tg-phone-landscape'); }
                if (insta.classList.contains('insta-phone-landscape')) { insta.classList.remove('insta-phone-landscape'); }
            }
        }

        //alert("Ориентация: " + orientation);
    }
    detectDeviceType();


    // let element = document.querySelector('.header');
    // let back = document.querySelector('.background');
    // let tg = document.querySelector('.tg');
    // let ins = document.querySelector('.insta');

    element.classList.add('visible');
    back.classList.add('visible');
    tg.classList.add('visible');
    ins.classList.add('visible');

});

let all_menu = [
    document.querySelector('.first'),
    document.querySelector('.second'),
    document.querySelector('.third'),
    document.querySelector('.fourth')
];
let menu_button = document.querySelector('.menu');
menu_button.addEventListener('click', function () {
    document.querySelector('.menu-drop').classList.toggle('visible');
    for (let i = 0; i < all_menu.length; ++i) {
        all_menu[i].classList.toggle('move');
    }
});

let send_button = document.querySelector('.form-button');
let form_text = document.getElementById('form-text');

let fill_text = [document.getElementById('name'), document.getElementById('phone'), document.getElementById('email')];

let drop = document.querySelector('.dropdown-select');
let checkboxes = document.querySelectorAll('#dropdownList input[type="checkbox"]');
let selected = Array.from(checkboxes).some(checkbox => checkbox.checked);

let dropdownList = document.getElementById('dropdownList');
let checkboxes_p = dropdownList.querySelectorAll('p');
for (let i = 0; i < checkboxes_p.length; ++i) {
    checkboxes[i].addEventListener('click', function() {
        checkboxes[i].checked = !checkboxes[i].checked;
    });
    checkboxes_p[i].addEventListener('click', function() {
        checkboxes[i].checked = !checkboxes[i].checked;
    });
}

send_button.addEventListener('click', function () {
    selected = Array.from(checkboxes).some(checkbox => checkbox.checked);
    if (form_text.style.display == '') {
        if (fill_text[0].value !== '' && fill_text[1].value !== '' && fill_text[2].value !== '' && selected) {
            for (let i = 0; i < fill_text.length; ++i) {
                fill_text[i].classList.remove('error-form-field');
            }
            drop.classList.remove('error-dropdown-select');
            form_text.style.display = 'block';
            drop.textContent = 'Выберите предмет обращения...';
            drop.classList.remove('black-color-text');
        } else {
            for (let i = 0; i < fill_text.length; ++i) {
                if (fill_text[i].value === '') { fill_text[i].classList.add('error-form-field'); }
                else { fill_text[i].classList.remove('error-form-field'); }
            }
            if (!selected) { drop.classList.add('error-dropdown-select'); }
            else { drop.classList.remove('error-dropdown-select'); }
        }
    }
});

document.getElementById('dropdownSelect').addEventListener('click', function() {
    dropdownList.classList.toggle('hidden');
    send_button.ariaDisabled = true;
});

let f = false;
document.addEventListener('click', function(event) {

    let isClickInside = document.getElementById('dropdownSelect').contains(event.target);

    let count = 0;
    for (let i = 0; i < checkboxes.length; ++i) {
        if (checkboxes[i].checked == true) {
            if (count === 0) { drop.textContent = ''; }
            drop.textContent += checkboxes[i].value;
            drop.textContent += ', ';
            drop.value = drop.textContent;
            ++count;
        }
    }
    drop.textContent = drop.textContent.slice(0, -2);
    drop.classList.add('black-color-text');
    if (count === 0) { drop.textContent = 'Выберите предмет обращения...'; drop.classList.remove('black-color-text'); }

    if (!isClickInside && !dropdownList.contains(event.target)) {
        dropdownList.classList.add('hidden');
        //send_button.classList.remove('hidden');
        send_button.ariaDisabled = true;
        //dropdownList.style.display = 'none';
    }

    let menu_drop = document.querySelector('.menu-drop');
    if (!menu_drop.contains(event.target) && f) {
        f = false;
        if (menu_drop.classList.contains('visible')) {
            menu_drop.classList.remove('visible');
            for (let i = 0; i < all_menu.length; ++i) {
                all_menu[i].classList.remove('move');
            }
        }
    } else if (menu_drop.classList.contains('visible')) {
        f = true;
    }

});

//let body = document.querySelector('.max-par');
let inactive_overlay = document.querySelector('.inactive-overlay')
let bl_back = document.querySelector('.background');
let reg_log_button = document.querySelector('.reg-log');
reg_log_button.addEventListener('click', function () {
    inactive_overlay.style.display = "block";
    // body.classList.add('blurred-back');
    // bl_back.classList.add('blurred-back');
    // tg.classList.add('blurred-back');
    document.body.classList.add('blurred-back');
});

inactive_overlay.addEventListener('click', function () {
    inactive_overlay.style.display = "none";
    document.body.classList.remove('blurred-back');
});