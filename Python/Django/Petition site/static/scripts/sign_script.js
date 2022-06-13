let h = document.getElementsByTagName('h2')[0];
let form = document.getElementsByTagName('form')[0];

if (h.innerText.includes('Ви вже')){
    form.style.visibility = 'hidden';
}