# 生成对话

基于千问联网检索Agent提供的 agent\_id 与 agent\_version 信息，提供联网知识检索、场景化对话等能力。

## **请求语法**

```
POST /web-search-agent/chat/completions HTTP/1.1
```

## **请求参数**

-   注意：请求提供动态参数后，将会直接覆盖应用配置中的状态值。
    

**参数名**

**类型**

**是否必须**

**说明**

stream

bool

是

必须填 true，当前版本仅支持流式响应。若提供false或不提供，请求将失败

input

object

是

输入字段

input.request\_id

str

否

请求ID（业务自定义）

input.messages

array\[object\]

是

对话消息

input.messages.\[\].role

str

是

角色，枚举值为：user、assistant

input.messages.\[\].content

str

是

消息内容

parameters

object

是

配置参数字段

parameters.agent\_options

object

是

智能体专用参数

parameters.agent\_options.agent\_id

string

是

应用ID

parameters.agent\_options.agent\_version

string

是

应用版本

parameters.agent\_options.session\_knowledge

string

否

session 会话级别知识

parameters.agent\_options.system\_prompt

string

否

系统提示词

parameters.agent\_options.agent\_policy

string

否

执行策略

-   standard: 默认策略（推荐）
    
-   agentic: 强制边想边搜
    
-   turbo: 极速模式
    

parameters.agent\_options.forced\_search

bool

否

是否强制搜索

-   开启时， agent\_policy默认为 standard
    

parameters.agent\_options.enable\_citation

bool

否

是否透出引用信息

parameters.agent\_options.enable\_text\_image\_mixed

bool

否

是否图文并茂生成

parameters.agent\_options.enable\_lemma

bool

否

是否透出百科词条

parameters.agent\_options.related\_video

bool

否

是否透出相关视频

parameters.agent\_options.enable\_rec\_question

bool

否

是否透出相关问题

## **返回参数**

**参数名**

**类型**

**是否必须**

**说明**

request\_id

str

是

请求ID（dashscope 平台）

code

str

是

状态码（成功：200）

message

str

是

状态信息

output

object

是

输出字段

output.request\_id

str

否

请求ID（业务自定义）

output.choices

array\[object\]

是

模型输出信息

output.choices.\[\].finish\_reason

str

是

生成结束原因，仅尾包输出stop

output.choices.\[\].message

object

是

对话消息

output.choices.\[\].message.role

str

是

角色，枚举值为：user、assistant、tool

output.choices.\[\].message.content

str | array\[object\]

是

生成内容/工具返回内容

output.choices.\[\].message.reasoning\_content

str

否

思考内容

output.choices.\[\].message.tool\_calls

array\[object\]

否

工具调用信息

output.choices.\[\].message.tool\_calls\[0\].arguments

dcit\[str,object\]

否

工具调用参数

output.choices.\[\].message.tool\_calls\[0\].name

str

否

工具调用名称

output.choices.\[\].message.additional\_kwargs.extra\_json

Any

否

工具调用返回时，携带结构化输出信息

output.choices.\[\].message.extra

dict

否

步骤状态信息

output.choices.\[\].message.extra.group

str

否

执行阶段

output.choices.\[\].message.extra.step\_change

str

否

步骤变化事件

output.choices.\[\].message.extra.step

str

否

当前步骤

output.choices.\[\].message.response\_metadata

dict

否

请求模型调用详细信息

output.usage

object

否

用量统计

output.usage.input\_tokens

int

否

输入 tokens

output.usage.output\_tokens

int

否

输出 tokens

output.usage.total\_tokens

int

否

总 tokens

## **执行阶段枚举**

执行阶段（`group`）

描述

说明

planning

计划中

对应plan模型，即系统处于任务规划阶段，该阶段包含 start 和 end 事件

generating

生成中

对应生成模型，表示系统正处于结果生成阶段，此阶段包含 start 和 end 事件。

当前步骤（`step`）

描述和说明

planning

计划中

generating

生成中

tool\_calling

工具调用中

tool\_calling\_{工具名称}

工具调用中，附带工具名称

-   由于模型原因 step\_change 值可能为不存在，请尽可能使用持久化的标志step
    
-   空包情况下 step、step\_change、group 字段的值可能不存在
    
