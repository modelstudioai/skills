# RunVideoScriptGenerate - AI生成视频剪辑脚本

AI生成视频剪辑脚本

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunVideoScriptGenerate)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/AiMiaoBi/2023-08-01/RunVideoScriptGenerate)

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

aimiaobi:RunVideoScriptGenerate

create

\*全部资源

`*`

无

无

## 请求语法

```
POST /miaobi/runVideoScriptGenerate HTTP/1.1
```

## 请求参数

名称

类型

必填

描述

示例值

WorkspaceId

string

是

阿里云百炼业务空间唯一标识：获取[业务空间 ID（Workspace ID）](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)

llm-xx

Prompt

string

是

视频脚本的提示词

写一篇关于黄山旅游的脚本

UseSearch

boolean

否

是否使用联网检索（如果选是，则会意图理解后联网检索相关参考素材）

true

ScriptLength

string

否

脚本篇幅 描述 可选值有：

20~75：10~15s 正常口播时长

75~150：15~30s 正常口播时长

150~300：≈30~60s 正常口播时长

\>=300：≥60s 正常口播时长

\>=300

Language

string

否

生成脚本的语言: 建议取值有：

zh-CN： 中文

en-US： 英文

默认中文

en-US

ScriptNumber

integer

否

生成脚本的篇数。默认 1 篇，最多同时生成三篇 如果指定多篇。则会并行返回流式多个脚本生成结果。（客户端通过不同 sessionId 区分）

2

## 返回参数

名称

类型

描述

示例值

object

Schema of Response

Header

object

响应头

ErrorCode

string

异常错误码

ScriptNumberExceed

ErrorMessage

string

调用失败时，返回的出错信息。

脚本篇数超限

Event

string

event 名称

result-generated

SessionId

string

会话 ID

3f7045e099474ba28ceca1b4eb6d6e21

StatusCode

integer

状态码。

400

TaskId

string

任务 ID

b057f2fa-2277-477b-babf-cbc062307828

TraceId

string

全链路 ID

2150451a17191950923411783e2927

Payload

object

响应体

Output

object

输出内容对象

Text

string

文本生成结果

大家好，我是\[xxx\]。今天带大家走进黄山，感受奇松、怪石、云海、温泉的绝美风光。首站迎客松，800年历史，枝干如臂，热情迎接每一位游客。接着登光明顶，360度全景尽收眼底。再探秘西海大峡谷，体验原始自然的震撼。最后，在温泉中放松身心，享受旅途的美好。希望这次旅行能给你留下难忘的记忆。我是\[你的名字\]，感谢观看，我们下次再见！","91522b25a4f440189320c9ede8ae6c85":"大家好，我是\[您的名字\]，今天带大家探索黄山的奇妙之旅。首先，我们将见到黄山的象征——迎客松，感受它800年的历史与欢迎。随后攀登光明顶，迎接壮丽的日出；漫步西海大峡谷，体验险峻之美；最后，在温泉中放松身心。希望这次旅行能让你爱上黄山。谢谢观看！","1c23af4a899e4b908bdcffa7d8d0ddc9":"大家好，欢迎来到黄山！这里以奇松、怪石、云海、温泉四绝闻名。从云谷寺开始，感受古朴氛围；挑战百步云梯，体验攀登乐趣；漫步西海大峡谷，领略壮丽景色；最后在玉屏楼迎接日出，享受心灵的宁静。希望这次旅行给你留下美好回忆！

Usage

object

token 用量

InputTokens

long

输入使用的 Token 数量

100

OutputTokens

long

输出 Token 数量

100

TotalTokens

long

总 token 数量

200

RequestId

string

请求唯一标识（当 Content-Type 返回 json 时 会返回该字段）

F2F366D6-E9FE-1006-BB70-2C650896AAB5

HttpStatusCode

string

HTTP 状态码（当 Content-Type 返回 json 时 会返回该字段）

403

Code

string

状态码，正常返回 200（当 Content-Type 返回 json 时 会返回该字段）

NoPermission

Message

string

错误说明（当 Content-Type 返回 json 时 会返回该字段）

You are not authorized to perform this action.

Success

boolean

是否成功：true 成功，false 失败（当 Content-Type 返回 json 时 会返回该字段）

false

## 示例

正常返回示例

`JSON`格式

```
{
  "Header": {
    "ErrorCode": "ScriptNumberExceed",
    "ErrorMessage": "脚本篇数超限",
    "Event": "result-generated\n",
    "SessionId": "3f7045e099474ba28ceca1b4eb6d6e21",
    "StatusCode": 400,
    "TaskId": "b057f2fa-2277-477b-babf-cbc062307828",
    "TraceId": "2150451a17191950923411783e2927"
  },
  "Payload": {
    "Output": {
      "Text": "大家好，我是[xxx]。今天带大家走进黄山，感受奇松、怪石、云海、温泉的绝美风光。首站迎客松，800年历史，枝干如臂，热情迎接每一位游客。接着登光明顶，360度全景尽收眼底。再探秘西海大峡谷，体验原始自然的震撼。最后，在温泉中放松身心，享受旅途的美好。希望这次旅行能给你留下难忘的记忆。我是[你的名字]，感谢观看，我们下次再见！\",\"91522b25a4f440189320c9ede8ae6c85\":\"大家好，我是[您的名字]，今天带大家探索黄山的奇妙之旅。首先，我们将见到黄山的象征——迎客松，感受它800年的历史与欢迎。随后攀登光明顶，迎接壮丽的日出；漫步西海大峡谷，体验险峻之美；最后，在温泉中放松身心。希望这次旅行能让你爱上黄山。谢谢观看！\",\"1c23af4a899e4b908bdcffa7d8d0ddc9\":\"大家好，欢迎来到黄山！这里以奇松、怪石、云海、温泉四绝闻名。从云谷寺开始，感受古朴氛围；挑战百步云梯，体验攀登乐趣；漫步西海大峡谷，领略壮丽景色；最后在玉屏楼迎接日出，享受心灵的宁静。希望这次旅行给你留下美好回忆！"
    },
    "Usage": {
      "InputTokens": 100,
      "OutputTokens": 100,
      "TotalTokens": 200
    }
  },
  "RequestId": "F2F366D6-E9FE-1006-BB70-2C650896AAB5",
  "HttpStatusCode": 403,
  "Code": "NoPermission",
  "Message": "You are not authorized to perform this action.",
  "Success": false
}
```

## 错误码

HTTP status code

错误码

错误信息

描述

403

NoPermission

You are not authorized to perform this action.

请检查workspaceId的赋值

访问[错误中心](< https://api.aliyun.com/document/AiMiaoBi/2023-08-01/errorCode>)查看更多错误码。
