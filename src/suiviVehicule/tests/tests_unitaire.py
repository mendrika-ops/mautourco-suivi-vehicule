import pytest
import mysql.connector

def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5  # Test réussi
    assert add(1, 1) == 2  # Test réussi


@pytest.fixture
def mysql_connection():
    config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'mautourcosuivivehicule'
    }
    connection = mysql.connector.connect(**config)
    yield connection
    connection.close()

def test_mysql_query(mysql_connection):
    cursor = mysql_connection.cursor()
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()
    assert db_name[0] == "test_db"
