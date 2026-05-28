# RunCompletionMessage - 使用原生Prompt调用通义晓蜜CCAI-对话分析AIO应用

支持以Message协议格式调用通义晓蜜CCAI-对话分析AIO应用获取对话摘要、关键信息抽取、质检结果、对话分析结果，应用调用支持 HTTP 调用来完成客户的响应，目前提供普通 HTTP 和 HTTP SSE 两种协议，您可根据自己的需求自行选择。

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

前提条件

1.  已开通通义晓蜜 CCAI-对话分析 AIO 服务。
2.  已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：[获取 APP-ID 和 WORKSPACE-ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/RunCompletionMessage)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/RunCompletionMessage)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/ccai/app/{appId}/completion_message HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

是

子业务空间标识

llm-ik\*\*\*\*\*\*RVYCKzt

appId

string

是

应用 ID

097d65c9c7004f8dad2b454850ac232b

body

object

否

schema of request body

Messages

array<object>

是

模型请求 Message 列表

object

否

Message 结构信息

Content

string

是

prompt 内容

如Role=system ,Content=You are a helpful assistant. Role=user , Content=请阅读以下对话内容，按照要求执行指令任务。

Role

string

是

（通话角色） user-客户 agent-客服 system-系统消息 function-函数

user

ModelCode

string

否

模型规格

tyxmTurbo

Stream

boolean

否

true 则会开启 SSE 响应，默认 false

false

## 返回参数

名称

类型

描述

示例值

object

Response 结构信息

FinishReason

string

如果是流式输出，正在生成时为 null，生成结束时如果由于停止 token 导致则为 stop。

stop

RequestId

string

系统生成的标志本次请求的唯一性 ID

17204B98-xxxx-4F9A-8464-2446A84821CA

Text

string

应用返回的结果。

这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。

## 示例

正常返回示例

`JSON`格式

```
{
  "FinishReason": "stop",
  "RequestId": "17204B98-xxxx-4F9A-8464-2446A84821CA\n",
  "Text": "这段对话似乎是客服与客户之间关于一个服务或产品的讨论，但具体内容难以明确理解，因为对话中的言语比较零散和抽象。",
  "inputTokens": "",
  "outputTokens": "",
  "totalTokens": ""
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

CCAI.Throttling.Qpm

Trigger QPM flow restriction. Please purchase higher QPM for paid API. If free API has special requirements, please contact us through DingTalk group (62730018475).

触发QPM限流，付费API请购买更高QPM，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。

400

CCAI.Throttling.Qps

Trigger current QPS limit, pay API please buy higher QPS, the free API if you have special requirements, please contact us through the DingTalk group (62730018475).

触发限流，付费API请购买更高QPS，免费API如有特殊需求，请通过钉钉群（62730018475）联系我们。

400

CCAI.ParamInvalid.IllegalParamValue

The parameter value of the request API is illegal %s.

请求API的参数不合法

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
