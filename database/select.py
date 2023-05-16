from database.database_connect import DatabaseConnection


class Select(DatabaseConnection):
    ############################################################################################################
    # INSERT
    ############################################################################################################
    def repayment_user_select(self):
        try:
            query = """select * from repayment_user WHERE cpl = 0"""

            self.cursor.execute(query)
            self.connection.commit()

            return self.cursor.fetchall()
        except Exception as e:
            print('Database - select Error :', e)
    def overdue_user_select(self):
        try:
            query = """select * from overdue_user WHERE cpl = 0"""

            self.cursor.execute(query)
            self.connection.commit()

            return self.cursor.fetchall()
        except Exception as e:
            print('Database - select Error :', e)