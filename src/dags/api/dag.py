# from airflow.hooks.base_hook import BaseHook
from airflow.hooks.base import BaseHook
from airflow.operators.python_operator import PythonOperator

from config.dag_factory import MyDAG


def main():
    import sqlalchemy
    import psycopg2
    import requests
    import pandas as pd
    import logging

    dwh_conn = BaseHook.get_connection("dwh")

    api_conn = BaseHook.get_connection("live_score_api")
    api_key = api_conn.login
    api_secret = api_conn.password

    url = f"{api_conn.host}.json?key={api_key}&secret={api_secret}"

    headers = {
        "Accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.get(url, headers=headers)
    response.json()

    df = pd.DataFrame(response.json()['data']['match']).sort_values(by='scheduled', ascending=True)
    df.reset_index(drop=True, inplace=True)

    conn = psycopg2.connect(dbname=dwh_conn.schema, host=dwh_conn.host,
                            port=dwh_conn.port, user=dwh_conn.login, password=dwh_conn.password)
    cur = conn.cursor()
    query = '''
        SELECT schema_name
        FROM information_schema.schemata WHERE schema_name = 'sandbox'
    '''
    cur.execute(query)

    data = cur.fetchall()
    if len(data) == 0:
        logging.info('[Creating schema "sandbox"]')
        query = '''
            create schema sandbox;
            alter schema sandbox owner to airflow;
            GRANT ALL ON ALL TABLES IN SCHEMA sandbox TO group airflow;
        '''
        cur.execute(query)
        conn.commit()
    else:
        logging.info('[Using schema "sandbox"]')

    dwh_engine = sqlalchemy.create_engine(
        f"postgresql://{dwh_conn.login}:{dwh_conn.password}@{dwh_conn.host}:{dwh_conn.port}/{dwh_conn.schema}")

    df.iloc[:3].to_sql(name='temp',
                       schema='sandbox',
                       con=dwh_engine,
                       if_exists='replace',
                       index=False,
                       method='multi', dtype={"odds": sqlalchemy.types.JSON,
                                              "country": sqlalchemy.types.JSON,
                                              "federation": sqlalchemy.types.JSON,
                                              "outcomes": sqlalchemy.types.JSON}
                       )
    logging.info('[Fetch data from api and stored it in "sandbox.temp"]')
    query = '''
            CREATE TABLE IF NOT EXISTS sandbox.match_log  (like sandbox.temp including defaults);
    '''
    cur.execute(query)
    conn.commit()

    # All columns list
    query = '''
        SELECT
            column_name,
            data_type
        FROM
            information_schema.columns
        WHERE
            table_schema||'.'||table_name = 'sandbox.match_log';
    '''
    cur.execute(query)

    columns_tuple = cur.fetchall()

    query = f'''
        BEGIN TRANSACTION;
        DELETE FROM sandbox.match_log
        WHERE '_hash_func=' || coalesce(id::TEXT, '_') IN (
          SELECT '_hash_func=' || coalesce(id::TEXT, '_') FROM sandbox.temp
        );
        INSERT INTO sandbox.match_log ({','.join(i[0] for i in columns_tuple)})
            SELECT {','.join(i[0] for i in columns_tuple)}
            FROM sandbox.temp;
        END TRANSACTION;
    '''
    cur.execute(query)
    conn.commit()
    logging.info('[Done updating "sandbox.match_log" table]')
    conn.close()


with MyDAG('Vlad', dag_id='fetch_api', schedule_interval="5 * * * *") as dag:
    main = PythonOperator(task_id='builder_block',
                          python_callable=main,
                          provide_context=True, )

    main
