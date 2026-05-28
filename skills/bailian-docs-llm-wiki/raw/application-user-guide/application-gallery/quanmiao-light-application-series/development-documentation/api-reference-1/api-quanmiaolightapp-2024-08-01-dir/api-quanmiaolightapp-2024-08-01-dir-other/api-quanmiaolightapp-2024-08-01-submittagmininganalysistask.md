# SubmitTagMiningAnalysisTask - 提交标签挖掘分析任务

轻应用-标签挖掘。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/SubmitTagMiningAnalysisTask)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/SubmitTagMiningAnalysisTask)

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

quanmiaolightapp:SubmitTagMiningAnalysisTask

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/quanmiao/lightapp/submitTagMiningAnalysisTask HTTP/1.1
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

阿里云百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

modelId

string

否

模型 ID

qwen-max

businessType

string

否

业务类型

clueMining

taskDescription

string

否

任务描述

给你一条待分析文本数据，请你按照标签体系来对数据进行打标。

tags

array<object>

否

标签体系列表

object

否

标签定义

tagName

string

否

标签名称

xxxx

tagDefinePrompt

string

否

标签定义提示词

xxxx

extraInfo

string

否

额外信息

额外信息

outputFormat

string

否

输出格式

请返回如下JSON格式，{"key1":"","key2":""}

url

string

否

待分析的内容文件 URl（每条内容通过换行符分隔，contents、url 二选一）

http://www.example.com/xxxx.txt

contents

array

否

待分析的内容列表（contents、url 二选一）

string

否

待分析的内容

xxx

apiKey

string

否

阿里云百炼 API KEY

batchTask

boolean

否

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

响应

requestId

string

Id of the request

117F5ABE-CF02-5502-9A3F-E56BC9081A64

code

string

错误码

successful

message

string

错误消息

ok

httpStatusCode

integer

http 响应码

200

success

boolean

请求是否成功

true

data

object

任务提交响应

taskId

string

任务 ID

3feb69ed02d9b1a17d0f1a942675d300

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "117F5ABE-CF02-5502-9A3F-E56BC9081A64",
  "code": "successful",
  "message": "ok",
  "httpStatusCode": 200,
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

更多信息，参考[变更详情](https://api.aliyun.com/document/QuanMiaoLightApp/2024-08-01/SubmitTagMiningAnalysisTask#workbench-doc-change-demo)。
