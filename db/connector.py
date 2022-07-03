import mysql.connector
from mysql.connector import Error

config = None

#todo: refactor db password o be retrieved via vault

def load_config():
    import yaml

    with open("/db/conf.yaml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def connect_to_kis_db():
    load_config()
    try:
        connection = mysql.connector.connect(config['dev']['host'],
                                             config['dev']['database'],
                                             config['dev']['user'],
                                             config['dev']['password'])
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)


def connect_to_kis_db_no_config_file():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='kis_reports',
                                             user='root',
                                             password='nimda')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)

def fetch_jsons(connection):
    cursor = connection.cursor()
    cursor.execute("select content_red from report_nf ")
    records = cursor.fetchall()
    return records



if __name__ == "__main__":
    con = connect_to_kis_db()
    fetch_jsons(con)
    con.close()