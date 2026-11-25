# Intent扩展

已完成自研Agent与多模态交互开发套件的基础集成后，如果想进一步由多模态交互开发套件根据用户意图对自研Agent的技能进行匹配，可以参考此文档来完成协议扩展。

<a id="扩展协议声明"></a>

<a id="d9d1908dbczfz"></a>

## 扩展协议声明

将本文档URI添加到[AgentCard](multimodal-integration-a2a-9862d72fb0298480.md#854b8c0b10ozm)的`capabilities.extensions`字段，声明支持其中定义的扩展协议。

本文档URI为：`https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent`。

**示例：**

<a id="code-block"></a>

```json
{
  ...
  "capabilities": {
    "extensions": [
      {
        "uri": "https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent",
        "params": {
          "skills": [
            {
              "id": "ai-calculate",
              "inputSchema": {
                "type": "object",
                "properties": {
                  "num1": {
                    "type": "int",
                    "description": "The first number"
                  },
                  "num2": {
                    "type": "int",
                    "description": "The second number"
                  }
                }
              }
            }
          ]
        }
      },
      ...
    ],
    ...
  },
  ...
}
```

<a id="字段说明"></a>

<a id="2eef68a8e2pj7"></a>

## 字段说明

<a id="agentcard返回字段"></a>

<a id="b4c448689esav"></a>

### AgentCard返回字段

<a id="agentextension"></a>

<a id="1fb43a8c55vbr"></a>

#### AgentExtension

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| uri | String | 是 | 固定为："[](multimodal-integration-a2a-intent-c31b4ac77d266ee3.md)[https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent](multimodal-integration-a2a-intent-c31b4ac77d266ee3.md)"。 |
| params | Map<String, [SkillExtension](multimodal-integration-a2a-intent-c31b4ac77d266ee3.md#e967c0503e4ql)\[\]> | 否 | 特定于扩展的配置参数。使用此字段扩展希望识别的技能参数，Map的key固定为"skills"，value为 [SkillExtension](multimodal-integration-a2a-intent-c31b4ac77d266ee3.md#e967c0503e4ql)\[\]。 |

<a id="skillextension"></a>

<a id="e967c0503e4ql"></a>

#### SkillExtension

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| id | String | 是 | Agent内的唯一技能标识符，同[AgentSkill](multimodal-integration-a2a-9862d72fb0298480.md#9567dc941c71f).id。 |
| inputSchema | Object | 是 | 在开启了该扩展，且需要由多模态应用识别技能参数时设置，结构同MCP Tools协议定义。 |

<a id="示例"></a>

<a id="abd4d3df34ksc"></a>

#### 示例

<a id="code-block-2"></a>

```json
{
  ...
  "capabilities": {
    "extensions": [
      {
        "uri": "https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent",
        "params": {
          "skills": [
            {
              "id": "ai-calculate",
              "inputSchema": {
                "type": "object",
                "properties": {
                  "num1": {
                    "type": "int",
                    "description": "The first number"
                  },
                  "num2": {
                    "type": "int",
                    "description": "The second number"
                  }
                }
              }
            }
          ]
        }
      },
      ...
    ],
    ...
  },
  ...
}
```

<a id="agent调用请求字段"></a>

<a id="9878de0c55013"></a>

### Agent调用请求字段

<a id="message"></a>

<a id="1f61b50405m3h"></a>

#### Message

<table><thead><tr><th><p><strong>字段名称</strong></p></th><th><p><strong>类型</strong></p></th><th><p><strong>是否必填</strong></p></th><th><p><strong>说明</strong></p></th></tr></thead><tbody><tr><td><p>metadata</p></td><td><p>Map&lt;String, <a href="multimodal-integration-a2a-intent-c31b4ac77d266ee3.md#389d41fe17slp">IntentInfo</a>[]&gt;</p></td><td><p>是</p></td><td><p>与此消息关联的元数据，会由多模态应用自动注入。</p><ul><li><p>intentInfos：意图信息</p></li></ul></td></tr></tbody></table>

<a id="intentinfo"></a>

<a id="389d41fe17slp"></a>

#### IntentInfo

技能的意图路由信息。

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| intent | String | 是 | 意图路由到的技能ID。 |
| slots | [Slot](multimodal-integration-a2a-intent-c31b4ac77d266ee3.md#c0478044cbqaa)\[\] | 否 | 技能参数信息。 |

<a id="slot"></a>

<a id="c0478044cbqaa"></a>

#### Slot

| 字段名称 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| name | String | 是 | 技能参数名称。 |
| value | String | 是 | 技能参数值。 |
| normValue | String | 否 | 技能参数归一化后的值。 |

<a id="示例-2"></a>

<a id="77be9dfec91j8"></a>

#### 示例

<a id="code-block-3"></a>

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
          "text": "101加102等于几？"
        }
      ],
      "metadata": {
        "intentInfos": [
          {
            "intent": "ai-calculate",
            "slots": [
              {
                "name": "num1",
                "value": "101",
                "normValue": "101"
              },
              {
                "name": "num2",
                "value": "102",
                "normValue": "102"
              }
            ]
          }
        ]
      }
    }
  }
}
```
