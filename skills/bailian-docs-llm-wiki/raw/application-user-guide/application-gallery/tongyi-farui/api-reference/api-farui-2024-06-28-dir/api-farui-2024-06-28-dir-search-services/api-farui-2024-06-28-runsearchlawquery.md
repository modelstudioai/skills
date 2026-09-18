# RunSearchLawQuery - 法规检索

该接口用于检索用户描述的问题对应的相关法规。用户输入问题后，会调用大模型分析并检索对应的法规法条。

## 接口说明

请确保在使用该接口前，已充分了解法睿产品的收费方式和价格。

-   该接口需要开通法睿商品相关的后付费服务（开通免费），可以使用该账号的 AccessKey 和 AccessSecret 来调用我们的 OpenApi 服务
-   服务的响应结果是以流式的形式来返回（SSE）。
-   接口的调用需要百炼平台的工作空间权限。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/FaRui/2024-06-28/RunSearchLawQuery)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/farui/search/law/query HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

workspaceId

string

否

阿里云百炼平台工作空间 ID

llm-kqtrcpdee4xm29

appId

string

否

应用 ID

farui

thread

object

否

线程

messages

array<object>

否

请求上下文

object

否

请求上下文

content

string

否

对话内容

朋友借了我10万块钱，约定两个月归还且不需要利息。已经半年过去了但他一直没有还，我可以要求增加利息吗？

role

string

否

对话角色

user

query

string

是

待查询问题

劳动法

queryKeywords

array

否

关键词数组

string

否

关键词

\["盗窃","抢劫"\]

pageParam

object

否

分页参数

pageNumber

integer

否

页码

1

pageSize

integer

否

分页大小，默认 10，最大 50

10

filterCondition

object

否

筛选条件

lawName

string

否

法规名称

劳动法

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

requestId

string

Id of the request

05062567-EB51-50F6-AF56-0BE44955848D

data

object

返回信息

currentPage

integer

页码

1

lawResult

array<object>

法规搜索结果对象

法规结果

object

法规搜索结果

lawDomain

object

法规信息

abolitionBasis

string

废止依据内容

\[{\\"lawId\\":\\"chl542s333.txt\\",\\"times\\":\\"20170309\\",\\"lawName\\":\\"最高人民法院关于实施修订后的《关于常见犯罪的量刑指导意见》的通知\\"}\]"

implementYearMonthDate

string

施行日期

2014年01月03日

invalidBasis

string

失效依据

null

issuingNo

string

发文字号

""

issuingOrgan

string

发文机关

"{\\"level1Name\\":\\"最高人民法院\\",\\"level1Id\\":\\"6\\"}"

lawId

string

法规 id

b2274825c8c3bc2343ca73680243ddc8

lawItemId

string

法条 id

ccc209683be1509676174fd6890f24b8

lawName

string

法规名称

最高人民法院关于常见犯罪的量刑指导意见

lawOrder

string

法条名称

第二百六十三条

lawTitle

string

法规标题

最高人民法院关于常见犯罪的量刑指导意见第二百六十三条

modifyBasis

string

修改依据

"\[\]"

potencyLevel

string

效力级别

"{\\"level2Name\\":\\"两高工作文件\\",\\"level1Name\\":\\"司法解释\\",\\"level2Id\\":\\"002004\\",\\"level1Id\\":\\"002004\\"}"

releaseYearMonthDate

string

发布日期

2014年01月03日

thematicClassify

string

专题分类

null

lawSourceContent

string

法规正文

第二百六十三条……

timeliness

string

时效性

已废止/失效

similarity

string

相似度

0.0050

pageSize

integer

分页大小

0

query

string

检索的问题

抢劫

queryKeywords

array

关键词数组

关键词

string

关键词

\["抢劫"\]

sortKeyAndDirection

object

搜索排序字段

similarity

string

相似度排序方式 desc、asc

desc

releaseYearMonthDate

string

发布日期排序方式：desc,asc

desc

totalCount

long

总记录数

0

httpStatusCode

long

HTTP 状态码

200

success

boolean

true 接口调用成功，false 接口调用失败

true

message

string

错误信息

系统错误（接口正常为空）

code

string

错误码

Ok

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "05062567-EB51-50F6-AF56-0BE44955848D",
  "data": {
    "currentPage": 1,
    "lawResult": [
      {
        "lawDomain": {
          "abolitionBasis": "[{\\\"lawId\\\":\\\"chl542s333.txt\\\",\\\"times\\\":\\\"20170309\\\",\\\"lawName\\\":\\\"最高人民法院关于实施修订后的《关于常见犯罪的量刑指导意见》的通知\\\"}]\"",
          "implementYearMonthDate": "2014年01月03日",
          "invalidBasis": null,
          "issuingNo": "",
          "issuingOrgan": {
            "level1Name": "最高人民法院",
            "level1Id": 6
          },
          "lawId": "b2274825c8c3bc2343ca73680243ddc8",
          "lawItemId": "ccc209683be1509676174fd6890f24b8",
          "lawName": "最高人民法院关于常见犯罪的量刑指导意见",
          "lawOrder": "第二百六十三条",
          "lawTitle": "最高人民法院关于常见犯罪的量刑指导意见第二百六十三条",
          "modifyBasis": [],
          "potencyLevel": {
            "level2Name": "两高工作文件",
            "level1Name": "司法解释",
            "level2Id": "002004",
            "level1Id": "002004"
          },
          "releaseYearMonthDate": "2014年01月03日",
          "thematicClassify": null,
          "lawSourceContent": "第二百六十三条……",
          "timeliness": "已废止/失效"
        },
        "similarity": 0.005
      }
    ],
    "pageSize": 0,
    "query": "抢劫",
    "queryKeywords": [
      [
        "抢劫"
      ]
    ],
    "sortKeyAndDirection": {
      "similarity": "desc",
      "releaseYearMonthDate": "desc"
    },
    "totalCount": 0
  },
  "httpStatusCode": 200,
  "success": true,
  "message": "系统错误（接口正常为空）",
  "code": "Ok"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/FaRui/2024-06-28/errorCode)查看更多错误码。
