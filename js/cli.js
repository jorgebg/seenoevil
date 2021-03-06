const URL = require('url').URL;

const server = new URL(process.env.HOST || 'http://127.0.0.1:8000');
const http = server.protocol == 'https:' ? require('https') : require('http');
const options = {
  hostname: server.hostname,
  port: server.port,
  headers: {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'application/json',
  },
};

function create(rawData, expiration=3, reads=3) {
  const vault = encrypt(rawData);
  const secret = {data: vault.data, expiration, reads};
  options.method = 'POST';
  const req = http.request(options, (res) => {
    res.on('data', (d) => {
      checkError(res, d);
      const path = JSON.parse(d).path + '#' + vault.key;
      process.stdout.write(JSON.stringify({path}));
    });
  });
  req.write(JSON.stringify(secret));
  req.end();
}

function show(url) {
  let path, hash;
  try {
    ({ pathname, hash } = new URL(url));
    hash = hash.slice(1);
  } catch(e) {
    ([ pathname, hash ] = url.split('#'));
  }
  options.path = pathname;
  const req = http.request(options, (res) => {
    res.on('data', (d) => {
      checkError(res, d);
      const secret = JSON.parse(d);
      secret.data = decrypt(hash, secret.data);
      process.stdout.write(JSON.stringify(secret));
    });
  });
  req.end();
}

function checkError(res, d) {
    if (res.statusCode !== 200) {
      process.stdout.write(d);
      process.exit(1);
    }
}

function usage() {
  process.stdout.write(
`usage: seenoevil create DATA [EXPIRATION[ READS]]
       seenoevil show URL
`);
}


const action = process.argv[2];
const args = process.argv.slice(3);
const actions = {create, show};
if (args.length == 0 || process.argv.some((el) => ['-h', '--help'].includes(el))) {
  usage();
} else {
  actions[action](...args);
}
