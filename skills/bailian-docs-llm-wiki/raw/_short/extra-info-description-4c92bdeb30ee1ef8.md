# 多模态对话结果 extra_info 说明

<a id="通过-sdk-或者-api-获取llm-的结果"></a>

<a id="31f723c481ecu"></a>

## 通过 SDK 或者 API 获取LLM 的结果

<a id="respondingcontent"></a>

<a id="e4e53900dffzz"></a>

### RespondingContent

服务端通过 type 为 RespondingContent 类型结果下发 LLM 对话、Agent、插件的结果。

<table><thead><tr><th><p>一级参数</p></th><th><p>二级参数</p></th><th><p>类型</p></th><th><p>是否必选</p></th><th><p>说明</p></th></tr></thead><tbody><tr><td><p>output</p></td><td><p>event</p></td><td><p>string</p></td><td><p>是</p></td><td><p>事件名称：RespondingContent</p></td></tr><tr><td></td><td><p>dialog_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>对话ID</p></td></tr><tr><td></td><td><p>round_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>本轮交互的ID</p></td></tr><tr><td></td><td><p>llm_request_id</p></td><td><p>string</p></td><td><p>是</p></td><td><p>调用llm的request_id</p></td></tr><tr><td></td><td><p>text</p></td><td><p>string</p></td><td><p>是</p></td><td><p>系统对外输出的文本，流式全量输出</p></td></tr><tr><td></td><td><p>spoken</p></td><td><p>string</p></td><td><p>是</p></td><td><p>合成语音时使用的文本，流式全量输出</p></td></tr><tr><td></td><td><p>finished</p></td><td><p>bool</p></td><td><p>是</p></td><td><p>输出是否结束</p></td></tr><tr><td></td><td><p>extra_info</p></td><td><p>object</p></td><td><p>否</p></td><td><p>其他扩展信息，目前支持：</p><ul><li><p>commands: 命令字符串，此字段为JSON字符串，需要进行二次解析。各类agent使用的命令字符串可以参考<a href="official-agent-297b22931e69e622.md">调用官方Agent</a>的说明。</p></li><li><p>agent_info: 智能体信息</p></li><li><p>tool_calls: 插件返回的信息</p></li></ul><p>如果没有扩展信息要提交则省略此字段。</p></td></tr></tbody></table>

<a id="1-1-extra-info-commands"></a>

<a id="6566feb14228x"></a>

### 1.1 extra\_info.commands

**多模态应用**下发的指令。

<a id="code-block"></a>

```json
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

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | 参数 |  | 类型 | 其他 | 说明 |
| command | name |  | String |  | 指令名称 |
|  | params\[\] |  | Array | 如果有，下发 | 技能或者 Agent 下发的参数 |
|  |  | name | String |  | 参数名 |
|  |  | value | String |  | 值 |
|  | command\_request\_id |  | String | 非必传 | Agent或技能生成的唯一ID，在回传执行结果时需要使用。参考下方。 |
|  | **intent\_infos\[\]** |  | Array | 非必传 |  |
|  |  | domain | String |  | 语义理解的 domain |
|  |  | intent | String |  | 语音理解的 intent |

<a id="1-2-extra-info-agent-info"></a>

<a id="a28d8e6f7b7mz"></a>

### 1.2 extra\_info.agent\_info

<a id="code-block-2"></a>

```json
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

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | 参数 |  | 类型 | 其他 | 说明 |
| agent\_info | device |  |  |  |  |
|  |  | device\_id | String |  | 设备 id |
|  | round |  | int |  | 进入 Agent 之后的对话轮次 |
|  | **intent\_infos\[\]** |  | Array |  |  |
|  |  | domain | String |  | Agent的 domain，在百链 Agent 中代表 Agent 的 id |
|  |  | intent | String |  | 业务定义的 intent，协议透传 |

<a id="1-3-extra-info-tool-calls"></a>

<a id="9e17d42a0e5tt"></a>

### 1.3 extra\_info.tool\_calls

**插件和语音应用**的技能调用结果从这个接口返回。

<a id="code-block-3"></a>

```json
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

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
|  | 参数 |  | 类型 | 其他 | 说明 |
| tool\_calls\[\] | type |  | String |  | 字段名一般固定为“FUNCTION”。代表 function call |
|  | function |  |  |  |  |
|  |  | name | String |  | 字段为自定义的工具函数名称，与多模态应用的 domain 类似 |
|  |  | arguments | list |  | 插件或者技能下发的参数列表 |

<a id="技能执行结果的响应"></a>

<a id="9ebde9f3a0ytx"></a>

## 技能执行结果的响应

<a id="配置技能响应"></a>

<a id="6138755dcbfgk"></a>

### 配置技能响应

在管控台选择技能根据执行情况回复。

回复方式包含两个选项：**根据执行情况回复**（根据设备返回的执行结果生成回复，如果设备不返回结果则仅下发指令）和**自动回复**（下发指令的同时自动生成回复）。

通过语音指令“取消静音”的下发结果为：

<a id="code-block-4"></a>

```json
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

<a id="端侧回复参数"></a>

<a id="1e50baeecbzbl"></a>

### 端侧回复参数

您在收到指令或者 Agent的结果后，通过端侧执行，获得一个成功或者失败的结果，同步给服务端，通过如下接口提交：

<table><tbody><tr><td><p>参数</p></td><td><p>一级参数</p></td><td><p>二级参数</p></td><td><p>三级参数</p></td><td><p>四级参数</p></td><td><p>参数说明</p></td></tr><tr><td colspan="5"><p><strong>技能响应/三方 Agent 回调执行结果</strong></p></td><td></td></tr><tr><td rowspan="5"><p>biz_params</p></td><td rowspan="5"><p>command_results[]</p></td><td><p>command_request_id</p></td><td><p>string</p></td><td></td><td><p>请求 id</p></td></tr><tr><td rowspan="4"><p>invoke_result</p></td><td></td><td></td><td><p>执行结果</p></td></tr><tr><td><p>content</p></td><td><p>Object</p></td><td><p>根据不同结果区分，详见端侧统一返回规范</p></td></tr><tr><td><p>structuredContent</p></td><td><p>JSON object</p></td><td><p>结构化返回信息</p></td></tr><tr><td><p><strong>structuredContent.success</strong></p></td><td><p><strong>Boolean</strong></p></td><td><p><strong>是否开启成功</strong></p></td></tr></tbody></table>

结果示例：

<a id="code-block-5"></a>

```json
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

<a id="请求代码-端侧回调执行结果-以-java-为例"></a>

<a id="a7da7f05b25ee"></a>

### 请求代码- 端侧回调执行结果（以 java 为例）

<a id="code-block-6"></a>

```java
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
