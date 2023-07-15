import mysql.connector


class MySQL:
    def __init__(self):
        self.conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="hackathon"
    )

    def execute(self, index, stmt):
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(stmt)
        result = cursor.fetchone()
        cursor.fetchall()
        cursor.close()
        self.conn.close()
        return result

