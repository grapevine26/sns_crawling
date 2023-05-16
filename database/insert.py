from database.database_connect import DatabaseConnection


class Insert(DatabaseConnection):
    ############################################################################################################
    # INSERT
    ############################################################################################################
    def post_insert(self, user_pk, name, post, sns, date):
        try:
            query = """INSERT INTO overdue_data (
                             user_pk, name, post, sns, date
                             ) VALUES(
                             %s, %s, %s, %s, %s)
                            """

            self.cursor.execute(query, (user_pk, name, post, sns, date))
            self.connection.commit()

        except Exception as e:
            print(sns, 'Database - post_insert Error :', e)
