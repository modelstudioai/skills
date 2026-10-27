# 定制热词Python SDK参考

通过Python SDK管理定制热词列表，包括client.audio.vocabularies资源的方法说明与示例代码。

**用户指南：**[提升识别准确率](raw/model-user-guide/model-experience/speech-recognition/improve-asr-accuracy.md)。热词列表数量上限等使用限制详见[热词限制与计费](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw10_limit_h2)。

**重要**新加坡地域的子业务空间暂不支持热词功能。

## 接口地址

SDK 默认使用**北京地域**的接口地址。如需切换到其他地域，在构造 `dashscope.Client` 时指定 `region` 参数（如新加坡地域为 `ap-southeast-1`）。

#### 华北2（北京）

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

#### 新加坡

`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`

调用时请将`{WorkspaceId}`替换为真实的[业务空间ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`

`{WorkspaceId}`需要替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)。现有域名仍可正常使用。

**切换到新加坡地域**：

```
import os
import dashscope

# 构造 Client 时指定新加坡地域
client = dashscope.Client(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    region='ap-southeast-1',
)
```

**注意**：

-   不同地域的 API Key 不同，请确保使用对应地域的 API Key
-   地域配置为 `dashscope.Client` 实例级设置，仅影响该 client 的 API 调用

## client.audio.vocabularies

**资源入口**：`dashscope.Client` 实例的 `client.audio.vocabularies` 资源

**功能**：管理热词列表的生命周期（创建、查询、更新、删除）

### 构造方法

```
import os
import dashscope

client = dashscope.Client(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    workspace='{WorkspaceId}',
    region='cn-beijing',
)
```

未传 `api_key` 时，SDK 自动读取 `DASHSCOPE_API_KEY` 环境变量的值。

### create() - 创建热词列表

**方法签名**：

```
def create(
    self,
    *,
    target_model: str,
    prefix: str,
    vocabulary: List[dict]) -> Vocabulary
```

**参数**：

**参数**

**类型**

**必填**

**说明**

target\_model

str

是

使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。

prefix

str

是

热词列表自定义前缀，仅允许数字和小写字母，长度不超过10个字符。

vocabulary

List\[dict\]

是

热词列表，每个dict包含 text、weight、lang 等字段。

详情请参见[热词字典结构](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)。

**返回值**：

**类型**

**说明**

Vocabulary

热词列表对象，通过 `vocabulary_id` 字段获取热词列表ID。

### list() - 批量查询热词列表

对应 HTTP API 的 `action: list_vocabulary`。

**方法签名**：

```
def list(
    self,
    *,
    prefix: str = None,
    page_index: int = 0,
    page_size: int = 10) -> VocabularyList
```

**参数**：

**参数**

**类型**

**必填**

**说明**

prefix

str

否

热词列表自定义前缀，如果设定则只返回指定前缀的热词列表。

page\_index

int

否

页码索引，从0开始计数。

默认值：0。

page\_size

int

否

每页包含数据条数。

默认值：10。

**返回值**：

**类型**

**说明**

VocabularyList

热词列表分页对象，`vocabularies` 字段为热词列表信息数组，每个dict包含 vocabulary\_id、gmt\_create、gmt\_modified、status。

**返回对象字段**：

**字段**

**类型**

**说明**

vocabulary\_id

str

热词列表ID。

gmt\_create

str

创建时间。

gmt\_modified

str

修改时间。

status

str

状态：

-   OK：可调用
    
-   UNDEPLOYED：不可调用。
    

* * *

### get() - 查询热词列表

对应 1.x SDK 的 `query_vocabulary()`。

**方法签名**：

```
def get(
    self,
    vocabulary_id: str) -> Vocabulary
```

**参数**：

**参数**

**类型**

**必填**

**说明**

vocabulary\_id

str

是

需要查询的热词列表ID。

**返回值**：

**类型**

**说明**

Vocabulary

热词列表详细信息对象，包含 vocabulary、target\_model、gmt\_create、gmt\_modified、status。

**返回对象字段**：

**字段**

**类型**

**说明**

vocabulary

List\[dict\]

热词列表内容。

target\_model

str

使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。

gmt\_create

str

创建时间。

gmt\_modified

str

修改时间。

status

str

状态：

-   OK：可调用
    
-   UNDEPLOYED：不可调用。
    

### update() - 更新热词列表

**方法签名**：

```
def update(
    self,
    vocabulary_id: str,
    *,
    vocabulary: List[dict]) -> JobStatus
```

**参数**：

**参数**

**类型**

**必填**

**说明**

vocabulary\_id

str

是

需要更新的热词列表ID。

vocabulary

List\[dict\]

是

新的热词列表，将完全替换原有内容。

**返回值**：JobStatus 对象，status 字段为操作状态。

### delete() - 删除热词列表

**方法签名**：

```
def delete(
    self,
    vocabulary_id: str) -> JobStatus
```

**参数**：

**参数**

**类型**

**必填**

**说明**

vocabulary\_id

str

是

需要删除的热词列表ID。

**返回值**：JobStatus 对象，status 字段为操作状态。

## 热词字典结构

**用于**`vocabulary`**参数的字典定义**：

**字段**

**类型**

**必填**

**说明**

text

str

是

热词文本。

热词文本的语言必须在所选模型的支持范围内，不同模型支持的语言各不相同。

热词用于提升识别的准确率，请使用实际词语而非任意字符组合。

长度限制：含非 ASCII 字符时不超过 15 个字符；纯 ASCII 时空格分隔片段不超过 7 个。

weight

int

是

热词权重。常用值：4。

取值范围：\[1, 5\]。

如果效果不明显，可以适当增加权重，但权重过大可能产生负面效果，导致其他词语识别不准确。

lang

str

否

待识别音频的语言代码。设置后，系统将对指定语种进行热词识别增强。如果无法提前确定语种，可不设置，模型会自动识别语种。

取值范围（因模型而异）：

-   Paraformer：
    
    -   zh: 中文
        
    -   en: 英文
        
    -   ja: 日语
        
    -   yue: 粤语
        
    -   ko: 韩语
        
    -   de：德语
        
    -   fr：法语
        
    -   ru：俄语
        
-   Fun-ASR：
    
    -   zh: 中文
        
    -   en: 英文
        
    -   ja: 日语
        

## 示例代码

### 创建热词列表

```
import os
import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 未配置环境变量时，将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace='{WorkspaceId}',
    region='cn-beijing',
)

