# AnalyzeImage - 图片内容分析

通过通义晓蜜CCAI-对话分析AIO应用进行图片内容分析。具体包括以下场景：水印检测。应用调用支持 HTTP 调用来完成客户的响应。

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

前提条件

1.  已开通通义晓蜜 CCAI-对话分析 AIO 服务。
2.  已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：[获取 APP-ID 和 WORKSPACE-ID](https://help.aliyun.com/zh/model-studio/developer-reference/obtain-api-key-app-id-and-workspace-id?spm=openapi-amp.newDocPublishment.0.0.2eb8281f6Dxglg)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/AnalyzeImage)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/AnalyzeImage)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/ccai/app/{appId}/analyzeImage HTTP/1.1
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

是

必填。是否流式：true，流式返回答案；false，全量返回答案。

false

imageUrls

array

否

图片地址列表

string

否

图片地址列表

https://img.123.com/1.jppg

resultTypes

array

否

任务类型列表

string

否

watermark-图片水印分析

watermark

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

请求 id

9\*\*\*\*\*-AE0D-5EE3-B1AF-48632CB0831C

success

boolean

请求是否成功

True

text

string

应用返回的结果。

\[{\\"num\\":\\"1\\",\\"isHit\\":\\"false\\",\\"remarks\\":\\"无水印\\"}\]

finishReason

string

如果是流式输出，正在生成时为 null，生成结束时如果由于停止 token 导致则为 stop。

stop

inputTokens

string

输入 Token 数量

1000

outputTokens

string

输出 Token 数量

2000

totalTokens

string

Tokens 总量

3000

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "9*****-AE0D-5EE3-B1AF-48632CB0831C",
  "success": true,
  "text": "[{\\\"num\\\":\\\"1\\\",\\\"isHit\\\":\\\"false\\\",\\\"remarks\\\":\\\"无水印\\\"}]",
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

CCAI.IllegalPermission.NoAuth

User not authorized to operate on the specified resource.

该用户未被授权可操作指定资源

403

CCAI.ParamNotfound.MissParam

Parameter verification failed, The specified parameter %s is missing.

参数校验失败，指定参数缺失。

403

CCAI.TenantPermission.NoAuth

The current account does not have the permission to specify the business space. Please authorize the business space permission.

当前账号没有指定业务空间的权限，请进行业务空间权限授权。

500

CCAI.InternalError

The request processing has failed due to some unknown error, exception or failure.

系统内部错误，请稍后重试

访问[错误中心](< https://api.aliyun.com/document/ContactCenterAI/2024-06-03/errorCode>)查看更多错误码。
