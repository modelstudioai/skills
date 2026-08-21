# ListGeneralConfigs - 通用配置-列表

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListGeneralConfigs)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/ListGeneralConfigs)

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

aimiaobi:ListGeneralConfigs

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

WorkspaceId

string

是

百炼业务空间唯一标识：[获取 workspaceId](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-

PageSize

integer

否

每页条数

1

PageNumber

integer

否

当前页：默认 1

1

## 返回参数

名称

类型

描述

示例值

object

响应结果

Data

array<object>

查询结果

Data

object

查询结果

ConfigKey

string

配置项唯一标识

xxx

ConfigValue

string

配置值

xxx

ConfigValueType

string

配置项类型

CustomSemanticSearch

ConfigDesc

string

配置项说明

xxx

PageNumber

integer

当前页码

1

RequestId

string

请求唯一标识

1813ceee-7fe5-41b4-87e5-982a4d18cca5

Success

boolean

是否成功：true 成功，false 失败

true

Code

string

状态码

NoData

Message

string

错误说明

success

HttpStatusCode

integer

http 状态码

200

TotalCount

integer

总条数

100

PageSize

integer

每页条数

10

## 示例

正常返回示例

`JSON`格式

```
{
  "Data": [
    {
      "ConfigKey": "xxx",
      "ConfigValue": "xxx",
      "ConfigValueType": "CustomSemanticSearch",
      "ConfigDesc": "xxx"
    }
  ],
  "PageNumber": 1,
  "RequestId": "1813ceee-7fe5-41b4-87e5-982a4d18cca5",
  "Success": true,
  "Code": "NoData",
  "Message": "success",
  "HttpStatusCode": 200,
  "TotalCount": 100,
  "PageSize": 10
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2025-11-12

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/AiMiaoBi/2023-08-01/ListGeneralConfigs?updateTime=2025-11-12#workbench-doc-change-demo)
