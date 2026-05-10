import pytest
import allure


@allure.feature("数据库验证")
@allure.story("查询初始数据")
def test_initial_posts_count(db_cursor):
    """验证初始数据至少有 2 条"""
    with allure.step("查询 posts 表总记录数"):
        db_cursor.execute("SELECT COUNT(*) FROM posts")
        count = db_cursor.fetchone()[0]

    with allure.step("断言记录数 >= 2"):
        assert count >= 2, f"数据库里只有 {count} 条记录，预期至少 2 条"


@allure.feature("数据库验证")
@allure.story("插入一条新记录并验证")
def test_insert_and_verify(db_cursor):
    """模拟创建操作：插入一条新记录，然后用 SQL 验证它是否真的存在"""
    title = "SQL验证测试标题"
    body = "SQL验证测试内容"
    user_id = 1

    with allure.step("插入一条新帖子"):
        db_cursor.execute(
            "INSERT INTO posts (title, body, userId) VALUES (?, ?, ?)",
            (title, body, user_id)
        )

    with allure.step("查询刚插入的帖子"):
        db_cursor.execute(
            "SELECT id, title, body, userId FROM posts WHERE title = ?",
            (title,)
        )
        row = db_cursor.fetchone()

    with allure.step("断言查询结果不为空"):
        assert row is not None, "插入后无法查到该帖子"

    with allure.step("断言各字段值正确"):
        assert row[1] == title
        assert row[2] == body
        assert row[3] == user_id


@allure.feature("数据库验证")
@allure.story("删除一条记录并验证")
def test_delete_and_verify(db_cursor):
    """模拟删除操作：删除一条记录，然后用 SQL 验证它是否真的消失"""
    # 先插入一条临时数据
    db_cursor.execute(
        "INSERT INTO posts (title, body, userId) VALUES (?, ?, ?)",
        ("待删除的文章", "删除测试", 1)
    )
    # 获取刚插入的 id
    post_id = db_cursor.lastrowid

    with allure.step("执行删除"):
        db_cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))

    with allure.step("查询被删除的帖子"):
        db_cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        row = db_cursor.fetchone()

    with allure.step("断言记录不存在"):
        assert row is None, f"帖子 id={post_id} 应该已被删除，但数据库里还能查到"