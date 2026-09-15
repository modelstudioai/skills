# 删除 File

硬删除文件元数据与原始内容，不可恢复。已挂载到会话沙箱的内部拷贝不受影响；新会话无法再挂载该 file\_id。

## 前提

已完成 Endpoint 与鉴权配置，详见[API 总览与认证](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)。

## 接口

**DELETE** `/files/{file_id}`

## 请求示例

bash

```
curl -X DELETE "$AGENTSTUDIO_URL/files/file_xxx" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

python

```
client.files.delete("file_xxx")
```

Python SDK

```
import os
from dashscope import Files

# 删除文件
result = Files.delete(file_id='file-xxx', api_key=os.getenv('DASHSCOPE_API_KEY'))
print(result)
```

java

```
client.files().delete("file_xxx");
```

## 响应示例

```
{
  "request_id": "xxx"
}
```

### 响应字段

字段

类型

说明

`request_id`

string

本次请求的唯一标识
