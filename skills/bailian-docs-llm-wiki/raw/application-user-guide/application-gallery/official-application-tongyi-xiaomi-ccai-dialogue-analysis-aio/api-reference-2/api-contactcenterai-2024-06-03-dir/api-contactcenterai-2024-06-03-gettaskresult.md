# GetTaskResult - 通过任务ID获取离线任务分析结果

通过任务ID获取离线任务对话分析结果。应用调用支持 HTTPS调用来完成客户的响应。

## 接口说明

请确保在使用该接口前，已充分了解通义晓蜜 CCAI-对话分析 AIO 产品的收费方式和价格。

前提条件

1.  已开通通义晓蜜 CCAI-对话分析 AIO 服务。
    
2.  已创建应用：应用中心完成通义晓蜜 CCAI-对话分析 AIO 应用创建，并获取到 APP-ID 和 WORKSPACE-ID：[获取 APP-ID 和 WORKSPACE-ID](https://help.aliyun.com/zh/model-studio/developer-reference/obtain-api-key-app-id-and-workspace-id?spm=openapi-amp.newDocPublishment.0.0.310f281ffuUD8V)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/GetTaskResult)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/ContactCenterAI/2024-06-03/GetTaskResult)

## **授权信息**

当前API暂无授权信息透出。

## 请求语法

```
GET /ccai/app/getTaskResult HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

taskId

string

否

任务 ID

20240905-\*\*\*\*\*\*\*\*-93E9-5D45-B4EF-045743A34071

requiredFieldList

array

否

string

否

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

Schema of Response

data

object

返回数据。

taskId

string

任务 ID。

20240905-\*\*\*\*\*\*\*\*-93E9-5D45-B4EF-045743A34071

text

string

应用返回的结果。

对话中没有发现客服故意套取客户隐私信息的行为

taskErrorMessage

string

taskStatus

string

任务状态。QUEUE-排队中，FINISH-已完成，ERROR-任务出错

FINISH

asrResult

array<object>

object

begin

integer

emotionValue

integer

end

integer

role

string

speechRate

integer

words

string

roleName

string

extra

string

ragStatus

string

ragResult

string

usage

object

rag

object

dialogSummary

object

inputTokens

integer

outputTokens

integer

invokeCount

integer

adaptive

object

inputTokens

integer

outputTokens

integer

invokeCount

integer

ragErrorMessage

string

requestId

string

请求 id

968A8634-FA2C-5381-9B3E-C552DED7E8BF

success

string

请求是否成功

True

## 示例

正常返回示例

`JSON`格式

```
{
  "data": {
    "taskId": "20240905-********-93E9-5D45-B4EF-045743A34071\n",
    "text": "对话中没有发现客服故意套取客户隐私信息的行为",
    "taskErrorMessage": "",
    "taskStatus": "FINISH",
    "asrResult": [
      {
        "begin": 0,
        "emotionValue": 0,
        "end": 0,
        "role": "",
        "speechRate": 0,
        "words": "",
        "roleName": ""
      }
    ],
    "extra": "",
    "ragStatus": "",
    "ragResult": "",
    "usage": {
      "rag": {
        "dialogSummary": {
          "inputTokens": 0,
          "outputTokens": 0,
          "invokeCount": 0
        },
        "adaptive": {
          "inputTokens": 0,
          "outputTokens": 0,
          "invokeCount": 0
        }
      }
    },
    "ragErrorMessage": ""
  },
  "requestId": "968A8634-FA2C-5381-9B3E-C552DED7E8BF",
  "success": "True"
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

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

500

CCAI.InternalError

The request processing has failed due to some unknown error, exception or failure.

系统内部错误，请稍后重试

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

User not authorized to operate on the specified resource %s .

该用户未被授权可操作指定资源

429

Ccai.Throttling.Qps

Trigger current QPS limit, pay API please buy higher QPS, free API if you have special requirements, please contact us through the DingTalk group (62730018475).

无效错误码，后续下线

访问[错误中心](https://api.aliyun.com/document/ContactCenterAI/2024-06-03/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/ContactCenterAI/2024-06-03/GetTaskResult#workbench-doc-change-demo)。
