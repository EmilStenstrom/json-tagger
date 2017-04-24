import requests
r = requests.post("http://localhost:8000/tag?pretty=1", data="Fördomen har alltid sin rot i vardagslivet - Olof Palme".encode("utf-8"))
print(r.text)
