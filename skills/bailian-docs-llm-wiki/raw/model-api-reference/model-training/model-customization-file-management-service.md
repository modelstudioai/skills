# 百炼文件管理 API

通过模型定制文件管理服务，您可以对您的文件进行统一管理，只需要一次上传即可多次复用在多个任务中。

## **使用限制**

当您使用本服务时，会有如下限制存在

-   单个文件大小最大为1GB。
    
-   有效文件（未删除）总使用空间配额为5GB。
    
-   有效文件（未删除）总数量配额为100个。
    

OpenAI 兼容方式调用请参考：[OpenAI兼容-File](https://help.aliyun.com/zh/model-studio/openai-file-interface)。

## **上传文件**

```
POST https://dashscope.aliyuncs.com/api/v1/files
Content-type: multipart/form-data
```

### **请求示例**

```
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/your/file1.jsonl"' \
  --form 'purpose="fine-tune"'\
  --form 'descriptions="a sample fine-tune data file for qwen"' \
  --form 'files=@"/path/to/your/file2.jsonl"' \
  --form 'purpose="fine-tune"'\
  --form 'descriptions="a sample fine-tune data file for qwen"'
```

### **请求参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

files

文件流

multipart/form-data

是

训练文件，支持多文件上传

purpose

字符串

multipart/form-data

是

**字段**

**用途**

`fine-tune`

通过上传后的`file_id`[创建调优任务](https://help.aliyun.com/zh/model-studio/fine-tuning-api-guide#693401fe5dxia)。

`file-extract`

通过上传后的`file_id`进行[长上下文（Qwen-Long）](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)内容分析。

`batch`

通过上传后的`file_id`来[创建Batch任务](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/#ad26763d91p5o)。

descriptions

文件流

multipart/form-data

否

文件描述

### **返回示例**

```
{
    "request_id": "xxx",
    "data": {
        "uploaded_files": [
            {
                "file_id": "9G2EaQtq7p1fw7oRhYXdHTtDFYAMVQSh95432B38CAB211EDB8F952C2E8001733",
                "name": "test.txt"
            }
        ],
        "failed_uploads": [
            {
                "name": "test1.jpg",
                "code": "BadRequest.TooLarge",
                "message": "Out of space, <839> B of <1024> B storage space has been used."
            },
            {
                "name": "test2.jpg",
                "code": "BadRequest.TooMany",
                "message": "Out of number, <10> of <10> files has been uploaded."
            }
        ]
    }
}
```

### **返回参数**

**字段**

**类型**

**描述**

data.failed\_uploads

Array

上传失败的文件信息

data.uploaded\_files

Array

上传成功的文件信息

data.uploaded\_files.$.file\_id

String

文件ID

data.uploaded\_files.$.name

String

文件名称

request\_id

String

本次请求的系统唯一码

## **列举当前所有的文件**

```
GET https://dashscope.aliyuncs.com/api/v1/files
Accept: application/json
```

### **请求示例**

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/files?page_no=1&page_size=20" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### **请求参数**

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

### **返回示例**

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
```

### **返回参数**

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

文件列表

data.files.$.file\_id

String

文件ID

data.files.$.url

String

文件下载链接

data.files.$.name

String

文件名

data.files.$.size

Number

文件大小

data.files.$.md5

String

文件的md5

data.files.$.description

String

文件的描述

data.files.$.gmt\_create

Date

文件上传时间

data.files.$.id

Number

文件的内部ID

data.files.$.region

String

文件所在地域

data.files.$.user\_id

String

用户ID

data.files.$.api\_key\_id

String

API Key ID

data.files.$.purpose

String

文件用途

request\_id

String

本次请求的系统唯一码

## **获取指定文件信息**

```
GET https://dashscope.aliyuncs.com/api/v1/files/{file_id}
Accept: application/json
```

### **请求示例**

```
curl --location --request GET "https://dashscope.aliyuncs.com/api/v1/files/123" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### **请求参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

file\_id

String

path

是

文件ID

### **返回示例**

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
        "url": "http://xxxxx.oss-cn-hangzhou.aliyuncs.com/oss%3A//dashscope-pre/api-fs/1253/236/dogs.jpg?Expires=1679797621&OSSAccessKeyId=demo&Signature=demo%3D"
    }
}
```

### **返回参数**

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

## **删除文件**

```
DELETE https://dashscope.aliyuncs.com/api/v1/files/{file_id}
Accept: application/json
```

### **请求示例**

```
curl --location --request DELETE "https://dashscope.aliyuncs.com/api/v1/files/123" \
--header "Authorization: Bearer ${DASHSCOPE_API_KEY}"
```

### **请求参数**

**字段**

**类型**

**传参方式**

**必选**

**描述**

file\_id

String

path

是

文件ID

### **返回示例**

```
{
    "request_id": "038e9953-6f0e-4691-afcc-1f0fe07b32c2"
}
```

### **返回参数**

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

## **请求异常**

### **返回示例**

当返回的HTTP状态码不为200时，表示请求失败，此时示例返回如下。

```
{
    "request_id": "8f25f57c-5cc0-9881-9c83-62bc173dc9ad",
    "code": "InvalidParameter",
    "message": "File not found."
}
```

### **返回参数**

**字段**

**类型**

**描述**

code

String

错误码。

request\_id

String

本次请求的系统唯一码。

message

String

错误信息。
