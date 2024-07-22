const themeBtn = document.querySelector("#theme");

themeBtn.addEventListener('change', setTheme);

(function () {
    let dark = JSON.parse(localStorage.getItem("dark"));
    if (dark == null) {
        dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        saveTheme(dark)
    }
    if (dark) {
        document.querySelector('html').setAttribute("data-bs-theme", "dark");
        themeBtn.checked = false;
    }
})();

function setTheme(e) {
    let dark;
    if (e.target.checked) {
        document.querySelector('html').removeAttribute("data-bs-theme");
        dark = false;
    } else {
        document.querySelector('html').setAttribute("data-bs-theme", "dark");
        dark = true;
    }
    saveTheme(dark);
}

function saveTheme(dark) {
    localStorage.setItem('dark', JSON.stringify(dark));
}