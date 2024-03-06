from regulondb_webservices import connection

class RegulonDB_webservices:
    def __init__(self):
        pass
    
    def execute_query(self, url, query):
        connection.ejecutar_query(url, query)