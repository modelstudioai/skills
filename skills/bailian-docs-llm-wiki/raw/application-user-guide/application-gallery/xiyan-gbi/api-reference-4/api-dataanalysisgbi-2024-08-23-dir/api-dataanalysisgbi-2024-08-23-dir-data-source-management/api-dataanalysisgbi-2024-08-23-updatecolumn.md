# UpdateColumn - 修改数据列信息

修改当前指定业务空间中，指定列的信息。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/UpdateColumn)

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

dataanalysisgbi:UpdateColumn

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /gbi/update/column HTTP/1.1
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

columnIdKey

string

是

数据列的唯一标识符 id

column-AAAAAAAAh6cWOUPagYstkg

tableIdKey

string

是

数据表的唯一标识符 id

table-AAAAAAAAFQBwSLJkUj4CYg

chineseName

string

否

数据列的中文名字

学生姓名

description

string

否

数据列的描述

这个列用于表示学生的姓名

enumType

integer

是

当前字段是否为枚举类型，是枚举值类型的基础下，可以补充 enumValues 字段来进行枚举值的补充

枚举值：

-   0：非枚举值类型。
-   1：是枚举值类型。

1

enumValues

array

否

枚举值列表

EnumValue

string

否

枚举值

北京

samples

array

否

数据样例列表，在关联数据表时若选择允许拉取数据样例，这个字段会自行进行补充

Sample

string

否

数据样例内容

上海

rangeMin

long

否

数字类型数据取值范围，最小值

0

rangeMax

long

否

数字类型数据取值范围，最大值

2000

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

错误信息

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

45390C6D-016D-5030-BF65-031ED1F65003

## 示例

正常返回示例

`JSON`格式

```
{
  "data": true,
  "errorMsg": "NoAuth",
  "code": "NoAuth",
  "success": true,
  "requestId": "45390C6D-016D-5030-BF65-031ED1F65003"
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

401

Internal.Error

Bad Request: Internal Error.

内部错误，请联系客服人员排查

401

NoAuth

Bad Request: Workspace.Illegal.Auth.

当前所使用的账号无所指定业务空间的权限

401

NoResourceAuth

Bad Request: Resource Auth Error.

没有请求的资源的权限，请确保所请求的资源属于当前参数中的业务空间

401

SystemOperationInProgress

Xiyan GBI is learning your previous modifications. Please try again later.

析言GBI正在学习您之前的修改内容，请稍后重试

访问[错误中心](https://api.aliyun.com/document/DataAnalysisGBI/2024-08-23/errorCode)查看更多错误码。
