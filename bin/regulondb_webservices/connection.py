from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def ejecutar_query(endpoint, query):
    # Deshabilitar la verificación del certificado SSL
    transport = RequestsHTTPTransport(
        url=endpoint,
        use_json=True,
        verify=False,  # Agregar esta línea para deshabilitar la verificación del certificado SSL
    )
    
    # Crear un cliente GraphQL con el transporte configurado
    cliente = Client(transport=transport, fetch_schema_from_transport=True)
    consulta_ejemplo = gql(query)
    
    # Ejecutar la consulta y mostrar la respuesta
    try:
        respuesta_graphql = cliente.execute(consulta_ejemplo)
        return respuesta_graphql
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")