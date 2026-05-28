# GeneralAnalyzeImage - 通用图片分析

通用图片分析。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/GeneralAnalyzeImage)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/GeneralAnalyzeImage)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/ccai/app/{appId}/generalanalyzeImage HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

否

工作空间 ID

llm-ik\*\*\*\*\*\*RVYCKzt

appId

string

否

应用 id。

a070a49c681f4a95a0f0\*\*\*\*\*\*\*\*\*35c

body

object

否

请求体。

stream

boolean

否

必填。是否流式：true，流式返回答案；false，全量返回答案。

true

imageUrls

array

是

图片地址列表

string

否

图片地址列表

https://img.123.com/1.jppg

customPrompt

string

否

自定义指令

Analyze the content in the image

templateIds

array

否

模版 id，模版 id 和 customPrompt 同时存在时，优先使用模版 id

long

是

模版 id，模版 id 和指令任务类型同时存在时，优先使用模版 id

34

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

Id of the request

2D718325-92F9-5588-803B-C4A69A5F0AE1

success

boolean

请求是否成功

True

text

string

应用返回的结果。

这张图片中没有可识别的文本内容。因此，无法进行OCR（光学字符识别）。如果你有其他需求或问题，请告诉我

finishReason

string

如果是流式输出，正在生成时为 null，生成结束时如果由于停止 token 导致则为 stop。

stop

inputTokens

integer

输入 Token 数量

1000

outputTokens

integer

输出 Token 数量

2000

totalTokens

integer

Tokens 总量

3000

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "2D718325-92F9-5588-803B-C4A69A5F0AE1",
  "success": true,
  "text": "这张图片中没有可识别的文本内容。因此，无法进行OCR（光学字符识别）。如果你有其他需求或问题，请告诉我",
  "finishReason": "stop",
  "inputTokens": 1000,
  "outputTokens": 2000,
  "totalTokens": 3000
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

400

CCAI.InvalidParam.NotExist

The specified parameter %s is not valid.

请求API的参数不存在

400

CCAI.ParamInvalid.IllegalParamValue

The parameter value of the request API is illegal %s.

请求API的参数不合法

400

CCAI.Throttling.Qpm

Trigger QPM flow restriction. Please purchase higher QPM for paid API. If free API has special requirements, please contact us through DingTalk group (62730018475).

触发QPM限流，付费API请购买更高QPM，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。

400

CCAI.Throttling.Qps

Trigger current QPS limit, pay API please buy higher QPS, the free API if you have special requirements, please contact us through the DingTalk group (62730018475).

触发限流，付费API请购买更高QPS，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。

403

CCAI.ParamNotfound.MissParam

Parameter verification failed, The specified parameter %s is missing.

参数校验失败，指定参数缺失。

403

CCAI.TenantPermission.NoAuth

The current account does not have the permission to specify the business space. Please authorize the business space permission.

当前账号没有指定业务空间的权限，请进行业务空间权限授权。

403

CCAI.IllegalPermission.NoAuth

User not authorized to operate on the specified resource.

该用户未被授权可操作指定资源

500

CCAI.InternalError

The request processing has failed due to some unknown error, exception or failure.

系统内部错误，请稍后重试

访问[错误中心](< https://api.aliyun.com/document/ContactCenterAI/2024-06-03/errorCode>)查看更多错误码。
