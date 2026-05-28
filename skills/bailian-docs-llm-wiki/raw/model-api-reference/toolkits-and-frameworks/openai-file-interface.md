# OpenAI文件接口兼容

文件上传接口用于上传文件，以便在[Qwen-Long](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)和[Qwen-Doc-Turbo](https://help.aliyun.com/zh/model-studio/data-mining-qwen-doc)模型中进行文档问答与数据提取，或将其用作批量推理任务的输入文件。

## 使用方式

支持通过OpenAI SDK（Python、Java）或HTTP API调用文件接口，包括上传、查询、删除等操作。

### **前提条件**

-   阿里云百炼API-KEY：[获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)
    
-   使用OpenAI SDK调用服务，您还需安装[OpenAI SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

## 支持的模型

文件ID可用于以下场景：

-   **Qwen-Long**：通过文件ID进行长文档问答
    
-   **Qwen-Doc-Turbo**：通过文件ID进行文件内数据提取与问答
    
-   [**批量推理**](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/#80d1d39cf85zk)：通过文件ID上传批量任务输入文件
    

## 快速开始

### **上传文件**

百炼存储空间支持的最大文件数为10000个，总大小不超过100 GB，暂时没有有效期限制。当文件数量或总大小达到任一上限时，新的文件上传请求将会失败。请删除不再需要的文件以释放配额，然后才能继续上传。

### 用于文档分析

将purpose指定为`file-extract`，文件格式支持文本文件（ TXT、DOCX、PDF、XLSX、EPUB、MOBI、MD、CSV、JSON），图片文件（BMP、PNG、JPG/JPEG、GIF和PDF扫描件），单个文件最大为 **150 MB**。

> 关于通过file\_id进行文档分析，请参考[长上下文（Qwen-Long）](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)。

#### **请求示例**

Python

```
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

Java

```
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

curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'file=@"test.txt"' \
--form 'purpose="file-extract"'
```

#### **响应示例**

```
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

### **用于Batch调用**

将purpose指定为`batch`，输入文件必须是jsonl文件且符合[输入文件大小与格式要求](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/#578afe12c1uvz)，上传Batch任务的单个文件最大为500 MB。

> 关于Batch调用的更多用法，请参考[OpenAI兼容-Batch](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)。

#### **请求示例**

Python

```
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

Java

```
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

curl

```
curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
--form 'file=@"test.jsonl"' \
--form 'purpose="batch"'
```

#### **响应示例**

```
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

### **查询文件信息**

通过在retrieve或GET方法中指定`file_id`来查询文件信息。

## OpenAI Python SDK

#### 请求示例

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file = client.files.retrieve(file_id="file-batch-xxx")

print(file.model_dump_json())
```

#### **返回示例**

```
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

## OpenAI Java SDK

```
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

## HTTP

#### 需要配置的endpoint

```
GET https://dashscope.aliyuncs.com/compatible-mode/v1/files/{file_id}
```

#### **请求示例**

```
curl -X GET https://dashscope.aliyuncs.com/compatible-mode/v1/files/file-batch-xxx \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### **返回示例**

```
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

### 查询文件列表

返回所有文件的信息，包括通过上传文件接口上传的文件以及batch任务的结果文件。

**说明**

此接口支持更多筛选参数，详情请参见[参数说明](#a9b268386f7x8)。

## OpenAI Python SDK

#### 请求示例

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file_stk = client.files.list(after="file-batch-xxx",limit=20)
print(file_stk.model_dump_json())
```

#### **返回示例**

```
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

## OpenAI Java SDK

```
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

## HTTP

#### 需要配置的endpoint

```
GET https://dashscope.aliyuncs.com/compatible-mode/v1/files
```

#### **请求示例**

```
curl -X GET https://dashscope.aliyuncs.com/compatible-mode/v1/files \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### **返回示例**

```
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

### 删除文件

通过删除文件接口删除指定`file_id`的文件。可以通过[查询文件列表](#77a1a1d0bdq4n)接口查询文件信息。

## OpenAI Python SDK

#### **请求示例**

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

file_object = client.files.delete("file-batch-xxx")
print(file_object.model_dump_json())
```

#### **返回示例**

```
{
  "object": "file",
  "deleted": true,
  "id": "file-batch-xxx"
}
```

## OpenAI Java SDK

```
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.FileDeleteParams;
import com.openai.models.FileListPage;
import com.openai.models.FileListParams;

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

## HTTP

#### 需要配置的endpoint

```
DELETE https://dashscope.aliyuncs.com/compatible-mode/v1/files/{file_id}
```

#### **请求示例**

```
curl -X  DELETE https://dashscope.aliyuncs.com/compatible-mode/v1/files/file-batch-xxx \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

#### **返回示例**

```
{
  "object": "file",
  "deleted": true,
  "id": "file-batch-oLIon7bzfxELqJBTS5okwC4E"
}
```

## 计费说明

文件上传、存储和查询操作不产生费用。仅在调用模型API时，根据实际使用的输入Token和输出Token进行计费。

## 限流

上传文件接口的QPS（每秒请求数）限制为3。查询文件信息、查询文件列表、删除文件接口的QPS总和限制为10。

## 应用于生产环境

-   **定期清理**：定期删除不再使用的文件，避免达到10000个文件上限。
    
-   **状态检查**：上传后检查文件状态，确保`status`为`processed`后再使用。
    
-   **限流检查**：上传文件接口的QPS（每秒请求数）限制为3。查询文件信息、查询文件列表、删除文件接口的QPS总和限制为10。
    
-   **错误处理**：实现完整的异常处理机制，包括网络错误、API错误等。
    

## 常见问题

### **1\. 文件上传后状态一直是"processing"怎么办？**

文件处理需要一定时间，通常几秒内完成。如果长时间处于"processing"状态：

-   检查文件格式是否支持
    
-   检查文件大小是否超过限制
    
-   使用`retrieve`接口定期查询状态
    

### **2\. 文件ID可以跨账号使用吗？**

不可以。文件ID仅在生成它的阿里云主账号内有效，不支持跨账号共享。

### **3\. 上传的文件会被永久保存吗？**

是的，上传的文件会被永久保存在您的阿里云账号下，除非主动删除。建议定期清理不需要的文件。

### **4\. 文件上传失败，可能的原因有哪些？**

-   API Key无效或未配置
    
-   文件格式不支持
    
-   文件大小超过限制（file-extract: 150MB，batch: 500MB）
    
-   已达到文件数量上限（10000个）或总大小上限（100GB）
    
-   上传文件接口的QPS（每秒请求数）限制为3。
    

### **5\. purpose参数应该如何选择？**

-   `file-extract`：用于文档分析场景，配合Qwen-Long或Qwen-Doc-Turbo使用
    
-   `batch`：用于批量推理任务，文件必须是符合格式要求的JSONL文件
    

## **参数说明**

**接口类别**

**参数名**

**类型**

**必选**

**说明**

**示例值**

文档上传

file

_File_

是

用于指定待上传的文件。

Path("test.txt")

purpose

_String_

是

用于指定上传文件的用途。每种用途所需的文件格式、大小及内容规范，请参考对应功能文档中的详细要求。当前可选值如下：

`file-extract`: 用于[Qwen-Long](https://help.aliyun.com/zh/model-studio/long-context-qwen-long)与[Qwen-Doc](https://help.aliyun.com/zh/model-studio/data-mining-qwen-doc)模型的文档理解与数据提取；

`batch`: 用于[OpenAI兼容-Batch](https://help.aliyun.com/zh/model-studio/batch-interfaces-compatible-with-openai/)任务；

"file-extract"

文件查询

file\_id

_String_

是

待查询的文件id。

"file-fe-xxx"

after

_String_

否

[查询文件列表](#77a1a1d0bdq4n)任务中用于分页的游标。

参数`after`的取值为当前分页的最后一个file\_id，表示查询该ID之后下一页的数据。

例如，若本次查询返回了20条数据，且最后一个file\_id是file-batch-xxx，则后续查询时可以设置`after="file-batch-xxx"`，以获取列表的下一页。

"file-fe-xxx"

create\_before

_String_

否

[查询文件列表](#77a1a1d0bdq4n)任务中，一个字符串格式的时间戳。用于筛选并返回创建时间**早于**该指定时间点的file\_id。

`"20250306123000"`, `"2025-11-12 10:10:10"`, `"2025-11-12"`, `"20251112"`

create\_after

_String_

否

[查询文件列表](#77a1a1d0bdq4n)任务中，一个字符串格式的时间戳。用于筛选并返回创建时间**晚于**该指定时间点的file\_id。

`"20250306123000"`, `"2025-11-12 10:10:10"`, `"2025-11-12"`, `"20251112"`

purpose

_String_

否

[查询文件列表](#77a1a1d0bdq4n)任务中根据文件的用途进行筛选，仅返回与指定 purpose（`file-extract`或`batch`）相匹配的file\_id。

"batch"

limit

_Integer_

否

[查询文件列表](#77a1a1d0bdq4n)任务中每次查询返回的文件数量，取值范围\[1,2000\]，默认2000。

2000

文件删除

file\_id

_String_

是

待删除文件id。

"file-fe-xxx"

**响应参数**

通用响应参数

id

_String_

\\

文件的标识符

[删除文件](#3457ce1d7ezr3)任务中表示成功删除的文件的id。

"file-fe-xxx"

bytes

_Integer_

文件大小，单位为字节。

81067

created\_at

_Integer_

文件创建时的 Unix 时间戳（秒）。

1617981067

filename

_String_

上传的文件名。

"text.txt"

object

_String_

对象类型

[查询文件列表](#77a1a1d0bdq4n)任务中始终为"list"。

其余类型任务中始终为"file"。

"file"

purpose

_String_

文件的用途，取值有`batch`、`file-extract`、`batch_output`。

"file-extract"

status

_String_

文件的当前状态。

"processed"

查询文件列表

has\_more

_Boolean_

是否还有下一页数据。

false

data

_Array_

返回的文件列表，列表中每个元素格式与通用相应参数一致。

```
[{
 "id": "xxx",
 "bytes": 27,
 "created_at": 1722480543,
 "filename": "test.txt",
 "object": "file",
 "purpose": "batch",
 "status": "processed",
 "status_details": null
 }]
```

删除文件

deleted

_Boolean_

是否删除成功，true表示删除成功。

true

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。
