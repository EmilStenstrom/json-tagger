# -*- coding: utf-8 -*-
import requests
r = requests.post("http://localhost:8000/tag", data="Fördomen har alltid sin rot i vardagslivet - Olof Palme")
print r.text
