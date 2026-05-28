# RealTimeDialog - 实时会话

实时会话，通过API CreateDialog创建会话后，可使用该API进行实时会话。

## 接口说明

请确保在使用该接口前，已充分了解通义点金产品的收费方式和价格。

前提条件

已开通阿里云百炼服务和通义点金服务。

获取到 workspaceId：获取 [workspace 标识](https://help.aliyun.com/zh/model-studio/developer-reference/get-app-id-and-workspace?spm=openapi-amp.newDocPublishment.0.0.2eb8281foUVd15#2612f896detsz:~:text=%E6%9F%A5%E7%9C%8BAPI%2DKEY%E3%80%82-,%E8%8E%B7%E5%8F%96APP%2DID%E5%92%8CWORKSPACE,-%E8%BF%9B%E5%85%A5%E6%88%91%E7%9A%84%E5%BA%94%E7%94%A8)。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/DianJin/2024-06-28/RealTimeDialog)

 [![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png) 调试](https://api.aliyun.com/api/DianJin/2024-06-28/RealTimeDialog)

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

dianjin:RealTimeDialog

none

\*全部资源

`*`

无

无

## 请求语法

```
POST /{workspaceId}/api/realtime/dialog/chat HTTP/1.1
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

llm-xxxxx

## 请求参数

**名称**

**类型**

**必填**

**描述**

**示例值**

body

object

否

请求体参数。

bizType

string

否

业务类型，默认 mixIntentChat。

mixIntentChat

analysis

boolean

否

是否分析

false

recommend

boolean

否

推荐意图

false

metaData

object

否

元信息，用于封装提示词。

{ "phoneTailNumber": "机主尾号：98X1", "preScreeningQuota": "预审额度：3万", "generalInterest": "平台一般利息：20.4%" }

stream

boolean

否

是否流式返回

false

conversationModel

array<object>

是

对话列表

object

否

对话

role

integer

是

角色。0 表示客户，1 表示坐席。

0

intentionCode

string

否

意图编码

198379874354

customerServiceType

string

否

坐席类型，0: 机器人，1: 人工。

0

customerServiceId

string

否

客服 ID，**必填**。

1374683645635

customerId

string

否

对话角色的唯一标识，**必填**。

98457834685635

content

string

是

对话的具体内容

人工客服

type

string

是

对话内容的类型\[text(文本),audio(音频),image(图片)\]

audio

beginTime

string

否

这句话的开始时间

2024-11-08 09:51:16

begin

integer

否

本句话的开始时间，相对于会话开始点的偏移时间 ms

5

end

integer

否

本句话的结束时间，相对于会话开始点的偏移时间 ms

10

sessionId

string

是

会话 ID

237645726354

dialogMemoryTurns

integer

否

携带的会话历史轮数

3

userVad

boolean

否

是否用户打断

true

scriptContentPlayed

string

否

上一句客服话术已经播报的部分

你好，我是

opType

string

否

操作类型：目前仅支持 common/hierarchical

common

## **返回参数**

**名称**

**类型**

**描述**

**示例值**

object

IntentionChatResp

id

string

本次调用的唯一标识符。每个 chunk 对象有相同的 id。

eb2b6139-ddf1-91a0-a47f-df7617ae9032

choices

array<object>

生成内容的数组，可包含一个或多个 choices 对象。

array<object>

生成内容

index

integer

在 choices 列表中的序列编号。

0

finishReason

string

会话结束时为 stop，会话正在进行中为 null；当 success 为 false 时，为错误信息。

stop

message

object

非流式时，返回的全量结果。流式时为空。

intentionCode

string

意图 code

1853360771162058752

intentionScript

string

意图话术

抱歉，我没有明白您的意思，或者您可以拨打我们的客服热线，请客服人员为您解答。

intentionName

string

意图名称

其它

recommendIntention

string

推荐意图

null

recommendScript

string

推荐话术

null

analysisProcess

string

分析过程

null

selfDirectedScript

string

自主问答话术，增量数据。流式时为空。

null

callTime

string

time

1735139569523

hangUpDialog

boolean

挂断对话

false

selfDirectedScriptFullContent

string

自主问答话术，全量数据

关于宇宙的大小，这是一个非常深奥的科学话题

interrupt

boolean

是否打断

false

skipCurrentRecognize

boolean

是否跳过当前识别

delta

object

流式时，返回的增量结果。非流式时为空。

intentionCode

string

意图 code

1853360771162058752

intentionScript

string

意图话术

抱歉，我没有明白您的意思，或者您可以拨打我们的客服热线，请客服人员为您解答。

intentionName

string

意图名称

其他

recommendIntention

string

推荐意图

null

recommendScript

string

推荐话术

null

analysisProcess

string

分析过程

null

selfDirectedScript

string

自主问答话术，增量数据

话题

callTime

string

time

null

hangUpDialog

boolean

挂断对话

false

selfDirectedScriptFullContent

string

自主问答话术，全量数据

关于宇宙的大小，这是一个非常深奥的科学话题

interrupt

boolean

是否打断

false

skipCurrentRecognize

boolean

是否跳过当前识别

false

created

string

本次请求被创建的时间戳

1735139569523

success

boolean

是否成功

true

requestId

string

请求 id

5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658

## 示例

正常返回示例

`JSON`格式

```
{
  "id": "eb2b6139-ddf1-91a0-a47f-df7617ae9032",
  "choices": [
    {
      "index": 0,
      "finishReason": "stop",
      "message": {
        "intentionCode": "1853360771162058752",
        "intentionScript": "抱歉，我没有明白您的意思，或者您可以拨打我们的客服热线，请客服人员为您解答。",
        "intentionName": "其它",
        "recommendIntention": "null",
        "recommendScript": "null",
        "analysisProcess": "null",
        "selfDirectedScript": "null",
        "callTime": "1735139569523",
        "hangUpDialog": false,
        "selfDirectedScriptFullContent": "关于宇宙的大小，这是一个非常深奥的科学话题\n",
        "interrupt": false,
        "skipCurrentRecognize": true
      },
      "delta": {
        "intentionCode": "1853360771162058752",
        "intentionScript": "抱歉，我没有明白您的意思，或者您可以拨打我们的客服热线，请客服人员为您解答。",
        "intentionName": "其他",
        "recommendIntention": "null",
        "recommendScript": "null",
        "analysisProcess": "null",
        "selfDirectedScript": "话题",
        "callTime": "null",
        "hangUpDialog": false,
        "selfDirectedScriptFullContent": "关于宇宙的大小，这是一个非常深奥的科学话题",
        "interrupt": false,
        "skipCurrentRecognize": false
      }
    }
  ],
  "created": "1735139569523",
  "success": true,
  "requestId": "5E3FBAF1-17AF-53B7-AF0A-CDCEEB6DE658"
}
```

## 错误码

访问[错误中心](https://api.aliyun.com/document/DianJin/2024-06-28/errorCode)查看更多错误码。

## **变更历史**

更多信息，参考[变更详情](https://api.aliyun.com/document/DianJin/2024-06-28/RealTimeDialog#workbench-doc-change-demo)。
