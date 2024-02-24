const theme = localStorage.getItem('theme');
const isSolar = localStorage.getItem('isSolar');

if (theme) {
    body.classList.add(theme);
    isSolar && body.classList.add('solar')
}
const body = document.body

const lightButton = document.getElementById('button-light');
const darkButton  = document.getElementById('button-dark');
const solarButton = document.getElementById('button-solar');


lightButton.onclick = () => {
    body.classList.replace('dark', 'light');
    localStorage.setItem('theme', 'light');
}

darkButton.onclick = () => {
    body.classList.replace('light', 'dark');
    localStorage.setItem('theme', 'dark');
}

solarButton.onclick = () => {
    if (body.classList.contains('solar'))
    {
        body.classList.remove('solar');
        solarButton.innerText = 'Solarize';
        localStorage.removeItem('isSolar');
    } else {
        body.classList.add('solar');
        solarButton.innerText = 'Solarized';
        localStorage.setItem('isSolar', true);
    }
}