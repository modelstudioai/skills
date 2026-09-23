# GetTask - 查询通用服务洞察任务状态和结果

查询通用服务洞察任务的状态和结果。

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

定义业务类型，固定为`tingwu-service-insights`

tingwu-service-insights

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

语音转文字结果的ossUrl，参见[output.transcriptionPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-service-insights-api-get-task#760913439awmi)

ossUrl对应的文件内容解析协议参见：

-   [output.transcriptionPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-service-insights-api-get-task#760913439awmi)
    
-   [output.generalServiceInsightsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-service-insights-api-get-task#20d08cc597wbf)
    
-   [output.generalSaleInsightsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-service-insights-api-get-task#23631e2d69zrj)
    

output.generalServiceInsightsPath

string

洞察结果的ossUrl，参见[output.generalServiceInsightsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-service-insights-api-get-task#20d08cc597wbf)

output.generalSaleInsightsPath

string

返回分析结果的ossUrl，参见

[output.generalSaleInsightsPath的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-service-insights-api-get-task#23631e2d69zrj)

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

### output.generalServiceInsightsPath的解析协议

最外层是一个Object，具体字段如下：

**名称**

**类型**

**描述**

**示例值**

generalServiceInsights\[i\].title

string

服务质检结果的名称，和[入参](raw/_short/tingwu-service-insights-api-create-task-0319988ac9ac5c9b.md)的serviceInsights.InsightsContents\[i\].title对应

到店迎接-欢迎语

generalServiceInsights\[i\].matched

boolean

本条服务质检项是否命中

true

generalServiceInsights\[i\].remarks

string

大模型对本条质检项的分析

销售人员通过询问开启对话，表现出一定的迎接意图。

generalServiceInsights\[i\].score

string

本条洞察项的最终得分：

-   匹配：置为用户设置的分值
    
-   不匹配：置为零分
    

20

generalServiceInsights\[i\].matchedSentenceIds

list\[\]

命中该质检项的原始对话，在原文中的句子id

\[1, 2, 3\]

示例json如下：

```
"generalServiceInsights": [
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

### output.generalSaleInsightsPath的解析协议

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
"generalSaleInsights": {
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
  "model": "tingwu-service-insights",
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
        "generalServiceInsightsPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/servInspec/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/11/***?Expires=1752299850&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "generalSaleInsightsPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/saleInspec/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/11/***?Expires=1752299850&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "status": 0,
        "transcriptionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/transcription/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/11/***?Expires=1752299850&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE"
    },
    "usage": {},
    "request_id": "fccef963-ebb4-98f2-9c2b-6bd9f1b9b094"
}
```
