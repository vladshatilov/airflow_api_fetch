import yaml
from airflow import settings
from airflow.models import Connection

session = settings.Session()  # get the session

with open(r'connections_filled.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    connections = yaml.load(file, Loader=yaml.FullLoader)

for conn_id, conn_values in connections.items():
    print(f'Adding {conn_id}')

    if 'password' in conn_values:
        conn_values['password'] = str(conn_values['password'])

    if 'extra' in conn_values:
        conn_values['extra'] = str(conn_values['extra'])

    session.query(Connection).filter(Connection.conn_id == conn_id).delete()

    conn = Connection(conn_id=conn_id, **conn_values)

    session.add(conn)

session.commit()
session.close()

print('Connections committed')
