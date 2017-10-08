from suds.client import Client
from suds.cache import NoCache

url = 'http://127.0.0.1:7789/?wsdl'
print 'Fetching WSDL from \"' + url + '\" ...'
client = Client(url, cache=NoCache())
print 'Done!\n'

#print 'Using method get_opertors()'
#result = client.service.get_opertors()

#print 'Using method get_routes()'
#result = client.service.get_routes()

#print 'Using method get_timetable()'
#result = client.service.get_timetable()

print 'Using method get_routes_filtered_by_destination("Pattaya")'
result = client.service.get_routes_filtered_by_destination("Pattaya")

print '\n============ result ============\n'
print result[0]
print '\n================================\n'
