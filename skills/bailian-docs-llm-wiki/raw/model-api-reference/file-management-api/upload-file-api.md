# 上传文件

上传文件到百炼平台，支持多文件上传，上传后可在多个任务中复用。

## 使用限制

当您使用本服务时，会有如下限制存在

-   单个文件大小限制因 purpose 而异：file-extract 最大 150MB，batch 最大 500MB，fine-tune 最大 300MB。
-   有效文件（未删除）总使用空间配额为100GB。
-   有效文件（未删除）总数量配额为10000个。

OpenAI 兼容方式调用请参考：相关文档。

**说明**通过 fine-tune purpose 上传的调优文件，在百炼控制台模型调优页面与 API 调用中均可见可用。

## 上传文件

```
POST https://dashscope.aliyuncs.com/api/v1/files
Content-type: multipart/form-data
```

### 请求示例

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

### 请求参数

**字段**

**类型**

**传参方式**

**必选**

**描述**

files

文件流

multipart/form-data

是

调优文件，支持多文件上传

purpose

字符串

multipart/form-data

否

**字段**

**用途**

`fine-tune`

通过上传后的`file_id`进行模型调优。视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）；也可通过 OSS 挂载方式加载，将未经压缩的数据集文件夹整体上传到 OSS，不支持 zip 文件。

`file-extract`

通过上传后的`file_id`进行内容分析。

`batch`

通过上传后的`file_id`来[创建Batch任务](raw/model-api-reference/toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md)。

不传 purpose 时文件仍可上传成功，建议明确指定 purpose 以便后续按用途管理文件。

descriptions

文件流

multipart/form-data

否

文件描述

### 返回示例

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

### 返回参数

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

文件ID，可用于查询文件详情和删除文件接口

data.uploaded\_files.$.name

String

文件名称

request\_id

String

本次请求的系统唯一码

## 请求异常

### 返回示例

当返回的HTTP状态码不为200时，表示请求失败，此时示例返回如下。

```
{
    "request_id": "8f25f57c-5cc0-9881-9c83-62bc173dc9ad",
    "code": "InvalidParameter",
    "message": "File not found."
}
```

### 返回参数

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
