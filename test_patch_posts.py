import requests

# 只发送要修改的字段（只有 title，不传 body 和 userId）
patch_data = {
     "title": "我只改了标题，没动其他内容"
}

response = requests.patch(
    "https://jsonplaceholder.typicode.com/posts/1",
    json = patch_data
)

print("状态码：",response.status_code)
print("返回数据",response.json())

assert response.status_code == 200,f"状态码不是200，而是{response.status_code}"

data = response.json()
assert data["title"] == "我只改了标题，没动其他内容","标题没有被成功修改"

#断言：body没有被清空（局部修改的核心验证！）
assert "body" in data,"body 字段丢失"
assert len(data["body"]) > 0,"body被清空了，PACTH行为可能异常"

print("\n✔ 局部修改帖子成功！")