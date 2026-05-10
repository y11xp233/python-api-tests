import requests

#准备要发送的数据（字典格式，就是json的python写法）
new_post = {
    "title":"我用python创建的帖子",
    "body":"这是内容，来自自动化脚本",
    "userId":1
}

#发送POST请求，json参数会自动转化为JSON格式
response = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json = new_post          #告诉 requests 把字典转成 JSON 发给服务器

)

print("状态码：", response.status_code)

# print("打印服务器返回的数据：",response.json)  #打印服务器返回的数据： <bound method Response.json of <Response [201]>>
print("打印服务器返回的数据：",response.json()) #打印服务器返回的数据： {'title': '我用python创建的帖子', 'body': '这是内容，来自自动化脚本', 'userId': 1, 'id': 101}

#断言：POST成功应该是201 Created
assert response.status_code == 201,f"状态码不是201，而是{response.status_code}"

# 断言：返回的数据里应该有 id 字段
data = response.json()
assert 'id' in data,"返回的数据里没有id字段"

print("\n✔ 创建帖子成功！")