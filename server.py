import soaplib

from soaplib.core.service import soap
from soaplib.core.service import DefinitionBase
from soaplib.core.model.primitive import String, Integer

from soaplib.core.server import wsgi
from soaplib.core.model.clazz import Array

import mysql.connector
conn = mysql.connector.connect( user='test_admin',
                                password='1234',
                                host='192.168.1.2',
                                port='3306',
                                database='van_operator')

cursor = conn.cursor()
cursor.execute("select name, tel, location from operator")
operator = cursor.fetchall()

cursor.execute("select source,destination,name,tel,convert(price using utf8) as price,convert(distance using utf8) as distance from operator,opro,route where operator.id = op_id and ro_id = route.id order by source,destination")
route = cursor.fetchall()

cursor.execute("select convert(time using utf8) as time,source,destination,name,convert(distance using utf8) as distance from operator,opro,route,opro_time,time where operator.id = op_id and ro_id = route.id and opro_id = opro.id and t_id = time.id order by time,source,destination,name")
timetable = cursor.fetchall()

class Service(DefinitionBase):
    @soap(_returns=Array(Array(String)))
    def get_opertors(self):
        global operator
        return operator
    
    @soap(_returns=Array(Array(String)))
    def get_routes(self):
        global route
        return route
    
    @soap(_returns=Array(Array(String)))
    def get_timetable(self):
        global timetable
        return timetable
    
    @soap(String,_returns=Array(Array(String)))
    def get_routes_filtered_by_destination(self,destination):
        query = "select source,destination,name,tel,convert(price using utf8) as price,convert(distance using utf8) as distance from operator,opro,route where operator.id = op_id and ro_id = route.id and"
        query += " destination = '" + destination + "'"
        query += " order by source,destination"
        cursor.execute(query)
        route = cursor.fetchall()
        return route

if __name__=='__main__':
    try:
        from wsgiref.simple_server import make_server
        soap_application = soaplib.core.Application([Service], 'tns')
        wsgi_application = wsgi.Application(soap_application)
        print "wsdl is at: http://127.0.0.1:7789/?wsdl"
        server = make_server('localhost', 7789, wsgi_application)
        server.serve_forever()

    except ImportError:
		print "ImportError"
