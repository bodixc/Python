var text = document.getElementsByTagName('textarea')[0];

text.onblur = function() {
    text.style.width = '65%';
    text.style.height = 'initial';
}

var form = document.getElementsByClassName('form')[0];
form.style.marginTop = '100px';