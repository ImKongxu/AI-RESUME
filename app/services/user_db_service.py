
import sqlite3
from typing import Optional

# 数据库文件路径
DB_PATH = 'user.db'

def init_db():
    """
    初始化数据库，创建用户表（如不存在）。
    表结构：
        user_id: 用户自定义ID（主键，字符串）
        credential: int类型的用户凭证
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            credential INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id: str, credential: int) -> bool:
    """
    新增用户数据。
    参数：
        user_id (str): 用户自定义ID
        credential (int): 用户凭证
    返回：
        bool: 添加成功返回True，若user_id已存在返回False
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO users (user_id, credential) VALUES (?, ?)', (user_id, credential))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # user_id已存在
        return False

def get_user(user_id: str) -> Optional[int]:
    """
    根据用户ID查询凭证。
    参数：
        user_id (str): 用户自定义ID
    返回：
        int或None: 若存在返回凭证int，否则返回None
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT credential FROM users WHERE user_id = ?', (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

# 模块加载时自动初始化数据库
init_db()