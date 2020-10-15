
import base64
with open("./picture/k_/4.png","rb") as f:#转为二进制格式
    base64_data1 = base64.b64encode(f.read())#使用base64进行加密

with open("./problem/4.png","rb") as f:#转为二进制格式
    base64_data2 = base64.b64encode(f.read())#使用base64进行加密

with open("./problem/4.jpg","rb") as f:#转为二进制格式
    base64_data = base64.b64encode(f.read())#使用base64进行加密
    print(type(base64_data))
if base64_data1==base64_data2:
    print(1)