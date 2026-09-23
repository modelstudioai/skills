# RunDataResultAnalysis - 执行结果分析

对结构化数据类型的执行结果进行分析、可视化信息生成。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/RunDataResultAnalysis)

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

dataanalysisgbi:RunDataResultAnalysis

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /gbi/runDataResultAnalysis HTTP/1.1
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

sqlData

object

否

sql 执行后所查询到的结构化数据内容，当前情况下此参数必传

Details

**sqlData 示例子**

{ "column": \[ "month", "total\_received" \], "data": \[ { "month": "2024-01", "total\_received": "603" }, { "month": "2024-02", "total\_received": "749" }, { "month": "2024-03", "total\_received": "1311" }, { "month": "2024-04", "total\_received": "1003" }, { "month": "2024-05", "total\_received": "726" }, { "month": "2024-06", "total\_received": "791" }, { "month": "2024-07", "total\_received": "60" } \] }

column

array

否

SQL 执行结果中，查询到的具体的字段名字列表

Column

string

否

SQL 执行结果中，查询到的具体的列名

month

data

array<object>

否

与 SQL 执行结果中的列名对应的结构化信息列表，详细结构可参考上方 sqlData 的示例

Data

object

否

与 SQL 执行结果中的列名对应的结构化信息，每一个代表着一行数据，其中的字段与表头列表应该为一一对应的关系

string

否

当前列名所对应的一条数据的具体内容

2024-01

analysisMode

string

否

当前希望执行的可视化类型，可以只生成图表或只生成文本分析

枚举值：

-   all：生成图表和文字分析。
-   text：只生成文字分析。
-   chart：只生成图表。

all

requestId

string

是

请求 id，这里的请求 id 为 RunSqlGeneration 接口中执行返回的 requestId，若传入未被 RunSqlGeneration 执行过的 requestId，执行会被拒绝

FF76AD3F-8B32-567E-819B-0D3738917006

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

data

object

返回结果

errorMessage

string

错误信息

Access was denied, message: No such namespace namespaces/tech-scp-chain7.

event

string

事件类型

枚举值：

-   result：结果事件。

result

requestId

string

当前本次请求的 id

DA2578F7-88A5-5D6E-9305-33E724E97D60

visualization

object

用于可视化模块展示所需要的信息

data

object

数据列表

plotType

string

可视化图表展示的类型

bar

xAxis

array

具体某一个 x 轴所展示的字段列表

xAxis

string

具体某一个 x 轴所展示的字段

product\_name

yAxis

array

具体某一个 y 轴所展示的字段列表

yAxis

string

具体某一个 y 轴所展示的字段

total\_sales

text

string

对于 sql 执行结果的分析总结

查询结果显示，在过去两年中销量超过5的所有产品包括：2L大容量空气炸锅销售了109件，青春版运动手环销售了119件，2L大容量全自动豆浆机销售了106件，无线蓝牙耳机快充版销售了84件，2L大容量便携式榨汁机销售了136件，青春版智能手表销售了104件，挂壁式护眼台灯销售了102件，P30手机8+256G销售了83件，2L大容量电热水壶销售了84件，男士电动化妆刷套装销售了197件，旅行箱销售了82件，手链销售了101件，项链销售了84件，头饰发链销售了89件，腕表销售了98件，戒指销售了157件，真皮皮包销售了136件，风衣大衣销售了76件，运动旅行包销售了91件，丝巾销售了265件，1L迷你空气炸锅销售了85件，豪华款运动手环销售了132件，1L迷你全自动豆浆机销售了81件，豪华版无线蓝牙耳机（绿色）销售了122件，1L迷你便携式榨汁机销售了76件，豪华款智能手表销售了76件，粘贴式护眼台灯销售了109件，M60手机16+512G销售了109件，1L迷你电热水壶销售了63件，女士电动化妆刷套装销售了158件。

sql

string

当前对话生成的 SQL 语句

select p.product\_id, p.product\_name, sum(o.quantity) as total\_sales from products p join orders o on p.product\_id = o.product\_id where o.order\_date between '2022-10-22' and '2024-10-22' group by p.product\_id, p.product\_name having total\_sales > 5

rewrite

string

改写后的用户输入

过去两年中，销量超过5的产品有哪些

## 示例

正常返回示例

`JSON`格式

```
{
  "data": {
    "errorMessage": "Access was denied, message: No such namespace namespaces/tech-scp-chain7.",
    "event": "result",
    "requestId": "DA2578F7-88A5-5D6E-9305-33E724E97D60",
    "visualization": {
      "data": {
        "plotType": "bar",
        "xAxis": [
          "product_name"
        ],
        "yAxis": [
          "total_sales"
        ]
      },
      "text": "查询结果显示，在过去两年中销量超过5的所有产品包括：2L大容量空气炸锅销售了109件，青春版运动手环销售了119件，2L大容量全自动豆浆机销售了106件，无线蓝牙耳机快充版销售了84件，2L大容量便携式榨汁机销售了136件，青春版智能手表销售了104件，挂壁式护眼台灯销售了102件，P30手机8+256G销售了83件，2L大容量电热水壶销售了84件，男士电动化妆刷套装销售了197件，旅行箱销售了82件，手链销售了101件，项链销售了84件，头饰发链销售了89件，腕表销售了98件，戒指销售了157件，真皮皮包销售了136件，风衣大衣销售了76件，运动旅行包销售了91件，丝巾销售了265件，1L迷你空气炸锅销售了85件，豪华款运动手环销售了132件，1L迷你全自动豆浆机销售了81件，豪华版无线蓝牙耳机（绿色）销售了122件，1L迷你便携式榨汁机销售了76件，豪华款智能手表销售了76件，粘贴式护眼台灯销售了109件，M60手机16+512G销售了109件，1L迷你电热水壶销售了63件，女士电动化妆刷套装销售了158件。"
    },
    "sql": "select p.product_id, p.product_name, sum(o.quantity) as total_sales from products p join orders o on p.product_id = o.product_id where o.order_date between '2022-10-22' and '2024-10-22' group by p.product_id, p.product_name having total_sales > 5",
    "rewrite": "过去两年中，销量超过5的产品有哪些"
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

Invalid.RequestId

Bad Request: Invalid RequestId.

requestId错误或已过期

访问[错误中心](https://api.aliyun.com/document/DataAnalysisGBI/2024-08-23/errorCode)查看更多错误码。
