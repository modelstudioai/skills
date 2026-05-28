# 文本排序

检索系统在“召回”阶段为保证效率，返回的结果可能不够精准。排序模型能对召回的文档进行二次精准排序，确保将与用户查询最相关的结果排在最前，有效提升应用准确率。

## 模型概览

**重要**

gte-rerank模型将于2026年05月30日下线，推荐使用qwen3-rerank模型替代。详情请参见[官网公告](https://www.aliyun.com/notice/118217)。

**模型名称**

**最大文档数**

**单条最大输入Token**

**请求最大输入Token**

**语种支持**

**应用场景**

qwen3-vl-rerank

文本：100

图片：40

视频：4

8,000

120,000

中、英、日、韩、法、德等33种主流语言

-   图像聚类
    
-   跨模态搜索
    
-   图片检索
    

qwen3-rerank

500

4,000

中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄罗斯语等100+主流语种

-   文本语义检索
    
-   RAG应用
    

gte-rerank-v2

30,000

中、英、日、韩、泰语、西、法、葡、德、印尼语、阿拉伯语等50余语种

-   **单条最大输入Token**：每个Query或Document的最大Token数量。输入内容超长将被截断。API仅基于截断后的内容计算，这可能导致排序结果不准确。
    
-   **单次请求最大文档数**：单次请求允许的最大文档数量。对于 qwen3-vl-rerank 模型，该限制会根据文档类型（文本、图片、视频、混合模态）的不同而有所差异。
    
-   **请求最大输入Token**：计算公式为 `Query Tokens × Document 数量 + Document Tokens 总和`，该值不得超过请求最大输入Token。
    

### **输入格式限制：**

**模型**

**图片**

**视频**

qwen3-vl-rerank

JPEG, PNG, WEBP, BMP, TIFF, ICO, DIB, ICNS, SGI（支持URL或Base64）

MP4, AVI, MOV（仅支持URL）

## **前提条件**

您需要已[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)并[配置API Key到环境变量DASHSCOPE\_API\_KEY](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过SDK调用，还需要[安装DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。

## **HTTP调用**

不同模型使用不同的API接口：

-   **qwen3-rerank**：`POST https://dashscope.aliyuncs.com/compatible-api/v1/reranks`
    
-   **qwen3-vl-rerank / gte-rerank-v2**：`POST https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank`
    

> 两种接口的请求体结构和响应格式不同，请参考对应模型的请求示例和响应示例。

### **请求**

#### qwen3-rerank

```
curl --request POST \
  --url https://dashscope.aliyuncs.com/compatible-api/v1/reranks \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
        "model": "qwen3-rerank",
        "documents": [
                "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序",
                "量子计算是计算科学的一个前沿领域",
                "预训练语言模型的发展给文本排序模型带来了新的进展"
        ],
        "query": "什么是文本排序模型",
        "top_n": 2,
        "instruct": "Given a web search query, retrieve relevant passages that answer the query."
}'
```

## qwen3-vl-rerank

文本查询

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3-vl-rerank",
    "input":{
         "query": {"text": "什么是文本排序模型"},
         "documents": [
            {"text": "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序"},
            {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
            {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"}
         ]
    },
    "parameters": {
        "return_documents": true,
        "top_n": 2,
        "fps": 1.0
    }
}'
```

图片查询

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen3-vl-rerank",
    "input":{
         "query": {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
         "documents": [
            {"text": "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序"},
            {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
            {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"}
         ]
    },
    "parameters": {
        "return_documents": true,
        "top_n": 2,
        "fps": 1.0
    }
}'
```

## gte-rerank-v2

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "gte-rerank-v2",
    "input":{
         "query": "什么是文本排序模型",
         "documents": [
         "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序",
         "量子计算是计算科学的一个前沿领域",
         "预训练语言模型的发展给文本排序模型带来了新的进展"
         ]
    },
    "parameters": {
        "return_documents": true,
        "top_n": 2
    }
}'
```

#### **请求头（Headers）**

**Content-Type** `_string_` **（必选）**

请求内容类型。此参数必须设置为`application/json`。

**Authorization** `_string_`**（必选）**

请求身份认证。接口使用阿里云百炼API Key进行身份认证。示例值：Bearer sk-xxxx。

#### **请求体（Request Body）**

**model** `_string_`**（必选）**

模型名称。支持的模型：qwen3-rerank、gte-rerank-v2、qwen3-vl-rerank。

**input** `_object_` **（必选）**

输入内容。

> 当使用 `qwen3-rerank` 模型时，无需使用 `input` 对象参数。此时，`query` 和 documents 参数需与 `model` 等参数位于同一层级。

**属性**

**query** `_string | object_`**（必选）**

查询内容。最大长度不能超过4,000个Token。

当使用`qwen3-vl-rerank`模型时，`query`支持以下两种格式：

-   字符串格式：直接传入文本字符串，例如`"query": "什么是文本排序模型"`。
    
-   对象格式：传入字典指定模态类型和值，格式为`{"模态类型": "输入内容"}`。支持`text`和`image`两种模态类型。
    
    -   文本查询：`"query": {"text": "什么是文本排序模型"}`
        
    -   图片查询：`"query": {"image": "图片URL或Base64"}`
        

**documents** `_array_`**（必选）**

待排序的候选文档列表。每个元素是一个字符串。

当使用`qwen3-vl-rerank`模型时，每个元素是一个字典或者字符串，用于指定内容的类型和值。格式为{"模态类型": "输入字符串或图像、视频url"}。支持`text`, `image`, `video`三种模态类型。

-   文本：key为`text`。value为字符串形式。也可不通过dict直接传入字符串。
    
-   图片：key为`image`。value可以是公开可访问的URL，或Base64编码的Data URI。Base64格式为 `data:image/{format};base64,{data}`，其中 `{format}` 是图片格式（如 `jpeg`、`png`），`{data}` 是Base64编码字符串。
    
-   视频：key为`video`，value必须是公开可访问的URL。
    

**parameters** `_object_`**（可选）**

可选参数。

> 当使用 `qwen3-rerank` 模型时，无需使用 `parameters` 对象参数。此时，`top_n` 和 `instruct` 参数需与 `model` 等参数位于同一层级。

**属性**

**top\_n** `_int_`**（可选）**

返回排序后的top\_n个文档。默认返回全部文档。如果指定的值大于文档总数，将返回全部文档。

**return\_documents** `_bool_`**（可选）**

是否在排序结果中返回文档原文。默认值`false`，以减少网络传输开销。支持的模型：`gte-rerank-v2`、`qwen3-vl-rerank`。

**instruct** `_string_` **可选**

添加自定义排序任务类型说明，仅在使用 `qwen3-rerank` 及`qwen3-vl-rerank`模型时生效。通过该参数可以指导模型采用不同的排序策略，例如：

-   **问答检索任务（默认）**：`"Given a web search query, retrieve relevant passages that answer the query."`
    
    -   侧重点：寻找问题的答案。模型会优先评估文档是否解答了Query中的问题。
        
    -   示例：对于Query“如何预防感冒？”，文档“勤洗手是预防感冒的有效方法”会获得高分；而文档“感冒是一种常见疾病”虽然主题相关，但因未提供答案，得分会显著更低。
        
-   **语义相似度排序任务**：`"Retrieve semantically similar text."`
    
    -   侧重点：判断语义的等价性。模型会评估Query和文档的核心含义是否一致，而不管具体措辞或句式。
        
    -   示例：在FAQ场景中，用户Query“如何修改密码？”与候选问题“忘记密码怎么办？”在语义上高度相似，应获得高分。模型会关注两者是否指向同一个用户意图。
        

建议使用英文撰写。如不指定该参数，将默认按问答检索任务进行排序。更多任务指令可参考[模型仓库](https://github.com/QwenLM/Qwen3-Embedding/blob/main/evaluation/task_prompts.json)中的示例。

**fps** `_float_` **可选**

仅`qwen3-vl-rerank`模型支持此参数。控制视频的帧数，比例越小，实际抽取的帧数越少，范围为 \[0,1\]。默认值为1.0。

### **响应**

## 成功响应

### qwen3-rerank

```
{
    "object": "list",
    "results": [
        {
            "index": 0,
            "relevance_score": 0.9334521178273196
        },
        {
            "index": 2,
            "relevance_score": 0.34100082626411193
        }
    ],
    "model": "qwen3-rerank",
    "id": "85ba5752-1900-47d2-8896-23f99b13f6e1",
    "usage": {
        "total_tokens": 79
    }
}
```

### qwen3-vl-rerank / gte-rerank-v2

```
{
    "output": {
        "results": [
            {
                "document": {
                    "text": "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序"
                },
                "index": 0,
                "relevance_score": 0.9334521178273196
            },
            {
                "document": {
                    "text": "预训练语言模型的发展给文本排序模型带来了新的进展"
                },
                "index": 2,
                "relevance_score": 0.34100082626411193
            }
        ]
    },
    "usage": {
        "total_tokens": 79
    },
    "request_id": "85ba5752-1900-47d2-8896-23f99b13f6e1"
}
```

## 失败响应

在访问请求出错的情况下，输出的结果中会通过`code`和`message`指明出错原因。

```
{
    "code":"InvalidApiKey",
    "message":"Invalid API-key provided.",
    "request_id":"fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1"
}
```

**request\_id** `_string_`

请求唯一标识。可用于请求明细溯源和问题排查。

**output** `_object_`

任务输出信息。

> 当使用 `qwen3-rerank` 模型时，响应中不包含 `output` 对象，`results` 直接位于响应顶层。

**属性**

**results** `_array_`

排序结果列表。按 `relevance_score` 从高到低排列。

**属性**

**document** `_dict_`

文档原文对象。仅在请求参数 `return_documents` 为 `true` 时返回。结构为 `{"text": "文档原文"}`。

**index** `_int_`

表示该结果对应于输入 `documents` 列表中的原始索引位置。

**relevance\_score** `double`

该文档与查询的语义相关性得分，取值范围为 0.0 到 1.0。分数越高，相关性越强。

**说明**

此分数为当前请求中的相对分数，主要用于对本次请求内的文档排序，不可作为跨请求比较的绝对值。

**usage** `_object_`

输出信息统计。

**属性**

**total\_tokens** `_int_`

本次请求消耗的总 Token 数量。

**code** `_string_`

请求失败的错误码。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

**message** `_string_`

请求失败的详细信息。请求成功时不会返回此参数，详情请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)。

## **SDK调用**

### **调用示例**

以下示例展示了调用文档排序模型API的代码示例。

> SDK 的参数命名与HTTP接口基本一致，参数结构进行了一定封装。比如 HTTP 使用嵌套的 `input` 和 `parameters` 结构，但SDK 使用扁平参数。请在开发时注意区分。

Python

```
import dashscope
from http import HTTPStatus

def text_rerank():
    resp = dashscope.TextReRank.call(
        model="qwen3-rerank",
        query="什么是文本排序模型",
        documents=[
            "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序",
            "量子计算是计算科学的一个前沿领域",
            "预训练语言模型的发展给文本排序模型带来了新的进展"
        ],
        top_n=10,
        return_documents=True,
        instruct="Given a web search query, retrieve relevant passages that answer the query."
    )
    if resp.status_code == HTTPStatus.OK:
        print(resp)
    else:
        print(resp)

if __name__ == '__main__':
    text_rerank()
```

以下示例展示了使用`qwen3-vl-rerank`模型进行多模态排序（以图片作为查询）的代码示例。

Python

```
import dashscope
from http import HTTPStatus
import json

def vl_rerank():
    resp = dashscope.TextReRank.call(
        model="qwen3-vl-rerank",
        query={"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
        documents=[
            {"text": "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序"},
            {"image": "https://img.alicdn.com/imgextra/i3/O1CN01rdstgY1uiZWt8gqSL_!!6000000006071-0-tps-1970-356.jpg"},
            {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"}
        ],
        top_n=2,
        return_documents=True
    )
    if resp.status_code == HTTPStatus.OK:
        print(json.dumps(resp, default=str, ensure_ascii=False, indent=4))
    else:
        print(resp)

if __name__ == '__main__':
    vl_rerank()
```

### **输出示例**

**说明**

SDK对原始HTTP响应进行了封装，成功时会固定返回`code`和`message`字段，值为空字符串。

```
{
    "status_code": 200,
    "request_id": "4b0805c0-6b36-490d-8bc1-4365f4c89905",
    "code": "",
    "message": "",
    "output": {
        "results": [
            {
                "index": 0,
                "relevance_score": 0.9334521178273196,
                "document": {
                    "text": "文本排序模型广泛用于搜索引擎和推荐系统中，它们根据文本相关性对候选文本进行排序"
                }
            },
            {
                "index": 2,
                "relevance_score": 0.34100082626411193,
                "document": {
                    "text": "预训练语言模型的发展给文本排序模型带来了新的进展"
                }
            }
        ]
    },
    "usage": {
        "total_tokens": 79
    }
}
```

## **错误码**

如果模型调用失败并返回报错信息，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行解决。

## 限流

模型限流触发条件请参考[限流](https://help.aliyun.com/zh/model-studio/rate-limit)。
