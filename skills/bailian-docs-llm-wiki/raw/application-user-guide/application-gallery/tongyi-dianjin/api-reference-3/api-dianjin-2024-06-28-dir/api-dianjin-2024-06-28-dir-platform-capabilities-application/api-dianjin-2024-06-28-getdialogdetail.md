# GetDialogDetail - 获取会话详情

获取会话详情信息。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/GetDialogDetail)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/DianJin/2024-06-28/GetDialogDetail)

## **授权信息**

下表是API对应的授权信息，可以在RAM权限策略语句的`Action`元素中使用，用来给RAM用户或RAM角色授予调用此API的权限。具体说明如下：

-   操作：是指具体的权限点。
    
-   访问级别：是指每个操作的访问级别，取值为写入（Write）、读取（Read）或列出（List）。
    
-   资源类型：是指操作中支持授权的资源类型。具体说明如下：
    
    -   对于必选的资源类型，用前面加 \* 表示。
        
    -   对于不支持资源级授权的操作，用`全部资源`表示。
        
-   条件关键字：是指云产品自身定义的条件关键字。
    
-   关联操作：是指成功执行操作所需要的其他权限。操作者必须同时具备关联操作的权限，操作才能成功。
    

**操作**

**访问级别**

**资源类型**

**条件关键字**

**关联操作**

dianjin:GetDialogDetail

get

\*全部资源

`*`

无

无

## 请求语法

```
GET /{workspaceId}/api/virtualHuman/dialog/detail HTTP/1.1
```

## 路径参数

**名称**

**类型**

**必填**

**描述**

**示例值**

workspaceId

string

是

业务空间 Id

llm-xxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

sessionId

string

是

会话 ID

1906623923815534xxx

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

ResultCode

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

2024-04-24 11:54:34

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

totalDialogTurns

integer

总对话轮次。总交互轮次按 AI 与客户的对话次数计算，AI 或客户的连续多句算作一轮。最后一句若由 AI 说出且非挂机，则整体轮次减 1。

10

validDialogTurns

integer

有效对话轮次。 AI、客户一问一答算一轮的，有效交互轮次指一问一答算一次，不同于总轮次的统计方式。

5

dialogueList

array<object>

对话明细列表

object

对话明细

role

string

角色：

-   0：客户
    
-   1：坐席
    

0

customerServiceType

string

坐席类型：

-   0: 机器人
    
-   1: 人工
    

0

customerServiceId

string

客服 ID

BOT

customerId

string

客户 ID

123761283

content

string

对话的具体内容

请问具体怎么操作呢？

type

string

对话内容的类型：text（文本）；audio（语音）；image（图片）。目前仅支持文本类型。

text

id

integer

本句话的唯一标识,内部赋值。可能为空，建议使用 recordId。

1742869659849

recordId

string

本句话的唯一标识,内部赋值，String 类型。

19387872364736xdhcb

intentCode

string

意图 code

193874634xxx

intentName

string

意图名称

客户询问如何操作

hangUpDialog

boolean

是否挂断：当句是否挂断会话标识

true

status

string

会话状态

COMPLETED

gmtCreate

string

会话时间

2024-09-27 11:23:20

requestId

string

请求 id

5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658

cost

integer

耗时

null

## 示例

正常返回示例

`JSON`格式

```
{
  "success": true,
  "dataType": "null",
  "time": "2024-04-24 11:54:34",
  "errCode": "0",
  "message": "ok",
  "data": {
    "totalDialogTurns": 10,
    "validDialogTurns": 5,
    "dialogueList": [
      {
        "role": "0",
        "customerServiceType": "0",
        "customerServiceId": "BOT",
        "customerId": "123761283",
        "content": "请问具体怎么操作呢？",
        "type": "text",
        "id": 1742869659849,
        "recordId": "19387872364736xdhcb",
        "intentCode": "193874634xxx",
        "intentName": "客户询问如何操作",
        "hangUpDialog": true
      }
    ],
    "status": "COMPLETED",
    "gmtCreate": "2024-09-27 11:23:20"
  },
  "requestId": "5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658",
  "cost": 0
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/DianJin/2024-06-28/GetDialogDetail#workbench-doc-change-demo)。
