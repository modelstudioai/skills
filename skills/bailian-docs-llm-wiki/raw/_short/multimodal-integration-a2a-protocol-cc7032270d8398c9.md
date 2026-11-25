# Protocol扩展

已完成自研Agent与多模态交互开发套件的基础集成后，如果想进一步获取端侧的用户信息、设备信息、位置信息、自定义传参信息，或向端侧下发端指令信息等，可以参考此文档来完成协议扩展。

<a id="扩展协议声明"></a>

<a id="d9c96f985051p"></a>

## 扩展协议声明

将本文档URI添加到[AgentCard](multimodal-integration-a2a-9862d72fb0298480.md#854b8c0b10ozm)的`capabilities.extensions`字段，声明支持其中定义的扩展协议。

本文档URI为：`https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-protocol`。

**示例：**

<a id="code-block"></a>

```json
{
  ...
  "capabilities": {
    "extensions": [
      {
        "uri": "https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-protocol"
      },
      ...
    ],
    ...
  },
  ...
}
```

<a id="字段说明"></a>

<a id="c44376a5efw3b"></a>

## 字段说明

<a id="agent调用请求字段"></a>

<a id="9878de0c55013"></a>

### Agent调用请求字段

<a id="message"></a>

<a id="1f61b50405m3h"></a>

#### Message

Message其他字段说明，请参见[Message](multimodal-integration-a2a-9862d72fb0298480.md#ad7fc73eeelos)。

<table><thead><tr><th><p><strong>字段名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必填</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>metadata</p></td><td><p>Map&lt;String, Object&gt;</p></td><td><p>是</p></td><td><p>与此消息关联的元数据。</p><ul><li><p>user: 用户信息</p></li><li><p>device: 设备信息</p></li><li><p>location: 位置信息</p></li><li><p>userDefinedParams: 自定义参数</p></li><li><p>commandResults: 指令执行结果</p></li><li><p>images：图片信息</p></li><li><p>chatId：标识一轮对话ID</p></li></ul></td></tr></tbody></table>

<a id="示例"></a>

<a id="77be9dfec91j8"></a>

#### 示例

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
      ],
      "metadata": {
        "user": {
          "userId": "用户ID"
        },
        "device": {
          "clientIp": "设备IP",
          "deviceId": "设备ID"
        },
        "location": {
          "city": "城市",
          "longitude": "经度",
          "latitude": "纬度"
        },
        "userDefinedParams": {
          "param1": "value1"
        },
        "images": [
          {
            "type": "url",
            "value": "https://image_url****"
          }
        ],
        "chatId": "3eca6a13-fcfd-48b0-b1b7-34bfe735****"
      }
    }
  }
}
```

<a id="agent调用返回字段"></a>

<a id="6e74c0e6d8uwa"></a>

### Agent调用返回字段

<a id="artifact"></a>

<a id="40569462abr4e"></a>

#### Artifact

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| metadata | Map<String, [Command](multimodal-integration-a2a-protocol-cc7032270d8398c9.md#06b2940f44vev)\[\]> | 否 | 与此消息关联的元数据。可在返回的最后一个Artifact结构中添加扩展字段。 |

<a id="command"></a>

<a id="06b2940f44vev"></a>

#### Command

下发给终端的指令。

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| name | String | 是 | 指令名称。 |
| params | [Param](multimodal-integration-a2a-protocol-cc7032270d8398c9.md#b98dc04c3erj1)\[\] | 否 | 指令参数信息。 |
| commandRequestId | String | 否 | 指令请求ID。 |

<a id="param"></a>

<a id="b98dc04c3erj1"></a>

#### Param

| 字段 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| name | String | 是 | 指令参数名称。 |
| value | String | 是 | 指令参数值。 |
| normValue | String | 否 | 指令参数归一化后的值。 |

<a id="示例-2"></a>

<a id="5e39bbcd14tas"></a>

#### 示例

<a id="code-block-3"></a>

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
        ],
        "metadata": {
          "commands": [
              {
                  "name": "下发指令名称",
                  "params": [
                      {
                          "name": "参数名",
                          "value": "参数值",
                          "normValue": "参数归一化值"
                      }
                  ],
                  "commandRequestId": "指令请求ID"
              }
          ]
        }
      }
    ]
  }
}
```
