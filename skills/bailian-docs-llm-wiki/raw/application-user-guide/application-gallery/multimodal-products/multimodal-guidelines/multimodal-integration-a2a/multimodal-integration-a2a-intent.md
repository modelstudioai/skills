# Intent扩展

已完成自研Agent与多模态交互开发套件的基础集成后，如果想进一步由多模态交互开发套件根据用户意图对自研Agent的技能进行匹配，可以参考此文档来完成协议扩展。

## 扩展协议声明

将本文档URI添加到[AgentCard](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a#854b8c0b10ozm)的`capabilities.extensions`字段，声明支持其中定义的扩展协议。

本文档URI为：`https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent`。

**示例：**
```
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

## 字段说明

### AgentCard返回字段

#### AgentExtension

**字段名称**

**类型**

**是否必填**

**说明**

uri

String

是

固定为："[](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent)[https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent)"。

params

Map<String, [SkillExtension](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent#e967c0503e4ql)\[\]>

否

特定于扩展的配置参数。使用此字段扩展希望识别的技能参数，Map的key固定为"skills"，value为 [SkillExtension](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent#e967c0503e4ql)\[\]。

#### SkillExtension

**字段名称**

**类型**

**是否必填**

**说明**

id

String

是

Agent内的唯一技能标识符，同[AgentSkill](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a#9567dc941c71f).id。

inputSchema

Object

是

在开启了该扩展，且需要由多模态应用识别技能参数时设置，结构同MCP Tools协议定义。

#### 示例

```
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

### Agent调用请求字段

#### Message

**字段名称**

**类型**

**是否必填**

**说明**

metadata

Map<String, [IntentInfo](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent#389d41fe17slp)\[\]>

是

与此消息关联的元数据，会由多模态应用自动注入。

-   intentInfos：意图信息
    

#### IntentInfo

技能的意图路由信息。

**字段名称**

**类型**

**是否必填**

**说明**

intent

String

是

意图路由到的技能ID。

slots

[Slot](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-intent#c0478044cbqaa)\[\]

否

技能参数信息。

#### Slot

**字段名称**

**类型**

**是否必填**

**说明**

name

String

是

技能参数名称。

value

String

是

技能参数值。

normValue

String

否

技能参数归一化后的值。

#### 示例

```
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
