# CreatePdfTranslateTask - 创建pdf文档翻译任务

创建pdf文档翻译任务。提交翻译任务，异步执行翻译过程。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

**前提条件**

-   已开通阿里云百炼服务和通义点金服务。
    
-   获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。
    

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/CreatePdfTranslateTask)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/CreatePdfTranslateTask)

## 授权信息

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    -   对于必选的资源类型，用前面加 \* 表示。
    -   对于不支持资源级授权的操作，用`全部资源`表示。
-   条件关键字：是指云产品自身定义的条件关键字。
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。

操作

访问级别

资源类型

条件关键字

关联操作

dianjin:CreatePdfTranslateTask

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/task/pdfTranslate HTTP/1.1
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

业务空间 id

llm-ik\*\*\*\*\*\*RVYCKzt

body

object

否

请求体。

docId

string

是

文档 id

873648346573245

knowledge

string

否

知识：翻译时参考的领域知识

净利润 (Net Profit) 英文：Net Profit 中文：净利润（通常指扣除所有费用和税后的利润）

libraryId

string

是

文档库 id

cjshcxxxx

modelId

string

是

模型 id

qwen-plus

translateTo

string

否

目标语言：默认为中文

中文

## 返回参数

名称

类型

描述

示例值

object

ResultCode

cost

long

接口的响应耗时

null

data

string

响应数据。返回任务 Id。可使用该 Id 查询任务状态和结果。

3284627354

dataType

string

数据类型

null

errCode

string

错误码

0

message

string

错误信息

ok

requestId

string

请求 id

5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658

success

boolean

是否成功

true

time

string

时间戳

2024-04-24 11:54:34

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 0,
  "data": 3284627354,
  "dataType": null,
  "errCode": 0,
  "message": "ok",
  "requestId": "5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658",
  "success": true,
  "time": "2024-04-24 11:54:34"
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。
