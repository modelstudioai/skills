# RunLibraryChatGeneration - 文档库会话生成

文档库会话生成，用自然语言提问，检索文档库相关信息，总结回答。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/RunLibraryChatGeneration)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/RunLibraryChatGeneration)

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

dianjin:RunLibraryChatGeneration

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/run/library/chat/generation HTTP/1.1
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

业务空间 Id

llm-xxxx

body

object

否

请求体。

docIdList

array

否

文档 id 列表

docIdList

string

否

文档 id

1273827636xxx

enableFollowUp

boolean

否

是否开启多轮增强

false

enableMultiQuery

boolean

否

是否开启 query 拆分

false

enableOpenQa

boolean

否

是否开启 openQA

false

followUpLlm

string

否

query 多轮增强使用的 llm

qwen-max

libraryId

string

是

文档库 id

3akzl28vap

llmType

string

是

大模型类型

qwen-max

multiQueryLlm

string

否

query 拆分使用的 llm

qwen-max

query

string

是

用户输入的 query

这两天北京气候怎么样

queryCriteria

object

否

属性过滤器

and

array<object>

否

and 表达式，用于筛选文档/文档块

and

object

否

and 表达式的内容

boost

float

否

标签的权重。当该值小于 1 时，则降低对应关键词的权重；反之，大于 1 时，增大对应关键词的权重。

0.5

key

string

否

标签的 key

city

operator

string

否

标签的操作符：文档库元信息 key 存储的 value 和您输入的 value 之间的关系

-   eq: 文档库元信息 key 存储的 value = 您输入的 value
-   lte：文档库元信息 key 存储的 value <= 您输入的 value
-   gte：文档库元信息 key 存储的 value >= 您输入的 value
-   lt：文档库元信息 key 存储的 value < 您输入的 value
-   gt：文档库元信息 key 存储的 value > 您输入的 value

eq

value

string

否

标签的值

北京

or

array<object>

否

or 表达式，用于筛选文档/文档块

or

object

否

or 表达式的内容

boost

float

否

标签的权重。当该值小于 1 时，则降低对应关键词的权重；反之，大于 1 时，增大对应关键词的权重。

0.5

key

string

否

标签的 key

city

operator

string

否

标签的操作符：文档库元信息 key 存储的 value 和您输入的 value 之间的关系

-   eq: 文档库元信息 key 存储的 value = 您输入的 value
-   lte：文档库元信息 key 存储的 value <= 您输入的 value
-   gte：文档库元信息 key 存储的 value >= 您输入的 value
-   lt：文档库元信息 key 存储的 value < 您输入的 value
-   gt：文档库元信息 key 存储的 value > 您输入的 value

eq

value

string

否

标签的值

北京

rerankType

string

否

排序策略类型：linear/model (linear: 基于规则排序, model: 模型排序, llm)

linear

sessionId

string

否

sessionId

null

stream

boolean

否

流式/非流式

false

subQueryList

array

否

子查询 query 列表

subQueryList

string

否

子查询 query

北京最近气温如何？

textSearchParameter

object

否

搜索引擎参数--文本搜索参数

limit

integer

否

返回行数

10

searchAnalyzerType

string

否

搜索分词器（Standard, IkMaxWord, IkSmart），根据业务需求灵活配置，如果留空，使用文档库绑定的搜索分词器。

IkMaxWord

topK

integer

否

最终召回的语料数量

1

vectorSearchParameter

object

否

搜索引擎参数--向量搜索参数

limit

integer

否

返回行数

10

withDocumentReference

boolean

否

是否返回文档引用

false

## 返回参数

名称

类型

描述

示例值

object

ResultCode

cost

long

耗时

null

data

any

响应数据（非流式）。

