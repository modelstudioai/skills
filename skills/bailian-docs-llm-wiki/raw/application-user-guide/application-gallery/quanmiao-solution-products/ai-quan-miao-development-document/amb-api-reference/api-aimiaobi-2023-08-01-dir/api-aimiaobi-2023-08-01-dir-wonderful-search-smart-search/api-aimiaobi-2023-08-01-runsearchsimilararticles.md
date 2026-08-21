# RunSearchSimilarArticles - 妙搜-文搜文

妙搜-文搜文。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunSearchSimilarArticles)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunSearchSimilarArticles)

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

aimiaobi:RunSearchSimilarArticles

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /quanmiao/aimiaosou/runSearchSimilarArticles HTTP/1.1
```

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

xxxx

ChatConfig

object

否

通信配置参数

SearchParam

object

否

搜索配置参数

SearchSources

array<object>

否

搜索源

object

否

Code

string

否

搜索源类型：

-   SystemSearch：系统内置搜索
    
-   CustomSemanticSearch：自建语义索引搜索
    
-   ThirdSearch：三方 API 搜索
    

SystemSearch

Name

string

否

搜索源名称（非必选）

互联网搜索

DatasetName

string

否

搜索源唯一标识

QuarkCommonNews

CategoryUuids

array

否

string

否

Tags

array

否

string

否

Extend1

string

否

Extend2

string

否

Extend3

string

否

CreateTimeStart

integer

否

CreateTimeEnd

integer

否

StartTime

integer

否

EndTime

integer

否

DocUuids

array

否

string

否

DocIds

array

否

string

否

DocTypes

array

否

string

否

Title

string

否

文章标题

标题

DocType

string

否

文档类型

html

Url

string

是

文章地址

https://xxx/xxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

BaseLlmResponse

Header

object

响应头

ErrorCode

string

错误码

错误码

ErrorMessage

string

错误信息

错误信息

Event

string

SSE 事件。task-started：开始，task-finished：结束，task-failed：失败

task-started

SessionId

string

会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

TaskId

string

任务 ID

3f7045e099474ba28ceca1b4eb6d6e21

Payload

object

响应体

Output

object

输出

Text

string

文本生成结果

文本生成结果

Articles

array<object>

文章列表

object

DocUuid

string

文章 id

a26c2c1

SearchSourceName

string

搜索源名称

互联网搜索

PubTime

string

发布时间

2025-01-16 18:07:22

Source

string

文章来源

xxx.com

Title

string

标题

标题

Url

string

地址

https://xxx

Summary

string

摘要

xxx

DocId

string

文档-自定义的唯一 ID

xxx

CategoryUuid

string

Extend1

string

Extend2

string

Extend3

string

Tags

array

string

SearchSource

string

SearchSourceType

string

DocType

string

Usage

object

镜像是否已经运行在 ECS 实例中。取值范围：

instance：镜像处于运行状态，有 ECS 实例使用。 none：镜像处于闲置状态，暂无 ECS 实例使用。

InputTokens

integer

输入 Token 数量

81

OutputTokens

integer

输出 Token 数量

9

TotalTokens

integer

总 Token 数量

50

RequestId

string

请求 Id

3f7045e099474ba28ceca1b4eb6d6e21

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "错误码",
    "ErrorMessage": "错误信息",
    "Event": "task-started",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "TaskId": "3f7045e099474ba28ceca1b4eb6d6e21"
  },
  "Payload": {
    "Output": {
      "Text": "文本生成结果",
      "Articles": [
        {
          "DocUuid": "a26c2c1",
          "SearchSourceName": "互联网搜索",
          "PubTime": "2025-01-16 18:07:22",
          "Source": "xxx.com",
          "Title": "标题",
          "Url": "https://xxx",
          "Summary": "xxx",
          "DocId": "xxx",
          "CategoryUuid": "",
          "Extend1": "",
          "Extend2": "",
          "Extend3": "",
          "Tags": [
            ""
          ],
          "SearchSource": "",
          "SearchSourceType": "",
          "DocType": ""
        }
      ]
    },
    "Usage": {
      "InputTokens": 81,
      "OutputTokens": 9,
      "TotalTokens": 50
    }
  },
  "RequestId": "3f7045e099474ba28ceca1b4eb6d6e21"
}
```

## 错误码

   

**HTTP status code**

**错误码**

**错误信息**

**描述**

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/RunSearchSimilarArticles#workbench-doc-change-demo)。
