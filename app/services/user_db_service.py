import sqlite3
from typing import Optional

DB_PATH = 'user.db'

# 初始化数据库连接并创建用户表
# 此函数会连接到SQLite数据库，并创建一个users表（如果不存在）
# 表结构包含：
# - user_id: TEXT类型，主键，存储用户唯一标识
# - credential: INTEGER类型，非空，存储用户凭证信息
# 执行完毕后会提交事务并关闭数据库连接
# 注意：此函数在模块加载时自动执行（见文件末尾调用）
def init_db():
    # 连接到指定路径的SQLite数据库文件
    conn = sqlite3.connect(DB_PATH)
    # 创建游标对象用于执行SQL语句
    c = conn.cursor()
    # 执行SQL语句创建users表（如果不存在）
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            credential INTEGER NOT NULL
        )
    ''')
    # 提交事务，保存对数据库的修改
    conn.commit()
    # 关闭数据库连接
    conn.close()

def add_user(user_id: str, credential: int) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO users (user_id, credential) VALUES (?, ?)', (user_id, credential))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user(user_id: str) -> Optional[int]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT credential FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

init_db()