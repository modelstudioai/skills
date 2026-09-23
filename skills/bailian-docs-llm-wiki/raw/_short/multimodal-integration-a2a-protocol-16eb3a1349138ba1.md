# Protocol扩展

已完成自研Agent与多模态交互开发套件的基础集成后，如果想进一步获取端侧的用户信息、设备信息、位置信息、自定义传参信息，或向端侧下发端指令信息等，可以参考此文档来完成协议扩展。

## 扩展协议声明

将本文档URI添加到[AgentCard](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a#854b8c0b10ozm)的`capabilities.extensions`字段，声明支持其中定义的扩展协议。

本文档URI为：`https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-protocol`。

**示例：**
```
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

## 字段说明

### Agent调用请求字段

#### Message

Message其他字段说明，请参见[Message](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a#ad7fc73eeelos)。

**字段名称**

**类型**

**是否必填**

**说明**

metadata

Map<String, Object>

是

与此消息关联的元数据。

-   user: 用户信息
    
-   device: 设备信息
    
-   location: 位置信息
    
-   userDefinedParams: 自定义参数
    
-   commandResults: 指令执行结果
    
-   images：图片信息
    
-   chatId：标识一轮对话ID
    

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

### Agent调用返回字段

#### Artifact

**字段名称**

**类型**

**是否必填**

**说明**

metadata

Map<String, [Command](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-protocol#06b2940f44vev)\[\]>

否

与此消息关联的元数据。可在返回的最后一个Artifact结构中添加扩展字段。

#### Command

下发给终端的指令。

**字段名称**

**类型**

**是否必填**

**说明**

name

String

是

指令名称。

params

[Param](https://help.aliyun.com/zh/model-studio/multimodal-integration-a2a-protocol#b98dc04c3erj1)\[\]

否

指令参数信息。

commandRequestId

String

否

指令请求ID。

#### Param

**字段**

**类型**

**是否必填**

**说明**

name

String

是

指令参数名称。

value

String

是

指令参数值。

normValue

String

否

指令参数归一化后的值。

#### 示例

```
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
