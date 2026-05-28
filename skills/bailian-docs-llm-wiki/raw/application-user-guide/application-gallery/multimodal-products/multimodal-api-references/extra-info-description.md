# 多模态对话结果 extra_info 说明

## **通过 SDK 或者 API 获取LLM 的结果**

### **RespondingContent**

服务端通过 type 为 RespondingContent 类型结果下发 LLM 对话、Agent、插件的结果。

一级参数

二级参数

类型

是否必选

说明

output

event

string

是

事件名称：RespondingContent

dialog\_id

string

是

对话ID

round\_id

string

是

本轮交互的ID

llm\_request\_id

string

是

调用llm的request\_id

text

string

是

系统对外输出的文本，流式全量输出

spoken

string

是

合成语音时使用的文本，流式全量输出

finished

bool

是

输出是否结束

extra\_info

object

否

其他扩展信息，目前支持：

-   commands: 命令字符串，此字段为JSON字符串，需要进行二次解析。各类agent使用的命令字符串可以参考[调用官方Agent](https://help.aliyun.com/zh/model-studio/official-agent)的说明。
    
-   agent\_info: 智能体信息
    
-   tool\_calls: 插件返回的信息
    

如果没有扩展信息要提交则省略此字段。

### **1.1 extra\_info.commands**

**多模态应用**下发的指令。

```
{
    "commands": [
        {
            "name": "VOLUME_SET",
            "params": [
                {
                    "name": "series",
                    "normValue": "70",
                    "value": "70"
                }
            ]
        }
    ]
}
```

参数

类型

其他

说明

command

name

String

指令名称

params\[\]

Array

如果有，下发

技能或者 Agent 下发的参数

name

String

参数名

value

String

值

command\_request\_id

String

非必传

Agent或技能生成的唯一ID，在回传执行结果时需要使用。参考下方。

**intent\_infos\[\]**

Array

非必传

domain

String

语义理解的 domain

intent

String

语音理解的 intent

### **1.2 extra\_info.agent\_info**

```
{
    "agent_info": {
        "intent_infos": [
            {
                "domain": "67f3ad7d6496475483db4a184c926e77",
                "intent": "open_agent_67f3ad7d6496475483db4a184c926e77"
            }
        ],
        "device": {
            "device_id": "uuid_12345"
        },
        "round": 1
    }
}
```

参数

类型

其他

说明

agent\_info

device

device\_id

String

设备 id

round

int

进入 Agent 之后的对话轮次

**intent\_infos\[\]**

Array

domain

String

Agent的 domain，在百链 Agent 中代表 Agent 的 id

intent

String

业务定义的 intent，协议透传

### **1.3 extra\_info.**tool\_calls

**插件和语音应用**的技能调用结果从这个接口返回。

```
{
    "tool_calls": [
        {
            "function": {
                "name": "INCREASE_DEFAULT_volume",
                "arguments": "{}"
            },
            "type": "FUNCTION"
        }
    ]
}
```

参数

类型

其他

说明

tool\_calls\[\]

type

String

字段名一般固定为“FUNCTION”。代表 function call

function

name

String

字段为自定义的工具函数名称，与多模态应用的 domain 类似

arguments

list

插件或者技能下发的参数列表

## **技能执行结果的响应**

### **配置技能响应**

在管控台选择技能根据执行情况回复。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9742967671/p1041234.png)

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

### **端侧回复参数**

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

结果示例：

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

### **请求代码- 端侧回调执行结果（以 java 为例）**

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