{ "finish":true, "text":"是的，记名预付卡的有效期不得低于3年。", "message": "是的，记名预付卡的有效期不得低于3年。", "queryResult":{ "errCode": "0", //接口协议层面的错误码，正常为0，未授权，参数错误，服务器异常时会发生变化，可以忽略不处理 "message": "ok", //接口协议层面的消息 "data":{ "success": true, //有回答true 无回答false "answer": null, //大模型生成的回答结果 "embeddingElapsedMs": 127, "vectorSearchElapsedMs": 2745, "llmElapsedMs": 7911, "totalElapsedMs": 10820, "chunks": \[ //召回的分块信息，一般为top5或top10，可联系我们调整效果 { "chunkId": "470182177892469799", //分块信息的编号 "docId": "22666332", //分块关联的文档编号 "chunkText": "Profits plummeted in the first quarter, can't you bear it? In fact, previous rounds of price cuts have indeed had a certain impact on Tesla's financial data. Tesla has just released its financial report for the first quarter of this year. The data shows that in Q1 2023, Tesla achieved revenue of 23.33 billion US dollars, an increase of 24% over the previous year; Tesla delivered more than 422,000 electric vehicles worldwide in the first quarter, an increase of 36% over the previous year", //新闻原始内容 "chunkMeta": { // demo数据中的其他metadata "language": "en", "unique\_id": "news\_22666332\_13", "content\_type": "news", "stock\_id\_list": \[\] } }\], "documents": \[{ "docId": "1686637056086872065", //文档编号 "gmtCreate": "2023-08-02 15:16:25", //文档的创建时间 "libraryId": "a1b2c3", //文档关联的知识库编号 "title": "2023年工银信用卡微信、京东绑卡消费累计积分活动", //文档标题 "url": null //文档连接，如有 }\] //块文本关联的文档 }, "success": true //接口协议层面的成功/失败状态 true就是errCode为0 } }

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

## [](#流式接口返回说明)流式接口返回说明

### [](#根据历史对话改写结果)根据历史对话改写结果

```json
{
    "success": true,
    "dataType": "copilotStep",
    "time": "2024-08-26 11:28:10",
    "errCode": "0",
    "message": "ok",
    "data": {
        "stepName": "start_followup_query",  // 开始改写
        "data": "业绩表现如何"
    },
    "requestId": null,
    "cost": null
}

{
    "success": true,
    "dataType": "copilotStep",
    "time": "2024-08-26 11:28:10",
    "errCode": "0",
    "message": "ok",
    "data": {
        "stepName": "completed_followup_query", // 完成改写
        "data": "业绩表现如何"
    },
    "requestId": null,
    "cost": null
}
```

### [](#query-分解)query 分解

```json
{
    "success": true,
    "dataType": "copilotStep",
    "time": "2024-08-26 11:28:10",
    "errCode": "0",
    "message": "ok",
    "data": {
        "stepName": "start_understand_query",  // 开始拆分
        "data": "业绩表现如何"
    },
    "requestId": null,
    "cost": null
}

{
    "success": true,
    "dataType": "copilotStep",
    "time": "2024-08-26 11:28:12",
    "errCode": "0",
    "message": "ok",
    "data": {
        "stepName": "completed_understand_query",  // 完成拆分
        "data": [
            "业绩表现的具体时间段是什么？",
            "是指哪一行业的业绩表现，或者哪个公司的业绩表现？",
            "业绩表现的数据指标有哪些？例如营收、利润、市场份额等。"
        ]
    },
    "requestId": null,
    "cost": null
}
```

### [](#召回结果)召回结果

```json
{
    "success": true,
    "dataType": "queryResult",
    "time": "2023-09-20 16:36:04",
    "errCode": "0",
    "message": "retriever completed",
    "data": {
        "success": true,
        "answer": null,
        "prompt": "请使用以下上下文来回答最后的问题。\n 以下是上下文内容：\n 回，本办法另有规定的除外。不记名预付卡有效期不得低于 3 年。\n 预付卡不得具有透支功能。\n 发卡机构发行销售预付卡时，应向持卡人告知预付卡的有效 期及计算方法。超过有效期尚有资金余额的预付卡，发卡机构应 当提供延期、激活、换卡等服务，保障持卡人继续使用。\n 第九条预付卡卡面应当记载预付卡名称、发卡机构名称、 是否记名、卡号、有效期限或有效期截止日、持卡人注意事项、 客户服务电话等要素。\n 第十条个人或单位购买记名预付卡或一次性购买不记名预 付卡 1 万元以上的，应当使用实名并提供有效身份证件。\n 发卡机构应当识别购卡人、单位经办人的身份，\n\n 息。\n 对于记名预付卡，发卡机构还应当在预付卡核心业务处理系 统中记载持卡人的有效身份证件信息、预付卡卡号、金额等信息。\n 第十二条单位一次性购买预付卡 5000 元以上，个人一次性购 买预付卡 5 万元以上的，应当通过银行转账等非现金结算方式购 买，不得使用现金。\n 购卡人不得使用信用卡购买预付卡。\n 第十三条采用银行转账等非现金结算方式购买预付卡的， 付款人银行账户名称和购卡人名称应当一致。\n 发卡机构应当核对账户信息和身份信息的一致性，在预付卡 核心业务处理系统中记载付款人银行账户名称和账号、收款人银 行账户名称和账号、转账金额等信息。\n 第十四\n\n\n\n 基于上下文理解作出回答，保持回答尽可能简洁。如果你不知道答案，直接回答我不知道。\n 问题：记名预付卡有效期不得低于 3 年吗？\n 答案：",
        "embeddingElapsedMs": 1423,
        "vectorSearchElapsedMs": 115,
        "textSearchElapsedMs": 0,
        "llmElapsedMs": null,
        "totalElapsedMs": 1626,
        "reRankElapsedMs": 8,
        "chunks": [
            {
                "libraryId": "5rdxr3dxmk",
                "libraryName": "富滇银行测试知识库",
                "title": "《支付机构预付卡业务管理办法》(中国人民银行公告〔2012〕第 12 号)",
                "chunkId": "478245189908103170",
                "docId": "1701838553380655106",
                "chunkText": "回，本办法另有规定的除外。不记名预付卡有效期不得低于 3 年。\n 预付卡不得具有透支功能。\n 发卡机构发行销售预付卡时，应向持卡人告知预付卡的有效 期及计算方法。超过有效期尚有资金余额的预付卡，发卡机构应 当提供延期、激活、换卡等服务，保障持卡人继续使用。\n 第九条预付卡卡面应当记载预付卡名称、发卡机构名称、 是否记名、卡号、有效期限或有效期截止日、持卡人注意事项、 客户服务电话等要素。\n 第十条个人或单位购买记名预付卡或一次性购买不记名预 付卡 1 万元以上的，应当使用实名并提供有效身份证件。\n 发卡机构应当识别购卡人、单位经办人的身份，",
                "fileType": "pdf",
                "chunkMeta": {},
                "score": 0.92747295
            },
            {
                "libraryId": "5rdxr3dxmk",
                "libraryName": "富滇银行测试知识库",
                "title": "《支付机构预付卡业务管理办法》(中国人民银行公告〔2012〕第 12 号)",
                "chunkId": "478245189908234242",
                "docId": "1701838553380655106",
                "chunkText": "息。\n 对于记名预付卡，发卡机构还应当在预付卡核心业务处理系 统中记载持卡人的有效身份证件信息、预付卡卡号、金额等信息。\n 第十二条单位一次性购买预付卡 5000 元以上，个人一次性购 买预付卡 5 万元以上的，应当通过银行转账等非现金结算方式购 买，不得使用现金。\n 购卡人不得使用信用卡购买预付卡。\n 第十三条采用银行转账等非现金结算方式购买预付卡的， 付款人银行账户名称和购卡人名称应当一致。\n 发卡机构应当核对账户信息和身份信息的一致性，在预付卡 核心业务处理系统中记载付款人银行账户名称和账号、收款人银 行账户名称和账号、转账金额等信息。\n 第十四",
                "fileType": "pdf",
                "chunkMeta": {},
                "score": 0.8335201
            }
        ],
        "vectorChunks": [
            {
                "libraryId": "5rdxr3dxmk",
                "libraryName": null,
                "title": null,
                "chunkId": "478245189908103170",
                "docId": "1701838553380655106",
                "chunkText": "回，本办法另有规定的除外。不记名预付卡有效期不得低于 3 年。\n 预付卡不得具有透支功能。\n 发卡机构发行销售预付卡时，应向持卡人告知预付卡的有效 期及计算方法。超过有效期尚有资金余额的预付卡，发卡机构应 当提供延期、激活、换卡等服务，保障持卡人继续使用。\n 第九条预付卡卡面应当记载预付卡名称、发卡机构名称、 是否记名、卡号、有效期限或有效期截止日、持卡人注意事项、 客户服务电话等要素。\n 第十条个人或单位购买记名预付卡或一次性购买不记名预 付卡 1 万元以上的，应当使用实名并提供有效身份证件。\n 发卡机构应当识别购卡人、单位经办人的身份，",
                "fileType": null,
                "chunkMeta": {},
                "score": 0.85494584
            },
            {
                "libraryId": "5rdxr3dxmk",
                "libraryName": null,
                "title": null,
                "chunkId": "478245189908234242",
                "docId": "1701838553380655106",
                "chunkText": "息。\n 对于记名预付卡，发卡机构还应当在预付卡核心业务处理系 统中记载持卡人的有效身份证件信息、预付卡卡号、金额等信息。\n 第十二条单位一次性购买预付卡 5000 元以上，个人一次性购 买预付卡 5 万元以上的，应当通过银行转账等非现金结算方式购 买，不得使用现金。\n 购卡人不得使用信用卡购买预付卡。\n 第十三条采用银行转账等非现金结算方式购买预付卡的， 付款人银行账户名称和购卡人名称应当一致。\n 发卡机构应当核对账户信息和身份信息的一致性，在预付卡 核心业务处理系统中记载付款人银行账户名称和账号、收款人银 行账户名称和账号、转账金额等信息。\n 第十四",
                "fileType": null,
                "chunkMeta": {},
                "score": 0.6670402
            }
        ],
        "textChunks": [],
        "chunkParts": [],
        "chunkTextList": [
            "回，本办法另有规定的除外。不记名预付卡有效期不得低于 3 年。\n 预付卡不得具有透支功能。\n 发卡机构发行销售预付卡时，应向持卡人告知预付卡的有效 期及计算方法。超过有效期尚有资金余额的预付卡，发卡机构应 当提供延期、激活、换卡等服务，保障持卡人继续使用。\n 第九条预付卡卡面应当记载预付卡名称、发卡机构名称、 是否记名、卡号、有效期限或有效期截止日、持卡人注意事项、 客户服务电话等要素。\n 第十条个人或单位购买记名预付卡或一次性购买不记名预 付卡 1 万元以上的，应当使用实名并提供有效身份证件。\n 发卡机构应当识别购卡人、单位经办人的身份，",
            "息。\n 对于记名预付卡，发卡机构还应当在预付卡核心业务处理系 统中记载持卡人的有效身份证件信息、预付卡卡号、金额等信息。\n 第十二条单位一次性购买预付卡 5000 元以上，个人一次性购 买预付卡 5 万元以上的，应当通过银行转账等非现金结算方式购 买，不得使用现金。\n 购卡人不得使用信用卡购买预付卡。\n 第十三条采用银行转账等非现金结算方式购买预付卡的， 付款人银行账户名称和购卡人名称应当一致。\n 发卡机构应当核对账户信息和身份信息的一致性，在预付卡 核心业务处理系统中记载付款人银行账户名称和账号、收款人银 行账户名称和账号、转账金额等信息。\n 第十四"
        ],
        "documents": [
            {
                "docId": "1701838553380655106",
                "gmtCreate": "2023-09-13 14:01:44",
                "libraryId": null,
                "title": "《支付机构预付卡业务管理办法》(中国人民银行公告〔2012〕第 12 号)",
                "url": null,
                "fileType": "pdf"
            }
        ]
    },
    "cost": null
}
```

### [](#模型总结的结果)模型总结的结果

```json
{
    "success": true,
    "dataType": "message",
    "time": "2023-09-20 16:36:05",
    "errCode": "0",
    "message": "ok",
    "data": {
        "message": "是的，",// 增量答案
        "text": "是的，", // 累计答案
        "finish": false
    },
    "cost": null
}
```

## 示例

正常返回示例

`JSON`格式

```
{
  "cost": 0,
  "data": "{\n    \"finish\":true,\n    \"text\":\"是的，记名预付卡的有效期不得低于3年。\",\n    \"message\": \"是的，记名预付卡的有效期不得低于3年。\",\n    \"queryResult\":{\n      \"errCode\": \"0\",\t//接口协议层面的错误码，正常为0，未授权，参数错误，服务器异常时会发生变化，可以忽略不处理\n      \"message\": \"ok\",\t//接口协议层面的消息\n      \"data\":{\n        \"success\": true,\t//有回答true 无回答false\n        \"answer\": null,\t//大模型生成的回答结果\n        \"embeddingElapsedMs\": 127,\n        \"vectorSearchElapsedMs\": 2745,\n        \"llmElapsedMs\": 7911,\n        \"totalElapsedMs\": 10820,\n        \"chunks\": [\t//召回的分块信息，一般为top5或top10，可联系我们调整效果\n          {\n            \"chunkId\": \"470182177892469799\",\t//分块信息的编号\n            \"docId\": \"22666332\",\t//分块关联的文档编号\n            \"chunkText\": \"Profits plummeted in the first quarter, can't you bear it? In fact, previous rounds of price cuts have indeed had a certain impact on Tesla's financial data. Tesla has just released its financial report for the first quarter of this year. The data shows that in Q1 2023, Tesla achieved revenue of 23.33 billion US dollars, an increase of 24% over the previous year; Tesla delivered more than 422,000 electric vehicles worldwide in the first quarter, an increase of 36% over the previous year\",\t//新闻原始内容\n            \"chunkMeta\": {\t// demo数据中的其他metadata\n              \"language\": \"en\",\n              \"unique_id\": \"news_22666332_13\",\n              \"content_type\": \"news\",\n              \"stock_id_list\": []\n            }\n          }],\n        \"documents\": [{\n          \"docId\": \"1686637056086872065\",\t//文档编号\n          \"gmtCreate\": \"2023-08-02 15:16:25\",\t//文档的创建时间\n          \"libraryId\": \"a1b2c3\",\t//文档关联的知识库编号\n          \"title\": \"2023年工银信用卡微信、京东绑卡消费累计积分活动\",\t//文档标题\n          \"url\": null\t//文档连接，如有\n        }]\t//块文本关联的文档\n      },\n      \"success\": true\t//接口协议层面的成功/失败状态 true就是errCode为0\n    }\n  }",
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
