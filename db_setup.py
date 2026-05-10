import sqlite3


# 连接数据库（如果 test.db 不存在会自动创建）
conn = sqlite3.connect("test.db")
#cursor专门用来执行 SQL 语句、获取结果
cursor = conn.cursor()                 #conn = 建立连接，cursor = 用这条连接来干活

# 通过 cursor.execute() 来执行:创建 posts 表
cursor.execute(
    """CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT,
    userId INTEGER)"""
)

# 插入几条初始数据（模拟已有数据）
initial_posts = [
    ("第一篇文章", "这是第一篇文章的内容", 1),
    ("第二篇文章", "这是第二篇文章的内容", 2),
]

#executemany批量执行同一条 SQL，每行数据都用 ? 占位符替换
cursor.executemany(
    "INSERT INTO posts (title, body, userId) VALUES (?, ?, ?)",
    initial_posts
)

conn.commit()
conn.close()

print("数据库初始化完成：posts 表已创建，初始数据已插入。")

