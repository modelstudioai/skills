# UpdateSubscription - 更新订阅信息

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/UpdateSubscription)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/UpdateSubscription)

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

bailianvoicebot:UpdateSubscription

update

\*全部资源

`*`

无

无

## 请求参数

名称

类型

必填

描述

示例值

BusinessUnitId

string

是

百炼业务空间 ID

llm-c11iig67g863rih8

MqType

string

是

消息推送类型

ROCKET\_MQ\_4

EventSubscriptions

array

是

订阅事件列表

string

是

订阅事件  
Established - 接通  
Released - 通话结束  
RecordingReady - 录音就绪  
CdrReady - 话单生成  
LabelReady - 标签生成

Released

Endpoint

string

否

接入点(使用 ROCKET\_MQ\_4、ROCKET\_MQ\_5 时必填)

rmq-cn-l4p89zajz67.cn-hangzhou.rmq.aliyuncs.com:8080

Topic

string

否

队列 topic(使用 ROCKET\_MQ\_4、ROCKET\_MQ\_5 时必填)

test

UserName

string

否

用户名(使用 ROCKET\_MQ\_5 时必填)

username

Password

string

否

密码(使用 ROCKET\_MQ\_5 时必填)

pwd

MqInstanceId

string

否

MQ 实例 ID(使用 ROCKET\_MQ\_5 时必填)

rmq-cn-l4p89zajz67.cn

ProducerId

string

否

生产者标识(使用 ROCKET\_MQ\_4 时必填)

user1

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

RequestId

string

Id of the request

D771A1B6-3D5F-174A-BEE1-98CE1000D337

HttpStatusCode

integer

http 状态码

200

Message

string

信息。

Instance llm-rj6aqmctjcit4acy does not exist.

Code

string

接口状态或 POP 错误码。

OK

Data

string

返回结果（应用 ID）

a395011f-a247-400f-bc69-28796749fd52

Params

array

动态错误参数

param

string

动态错误参数

llm-xdne77rxe14ziszr

## 示例

正常返回示例

`JSON`格式

```
{
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "HttpStatusCode": 200,
  "Message": "Instance llm-rj6aqmctjcit4acy does not exist.",
  "Code": "OK",
  "Data": "a395011f-a247-400f-bc69-28796749fd52\n",
  "Params": [
    "llm-xdne77rxe14ziszr"
  ]
}
```

## 错误码

访问[错误中心](< https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-04-22

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/UpdateSubscription?updateTime=2026-04-22#workbench-doc-change-demo)
