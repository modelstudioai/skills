# GetTask - 查询汽车销售服务洞察任务状态和结果

查询汽车销售服务洞察任务的状态和结果。

## 前提条件

已开通服务并[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。

**说明**当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](raw/model-api-reference/more-about-models/generate-temporary-api-key.md)。

与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。

使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。

## 接入地址

```
https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
```

## 请求方式

POST

## 请求头

```
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Content-Type: application/json
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

model

string

是

定义业务类型，固定为`tingwu-automotive-service-insights`

tingwu-automotive-service-insights

input

object

是

传入相关业务参数

input.task

string

是

定义任务类型，固定为`getTask`，表示获取任务结果

getTask

input.dataId

string

是

需要查询的音频任务id，从createTask任务的返回参数中获取

wkb\*\*\*

## 返回参数

**名称**

**类型**

**描述**

**示例值/解析协议**

code

string

错误码

message

string

错误信息

request\_id

string

请求id

f97ee37d-0f9c-9b93-b6bf-bd263a232bf9

usage

object

用量

output

object

业务返回体

output.status

string

任务状态：

-   0：成功
    
-   1：进行中
    
-   2：失败
    

0

output.errorCode

string

任务成功提交，但是执行失败（`status`为2时）的错误码

TSC.FileError

output.errorMessage

string

任务成功提交，但是任务执行失败（`status`为2时）的错误信息

"File cannot be read."

output.transcriptionPath

string

语音转文字结果的ossUrl，参见[output.transcriptionPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-api-get-task#760913439awmi)

ossUrl对应的文件内容解析协议参见：

-   [output.transcriptionPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-api-get-task#760913439awmi)
    
-   [output.serviceInsightsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-api-get-task#20d08cc597wbf)
    
-   [output.serviceInsightsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-api-get-task#20d08cc597wbf)
    

output.serviceInsightsPath

string

洞察结果的ossUrl，参见[output.serviceInsightsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-api-get-task#20d08cc597wbf)

output.saleInsightsPath

string

返回分析结果的ossUrl，参见[output.serviceInsightsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-api-get-task#20d08cc597wbf)

### output.transcriptionPath 的解析协议

最外层是一个Object，具体字段如下：

**名称**

**类型**

**描述**

**示例值**

paragraphs

Array

段落列表

paragraphs\[i\].paragraphId

String

段落ID

16987422100275\*\*\*\*\*

paragraphs\[i\].speakerId

String

说话者ID

1

paragraphs\[i\].words

Array

字词列表

paragraphs\[i\].words\[i\].id

Integer

字词编号

10

paragraphs\[i\].words\[i\].sentenceId

Integer

句子ID

1

paragraphs\[i\].words\[i\].start

Integer

开始时间（毫秒）

4970

paragraphs\[i\].words\[i\].end

Integer

结束时间（毫秒）

5560

paragraphs\[i\].words\[i\].text

String

字词文本

我是

示例json如下：

```
{
  "paragraphs": [
    {
      "paragraphId": "16987422100275*******",
      "speakerId": "1",
      "words": [
        {
          "id": 10,
          "sentenceId": 1,
          "start": 4970,
          "end": 5560,
          "text": "您好，"
        },
        {
          "id": 20,
          "sentenceId": 1,
          "start": 5730,
          "end": 6176,
          "text": "我是"
        }
      ]
    }
  ]
}
```

### output.serviceInsightsPath的解析协议

最外层是一个Object，具体字段如下：

**名称**

**类型**

**描述**

**示例值**

serviceInsights\[i\].title

string

服务质检结果的名称，和[入参](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-api-create-task#34b842a7838b1)的serviceInsights.InsightsContents\[i\].title对应

到店迎接-欢迎语

serviceInsights\[i\].matched

boolean

本条服务质检项是否命中

true

serviceInsights\[i\].remarks

string

大模型对本条质检项的分析

销售人员通过询问开启对话，表现出一定的迎接意图。

serviceInsights\[i\].score

string

本条洞察项的最终得分：

-   匹配：置为用户设置的分值
    
-   不匹配：置为零分
    

20

serviceInsights\[i\].matchedSentenceIds

list\[\]

命中该质检项的原始对话，在原文中的句子id

\[1, 2, 3\]

示例json如下：

```
"serviceInsights": [
    {
        "title": "到店迎接-欢迎语",
        "matched": true,
        "remarks": "销售人员通过询问开启对话，表现出一定的迎接意图。",
        "matchedSentenceIds": [1, 3, 5]
    },
    {
        "title": "离店送别-客户留资",
        "matched": true,
        "remarks": "销售人员提出加微信的方式以便后续联系。",
        "matchedSentenceIds": [2, 4]
    },
    {
        "title": "到店迎接-饮品提供",
        "matched": false,
        "remarks": "对话中未提及提供饮品的信息。",
        "matchedSentenceIds": []
    }
]
```

### output.saleInsights的解析协议

最外层是一个Object，具体字段如下：

**名称**

**类型**

**描述**

**示例值**

missedSum

int

洞察项未命中个数

5

matchedSum

int

洞察项命中数

10

示例json如下：

```
"saleInsights": {
  "missedSum": 20,
  "matchedSum": 2
}
```

## 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-***' \
--header 'Content-Type: application/json' \
--data '{
  "model": "tingwu-automotive-service-insights",
  "input": {
    "dataId": "***",
    "task": "getTask"
  }
}'
```

## 返回示例

```
{
    "output": {
        "serviceInsightsPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/servInspec/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/11/***?Expires=1752299850&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "saleInsightsPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/saleInspec/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/11/***?Expires=1752299850&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "status": 0,
        "transcriptionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/transcription/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/11/***?Expires=1752299850&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE"
    },
    "usage": {},
    "request_id": "fccef963-ebb4-98f2-9c2b-6bd9f1b9b094"
}
```
