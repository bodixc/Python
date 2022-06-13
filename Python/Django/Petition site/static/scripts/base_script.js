var Url = document.getElementsByClassName("link")[0];
Url.innerHTML = document.URL;

var User = document.getElementsByClassName("user")[0];
User.href = '../../../user' + User.innerHTML.substring(1);

let signers = document.getElementsByClassName('Signers')[0];
let list = signers.textContent.split(',');
signers.innerHTML = '';
let table = signers.appendChild(document.createElement('table'));
const len = list.length - 1;
if (len >= 4){
        for (let i = 0; i < parseInt(len/4); i++){
                let tr = table.appendChild(document.createElement('tr'));
                for (let j = 0; j < 4; j++) {
                        let th = tr.appendChild(document.createElement('th'));
                        th.innerHTML = list[i+j];
                }
        }
}

if (len % 4 != 0) {
        last = len - len % 4;
        let tr = table.appendChild(document.createElement('tr'));
        for (let i = 0; i < len % 4; i++) {
                let th = tr.appendChild(document.createElement('th'));
                th.innerHTML = list[last + i];
        }
}

document.styleSheets[5].rules[19][1]['style']['width'] = len/2 + '%';
var progress_value = document.getElementsByClassName("progress-value")[0];
progress_value.innerHTML = '<p>'+ len + '/200</p>';

let tip = document.getElementsByClassName('tip')[0];

Url.onclick = function (event){
        tip.style.visibility = 'hidden';
        let range, selection;
        selection = window.getSelection();
        range = document.createRange();
        range.selectNodeContents(event.target);
        selection.removeAllRanges();
        selection.addRange(range);
        document.execCommand("copy");
        selection.removeAllRanges();
        tip.style.width = Url.getBoundingClientRect().width + 5 + 'px';
        tip.style.top = Url.getBoundingClientRect().y - 1 + 'px';
        tip.style.left = Url.getBoundingClientRect().x -1 + 'px';
        tip.style.visibility = 'visible';
        window.setTimeout(() => tip.style.visibility = 'hidden', 1000);
}

let status = document.getElementsByClassName('Status')[0];
let sign = document.getElementsByClassName('Sign')[0];

if (status.textContent != 'Збір підписів'){
        sign.style.visibility = 'hidden';
}
