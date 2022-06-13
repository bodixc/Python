if (document.getElementsByTagName('select')[0].value == '2'){
    var search = document.getElementsByName('field')[0].value.trim();
    var titles = document.getElementsByClassName('title');
    for (let i = 0; i < titles.length; i++) {
        var oldHTML = titles[i].innerHTML;
        var newHTML = oldHTML.replaceAll(search, search.fontcolor('yellow'));
        titles[i].innerHTML = newHTML;
    }
}

else if (document.getElementsByTagName('select')[0].value == '3'){
    var search = document.getElementsByName('field')[0].value.trim();
    var text = document.getElementsByClassName('text');
    for (let i = 0; i < text.length; i++) {
        var oldHTML = text[i].innerHTML;
        var newHTML = oldHTML.replaceAll(search, '<span style="background: yellow">' + search + '</span>');
        text[i].innerHTML = newHTML;
    }
}


