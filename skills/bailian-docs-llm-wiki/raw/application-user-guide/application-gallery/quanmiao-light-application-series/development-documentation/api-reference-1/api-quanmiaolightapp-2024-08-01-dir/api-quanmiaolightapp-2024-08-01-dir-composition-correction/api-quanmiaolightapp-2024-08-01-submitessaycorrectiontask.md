# SubmitEssayCorrectionTask - 提交作文批改任务

提交作文批改任务。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/SubmitEssayCorrectionTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/SubmitEssayCorrectionTask)

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

quanmiaolightapp:SubmitEssayCorrectionTask

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/submitEssayCorrectionTask HTTP/1.1
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

xxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

tasks

array<object>

否

批改任务列表

\[{"grade": "高中二年级", "subject": "语文", "totalScore": 60, "question": "请以我的梦想为主题写一篇作文", "answer": "我的梦想是成为一名科学家...", "customId": "task-001"}\]

object

否

子任务

grade

string

否

年级，可选值有： \[ "初中一年级", "初中二年级", "初中三年级", "高中一年级", "高中二年级", "高中三年级" \]

高中二年级

subject

string

否

科目，可选值有：\[ "语文", "英语应用文", "英语读后续写" \]

语文

totalScore

integer

否

总分

60

question

string

否

作文题目

xxx

answer

string

否

作文回答

xxx

otherReviewPoints

string

否

其他审阅要点

xxx

customId

string

否

用户自定义 ID。用来唯一标识每个任务，不能重复

xxxxx

grade

string

否

年级（公共值，优先取子任务中的 grade）

高中二年级

subject

string

否

科目（公共值，优先取子任务中的 subject）

语文

totalScore

integer

否

总分（公共值，优先取子任务中的 totalScore）

60

question

string

否

作文题目（公共值，优先取子任务中的 question）

xxx

otherReviewPoints

string

否

其他评阅要点（公共值，优先取子任务中的 otherReviewPoints ）

xxx

modelId

string

否

模型 ID

可参考模型列表如下：

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

PlainResult

code

string

状态码

NoData

httpStatusCode

integer

http 状态码

200

message

string

错误说明

success

requestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

success

boolean

是否成功：true 成功，false 失败

true

data

object

任务结果

taskId

string

任务 ID

3feb69ed02d9b1a17d0f1a942675d300

## 示例

正常返回示例

`JSON`格式

```
{
  "code": "NoData",
  "httpStatusCode": 200,
  "message": "success",
  "requestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "success": true,
  "data": {
    "taskId": "3feb69ed02d9b1a17d0f1a942675d300"
  }
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

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/SubmitEssayCorrectionTask#workbench-doc-change-demo)。
