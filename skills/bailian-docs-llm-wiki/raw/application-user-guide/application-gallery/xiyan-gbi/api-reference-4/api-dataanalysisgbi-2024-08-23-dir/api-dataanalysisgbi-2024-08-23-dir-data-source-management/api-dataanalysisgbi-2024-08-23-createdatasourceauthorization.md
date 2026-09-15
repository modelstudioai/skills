# CreateDatasourceAuthorization - 数据源关联关系授权

创建数据库关联授权，在您指定的业务空间，对指定的数据源进行关联关系的创建，创建后可以对数据源下的表结构进行采集。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/CreateDatasourceAuthorization)

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

dataanalysisgbi:CreateDatasourceAuthorization

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /gbi/create/datasource HTTP/1.1
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

type

integer

是

当前关联数据源的类型

枚举值：

-   1：mysql类型数据源。
-   2：postgresql类型数据源。
-   10：hologress类型数据源。
-   11：mysql类型数据源使用vpc链接。
-   12：postgresql类型数据源使用vpc链接。
-   51：mysql类型虚拟数据源实例。
-   52：postgresql类型虚拟数据源实例。

1

url

string

否

当前创建数据源的 jdbc 链接串地址

jdbc:mysql://rm-2zedvv990c8d8rj8ejo.mysql.rds.aliyuncs.com:3306/gbi\_good\_case

userName

string

否

登录当前数据源的用户名名称

root

password

string

否

登录当前数据源所使用的用户名的密码

password

vdbId

string

否

关联的类型为虚拟数据源时填写，内容为虚拟数据源的实例 id，其他情况无需填写

vdb-E0F693C8-9F72-5830-B81A-696C9D8EBBD1

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

E0F693C8-9F72-5830-B81A-696C9D8EBBD1

## 示例

正常返回示例

`JSON`格式

```
{
  "data": true,
  "errorMsg": "NoAuth",
  "code": "NoAuth",
  "success": true,
  "requestId": "E0F693C8-9F72-5830-B81A-696C9D8EBBD1"
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
