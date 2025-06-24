import psycopg2

class DB:
    def __init__(self, config: dict):
        self.connection = psycopg2.connect(
            user = config.get('user'),
            password = config.get('password'),
            database = config.get('dbname', 'postgres'),
            host = config.get('host','localhost'),
            port = config.get('port','3333'),
    )
        
    def get_connection(self):
        return self.connection
    
    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    
    def execute_non_query(self, query, values):
        cursor = self.connection.cursor()
        cursor.execute(query, values)
        self.connection.commit()
        cursor.close()

    def fetch_one(self, query: str, values: tuple):
        """Use for SELECT queries expected to return a single row."""
        with self.connection.cursor() as cursor:
            cursor.execute(query, values)
            return cursor.fetchone()

    
    def close_connection(self):
        if self.connection:
            self.connection.close()
    