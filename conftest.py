'''
conftest.py 是 fixture 的仓库，专门存放用 @pytest.fixture 定义的函数。
它的作用是在测试运行前准备好环境、数据或连接，供测试函数通过参数名来“领取”。

'''



import pytest
import requests
import sqlite3

@pytest.fixture(scope="session")
def base_url():
    """所有接口的基础 URL"""
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def fist_posts_id(base_url):
    """获取第一条帖子的ID，供关联接口使用"""
    response = requests.get(f"{base_url}/posts")
    data = response.json()
    return data[0]["id"]



'''
@pytest.fixture(scope="function")
def db_cursor():
    """每个测试函数获取一个独立的数据库游标，测试结束后自动回滚，保持数据干净"""
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()


     # 开启事务
     # 事务 = 一组打包操作的"后悔药"。在事务开启后，所有数据库操作（INSERT、DELETE 等）都不会立刻生效，
     # 而是在你确认无误后 COMMIT（提交），或者发现有问题后 ROLLBACK（回滚，撤销所有操作）。
    conn.execute("BEGIN")    #--手动开启一个事务

     #暂停 fixture 的执行，把 cursor 这个变量交给测试函数使用。等测试函数执行完了，再回到这里继续往下走。
     #在 pytest fixture 里，yield的作用就是：把 fixture 拆成“准备阶段”和“清理阶段”。
    yield cursor

     # 测试结束后回滚，撤销本次测试的所有数据库操作
    conn.rollback()
    conn.close()
'''

@pytest.fixture(scope="session")
def db_connection():
    """整个测试会话只创建一次数据库连接（节省资源）"""
    conn = sqlite3.connect("test.db")
    yield conn
    conn.close()

@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """每个测试函数获得独立的游标，并在测试结束后回滚"""
    cursor = db_connection.cursor()
    db_connection.execute("BEGIN")
    yield cursor
    db_connection.rollback()