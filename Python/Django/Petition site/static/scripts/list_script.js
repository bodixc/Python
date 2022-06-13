let ps = document.getElementsByTagName('p');
for (var i = 0; i < ps.length; i++){
    if (ps[i].innerText.length > 200){
        ps[i].innerText = ps[i].innerText.substring(0, 200) + '...';
    }
}
