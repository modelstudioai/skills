# GetChatQuestionResp - 获取问答结果

获取问答结果，即API SubmitChatQuestion的结果。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetChatQuestionResp)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetChatQuestionResp)

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

dianjin:GetChatQuestionResp

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/virtualHuman/chat/query HTTP/1.1
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

业务空间 id

llm-xxxxx

body

object

否

请求体

sessionId

string

是

所属会话 ID

237645726354

batchId

string

是

问题批次 ID

1869307330227937280

## 返回参数

名称

类型

描述

示例值

object

结果

success

boolean

是否成功

true

dataType

string

数据类型

null

time

string

时间戳

2024-01-01 00:00:00

errCode

string

错误码

0

message

string

错误信息

ok

data

object

响应数据

currentState

string

当前状态\[INIT(初始化),PROCESSING(处理中),COMPLETED(已结束)\]

PROCESSING

questionList

array<object>

问题列表

questionList

object

问题

sessionId

string

所属会话 ID

1732846760323001

userId

string

直播间提问用户的唯一 ID

39847834568436

userName

string

直播间提问用户的名称

张\*

content

string

问题内容

今天天气怎么样

gmtCreate

string

原始提问时间

2024-11-17 10:05:00

type

string

问题类型\[PRODUCT\_QA(音频提交),GOSSIP(操作提交),UNKNOWN(未知)\]

PRODUCT\_QA

reply

string

答复内容，回复的内容

感谢您的支持！

oriContent

string

原始问题

今天天气怎么样

requestId

string

请求 id

44BD277A-87F9-5310-8D63-3E6645F1DA85

cost

long

耗时

null

## 示例

正常返回示例

`JSON`格式

```
{
  "success": true,
  "dataType": null,
  "time": "2024-01-01 00:00:00",
  "errCode": 0,
  "message": "ok",
  "data": {
    "currentState": "PROCESSING",
    "questionList": [
      {
        "sessionId": 1732846760323001,
        "userId": 39847834568436,
        "userName": "张*",
        "content": "今天天气怎么样",
        "gmtCreate": "2024-11-17 10:05:00",
        "type": "PRODUCT_QA",
        "reply": "感谢您的支持！",
        "oriContent": "今天天气怎么样"
      }
    ]
  },
  "requestId": "44BD277A-87F9-5310-8D63-3E6645F1DA85",
  "cost": 0
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/DianJin/2024-06-28/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

暂无变更历史
