# 自定义指令实践

本文档系统阐述多模态指令配置标准及设备交互规范，核心内容包括：指令设计、时间格式、交互流程、开发支持。该规范旨在确保意图模型与设备控制的无缝衔接，实现标准化、高可靠性的交互过程。

## **指令简介**

指令由多模态交互云端下发给终端，用于将用户的交互意图转化为具体的业务动作。开发者可以通过指令扩展功能，实现对设备硬件控制（如开关、调节、动作）、媒体播放（如进度、音效）及应用程序（如跳转）的灵活控制，具有良好的扩展性，我们提供了一系列常见预置指令，也支持开发者根据业务需求自定义。

管控台的配置方式可以参考[应用配置](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration#20261288470en)。

## **指令配置技巧**

为了确保意图模型能够准确地理解并调用正确的工具，我们需要遵循一套严谨的工具定义规范。以下是一些关键点和示例来帮助您更好地定义工具。

### **工具描述要清晰准确**

-   **目标**：让意图模型明白这个工具是用来做什么的。
    
-   **注意事项**：避免使用模糊不清的语言，确保描述与实际功能一致。
    

**示例**：

-   **好**：`"查询指定日期的天气情况"`
    
-   **不好**：`"查看天气"`（过于宽泛，可能被误用于其他天气相关操作）
    

### **参数定义需无歧义**

-   **目标**：每个参数的作用和取值范围都应明确。
    
-   **建议做法**：尽可能使用枚举值限制参数选项（目前暂未开放枚举值定义，请在描述中定义）；对于开放性输入，则提供详细的描述。
    

**示例** - 定义一个播放音乐的工具：

```
{
  "type": "object",
  "required": ["action", "media"],
  "properties": {
    "action": {
      "type": "string",
      "description": "播放控制动作",
      "enum": ["play", "pause", "stop"]
    },
    "media": {
      "type": "string",
      "description": "媒体文件名或URL"
    }
  }
}
```

### **精简而全面**

-   **目标**：保持工具定义简洁但信息完整。
    
-   **注意事项**：不要过度列举例子，仅保留必要的说明部分。
    

**示例** - 查询的工具定义：

```
{
  "name": "query_city_news",
  "description": "查询指定城市的新闻",
  "parameters": {
    "type": "object",
    "required": ["city"],
    "properties": {
      "city": {
        "type": "string",
        "description": "要查询的城市名称"
      },
      "date": {
        "type": "string",
        "description": "查询的日期，格式为 yyyy-mm-dd，如果为空则查询当前日期"
      }
    }
  }
}
```

### **合理合并相似参数**

在设计工具调用接口时，合理合并相似参数意味着将具有类似功能或可以共同处理的多个参数整合为一个。这样做不仅能够简化接口定义，减少冗余，还能使工具调用更加直观易懂。下面通过几个例子来具体说明如何进行合理的参数合并：

#### **例子1: 控制播放器**

假设我们有两个独立的工具函数用于控制媒体播放器的状态：一个是play\_media用来开始播放媒体内容，另一个是pause\_media用来暂停当前播放的内容。这两个工具其实都是关于控制播放状态的操作，因此可以考虑将其合并为一个工具control\_playback，并通过引入一个额外的参数action来区分具体的命令。

##### **原始定义**

-   play\_media
    
    -   参数: 无
        
-   pause\_media
    
    -   参数: 无
        

##### **合并后的定义**

-   control\_playback
    
    -   参数:
        
        -   action: {"type": "string", "description": "指定要执行的动作（例如 'play' 或 'pause'）", "enum": \["play", "pause"\]}
            

这样做的好处是减少了需要维护的工具数量，并且使得对于播放状态的控制变得更加灵活和一致。

#### **例子2: 设置提醒**

如果我们有一个设置闹钟的应用场景，其中包含两个不同的工具：set\_alarm用于设定一次性闹钟，而set\_repeating\_alarm则用于创建重复性闹钟。这两个工具实际上都是关于配置闹钟的行为，只是它们的触发条件不同。因此，可以通过增加一个表示重复模式的新参数来合并这两个工具。

##### **原始定义**

-   set\_alarm
    
    -   参数:
        
        -   time: 人类可读时间
            
-   set\_repeating\_alarm
    
    -   参数:
        
        -   repeat\_pattern: 人类可读循环日期
            
        -   time: 人类可读时间
            

##### **合并后的定义**

-   set\_alarm
    
    -   参数：
        
        -   time: 人类可读时间
            
        -   repeat\_pattern: {"type": \["string", "null"\], "description": "如果设置了，则表示这是一个重复性闹钟；否则为单次闹钟。支持人类可读循环日期格式。默认值为 null 表示非重复"}
            

在这个案例中，通过添加一个可选参数repeat\_pattern，我们可以同时支持一次性与重复性闹钟的设置，从而避免了创建两个非常类似的工具。

#### **总结**

合理地合并相似参数关键在于识别出哪些参数本质上是在做相同或高度相关的事情，并尝试找到一种方式将这些行为统一起来。这不仅有助于简化系统设计，还可以提高代码的可维护性和用户体验。但需要注意的是，在合并参数的过程中也要确保不会过度复杂化单一工具的功能，以免造成混淆或使用上的困难。

### **人类可读时间规范**

```
{
        "humanReadableDate": {
            "title": "人类可读日期",
            "type": "string",
            "x-type": "humanReadableTime",
            "description": "可以是绝对日期，相对日期，标准日期，系统会自动解析成 yyyy-mm-dd 格式",
            "examples": [
                "明天",
                "下周二",
                "三天后"
            ]
        },
        "humanReadableTime": {
            "title": "人类可读时间",
            "type": "string",
            "x-type": "humanReadableTime",
            "description": "可以是自然语言描述的绝对时刻，相对时刻，系统会自动解析成 HH:MM:SS 格式",
            "examples": [
                "三小时后",
                "今天下午5点",
                "12点15"
            ]
        }
    }
```

参数名 以"date\_"开头，系统会把参数理解为humanReadableDate

参数名 以"time\_"开头，系统会把参数理解为humanReadableTime

## 自定义工具JSON文件格式

运行用户直接上传全部工具的定义，文件约定为json格式，其json schema如下。

### **1\. 定义结构说明**

```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LLM Tool Definition with Examples",
  "type": "object",
  "required": ["tool_definition", "usage_examples"],
  "properties": {
    "tool_definition": {
      "type": "object",
      "description": "符合大模型标准的工具功能定义",
      "required": ["name", "description", "parameters"],
      "properties": {
        "name": {
          "type": "string",
          "description": "工具的唯一识别名称，建议使用下划线命名法"
        },
        "description": {
          "type": "string",
          "description": "详细描述工具的功能，以便模型判断何时调用"
        },
        "parameters": {
          "type": "object",
          "description": "参数定义的 JSON Schema 子集"
        }
      }
    },
    "response_type": {
      "type": "string",
      "description": "工具调用后的响应类型",
      "enum": ["ON_EXECUTION_RESULT", "IMMEDIATE"],
      "default": "ON_EXECUTION_RESULT"
    },
    "usage_examples": {
      "type": "array",
      "description": "提供给模型参考的少样本（Few-shot）示例数组",
      "items": {
        "type": "object",
        "required": ["text", "tool_call"],
        "properties": {
          "text": {
            "type": "string",
            "description": "用户的自然语言查询文本"
          },
          "tool_call": {
            "type": "object",
            "description": "对应上述文本应当生成的参数结果",
            "required": ["arguments"],
            "properties": {
              "arguments": {
                "type": "object",
                "description": "具体的参数键值对"
              }
            }
          }
        }
      }
    }
  }
}
```

```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LLM Tool Set Definition",
  "type": "object",
  "required": ["set_name", "tools"],
  "properties": {
    "set_name": {
      "type": "string",
      "description": "工具集的逻辑名称，例如 'office_automation' 或 'social_media_tools'"
    },
    "description": {
      "type": "string",
      "description": "对该工具集用途的整体描述"
    },
    "tools": {
      "type": "array",
      "description": "该集合下包含的所有工具列表",
      "items": {$单个工具的JSON schema}
    }
  }
}
```

```
{
  "tool_set_name": "content_manager",
  "tools": [
    {
      "tool_definition": {
        "name": "create_note",
        "description": "创建一个新的文本笔记",
        "parameters": {
          "type": "object",
          "properties": {
            "title": { "type": "string", "description": "笔记标题" },
            "content": { "type": "string", "description": "笔记详细内容" }
          },
          "required": ["title", "content"]
        }
      },
      "usage_examples": [
        {
          "text": "帮我记一下，明天下午三点有个周会",
          "tool_call": {
            "arguments": {
              "title": "日程提醒",
              "content": "明天下午三点有个周会"
            }
          }
        }
      ],
      "response_type": "ON_EXECUTION_RESULT"
    },
    {
      "tool_definition": {
        "name": "add_to_list",
        "description": "向指定的清单中添加项目",
        "parameters": {
          "type": "object",
          "properties": {
            "list_name": { "type": "string", "description": "清单名称，如：购物清单" },
            "item": { "type": "string", "description": "要添加的项目名称" }
          },
          "required": ["list_name", "item"]
        }
      },
      "usage_examples": [
        {
          "text": "在我的购物清单里加上苹果",
          "tool_call": {
            "arguments": {
              "list_name": "购物清单",
              "item": "苹果"
            }
          }
        }
      ],
      "response_type": "ON_EXECUTION_RESULT"
    }
  ]
}
```

一个完整的工具定义包含以下三个核心部分：

**字段名**

**类型**

**必填**

**说明**

`name`

`string`

是

工具的唯一标识符。只能包含字母、数字、下划线，建议使用 `snake_case`。

`description`

`string`

是

**至关重要**。描述工具的功能、适用场景。模型根据此描述决定是否调用该工具。

`parameters`

`object`

是

定义工具接收的参数。必须是一个符合 JSON Schema 的对象。

### `**parameters**` **内部结构**

-   `**type**`: 固定为 `"object"`。
    
-   `**properties**`: 定义具体的键值对，每个键代表一个参数。
    
-   `**required**`: 一个字符串数组，列出所有必填参数的名称。
    

工具列表的元定义

```
{
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string", "pattern": "^[a-zA-Z0-9_-]+$" },
          "description": { "type": "string", "minLength": 1 },
          "parameters": { "type": "object" }
        },
        "required": ["name", "description"],
        "additionalProperties": false
      }
}
```

## 下发指令时给出模型回复

### **管控台配置**

如果需要下发指令的同时给出模型回复，可以在设置页中选择回复模式：

-   根据执行情况回复（默认）：下发指令后，等待端侧返回成功/失败信息，模型生成对应回复，如“已将空调调整到26度”、“已经是最高音量，无法继续调高”。
    
-   自动回复：下发指令的同时，自动输出回复。
    

![截屏2025-11-25 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4861376671/p1038882.png)

### **端侧接受指令**

如 3.1 配置取消静音技能需要回复。

通过语音指令“取消静音”的下发结果为：

```
{
    "payload": {
        "output": {
            "event": "RespondingContent",
            "text": "",
            "spoken": "",
            "finished": true,
            "finish_reason": "stop",
            "extra_info": {
                "tool_infos": [

                ],
                "agent_info": {
                    "intent_infos": [
                        {
                            "domain": "general_command",
                            "intent": "unmute"
                        }
                    ],
                    "round": 1
                },
                "commands": "[{\"intent_info\":{\"domain\":\"general_command\",\"intent\":\"unmute\"},\"command_request_id\":\"35b635f3-6511-450e-8fa1-6955d5279367\",\"name\":\"unmute\",\"params\":[]}]",
                "query": "取消静音"
            },
            "dialog_id": "56fe9300-d80c-471a-80bd-20c0296acd93",
            "round_id": "70f636e1d0284bc8a8bac2767e61b4b5",
            "llm_request_id": "1d8f3469274e4d13bbc3b28460eabb76"
        }
    }
}
```

结果中 payload.output.extra\_info.commands 为指令执行结果。

当用户选择根据执行情况回复时， 返回结果中包含command\_request\_id。在回复结果时，这个 ID 作为回复的 key 使用。

### **端侧回复指令**

您在收到指令或者 Agent的结果后，通过端侧执行，获得一个成功或者失败的结果，同步给服务端，通过如下接口提交：

参数

一级参数

二级参数

三级参数

四级参数

参数说明

**技能响应/三方 Agent 回调执行结果**

biz\_params

command\_results\[\]

command\_request\_id

string

请求 id

invoke\_result

执行结果

content

Object

根据不同结果区分，详见端侧统一返回规范

structuredContent

JSON object

结构化返回信息

**structuredContent.success**

**Boolean**

**是否开启成功**

invoke\_result.content 是端侧传递给Agent 的数据部分。我们推荐使用如下端侧统一返回规范格式：

参数名

类型

含义

content

Object

根据不同结果区分，详见下面的 text content/image content/audio content

##### **Text Content**

```
{
  "type": "text",
  "text": "Tool result text"
}
```

##### **Image Content**

```
{
  "type": "image",
  "data": "base64-encoded-data",
  "mimeType": "image/png"
  "annotations": {
    "audience": ["user"],
    "priority": 0.9
  }
}
```

##### **Audio Content**

```
{
  "type": "audio",
  "data": "base64-encoded-audio-data",
  "mimeType": "audio/wav"
}
```

##### **结果示例：**

```
[
    {
        "command_request_id": "xxxx",
        "invoke_result": {
            "content": {
                "type": "text",
                "text": "成功打开"
            },
            "structuredContent": {
                "success": true
            }
        }
    }
]
```

### **请求代码示例- 端侧回调执行结果（以 java 为例）**

```
public static HashMap<String,Object> getAgentorCommandResult() {

  HashMap<String,Object> commandResult = new HashMap<>();
  commandResult.put("command_request_id", "35b635f3-6511-450e-8fa1-6955d5279367");
  commandResult.put("invoke_result", new Object<>());
    // invoke_result.structuredContent.success = true/false 执行结果

  ArrayList<Object> commandResults = new ArrayList<>();
  commandResults.add(commandResult);

  HashMap<String,Object> passThroughParams = new HashMap<>();
  passThroughParams.put("command_results", commandResults);
  return passThroughParams;
}
 
//发起打开 agent 请求
MultiModalRequestParam.UpdateParams updateParams = MultiModalRequestParam.UpdateParams.builder()
    .bizParams(MultiModalRequestParam.BizParams.builder()
        .passThroughParams(getAgentorCommandResult())
        .build())
    .build();
conversation.requestToRespond("prompt", "", updateParams);
```
