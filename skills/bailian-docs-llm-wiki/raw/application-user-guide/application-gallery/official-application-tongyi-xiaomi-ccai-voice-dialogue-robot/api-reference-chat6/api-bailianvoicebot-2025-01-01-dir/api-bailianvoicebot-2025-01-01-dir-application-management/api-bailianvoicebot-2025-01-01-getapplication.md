# GetApplication - 获取语音机器人应用

获取语音机器人应用。

## 调试

[您可以在OpenAPI Explorer中直接运行该接口，免去您计算签名的困扰。运行成功后，OpenAPI Explorer可以自动生成SDK代码示例。](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/GetApplication)

[![](https://img.alicdn.com/tfs/TB16JcyXHr1gK0jSZR0XXbP8XXa-24-26.png)调试](https://api.aliyun.com/api/BailianVoiceBot/2025-01-01/GetApplication)

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

bailianvoicebot:GetApplication

get

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

应用 ID。

a395011f-a247-400f-bc69-28796749fd52

## 返回参数

名称

类型

描述

示例值

object

Code

string

code 码

OK

HttpStatusCode

integer

http 状态码

200

Message

string

响应信息

success

RequestId

string

请求 ID

D771A1B6-3D5F-174A-BEE1-98CE1000D337

Data

object

返回数据

ApplicationId

string

应用 ID

a395011f-a247-400f-bc69-28796749fd52

Name

string

应用名称

测试001

Description

string

应用描述

描述一下这个应用

Concurrency

integer

呼叫并发量，即同时在外呼的通话数量。

10

CreatedTime

long

应用创建时间。

1730081561000

UpdatedTime

long

应用修改的时间。

1730081561000

NluEngine

string

Nlu 引擎

PROMPTS

NluAccessType

string

Nlu 访问方式

MANAGED

DraftVersion

object

编辑版配置内容

VersionId

string

版本 ID

743219815472857088

TranscriberConfig

object

ASR 配置

NlsEngine

string

ASR 引擎

枚举值：

-   ALIYUN：ALIYUN。

ALIYUN

NlsAccessType

string

ASR 调用方式

枚举值：

-   MANAGED：MANAGED。

MANAGED

SynthesizerConfig

object

TTS 配置

NlsEngine

string

TTS 引擎

枚举值：

-   ALIYUN：ALIYUN。

ALIYUN

NlsAccessType

string

TTS 调用方式

枚举值：

-   MANAGED：MANAGED。

MANAGED

Voice

string

发音人

aixia

SpeechRate

integer

播报速度

**说明** 取值范围：-500~500。

1

Volume

integer

音量

50

PitchRate

integer

音调

**说明** 取值范围：-500~500。

5

ScriptProfile

object

应用模型配置

Model

string

模型

qwen-plus

Temperature

string

生成过程中的核采样方法概率阈值

**说明**-   例如，取值为 0.8 时，仅保留概率加起来大于等于 0.8 的最可能 token 的最小集合作为候选集。 \* 取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越低，生成的确定性越高

0.8

TopP

string

用于控制模型回复的随机性和多样性

**说明**-   具体来说，temperature 值控制了生成文本时对每个候选词的概率分布进行平滑的程度。 较高的 temperature 值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；而较低的 temperature 值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。
-   取值范围： \[0, 2)，不建议取值为 0，无意义。

0.1

AgentProfile

object

智能体配置信息

ScriptProfileTemplateId

string

应用模版 ID

SFM\_PROMPTS\_DEFAULT

AgentProfileId

string

智能体配置 ID。

6a50b67072d44788951de29758432d94

PromptsJson

string

提示词 json

{"prompts":"我是一个聊天机器人。"}

Description

string

智能体描述

聊天机器人

InteractionConfig

object

交互配置

SilenceDetectionConfig

object

静默检测配置

Timeout

integer

任务执行超时时间，单位秒。

3

RagConfig

object

RAG 配置

RagEngine

string

RAG 引擎

BAILIAN

Enabled

boolean

是否启用 RAG

false

KnowledgeBaseIds

array

知识库 ID 列表

knowledgeBaseIds

string

知识库 ID

8345xghryt

TopN

integer

取最大多少条数据

5

MaxContentLength

integer

RAG 内容最大拼接长度

2000

ToolConfig

object

工具配置

McpServers

array<object>

MCP 信息配置列表

mcpServers

object

Name

string

名称

phone-ai-call

BaseUrl

string

基础 URL

https://example.com

SseEndpoint

string

SSE 路径

/phone-ai-call/mcp/sse?key=value

PublishedVersion

object

已发布应用版本

VersionId

string

版本 ID

47889c1f-dd3f-4ace-9587-a13a3563e678

TranscriberConfig

object

ASR 配置

NlsEngine

string

ASR 引擎

枚举值：

-   ALIYUN：ALIYUN。

ALIYUN

NlsAccessType

string

ASR 调用方式

枚举值：

-   MANAGED：MANAGED。

MANAGED

SynthesizerConfig

object

TTS 配置

NlsEngine

string

TTS 引擎

枚举值：

-   ALIYUN：ALIYUN。

ALIYUN

NlsAccessType

string

TTS 调用方式

枚举值：

-   MANAGED：MANAGED。

MANAGED

Voice

string

发音人

aixia

SpeechRate

integer

播报速度

**说明** 取值范围：-500~500。

\-20

Volume

integer

音量

50

PitchRate

integer

音调

**说明** 取值范围：-500~500。

3

ScriptProfile

object

应用模型配置

Model

string

模型

qwen-plus

Temperature

string

生成过程中的核采样方法概率阈值

**说明**-   例如，取值为 0.8 时，仅保留概率加起来大于等于 0.8 的最可能 token 的最小集合作为候选集。 \* 取值范围为（0,1.0)，取值越大，生成的随机性越高；取值越低，生成的确定性越高

0.8

TopP

string

用于控制模型回复的随机性和多样性

**说明**-   具体来说，temperature 值控制了生成文本时对每个候选词的概率分布进行平滑的程度。 较高的 temperature 值会降低概率分布的峰值，使得更多的低概率词被选择，生成结果更加多样化；而较低的 temperature 值则会增强概率分布的峰值，使得高概率词更容易被选择，生成结果更加确定。
-   取值范围： \[0, 2)，不建议取值为 0，无意义。

0.1

AgentProfile

object

智能体配置信息

ScriptProfileTemplateId

string

智能体配置模版 ID

SFM\_PROMPTS\_DEFAULT

AgentProfileId

string

智能体配置 ID

b97b6822dd624c32b6c2a54d717db718

PromptsJson

string

提示词 json

{"prompts":"我是一个聊天机器人。"}

Description

string

智能体描述

我是一个聊天机器人

InteractionConfig

object

交互配置

SilenceDetectionConfig

object

静默检测配置

Timeout

integer

超时时长。

30

RagConfig

object

RAG 配置

RagEngine

string

RAG 引擎

BAILIAN

Enabled

boolean

是否启用 RAG

false

KnowledgeBaseIds

array

知识库 ID 列表

knowledgeBaseIds

string

知识库 ID

3472xghryt

TopN

integer

取最大多少条数据

5

MaxContentLength

integer

RAG 内容最大拼接长度

2000

ToolConfig

object

工具配置

McpServers

array<object>

MCP 信息配置列表

mcpServers

object

Name

string

名称。

phone-ai-call

BaseUrl

string

基础 URL

https://example.com

SseEndpoint

string

SSE 路径

/phone-ai-call/mcp/sse?key=value

## 示例

正常返回示例

`JSON`格式

```
{
  "Code": "OK",
  "HttpStatusCode": 200,
  "Message": "success",
  "RequestId": "D771A1B6-3D5F-174A-BEE1-98CE1000D337",
  "Data": {
    "ApplicationId": "a395011f-a247-400f-bc69-28796749fd52\n",
    "Name": "测试001\n",
    "Description": "描述一下这个应用\n",
    "Concurrency": 10,
    "CreatedTime": 1730081561000,
    "UpdatedTime": 1730081561000,
    "NluEngine": "PROMPTS",
    "NluAccessType": "MANAGED",
    "DraftVersion": {
      "VersionId": 743219815472857100,
      "TranscriberConfig": {
        "NlsEngine": "ALIYUN",
        "NlsAccessType": "MANAGED",
        "NlsAccessProfile": {
          "AccessProfileId": ""
        },
        "VocabularyId": "",
        "EndSilenceTimeout": 0,
        "CustomizationId": "",
        "SpeechNoiseThreshold": 0,
        "Model": "",
        "CorrectionRules": [
          {
            "Pattern": "",
            "Replacement": ""
          }
        ]
      },
      "SynthesizerConfig": {
        "NlsEngine": "ALIYUN",
        "NlsAccessType": "MANAGED",
        "Voice": "aixia",
        "SpeechRate": 1,
        "Volume": 50,
        "PitchRate": 5,
        "NlsAccessProfile": {
          "AccessProfileId": ""
        },
        "Model": "",
        "PronRules": [
          {
            "Pattern": "",
            "Replacement": ""
          }
        ]
      },
      "ScriptProfile": {
        "Model": "qwen-plus",
        "Temperature": 0.8,
        "TopP": 0.1,
        "AgentProfile": {
          "ScriptProfileTemplateId": "SFM_PROMPTS_DEFAULT",
          "AgentProfileId": "6a50b67072d44788951de29758432d94",
          "PromptsJson": {
            "prompts": "我是一个聊天机器人。"
          },
          "Description": "聊天机器人"
        }
      },
      "InteractionConfig": {
        "SilenceDetectionConfig": {
          "Timeout": 3
        }
      },
      "RagConfig": {
        "RagEngine": "BAILIAN",
        "Enabled": false,
        "KnowledgeBaseIds": [
          "8345xghryt"
        ],
        "TopN": 5,
        "MaxContentLength": 2000
      },
      "ToolConfig": {
        "McpServers": [
          {
            "Name": "phone-ai-call",
            "BaseUrl": "https://example.com",
            "SseEndpoint": "/phone-ai-call/mcp/sse?key=value"
          }
        ]
      }
    },
    "PublishedVersion": {
      "VersionId": "47889c1f-dd3f-4ace-9587-a13a3563e678",
      "TranscriberConfig": {
        "NlsEngine": "ALIYUN",
        "NlsAccessType": "MANAGED",
        "NlsAccessProfile": {
          "AccessProfileId": ""
        },
        "VocabularyId": "",
        "EndSilenceTimeout": 0,
        "CustomizationId": "",
        "SpeechNoiseThreshold": 0,
        "Model": "",
        "CorrectionRules": [
          {
            "Pattern": "",
            "Replacement": ""
          }
        ]
      },
      "SynthesizerConfig": {
        "NlsEngine": "ALIYUN",
        "NlsAccessType": "MANAGED",
        "Voice": "aixia",
        "SpeechRate": -20,
        "Volume": 50,
        "PitchRate": 3,
        "NlsAccessProfile": {
          "AccessProfileId": ""
        },
        "Model": "",
        "PronRules": [
          {
            "Pattern": "",
            "Replacement": ""
          }
        ]
      },
      "ScriptProfile": {
        "Model": "qwen-plus\n",
        "Temperature": 0.8,
        "TopP": 0.1,
        "AgentProfile": {
          "ScriptProfileTemplateId": "SFM_PROMPTS_DEFAULT",
          "AgentProfileId": "b97b6822dd624c32b6c2a54d717db718",
          "PromptsJson": {
            "prompts": "我是一个聊天机器人。"
          },
          "Description": "我是一个聊天机器人"
        }
      },
      "InteractionConfig": {
        "SilenceDetectionConfig": {
          "Timeout": 30
        }
      },
      "RagConfig": {
        "RagEngine": "BAILIAN",
        "Enabled": false,
        "KnowledgeBaseIds": [
          "3472xghryt"
        ],
        "TopN": 5,
        "MaxContentLength": 2000
      },
      "ToolConfig": {
        "McpServers": [
          {
            "Name": "phone-ai-call",
            "BaseUrl": "https://example.com",
            "SseEndpoint": "/phone-ai-call/mcp/sse?key=value"
          }
        ]
      }
    }
  }
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

OpenAPI 错误码发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GetApplication?updateTime=2026-05-21#workbench-doc-change-demo)

2026-05-20

OpenAPI 错误码发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GetApplication?updateTime=2026-05-20#workbench-doc-change-demo)

2026-05-12

OpenAPI 错误码发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GetApplication?updateTime=2026-05-12#workbench-doc-change-demo)

2026-05-06

OpenAPI 错误码发生变更、OpenAPI 返回结构发生变更

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GetApplication?updateTime=2026-05-06#workbench-doc-change-demo)

2026-01-28

新增 OpenAPI

[查看变更详情](https://api.aliyun.com/document/BailianVoiceBot/2025-01-01/GetApplication?updateTime=2026-01-28#workbench-doc-change-demo)
