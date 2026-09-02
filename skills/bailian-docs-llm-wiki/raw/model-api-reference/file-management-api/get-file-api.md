# 查询和管理文件

查询、列举和删除文件，并了解文件对象的属性信息。

## 获取指定文件信息

```
GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}
Accept: application/json
```

### 请求示例

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/files/123" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 请求参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

file\_id

String

path

是

文件ID，可通过[上传文件](raw/model-api-reference/file-management-api/upload-file-api.md)或列举文件接口获取

### 返回示例

```
{
    "request_id": "bddee90e-d320-4bf9-b32b-ac3359192d1e",
    "data": {
        "file_id": "mbSwIGR9yA6i1EtwIpndFErIoDKFyQ6W5601487ECAB111EDA20422ECF4959B5E",
        "name": "dogs.jpg",
        "description": "1",
        "size": 129862,
        "md5": "1d5ee55c2453009b14db98e74c453abb",
        "gmt_create": "2023-03-25 10:04:11",
        "url": "http://xxxxx.oss-cn-hangzhou.aliyuncs.com/oss%3A//dashscope-pre/api-fs/1253/236/dogs.jpg?Expires=1679797621&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE"
    }
}
```

### 返回参数

**字段**

**类型**

**描述**

data.file\_id

String

文件ID

data.url

String

文件下载链接

data.name

String

文件名

data.size

Number

文件大小

data.md5

String

文件的md5

data.description

String

文件的描述

data.gmt\_create

Date

文件上传时间

data.id

String

文件的内部ID

data.region

String

文件所在地域

data.user\_id

String

用户ID

data.api\_key\_id

String

API Key ID

request\_id

String

本次请求的系统唯一码

## 列举当前所有的文件

```
GET https://dashscope.aliyuncs.com/api/v1/files
Accept: application/json
```

### 请求示例

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 请求参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

page\_no

Number

Query

是

当前页，最小值为1，默认值为1

page\_size

Number

Query

是

分页大小。最小值为1，最大值为100，默认值为10

### 返回示例

```
{
    "request_id": "123456",
    "data": {
        "total": 2,
        "page_size": 20,
        "page_no": 1,
        "files": [
            {
                "id": 1001,
                "file_id": "9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733",
                "name": "test.txt",
                "description": "1",
                "size": 0,
                "md5": "d41d8cd98f00b204e9800998ecf8427e",
                "gmt_create": "2023-03-25 10:13:07",
                "url": "http://xxx.oss-cn-hangzhou.aliyuncs.com/oss%3A//dashscope-dev/api-fs/123456/123456/test.txt",
                "region": "cn-hangzhou",
                "user_id": "123456",
                "api_key_id": "sk-xxxx",
                "purpose": "fine-tune"
            },
            {
                "id": 1002,
                "file_id": "wmIDj6zemqjIb8L2o8NHIlMRk3QinjGP00E987C7CA3711ED83E0000EC63B0D1C",
                "name": "sdsdsd.mp4",
                "description": "1",
                "size": 780635,
                "md5": "8382b3d3137bce6eaf1beef9c8920ef6",
                "gmt_create": "2023-03-24 19:28:30",
                "url": "http://xxxx.oss-cn-hangzhou.aliyuncs.com/oss%3A//dashscope-dev/api-fs/123456/123456/sdsdsd.mp4",
                "region": "cn-hangzhou",
                "user_id": "123456",
                "api_key_id": "sk-xxxx",
                "purpose": "file-extract"
            }
        ]
    }
}
```

### 返回参数

**字段**

**类型**

**描述**

data.total

Number

总记录数

data.page\_size

Number

分页大小

data.page\_no

Number

当前页

data.files

Array

文件列表，元素为文件对象，属性详见文件对象小节

request\_id

String

本次请求的系统唯一码

## 删除文件

```
DELETE https://dashscope.aliyuncs.com/api/v1/files/{file_id}
Accept: application/json
```

### 请求示例

```
curl --location --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/123" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### 请求参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

file\_id

String

path

是

文件ID，可通过[上传文件](raw/model-api-reference/file-management-api/upload-file-api.md)或列举文件接口获取

### 返回示例

```
{
    "request_id": "038e9953-6f0e-4691-afcc-1f0fe07b32c2"
}
```

### 返回参数

**字段**

**类型**

**描述**

code

String

错误码，仅当本次请求出错时返回

message

String

错误信息，仅当本次请求出错时返回

request\_id

String

本次请求的系统唯一码

## 文件对象

文件对象表示已上传到百炼平台的文件及其属性信息。通过[上传文件](raw/model-api-reference/file-management-api/upload-file-api.md)接口创建，可通过列举文件和查询文件详情接口获取。

除 DashScope 原生接口外，您也可以通过 [OpenAI 兼容-File 接口](https://help.aliyun.com/zh/model-studio/openai-file-interface)（`/compatible-mode/v1/files`）管理文件。

> 当前文件管理 API 仅在北京 Region 开放。如您使用其他 Region，请通过该 Region 的百炼控制台完成文件管理操作。

**字段**

**类型**

**描述**

file\_id

String

文件ID

name

String

文件名

description

String

文件的描述

size

Number

文件大小

md5

String

文件的md5

url

String

文件下载链接

gmt\_create

Date

文件上传时间

id

String

文件的内部ID

region

String

文件所在地域

user\_id

String

用户ID

api\_key\_id

String

API Key ID

purpose

String

文件用途
