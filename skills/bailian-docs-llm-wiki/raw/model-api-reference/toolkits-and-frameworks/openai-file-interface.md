# OpenAI文件接口兼容

文件上传接口用于上传文件，以便在 Qwen-Long 和 Qwen-Doc-Turbo 模型中进行文档问答与数据提取，或将其用作批量推理任务的输入文件。

<a id="使用方式"></a>

<a id="c1e6d7bc04x7q"></a>

## 使用方式

支持通过OpenAI SDK（Python、Java）或HTTP API调用文件接口，包括上传、查询、删除等操作。

<a id="前提条件"></a>

<a id="618e4ed5b9oah"></a>

### 前提条件

-   阿里云百炼API-KEY：[获取与配置 API Key](../preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
-   使用OpenAI SDK调用服务，您还需安装[OpenAI SDK](../preparations/install-sdk.md)。

<a id="支持的模型"></a>

<a id="b75006f61am7t"></a>

## 支持的模型

文件ID可用于以下场景：

-   **Qwen-Long**：通过文件ID进行长文档问答
-   **Qwen-Doc-Turbo**：通过文件ID进行文件内数据提取与问答
-   [**批量推理**](batch-interfaces-compatible-with-openai.md)：通过文件ID上传批量任务输入文件

<a id="快速开始"></a>

<a id="efd2649f09bsz"></a>

## 快速开始

<a id="上传文件"></a>

<a id="a091dc7c8c7be"></a>

### 上传文件

百炼存储空间支持的最大文件数为10000个，总大小不超过100 GB，暂时没有有效期限制。当文件数量或总大小达到任一上限时，新的文件上传请求将会失败。请删除不再需要的文件以释放配额，然后才能继续上传。

<a id="sec-tabs"></a>

<a id="用于文档分析"></a>

<a id="用于文档分析-h4"></a>

#### 用于文档分析

将purpose指定为`file-extract`，文件格式支持文本文件（ TXT、DOCX、PDF、XLSX、EPUB、MOBI、MD、CSV、JSON），图片文件（BMP、PNG、JPG/JPEG、GIF和PDF扫描件），单个文件最大为 **150 MB**。

> 关于通过file\_id进行文档分析，请参考[长上下文（Qwen-Long）](../../model-user-guide/model-experience/text-generation-model/specialized-models/long-context-qwen-long.md)。

<a id="1d076474dd4lf"></a>

#### 请求示例

<a id="fig-code-group"></a>

<a id="fig-code-group-python-tab"></a>

python

<a id="code-code-group-python"></a>

```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# test.txt 是一个本地示例文件
file_object = client.files.create(file=Path("test.txt"), purpose="file-extract")

print(file_object.model_dump_json())
```

<a id="fig-code-group-java-tab"></a>

java

<a id="code-code-group-java"></a>

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.files.*;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();
        // 设置文件路径,请根据实际需求修改路径与文件名
        Path filePath = Paths.get("src/main/java/org/example/test.txt");
        // 创建文件上传参数
        FileCreateParams params = FileCreateParams.builder()
                .file(filePath)
                .purpose(FilePurpose.of("file-extract"))
                .build();

        // 上传文件
        FileObject fileObject = client.files().create(params);
        System.out.println(fileObject);
    }
}
```

<a id="fig-code-group-bash-tab"></a>

bash

<a id="code-code-group-bash"></a>

```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'file=@"test.txt"' \
--form 'purpose="file-extract"'
```

<a id="320c8b1c2cjzm"></a>

#### 响应示例

<a id="code-block"></a>

```json
{
    "id": "file-fe-xxx",
    "bytes": 2055,
    "created_at": 1729065448,
    "filename": "test.txt",
    "object": "file",
    "purpose": "file-extract",
    "status": "processed",
    "status_details": null
}
```

<a id="用于batch调用"></a>

<a id="用于batch调用-h4"></a>

#### 用于Batch调用

将purpose指定为`batch`，输入文件必须是jsonl文件且符合[输入文件大小与格式要求](batch-interfaces-compatible-with-openai.md)，上传Batch任务的单个文件最大为500 MB。

> 关于Batch调用的更多用法，请参考[OpenAI兼容-Batch（文件输入）](batch-interfaces-compatible-with-openai.md)。

<a id="f961be393c3bb"></a>

#### 请求示例

<a id="fig-code-group-2"></a>

<a id="fig-code-group-2-python-tab"></a>

python

<a id="code-code-group-2-python"></a>

```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# test.jsonl 是一个本地示例文件
file_object = client.files.create(file=Path("test.jsonl"), purpose="batch")

