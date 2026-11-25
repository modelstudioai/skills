# 三方Agent接入

如果多模态交互开发套件里内置的技能或Agent不满足需求，可以参考本文调用三方Agent的能力。

<a id="协议标准"></a>

<a id="a1f8ffb27f8qc"></a>

## 协议标准

需基于Google A2A协议进行集成（参见[A2A 0.2.5规范](https://a2aproject.github.io/A2A/latest/specification/)）

<a id="接入流程"></a>

<a id="95346d033fdl4"></a>

## 接入流程

<a id="1-配置agentcard"></a>

<a id="f9b165a09422s"></a>

### 1\. 配置AgentCard

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7028182571/p986101.png)

-   步骤3的返回结果及示例，请参见[AgentCard](multimodal-integration-a2a-9862d72fb0298480.md#854b8c0b10ozm)。

<a id="2-调用agent"></a>

<a id="c47d4db837br9"></a>

### 2\. 调用Agent

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7028182571/p986102.png)

-   步骤4的请求参数及示例，请参见[Agent调用请求字段](multimodal-integration-a2a-9862d72fb0298480.md#f5598eb155aob)。
-   步骤6返回结果及示例，请参见[Agent调用返回字段](multimodal-integration-a2a-9862d72fb0298480.md#6e74c0e6d8uwa)。

<a id="字段说明"></a>

<a id="85e9c48b55aj2"></a>

## 字段说明

<a id="agentcard"></a>

<a id="854b8c0b10ozm"></a>

### AgentCard

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| name | String | 是 | Agent名称。 |
| description | String | 是 | Agent描述。 |
| url | String | 是 | Agent服务的基础HTTPS URL。<br><br>支持流式传输时自动添加`/stream`路径后缀。 |
| version | String | 是 | Agent版本。 |
| protocolVersion | String | 是 | Agent支持的A2A协议版本。 |
| capabilities | [AgentCapabilities](multimodal-integration-a2a-9862d72fb0298480.md#8eb8061367cb6) | 是 | 指定支持的可选 A2A 协议功能（例如，流式传输）。 |
| security | String\[\] | 否 | 与Agent进行通信的安全要求。<br><br>目前支持apiKey安全策略，当配置时向Agent发起的请求中会包含如下Header：<br><br>`X-API-KEY: <value> //在管控台中的配置项 ` 。 |
| defaultInputModes | String\[\] | 是 | Agent接受的输入媒体类型。<br><br>当前支持："text/plain" |
| defaultOutputModes | String\[\] | 是 | Agent生成的输出媒体类型。<br><br>当前支持："text/plain" |
| skills | [AgentSkill](multimodal-integration-a2a-9862d72fb0298480.md#9567dc941c71f)\[\] | 是 | Agent技能列表（至少1项目）。 |

<a id="agentcapabilities"></a>

<a id="8eb8061367cb6"></a>

#### AgentCapabilities

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| streaming | Boolean | 否 | 是否支持 SSE 流式传输。 |
| extensions | [AgentExtension](multimodal-integration-a2a-9862d72fb0298480.md#dc95f15495kh2)\[\] | 否 | 支持的扩展列表。 |

<a id="agentextension"></a>

<a id="dc95f15495kh2"></a>

#### AgentExtension

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| uri | String | 是 | 支持的扩展的 URI，包含对扩展能力的说明。 |
| params | Map<String, Object> | 否 | 配置参数。 |

<a id="agentskill"></a>

<a id="9567dc941c71f"></a>

#### AgentSkill

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| id | String | 是 | Agent内的唯一技能标识符。 |
| name | String | 是 | 技能名称。 |
| description | String | 是 | 技能描述。 |
| tags | String\[\] | 是 | 技能关键词。 |
| examples | String\[\] | 否 | 技能使用示例。 |
| inputModes | String\[\] | 否 | 接收的媒体类型，设置时会覆盖`defaultInputModes`。 |
| outputModes | String\[\] | 否 | 输出的媒体类型，设置时会覆盖`defaultOutputModes`。 |

<a id="示例"></a>

<a id="636c3c5b59stt"></a>

#### 示例

<a id="code-block"></a>

```json
{
  "name": "超级AI助理",
  "description": "可以复读用户的话，计算两个数'相加'，记录并数出用户说了几句话，进行闪光，可以教你打蓝球、踢足球。总之，无所不能",
  "protocolVersion": "0.2.5",
  "url": "https://example/a2a/demo/v1",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "extensions": []
  },
  "security": [],
  "defaultInputModes": [
    "text/plain"
  ],
  "defaultOutputModes": [
    "text/plain"
  ],
  "skills": [
    {
      "id": "ai-repeat",
      "name": "AI复读",
      "description": "重复用户说的话",
      "tags": [
        "demo",
        "repeat"
      ],
      "examples": [
        "示例: 重复我说的话"
      ]
    },
    {
      "id": "ai-calculate",
      "name": "AI计算",
      "description": "计算两个数'相加'",
      "tags": [
        "demo",
        "calculate"
      ],
      "examples": [
        "示例: 1与2相加是多少"
      ]
    },
    {
      "id": "ai-count",
      "name": "AI数数",
      "description": "记录并数出用户说了几句话",
      "tags": [
        "demo",
        "count"
      ],
      "examples": [
        "示例: 数一下我说了几句话"
      ]
    },
    {
      "id": "ai-flash",
      "name": "AI闪光",
      "description": "可以进行闪光",
      "tags": [
        "demo",
        "flash"
      ],
      "examples": [
        "示例: 进行闪光"
      ]
    },
    {
      "id": "ai-coach",
      "name": "AI教练",
      "description": "可以教你打蓝球、踢足球",
      "tags": [
        "demo",
        "coach"
      ],
      "examples": [
        "示例: 如何打好蓝球"
      ]
    }
  ]
}
```

<a id="agent调用请求字段"></a>

<a id="f5598eb155aob"></a>

### Agent调用请求字段

<table><thead><tr><th><p><strong>字段名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必填</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>jsonrpc</p></td><td><p>String</p></td><td><p>是</p></td><td><p>固定为：&quot;2.0&quot;。</p></td></tr><tr><td><p>method</p></td><td><p>String</p></td><td><p>是</p></td><td><ul><li><p><code>&quot;message/stream&quot;</code>：支持SSE流式请求。</p></li><li><p><code>&quot;message/send&quot;</code>：不支持SSE流式请求。</p></li></ul></td></tr><tr><td><p>params</p></td><td><p><a href="multimodal-integration-a2a-9862d72fb0298480.md#7ae5771db9x5k">MessageSendParams</a></p></td><td><p>是</p></td><td><p>请求参数。</p></td></tr><tr><td><p>id</p></td><td><p>String</p></td><td><p>是</p></td><td><p>请求ID。</p></td></tr></tbody></table>

<a id="messagesendparams"></a>

<a id="7ae5771db9x5k"></a>

#### MessageSendParams

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| message | [Message](multimodal-integration-a2a-9862d72fb0298480.md#ad7fc73eeelos) | 是 | 要发送的消息内容 |

<a id="message"></a>

<a id="ad7fc73eeelos"></a>

#### Message

<table><thead><tr><th><p><strong>字段名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必填</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>kind</p></td><td><p>String</p></td><td><p>是</p></td><td><p>固定为：&quot;message&quot;。</p></td></tr><tr><td><p>role</p></td><td><p>String</p></td><td><p>是</p></td><td><ul><li><p>&quot;user&quot; ：表示当前消息是用户发送的消息。</p></li><li><p>&quot;agent&quot; ：表示当前消息是Agent返回的消息。</p></li></ul></td></tr><tr><td><p>parts</p></td><td><p><a href="multimodal-integration-a2a-9862d72fb0298480.md#8ec627dd2eu4p">Part</a>[]</p></td><td><p>是</p></td><td><p>内容部分数组。至少包含一个。</p></td></tr><tr><td><p>messageId</p></td><td><p>String</p></td><td><p>是</p></td><td><p>由消息发送方生成的消息标识符。</p></td></tr><tr><td><p>contextId</p></td><td><p>String</p></td><td><p>否</p></td><td><p>与消息相关联的上下文标识符。</p></td></tr><tr><td><p>metadata</p></td><td><p>Map&lt;String, Object&gt;</p></td><td><p>否</p></td><td><p>与此消息关联的元数据。</p></td></tr></tbody></table>

<a id="part"></a>

<a id="8ec627dd2eu4p"></a>

#### Part

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| kind | String | 是 | 标识此部分的内容类型。text：文本类型。 |
| text | String | 否 | 该部分的文本内容，kind=text时填写。 |

<a id="示例-2"></a>

<a id="0400bf60a6htt"></a>

#### 示例

<a id="95f6ba7d90wfr"></a>

##### HTTP请求

<a id="code-block-2"></a>

```json
{
  "jsonrpc": "2.0",
  "id": "request-1",
  "method": "message/send",
  "params": {
    "message": {
      "messageId": "msg-1",
      "kind": "message",
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "今天会下雨吗？"
        }
      ]
    }
  }
}
```

<a id="8f96336393poa"></a>

##### HTTP SSE请求

<a id="code-block-3"></a>

```json
{
  "jsonrpc": "2.0",
  "id": "request-1",
  "method": "message/stream",
  "params": {
    "message": {
      "messageId": "msg-1",
      "kind": "message",
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "今天会下雨吗？"
        }
      ]
    }
  }
}
```

<a id="agent调用返回字段"></a>

<a id="6e74c0e6d8uwa"></a>

### Agent调用返回字段

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| jsonrpc | String | 是 | 固定为："2.0"。 |
| id | String | 是 | 请求ID，与`JSONRPCRequest.id`值相同。 |
| result | [Task](multimodal-integration-a2a-9862d72fb0298480.md#3f23b86c115fe) \| [TaskStatusUpdateEvent](multimodal-integration-a2a-9862d72fb0298480.md#ee061dacccy6j) \| [TaskArtifactUpdateEvent](multimodal-integration-a2a-9862d72fb0298480.md#108a408128acg) | 否 | 请求处理成功时返回。 |
| error | [JSONRpcError](multimodal-integration-a2a-9862d72fb0298480.md#bea1cc7762ej1) | 否 | 请求处理失败时返回。 |

<a id="task"></a>

<a id="3f23b86c115fe"></a>

#### Task

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| id | String | 是 | 服务器生成的唯一任务标识符（例如 UUID）。 |
| contextId | String | 是 | 跨多轮交互的上下文对齐的服务器生成 ID。 |
| status | TaskStatus | 是 | 任务的当前状态。 |
| artifacts | Artifact\[\] | 否 | 此任务中Agent生成的输出结果。 |

<a id="taskstatus"></a>

<a id="a17dccfe81ar4"></a>

#### TaskStatus

<table><thead><tr><th><p><strong>字段名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必填</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>state</p></td><td><p>String</p></td><td><p>是</p></td><td><p>任务的当前生命周期状态：</p><ul><li><p>submitted：任务已由Agent接收并确认，但处理尚未开始。</p></li><li><p>working：该任务正在由Agent处理中。客户端可能期待进一步的更新或最终状态。</p></li><li><p>completed：任务已成功完成。</p></li><li><p>failed：由于处理过程中发生错误。</p></li><li><p>input-required：Agent需要从用户获取额外输入才能继续。此时多模态交互服务会把用户的下一轮输入也给到该Agent。</p></li><li><p>rejected：任务已终止。此时会由多模态交互服务接管本轮请求的处理。</p></li></ul></td></tr><tr><td><p>timestamp</p></td><td><p>String</p></td><td><p>否</p></td><td><p>记录此状态的时间戳（推荐使用 UTC 时间）。</p></td></tr></tbody></table>

<a id="artifact"></a>

<a id="40569462abr4e"></a>

#### Artifact

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| artifactId | String | 是 | Agent生成的结果的标识符。 |
| parts | Part\[\] | 是 | 结果的内容，至少有一个。 |
| metadata | Map<String, Object> | 否 | 与此消息关联的元数据。 |

<a id="taskstatusupdateevent"></a>

<a id="ee061dacccy6j"></a>

#### TaskStatusUpdateEvent

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| taskId | String | 是 | 正在更新的任务 ID。 |
| contextId | String | 是 | 关联任务的上下文 ID。 |
| kind | String | 是 | 固定为：status-update。 |
| status | TaskStatus | 是 | 新的 TaskStatus 状态。 |
| final | Boolean | 否 | 如果 true ，表示这是当前流循环的最终状态更新。服务器通常在之后关闭 SSE 连接。 |

<a id="taskartifactupdateevent"></a>

<a id="108a408128acg"></a>

#### TaskArtifactUpdateEvent

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| taskId | String | 是 | 与生成的结果部分相关联的任务 ID。 |
| contextId | String | 是 | 关联任务的上下文 ID。 |
| kind | String | 是 | 固定为：artifact-update。 |
| artifact | Artifact | 是 | 结果数据。可以是完整的结果，也可以是增量结果。 |
| append | Boolean | 否 | true 表示将该部分追加到已返回结果中；false （默认）表示替换掉已返回结果。 |
| lastChunk | Boolean | 否 | true 表示这是该结果的最终更新。 |

<a id="jsonrpcerror"></a>

<a id="bea1cc7762ej1"></a>

#### JSONRpcError

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| code | Integer | 是 | 错误代码。 |
| message | String | 是 | 错误描述信息。 |

<a id="示例-3"></a>

<a id="3bc2287c07kpk"></a>

#### 示例

<a id="198562b0f8g32"></a>

##### HTTP返回

<a id="code-block-4"></a>

```json
{
  "id": "request-1",
  "jsonrpc": "2.0",
  "result": {
    "id": "task-1",
    "contextId": "context-1",
    "kind": "task",
    "status": {
      "state": "completed",
      "timestamp": "2025-07-15T14:50:28.575338Z"
    },
    "artifacts": [
      {
        "artifactId": "c3fee4d5-7234-48a1-8d2c-cfb715c5ce9e",
        "parts": [
          {
            "kind": "text",
            "text": "今天天气晴，"
          }
        ]
      },
      {
        "artifactId": "c3fee4d5-7234-48a1-8d2c-cfb715c5ce9e",
        "parts": [
          {
            "kind": "text",
            "text": "没有雨。"
          }
        ]
      }
    ]
  }
}
```

<a id="17eb84bbe3ln4"></a>

##### HTTP SSE返回

<a id="code-block-5"></a>

```json
{
  "id": "request-1",
  "jsonrpc": "2.0",
  "result": {
    "id": "task-1",
    "contextId": "context-1",
    "kind": "task",
    "status": {
      "state": "submitted",
      "timestamp": "2025-07-15T14:52:28.277547Z"
    }
  }
}

{
  "id": "request-1",
  "jsonrpc": "2.0",
  "result": {
    "taskId": "task-1",
    "contextId": "context-1",
    "kind": "artifact-update",
    "artifact": {
      "artifactId": "82eb84b9-0d73-4072-95f8-03655adfbf25",
      "parts": [
        {
          "kind": "text",
          "text": "今天天气晴，"
        }
      ]
    },
    "append": true,
    "lastChunk": false
  }
}

{
  "id": "request-1",
  "jsonrpc": "2.0",
  "result": {
    "taskId": "task-1",
    "contextId": "context-1",
    "kind": "artifact-update",
    "artifact": {
      "artifactId": "82eb84b9-0d73-4072-95f8-03655adfbf25",
      "parts": [
        {
          "kind": "text",
          "text": "没有雨。"
        }
      ]
    },
    "append": true,
    "lastChunk": true
  }
}

{
  "id": "request-1",
  "jsonrpc": "2.0",
  "result": {
    "taskId": "task-1",
    "contextId": "context-1",
    "kind": "status-update",
    "status": {
      "state": "completed",
      "timestamp": "2025-07-15T14:52:28.277643Z"
    },
    "final": true
  }
}
```

<a id="接入示例"></a>

<a id="12c0891049d3t"></a>

## 接入示例

在管控台填入`https://example/.well-known/agent.json`可体验接入自研Agent的流程：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7028182571/p986762.png)

<a id="进一步集成"></a>

<a id="fa8c3acdb81si"></a>

## 进一步集成

至此，您已经完成了自研Agent与多模态交互套件的基础集成，如需进一步集成，请参见：

-   [Protocol扩展](multimodal-integration-a2a-protocol-cc7032270d8398c9.md)
-   [Intent扩展](multimodal-integration-a2a-intent-c31b4ac77d266ee3.md)
