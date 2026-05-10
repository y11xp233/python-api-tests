import requests
import allure
import pytest


post_test_data = [
    ("正常中文标题","正常中文内容",1),
    ("English Title","English Body content",2),
    ("标题带特殊字符","!@#$%",3),
    ("   前后带空格的标题   ","   前后带空格的内容   ",4),
]

@allure.feature("查询帖子")
@allure.story("获取所有帖子")
def test_get_all_posts_status_code(base_url):
    with allure.step("发送GTE请求到 /posts"):
        """测试获取所有帖子 - 状态码应为200"""
        response = requests.get(f"{base_url}/posts")

    with allure.step("校验状态码为 200"):
        assert response.status_code == 200, f"状态码不是200，而是{response.status_code}"

    with allure.step("校验响应体是数组且不为空"):
        data = response.json()
        assert isinstance(data, list), "返回的不是数组"
        assert len(data) > 0, "数组为空"



'''
@pytest.mark.parametrize 是 测试执行的控制装置。
它告诉 pytest:“这一个测试函数，请用这些不同的数据反复调用多次”。它必须直接装饰在测试函数上面，不能脱离测试函数单独存在。
'''

@allure.feature("创建帖子")
@allure.story("POST 创建新帖子 - 参数")
@pytest.mark.parametrize("title,body_test,user_id",post_test_data)
def test_create_post(base_url,title,body_test,user_id):
    new_post = {
        "title": title,
        "body": body_test,
        "userId": user_id,
    }

    with allure.step(f"发送 POST 请求创建帖子:{title}"):
        response = requests.post(f"{base_url}/posts", json=new_post)

    with allure.step("校验状态码为 201"):
        assert response.status_code == 201, f"状态码不是201，而是{response.status_code}"

    with allure.step("校验返回数据包含 id 且 title 一致"):
        data = response.json()
        assert "id" in data, "返回数据里没有 id 字段"
        assert data["title"] == title, "返回的 title 与发送的不一致"


@allure.feature("修改帖子")
@allure.story("PUT 全量修改")
def test_update_post(base_url):
    update_post = {
        "id": 1,
        "title": "pytest全量修改/更新",
        "body": "修改/更新后的内容",
        "userId": 2,
    }

    with allure.step("发送 PUT 请求全量修改 id=1 的帖子"):
        response = requests.put(f"{base_url}/posts/1", json=update_post)

    with allure.step("校验状态码为 200"):
        assert (
            response.status_code == 200
        ), f"状态码不是 200，而是 {response.status_code}"

    with allure.step("校验 title 已修改/更新"):
        date = response.json()
        assert (
            date["title"] == "pytest全量修改/更新"
        )  # assert response.json()["title"] == "pytest全量修改/更新"


@allure.feature("修改帖子")
@allure.story("PATCH 局部修改")
def test_patch_post(base_url):
    patch_post = {
        "title": "pytest局部修改",
    }

    with allure.step("发送 PATCH 请求局部修改标题"):
        response = requests.patch(f"{base_url}/posts/1", json=patch_post)

    with allure.step("校验状态码为 200"):
        assert (
            response.status_code == 200
        ), f"状态码不是 200，而是 {response.status_code}"

    with allure.step("校验 title 已更新"):
        assert response.json()["title"] == "pytest局部修改"

    with allure.step("校验 body 未被清空（局部修改核心）"):
        data = response.json()
        assert "body" in data, "body 字段丢失了！"
        assert len(data["body"]) > 0, "body 被清空了"


@allure.feature("删除帖子")
@allure.story("DELETE 删除")
def test_delete_post(base_url):
    with allure.step("发送 DELETE 请求删除 id=1 的帖子"):
        response = requests.delete(f"{base_url}/posts/1")

    with allure.step("校验状态码为 200"):
        assert (
            response.status_code == 200
        ), f"状态码不是 200，而是 {response.status_code}"


@allure.feature("查询评论")
@allure.story("参数关联 - 获取第一条帖子的评论")
def test_get_comments_fist_post(base_url, fist_posts_id):
    with allure.step(f"用提取到的帖子 ID={fist_posts_id} 查询评论"):
        response = requests.get(f"{base_url}/post/{fist_posts_id}/comments")

    with allure.step("校验状态码为 200"):
        assert response.status_code == 200, f"状态码不是 200，而 {response.status_code}"

    with allure.step("校验评论数不为空"):
        comments = response.json()
        assert len(comments) > 0, "错误：评论数不能为空"
