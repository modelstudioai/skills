# RunEssayCorrection - 作文批改

作业批改

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunEssayCorrection)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunEssayCorrection)

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

quanmiaolightapp:RunEssayCorrection

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/runEssayCorrection HTTP/1.1
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

[业务空间 ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xxxxxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

grade

string

否

年级

初中一年级

subject

string

否

学科

语文

totalScore

integer

否

总分

60

question

string

否

题目不能为空

xx

answer

string

否

作答内容

xxx

otherReviewPoints

string

否

其他评审要点

xxx

modelId

string

否

模型 ID，默认作文批改模型 1

```
[
                    {
                        "ModelName": "自定义批改模型",
                        "ModelId": "qwen-custom-correction-v1"
                    },
                    {
                        "ModelName": "作文批改模型 1",
                        "ModelId": "qwen-correction-v1"
                    },
                    {
                        "ModelName": "作文批改轻量模型",
                        "ModelId": "qwen-correction-v1-lite"
                    }
                ]
```

qwen-correction-v1

dimensions

array<object>

否

自定义评分维度列表（仅 qwen-custom-correction-v1 模型支持）

\[{"name": "内容完整度", "rubric": "文章内容是否完整，是否涵盖了题目的核心要求", "maxScore": 30}\]

object

否

自定义评分维度

name

string

否

维度名称

内容完整度

rubric

string

否

维度细则描述

文章内容是否完整，是否涵盖了题目的核心要求

maxScore

integer

否

维度满分

30

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

审阅结果

审阅结果

reasoningContent

string

推理思考过程

首先分析文章结构，发现开头、正文、结尾完整...

score

integer

作文审阅得分

50

dimensionResults

array<object>

各维度评分结果（自定义维度模式）

object

维度评分结果

name

string

维度名称

内容完整度

analysis

string

优劣势分析

文章内容较为完整，涵盖了题目的核心要求，但部分论述略显简略。

score

number

得分

25.5

maxScore

number

满分

30

overallComment

string

总评

整体表现良好，建议在论述深度上进一步加强。

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

117F5ABE-CF02-5502-9A3F-E56BC9081A64

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
      "text": "审阅结果\n\n",
      "reasoningContent": "首先分析文章结构，发现开头、正文、结尾完整...",
      "score": 50,
      "dimensionResults": [
        {
          "name": "内容完整度",
          "analysis": "文章内容较为完整，涵盖了题目的核心要求，但部分论述略显简略。",
          "score": 25.5,
          "maxScore": 30
        }
      ],
      "overallComment": "整体表现良好，建议在论述深度上进一步加强。"
    },
    "usage": {
      "inputTokens": 100,
      "outputTokens": 100,
      "totalTokens": 200
    }
  },
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/RunEssayCorrection#workbench-doc-change-demo)。
