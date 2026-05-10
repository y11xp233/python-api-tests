import requests

response = requests.delete("https://jsonplaceholder.typicode.com/posts/1")

print("状态码:", response.status_code)
print("返回数据:", response.text)

assert response.status_code == 200, f"状态码不是 200，而是 {response.status_code}"

print("\n✔ 删除帖子成功！")