import requests
r = requests.post("http://localhost:8000/tag", data={
	"data": "Fördomen har alltid sin rot i vardagslivet - Olof Palme".encode("utf-8"),
	"pretty": 1,
})
print(r.text)
