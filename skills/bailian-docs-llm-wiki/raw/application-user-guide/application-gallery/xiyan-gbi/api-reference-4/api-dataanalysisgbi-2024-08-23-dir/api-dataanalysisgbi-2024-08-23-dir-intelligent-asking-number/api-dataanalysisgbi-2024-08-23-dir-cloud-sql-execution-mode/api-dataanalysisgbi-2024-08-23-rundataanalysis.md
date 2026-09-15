# RunDataAnalysis - Chat对话接口

析言为您提供了与官方页面对话效果相同的OpenAPI接口，只需传入workspaceId以及query等相关信息，即可对您已经创建好的业务空间进行问答和数据分析。 该接口适合以下场景： 您在析言控制台关联了数据源，即析言可以通过公网或者VPC的方式访问您的数据库并执行SQL。 具体的使用，可以参考以下最佳实践文档： https://help.aliyun.com/zh/model-studio/gbi-best-practices

## 接口说明

请确保在使用该接口前，已充分了解析言产品的收费方式和[价格](https://common-buy.aliyun.com/?&msctype=email&mscareaid=cn&mscsiteid=cn&mscmsgid=3800124102101018568&yunge_info=email___3800124102101018568&commodityCode=sfm_DataAnalysisGBI_public_cn)。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/DataAnalysisGBI/2024-08-23/RunDataAnalysis)

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

dataanalysisgbi:RunDataAnalysis

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/gbi/runDataAnalysis HTTP/1.1
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

generateSqlOnly

boolean

否

当前请求只生成并返回 sql，不会执行

true

query

string

是

用户输入的 query

请问销量前十的产品有哪些

sessionId

string

否

消息会话 ID，服务窗回调消息返回的会话 ID。

sessionID

dataRole

array

否

数据权限-角色名称的列表

**说明** 数据权限的相关配置内容需要在产品页面进行配置后，方可获取参数在 api 中调用

string

否

数据权限-角色名称的具体名字

管理员

userParams

any

否

数据角色依赖的自定义参数，当该角色配置了外部参数，必须传入

**说明** 数据权限的相关配置内容需要在产品页面进行配置后，方可获取参数在 api 中调用

{ "shopId":\[ "1", "2" \], "userId":"10001" }

agentCtrlParams

any

否

当前对话接口所透传的自定义参数，现仅支持：跳过改写、跳过可视化模块、开启对话问题澄清

{ "withoutRewrite": true, "withoutVisualization": true, "enableChatMode": true }

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

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

-   result：最终结果事件。
-   evidence：所用到的辅助模型推理的信息。
-   sql\_part：流式生成sql的中间事件。
-   sql\_data：sql执行获取到结果的事件。
-   selector：选表事件。
-   refine：开启重试时的重试事件。
-   rewrite：改写事件。
-   sql：生成sql的最终事件。

rewrite

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

这次对话，召回了哪些表以用于 sql 的生成

selector

string

召回的具体的表的名字

table\_name1

sessionId

string

对话 ID

sessionid1

sql

string

当前对话生成的 SQL 语句

select p.product\_id, p.product\_name, sum(o.quantity) as total\_sales from products p join orders o on p.product\_id = o.product\_id where o.order\_date between '2022-10-22' and '2024-10-22' group by p.product\_id, p.product\_name having total\_sales > 5

sqlData

object

sql 执行所返回的结构化内容

column

array

sql 执行结果中，查询的具体的字段名字

column

string

具体的字段名字内容

product

data

array<object>

sql 执行后获取的结构化数据，可能是多条

value

object

sql 执行后所查询到的结构化数据的一条内容

{ "product\_id": "29", "total\_sales": "63", "product\_name": "1L迷你电热水壶" }

sqlError

string

当任务执行失败时，此字段会报错导致任务失败的原因

Can not issue data manipulation statements with executeQuery()

visualization

object

用于可视化模块展示所需要的信息

data

object

用于可视化模块展示的结构化信息

plotType

string

可视化图表展示的类型

枚举值：

-   bar：柱状图。
-   line：折线图。
-   pie：饼状图。

bar

xAxis

array

可视化图表中 x 轴的内容

xAxis

string

具体某一个 x 轴所展示的字段

product\_name

yAxis

array

可视化图表中 y 轴的内容

yAxis

string

具体某一个 y 轴所展示的字段

total\_sales

stack

boolean

是否以堆叠的方式展示柱状图。仅当图表类型是柱状图的情况下，该参数才有效

false

option

string

初始化前端组件所需要的配置信息。仅当入参 agentCtrlParams 中 chartsFramework=echarts 时，该字段才有效

{ xAxis: { type: 'category', data: \['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'\] }, yAxis: { type: 'value' }, series: \[ { data: \[150, 230, 224, 218, 135, 147, 260\], type: 'line' } \] }

text

string

对于 sql 执行结果的分析总结

查询结果显示，在过去两年中销量超过5的所有产品包括：2L大容量空气炸锅销售了109件，青春版运动手环销售了119件，2L大容量全自动豆浆机销售了106件，无线蓝牙耳机快充版销售了84件，2L大容量便携式榨汁机销售了136件，青春版智能手表销售了104件，挂壁式护眼台灯销售了102件，P30手机8+256G销售了83件，2L大容量电热水壶销售了84件，男士电动化妆刷套装销售了197件，旅行箱销售了82件，手链销售了101件，项链销售了84件，头饰发链销售了89件，腕表销售了98件，戒指销售了157件，真皮皮包销售了136件，风衣大衣销售了76件，运动旅行包销售了91件，丝巾销售了265件，1L迷你空气炸锅销售了85件，豪华款运动手环销售了132件，1L迷你全自动豆浆机销售了81件，豪华版无线蓝牙耳机（绿色）销售了122件，1L迷你便携式榨汁机销售了76件，豪华款智能手表销售了76件，粘贴式护眼台灯销售了109件，M60手机16+512G销售了109件，1L迷你电热水壶销售了63件，女士电动化妆刷套装销售了158件。

httpStatusCode

long

当前某一轮事件透出的 http 状态码，正常情况下不会额外透出，无需处理

200

attempts

array

开启 sql 校验时会输出的事件类型字段，包含每轮重试生成的 sql 以及报错原因

attempts

any

每伦重试生成的具体 sql、具体的报错信息

\[{"sql":"SHOW TABLES","sqlError":"sql is invalid"},{"sql":"SHOW TABLES;","sqlError":"sql is invalid"}\]

chat

object

澄清事件，当用户问题较模糊并开启了需要澄清的开关时产生的事件

text

string

澄清话术，模型判断当前用户问题与当前关联数据内容信息不匹配时所产生的反问话术，帮助用户确认问题内容

您想查询的是订单表的创建时间字段嘛？

message

string

系统错误透出的报错信息，用于报错排查，无需用户处理

org.springframework.core.task.TaskRejectedException: ExecutorService in active state did not accept task: java.util.concurrent.CompletableFuture$AsyncSupply@25653b3b

code

string

系统错误透出的错误码，用于报错排查，无需用户处理

NoAuth

httpStatusCode

long

当前本次请求透出的 http 状态码，正常情况下不会额外透出，无需处理

200

## 示例

正常返回示例

`JSON`格式

```
{
  "data": {
    "errorMessage": "Access was denied, message: No such namespace namespaces/tech-scp-chain7.",
    "event": "rewrite",
    "evidence": "今年是2024年",
    "requestId": "DA2578F7-88A5-5D6E-9305-33E724E97D60",
    "rewrite": "查询全部关键字数据，并以饼图形式展示",
    "selector": [
      "table_name1"
    ],
    "sessionId": "sessionid1",
    "sql": "select p.product_id, p.product_name, sum(o.quantity) as total_sales from products p join orders o on p.product_id = o.product_id where o.order_date between '2022-10-22' and '2024-10-22' group by p.product_id, p.product_name having total_sales > 5",
    "sqlData": {
      "column": [
        "product"
      ],
      "data": [
        {
          "product_id": 29,
          "total_sales": 63,
          "product_name": "1L迷你电热水壶"
        }
      ]
    },
    "sqlError": "Can not issue data manipulation statements with executeQuery()",
    "visualization": {
      "data": {
        "plotType": "bar",
        "xAxis": [
          "product_name"
        ],
        "yAxis": [
          "total_sales"
        ],
        "stack": false,
        "option": "{\n  xAxis: {\n    type: 'category',\n    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']\n  },\n  yAxis: {\n    type: 'value'\n  },\n  series: [\n    {\n      data: [150, 230, 224, 218, 135, 147, 260],\n      type: 'line'\n    }\n  ]\n}"
      },
      "text": "查询结果显示，在过去两年中销量超过5的所有产品包括：2L大容量空气炸锅销售了109件，青春版运动手环销售了119件，2L大容量全自动豆浆机销售了106件，无线蓝牙耳机快充版销售了84件，2L大容量便携式榨汁机销售了136件，青春版智能手表销售了104件，挂壁式护眼台灯销售了102件，P30手机8+256G销售了83件，2L大容量电热水壶销售了84件，男士电动化妆刷套装销售了197件，旅行箱销售了82件，手链销售了101件，项链销售了84件，头饰发链销售了89件，腕表销售了98件，戒指销售了157件，真皮皮包销售了136件，风衣大衣销售了76件，运动旅行包销售了91件，丝巾销售了265件，1L迷你空气炸锅销售了85件，豪华款运动手环销售了132件，1L迷你全自动豆浆机销售了81件，豪华版无线蓝牙耳机（绿色）销售了122件，1L迷你便携式榨汁机销售了76件，豪华款智能手表销售了76件，粘贴式护眼台灯销售了109件，M60手机16+512G销售了109件，1L迷你电热水壶销售了63件，女士电动化妆刷套装销售了158件。"
    },
    "httpStatusCode": 200,
    "attempts": [
      [
        {
          "sql": "SHOW TABLES",
          "sqlError": "sql is invalid"
        },
        {
          "sql": "SHOW TABLES;",
          "sqlError": "sql is invalid"
        }
      ]
    ],
    "chat": {
      "text": "您想查询的是订单表的创建时间字段嘛？"
    }
  },
  "message": "org.springframework.core.task.TaskRejectedException: ExecutorService in active state did not accept task: java.util.concurrent.CompletableFuture$AsyncSupply@25653b3b",
  "code": "NoAuth",
  "httpStatusCode": 200
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
