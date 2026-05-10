import requests

#发送一个GET请求
response = requests.get("https://jsonplaceholder.typicode.com/posts")

#打印状态码
print("状态码:",response.status_code)

#打印返回的json数据（前200个字符，防止刷屏）
print("返回数据预览：",response.text[:200])
#print("返回数据预览：",response.text)#这会打印返回的所有数据

#断言：状态码应该是200
assert response.status_code == 200,f"状态码不是200，而是{response.status_code}"

#返回的数据应该是数组(isinstance 是个“类型检查员”  list类型)
json_data = response.json()    #这行先把服务器返回的 JSON 数据，转换成 Python 能直接处理的数据结构
assert isinstance(json_data, list) , "返回的不是数组"

#断言：数组不为空；len() 用来计算数组内有多少元素，确保数据确实返回了
assert len(json_data) > 0, "数组为空"

print("\n✔ 所有断言通过！")