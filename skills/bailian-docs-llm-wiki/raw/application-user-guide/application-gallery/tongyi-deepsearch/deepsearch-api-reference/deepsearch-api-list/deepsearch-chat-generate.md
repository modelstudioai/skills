# 生成对话

基于智能体应用管理提供的 agent\_id 与 agent\_version 信息，提供场景化对话、研究、写作相关能力。

## **请求语法**

```
POST /deep-search-agent/chat/completions HTTP/1.1
```

## **请求参数**

**参数名**

**类型**

**是否必须**

**说明**

stream

bool

是

**必须填 true**，当前版本仅支持流式响应。若提供`false`或不提供，请求将失败

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

角色，枚举值为：`user`、`assistant`

input.messages.\[\].content

str

是

生成内容

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

parameters.agent\_options.session\_files

array\[string\]

否

动态文件 ID 列表，文件 ID 的获取参考文件上传文档，最大支持传入10个文件ID

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

生成结束原因，仅尾包输出`stop`

output.choices.\[\].message

object

是

对话消息

output.choices.\[\].message.role

str

是

角色，枚举值为：`user`、`assistant`、`tool`

output.choices.\[\].message.content

str | array\[object\]

是

生成内容/工具返回内容，当生成配置开启输出报告时，报告消息体类型为`array[object]`

output.choices.\[\].message.reasoning\_content

str

否

思考内容，如果 content内没有内容，则尝试获取最后一轮深度思考中的reasoning\_content内容

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

### **计划枚举**

**执行阶段（**`**group**`**）**

**描述**

**说明**

planning

计划中

对应plan模型，即系统处于任务规划阶段，该阶段包含 start 和 end 事件

generating

生成中

表示为写作模型，表示系统正处于报告生成阶段，此阶段不区分详细事件变化，无 start/end 事件；step 状态仅包括 thinking 和 generating，且不会调用工具。

**当前步骤（**`**step**`**）**

**描述和说明**

planning

计划中

thinking

思考中

reporting

总结中（法律场景特有）

generating

生成中

tool\_calling

工具调用中

tool\_calling\_{工具名称}

工具调用中，附带工具名称

-   由于模型原因 step\_change 值可能为不存在，请尽可能使用持久化的标志step
    
-   空包情况下 step、step\_change、group 字段的值可能不存在
    
-   plan、think、generation 均由 xxx\_start 事件 和 xxx\_end 事件两个事件组成
    
-   tool\_call 由 tool\_call\_start、tool\_calling、tool\_return 三个事件组成
    
-   tool\_call\_start 表示工具调用开始（开始流式收集工具调用信息，此时还无法吐出工具调用详情（name、args等））、tool\_calling 表示获取到完整工具调用的参数并会抛出完整的工具调用参数tool\_return 表示工具调用返回结果，同时会携带结构化的工具返回信息。
    

**步骤变化事件 (**`**step_change**`**)**

**事件发生时** `**step**` **的值**

**事件名称**

**解释说明**

plan\_start

`planning`

开始规划

`step` 状态变为 `planning`, 表示对应状态的开头（包含当前包）。

plan\_end

`planning`

结束规划

`step` 开始变成其他状态，事件发生时 `step` 仍为 `planning`，表示对应状态的结尾（包含当前包）。

think\_start

`thinking`

开始思考

与 `plan` 事件同理

think\_end

`thinking`

结束思考

与 `plan` 事件同理

report\_start

`reporting`

开始总结

与 `plan` 事件同理

report\_end

`reporting`

结束总结

与 `plan` 事件同理

generation\_start

`generating`

开始生成

与 `plan` 事件同理

generation\_end

`generating`

结束生成

与 `plan` 事件同理

tool\_call\_start

`tool_calling`

开始工具调用

表示工具调用开始（开始流式收集工具调用信息，此时还无法吐出工具调用详情（name、arguments等））。

tool\_calling

`tool_calling_{工具名称}`

工具调用中

会输出tool\_call的具体参数和工具名称，`tool_calling`状态变为`tool_calling_{工具名称}`。

tool\_return

`tool_calling_{工具名称}`

工具返回

会携带工具返回信息， `step` 开始变成其他状态，事件发生时 `step` 仍为 `tool_calling_{工具名称}`。

## **示例**

