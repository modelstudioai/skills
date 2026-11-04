# RunSearchCaseFullText - 案例检索

该接口用于检索用户描述的问题对应的相关案例。用户输入问题后，会调用大模型解析用户问题生成对应的检索条件，并根据检索条件检索对应的案例。

## 接口说明

-   该接口需要开通法睿商品相关的后付费服务（开通免费），可以使用该账号的 AccessKey 和 AccessSecret 来调用我们的 OpenApi 服务
-   接口的调用需要百炼平台的工作空间权限。

## 调试

您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。

[调试](https://api.aliyun.com/api/FaRui/2024-06-28/RunSearchCaseFullText)

## 授权信息

当前API暂无授权信息透出。

## 请求语法

```
POST /{workspaceId}/farui/search/case/fulltext HTTP/1.1
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

llm-9w5y60lseff0jiqm

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

9月19日，执行“和谐使命-2023”任务的海军“和平方舟”号医院船返回舟山到访基里巴斯、汤加、瓦努阿图、所罗门群岛、东帝汶等5国，诊疗民众多少人次？

queryKeywords

array

否

检索关键词数组

string

否

检索关键词

\["盗窃","抢劫"\]

pageParam

object

是

分页参数

pageNumber

integer

否

分页页码

1

pageSize

integer

否

每页数据量，默认 10，最高 200

10

sortKeyAndDirection

object

否

排序映射

string

否

排序字段 trialYearMonthDate 裁判日期 asc 升序 desc 降序

{"trialYearMonthDate":"desc"}

filterCondition

object

否

过滤条件

caseTitle

string

否

文书标题

杨怀平、广州市公安局越秀区分局公安行政管理:其他(公安)二审行政判决书

caseNo

string

否

文书案号

（2017）粤71行终2214号

referLevel

string

否

案例类型，只支持 其他、参考、指导性，默认是其他（普通案例）

其他

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

C844BE6B-33A9-5AC4-A1AE-97B131849E0F

data

object

返回信息

caseResult

array<object>

设置结果。如果设置成功，该字段值为 success。如果设置失败，该字段值为错误码描述，可参考本接口错误码的说明。

具体结果

object

设置结果。如果设置成功，该字段值为 success。如果设置失败，该字段值为错误码描述，可参考本接口错误码的说明。

caseDomain

object

案例信息

abstractObj

string

案件摘要

案件摘要

appliedLaws

string

法律依据，应用法条

法律依据，应用法条

caseBasic

string

案件基本情况

案件基本情况

caseFeature

string

案情特征

案情特征

basicCase

string

基本案情

基本案情

caseId

string

案件 id

案件id

caseNo

string

案号

案号

caseSummary

string

案件概述

案件概述

caseTitle

string

文书名称

文书名称

caseType

string

案件类型

案件类型

closeCaseCause

string

结案案由

结案案由

courtFindOut

string

本院查明

本院查明

courtThink

string

本院认为

本院认为

dataFrom

string

数据来源

数据来源

disputeFocus

string

争议焦点

争议焦点

disputeFocusTag

array

争议焦点段落

争议焦点

string

争议焦点段落

争议焦点段落

disputedpoints

string

争议点

争议点

keyfacts

string

核心事实

核心事实

legalBasis

string

法律依据

法律依据

documentType

string

文书类型

文书类型

litigants

string

当事人

当事人

litigationParticipant

string

诉讼参与人

诉讼参与人

openCaseCause

string

立案案由

立案案由

preTrialProcess

string

原审情况

原审情况

referLevel

string

参考类型

参考类型

sourceContent

string

文书正文

文书正文

trialCourt

object

审理法院信息

city

string

城市

遵义

commonLevel

string

审理法院层级

基层人民法院

country

string

国家

中国

county

string

区域

播州区

district

string

区

播州区

name

string

法院名

遵义市播州区人民法院

province

string

省

贵州省

specialLevel

string

法院级别

“”

trialDate

string

审理日期

2018-09-27

trialLevel

string

审判层级

审判层级

trialProcess

string

审理经过

审理经过

trialProgram

string

审判程序

审判程序

verdict

string

裁判结果段落

裁判结果段落

caseCause

string

案由

案由

judgReason

string

裁判理由

裁判理由

refereeGist

string

裁判要点

裁判要点

similarity

string

相似度

0.88

mode

string

前端渲染使用

normal

caseLevel

string

案例级别

"\[{\\"id\\":\\"指导性\\",\\"label\\":\\"指导性案例\\"}\]"

currentPage

integer

页码

1

pageSize

integer

每页显示条数。

10

query

string

过滤字段名字。

行政机关违反法定程序作出的行政处罚是否应被撤销的案例

queryKeywords

array

关键词数组

关键词列表

string

关键词

"行政机关"

totalCount

long

返回结果的总数量。

1

httpStatusCode

long

HTTP 状态码

200

message

string

响应消息。

成功时为空

code

string

响应状态码。

null

success

boolean

调用是否成功

True

## 示例

正常返回示例

`JSON`格式

```
{
  "requestId": "C844BE6B-33A9-5AC4-A1AE-97B131849E0F",
  "data": {
    "caseResult": [
      {
        "caseDomain": {
          "abstractObj": "案件摘要",
          "appliedLaws": "法律依据，应用法条",
          "caseBasic": "案件基本情况",
          "caseFeature": "案情特征",
          "basicCase": "基本案情",
          "caseId": "案件id",
          "caseNo": "案号",
          "caseSummary": "案件概述",
          "caseTitle": "文书名称",
          "caseType": "案件类型",
          "closeCaseCause": "结案案由",
          "courtFindOut": "本院查明\n\n",
          "courtThink": "本院认为",
          "dataFrom": "数据来源",
          "disputeFocus": "争议焦点",
          "disputeFocusTag": [
            "争议焦点段落"
          ],
          "disputedpoints": "争议点",
          "keyfacts": "核心事实",
          "legalBasis": "法律依据",
          "documentType": "文书类型",
          "litigants": "当事人",
          "litigationParticipant": "诉讼参与人",
          "openCaseCause": "立案案由",
          "preTrialProcess": "原审情况",
          "referLevel": "参考类型",
          "sourceContent": "文书正文",
          "trialCourt": {
            "city": "遵义",
            "commonLevel": "基层人民法院",
            "country": "中国",
            "county": "播州区",
            "district": "播州区",
            "name": "遵义市播州区人民法院",
            "province": "贵州省",
            "specialLevel": "“”"
          },
          "trialDate": "2018-09-27",
          "trialLevel": "审判层级",
          "trialProcess": "审理经过",
          "trialProgram": "审判程序",
          "verdict": "裁判结果段落",
          "caseCause": "案由\n",
          "judgReason": "裁判理由",
          "refereeGist": "裁判要点"
        },
        "similarity": 0.88,
        "mode": "normal"
      }
    ],
    "caseLevel": [
      {
        "id": "指导性",
        "label": "指导性案例"
      }
    ],
    "currentPage": 1,
    "pageSize": 10,
    "query": "行政机关违反法定程序作出的行政处罚是否应被撤销的案例",
    "queryKeywords": [
      "行政机关"
    ],
    "totalCount": 1
  },
  "httpStatusCode": 200,
  "message": "成功时为空",
  "code": null,
  "success": true
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/FaRui/2024-06-28/errorCode)查看更多错误码。
