# NOTE: Requires `gem install http`
require 'http'
r = HTTP.post("http://localhost:8000/tag", :body => "Fördomen har alltid sin rot i vardagslivet - Olof Palme")
puts r.to_s
