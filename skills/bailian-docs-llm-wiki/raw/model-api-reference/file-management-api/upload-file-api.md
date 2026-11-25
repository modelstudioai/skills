# 上传文件

上传文件到百炼平台，支持多文件上传，上传后可在多个任务中复用。

> **重要**
>
> 当前接口主要用于兼容历史场景，推荐优先使用 [OpenAI 兼容的 File 接口](../toolkits-and-frameworks/openai-file-interface.md)。

<a id="使用限制"></a>

<a id="7d3645a119ovw"></a>

## 使用限制

当您使用本服务时，会有如下限制存在

-   单个文件大小限制因 purpose 而异：file-extract 最大 150MB，batch 最大 500MB，fine-tune 最大 300MB。
-   有效文件（未删除）总使用空间配额为100GB。
-   有效文件（未删除）总数量配额为10000个。

OpenAI 兼容方式调用请参考：相关文档。

> **说明**
>
> 通过 fine-tune purpose 上传的调优文件，在百炼控制台模型调优页面与 API 调用中均可见可用。

<a id="上传文件"></a>

<a id="d031ae7105c1g"></a>

## 上传文件

<a id="code-block"></a>

```http
POST https://dashscope.aliyuncs.com/api/v1/files
Content-type: multipart/form-data
```

<a id="请求示例"></a>

<a id="bcaf80700ectd"></a>

### 请求示例

<a id="code-block-2"></a>

```bash
curl --request POST "https://dashscope.aliyuncs.com/api/v1/files" \
  --header "Authorization: Bearer ${DASHSCOPE_API_KEY}" \
  --form 'files=@"/path/to/your/file1.jsonl"' \
  --form 'purpose="fine-tune"'\
  --form 'descriptions="a sample fine-tune data file for qwen"' \
  --form 'files=@"/path/to/your/file2.jsonl"' \
  --form 'purpose="fine-tune"'\
  --form 'descriptions="a sample fine-tune data file for qwen"'
```

<a id="请求参数"></a>

<a id="1c39a3e005266"></a>

### 请求参数

<table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>传参方式</strong></p></th><th><p><strong>必选</strong></p></th><th><p><strong>描述</strong></p></th></tr></thead><tbody><tr><td><p>files</p></td><td><p>文件流</p></td><td><p>multipart/form-data</p></td><td><p>是</p></td><td><p>调优文件，支持多文件上传</p></td></tr><tr><td><p>purpose</p></td><td><p>字符串</p></td><td><p>multipart/form-data</p></td><td><p>否</p></td><td><table><thead><tr><th><p><strong>字段</strong></p></th><th><p><strong>用途</strong></p></th></tr></thead><tbody><tr><td><p><code>fine-tune</code></p></td><td><p>通过上传后的<code>file_id</code>进行模型调优。视频/图像生成模型微调的训练数据需以 .zip 格式上传（单个 zip 包不超过 1 GB）；也可通过 OSS 挂载方式加载，将未经压缩的数据集文件夹整体上传到 OSS，不支持 zip 文件。</p></td></tr><tr><td><p><code>file-extract</code></p></td><td><p>通过上传后的<code>file_id</code>进行内容分析。</p></td></tr><tr><td><p><code>batch</code></p></td><td><p>通过上传后的<code>file_id</code>来<a href="../toolkits-and-frameworks/batch-interfaces-compatible-with-openai.md">创建Batch任务</a>。</p></td></tr></tbody></table><p>不传 purpose 时文件仍可上传成功，建议明确指定 purpose 以便后续按用途管理文件。</p></td></tr><tr><td><p>descriptions</p></td><td><p>文件流</p></td><td><p>multipart/form-data</p></td><td><p>否</p></td><td><p>文件描述</p></td></tr></tbody></table>

<a id="返回示例"></a>

<a id="1f56ab800ef6n"></a>

### 返回示例

<a id="code-block-3"></a>

```json
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

<a id="返回参数"></a>

<a id="60a895400eugt"></a>

### 返回参数

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| data.failed\_uploads | Array | 上传失败的文件信息 |
| data.uploaded\_files | Array | 上传成功的文件信息 |
| data.uploaded\_files.$.file\_id | String | 文件ID，可用于查询文件详情和删除文件接口 |
| data.uploaded\_files.$.name | String | 文件名称 |
| request\_id | String | 本次请求的系统唯一码 |

<a id="请求异常"></a>

<a id="00778a43fdyo9"></a>

## 请求异常

<a id="返回示例-2"></a>

<a id="bbf7f215dag50"></a>

### 返回示例

当返回的HTTP状态码不为200时，表示请求失败，此时示例返回如下。

<a id="code-block-4"></a>

```json
{
    "request_id": "8f25f57c-5cc0-9881-9c83-62bc173dc9ad",
    "code": "InvalidParameter",
    "message": "File not found."
}
```

<a id="返回参数-2"></a>

<a id="1c2489084di6p"></a>

### 返回参数

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| code | String | 错误码。 |
| request\_id | String | 本次请求的系统唯一码。 |
| message | String | 错误信息。 |