prefix = 'testpfx'
target_model = "fun-asr"

my_vocabulary = [
    {"text": "赛德克巴莱", "weight": 4}
]

# 创建热词
vocabulary = client.audio.vocabularies.create(
    prefix=prefix,
    target_model=target_model,
    vocabulary=my_vocabulary)

print(f"热词列表ID为：{vocabulary.vocabulary_id}")
```

### 批量查询热词列表

```
import json
import os
import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 未配置环境变量时，将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace='{WorkspaceId}',
    region='cn-beijing',
)

result = client.audio.vocabularies.list()
print(f"热词列表：{json.dumps(result.vocabularies)}")
```

### 查询热词列表

```
import json
import os
import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 未配置环境变量时，将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace='{WorkspaceId}',
    region='cn-beijing',
)

# 查询时替换为实际的热词列表ID
vocabulary = client.audio.vocabularies.get("vocab-testpfx-xxx")
print(f"热词列表：{json.dumps(vocabulary.vocabulary)}")
```

### 更新热词列表

```
import os
import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 未配置环境变量时，将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace='{WorkspaceId}',
    region='cn-beijing',
)

my_vocabulary = [
    {"text": "赛德克巴莱", "weight": 4, "lang": "zh"}
]
# 替换为实际的热词列表ID
result = client.audio.vocabularies.update("vocab-testpfx-xxx", vocabulary=my_vocabulary)
print(f"更新状态：{result.status}")
```

### 删除热词列表

```
import os
import dashscope

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 未配置环境变量时，将下行替换为：api_key="sk-xxx"
client = dashscope.Client(
    api_key=os.environ.get('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。
    workspace='{WorkspaceId}',
    region='cn-beijing',
)

# 替换为实际的热词表ID
result = client.audio.vocabularies.delete("vocab-testpfx-xxxx")
print(f"删除状态：{result.status}")
```
