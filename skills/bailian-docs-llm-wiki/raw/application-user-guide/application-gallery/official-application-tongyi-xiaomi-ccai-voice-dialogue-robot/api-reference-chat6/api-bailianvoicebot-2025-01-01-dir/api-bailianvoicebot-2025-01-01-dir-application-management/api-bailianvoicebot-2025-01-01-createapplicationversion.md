# CreateApplicationVersion - 创建语音机器人应用版本

创建语音机器人应用版本。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/CreateApplicationVersion)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/CreateApplicationVersion)

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

bailianvoicebot:CreateApplicationVersion

create

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

ApplicationId

string

是

应用 ID

a395011f-a247-400f-bc69-28796749fd52

SourceVersionId

string

否

原 versionID(发布时使用)

20904943-f711-494f-9f1f-e7f340f37707

TranscriberConfig

object

否

ASR 语音配置

NlsAccessType

string

否

ASR 访问方式

MANAGED

NlsEngine

string

否

ASR 引擎类型

ALIYUN

NlsAccessProfile

object

否

关联配置

AccessProfileId

string

否

三方语音配置 ID（使用豆包、科大等三方 ASR 服务时需配置）

c2c9baae-9351-4c49-a8cb-6f24a83a8718

VocabularyId

string

否

热词表 ID

cd97223f-42f2-4cd9-95af-e734e2fe1fe3

EndSilenceTimeout

integer

否

静音检测（说话间隔超过 x 毫秒时触发断句，即 VAD）

700

CustomizationId

string

否

ASR 的定制语言模型 ID

cd97223f-42f2-4cd9-95af-e734e2fe1fe4

SpeechNoiseThreshold

integer

否

噪音参数阈值，参数范围：\[-100,100\]。取值说明如下：

取值越趋于-100，噪音被判定为语音的概率越大。

取值越趋于+100，语音被判定为噪音的概率越大。

0

Model

string

否

ASR 模型

枚举值：

-   fun-asr-flash-8k-realtime：fun-asr-flash-8k-realtime。
-   fun-asr-realtime-2026-02-28：fun-asr-realtime-2026-02-28。
-   paraformer-realtime-v2：paraformer-realtime-v2。
-   paraformer-realtime-8k-v2：paraformer-realtime-8k-v2。

fun-asr-flash-8k-realtime

SynthesizerConfig

object

否

TTS 语音配置

NlsAccessType

string

否

TTS 访问方式

MANAGED

NlsEngine

string

否

TTS 引擎类型

ALIYUN

Voice

string

否

发音人

aiqi

SpeechRate

integer

否

播报速度

**说明** 取值范围：-500~500。

\-156

Volume

integer

否

音量

50

PitchRate

integer

否

语调

**说明** 取值范围：-500~500。

50

ScriptProfile

object

否

模型

Model

string

否

LLM 模型 ID

qwen-plus

AgentProfile

object

否

智能体配置信息

ScriptProfileTemplateId

string

否

智能体配置模版 ID

SFM\_PROMPTS\_DEFAULT

PromptsJson

string

否

提示词 json

{"prompts":"我是一个语音聊天机器人。"}

Name

string

否

智能体名称

语音机器人小云

Description

string

否

智能体描述

语音机器人小云

InteractionConfig

object

否

交互配置

SilenceDetectionConfig

object

否

静默检测配置

Timeout

integer

否

超时时长（毫秒）

5000

RagConfig

object

否

RAG 配置

RagEngine

string

否

RAG 引擎

BAILIAN

Enabled

boolean

否

是否启用 RAG

false

KnowledgeBaseIds

array

否

知识库 ID 列表

string

否

知识库 ID

3457xghryt

TopN

integer

否

取最大多少条数据

5

MaxContentLength

integer

否

RAG 内容最大拼接长度

2000

ToolConfig

object

否

工具配置

McpServers

array<object>

否

MCP 信息配置列表

object

否

Name

string

否

名称

phone-ai-call

BaseUrl

string

否

基础 URL

https://example.com

SseEndpoint

string

否

SSE 路径

/phone-ai-call/mcp/sse?key=value

## 返回参数

名称

类型

描述

示例值

object

Code

string

接口状态码

OK

HttpStatusCode

integer

http 状态码

200

Message

string

返回提示信息

success

RequestId

string

请求 ID

CF6D3484-19A1-5C77-863B-AC8B5754D37C

Data

string

返回结果（VersionId）

20904943-f711-494f-9f1f-e7f340f37707

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "CF6D3484-19A1-5C77-863B-AC8B5754D37C",
  "Data": "20904943-f711-494f-9f1f-e7f340f37707"
}
```

## 错误码

HTTP status code

错误码

错误信息

400

Parameter.Enumeration

The parameter %s must be one of the value of enumeration %s.

400

Parameter.Blank

The parameter %s must not be null or empty.

400

Parameter.Empty

The parameter %s may not be null or empty.

400

Parameter.Null

The parameter %s may not be null.

403

Permission.Unauthorized

You are not authorized to perform this action. %s privileges are required.

404

NotExists.InstanceId

The specified instance %s does not exist.

访问[错误中心](< https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/errorCode>)查看更多错误码。

## 变更历史

变更时间

变更内容概要

操作

2026-05-21

OpenAPI 错误码发生变更、OpenAPI 入参发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/CreateApplicationVersion?updateTime=2026-05-21#workbench-doc-change-demo)

2026-05-20

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/CreateApplicationVersion?updateTime=2026-05-20#workbench-doc-change-demo)

2026-05-12

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/CreateApplicationVersion?updateTime=2026-05-12#workbench-doc-change-demo)

2026-05-06

OpenAPI 错误码发生变更、OpenAPI 入参发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/CreateApplicationVersion?updateTime=2026-05-06#workbench-doc-change-demo)

2026-04-02

OpenAPI 错误码发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/CreateApplicationVersion?updateTime=2026-04-02#workbench-doc-change-demo)

2026-01-28

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/CreateApplicationVersion?updateTime=2026-01-28#workbench-doc-change-demo)
