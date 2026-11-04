# SyncRemoteTables - 从数据源同步数据表

更新当前业务空间所关联的数据表，从远程数据源（虚拟数据源）同步最近的表并关联到您所指定的业务空间。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/SyncRemoteTables)

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

dataanalysisgbi:SyncRemoteTables

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /gbi/update/datasource/tables HTTP/1.1
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

当前请求所使用的阿里云百炼业务空间 id

llm-2v3934xtp49esw64

body

object

否

请求体参数

tableNames

array

是

需要关联的数据表的名称列表

TableName

string

否

数据表名称

user

pullSamples

boolean

否

关联数据表时是否拉取数据样例

true

keepTableNames

array

否

关联数据表时，需要执行"保留并新增"操作的数据表名称列表。

**说明** 保留并新增：对于选择“保留并新增"的表，析言将保留已关联列的信息，同时补充未关联列的信息。

KeepTableName

string

否

数据表名称

order

noModifiedTableNames

array

否

关联数据表时，需要"保留并跳过"的数据表名称列表。

**说明** 保留并跳过：对于选择"保留并跳过"的表，析言将保留所有已关联列的信息，同时不补充任何未关联列的信息。

string

否

数据表名称

user

## 返回参数

名称

类型

描述

示例值

object

Result

data

any

返回信息

true

errorMsg

string

错误描述信息

NoAuth

code

string

错误码

NoAuth

success

boolean

true 接口调用成功，false 接口调用失败

true

requestId

string

请求 id，每次请求都是唯一值，便于后续排查问题

E9563C85-5810-5835-B68C-78580BC3169E

## 示例

正常返回示例

`JSON`格式

```
{
  "data": true,
  "errorMsg": "NoAuth",
  "code": "NoAuth",
  "success": true,
  "requestId": "E9563C85-5810-5835-B68C-78580BC3169E"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

401

NoAuth

Bad Request: Workspace.Illegal.Auth.

当前所使用的账号无所指定业务空间的权限

401

Internal.Error

Bad Request: Internal Error.

内部错误，请联系客服人员排查

访问[错误中心](https://api.aliyun.com/document/DataAnalysisGBI/2024-08-23/errorCode)查看更多错误码。
