import sqlite3
import os

# 鎖定 instance/database.db 的路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')
DATABASE_PATH = os.path.join(INSTANCE_DIR, 'database.db')

def get_db_connection():
    # 確保 instance 資料夾存在，避免 sqlite3 初始化時報錯
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class Task:
    @staticmethod
    def create(title, priority='低'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, priority, is_completed) VALUES (?, ?, 0)',
            (title, priority)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        tasks = conn.execute('SELECT * FROM tasks ORDER BY created_at DESC').fetchall()
        conn.close()
        return tasks

    @staticmethod
    def get_by_id(task_id):
        conn = get_db_connection()
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        return task

    @staticmethod
    def update(task_id, title, priority, is_completed):
        conn = get_db_connection()
        conn.execute(
            'UPDATE tasks SET title = ?, priority = ?, is_completed = ? WHERE id = ?',
            (title, priority, is_completed, task_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def toggle_status(task_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        task = cursor.execute('SELECT is_completed FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if task:
            new_status = 1 if task['is_completed'] == 0 else 0
            cursor.execute('UPDATE tasks SET is_completed = ? WHERE id = ?', (new_status, task_id))
            conn.commit()
        conn.close()

    @staticmethod
    def delete(task_id):
        conn = get_db_connection()
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