### **请求示例**

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
    "parameters": {
        "agent_options": {
            "agent_id": "aid-xxx",
            "agent_version": "beta"
        }
    }
}
```

### **返回示例**

```
data: {
    "code": "200",
    "message": "",
    "output": {
        "choices": [{
            "finish_reason": "",
            "message": {
                "content": "",
                "additional_kwargs": {},
                "response_metadata": {},
                "tool_calls": [],
                "reasoning_content": "",
                "role": "assistant",
                "extra": {
                    "group": "planning",
                    "step_change": "think_start",
                    "step": "thinking"
                }
            }
        }]
    },
    "usage": null,
    "request_id": "5b853312-8d0c-42ff-9d26-08339d5ff38e"
}
```

当生成配置开启输出报告时，模型尾包会给出 html 和 md 的存储地址和路径，content 中 type 的含义参考如下

-   file\_path：文件存储路径用于后续导出pdf和二次获取以下文件下载链接
    
-   md\_file\_url：md下载链接
    
-   html\_file\_url：html下载链接
    

```
{
  "status_code": 200,
  "code": "",
  "message": "",
  "output": {
    "choices": [
      {
        "finish_reason": "stop", 
        "message": {
          "content": [
            {
              "type": "file_path", 
              "text": "msearch/agents/files/upload/536fa835-a381-4870-99c1-79dee3ab946c"
            },
            {
              "type": "md_file_url", 
              "text": "https://msearch-cloud.oss-cn-hangzhou.aliyuncs.com/msearch/agents/files/upload/536fa835-a381-4870-99c1-79dee3ab946c.md?x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-date=20250904T151053Z&x-oss-expires=900&x-oss-credential=LTAI5tCLjk1ruCfq2caq****%2F20250904%2Fcn-hangzhou%2Foss%2Faliyun_v4_request&x-oss-signature=9f9af4642f3611b1b8210bd801f10610236656a016e6bda67e2239ecf59b644f"
            },
            {
              "type": "html_file_url", 
              "text": "https://msearch-cloud.oss-cn-hangzhou.aliyuncs.com/msearch/agents/files/upload/536fa835-a381-4870-99c1-79dee3ab946c.html?x-oss-signature-version=OSS4-HMAC-SHA256&x-oss-date=20250904T151053Z&x-oss-expires=900&x-oss-credential=LTAI5tCLjk1ruCfq2caq****%2F20250904%2Fcn-hangzhou%2Foss%2Faliyun_v4_request&x-oss-signature=34164425671a0f26a39adacd12735d9ec127aec8caa68f8e1de6e252f5889a9c"
            }
          ],
          "additional_kwargs": {},
          "response_metadata": {
            "model_name": "deep-research-generation",
            "agent_name": "writing_agent"
          },
          "tool_calls": [],
          "reasoning_content": "",
          "role": "assistant"
        }
      }
    ]
  },
  "usage": null,
  "request_id": "3070fa78-c5d5-4bad-b2fc-e20787f6eb75"
}
```

## **调用示例**

Python

```
# coding=utf-8

import os
import json
import requests

split_line = "\\n-------------------------------------生成报告链接---------------------------------------------------\\n"

chat_completions_url = 'https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/chat/completions'

headers = {
    'Authorization': f'Bearer {os.getenv("DASHSCOPE_API_KEY", "")}',  # 配置 API KEY
    'Content-Type': 'application/json'
}

if __name__ == "__main__":
    params = {
        "input": {
            "messages": [{"role": "user", "content": "目前国内主流多模态模型分别有哪些，根据性能和效果做下评估"}]  # 传入请求消息
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
    
                    if not content:  # 如果 content内没有内容，则尝试获取最后一轮深度思考中的reasoning_content内容
                        content = msg.get('reasoning_content', '')
    
                    if isinstance(content, str):
                        if role == "tool":
                            print("\\n" + content + "\\n", end='')  # 前后都换行
                        else:
                            print(content, end='')  # 流式输出
                    else:
                        # 注意 content 可能不是字符串
                        print(split_line, content)
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

public class DeepSearchStreamDemo {

    // 配置 API KEY
    public final static String CHAT_COMPLETIONS_URL = "https://dashscope.aliyuncs.com/api/v2/apps/deep-search-agent/chat/completions";
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

                        // -------输出内容判断--------
                        if (isContentString) {
                            // 是字符串，无论空不空都直接打印（和Python一致）
                            if ("tool".equals(role)) {
                                System.out.print("\\n" + content + "\\n");
                            } else {
                                System.out.print(content);
                            }
                        } else {
                            // 不是字符串（比如Object/Array）时打印分隔线，再打印内容
                            System.out.println("\\n------------------------------------------------------------------生成报告链接------------------------------------------------------------------");
                            System.out.println(contentObj != null ? contentObj.toString() : "null");
                        }
                        // ------end----

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
