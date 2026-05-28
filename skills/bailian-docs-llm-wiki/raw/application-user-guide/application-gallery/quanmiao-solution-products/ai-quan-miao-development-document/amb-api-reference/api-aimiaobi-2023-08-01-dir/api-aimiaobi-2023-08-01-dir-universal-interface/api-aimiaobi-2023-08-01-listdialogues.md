# ListDialogues - 生成历史列表

在线推理场景的历史记录。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDialogues)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListDialogues)

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

aimiaobi:ListDialogues

list

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

AgentKey

string

是

业务空间唯一标识： [AgentKey](https://help.aliyun.com/zh/model-studio/get-accesskey-appid-and-agentkey)

xxxxx\_p\_efm

TaskId

string

否

任务唯一标识

**说明** TaskId 默认无需填写，系统将自动生成。当后续任务填写的 TaskId 相同时，表示这些任务属于同一组对话。

xxx

StartTime

string

否

开始时间

2024-01-04 11:46:07

EndTime

string

否

结束时间

2024-01-04 11:46:07

DialogueType

integer

否

生成类型：1：创作；2：智搜（默认）

2

Current

integer

否

当前页码

1

Size

integer

否

每页条数：默认 10

10

## 返回参数

名称

类型

描述

示例值

object

响应结果

Code

string

状态码

successful

Current

integer

当前页码

1

Data

array<object>

生成历史列表

Data

object

生成历史

Bot

string

模型生成

xx

CreateTime

string

创建日期

2024-01-04 11:46:07

CreateUser

string

创建者

xx

DialogueType

integer

生成类型：1：创作；2：智搜（默认）

2

TaskId

string

任务 ID

xx

User

string

用户输入

x

HttpStatusCode

integer

http 状态码

200

Message

string

错误说明

successful

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Size

integer

每页记录数

10

Success

boolean

是否成功：true 成功，false 失败

true

Total

integer

总记录数

100

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "successful",
  "Current": 1,
  "Data": [
    {
      "Bot": "xx",
      "CreateTime": "2024-01-04 11:46:07",
      "CreateUser": "xx",
      "DialogueType": 2,
      "TaskId": "xx",
      "User": "x"
    }
  ],
  "HttpStatusCode": 200,
  "Message": "successful",
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Size": 10,
  "Success": true,
  "Total": 100
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
