var request = require('request');
request.post({url: 'http://localhost:8000/tag', body: "Fördomen har alltid sin rot i vardagslivet - Olof Palme"}, function (error, response, body) {
    console.log(body)
})
