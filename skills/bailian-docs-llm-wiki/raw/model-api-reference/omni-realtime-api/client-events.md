# 客户端事件

Qwen-Omni-Realtime API的客户端事件参考。

## session.update

建立 WebSocket 连接后，发送此事件更新会话的默认配置。服务端收到 `session.update` 事件后校验参数，若参数不合法则返回错误，若参数合法则应用更改并返回会话配置。Qwen3.8-Omni-Flash-Realtime 的 MCP 连接地址与凭证不回显，详见[Qwen3.8 客户端事件](#qwen38-client)。

**type**`string`**（必选）**

事件类型，固定为 `session.update`。

```
{
    "event_id": "event_ToPZqeobitzUJnt3QqtWg",
    "type": "session.update",
    "session": {
        "modalities": [
            "text",
            "audio"
        ],
        "model": "qwen3.5-omni-flash-realtime",
        "voice": "Tina",
        "audio": {
            "input": {
                "format": {
                    "type": "pcm",
                    "sample_rate": 16000
                }
            },
            "output": {
                "format": {
                    "type": "wav",
                    "sample_rate": 24000
                }
            }
        },
        "instructions": "你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 800
        },
        "enable_search": true,
        "search_options": {
            "enable_source": true
        },
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "当你想查询指定城市的天气时非常有用。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ],
        "seed": 1314,
        "max_tokens": 16384,
        "repetition_penalty": 1.05,
        "presence_penalty": 0.0,
        "top_k": 50,
        "top_p": 1.0,
        "temperature": 0.9
    }
}
```

**session**`object`（可选）

会话配置。

属性

**modalities**`array`（可选）

模型输出模态设置，可选值：

-   \["text"\]
    
    仅输出文本。
    
-   \["text","audio"\]（默认值）
    
    同时输出文本和音频。
    

**voice**`string`（可选）

模型生成音频的音色，支持的音色参见[音色列表](https://help.aliyun.com/zh/model-studio/realtime#f4c9fd97f221z)。

默认音色：

-   Qwen3.5-Omni-Realtime 系列模型：`Tina`
-   Qwen3-Omni-Flash-Realtime：`Cherry`
-   Qwen-Omni-Turbo-Realtime：`Chelsie`

**audio**`object`（可选）

输入和输出音频配置。未配置时沿用现有默认行为。

**以下格式和采样率选项适用于 `qwen3.5-omni-plus-realtime`、`qwen3.5-omni-flash-realtime`。**Qwen3.8-Omni-Flash-Realtime 的输入格式字段和约束见[Qwen3.8 客户端事件](#qwen38-client)，未列出的字段沿用基础协议。

属性

**audio.input**`object`（可选）

用户输入音频配置。

**audio.input.format**`object`（可选）

用户输入音频的格式和采样率。建议在会话 IDLE 阶段（首次发送音频前）完成配置，发送音频后不可再修改。

**audio.input.format.type**`string`（可选）

用户输入音频格式。可选值：`pcm`（默认值，单声道、16 bit 裸 PCM）、`wav`（WAV 容器封装的单声道、16 bit PCM）。

**audio.input.format.sample\_rate**`integer`（可选）

用户输入音频采样率，单位为 Hz。可选值：`8000`、`16000`（默认值）、`24000`、`48000`。

**audio.output**`object`（可选）

模型输出音频配置。

**audio.output.format**`object`（可选）

模型输出音频的格式和采样率。建议在会话建立初期、尚未开始音频交互前完成配置。

**audio.output.format.type**`string`（可选）

模型输出音频格式。可选值：`pcm`（默认值，单声道、16 bit 裸 PCM）、`wav`（WAV 容器封装的单声道、16 bit PCM）。

**audio.output.format.sample\_rate**`integer`（可选）

模型输出音频采样率，单位为 Hz。可选值：`8000`、`16000`、`24000`（默认值）、`48000`。

**input\_audio\_format**`string`（可选）

历史兼容字段，新增接入建议使用 `audio.input.format` 同时配置输入格式和采样率。

**output\_audio\_format**`string`（可选）

历史兼容字段，新增接入建议使用 `audio.output.format` 同时配置输出格式和采样率。

**smooth\_output**`boolean｜null`（可选）

**仅在使用 Qwen3-Omni-Flash-Realtime 系列模型时生效。**

控制回复风格。可选值：

-   `true`（默认值）：口语化风格。
    
-   `false`：书面化、正式风格。
    
    > 难以朗读的内容可能效果不好。
    
-   `null`：模型自动选择口语化或书面化风格。
    

**instructions**`string`（可选）

系统消息，用于设定模型的目标或角色。

**turn\_detection**`object`（可选）

语音活动检测（VAD）配置。设为 `null` 可禁用 VAD，改为手动触发模型响应。若不提供此字段，系统将使用默认参数启用 VAD。

属性

**type**`string`（可选）

VAD 类型，可选值：

-   `server_vad`（默认值）：基于声学特征检测语音结束。
-   `semantic_vad`：基于语义有效性检测语音结束，可过滤回应语、背景音等无意义声音。Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列模型支持。

**threshold**`float`（可选）

VAD 灵敏度。值越低，VAD 越灵敏，越容易将微弱声音（包括背景噪音）识别为语音；值越高，越不灵敏，需要更清晰、音量更大的语音才能触发。

取值范围：`[-1.0, 1.0]`，默认值为 0.5。

**silence\_duration\_ms**`integer`（可选）

语音结束后需保持静音的最短时间（毫秒），超时即触发模型响应。值越低，响应越快，但可能在短暂停顿时误触发。

取值范围：\[200, 6000\]，默认值为 800。

**idle\_timeout\_ms**`integer`（可选）

**仅在使用 `qwen3.5-omni-plus-realtime` 或 `qwen3.5-omni-flash-realtime` 模型且 VAD 类型为 `server_vad` 时生效。**

静默超时时间（毫秒）。服务端完成音频播报且用户持续静默超过该时间（未触发 `speech.started`）后，模型将主动触发一轮响应，基于当前上下文引导用户继续对话。超时计时从上一条模型响应的音频播放完毕后开始。

取值范围：\[5000, 30000\]。

**enable\_search**`boolean`（可选）

适用于 Qwen3.8-Omni-Flash-Realtime 和 Qwen3.5-Omni-Realtime 系列模型。

是否启用联网搜索。设为 `true` 启用，默认为 `false`。启用后，模型可自主判断是否需要联网搜索来回答用户问题。

> tools 和 enable\_search 不兼容，不可同时开启。

**search\_options**`object`（可选）

联网搜索选项配置，需先启用 `enable_search` 才生效。

属性

**enable\_source**`boolean`（可选）

是否在响应中返回搜索结果来源列表。设为 `true` 启用。

**tools**`array`（可选）

工具定义列表。配置后模型可根据用户输入自主决定是否调用工具。

以下属性描述自定义 Function Calling 工具。Qwen3.8-Omni-Flash-Realtime 的 MCP 工具配置见[3.8 客户端事件](#qwen38-client)。

属性

**type**`string`（必选）

自定义 Function Calling 工具固定为 `function`。

**function.name**`string`（必选）

工具函数名称，建议与函数名保持一致，例如 `get_current_weather` 或 `get_current_time`。

**function.description**`string`（可选）

对工具函数功能的描述，模型据此判断是否调用该工具。

**function.parameters**`object`（可选）

对工具函数入参的描述，模型据此提取所需入参。若函数无需入参，可不指定。

属性

**type**`string`（必选）

固定为 `object`。

**properties**`object`（可选）

描述各入参的名称、数据类型与说明。Key 为入参名称，Value 为包含数据类型（`type`）和描述（`description`）的对象。

**required**`array`（可选）

指定哪些入参为必填项。

**temperature**`float`（可选）

采样温度，控制输出内容的多样性。值越高，输出越多样；值越低，输出越确定。

取值范围：\[0, 2)。

由于 temperature 和 top\_p 均可控制多样性，建议只设置其中一个。

默认值：

-   `qwen3.8-omni-flash-realtime`：0.6
-   Qwen3.5-Omni-Realtime 系列模型：0.7
-   `qwen3-omni-flash-realtime` 系列：0.9
-   `qwen-omni-turbo-realtime` 系列：1.0

> `qwen-omni-turbo` 系列模型**不支持修改**。

**top\_p**`float`（可选）

核采样概率阈值，控制输出内容的多样性。值越高，输出越多样；值越低，输出越确定。

取值范围：(0, 1.0\]。

由于 temperature 和 top\_p 均可控制多样性，建议只设置其中一个。

默认值：

-   `qwen3.8-omni-flash-realtime`：0.95
-   Qwen3.5-Omni-Realtime 系列模型：0.8
-   `qwen3-omni-flash-realtime` 系列：1.0
-   `qwen-omni-turbo-realtime` 系列：0.01

> `qwen-omni-turbo` 系列模型**不支持修改**。

**top\_k**`integer`（可选）

采样候选集大小。例如设为 50 时，每步生成仅从得分最高的 50 个 Token 中采样。值越大，随机性越高；值越小，确定性越高。设为 `null` 或大于 100 时，禁用 top\_k 策略，仅 `top_p` 生效。

取值需大于或等于 0。

默认值：

-   `qwen3.8-omni-flash-realtime`：20
-   Qwen3.5-Omni-Realtime 系列模型：20
-   `qwen3-omni-flash-realtime` 系列：50
-   `qwen-omni-turbo-realtime` 系列：20

> `qwen-omni-turbo` 系列模型**不支持修改**。

**max\_tokens**`integer`（可选）

本次请求返回的最大 Token 数。

> `max_tokens` 不影响模型的生成过程。若模型生成的 Token 数超过 `max_tokens`，响应将被截断。

`qwen3.8-omni-flash-realtime` 的取值范围为 \[1, 65536\]。其他模型的默认值和最大值均为模型的最大输出长度，各模型的最大输出长度参见[模型列表](raw/model-user-guide/get-started-with-models/models.md)。

适用于需要限制输出长度的场景，如生成摘要或关键词、控制成本、缩短响应时间等。

> `qwen-omni-turbo` 系列模型**不支持修改**。

**repetition\_penalty**`float`（可选）

控制生成内容中连续序列的重复度。值越高，重复惩罚越强；1.0 表示不做惩罚。`qwen3.8-omni-flash-realtime` 支持取值 0；其他模型取值需大于 0，无严格上限。

默认值：

-   `qwen3.8-omni-flash-realtime`：0
-   Qwen3.5-Omni-Realtime 系列模型：1.0
-   `qwen3-omni-flash-realtime` 系列：1.05
-   `qwen-omni-turbo-realtime` 系列：1.05

> `qwen-omni-turbo` 系列模型**不支持修改**。

**presence\_penalty** `float`（可选）

控制生成内容的重复度。

取值范围：\[-2.0, 2.0\]。正数降低重复度，负数增加重复度。

默认值：

-   `qwen3.8-omni-flash-realtime`：1
-   Qwen3.5-Omni-Realtime 系列模型：1.5
-   `qwen3-omni-flash-realtime` 系列：0.0
-   `qwen-omni-turbo-realtime` 系列：0.0

适用场景：

较高值适合创意写作、头脑风暴等需要多样性和创造性的场景。

较低值适合技术文档等需要一致性和专业术语的场景。

> `qwen-omni-turbo` 系列模型**不支持修改**。

**seed**`integer`（可选）

提高生成过程的确定性，常用于在相同参数下复现相同结果。

每次调用时传入相同的 seed 值并保持其他参数不变，模型将尽可能返回相同的结果。

取值范围：0 到 231−1，默认值为 -1。

> `qwen-omni-turbo` 系列模型**不支持修改**。

### Qwen3.8-Omni-Flash-Realtime

本节介绍 `qwen3.8-omni-flash-realtime` 的 `session.update` 配置字段。表中“必填”表示所属对象出现时必须提供。ID 均为不透明字符串，不应依赖其长度、前缀或生成规则。MCP 连接、工具发现和调用受服务配额及超时限制。

`qwen3.8-omni-flash-realtime` 的全部输入 Token 总数上限为 196608，输入长度计算规则与 Qwen3.5-Omni-Realtime 一致。

事件顶层包含以下字段：

字段路径

类型

必填

说明

type

string

是

固定为 session.update

session

object

是

本次更新的会话配置

#### session.audio.input.format

以下多通道音频配置适用于 WebSocket 接入。

字段路径

类型

必填与默认值

允许值与约束

说明

type

string

可选，默认 pcm

多通道输入只能为 pcm

输入音频编码类型

sample\_rate

integer

可选，默认 16000

多通道输入只能为 16000

采样率，单位 Hz

sample\_format

string

可选，默认 s16le

只能为 s16le

PCM 采样格式

channels

integer

可选，默认 1

仅支持 1、2、4

输入声道数；2、4 声道空间音频的输入 Token 数均为普通音频的 2 倍，详见[Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)

packing

string

可选，默认 interleaved

只能为 interleaved

多通道样本排列方式

channel\_layout

string

可选，按 channels 确定默认值

1 声道为 mono；2 声道为 raw\_mic\_array；4 声道为 foa\_ambix

显式提供时必须与 channels 匹配

使用限制：

-   多通道输入必须使用 PCM、16000 Hz、s16le 和 interleaved。
-   多通道配置应在发送首段音频数据前完成；音频输入开始后，不得修改上述音频格式配置。
-   字段省略时使用表中默认值；字段一旦出现，其类型和值必须满足约束，不得传入 null 代替省略。

双通道示例：

```
{
  "type": "session.update",
  "session": {
    "audio": {
      "input": {
        "format": {
          "type": "pcm",
          "sample_rate": 16000,
          "sample_format": "s16le",
          "channels": 2,
          "packing": "interleaved",
          "channel_layout": "raw_mic_array"
        }
      }
    }
  }
}
```

四通道示例：

```
{
  "type": "session.update",
  "session": {
    "audio": {
      "input": {
        "format": {
          "type": "pcm",
          "sample_rate": 16000,
          "sample_format": "s16le",
          "channels": 4,
          "packing": "interleaved",
          "channel_layout": "foa_ambix"
        }
      }
    }
  }
}
```

单通道兼容示例：

```
{
  "type": "session.update",
  "session": {
    "audio": {
      "input": {
        "format": {
          "type": "pcm",
          "sample_rate": 16000
        }
      }
    }
  }
}
```

#### session.video.input.representation\_compact

字段路径

类型

必填与默认值

允许值

说明

representation\_compact

string

可选；会话初始默认 none

none、normal

视频输入表征聚合方式

取值说明：

-   none：保留完整的细粒度视频输入表征。
-   normal：聚合视频输入表征，使用后会降低计算开销，适用于对视觉细节要求不高的场景。相同视频输入的 Token 数为 `none` 模式的 1/4，详见[Token 计算](https://help.aliyun.com/zh/model-studio/realtime#cfba3898e4d0h)。

该字段应在发送首段音频数据前设置；音频输入开始后不得修改。

示例：

```
{
  "type": "session.update",
  "session": {
    "video": {
      "input": {
        "representation_compact": "normal"
      }
    }
  }
}
```

#### session.audio.output.voice

字段路径

类型

必填

说明

session.audio.output.voice

string

否

输出音色；默认为 Tina；新增支持 longanlingxin

session.voice

string

否

兼容字段；建议新接入使用 session.audio.output.voice

如果两个字段同时出现，以 `session.audio.output.voice` 为准。音色效果可参考[音色列表](https://help.aliyun.com/zh/model-studio/omni-voice-list#qwen38-voices)。

示例：

```
{
  "type": "session.update",
  "session": {
    "audio": {
      "output": {
        "voice": "longanlingxin"
      }
    }
  }
}
```

#### session.tools 数组元素

当 `session.tools` 中的元素满足 `type="mcp"` 时，该元素表示一个 MCP Server 配置。同一会话可同时配置 Function Calling 和 MCP 工具；`tools` 与 `enable_search` 不可同时开启，该限制也适用于 MCP。服务数量、工具数量、超时及结果大小限制见[MCP 调用限制](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process#qwen38-mcp-flow)。

字段路径

类型

必填与默认值

允许值与约束

说明

type

string

必填

新增支持mcp

工具配置类型

server\_label

string

必填

会话内唯一；1～64 位；仅允许字母、数字、下划线和连字符

MCP Server 的会话内标识

server\_url

string

必填

公网 HTTPS 443 地址；最长 4096 字符

MCP Streamable HTTP 地址

authorization

string

可选

最长 8192 字符；仅允许可打印 ASCII 字符

出站 Authorization 值

headers

object

可选

最多 16 个键值对；键和值均为 string

额外出站 HTTP Header

allowed\_tools

array\[string\]

可选；省略表示允许全部；空数组表示不暴露任何工具

每个工具名 1～64 位；仅允许字母、数字、下划线、点和连字符

工具发现后的白名单过滤

require\_approval

string

可选，默认 always

always、never

工具调用审批策略

`server_url` 还必须满足以下要求：

-   不得包含用户名或密码。
-   不得包含 URL fragment。
-   域名解析结果必须为公网地址。

`headers` 的名称长度为 1～128 位，仅允许标准 HTTP Header 名称字符；值最长 8192 字符且仅允许可打印 ASCII 字符。以下 Header 不允许设置：

```
前缀：mcp-、proxy-、x-forwarded-

名称：host、authorization、connection、content-length、transfer-encoding、
accept、content-type、forwarded、cookie、origin、upgrade、te、trailer
```

每次新增或更新 MCP 配置时，都必须同时提供 `server_label` 和 `server_url`，不支持只传 `server_label` 复用已有配置。MCP 配置只能在当前没有活动 Response 时更新。

`server_url`、`authorization` 和 `headers` 仅用于服务端连接 MCP Server，不会在 `session.updated` 中回显。客户端不应依赖 `session.updated` 重建这些敏感配置。

配置示例：将 `server_url` 替换为可访问的 MCP 服务地址，`authorization` 替换为该服务要求的认证信息；`allowed_tools` 中填写该服务实际提供的工具名。

```
{
  "type": "session.update",
  "session": {
    "tools": [
      {
        "type": "mcp",
        "server_label": "amap",
        "server_url": "https://example.com/mcp",
        "authorization": "Bearer ***",
        "allowed_tools": ["maps_weather"],
        "require_approval": "always"
      }
    ]
  }
}
```

## response.create

`response.create` 事件用于指示服务端生成模型响应。VAD 模式下，服务端会自动生成响应，无需发送此事件。工具调用场景中，客户端通过 `conversation.item.create` 回传工具结果后，需发送此事件触发模型生成最终响应。

服务端以 `response.created` 事件开始响应，随后发送一个或多个项和内容事件（如 `conversation.item.created` 和 `response.content_part.added`），最后以 `response.done` 事件表示响应完成。

**type**`string`（必选）

事件类型，固定为 `response.create`。

```
{
    "type": "response.create",
    "event_id": "event_1718624400000"
}
```

## response.cancel

客户端发送此事件取消正在进行的响应。若当前无响应可取消，服务端将返回错误事件。

**type**`string`（必选）

事件类型，固定为 `response.cancel`。

```
{
    "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
    "type": "response.cancel"
}
```

## input\_audio\_buffer.append

将音频字节追加到输入音频缓冲区。

**type**`string`（必选）

事件类型，固定为 `input_audio_buffer.append`。

```
{
    "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
    "type": "input_audio_buffer.append",
    "audio": "UklGR..."
}
```

**audio**`string`（必选）

Base64 编码的音频数据。

## input\_audio\_buffer.commit

提交输入音频缓冲区，在对话中创建新的用户消息项。若音频缓冲区为空，服务端将返回错误事件。

-   [VAD 模式](raw/model-user-guide/model-experience/omni-modal/realtime.md)：服务端自动提交音频缓冲区，客户端无需发送此事件。
-   [Manual 模式](raw/model-user-guide/model-experience/omni-modal/realtime.md)：客户端必须提交音频缓冲区才能创建用户消息项。

提交音频缓冲区不会触发模型响应，服务端将以 `input_audio_buffer.committed` 事件响应。

> 若客户端已发送过 [input\_image\_buffer.append](https://help.aliyun.com/zh/model-studio/client-events#c28ed38410nfw) 事件，input\_audio\_buffer.commit 事件将同时提交图像缓冲区。

**type**`string`（必选）

事件类型，固定为 `input_audio_buffer.commit`。

```
{
    "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
    "type": "input_audio_buffer.commit"
}
```

## input\_audio\_buffer.clear

清除音频缓冲区中的字节。服务端以 `input_audio_buffer.cleared` 事件响应。

**type**`string`（必选）

事件类型，固定为 `input_audio_buffer.clear`。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.clear"
}
```

## input\_image\_buffer.append

将图像数据添加到图像缓冲区。图像可来自本地文件，也可从视频流实时采集。

图片输入限制如下：

-   图像格式必须为 JPG 或 JPEG。建议分辨率为 480p 或 720p 以获得最佳性能，最高不超过 1080p。
-   单张图片经Base64编码后不得超过256KB，建议编码前原始图片大小不超过190KB。
-   图片数据需经过 Base64 编码。
-   建议以 1 张/秒的频率向服务端发送图像。
-   发送 input\_image\_buffer.append 事件前，至少已发送过一次 input\_audio\_buffer.append 事件。

> 图像缓冲区与音频缓冲区通过 [input\_audio\_buffer.commit](https://help.aliyun.com/zh/model-studio/client-events#1cbea5fa7fkfl) 事件一起提交。

**type**`string`（必选）

事件类型，固定为 `input_image_buffer.append`。

```
{
    "event_id": "event_xxx",
    "type": "input_image_buffer.append",
    "image": "xxx"
}
```

**image**`string`（必选）

Base64 编码的图像数据。

## conversation.item.create

客户端发送此事件，将工具函数的执行结果回传给服务端。模型触发工具调用后，客户端在本地执行工具函数，通过此事件将结果发回，再发送 `response.create` 触发模型生成最终响应。

**说明**此处说明 `function_call_output` 类型的 item；Qwen3.8-Omni-Flash-Realtime 还支持[审批回复 `mcp_approval_response`](#qwen38-mcp-approval-response)。

**type**`string`（必选）

事件类型，固定为 `conversation.item.create`。

```
{
    "event_id": "event_55099cddb51b4f208cb95d1a994eef80",
    "type": "conversation.item.create",
    "item": {
        "id": "item_2a80d7682b4e473c9c2154da135041e9",
        "type": "function_call_output",
        "call_id": "call_62c24725afdb4c2680ac54",
        "output": "北京今天天气为霾转晴，气温4/-4℃，微风"
    }
}
```

**item**`object`（必选）

要创建的对话项，不能为空。

属性

**id**`string`（可选）

对话项 ID。可预先指定以对齐本地状态；若未提供，由服务端生成。

**type**`string`（必选）

此处对话项类型为 `function_call_output`；MCP 审批回复的结构见[审批回复](#qwen38-mcp-approval-response)。

**call\_id**`string`（必选）

`response.function_call_arguments.done` 事件中返回的 `call_id`。

**output**`string`（必选）

工具函数的执行结果。

### MCP 审批回复（Qwen3.8-Omni-Flash-Realtime）

当 MCP 配置的 `require_approval` 为 always 或省略时，服务端可能发送 `mcp_approval_request`。客户端使用既有 `conversation.item.create` 事件回复审批结果。

事件字段：

字段路径

类型

必填

说明

event\_id

string

否

客户端生成的事件 ID，用于日志追踪

type

string

是

固定为 conversation.item.create

item

object

是

MCP 审批回复对象

item 字段：

字段路径

类型

必填

说明

item.type

string

是

固定为 mcp\_approval\_response

item.approval\_request\_id

string

是

必须精确匹配一个尚未处理的 mcp\_approval\_request 的 item.id

item.approve

boolean

是

true 表示允许执行；false 表示拒绝，本次调用进入 failed

示例：

```
{
  "event_id": "event_client_xxx",
  "type": "conversation.item.create",
  "item": {
    "type": "mcp_approval_response",
    "approval_request_id": "opaque_approval_id",
    "approve": true
  }
}
```

> 另请参见： [实时（Qwen-Omni-Realtime）](raw/model-user-guide/model-experience/omni-modal/realtime.md) 。
