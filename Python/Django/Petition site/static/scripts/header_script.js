let div = document.getElementsByTagName('div')[1];
let category = document.getElementsByTagName('span')[2];

var vis = false;

category.onclick = function() {
    if (!vis){
        div.style.visibility = 'visible';
        vis = true;
        div.style.left = category.getBoundingClientRect().x + 2.5 + 'px';
        div.style.top = category.getBoundingClientRect().y + category.getBoundingClientRect().height + 'px';
        div.style.width = category.getBoundingClientRect().width - 4.5 + 'px';
    }
    else {
        div.style.visibility = 'hidden';
        vis = false;
    }
}

div.onmouseleave = function(){
    div.style.visibility = 'hidden';
    vis = false;
}