print(file_object.model_dump_json())
```

<a id="fig-code-group-2-java-tab"></a>

java

<a id="code-code-group-2-java"></a>

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.files.*;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();
        // 设置文件路径,请根据实际需求修改路径与文件名
        Path filePath = Paths.get("src/main/java/org/example/test.txt");
        // 创建文件上传参数
        FileCreateParams params = FileCreateParams.builder()
                .file(filePath)
                .purpose(FilePurpose.of("batch"))
                .build();

        // 上传文件
        FileObject fileObject = client.files().create(params);
        System.out.println(fileObject);
    }
}
```

<a id="fig-code-group-2-bash-tab"></a>

bash

<a id="code-code-group-2-bash"></a>

```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'file=@"test.jsonl"' \
--form 'purpose="batch"'
```

<a id="11363c76823pf"></a>

#### 响应示例

<a id="code-block-2"></a>

```json
{
    "id": "file-batch-xxx",
    "bytes": 231,
    "created_at": 1729065815,
    "filename": "test.jsonl",
    "object": "file",
    "purpose": "batch",
    "status": "processed",
    "status_details": null
}
```

<a id="用于创建调优任务"></a>

<a id="用于创建调优任务-h4"></a>

#### 用于创建调优任务

将purpose指定为`fine-tune`，输入文件必须是jsonl文件且符合[输入文件大小与格式要求](https://help.aliyun.com/zh/model-studio/model-customization-file-management-service)，上传调优数据集/训练集的单个文件最大为300 MB。

> 关于使用 API 进行模型调优的更多用法，请参考[模型调优](../../model-user-guide/model-training/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)

<a id="71c92b3f2fpck"></a>

#### 请求示例

<a id="fig-code-group-3"></a>

<a id="fig-code-group-3-python-tab"></a>

python

<a id="code-code-group-3-python"></a>

```python
import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# file.jsonl 是一个本地示例文件
file_object = client.files.create(file=Path("file.jsonl"), purpose="fine-tune")

print(file_object.model_dump_json())
```

<a id="fig-code-group-3-java-tab"></a>

java

<a id="code-code-group-3-java"></a>

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.files.*;

import java.nio.file.Path;
import java.nio.file.Paths;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();
        // 设置文件路径,请根据实际需求修改路径与文件名
        Path filePath = Paths.get("src/main/java/org/example/file.jsonl");
        // 创建文件上传参数
        FileCreateParams params = FileCreateParams.builder()
                .file(filePath)
                .purpose(FilePurpose.of("fine-tune"))
                .build();

        // 上传文件
        FileObject fileObject = client.files().create(params);
        System.out.println(fileObject);
    }
}
```

<a id="fig-code-group-3-bash-tab"></a>

bash

<a id="code-code-group-3-bash"></a>

```bash
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'file=@"file.jsonl"' \
--form 'purpose="fine-tune"'
```

<a id="查询文件信息"></a>

<a id="223fc94330wz5"></a>

### 查询文件信息

通过在retrieve或GET方法中指定`file_id`来查询文件信息。

<a id="sec-tabs-2"></a>

<a id="openai-python-sdk"></a>

<a id="openai-python-sdk-h4"></a>

#### OpenAI Python SDK

<a id="dc15197eebf5n"></a>

#### 请求示例

<a id="code-block-3"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file = client.files.retrieve(file_id="file-batch-xxx")

print(file.model_dump_json())
```

<a id="50433494402tj"></a>

#### 返回示例

<a id="code-block-4"></a>

```json
{
  "id": "file-batch-xxx",
  "bytes": 27,
  "created_at": 1722480306,
  "filename": "test.txt",
  "object": "file",
  "purpose": "batch",
  "status": "processed",
  "status_details": null
}
```

<a id="openai-java-sdk"></a>

<a id="openai-java-sdk-h4"></a>

#### OpenAI Java SDK

