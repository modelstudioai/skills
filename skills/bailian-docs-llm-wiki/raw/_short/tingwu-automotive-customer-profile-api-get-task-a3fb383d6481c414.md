# GetTask - 查询购车客户画像任务状态和结果

查询购车客户画像任务状态和结果的API参考。

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

post方法

## 请求头

```
Authorization: Bearer {api-key} // 需将{api-key}替换为实际的API Key
Content-Type: application/json
```

## 获取任务结果

获取购车客户画像分析任务结果。

### 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

model

string

是

定义业务类型，固定为`tingwu-automotive-customer-profile`

tingwu-automotive-customer-profile

input

object

是

传入相关业务参数

input.task

string

是

定义任务类型，固定为`getTask`，表示获取任务结果

input.dataId

string

是

需要查询的音频任务id

wkb\*\*\*

### 返回参数

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

{}

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

"TSC.FileError"

output.errorMessage

string

任务成功提交，但是任务执行失败（`status`为2时）的错误信息

"File cannot be read."

output.customerProfilePath

string

分析结果的ossUrl，参见[output.customerProfilePath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-api-get-task#613d249381m8l)

ossUrl对应的文件内容解析协议参见：

-   [output.customerProfilePath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-api-get-task#613d249381m8l)
    
-   [output.transcriptionPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-api-get-task#760913439awmi)
    
-   [output.identityRecognitionPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-api-get-task#ad71dfc56eizu)
    
-   [output.contentExtractionsPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-api-get-task#33e8cdf060pf3)
    

output.transcriptionPath

string

语音转文字结果的ossUrl，参见[output.transcriptionPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-api-get-task#760913439awmi)

output.identityRecognitionPath

string

角色识别结果ossUrl，参见[output.identityRecognitionPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-api-get-task#ad71dfc56eizu)

output.contentExtractionsPath

string

客户关注点内容提取结果ossUrl的集合（0个或多个），参见[output.contentExtractionsPath 的解析协议](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-api-get-task#33e8cdf060pf3)

#### output.transcriptionPath 的解析协议

最外层是一个Object，具体字段如下：

**名称**

**类型**

**描述**

**示例值**

paragraphs

Array

段落列表

paragraphs\[0\].paragraphId

String

段落ID

16987422100275\*\*\*\*\*

paragraphs\[0\].speakerId

String

说话者ID

1

paragraphs\[0\].words

Array

字词列表

paragraphs\[0\].words\[0\].id

Integer

字词编号

10

paragraphs\[0\].words\[0\].sentenceId

Integer

句子ID

1

paragraphs\[0\].words\[0\].start

Integer

开始时间（毫秒）

4970

paragraphs\[0\].words\[0\].end

Integer

结束时间（毫秒）

5560

paragraphs\[0\].words\[0\].text

String

字词文本

您好，

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

#### output.customerProfilePath 的解析协议

最外层是一个Object，具体字段如下：

**名称**

**类型**

**描述**

**示例值**

saleClueClassify

Object

销售线索分类

saleClueClassify.classify

String

线索类别

B

saleClueClassify.evidence

String

分类依据

客户仅表达想了解SUV，无明确购车意愿

customerNotMentioned

Integer

客户未提及个数

46

tryDriveIntentionEvaluation

Object

试驾意向评估

tryDriveIntentionEvaluation.score

Integer

评分

0

tryDriveIntentionEvaluation.evidence

String

评估依据

客户未提及试驾意愿，仅询问价位

customerConcerned

Integer

客户关注点个数

4

oneSentenceSumUp

String

客户关注点总结

客户关注点：SUV车型、外观设计、内饰质量、具体配置、续航能力、预计到店时间。顾虑点：购车过程中的价格透明度、售后服务、车辆实际性能与宣传是否一致。

示例json如下：

```
{
  "saleClueClassify": {
    "classify": "B",
    "evidence": "客户仅表达想了解SUV，无明确购车意愿"
  },
  "customerNotMentioned": 46,
  "tryDriveIntentionEvaluation": {
    "score": 0,
    "evidence": "客户未提及试驾意愿，仅询问价位"
  },
  "customerConcerned": 4,
  "oneSentenceSumUp": "客户关注点：SUV车型、外观设计、内饰质量、具体配置、续航能力、预计到店时间。\n顾虑点：购车过程中的价格透明度、售后服务、车辆实际性能与宣传是否一致。"
}
```

#### output.identityRecognitionPath 的解析协议

最外层是一个Object，具体字段如下：

**名称**

**类型**

**描述**

**示例值**

identityResults

Array

身份识别结果列表

identityResults\[0\].identity

String

识别的身份

客户

identityResults\[0\].speakerId

String

说话者ID

1

示例json如下：

```
{
  "identityResults": [
      {
          "identity": "客户",
          "speakerId": "1"
      },
      {
          "identity": "销售",
          "speakerId": "2"
      }
  ]
}
```

#### output.contentExtractionsPath 的解析协议

最外层是一个JSONArray，内部的每一个元素如下：

**名称**

**类型**

**描述**

**示例值**

result

String

结果描述

购车费用

matchedSentenceIds

Array<Integer>

匹配的句子ID列表

\[1, 2\]

title

String

标题

用车成本

remarks

String

备注

客户在对话中表达了对购车费用的关注，询问了关于价位的信息

示例json如下：

```
[
  {
    "result": "未提及",
    "matchedSentenceIds": [],
    "title": "产品配置",
    "remarks": "对话中客户与销售的交流未涉及任何具体的产品配置细节，如AR-HUD、电动脚托或脚垫、全景天幕等。"
  },
  {
    "result": "购车费用",
    "matchedSentenceIds": [
      1,
      2
    ],
    "title": "用车成本",
    "remarks": "客户在对话中表达了对购车费用的关注，询问了关于价位的信息。"
  }
]
```

### 请求示例

请求头Authorization中的"sk-\*\*\*"需要替换为真实的阿里云百炼[API Key](https://bailian.console.aliyun.com/?tab=model#/api-key)。

```
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
--header 'Authorization: Bearer sk-***' \
--header 'Content-Type: application/json' \
--data '{
  "model": "tingwu-automotive-customer-profile",
  "input": {
    "dataId": "***",
    "task": "getTask"
  }
}'
```

### 返回示例

```
{
    "output": {
        "identityRecognitionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/idRecog/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/09/2deb5d827f1548a88440b6a40836f239?Expires=***&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "customerProfilePath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/customerProfile/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/09/3880ad6e4b4e4f99a536ac472f083a04?Expires=***&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "contentExtractionsPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/conExtract/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/09/e669817cb93c4a90869d1b733aec8267?Expires=***&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "status": 0,
        "transcriptionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/agentic/prepub/CommonDataField/transcription/1627865205776705/llm-3cx2a3o4n8y45iee/2025/07/09/e565ebbb891e4943a482bda4619081aa?Expires=***&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE"
    },
    "usage": {},
    "request_id": "fb9f5972-0dc0-9d7f-afe6-3120b46419f4"
}
```
