# RunSqlGeneration - 运行sql生成

运行sql生成，根据当前的query信息，结合已关联的数据表，进行sql语句的生成。 该接口适合以下场景： 您的数据库在本地，不能被析言访问。 您可以通过析言关联虚拟数据源，调用该接口生成SQL，然后自行解析和执行SQL。 具体的使用，可以参考以下最佳实践文档： https://help.aliyun.com/zh/model-studio/xiyan-gbi-local-data-best-practices

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/RunSqlGeneration)

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

dataanalysisgbi:RunSqlGeneration

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /gbi/runSqlGeneration HTTP/1.1
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

specificationType

string

否

当前请求指定使用的版本信息，不填时使用默认业务空间版本

枚举值：

-   STANDARD\_TURBO：标准版turbo。
-   STANDARD\_MIX：标准版mix。
-   CUSTOMIZATION：定制版turbo。

STANDARD\_MIX

query

string

是

用户输入的 query

请问销量前十的产品有哪些

sessionId

string

否

消息会话 ID，多条 requestId 可以属于同一个会话 sessionId

d5eced84-fd25-43ee-a245-adb4e4a8c3be

## 返回参数

名称

类型

描述

示例值

object

SseEmitter

data

object

返回信息

errorMessage

string

错误信息

Access was denied, message: No such namespace namespaces/tech-scp-chain7.

event

string

事件类型

枚举值：

-   evidence：所用到的辅助模型推理的信息。
-   sql\_part：流式生成sql的中间事件。
-   selector：选表事件。
-   rewrite：改写事件。
-   sql：生成sql的最终事件。

sql

evidence

string

所用到的辅助模型推理的信息

今年是2024年

requestId

string

当前本次请求的 id

DA2578F7-88A5-5D6E-9305-33E724E97D60

rewrite

string

改写后的用户输入

查询全部关键字数据，并以饼图形式展示

selector

array

召回的具体的表的名字列表

selector

string

召回的具体的表的名字

table\_name1

sessionId

string

对话 ID

f64c38dd-a235-4bb4-ae6c-79eaedcba699

sql

string

当前对话生成的 SQL 语句

select p.product\_id, p.product\_name, sum(o.quantity) as total\_sales from products p join orders o on p.product\_id = o.product\_id where o.order\_date between '2022-10-22' and '2024-10-22' group by p.product\_id, p.product\_name having total\_sales > 5

sqlError

string

当任务执行失败时，此字段会报错导致任务失败的原因

Can not issue data manipulation statements with executeQuery()

## 示例

正常返回示例

`JSON`格式

```
{
  "data": {
    "errorMessage": "Access was denied, message: No such namespace namespaces/tech-scp-chain7.",
    "event": "sql",
    "evidence": "今年是2024年",
    "requestId": "DA2578F7-88A5-5D6E-9305-33E724E97D60",
    "rewrite": "查询全部关键字数据，并以饼图形式展示",
    "selector": [
      "table_name1"
    ],
    "sessionId": "f64c38dd-a235-4bb4-ae6c-79eaedcba699",
    "sql": "select p.product_id, p.product_name, sum(o.quantity) as total_sales from products p join orders o on p.product_id = o.product_id where o.order_date between '2022-10-22' and '2024-10-22' group by p.product_id, p.product_name having total_sales > 5",
    "sqlError": "Can not issue data manipulation statements with executeQuery()",
    "chat": {
      "text": ""
    }
  }
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
