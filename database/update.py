from database.database_connect import DatabaseConnection


class Update(DatabaseConnection):
    ############################################################################################################
    # INSERT
    ############################################################################################################
    def user_update(self, cpl, user_pk):
        try:
            query = """UPDATE overdue_user SET cpl = %s WHERE user_pk = %s"""

            self.cursor.execute(query, (cpl, user_pk))
            self.connection.commit()

        except Exception as e:
            print('Database - update Error :', e)
            raise