-   plan、generation 均由 xxx\_start 事件 和 xxx\_end 事件两个事件组成
    
-   tool\_call 由 tool\_call\_start、tool\_calling、tool\_return 三个事件组成
    
-   tool\_call\_start 表示工具调用开始、tool\_calling 表示获取到完整工具调用的参数并会抛出完整的工具调用参数、tool\_return 表示工具调用返回结果，同时会携带结构化的工具返回信息。
    

步骤变化事件 (`step_change`)

事件发生时 `step` 的值

事件名称

解释说明

plan\_start

`planning`

开始规划

`step` 状态变为 `planning`, 表示对应状态的开头（包含当前包）。

plan\_end

`planning`

结束规划

`step` 开始变成其他状态，事件发生时 `step` 仍为 `planning`，表示对应状态的结尾（包含当前包）。

generation\_start

`generating`

开始生成

与 `plan` 事件同理

generation\_end

`generating`

结束生成

与 `plan` 事件同理

tool\_call\_start

`tool_calling_{工具名称}`

开始工具调用

表示工具调用开始

tool\_calling

`tool_calling_{工具名称}`

工具调用中

会输出tool\_call的具体参数和工具名称，`tool_calling`状态变为`tool_calling_{工具名称}`。

tool\_return

`tool_calling_{工具名称}`

工具返回

会携带工具返回信息， `step` 开始变成其他状态，事件发生时 `step` 仍为 `tool_calling_{工具名称}`。

## **多模态图像理解问答**

联网搜索 Agent 多模态接口支持通过图片 + 文本的方式进行对话。用户可以上传图片 URL，并附加文本问题，Agent 将理解图片内容调用工具并给出回答。

### **请求参数**

**参数名**

**类型**

**是否必须**

**说明**

input

object

是

输入字段

input.messages

array

是

消息列表

input.messages\[\].role

string

是

角色，固定为 user

input.messages\[\].content

array

是

消息内容，支持图片和文本

input.messages\[\].content\[\].type

string

否

图片地址，支持两种格式：

