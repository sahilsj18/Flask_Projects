from db import get_db_connection

class Task:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        conn.close()
        return tasks

    @staticmethod
    def add(title):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(task_id, completed):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET completed = %s WHERE id = %s", (completed, task_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        conn.close()