<a id="code-block-5"></a>

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.FileObject;
import com.openai.models.FileRetrieveParams;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();
        // 创建文件查询参数,请根据实际需求替换相应的fileId
        FileRetrieveParams params= FileRetrieveParams.builder()
                .fileId("file-batch-xxx")
                .build();
        //查询文件
        FileObject fileObject = client.files().retrieve(params);
        System.out.println(fileObject);
    }
}
```

<a id="http"></a>

<a id="http-h4"></a>

#### HTTP

<a id="b11e6f04d7fnh"></a>

#### 需要配置的endpoint

<a id="code-block-6"></a>

```http
GET https://dashscope-intl.aliyuncs.com/compatible-mode/v1/files/{file_id}
```

<a id="e4c57eb780hem"></a>

#### 请求示例

<a id="code-block-7"></a>

```bash
curl -X GET https://dashscope.aliyuncs.com/compatible-mode/v1/files/file-batch-xxx \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="fdd2a3cf08cpc"></a>

#### 返回示例

<a id="code-block-8"></a>

```json
{
    "id": "file-batch-xxx",
    "object": "file",
    "bytes": 499719,
    "created_at": 1715935833,
    "filename": "test.txt",
    "purpose": "batch",
    "status": "processed"
}
```

<a id="查询文件列表"></a>

<a id="77a1a1d0bdq4n"></a>

### 查询文件列表

返回所有文件的信息，包括通过上传文件接口上传的文件以及batch任务的结果文件。

