# SaveStyleLearningResult - 保存文体学习分析结果

保存自定义文体。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SaveStyleLearningResult)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/SaveStyleLearningResult)

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

aimiaobi:SaveStyleLearningResult

create

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

RewriteResult

string

否

用户修订后内容

用户修订后内容

StyleName

string

否

保存后的文体名称

学习报告

AigcResult

string

否

AIGC 生成的内容

AIGC 生成的内容

CustomTextIdList

array

否

自定义文本素材集合

long

否

1

18

AgentKey

string

否

业务空间唯一标识：AgentKey

xxxxx\_p\_efm

TaskId

string

否

任务 id 和 SSE 接口中的 taskID 保持一致

3f7045e099474ba28ceca1b4eb6d6e21

MaterialIdList

array

否

素材 ID 集合

long

否

1

4

## 返回参数

名称

类型

描述

示例值

object

PlainResult

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Code

string

状态码

NoData

Data

boolean

业务数据

true

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

success

Success

boolean

是否成功：true 成功，false 失败

true

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Code": "NoData",
  "Data": true,
  "HttpStatusCode": 200,
  "Message": "success",
  "Success": true
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
