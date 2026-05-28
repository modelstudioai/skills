# 定制热词HTTP API参考

通过HTTP API管理定制热词列表，包括创建、查询、更新和删除热词列表。

**用户指南：**[自定义热词](https://help.aliyun.com/zh/model-studio/custom-hot-words-user-guide)。

**重要**

新加坡地域的子业务空间暂不支持热词功能。

## **服务端点**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源仅限于中国内地；静态数据存储于您所选的地域。该部署范围支持的地域：华北2（北京）。

`POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，模型推理计算资源在全球范围内动态调度（不含中国内地）；静态数据存储于您所选的地域。该部署范围支持的地域：新加坡。

`POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/customization`

## **请求头**

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将“`<your_api_key>`”替换为实际的API Key。

Content-Type

string

是

请求体的媒体类型，固定为`application/json`。

## **创建热词列表**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/customization`。

新加坡地域和北京地域的API Key不同，详情请参见[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "create_vocabulary",
        "target_model": "fun-asr",
        "prefix": "testpfx",
        "vocabulary": [
          {"text": "赛德克巴莱", "weight": 4}
        ]
    }
}'
```

**model** `_string_` **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型，固定为`create_vocabulary`。

**target\_model** `_string_` **（必选）**

使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。

**prefix** `_string_` **（必选）**

热词列表自定义前缀，仅允许数字和小写字母，长度不超过10个字符。

**vocabulary** `_array[object]_` **（必选）**

热词列表数组。

**属性**

**text** `_string_` **（必选）**

热词文本。

热词文本的语言必须在所选模型的支持范围内，不同模型支持的语言各不相同。

热词用于提升识别的准确率，请使用实际词语而非任意字符组合。

长度限制：含非 ASCII 字符时不超过 15 个字符；纯 ASCII 时空格分隔片段不超过 7 个。

**weight** `_integer_` **（必选）**

热词权重。常用值：4。

取值范围：\[1, 5\]。

如果效果不明显，可以适当增加权重，但权重过大可能产生负面效果，导致其他词语识别不准确。

**lang** `_string_` （可选）

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
        

### **返回体**

```
{
    "output": {
        "vocabulary_id": "vocab-testpfx-5112c3de3705486baxxxxxxx"
    },
    "usage": {
        "count": 1
    },
    "request_id": "aee47022-2352-40fe-acfa-xxxx"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**vocabulary\_id** `_string_`

创建的热词列表ID。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

创建的热词列表数量，固定为1。

## **批量查询热词列表**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/customization`。

新加坡地域和北京地域的API Key不同，详情请参见[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "list_vocabulary",
        "prefix": "testpfx",
        "page_index": 0,
        "page_size": 10
    }
}'
```

**model** `_string_` **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型，固定为`list_vocabulary`。

**prefix** `_string_` （可选）

热词列表自定义前缀，如果设定则只返回指定前缀的热词列表。

**page\_index** `_integer_`

页码索引，从0开始计数。

默认值：0。

**page\_size** `_integer_`

每页包含数据条数。

默认值：10。

### **返回体**

```
{
    "output": {
        "vocabulary_list": [
            {
                "gmt_create": "2026-03-02 18:07:38",
                "gmt_modified": "2026-03-02 18:07:38",
                "status": "OK",
                "vocabulary_id": "vocab-ciotest-8e74bef2accf4xxxxxxxx"
            },
            {
                "gmt_create": "2026-02-27 19:04:48",
                "gmt_modified": "2026-02-28 13:40:40",
                "status": "OK",
                "vocabulary_id": "vocab-sifasr-f483ad46e1844fxxxxxxxx"
            }
        ]
    },
    "usage": {
        "count": 1
    },
    "request_id": "81d51a05-8cdd-45c0-973f-xxxxxxxx"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**vocabulary\_list** `_array[object]_`

查询到的热词列表。

**属性**

**vocabulary\_id** `_string_`

热词列表ID。

**gmt\_create** `_string_`

创建时间。

**gmt\_modified** `_string_`

修改时间。

**status** `_string_`

状态：

-   OK：可调用
    
-   UNDEPLOYED：不可调用。
    

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

固定为1。

## **查询热词列表**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/customization`。

新加坡地域和北京地域的API Key不同，详情请参见[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "query_vocabulary",
        "vocabulary_id": "vocab-testpfx-xxxx"
    }
}'
```

**model** `_string_` **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型，固定为`query_vocabulary`。

**vocabulary\_id** `_string_` **（必选）**

需要查询的热词列表ID。

### **返回体**

```
{
  "output": {
    "gmt_create": "2025-12-19 11:47:11",
    "gmt_modified": "2025-12-19 11:47:11",
    "status": "OK",
    "target_model": "fun-asr",
    "vocabulary": [
      {
        "lang": "zh",
        "text": "赛德克巴莱",
        "weight": 4
      }
    ]
  },
  "usage": {
    "count": 1
  },
  "request_id": "3d461d3f-b2c4-4de5-xxxx"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据。

**属性**

**gmt\_create** `_string_`

创建时间。

**gmt\_modified** `_string_`

修改时间。

**status** `_string_`

状态：

-   OK：可调用
    
-   UNDEPLOYED：不可调用。
    

**target\_model** `_string_`

使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。

**vocabulary** `_array[object]_`

查询到的热词列表。

**属性**

**text** `_string_`

热词文本。

**weight** `_integer_`

热词权重。

**lang** `_string_`

待识别音频语种。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

固定为1。

## **更新热词列表**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/customization`。

新加坡地域和北京地域的API Key不同，详情请参见[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "update_vocabulary",
        "vocabulary_id": "vocab-testpfx-xxx",
        "vocabulary": [
          {"text": "赛德克巴莱", "weight": 4, "lang": "zh"}
        ]
    }
}'
```

**model** `_string_` **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型，固定为`update_vocabulary`。

**vocabulary\_id** `_string_` **（必选）**

需要更新的热词列表ID。

**vocabulary** `_array[object]_` **（必选）**

新的热词列表，将完全替换原有内容。

**属性**

**text** `_string_` **（必选）**

热词文本。

热词文本的语言必须在所选模型的支持范围内，不同模型支持的语言各不相同。

热词用于提升识别的准确率，请使用实际词语而非任意字符组合。

长度限制：含非 ASCII 字符时不超过 15 个字符；纯 ASCII 时空格分隔片段不超过 7 个。

**weight** `_integer_` **（必选）**

热词权重。常用值：4。

取值范围：\[1, 5\]。

如果效果不明显，可以适当增加权重，但权重过大可能产生负面效果，导致其他词语识别不准确。

**lang** `_string_` （可选）

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
        

### **返回体**

```
{
  "output": {},
  "usage": {
    "count": 1
  },
  "request_id": "aee47022-2352-40fe-acfa-xxxx"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据，固定为空。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

更新的热词列表数量，固定为1。

## **删除热词列表**

### **请求体**

以下为北京地域URL，若使用新加坡地域的模型，需将URL替换为：`https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/customization`。

新加坡地域和北京地域的API Key不同，详情请参见[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

```
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "delete_vocabulary",
        "vocabulary_id": "vocab-testpfx-xxx"
    }
}'
```

**model** `_string_` **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** `_object_` **（必选）**

输入参数对象。

**属性**

**action** `_string_` **（必选）**

操作类型，固定为`delete_vocabulary`。

**vocabulary\_id** `_string_` **（必选）**

需要删除的热词列表ID。

### **返回体**

```
{
  "output": {},
  "usage": {
    "count": 1
  },
  "request_id": "aee47022-2352-40fe-acfa-xxxx"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

模型返回的数据，固定为空。

**usage** `_object_`

本次请求用量信息。

**属性**

**count** `_integer_`

删除的热词列表数量，固定为1。