> **说明**
>
> 此接口支持更多筛选参数，详情请参见[参数说明](openai-file-interface.md#a9b268386f7x8)。

<a id="sec-tabs-3"></a>

<a id="openai-python-sdk-2"></a>

<a id="openai-python-sdk-2-h4"></a>

#### OpenAI Python SDK

<a id="fa31e017a91b4"></a>

#### 请求示例

<a id="code-block-9"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file_stk = client.files.list(after="file-batch-xxx",limit=20)
print(file_stk.model_dump_json())
```

<a id="13956abcefvqf"></a>

#### 返回示例

<a id="code-block-10"></a>

```json
{
  "data": [
    {
      "id": "file-batch-xxx",
      "bytes": 27,
      "created_at": 1722480543,
      "filename": "test.txt",
      "object": "file",
      "purpose": "batch",
      "status": "processed",
      "status_details": null
    },
    {
      "id": "file-batch-yyy",
      "bytes": 431986,
      "created_at": 1718089390,
      "filename": "test.pdf",
      "object": "file",
      "purpose": "batch",
      "status": "processed",
      "status_details": null
    }
  ],
  "object": "list",
  "has_more": false
}
```

<a id="openai-java-sdk-2"></a>

<a id="openai-java-sdk-2-h4"></a>

#### OpenAI Java SDK

<a id="code-block-11"></a>

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.FileListPage;
import com.openai.models.FileListParams;

public class Main {
    public static void main(String[] args) {
        // 创建客户端，使用环境变量中的API密钥
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();
        // 创建文件列表查询参数
        FileListParams params = FileListParams.builder()
                .after("file-batch-xxx")
                .limit(20)
                .build();
        //查询文件列表
        FileListPage file_stk = client.files().list(params);
        System.out.println(file_stk);
    }
}
```

<a id="http-2"></a>

<a id="http-2-h4"></a>

#### HTTP

<a id="f075ec68c96dk"></a>

#### 需要配置的endpoint

<a id="code-block-12"></a>

```http
GET https://dashscope-intl.aliyuncs.com/compatible-mode/v1/files
```

<a id="af7ec16f4d2vd"></a>

#### 请求示例

<a id="code-block-13"></a>

```bash
curl -X GET https://dashscope.aliyuncs.com/compatible-mode/v1/files \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="23f7a3f725viz"></a>

#### 返回示例

<a id="code-block-14"></a>

```json
{
    "object": "list",
    "has_more": true,
    "data": [
        {
            "id": "file-batch-xxx",
            "object": "file",
            "bytes": 84889,
            "created_at": 1715569225,
            "filename": "example.txt",
            "purpose": "batch",
            "status": "processed"
        },
        {
            "id": "file-batch-yyy",
            "object": "file",
            "bytes": 722355,
            "created_at": 1715413868,
            "filename": "Agent_survey.pdf",
            "purpose": "batch",
            "status": "processed"
        }
    ]
}
```

<a id="删除文件"></a>

<a id="3457ce1d7ezr3"></a>

### 删除文件

通过删除文件接口删除指定`file_id`的文件。可以通过[查询文件列表](openai-file-interface.md#77a1a1d0bdq4n)接口查询文件信息。

<a id="sec-tabs-4"></a>

<a id="openai-python-sdk-3"></a>

<a id="openai-python-sdk-3-h4"></a>

#### OpenAI Python SDK

<a id="37d7aabdd710j"></a>

#### 请求示例

<a id="code-block-15"></a>

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file_object = client.files.delete("file-batch-xxx")
print(file_object.model_dump_json())
```

<a id="91b8e19e964sx"></a>

#### 返回示例

<a id="code-block-16"></a>

```json
{
  "object": "file",
  "deleted": true,
  "id": "file-batch-xxx"
}
```

<a id="openai-java-sdk-3"></a>

<a id="openai-java-sdk-3-h4"></a>

#### OpenAI Java SDK

<a id="code-block-17"></a>

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.FileDeleteParams;

public class Main {
    public static void main(String[] args) {
        OpenAIClient client = OpenAIOkHttpClient.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();
        FileDeleteParams params = FileDeleteParams.builder()
                .fileId("file-batch-xxx")
                .build();

        System.out.println(client.files().delete(params));
    }
}
```

<a id="http-3"></a>

<a id="http-3-h4"></a>

#### HTTP

<a id="7b0e148addyle"></a>

#### 需要配置的endpoint

<a id="code-block-18"></a>

```http
DELETE https://dashscope-intl.aliyuncs.com/compatible-mode/v1/files/{file_id}
```

<a id="61f7514f1avj4"></a>

#### 请求示例

<a id="code-block-19"></a>

```bash
curl -X  DELETE https://dashscope.aliyuncs.com/compatible-mode/v1/files/file-batch-xxx \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<a id="2ac9ed70fa5dy"></a>

#### 返回示例

<a id="code-block-20"></a>

```json
{
  "object": "file",
  "deleted": true,
  "id": "file-batch-oLIon7bzfxELqJBTS5okwC4E"
}
```

<a id="计费说明"></a>

<a id="d5235cefad9sn"></a>

## 计费说明

文件上传、存储和查询操作不产生费用。仅在调用模型API时，根据实际使用的输入Token和输出Token进行计费。

<a id="限流"></a>

<a id="c02e8d0489yi3"></a>

## 限流

上传文件接口的QPS（每秒请求数）限制为3。查询文件信息、查询文件列表、删除文件接口的QPS总和限制为10。

<a id="应用于生产环境"></a>

<a id="e0515f28b4dol"></a>

## 应用于生产环境

-   **定期清理**：定期删除不再使用的文件，避免达到10000个文件上限。
-   **状态检查**：上传后检查文件状态。`status`为`processed`表示文件已上传完成、可用于引用，但不代表解析已完成；解析完成前调用可能返回`File parsing in progress`，请稍后重试。
-   **限流检查**：上传文件接口的QPS（每秒请求数）限制为3。查询文件信息、查询文件列表、删除文件接口的QPS总和限制为10。
-   **错误处理**：实现完整的异常处理机制，包括网络错误、API错误等。

<a id="常见问题"></a>

<a id="444fba1975ivw"></a>

## 常见问题

<a id="1-文件上传后状态一直是-processing-怎么办"></a>

<a id="1-processing-"></a>

### 1\. 文件上传后状态一直是"processing"怎么办？

文件处理需要一定时间，通常几秒内完成。如果长时间处于"processing"状态：

-   检查文件格式是否支持
-   检查文件大小是否超过限制
-   使用`retrieve`接口定期查询状态

<a id="2-文件id可以跨账号使用吗"></a>

<a id="2-id-"></a>

### 2\. 文件ID可以跨账号使用吗？

不可以。文件ID仅在生成它的阿里云主账号内有效，不支持跨账号共享。

<a id="3-上传的文件会被永久保存吗"></a>

<a id="3-"></a>

### 3\. 上传的文件会被永久保存吗？

是的，上传的文件会被永久保存在您的阿里云账号下，除非主动删除。建议定期清理不需要的文件。

<a id="4-文件上传失败-可能的原因有哪些"></a>

<a id="4-"></a>

### 4\. 文件上传失败，可能的原因有哪些？

-   API Key无效或未配置
-   文件格式不支持
-   文件大小超过限制（file-extract: 150MB，batch: 500MB）
-   已达到文件数量上限（10000个）或总大小上限（100GB）
-   上传文件接口的QPS（每秒请求数）限制为3。

<a id="5-purpose参数应该如何选择"></a>

<a id="5-purpose-file-extract-batch-"></a>

### 5\. purpose参数应该如何选择？

-   `file-extract`：用于文档分析场景，配合Qwen-Long或Qwen-Doc-Turbo使用
-   `batch`：用于批量推理任务，文件必须是符合格式要求的JSONL文件

<a id="6-status-为-processed-后调用-qwen-long-仍提示文件解析中怎么办"></a>

<a id="6-processed-qwen-long-file-parsing"></a>

### 6\. status 为 "processed" 后调用 Qwen-Long 仍提示文件解析中怎么办？

`status` 为 `processed` 仅表示文件已上传完成、可用于引用，不代表解析已完成。如果调用 Qwen-Long 时返回 `File parsing in progress, please try again later.`，请稍后重试，待文件解析完成后即可正常调用。

<a id="参数说明"></a>

<a id="a9b268386f7x8"></a>

## 参数说明

<table><thead><tr><th><strong>接口类别</strong></th><th><strong>参数名</strong></th><th><strong>类型</strong></th><th><strong>必选</strong></th><th><strong>说明</strong></th><th><strong>示例值</strong></th></tr></thead><tbody><tr><td rowspan="2"><p>文档上传</p></td><td><p>file</p></td><td><p><em>File</em></p></td><td><p>是</p></td><td><p>用于指定待上传的文件。</p></td><td><p>Path(&quot;test.txt&quot;)</p></td></tr><tr><td><p>purpose</p></td><td><p><em>String</em></p></td><td><p>是</p></td><td><p>用于指定上传文件的用途。每种用途所需的文件格式、大小及内容规范，请参考对应功能文档中的详细要求。当前可选值如下：</p><p><code>file-extract</code>: 用于<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/long-context-qwen-long.md">Qwen-Long</a>与<a href="../../model-user-guide/model-experience/text-generation-model/specialized-models/data-mining-qwen-doc.md">Qwen-Doc</a>模型的文档理解与数据提取；</p><p><code>batch</code>: 用于<a href="batch-interfaces-compatible-with-openai.md">OpenAI兼容-Batch（文件输入）</a>任务；</p></td><td><p>&quot;file-extract&quot;</p></td></tr><tr><td rowspan="6"><p>文件查询</p></td><td><p>file_id</p></td><td><p><em>String</em></p></td><td><p>是</p></td><td><p>待查询的文件id。</p></td><td><p>&quot;file-fe-xxx&quot;</p></td></tr><tr><td><p>after</p></td><td><p><em>String</em></p></td><td><p>否</p></td><td><p><a href="openai-file-interface.md#77a1a1d0bdq4n">查询文件列表</a>任务中用于分页的游标。</p><p>参数<code>after</code>的取值为当前分页的最后一个file_id，表示查询该ID之后下一页的数据。</p><p>例如，若本次查询返回了20条数据，且最后一个file_id是file-batch-xxx，则后续查询时可以设置<code>after=&quot;file-batch-xxx&quot;</code>，以获取列表的下一页。</p></td><td><p>&quot;file-fe-xxx&quot;</p></td></tr><tr><td><p>create_before</p></td><td><p><em>String</em></p></td><td><p>否</p></td><td><p><a href="openai-file-interface.md#77a1a1d0bdq4n">查询文件列表</a>任务中，一个字符串格式的时间戳。用于筛选并返回创建时间<strong>早于</strong>该指定时间点的file_id。</p></td><td><p><code>&quot;20250306123000&quot;</code>, <code>&quot;2025-11-12 10:10:10&quot;</code>, <code>&quot;2025-11-12&quot;</code>, <code>&quot;20251112&quot;</code></p></td></tr><tr><td><p>create_after</p></td><td><p><em>String</em></p></td><td><p>否</p></td><td><p><a href="openai-file-interface.md#77a1a1d0bdq4n">查询文件列表</a>任务中，一个字符串格式的时间戳。用于筛选并返回创建时间<strong>晚于</strong>该指定时间点的file_id。</p></td><td><p><code>&quot;20250306123000&quot;</code>, <code>&quot;2025-11-12 10:10:10&quot;</code>, <code>&quot;2025-11-12&quot;</code>, <code>&quot;20251112&quot;</code></p></td></tr><tr><td><p>purpose</p></td><td><p><em>String</em></p></td><td><p>否</p></td><td><p><a href="openai-file-interface.md#77a1a1d0bdq4n">查询文件列表</a>任务中根据文件的用途进行筛选，仅返回与指定 purpose（<code>file-extract</code>或<code>batch</code>）相匹配的file_id。</p></td><td><p>&quot;batch&quot;</p></td></tr><tr><td><p>limit</p></td><td><p><em>Integer</em></p></td><td><p>否</p></td><td><p><a href="openai-file-interface.md#77a1a1d0bdq4n">查询文件列表</a>任务中每次查询返回的文件数量，取值范围[1,2000]，默认2000。</p></td><td><p>2000</p></td></tr><tr><td><p>文件删除</p></td><td><p>file_id</p></td><td><p><em>String</em></p></td><td><p>是</p></td><td><p>待删除文件id。</p></td><td><p>&quot;file-fe-xxx&quot;</p></td></tr><tr><td colspan="6"><strong>响应参数</strong></td></tr><tr><td rowspan="7"><p>通用响应参数</p></td><td><p>id</p></td><td><p><em>String</em></p></td><td rowspan="10"><p>\</p></td><td><p>文件的标识符</p><p><a href="openai-file-interface.md#3457ce1d7ezr3">删除文件</a>任务中表示成功删除的文件的id。</p></td><td><p>&quot;file-fe-xxx&quot;</p></td></tr><tr><td><p>bytes</p></td><td><p><em>Integer</em></p></td><td><p>文件大小，单位为字节。</p></td><td><p>81067</p></td></tr><tr><td><p>created_at</p></td><td><p><em>Integer</em></p></td><td><p>文件创建时的 Unix 时间戳（秒）。</p></td><td><p>1617981067</p></td></tr><tr><td><p>filename</p></td><td><p><em>String</em></p></td><td><p>上传的文件名。</p></td><td><p>&quot;text.txt&quot;</p></td></tr><tr><td><p>object</p></td><td><p><em>String</em></p></td><td><p>对象类型</p><p><a href="openai-file-interface.md#77a1a1d0bdq4n">查询文件列表</a>任务中始终为&quot;list&quot;。</p><p>其余类型任务中始终为&quot;file&quot;。</p></td><td><p>&quot;file&quot;</p></td></tr><tr><td><p>purpose</p></td><td><p><em>String</em></p></td><td><p>文件的用途，取值有<code>batch</code>、<code>file-extract</code>、<code>batch_output</code>。</p></td><td><p>&quot;file-extract&quot;</p></td></tr><tr><td><p>status</p></td><td><p><em>String</em></p></td><td><p>文件的当前状态。可能的状态有：<code>uploaded</code>（已上传，等待处理）, <code>processing</code>（处理中）, <code>processed</code>（上传已完成，可用于引用；不代表解析已完成）, <code>error</code>（处理失败）。</p></td><td><p>&quot;processed&quot;</p></td></tr><tr><td rowspan="2"><p>查询文件列表</p></td><td><p>has_more</p></td><td><p><em>Boolean</em></p></td><td><p>是否还有下一页数据。</p></td><td><p>false</p></td></tr><tr><td><p>data</p></td><td><p><em>Array</em></p></td><td><p>返回的文件列表，列表中每个元素格式与通用相应参数一致。</p></td><td><a id="code-block-21"></a><pre class="language-json"><code>[{
 &quot;id&quot;: &quot;xxx&quot;,
 &quot;bytes&quot;: 27,
 &quot;created_at&quot;: 1722480543,
 &quot;filename&quot;: &quot;test.txt&quot;,
 &quot;object&quot;: &quot;file&quot;,
 &quot;purpose&quot;: &quot;batch&quot;,
 &quot;status&quot;: &quot;processed&quot;,
 &quot;status_details&quot;: null
 }]
</code></pre></td></tr><tr><td><p>删除文件</p></td><td><p>deleted</p></td><td><p><em>Boolean</em></p></td><td><p>是否删除成功，true表示删除成功。</p></td><td><p>true</p></td></tr></tbody></table>

<a id="错误码"></a>

<a id="efc117f59a2gm"></a>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](../preparations/error-code.md)进行解决。
