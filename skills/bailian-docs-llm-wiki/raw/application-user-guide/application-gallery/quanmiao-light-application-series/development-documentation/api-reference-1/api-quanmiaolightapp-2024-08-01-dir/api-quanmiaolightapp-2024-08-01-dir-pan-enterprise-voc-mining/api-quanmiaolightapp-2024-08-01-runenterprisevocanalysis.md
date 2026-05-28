# RunEnterpriseVocAnalysis - 在线企业VOC分析

企业VOC分析。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunEnterpriseVocAnalysis)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunEnterpriseVocAnalysis)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

quanmiaolightapp:RunEnterpriseVocAnalysis

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runEnterpriseVocAnalysis HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

workspaceId

string

是

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

taskDescription

string

否

任务描述

你是一名经验丰富的数据分析师，擅长从文本评论中提取结构化信息。你需要从用户评论列表中识别和提取出与以下四个维度相关的关键词和短语： 索引：输入评论JSON数组中的索引（从零开始）表示针对该条索引抽取的维度。 购买动机：描述用户购买产品的原因、需求或驱动力的关键词或短语。 未满足需求点：用户在使用产品过程中提到的未满足需求或问题的关键词或短语。 使用场景：用户提到的具体使用场景、使用方式或环境的关键词或短语。 正负面观点：明确表示用户对产品或服务的正面或负面看法的关键词或短语。

modelId

string

否

模型 ID

qwen-max

extraInfo

string

否

额外信息(业务补充信息)

额外信息

outputFormat

string

否

输出格式

按照如下格式输出：{"text1": "xxxx", "text2": "xxxx"}

content

string

否

内容

这是一段需要分析的文本内容

tags

array<object>

否

业务标签体系

object

否

标签体系列表

tagName

string

否

标签名称

标签名称

tagDefinePrompt

string

否

标签定义提示词

标签定义提示词

filterTags

array<object>

否

过滤标签

object

否

tagName

string

否

标签名称

标签名称

tagDefinePrompt

string

否

标签定义提示词

标签定义提示词

apiKey

string

否

百炼 APIKEY

sk-xxxx

akProxy

string

否

none

none

sourceTrace

boolean

否

是否启用溯源（启用溯源时不支持自定义 outputformat）

true

positiveFilter

boolean

否

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应

header

object

消息头

errorCode

string

错误码 code

AccessForbidden

errorMessage

string

错误描述

错误信息

event

string

事件

task-finished

sessionId

string

会话唯一标识

xxxx

taskId

string

任务唯一标识

xxxx

traceId

string

全链路唯一标识

xxxxx

payload

object

消息体

output

object

输出结果

text

string

输出摘要文本

输出摘要文本

filterResult

object

过滤结果

filterResults

array<object>

过滤结果列表

object

tagName

string

过滤标签命中的标签

过滤标签命中的标签

tagValue

string

命中的值（是、否）

是

hit

boolean

是否命中

true

reasonContent

string

推理模型返回的推理内容

usage

object

token 消耗

inputTokens

integer

输入 token

100

outputTokens

integer

输出 token

100

totalTokens

integer

总 token

200

requestId

string

Id of the request

49483FFC-0CB9-5163-8D3E-234E276E6DA8

## 示例

正常返回示例

`JSON`格式

```
{
  "header": {
    "errorCode": "AccessForbidden",
    "errorMessage": "错误信息",
    "event": "task-finished",
    "sessionId": "xxxx",
    "taskId": "xxxx",
    "traceId": "xxxxx"
  },
  "payload": {
    "output": {
      "text": "输出摘要文本\n\n",
      "filterResult": {
        "filterResults": [
          {
            "tagName": "过滤标签命中的标签",
            "tagValue": "是",
            "hit": true
          }
        ]
      },
      "reasonContent": ""
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
  },
  "requestId": "49483FFC-0CB9-5163-8D3E-234E276E6DA8"
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action , Please check the assignment of the workspaceId.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/RunEnterpriseVocAnalysis#workbench-doc-change-demo)。
