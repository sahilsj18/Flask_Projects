import mysql.connector

class Blog:
    @staticmethod
    def get_db_connection():
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql@24",
            database="blog_db"
        )

    @staticmethod
    def create_post(title, content):
        conn = Blog.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all_posts():
        conn = Blog.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        cursor.close()
        conn.close()
        return posts

    @staticmethod
    def get_post(post_id):
        conn = Blog.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
        post = cursor.fetchone()
        cursor.close()
        conn.close()
        return post

    @staticmethod
    def update_post(post_id, title, content):
        conn = Blog.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete_post(post_id):
        conn = Blog.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        conn.commit()
        cursor.close()
        conn.close()
