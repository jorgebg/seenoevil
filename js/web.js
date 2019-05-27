var $ = Element.prototype.$ = function (selector) {
    return (this || document).querySelector(selector);
};

function setupCreate() {
  var $secret = $('form#secret');
  $secret.onsubmit = function() {
    var fd = new FormData($secret);
    var vault = encrypt(fd.get('rawData'));
    var secret = {
      data: vault.data,
      expiration: fd.get('expiration'),
      reads: fd.get('reads'),
    };

    for (var i = 0; i < $secret.elements.length; i++) {
        $secret.elements[i].disabled = true;
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/', true);
    xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhr.setRequestHeader('Accept', 'application/json');
    xhr.onload = function() {
      var url = window.location.origin + JSON.parse(this.responseText).path + '#' + vault.key;
      $secret.hidden = true;
      clipboard(url);
    };
    xhr.send(JSON.stringify(secret));
    return false;
  }
  $secret.$('[type=submit]').disabled = false;
};

function setupShow(data) {
  var key = window.location.hash.substr(1);
  clipboard(decrypt(key, data));
};

function clipboard(content) {
  var $clipboard = $('form#clipboard');
  var $submit = $clipboard.$('[type=submit]');
  var $content = $clipboard.$('[name=content]');
  $clipboard.hidden = false;
  $clipboard.onsubmit = function() {
    document.execCommand("copy");
    var previousValue = $submit.value;
    $submit.value = 'Copied!';
    $submit.disabled = true;
    setTimeout(function(){
      $submit.value = previousValue;
      $submit.disabled = false;
    }, 1000);
    return false;
  };
  $content.value = content;
  $content.focus();
  $content.select();
  $submit.disabled = false;
}
