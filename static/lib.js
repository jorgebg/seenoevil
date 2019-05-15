var sjcl = ("undefined" == typeof sjcl) ? require('./sjcl.js') : sjcl;

function encrypt(data) {
    var key = sjcl.random.randomWords(8, 10); //8x4 bytes 256 bit key, level 10 paranoia
    data = sjcl.encrypt(key, data, {ts: 128, ks: 256});
    return {
        "key": sjcl.codec.base64url.fromBits(key),
        "data": data
    };
}

function decrypt(key, data) {
    key = sjcl.codec.base64url.toBits(key);
    var decrypted = sjcl.decrypt(key, data, {ts: 128, ks: 256});
    return decrypted;
}

if ("undefined" !== typeof module) {
    module.exports = { encrypt, decrypt };
}