1\. URL 格式（[推荐](https://help.aliyun.com/zh/model-studio/web-search-agent-api-chat-multimodal-file)）：[https://example.com/image.jpg](https://example.com/image.jpg)

2\. Base64 格式：data:<content\_type>;base64,<base64\_data>，其中 content\_type 为图片 MIME 类型（如 image/jpeg）

input.messages\[\].content\[\].image\_url

object

条件必须

当 type为 image\_url 时必须

## **示例**

### **请求示例**

-   文本请求示例
    

```
{
    "input": {
        "messages": [
            {
                "role": "user", 
                "content": "现在日期"
            }
        ]
    },
    "stream": true,
    "parameters": {
        "agent_options": {
            "agent_id": "aid-xxx",
            "agent_version": "beta"
        }
    }
}
```

-   多模态请求示例
    

```
{
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "image_url": {
                            "url": "http://other-general-huabei2.oss-cn-beijing.aliyuncs.com/upload/36e553b350e98ba81f6b33b08833a784.png"
                        },
                        "type": "image_url"
                    },
                    {
                        "text": "这是什么动物，一般生活在哪些地域",
                        "type": "text"
                    }
                ]
            }
        ]
    },
    "stream": true,
    "parameters": {
        "agent_options": {
            "agent_version": "beta",
            "agent_id": "aid-xxx"
        }
    }
}
```

### **返回示例**

```
data: {
    "status_code": 200,
    "code": "",
    "message": "",
    "output": {
        "choices": [
            {
                "finish_reason": "",
                "message": {
                    "content": "xxx",
                    "additional_kwargs": {},
                    "response_metadata": {
                        "headers": {
                            "vary": "Origin",
                            "x-request-id": "ca7a41ad-3994-9dcf-adf6-f7aa56bec62b",
                            "content-type": "text/event-stream;charset=UTF-8",
                            "x-dashscope-call-gateway": "true",
                            "req-cost-time": "508",
                            "req-arrive-time": "1773800485527",
                            "resp-start-time": "1773800486035",
                            "x-envoy-upstream-service-time": "506",
                            "date": "Wed, 18 Mar 2026 02:21:25 GMT",
                            "server": "istio-envoy",
                            "transfer-encoding": "chunked"
                        }
                    },
                    "type": "ai",
                    "name": null,
                    "id": "run--019cfebf-7194-78b3-ad12-c3df6b6423b1",
                    "example": false,
                    "tool_calls": [],
                    "invalid_tool_calls": [],
                    "usage_metadata": null,
                    "tool_call_chunks": [],
                    "reasoning_content": "",
                    "role": "assistant",
                    "extra": {
                        "group": "generating",
                        "step_change": "generation_start",
                        "step": "generating"
                    }
                }
            }
        ]
    },
    "usage": null,
    "request_id": "xxxx-xxxx"
}
```

### **调用示例**

Python

```
# coding=utf-8

import os
import json
import requests

chat_completions_url = 'https://dashscope.aliyuncs.com/api/v2/apps/web-search-agent/chat/completions'

headers = {
    'Authorization': f'Bearer {os.getenv("DASHSCOPE_API_KEY", "")}',  # 配置 API KEY
    'Content-Type': 'application/json'
}

if __name__ == "__main__":
    params = {
        "input": {
            "messages": [{"role": "user", "content": "目前国内主流多模态模型分别有哪些，根据性能和效果做下分析"}]  # 传入请求消息
        },
        "parameters": {
            "agent_options": {  # 设置 agent 选项
                "agent_id": "${agent_id}",  # 应用ID，可在应用管理页面获取到，例如：aid-8fd***e00
                "agent_version": "${agent_version}"  # 应用版本，beta 测试版本 / release 发布版本
            }
        },
        "stream": True
    }
    
    response = requests.post(chat_completions_url, headers=headers, json=params, stream=True)
    
    resultlist = []
    stage = ''
    action = ''
    content = ''
    reasoning_content = ''
    for chunk in response.iter_lines():
        if chunk:
            chunk_str = chunk.decode('utf-8').strip()
            if chunk_str.startswith('data:'):
                json_str = chunk_str[len('data:'):].strip()
                try:
                    obj = json.loads(json_str)
                    # 检查异常
                    if obj.get('code') != '200':
                        print("服务异常：", obj)
                    # 获取消息体
                    msg = obj.get('output', {}).get('choices', [{}])[0].get('message', {})
                    extra_flags = msg.get('extra', {})  # 获取模型状态标记字段
    
                    if stage != extra_flags.get('group', ''):  # 获取 模型当前阶段
                        print(f"agent stage: {extra_flags.get('group', '')}")
                    stage = extra_flags.get('group', '')
    
                    if action != extra_flags.get('step', '') and extra_flags.get('step', ''):  # 获取 模型当前阶段
                        print(f"agent action: {extra_flags.get('step', '')}")
                    action = extra_flags.get('step', '')
    
                    role = msg.get('role', '')  # 获取模型角色 assistant or role
                    content = msg.get('content')  # 获取生成内容
                    toolcalls = msg.get('tool_calls', [])  # 获取工具调用
                    if toolcalls:
                        print(f'{toolcalls}')
    
                    if role == "tool":
                        print("\\n" + content + "\\n", end='')  # 前后都换行
                    else:
                        print(content, end='')  # 流式输出
                    # 可按需保存
                    resultlist.append(obj)
                except Exception as e:
                    print("异常解析:", e)
```

Java

```
import java.io.*;
import java.net.*;
import java.util.*;
import com.alibaba.fastjson.*;
import java.nio.charset.StandardCharsets;

public class WebSearchStreamDemo {

    // 配置 API KEY
    public final static String CHAT_COMPLETIONS_URL = "https://dashscope.aliyuncs.com/api/v2/apps/web-search-agent/chat/completions";
    public final static String API_KEY = System.getenv("DASHSCOPE_API_KEY");

    public static void main(String[] args) throws Exception {
        // 构造参数
        Map<String, Object> params = new HashMap<>();
        // input.messages
        List<Map<String, Object>> messages = new ArrayList<>();
        Map<String, Object> msgObj = new HashMap<>();
        msgObj.put("role", "user");
        msgObj.put("content", "${prompt}");
        messages.add(msgObj);
        // input
        Map<String, Object> input = new HashMap<>();
        input.put("messages", messages);
        // parameters.agent_options
        Map<String, Object> agentOptions = new HashMap<>(); // 
        agentOptions.put("agent_id", "${agent_id}");// 应用ID，可在应用管理页面获取到，例如：aid-8fd***e00
        agentOptions.put("agent_version", "${agent_version}"); // 应用版本，beta 测试版本 / release 发布版本
        // parameters
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("agent_options", agentOptions);

        params.put("input", input);
        params.put("parameters", parameters);
        params.put("stream", true);

        String body = JSON.toJSONString(params);

        // HTTP 请求
        URL apiUrl = new URL(CHAT_COMPLETIONS_URL);
        HttpURLConnection conn = (HttpURLConnection) apiUrl.openConnection();
        conn.setRequestMethod("POST");
        conn.setDoOutput(true);
        conn.setRequestProperty("Authorization", "Bearer " + API_KEY);
        conn.setRequestProperty("Content-Type", "application/json");

        // 发送 body
        try (OutputStream os = conn.getOutputStream()) {
            os.write(body.getBytes(StandardCharsets.UTF_8));
        }

        // 处理流式响应
        InputStream inputStream = conn.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8));
        String line;
        String stage = "";
        String action = "";
        List<JSONObject> resultList = new ArrayList<>();

        while ((line = reader.readLine()) != null) {
            if (!line.trim().isEmpty()) {
                String chunkStr = line.trim();
                if (chunkStr.startsWith("data:")) {
                    String jsonStr = chunkStr.substring(5).trim();
                    try {
                        JSONObject obj = JSON.parseObject(jsonStr);
                        // 检查异常
                        if (!"200".equals(obj.getString("code"))) {
                            System.out.print("服务异常: " + obj);
                        }
                        // 获取  output->choices[0]->message
                        JSONObject msg = null;
                        if (obj.containsKey("output")) {
                            JSONObject output = obj.getJSONObject("output");
                            if (output != null && output.containsKey("choices")) {
                                JSONArray choices = output.getJSONArray("choices");
                                if (choices != null && !choices.isEmpty()) {
                                    JSONObject firstChoice = choices.getJSONObject(0);
                                    if (firstChoice.containsKey("message")) {
                                        msg = firstChoice.getJSONObject("message");
                                    }
                                }
                            }
                        }
                        if (msg == null) {
                            continue;
                        }

                        // 获取 extra_flags 字段
                        JSONObject extraFlags = msg.containsKey("extra") && msg.get("extra") != null
                                ? msg.getJSONObject("extra") : new JSONObject();

                        // agent stage
                        String stageNew = extraFlags.containsKey("group") && extraFlags.get("group") != null
                                ? extraFlags.getString("group") : "";
                        if (!stage.equals(stageNew)) {
                            System.out.println("agent stage: " + stageNew);
                        }
                        stage = stageNew;

                        // agent action
                        String actionNew = extraFlags.containsKey("step") && extraFlags.get("step") != null
                                ? extraFlags.getString("step") : "";
                        if (!action.equals(actionNew) && !actionNew.isEmpty()) {
                            System.out.println("agent action: " + actionNew);
                        }
                        action = actionNew;

                        String role = msg.containsKey("role") && msg.get("role") != null
                                ? msg.getString("role") : "";

                        Object contentObj = msg.get("content");
                        String content = null;
                        boolean isContentString = false;
                        // content 是字符串类型
                        if (contentObj instanceof String) {
                            content = contentObj.toString();
                            isContentString = true;
                        }

                        // 字符串为空时补 reasoning_content
                        if (isContentString && content.isEmpty()) {
                            Object reasoningContentObj = msg.get("reasoning_content");
                            if (reasoningContentObj instanceof String) {
                                content = reasoningContentObj.toString();
                            }
                        }

                        // 工具调用
                        if (msg.containsKey("tool_calls") && msg.get("tool_calls") instanceof List) {
                            JSONArray toolCalls = msg.getJSONArray("tool_calls");
                            if (!toolCalls.isEmpty()) {
                                System.out.println(toolCalls);
                            }
                        }

                       if ("tool".equals(role)) {
                            System.out.print("\\n" + content + "\\n");
                        } else {
                            System.out.print(content);
                        }

                        // 可按需保存
                        resultList.add(obj);
                    } catch (Exception e) {
                        System.out.println("异常解析: " + e);
                    }
                }
            }
        }
        reader.close();
    }
}
```
