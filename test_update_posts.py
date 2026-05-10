import requests

#新的完整的数据（用来替换id=1的帖子）
update_post = {
    "id" : 1,
    "title" : "被python修改后的标题",
    "body" : "被修改后的内容",
    "userid" : 2
}


response = requests.put(
    "https://jsonplaceholder.typicode.com/posts/1",
    json = update_post
)

print("状态码：",response.status_code)
print("返回数据：",response.json())

assert response.status_code == 200,f"状态码不是200，而是{response.status_code}"

data = response.json()
assert data["title"] == "被python修改后的标题","标题没有被成功修改"

print("\n✔ 全量修改帖子成功！")


