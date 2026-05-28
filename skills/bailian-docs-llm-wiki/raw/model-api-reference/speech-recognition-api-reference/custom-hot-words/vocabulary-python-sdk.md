# 定制热词Python SDK参考

通过Python SDK管理定制热词列表，包括VocabularyService类的方法说明与示例代码。

**用户指南：**[自定义热词](https://help.aliyun.com/zh/model-studio/custom-hot-words-user-guide)。

**重要**

新加坡地域的子业务空间暂不支持热词功能。

## **服务端点**

SDK 默认使用**北京地域**的服务端点。如需切换到其他地域，需在初始化前修改 `dashscope.base_http_api_url`。

### 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

`https://dashscope.aliyuncs.com/api/v1`

### 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

`https://dashscope-intl.aliyuncs.com/api/v1`

**切换到新加坡地域**：

```
import dashscope

# 在代码开头设置
dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
```

**注意**：

-   不同地域的 API Key 不同，请确保使用对应地域的 API Key
    
-   地域配置为全局设置，影响所有 DashScope SDK 的 API 调用
    

## **VocabularyService**

**包路径**：`dashscope.audio.asr.VocabularyService`

**功能**：管理热词列表的生命周期（创建、查询、更新、删除）

### **构造方法**

```
VocabularyService(api_key: str = None, workspace: str = None, model: str = None)
```

未传 `api_key` 时，SDK 使用全局 `dashscope.api_key` 的值。

### **create\_vocabulary() - 创建热词列表**

**方法签名**：

```
def create_vocabulary(
    self,
    target_model: str,
    prefix: str,
    vocabulary: List[dict]) -> str
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

详情请参见[热词字典结构](#热词字典结构)。

**返回值**：

**类型**

**说明**

str

热词列表ID。

### **list\_vocabularies() - 批量查询热词列表**

对应 HTTP API 的 `action: list_vocabulary`（HTTP 用单数，Python 方法名用复数 `list_vocabularies`）。

**方法签名**：

```
def list_vocabularies(
    self,
    prefix: str = None,
    page_index: int = 0,
    page_size: int = 10) -> List[dict]
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

List\[dict\]

热词列表信息数组，每个dict包含 vocabulary\_id、gmt\_create、gmt\_modified、status。

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

### **query\_vocabulary() - 查询热词列表**

**方法签名**：

```
def query_vocabulary(
    self,
    vocabulary_id: str) -> dict
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

dict

热词列表详细信息，包含 vocabulary、target\_model、gmt\_create、gmt\_modified、status。

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
    

### **update\_vocabulary() - 更新热词列表**

**方法签名**：

```
def update_vocabulary(
    self,
    vocabulary_id: str,
    vocabulary: List[dict]) -> None
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

**返回值**：无

### **delete\_vocabulary() - 删除热词列表**

**方法签名**：

```
def delete_vocabulary(
    self,
    vocabulary_id: str) -> None
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

**返回值**：无

## **热词字典结构**

**用于** `**vocabulary**` **参数的字典定义**：

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
        

## **示例代码**

### **创建热词列表**

```
import dashscope
from dashscope.audio.asr import *
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

prefix = 'testpfx'
target_model = "fun-asr"

my_vocabulary = [
    {"text": "赛德克巴莱", "weight": 4}
]

# 创建热词
service = VocabularyService()
vocabulary_id = service.create_vocabulary(
    prefix=prefix,
    target_model=target_model,
    vocabulary=my_vocabulary)

print(f"热词列表ID为：{vocabulary_id}")
```

### **批量查询热词列表**

```
import dashscope
from dashscope.audio.asr import *
import json
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

service = VocabularyService()
vocabularies = service.list_vocabularies()
print(f"热词列表：{json.dumps(vocabularies)}")
```

### **查询热词列表**

```
import dashscope
from dashscope.audio.asr import *
import json
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

service = VocabularyService()
# 查询时替换为实际的热词列表ID
vocabulary = service.query_vocabulary("vocab-testpfx-xxx")
print(f"热词列表：{json.dumps(vocabulary)}")
```

### **更新热词列表**

```
import dashscope
from dashscope.audio.asr import *
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

service = VocabularyService()
my_vocabulary = [
    {"text": "赛德克巴莱", "weight": 4, "lang": "zh"}
]
# 替换为实际的热词列表ID
service.update_vocabulary("vocab-testpfx-xxx", my_vocabulary)
```

### **删除热词列表**

```
import dashscope
from dashscope.audio.asr import *
import os

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

service = VocabularyService()
# 替换为实际的热词表ID
service.delete_vocabulary("vocab-testpfx-xxxx")
```
