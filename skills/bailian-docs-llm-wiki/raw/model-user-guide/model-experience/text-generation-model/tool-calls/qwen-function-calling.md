# Function Calling

大模型无法访问实时数据和外部系统。Function Calling 允许模型调用外部工具（API、数据库、自定义函数等），获取信息或执行操作，突破模型自身能力的限制。

## 工作原理

Function Calling 通过应用程序与大模型之间的多步骤交互实现：

1.  **发起第一次模型调用**
    
    应用程序向大模型发送用户问题和可用工具清单。
    
2.  **接收模型的工具调用指令（工具名称与入参）**
    
    若模型判断需要调用外部工具，返回JSON格式的指令，指定函数名称与入参。
    
    > 若模型判断无需调用工具，会返回自然语言格式的回复。
    
3.  **在应用端运行工具**
    
    应用程序执行指定工具，获取输出结果。
    
4.  **发起第二次模型调用**
    
    将工具输出结果添加到消息数组（messages），再次调用模型。
    
5.  **接收来自模型的最终响应**
    
    模型综合工具输出与用户问题，生成自然语言回复。
    

工作流程示意图：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9256127871/CAEQYhiBgIDE9unxyRkiIDVjNDgwMDBjYTE0NzQ5MTBiMzBiNjJkNTk5ZjE2YTIz4358988_20240409160230.951.svg)

## 支持的模型

#### 千问

-   **文本生成模型**
    -   千问Max：Qwen3.8-Max系列、Qwen3.7-Max系列、Qwen3.6-Max系列、Qwen3-Max系列、Qwen-Max系列
    -   千问Plus：Qwen3.7-Plus系列、Qwen3.6-Plus系列、Qwen3.5-Plus系列、Qwen-Plus系列
    -   千问Flash：Qwen3.8-Flash系列、Qwen3.7-Flash系列、Qwen3.6-Flash系列、Qwen3.5-Flash系列、Qwen-Flash系列
    -   千问Coder：Qwen3-Coder系列、Qwen2.5-Coder系列、Qwen-Coder系列
    -   千问Turbo：Qwen-Turbo系列
    -   Qwen3.6开源系列
    -   Qwen3.5开源系列
    -   Qwen3开源系列
    -   Qwen2.5开源系列
    -   Qwen3.8开源系列
-   **多模态模型**
    -   千问VL： Qwen3-VL-Plus系列、 Qwen3-VL-Flash系列
    -   千问Omni：Qwen3.8-Omni-Flash、Qwen3.5-Omni-Plus系列、Qwen3.5-Omni-Flash系列、Qwen3-Omni-Flash系列
    -   千问Omni-Realtime：Qwen3.8-Omni-Flash-Realtime、Qwen3.5-Omni-Plus-Realtime系列、Qwen3.5-Omni-Flash-Realtime系列
    -   Qwen3-VL 开源系列
-   **语音对话模型**
    -   千问Audio-Realtime：Qwen-Audio-3.1-Realtime-Plus、Qwen-Audio-3.0-Realtime-Plus系列、Qwen-Audio-3.0-Realtime-Flash系列

#### DeepSeek

-   阿里云百炼部署
    
    -   deepseek-v4-pro
    -   deepseek-v4-flash
    -   deepseek-v3.2
    -   deepseek-v3.2-exp（非思考模式）
    -   deepseek-v3.1（非思考模式）
    -   deepseek-r1
    -   deepseek-r1-0528
    -   deepseek-v3
-   硅基流动部署
    
    -   siliconflow/deepseek-v3.2
    -   siliconflow/deepseek-v3.1-terminus
    -   siliconflow/deepseek-r1-0528
    -   siliconflow/deepseek-v3-0324
-   快手万擎部署
    
    -   vanchin/deepseek-v3.2-think
    -   vanchin/deepseek-v3.1-terminus
    -   vanchin/deepseek-r1
    -   vanchin/deepseek-v3

#### GLM

**重要**调用 GLM 系列模型的 Function Calling 时，需在请求中传入 extra\_body={"tool\_stream": True}，否则模型不会返回 tool\_calls，工具调用不生效。glm-5.3 的 tool\_stream 默认值为 true，无需显式传入。

-   glm-5.3
-   glm-5.2
-   glm-5.1
-   glm-5
-   glm-4.7
-   glm-4.6
-   glm-4.5
-   glm-4.5-air

#### Kimi

-   阿里云百炼部署
    
    -   kimi-k3
    -   kimi-k2.7-code
    -   kimi-k2.6
    -   kimi-k2.5
    -   kimi-k2-thinking
    -   Moonshot-Kimi-K2-Instruct
-   月之暗面部署
    
    -   kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6、kimi/kimi-k2.5

> 在思考模式下，使用 kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6、kimi/kimi-k2.5 进行工具调用时，需在每轮 assistant 消息中保留 `reasoning_content` 字段；`tool_choice` 支持 `"auto"`（默认）、`"none"`，kimi/kimi-k3 还支持 `"required"`，否则会报错。

#### MiniMax

-   阿里云百炼部署
    
    -   MiniMax-M2.5
    -   MiniMax-M2.1
-   稀宇科技部署
    
    -   MiniMax/MiniMax-M3
    -   MiniMax/MiniMax-M2.7
    -   MiniMax/MiniMax-M2.5
    -   MiniMax/MiniMax-M2.1

## 快速开始

您需要已获取与配置 API Key并配置API Key到环境变量。如果通过 OpenAI SDK或 DashScope SDK调用，还需安装SDK。

以下示例演示天气查询场景的完整 Function Calling 流程。

#### OpenAI 兼容

python

```
from openai import OpenAI
from datetime import datetime
import json
import os
import random

# 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
# 模拟用户问题
USER_QUESTION = "北京天气咋样"
# 定义工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
]

# 模拟天气查询工具
def get_current_weather(arguments):
    weather_conditions = ["晴天", "多云", "雨天"]
    random_weather = random.choice(weather_conditions)
    location = arguments["location"]
    return f"{location}今天是{random_weather}。"

# 封装模型响应函数
def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen3.8-max",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
    )
    return completion

messages = [{"role": "user", "content": USER_QUESTION}]
response = get_response(messages)
assistant_output = response.choices[0].message
if assistant_output.content is None:
    assistant_output.content = ""
messages.append(assistant_output)
# 如果不需要调用工具，直接输出内容
if assistant_output.tool_calls is None:
    print(f"无需调用天气查询工具，直接回复：{assistant_output.content}")
else:
    # 进入工具调用循环
    while assistant_output.tool_calls is not None:
        # 遍历本轮返回的全部工具调用，避免只处理第一个而遗漏其余工具的返回结果
        for tool_call in assistant_output.tool_calls:
            tool_call_id = tool_call.id
            func_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"正在调用工具 [{func_name}]，参数：{arguments}")
            # 执行工具
            tool_result = get_current_weather(arguments)
            # 构造工具返回信息
            tool_message = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": tool_result,  # 保持原始工具输出
            }
            print(f"工具返回：{tool_message['content']}")
            messages.append(tool_message)
        # 再次调用模型，获取总结后的自然语言回复
        response = get_response(messages)
        assistant_output = response.choices[0].message
        if assistant_output.content is None:
            assistant_output.content = ""
        messages.append(assistant_output)
    print(f"助手最终回复：{assistant_output.content}")
```

javascript

```
import OpenAI from 'openai';

// 初始化客户端
const openai = new OpenAI({
  // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
  // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
  baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

// 定义工具列表
const tools = [
  {
    type: "function",
    function: {
      name: "get_current_weather",
      description: "当你想查询指定城市的天气时非常有用。",
      parameters: {
        type: "object",
        properties: {
          location: {
            type: "string",
            description: "城市或县区，比如北京市、杭州市、余杭区等。",
          },
        },
        required: ["location"],
      },
    },
  },
];

// 模拟天气查询工具
const getCurrentWeather = (args) => {
  const weatherConditions = ["晴天", "多云", "雨天"];
  const randomWeather = weatherConditions[Math.floor(Math.random() * weatherConditions.length)];
  const location = args.location;
  return `${location}今天是${randomWeather}。`;
};

// 封装模型响应函数
const getResponse = async (messages) => {
  const response = await openai.chat.completions.create({
    model: "qwen3.8-max",
    enable_thinking: false,
    messages: messages,
    tools: tools,
  });
  return response;
};

const main = async () => {
  const input = "北京天气咋样";

  let messages = [
    {
      role: "user",
      content: input,
    }
  ];
  let response = await getResponse(messages);
  let assistantOutput = response.choices[0].message;
  // 确保 content 不是 null
  if (!assistantOutput.content) assistantOutput.content = "";
  messages.push(assistantOutput);
  // 判断是否需要调用工具
  if (!assistantOutput.tool_calls) {
    console.log(`无需调用天气查询工具，直接回复：${assistantOutput.content}`);
  } else {
    // 进入工具调用循环
    while (assistantOutput.tool_calls) {
      // 遍历本轮返回的全部工具调用，避免只处理第一个而遗漏其余工具的返回结果
      for (const toolCall of assistantOutput.tool_calls) {
        const toolCallId = toolCall.id;
        const funcName = toolCall.function.name;
        const funcArgs = JSON.parse(toolCall.function.arguments);
        console.log(`正在调用工具 [${funcName}]，参数：`, funcArgs);
        // 执行工具
        const toolResult = getCurrentWeather(funcArgs);
        // 构造工具返回信息
        const toolMessage = {
          role: "tool",
          tool_call_id: toolCallId,
          content: toolResult,
        };
        console.log(`工具返回：${toolMessage.content}`);
        messages.push(toolMessage);
      }
      // 再次调用模型获取自然语言总结
      response = await getResponse(messages);
      assistantOutput = response.choices[0].message;
      if (!assistantOutput.content) assistantOutput.content = "";
      messages.push(assistantOutput);
    }
    console.log(`助手最终回复：${assistantOutput.content}`);
  }
};

// 启动程序
main().catch(console.error);
```

#### DashScope

python

```
import os
from dashscope import MultiModalConversation
import json
import random
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 1. 定义工具列表
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    }
]

# 2. 模拟天气查询工具
def get_current_weather(arguments):
    weather_conditions = ["晴天", "多云", "雨天"]
    random_weather = random.choice(weather_conditions)
    location = arguments["location"]
    return f"{location}今天是{random_weather}。"

# 3. 封装模型响应函数
def get_response(messages):
    response = MultiModalConversation.call(
        # 如果没有配置环境变量，请将下行替换为api_key="sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 此处以多模态模型 qwen3.8-max 为例。若调用 qwen3.6-max-preview、qwen-plus 等纯文本模型需使用纯文本模型接口，参见https://help.aliyun.com/model-studio/qwen-api-via-dashscope
        model="qwen3.8-max",
        enable_thinking=False,
        messages=messages,
        tools=tools,
        result_format="message",
    )
    return response

# 4. 初始化对话历史
messages = [
    {
        "role": "user",
        "content": [{"text": "北京天气咋样"}]
    }
]

# 5. 第一次调用模型
response = get_response(messages)
assistant_output = response.output.choices[0].message
messages.append(assistant_output)

# 6. 判断是否需要调用工具
if "tool_calls" not in assistant_output or not assistant_output["tool_calls"]:
    print(f"无需调用工具，直接回复：{assistant_output['content']}")
else:
    # 7. 进入工具调用循环
    # 循环条件：只要最新的模型回复中包含工具调用请求
    while "tool_calls" in assistant_output and assistant_output["tool_calls"]:
        tool_call = assistant_output["tool_calls"][0]
        # 解析工具调用的信息
        func_name = tool_call["function"]["name"]
        arguments = json.loads(tool_call["function"]["arguments"])
        tool_call_id = tool_call.get("id")  # 获取 tool_call_id
        print(f"正在调用工具 [{func_name}]，参数：{arguments}")
        # 执行对应的工具函数
        tool_result = get_current_weather(arguments)
        # 构造工具返回信息
        tool_message = {
            "role": "tool",
            "content": tool_result,
            "tool_call_id": tool_call_id
        }
        print(f"工具返回：{tool_message['content']}")
        messages.append(tool_message)
        # 再次调用模型，让模型基于工具结果进行回复
        response = get_response(messages)
        assistant_output = response.output.choices[0].message
        messages.append(assistant_output)
    # 8. 输出最终的自然语言回复
    content = assistant_output["content"]
    if isinstance(content, list) and content:
        content = content[0].get("text", "") if isinstance(content[0], dict) else str(content[0])
    print(f"助手最终回复：{content}")
```

java

```
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.tools.FunctionDefinition;
import com.alibaba.dashscope.tools.ToolCallBase;
import com.alibaba.dashscope.tools.ToolCallFunction;
import com.alibaba.dashscope.tools.ToolFunction;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Random;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    /**
     * 从 MultiModalMessage 的 content 中提取纯文本。
     * content 格式为 List<Map<String, String>>，例如：[{text=天气是晴天}]
     */
    @SuppressWarnings("unchecked")
    public static String getTextContent(Object content) {
        if (content instanceof List) {
            for (Object item : (List<?>) content) {
                if (item instanceof Map) {
                    Object text = ((Map<String, Object>) item).get("text");
                    if (text != null) return text.toString();
                }
            }
        }
        return content != null ? content.toString() : "";
    }

    /**
     * 第一步：定义工具的本地实现。
     * @param arguments 模型传入的、包含工具所需参数的JSON字符串。
     * @return 工具执行后的结果字符串。
     */
    public static String getCurrentWeather(String arguments) {
        try {
            // 模型提供的参数是JSON格式的，需要我们手动解析。
            ObjectMapper objectMapper = new ObjectMapper();
            JsonNode argsNode = objectMapper.readTree(arguments);
            String location = argsNode.get("location").asText();

            // 用随机结果来模拟真实的API调用或业务逻辑。
            List<String> weatherConditions = Arrays.asList("晴天", "多云", "雨天");
            String randomWeather = weatherConditions.get(new Random().nextInt(weatherConditions.size()));

            return location + "今天是" + randomWeather + "。";
        } catch (Exception e) {
            // 异常处理，确保程序健壮性。
            return "无法解析地点参数。";
        }
    }

    public static void main(String[] args) {
        try {
            // 第二步：向模型描述（注册）我们的工具。
            String weatherParamsSchema =
                    "{\"type\":\"object\",\"properties\":{\"location\":{\"type\":\"string\",\"description\":\"城市或县区，比如北京市、杭州市、余杭区等。\"}},\"required\":[\"location\"]}";

            FunctionDefinition weatherFunction = FunctionDefinition.builder()
                    .name("get_current_weather") // 工具的唯一标识名，必须与本地实现对应。
                    .description("当你想查询指定城市的天气时非常有用。") // 清晰的描述能帮助模型更好地决定何时使用该工具。
                    .parameters(JsonUtils.parseString(weatherParamsSchema).getAsJsonObject())
                    .build();
            MultiModalConversation conv = new MultiModalConversation();
            String userInput = "北京天气咋样";

            List<MultiModalMessage> messages = new ArrayList<>();
            messages.add(MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("text", userInput))).build());

            // 第四步：首次调用模型。将用户的请求和我们定义好的工具列表一同发送给模型。
            MultiModalConversationParam param = MultiModalConversationParam.builder()
                    .model("qwen3.8-max") //此处以多模态模型 qwen3.8-max 为例。若调用 qwen3.6-max-preview、qwen-plus 等纯文本模型需使用纯文本模型接口，参见https://help.aliyun.com/model-studio/qwen-api-via-dashscope
                    .enableThinking(false)
                    .apiKey(System.getenv("DASHSCOPE_API_KEY")) // 从环境变量中获取API Key。
                    .messages(messages) // 传入当前的对话历史。
                    .tools(Arrays.asList(ToolFunction.builder().function(weatherFunction).build())) // 传入可用的工具列表。
                    .build();

            MultiModalConversationResult result = conv.call(param);
            MultiModalMessage assistantOutput = result.getOutput().getChoices().get(0).getMessage();
            messages.add(assistantOutput); // 将模型的首次回复也加入到对话历史中。

            // 第五步：检查模型的回复，判断它是否请求调用工具。
            if (assistantOutput.getToolCalls() == null || assistantOutput.getToolCalls().isEmpty()) {
                // 情况A：模型没有调用工具，而是直接给出了回答。
                System.out.println("无需调用天气查询工具，直接回复：" + getTextContent(assistantOutput.getContent()));
            } else {
                // 情况B：模型决定调用工具。
                // 使用 while 循环可以处理模型连续调用多次工具的场景。
                while (assistantOutput.getToolCalls() != null && !assistantOutput.getToolCalls().isEmpty()) {
                    ToolCallBase toolCall = assistantOutput.getToolCalls().get(0);

                    // 从模型的回复中解析出工具调用的具体信息（要调用的函数名、参数）。
                    ToolCallFunction functionCall = (ToolCallFunction) toolCall;
                    String funcName = functionCall.getFunction().getName();
                    String funcArguments = functionCall.getFunction().getArguments();
                    System.out.println("正在调用工具 [" + funcName + "]，参数：" + funcArguments);

                    // 根据工具名，在本地执行对应的Java方法。
                    String toolResult = getCurrentWeather(funcArguments);

                    // 构造一个 role 为 "tool" 的消息，其中包含工具的执行结果。
                    MultiModalMessage toolMessage = MultiModalMessage.builder()
                            .role("tool")
                            .toolCallId(toolCall.getId())
                            .content(Arrays.asList(Collections.singletonMap("text", toolResult)))
                            .build();
                    System.out.println("工具返回：" + toolResult);
                    messages.add(toolMessage); // 将工具的返回结果也加入到对话历史中。

                    // 第六步：再次调用模型。
                    param.setMessages((List) messages);
                    result = conv.call(param);
                    assistantOutput = result.getOutput().getChoices().get(0).getMessage();
                    messages.add(assistantOutput);
                }

                // 第七步：打印模型经过总结后，生成的最终回复。
                System.out.println("助手最终回复：" + getTextContent(assistantOutput.getContent()));
            }

        } catch (NoApiKeyException | UploadFileException e) {
            System.err.println("错误: " + e.getMessage());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

运行后得到如下输出：

```
正在调用工具 [get_current_weather]，参数：{'location': '北京'}
工具返回：北京今天是多云。
助手最终回复：北京今天是多云的天气。
```

## 如何使用

Function Calling 支持两种传入工具信息的方式：

-   方式一：通过 tools 参数传入（推荐）
    
    参见[如何使用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#038e24005c1vt)，按照**定义工具**、**创建 messages 数组**、**发起 Function Calling**、**运行工具函数**、**大模型总结工具函数输出**的步骤调用。
    
-   方式二：通过 System Message 传入
    
    通过 tools 参数传入效果最佳，服务端会自动适配最优 prompt 模板。如使用 Qwen 模型且不期望使用 tools 参数，参见[通过 System Message 传入工具信息](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)。
    

以下以 OpenAI 兼容接口为例，通过 tools 参数分步骤介绍 Function Calling 的详细用法。

假设业务场景会收到天气查询与时间查询两类问题。

### 1\. 定义工具

工具连接大模型与外部服务，首先需定义工具。

#### 1.1. 创建工具函数

创建两个工具函数：天气查询工具与时间查询工具。

-   **天气查询工具**
    
    接收`arguments`参数，`arguments`格式为`{"location": "查询的地点"}`。工具的输出为字符串，格式为：`“{位置}今天是{天气}”`。
    
    > 为了便于演示，此处定义的天气查询工具并不真正查询天气，会从晴天、多云、雨天随机选择。在实际业务中可使用如 [高德天气查询](https://lbs.amap.com/api/webservice/guide/api/weatherinfo) 等工具进行替换。
    
-   **时间查询工具**
    
    时间查询工具不需要输入参数。工具的输出为字符串，格式为：`“当前时间：{查询到的时间}。”`。
    
    > 如果使用 Node.js，请运行 `npm install date-fns` 安装获取时间的工具包 date-fns：
    

python

```
## 步骤1.1:定义工具函数

# 添加导入random模块
import random
from datetime import datetime

# 模拟天气查询工具。返回结果示例：“北京今天是雨天。”
def get_current_weather(arguments):
    # 定义备选的天气条件列表
    weather_conditions = ["晴天", "多云", "雨天"]
    # 随机选择一个天气条件
    random_weather = random.choice(weather_conditions)
    # 从 JSON 中提取位置信息
    location = arguments["location"]
    # 返回格式化的天气信息
    return f"{location}今天是{random_weather}。"

# 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"

# 测试工具函数并输出结果，运行后续步骤时可以去掉以下四句测试代码
print("测试工具输出：")
print(get_current_weather({"location": "上海"}))
print(get_current_time())
print("\n")
```

javascript

```
// 步骤1.1:定义工具函数

// 导入时间查询工具
import { format } from 'date-fns';

function getCurrentWeather(args) {
    // 定义备选的天气条件列表
    const weatherConditions = ["晴天", "多云", "雨天"];
    // 随机选择一个天气条件
    const randomWeather = weatherConditions[Math.floor(Math.random() * weatherConditions.length)];
    // 从 JSON 中提取位置信息
    const location = args.location;
    // 返回格式化的天气信息
    return `${location}今天是${randomWeather}。`;
}

function getCurrentTime() {
    // 获取当前日期和时间
    const currentDatetime = new Date();
    // 格式化当前日期和时间
    const formattedTime = format(currentDatetime, 'yyyy-MM-dd HH:mm:ss');
    // 返回格式化后的当前时间
    return `当前时间：${formattedTime}。`;
}

// 测试工具函数并输出结果，运行后续步骤时可以去掉以下四句测试代码
console.log("测试工具输出：")
console.log(getCurrentWeather({location:"上海"}));
console.log(getCurrentTime());
console.log("\n")
```

运行工具后，得到输出：

```
测试工具输出：
上海今天是多云。
当前时间：2025-01-08 20:21:45。
```

#### 1.2 创建 tools 数组

人类选择工具前需了解工具的功能、使用场景和输入参数。大模型同理——模型依据这些信息选择合适的工具。按以下JSON格式提供工具信息。

-   `type`字段固定为`"function"`；
    
-   `function`字段为 Object 类型；
    
    -   `name`字段为自定义的工具函数名称，建议使用与函数相同的名称，如`get_current_weather`或`get_current_time`；
        
    -   `description`字段是对工具函数功能的描述，大模型会参考该字段来选择是否使用该工具函数。
        
    -   `parameters`字段是对工具函数入参的描述，类型是 Object ，大模型会参考该字段来进行入参的提取。如果工具函数不需要输入参数，则无需指定`parameters`参数。
        
        -   `type`字段固定为`"object"`；
        -   `properties`字段描述了入参的名称、数据类型与描述，为 Object 类型，Key 值为入参的名称，Value 值为入参的数据类型与描述；
        -   `required`字段指定哪些参数为必填项，为 Array 类型。

对于天气查询工具来说，工具描述信息的格式如下：

```
{
    "type": "function",
    "function": {
        "name": "get_current_weather",
        "description": "当你想查询指定城市的天气时非常有用。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                }
            },
            "required": ["location"]
        }
    }
}
```

发起 Function Calling 前，在代码中定义工具信息数组（tools），包含每个工具的函数名、描述和参数定义。该数组在后续请求时作为参数传入。

python

```
# 请将以下代码粘贴到步骤1.1代码后

## 步骤1.2:创建 tools 数组

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"]
            }
        }
    }
]
tool_name = [tool["function"]["name"] for tool in tools]
print(f"创建了{len(tools)}个工具，为：{tool_name}\n")
```

javascript

```
// 请将以下代码粘贴到步骤1.1代码后

// 步骤1.2:创建 tools 数组

const tools = [
    {
      type: "function",
      function: {
        name: "get_current_time",
        description: "当你想知道现在的时间时非常有用。",
        parameters: {}
      }
    },
    {
      type: "function",
      function: {
        name: "get_current_weather",
        description: "当你想查询指定城市的天气时非常有用。",
        parameters: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "城市或县区，比如北京市、杭州市、余杭区等。",
            }
          },
          required: ["location"]
        }
      }
    }
  ];

const toolNames = tools.map(tool => tool.function.name);
console.log(`创建了${tools.length}个工具，为：${toolNames.join(', ')}\n`);
```

### 2\. 创建messages数组

Function Calling 通过 messages 数组向大模型传入指令与上下文。发起调用前，messages 数组需包含 System Message 和 User Message。

#### System Message

尽管在[创建 tools 数组](https://help.aliyun.com/zh/model-studio/qwen-function-calling#b7c8a0e72a9d0)时已描述了工具的功能和使用场景，但在 System Message 中进一步强调何时调用工具，通常能提高工具调用的准确率。当前场景可将 System Prompt 设置为：

```
你是一个很有帮助的助手。如果用户提问关于天气的问题，请调用 ‘get_current_weather’ 函数;
如果用户提问关于时间的问题，请调用‘get_current_time’函数。
请以友好的语气回答问题。
```

#### User Message

User Message 用于传入用户提问的问题。假设用户提问“上海天气”，此时的 messages 数组为：

python

```
# 步骤2:创建messages数组
# 请将以下代码粘贴到步骤1.2 代码后
# 文本生成模型的 User Message示例
messages = [
    {
        "role": "system",
        "content": """你是一个很有帮助的助手。如果用户提问关于天气的问题，请调用 ‘get_current_weather’ 函数;
     如果用户提问关于时间的问题，请调用‘get_current_time’函数。
     请以友好的语气回答问题。""",
    },
    {
        "role": "user",
        "content": "上海天气"
    }
]

# 多模态模型的 User Message示例
# messages=[
#  {
#         "role": "system",
#         "content": """你是一个很有帮助的助手。如果用户提问关于天气的问题，请调用 ‘get_current_weather’ 函数;
#      如果用户提问关于时间的问题，请调用‘get_current_time’函数。
#      请以友好的语气回答问题。""",
#     },
#     {"role": "user",
#      "content": [{"type": "image_url","image_url": {"url": "https://img.alicdn.com/imgextra/i2/O1CN01FbTJon1ErXVGMRdsN_!!6000000000405-0-tps-1024-683.jpg"}},
#                  {"type": "text", "text": "根据图像上的地点，查询该地点当前天气"}]},
# ]

print("messages 数组创建完成\n")
```

javascript

```
// 步骤2:创建messages数组
// 请将以下代码粘贴到步骤1.2 代码后
const messages = [
    {
        role: "system",
        content: "你是一个很有帮助的助手。如果用户提问关于天气的问题，请调用 ‘get_current_weather’ 函数; 如果用户提问关于时间的问题，请调用‘get_current_time’函数。请以友好的语气回答问题。",
    },
    {
        role: "user",
        content: "上海天气"
    }
];
// 多模态模型的 User Message示例，
// const messages: [{
//     role: "user",
//     content: [{type: "image_url", image_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}},
//               {type: "text", text: "图中描绘的是什么景象?"}]
//   }];

console.log("messages 数组创建完成\n");
```

> 由于备选工具包含天气查询与时间查询，也可提问关于当前时间的问题。

### 3\. 发起 Function Calling

将创建好的 `tools` 与 `messages` 传入大模型，即可发起一次 Function Calling。大模型会判断是否调用工具。若调用，则返回该工具的函数名与参数。

> 支持的模型参见 [支持的模型](https://help.aliyun.com/zh/model-studio/qwen-function-calling#48631a8d2emg8) 。

python

```
# 步骤3:发起 function calling
# 请将以下代码粘贴到步骤2 代码后

from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

def function_calling():
    completion = client.chat.completions.create(
        model="qwen3.8-max",  # 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools
    )
    print("返回对象：")
    print(completion.choices[0].message.model_dump_json())
    print("\n")
    return completion

print("正在发起function calling...")
completion = function_calling()
```

javascript

```
// 步骤3:发起 function calling
// 请将以下代码粘贴到步骤2 代码后

import OpenAI from "openai";
const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

async function functionCalling() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.8-max",  // 此处以qwen3.8-max为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        enable_thinking: false,
        messages: messages,
        tools: tools
    });
    console.log("返回对象：");
    console.log(JSON.stringify(completion.choices[0].message));
    console.log("\n");
    return completion;
}

const completion = await functionCalling();
```

由于用户提问为上海天气，大模型指定需要使用的工具函数名称为：`"get_current_weather"`，函数的入参为：`"{\"location\": \"上海\"}"`。

```
{
    "content": "",
    "refusal": null,
    "role": "assistant",
    "audio": null,
    "function_call": null,
    "tool_calls": [
        {
            "id": "call_6596dafa2a6a46f7a217da",
            "function": {
                "arguments": "{\"location\": \"上海\"}",
                "name": "get_current_weather"
            },
            "type": "function",
            "index": 0
        }
    ]
}
```

需要注意，如果问题被大模型判断为无需使用工具，会通过`content`参数直接回复。在输入“你好”时，`tool_calls`参数为空，返回对象格式为：

```
{
    "content": "你好！有什么可以帮助你的吗？如果你有关于天气或者时间的问题，我特别擅长回答。",
    "refusal": null,
    "role": "assistant",
    "audio": null,
    "function_call": null,
    "tool_calls": null
}
```

> 如果 `tool_calls` 参数为空，可使程序直接返回 `content` ，无需运行以下步骤。

> 若希望每次发起 Function Calling 后大模型都可以选择指定工具，请参见 [强制工具调用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#b0910669927j7) 。

### 4\. 运行工具函数

运行工具函数将模型决策转化为实际操作。

> 运行工具函数的过程由您的计算环境而非大模型来完成。

大模型仅输出字符串格式，运行工具函数前需对工具函数名称与入参分别解析。

-   工具函数
    
    建立一个**工具函数名称**到**工具函数实体**的映射`function_mapper`，将返回的工具函数字符串映射到工具函数实体；
    
-   入参
    
    Function Calling 返回的入参为JSON字符串，使用工具将其解析为JSON对象，提取入参信息。
    

完成解析后，将参数传入工具函数并执行，获取输出结果。

python

```
# 步骤4:运行工具函数
# 请将以下代码粘贴到步骤3 代码后
import json

print("正在执行工具函数...")
# 从返回的结果中获取函数名称和入参
function_name = completion.choices[0].message.tool_calls[0].function.name
arguments_string = completion.choices[0].message.tool_calls[0].function.arguments

# 使用json模块解析参数字符串
arguments = json.loads(arguments_string)
# 创建一个函数映射表
function_mapper = {
    "get_current_weather": get_current_weather,
    "get_current_time": get_current_time
}
# 获取函数实体
function = function_mapper[function_name]
# 如果入参为空，则直接调用函数
if arguments == {}:
    function_output = function()
# 否则，传入参数后调用函数
else:
    function_output = function(arguments)
# 打印工具的输出
print(f"工具函数输出：{function_output}\n")
```

javascript

```
// 步骤4:运行工具函数
// 请将以下代码粘贴到步骤3 代码后

console.log("正在执行工具函数...");
const function_name = completion.choices[0].message.tool_calls[0].function.name;
const arguments_string = completion.choices[0].message.tool_calls[0].function.arguments;

// 使用JSON模块解析参数字符串
const args = JSON.parse(arguments_string);

// 创建一个函数映射表
const functionMapper = {
    "get_current_weather": getCurrentWeather,
    "get_current_time": getCurrentTime
};

// 获取函数实体
const func = functionMapper[function_name];

// 如果入参为空，则直接调用函数
let functionOutput;
if (Object.keys(args).length === 0) {
    functionOutput = func();
} else {
    // 否则，传入参数后调用函数
    functionOutput = func(args);
}

// 打印工具的输出
console.log(`工具函数输出：${functionOutput}\n`);
```

运行后得到如下输出：

```
上海今天是多云。
```

**说明**实际业务中，许多工具执行具体操作（如邮件发送、文件上传），而非数据查询，不会输出字符串。建议为此类工具添加状态描述信息（如“邮件发送完成”、“操作执行失败”），帮助大模型了解执行状态。

### 5\. 大模型总结工具函数输出

工具函数的输出格式较为固定，直接返回用户可能语气生硬。将工具输出提交到模型上下文并再次调用模型，可生成自然语言风格的回复。

1.  添加 Assistant Message
    
    [发起 Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#9f478b2e76wrk)后，通过`completion.choices[0].message`得到 Assistant Message，首先将它添加到 messages 数组中；
    
2.  添加 Tool Message
    
    将工具的输出通过`{"role": "tool", "content": "工具的输出","tool_call_id": completion.choices[0].message.tool_calls[0].id}`形式添加到 messages 数组。
    
    **说明**
    
    -   请确保工具的输出为字符串格式。
    -   `tool_call_id` 是系统为每一次的工具调用请求生成的**唯一标识符**。模型可能一次性要求调用多个工具，将多个工具结果返回给模型时，`tool_call_id`可确保工具的输出结果能够与它的调用意图对应。
    

python

```
# 步骤5.1:向大模型提交工具输出
# 请将以下代码粘贴到步骤4 代码后

messages.append(completion.choices[0].message)
print("已添加assistant message")
messages.append({"role": "tool", "content": function_output, "tool_call_id": completion.choices[0].message.tool_calls[0].id})
print("已添加tool message\n")
```

javascript

```
// 步骤5.1:向大模型提交工具输出
// 请将以下代码粘贴到步骤4 代码后

messages.push(completion.choices[0].message);
console.log("已添加 assistant message")
messages.push({
    "role": "tool",
    "content": functionOutput,
    "tool_call_id": completion.choices[0].message.tool_calls[0].id
});
console.log("已添加 tool message\n");
```

此时的 messages 数组为：

```
[
  System Message -- 指引模型调用工具的策略
  User Message -- 用户的问题
  Assistant Message -- 模型返回的工具调用信息
  Tool Message -- 工具的输出信息（如果采用下文介绍的并行工具调用，可能有多个 Tool Message）
]
```

更新 messages 数组后，运行以下代码。

python

```
# 步骤5.2:大模型总结工具输出
# 请将以下代码粘贴到步骤5.1 代码后
print("正在总结工具输出...")
completion = function_calling()
```

javascript

```
// 步骤5.2:大模型总结工具输出
// 请将以下代码粘贴到步骤5.1 代码后

console.log("正在总结工具输出...");
const completion_1 = await functionCalling();
```

可从`content`得到回复内容：“上海今天的天气是多云。如果您有其他问题，欢迎继续提问。”

```
{
    "content": "上海今天的天气是多云。如果您有其他问题，欢迎继续提问。",
    "refusal": null,
    "role": "assistant",
    "audio": null,
    "function_call": null,
    "tool_calls": null
}
```

至此，您已完成了一次完整的 Function Calling 流程。

## 进阶用法

### 指定工具调用方式

#### 并行工具调用

单一城市天气查询只需一次工具调用。若问题需要多次调用工具，如“北京上海的天气如何”或“杭州天气，以及现在几点了”，[发起 Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#9f478b2e76wrk) 后只会返回一个工具调用信息，以提问“北京上海的天气如何”为例：

```
{
    "content": "",
    "refusal": null,
    "role": "assistant",
    "audio": null,
    "function_call": null,
    "tool_calls": [
        {
            "id": "call_61a2bbd82a8042289f1ff2",
            "function": {
                "arguments": "{\"location\": \"北京市\"}",
                "name": "get_current_weather"
            },
            "type": "function",
            "index": 0
        }
    ]
}
```

返回结果中只有北京市的入参信息。为了解决这一问题，在[发起 Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#9f478b2e76wrk)时，可设置请求参数`parallel_tool_calls`为`true`，这样返回对象中将包含所有需要调用的工具函数与入参信息。

**说明**并行工具调用适合任务之间无依赖的情况。若任务之间有依赖关系（工具A的输入与工具B的输出结果有关），请参见[快速开始](https://help.aliyun.com/zh/model-studio/qwen-function-calling#dd5a3dca390k9)，通过while循环实现串行工具调用（一次调用一个工具）。

python

```
def function_calling():
    completion = client.chat.completions.create(
        model="qwen3.8-max",  # 此处以qwen3.8-max为例，可按需更换模型名称
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
        # 新增参数
        parallel_tool_calls=True
    )
    print("返回对象：")
    print(completion.choices[0].message.model_dump_json())
    print("\n")
    return completion

print("正在发起function calling...")
completion = function_calling()
```

javascript

```
async function functionCalling() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.8-max",  // 此处以qwen3.8-max为例，可按需更换模型名称
        enable_thinking: false,
        messages: messages,
        tools: tools,
        parallel_tool_calls: true
    });
    console.log("返回对象：");
    console.log(JSON.stringify(completion.choices[0].message));
    console.log("\n");
    return completion;
}

const completion = await functionCalling();
```

在返回对象的`tool_calls`数组中包含了北京上海的入参信息：

```
{
    "content": "",
    "role": "assistant",
    "tool_calls": [
        {
            "function": {
                "name": "get_current_weather",
                "arguments": "{\"location\": \"北京市\"}"
            },
            "index": 0,
            "id": "call_c2d8a3a24c4d4929b26ae2",
            "type": "function"
        },
        {
            "function": {
                "name": "get_current_weather",
                "arguments": "{\"location\": \"上海市\"}"
            },
            "index": 1,
            "id": "call_dc7f2f678f1944da9194cd",
            "type": "function"
        }
    ]
}
```

#### 强制工具调用

大模型生成内容具有不确定性，可能选择错误的工具。如需对某类问题强制使用或禁用特定工具，可修改`tool_choice`参数。`tool_choice`参数的默认值为`"auto"`，表示由大模型自主判断如何进行工具调用。

> 大模型总结工具函数输出时，请将 `tool_choice` 参数去除，否则API仍会返回工具调用信息。

-   **强制使用某个工具**
    
    如果您希望对于某一类问题，Function Calling 能强制调用某个工具，可设定`tool_choice`参数为`{"type": "function", "function": {"name": "the_function_to_call"}}`，大模型将不参与工具的选择，只输出入参信息。
    
    假设当前场景中只包含天气查询的问题，可修改 function\_calling 代码为：
    

```
def function_calling():
    completion = client.chat.completions.create(
        model="qwen3.8-max",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "get_current_weather"}}
    )
    print(completion.model_dump_json())

function_calling()
```
```
async function functionCalling() {
    const response = await openai.chat.completions.create({
        model: "qwen3.8-max",
        enable_thinking: false,
        messages: messages,
        tools: tools,
        tool_choice: {"type": "function", "function": {"name": "get_current_weather"}}
    });
    console.log("返回对象：");
    console.log(JSON.stringify(response.choices[0].message));
    console.log("\n");
    return response;
}

const response = await functionCalling();
```

无论输入什么问题，返回对象的工具函数都会是`get_current_weather`。

> 使用该策略前请确保问题与选择的工具相关，否则可能返回不符合预期的结果。

**强制使用至少一个工具**

某些需要使用工具的问题，大模型可能判断为无需调用。如需强制 Function Calling 始终进行工具调用（返回对象中`tool_calls`参数不为空），可以设定`tool_choice`参数为`"required"`，Function Calling 将始终返回工具与入参信息。

> Qwen 系列模型暂不支持将`tool_choice`设为`"required"`：非思考模式下`required`无法保证一定调用工具，思考模式下当前不支持`"required"`。

假设当前场景中的问题均需要调用工具，您可以修改 function\_calling 代码为：

python

```
def function_calling():
    completion = client.chat.completions.create(
        model="kimi/kimi-k3",
        messages=messages,
        tools=tools,
        tool_choice="required"
    )
    print(completion.model_dump_json())

function_calling()
```

javascript

```
async function functionCalling() {
    const completion = await openai.chat.completions.create({
        model: "kimi/kimi-k3",
        messages: messages,
        tools: tools,
        tool_choice: "required"
    });
    console.log("返回对象：");
    console.log(JSON.stringify(completion.choices[0].message));
    console.log("\n");
    return completion;
}

const completion = await functionCalling();
```

无论输入什么问题，返回对象的`tool_calls`参数将始终不为空。

> 使用该策略前请确保问题与工具相关，否则可能返回不符合预期的结果。

-   **强制不使用工具**
    
    如需 Function Calling 始终不进行工具调用（返回对象中包含回复内容`content`而`tool_calls`参数为空），可设定`tool_choice`参数为`"none"`，或不传入`tools`参数，Function Calling 返回的`tool_calls`参数将始终为空。
    
    假设当前场景中的问题均无需调用工具，可修改 function\_calling 代码为：
    

```
def function_calling():
    completion = client.chat.completions.create(
        model="qwen3.8-max",
        extra_body={"enable_thinking": False},
        messages=messages,
        tools=tools,
        tool_choice="none"
    )
    print(completion.model_dump_json())

function_calling()
```
```
async function functionCalling() {
    const completion = await openai.chat.completions.create({
        model: "qwen3.8-max",
        enable_thinking: false,
        messages: messages,
        tools: tools,
        tool_choice: "none"
    });
    console.log("返回对象：");
    console.log(JSON.stringify(completion.choices[0].message));
    console.log("\n");
    return completion;
}

const completion = await functionCalling();
```

### 多轮对话

用户可能第一轮提问“北京天气”，第二轮提问“上海的呢？”。若模型上下文缺少第一轮信息，模型无法判断调用哪个工具。多轮对话场景中，每轮结束后保持 messages 数组完整，在此基础上添加 User Message 并[发起 Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling#9f478b2e76wrk)以及后续步骤。messages 结构如下所示：

```
[
  System Message -- 指引模型调用工具的策略
  User Message -- 用户的问题
  Assistant Message -- 模型返回的工具调用信息
  Tool Message -- 工具的输出信息
  Assistant Message -- 模型总结的工具调用信息
  User Message -- 用户第二轮的问题
]
```

### 流式输出

使用流式输出可实时获取工具函数名称与入参信息，提升用户体验。其中：

-   工具调用的参数信息：以数据流的形式分块返回。
-   工具函数名称：在流式响应的第一个数据块中返回。

python

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
]

stream = client.chat.completions.create(
    model="qwen3.8-max",
    extra_body={"enable_thinking": False},
    messages=[{"role": "user", "content": "杭州天气?"}],
    tools=tools,
    stream=True
)

for chunk in stream:
    delta = chunk.choices[0].delta
    print(delta.tool_calls)
```

javascript

```
import { OpenAI } from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
const tools = [
    {
        "type": "function",
        "function": {
            "name": "getCurrentWeather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
];

const stream = await openai.chat.completions.create({
    model: "qwen3.8-max",
    enable_thinking: false,
    messages: [{ role: "user", content: "北京天气" }],
    tools: tools,
    stream: true,
});

for await (const chunk of stream) {
    const delta = chunk.choices[0].delta;
    console.log(delta.tool_calls);
}
```

运行后得到如下输出：

```
[ChoiceDeltaToolCall(index=0, id='call_8f08d2b0fc0c4d8fab7123', function=ChoiceDeltaToolCallFunction(arguments='{"location":', name='get_current_weather'), type='function')]
[ChoiceDeltaToolCall(index=0, id='', function=ChoiceDeltaToolCallFunction(arguments=' "杭州"}', name=None), type='function')]
None
```

运行以下代码拼接入参信息（`arguments`）：

python

```
tool_calls = {}
for response_chunk in stream:
    delta_tool_calls = response_chunk.choices[0].delta.tool_calls
    if delta_tool_calls:
        for tool_call_chunk in delta_tool_calls:
            call_index = tool_call_chunk.index
            tool_call_chunk.function.arguments = tool_call_chunk.function.arguments or ""
            if call_index not in tool_calls:
                tool_calls[call_index] = tool_call_chunk
            else:
                tool_calls[call_index].function.arguments += tool_call_chunk.function.arguments
print(tool_calls[0].model_dump_json())
```

javascript

```
const toolCalls = {};
for await (const responseChunk of stream) {
  const deltaToolCalls = responseChunk.choices[0]?.delta?.tool_calls;
  if (deltaToolCalls) {
    for (const toolCallChunk of deltaToolCalls) {
      const index = toolCallChunk.index;
      toolCallChunk.function.arguments = toolCallChunk.function.arguments || "";
      if (!toolCalls[index]) {
        toolCalls[index] = { ...toolCallChunk };
        if (!toolCalls[index].function) {
            toolCalls[index].function = { name: '', arguments: '' };
        }
      }
      else if (toolCallChunk.function?.arguments) {
        toolCalls[index].function.arguments += toolCallChunk.function.arguments;
      }
    }
  }
}
console.log(JSON.stringify(toolCalls[0]));
```

获得如下输出：

```
{"index":0,"id":"call_16c72bef988a4c6c8cc662","function":{"arguments":"{\"location\": \"杭州\"}","name":"get_current_weather"},"type":"function"}
```

在使用大模型总结工具函数输出步骤，添加的 Assistant Message 需要符合下方格式。仅需将下方的`tool_calls`中的元素替换为以上内容即可。

```
{
    "content": "",
    "refusal": None,
    "role": "assistant",
    "audio": None,
    "function_call": None,
    "tool_calls": [
        {
            "id": "call_xxx",
            "function": {
                "arguments": '{"location": "xx"}',
                "name": "get_current_weather",
            },
            "type": "function",
            "index": 0,
        }
    ],
}
```

### Responses API的工具调用

上述示例基于 OpenAI Chat Completions 和 DashScope API。若使用 OpenAI Responses API，整体流程相同，但接口格式有以下区别：

**维度**

**Chat Completions**

**Responses API**

工具定义格式

```
{
    "type": "function",
    "function": {
        "name":...,
        "parameters":...
    }
}
```

```
{
    "type": "function",
    "name":...,
    "parameters":...
}
```

工具调用输出

response.choices\[0\].message.tool\_calls

response.output 中 type 为 function\_call 的项

工具结果回传

```
{
    "role": "tool",
    "tool_call_id":...,
    "content":...
}
```

```
{
    "type": "function_call_output",
    "call_id":...,
    "output":...
}
```

最终回复

response.choices\[0\].message.content

response.output\_text

python

```
from openai import OpenAI
import json
import os
import random

# 初始化客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
# 模拟用户问题
USER_QUESTION = "北京天气咋样"
# 定义工具列表
tools = [
    {
        "type": "function",
        "name": "get_current_weather",
        "description": "当你想查询指定城市的天气时非常有用。",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
            },
            "required": ["location"],
        },
    }
]

# 模拟天气查询工具
def get_current_weather(arguments):
    weather_conditions = ["晴天", "多云", "雨天"]
    random_weather = random.choice(weather_conditions)
    location = arguments["location"]
    return f"{location}今天是{random_weather}。"

# 封装模型响应函数
def get_response(input_data):
    response = client.responses.create(
        model="qwen3.8-max",
        extra_body={"enable_thinking": False},
        input=input_data,
        tools=tools,
    )
    return response

# 维护对话上下文
conversation = [{"role": "user", "content": USER_QUESTION}]

response = get_response(conversation)
function_calls = [item for item in response.output if item.type == "function_call"]
# 如果不需要调用工具，直接输出内容
if not function_calls:
    print(f"助手最终回复：{response.output_text}")
else:
    # 进入工具调用循环
    while function_calls:
        for fc in function_calls:
            func_name = fc.name
            arguments = json.loads(fc.arguments)
            print(f"正在调用工具 [{func_name}]，参数：{arguments}")
            # 执行工具
            tool_result = get_current_weather(arguments)
            print(f"工具返回：{tool_result}")
            # 将工具调用和结果成对追加到上下文中
            conversation.append(
                {
                    "type": "function_call",
                    "name": fc.name,
                    "arguments": fc.arguments,
                    "call_id": fc.call_id,
                }
            )
            conversation.append(
                {
                    "type": "function_call_output",
                    "call_id": fc.call_id,
                    "output": tool_result,
                }
            )
        # 携带完整上下文再次调用模型
        response = get_response(conversation)
        function_calls = [
            item for item in response.output if item.type == "function_call"
        ]
    print(f"助手最终回复：{response.output_text}")
```

javascript

```
import OpenAI from "openai";

// 初始化客户端
const openai = new OpenAI({
  // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
  // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL:
    "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

// 定义工具列表
const tools = [
  {
    type: "function",
    name: "get_current_weather",
    description: "当你想查询指定城市的天气时非常有用。",
    parameters: {
      type: "object",
      properties: {
        location: {
          type: "string",
          description: "城市或县区，比如北京市、杭州市、余杭区等。",
        },
      },
      required: ["location"],
    },
  },
];

// 模拟天气查询工具
const getCurrentWeather = (args) => {
  const weatherConditions = ["晴天", "多云", "雨天"];
  const randomWeather =
    weatherConditions[Math.floor(Math.random() * weatherConditions.length)];
  const location = args.location;
  return `${location}今天是${randomWeather}。`;
};

// 封装模型响应函数
const getResponse = async (inputData) => {
  const response = await openai.responses.create({
    model: "qwen3.8-max",
    enable_thinking: false,
    input: inputData,
    tools: tools,
  });
  return response;
};

const main = async () => {
  const userQuestion = "北京天气";

  // 维护对话上下文
  const conversation = [{ role: "user", content: userQuestion }];

  let response = await getResponse(conversation);
  let functionCalls = response.output.filter(
    (item) => item.type === "function_call"
  );
  // 如果不需要调用工具，直接输出内容
  if (functionCalls.length === 0) {
    console.log(`助手最终回复：${response.output_text}`);
  } else {
    // 进入工具调用循环
    while (functionCalls.length > 0) {
      for (const fc of functionCalls) {
        const funcName = fc.name;
        const args = JSON.parse(fc.arguments);
        console.log(`正在调用工具 [${funcName}]，参数：`, args);
        // 执行工具
        const toolResult = getCurrentWeather(args);
        console.log(`工具返回：${toolResult}`);
        // 将工具调用和结果成对追加到上下文中
        conversation.push({
          type: "function_call",
          name: fc.name,
          arguments: fc.arguments,
          call_id: fc.call_id,
        });
        conversation.push({
          type: "function_call_output",
          call_id: fc.call_id,
          output: toolResult,
        });
      }
      // 携带完整上下文再次调用模型
      response = await getResponse(conversation);
      functionCalls = response.output.filter(
        (item) => item.type === "function_call"
      );
    }
    console.log(`助手最终回复：${response.output_text}`);
  }
};

// 启动程序
main().catch(console.error);
```

### 全模态模型的工具调用

全模态模型支持工具调用，Qwen-Omni 系列和 Qwen-Omni-Realtime 系列的调用方式不同。

#### Qwen-Omni 系列

文本工具调用使用 `qwen3.8-omni-flash`，可通过 Chat Completions 或 Responses 接入。以下 Python 和 JavaScript 示例使用 Chat Completions，关闭思考并流式读取文本和工具调用增量。音视频输入见 [Qwen3.8-Omni-Flash](https://help.aliyun.com/zh/model-studio/qwen-omni#qwen38-offline)。

示例设置 `reasoning_effort="none"` 关闭思考。需要结合思考进行工具调用时，可省略该参数，使用默认的 `xhigh`，并分别读取 `reasoning_content`、`content` 和 `tool_calls`。此时多轮请求需将上一轮 assistant 消息的思考内容、回复和工具调用一起加入历史，再传入工具结果；`preserve_thinking` 默认开启。详见[传递思考过程](https://help.aliyun.com/zh/model-studio/deep-thinking#jln7docdq5et5)。

先[安装 OpenAI SDK](raw/model-api-reference/preparations/install-sdk.md)，配置 `DASHSCOPE_API_KEY`，并将 `DASHSCOPE_BASE_URL` 设置为业务空间的 [Chat Completions 地址](raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。API Key 与地址使用同一地域。

python

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),

    base_url=os.environ["DASHSCOPE_BASE_URL"],
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
]

completion = client.chat.completions.create(
    model="qwen3.8-omni-flash",
    reasoning_effort="none",
    messages=[{"role": "user", "content": "杭州天气?"}],
    stream=True,
    tools=tools
)

for chunk in completion:
    if not chunk.choices:
        continue
    delta = chunk.choices[0].delta
    if delta.content:
        print("Text:", delta.content)
    if delta.tool_calls:
        print(delta.tool_calls)
```

javascript

```
import { OpenAI } from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,

        baseURL: process.env.DASHSCOPE_BASE_URL
    }
);

const tools = [
    {
        "type": "function",
        "function": {
            "name": "getCurrentWeather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
];

const stream = await openai.chat.completions.create({
    model: "qwen3.8-omni-flash",
    reasoning_effort: "none",
    messages: [
        {
            "role": "user",
            "content": "杭州天气"
        }],
    stream: true,
    tools:tools
});

for await (const chunk of stream) {
    const delta = chunk.choices?.[0]?.delta;
    if (!delta) continue;
    if (delta.content) console.log("Text:", delta.content);
    if (delta.tool_calls) console.log(delta.tool_calls);
}
```

Python 工具调用增量格式示意如下；实际内容由模型返回，函数名和参数可能分多个数据块到达：

```
[ChoiceDeltaToolCall(index=0, id='call_391c8e5787bc4972a388aa', function=ChoiceDeltaToolCallFunction(arguments=None, name='get_current_weather'), type='function')]
[ChoiceDeltaToolCall(index=0, id='call_391c8e5787bc4972a388aa', function=ChoiceDeltaToolCallFunction(arguments=' {"location": "杭州市"}', name=None), type='function')]
```

拼接入参信息（`arguments`）的代码请参见[流式输出](https://help.aliyun.com/zh/model-studio/qwen-function-calling#953d0d7b1ahuk)。

> Qwen3.5-Omni-Plus、Qwen3.5-Omni-Flash 和 Qwen3-Omni-Flash 的既有调用必须设置 `stream=True`。获取工具信息时可使用 `modalities=["text"]`；Qwen3.5-Omni 同时输出音频时需跳过音频数据块。

#### Qwen-Omni-Realtime 系列

Qwen3.8-Omni-Flash-Realtime、Qwen3.5-Omni-Plus-Realtime 和 Qwen3.5-Omni-Flash-Realtime 支持自定义 Function Calling，适用于语音对话场景。以下流程通过 DashScope SDK 或 WebSocket 原生协议调用，接入方式与 SDK 配置见[实时调用指南](raw/model-user-guide/model-experience/omni-modal/realtime.md)。

Qwen3.8-Omni-Flash-Realtime 的服务端 MCP 工具调用与审批流程见[MCP 交互流程](https://help.aliyun.com/zh/model-studio/omni-realtime-interaction-process#qwen38-mcp-flow)。

**工作流程**：

建立 WebSocket 连接后，通过 `session.update` 传入工具定义，即可进入以下交互流程：

**阶段一：语音输入与工具调用**

1.  用户发起语音提问，客户端采集音频并发送至服务端（对应 `append_audio()` 方法），服务端 VAD 检测语音结束后进行模型推理，判断需要调用工具。
2.  服务端将工具调用信息返回给客户端（对应 `response.function_call_arguments.done` 事件），包含函数名（`name`）、函数入参（`arguments`）和调用标识（`call_id`），示例如下：

```
{
    "type": "response.function_call_arguments.done",
    "response_id": "resp_JnTOsWXlFhKcFohZbtfz6",
    "item_id": "item_Rhcms7CauTNsQprV5S4Hr",
    "output_index": 0,
    "name": "get_current_weather",
    "call_id": "call_2be200f4cafe419b9530dd",
    "arguments": "{\"location\": \"杭州\"}"
}
```

3.  客户端根据函数名和入参，在本地执行对应的工具函数，获得执行结果。

**阶段二：客户端回传工具结果并触发最终响应**

1.  客户端将工具执行结果发回服务端（对应 `conversation.item.create` 事件），包含调用标识（`call_id`）和执行结果（`output`），示例如下：

```
{
    "type": "conversation.item.create",
    "item": {
        "type": "function_call_output",
        "call_id": "call_2be200f4cafe419b9530dd",
        "output": "杭州今天天气为晴，气温25℃，微风"
    }
}
```

2.  客户端继续发送 `response.create` 事件，触发服务端基于工具执行结果生成最终语音回答。
3.  客户端接收服务端返回的语音和文本（对应 `response.audio.delta` 和 `response.audio_transcript.delta` 事件），播放语音回复给用户。

> Qwen-Omni-Realtime 系列不支持 `tool_choice` 和 `parallel_tool_calls` 参数。

> 千问Omni-Realtime详情请参见： 实时（Qwen-Omni-Realtime） 、 客户端事件 、 服务端事件 。

DashScope Python SDK

```
# DashScope Python SDK v1.25.17
import os
import uuid
import threading
import traceback
import json
import base64
import signal
import sys
import time
from typing import Dict, Any, Optional, List
import pyaudio
import queue
import contextlib
import dashscope
from dashscope.audio.qwen_omni import *

# ==================== 常量定义 ====================
VOICE = 'Tina'
MODEL = "qwen3.5-omni-plus-realtime"
# 如果需要访问新加坡地域，请WS_URL将替换为：wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime
WS_URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime"
# 配置 API Key，若没有设置环境变量，请用 API Key 将下行替换为 dashscope.api_key = "sk-xxx"
dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHUNK_SIZE = 3200
OUTPUT_AUDIO_SAMPLE_RATE = 24000

# ==================== 工具定义 ====================
def get_train_price(src: str, dst: str) -> str:
    """查询火车票价格"""
    return f"{src}到{dst}的火车票价格为100~200元。"

def get_flight_price(src: str, dst: str) -> str:
    """查询飞机票价格"""
    return f"{src}到{dst}的机票价格为200~300美元。"

def get_current_weather(location: str) -> str:
    """查询指定城市天气"""
    return f"{location}今天天气为霾转晴，气温4/-4℃，微风"

# 统一的 OpenAI 格式工具定义
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_flight_price",
            "description": "当你想查询飞机票价格时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "src": {
                        "type": "string",
                        "description": "飞机起飞的城市，比如北京市、杭州市等。",
                    },
                    "dst": {
                        "type": "string",
                        "description": "飞机降落的城市，比如北京市、杭州市区等。",
                    },
                },
                "required": ["src", "dst"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_train_price",
            "description": "当你想查询火车票价格时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "src": {
                        "type": "string",
                        "description": "火车出发的城市，比如北京市、杭州市等。",
                    },
                    "dst": {
                        "type": "string",
                        "description": "火车到达的城市，比如北京市、杭州市区等。",
                    },
                },
                "required": ["src", "dst"],
            },
        },
    },
]

# 工具名称到函数的映射
TOOL_FUNCTIONS = {
    "get_current_weather": get_current_weather,
    "get_flight_price": get_flight_price,
    "get_train_price": get_train_price,
}

# ==================== 工具调用处理 ====================
def handle_tool_call(tool_call_response: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理工具调用请求

    Args:
        tool_call_response: 包含 name, arguments, call_id 的工具调用信息

    Returns:
        更新后的工具调用响应，包含 output 字段
    """
    try:
        function_name = tool_call_response['name']
        tool_call_arguments = json.loads(tool_call_response['arguments'])

        print(f'[Tool Call] 开始处理: name={function_name}, args={tool_call_arguments}')

        # 查找对应的函数
        if function_name not in TOOL_FUNCTIONS:
            tool_call_response['output'] = f"客户端未找到工具: {function_name}"
            print(f'[Tool Call] 错误: 未找到工具 {function_name}')
            return tool_call_response

        # 调用函数
        func = TOOL_FUNCTIONS[function_name]
        result = func(**tool_call_arguments)
        tool_call_response['output'] = result

        print(f'[Tool Call] 完成: {result}')
        return tool_call_response

    except Exception as e:
        error_msg = f"工具调用失败: {str(e)}"
        tool_call_response['output'] = error_msg
        print(f'[Tool Call] 异常: {error_msg}')
        traceback.print_exc()
        return tool_call_response

def send_tool_call_response(conversation: OmniRealtimeConversation, response: Dict[str, Any]) -> None:
    """发送工具调用结果到服务端"""
    conversation.create_item({
        "id": 'item_' + uuid.uuid4().hex,
        "type": "function_call_output",
        "call_id": response['call_id'],
        "output": response["output"],
    })

# ==================== PCM 音频播放器 ====================
class PCMPlayer:
    """
    PCM 音频播放器

    使用双线程架构实现实时音频播放：
    - 解码线程：将 base64 编码的音频数据解码为原始 PCM 数据
    - 播放线程：将 PCM 数据写入音频输出设备

    支持动态添加音频数据、取消播放、保存音频文件等功能。
    """

    def __init__(self, pya: pyaudio.PyAudio, sample_rate=24000, chunk_size_ms=100, save_file=False):
        """
        初始化 PCM 播放器

        Args:
            pya: pyaudio.PyAudio 实例
            sample_rate: 音频采样率（Hz），默认 24000
            chunk_size_ms: 音频块大小（毫秒），影响取消播放的延迟，默认 100ms
            save_file: 是否保存播放的音频到文件（result.pcm），默认 False
        """

        self.pya = pya
        self.sample_rate = sample_rate
        self.chunk_size_bytes = chunk_size_ms * sample_rate * 2 // 1000
        self.player_stream = pya.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=sample_rate,
                                       output=True)

        self.raw_audio_buffer: queue.Queue = queue.Queue()
        self.b64_audio_buffer: queue.Queue = queue.Queue()
        self.status_lock = threading.Lock()
        self.status = 'playing'
        self.decoder_thread = threading.Thread(target=self.decoder_loop)
        self.player_thread = threading.Thread(target=self.player_loop)
        self.decoder_thread.start()
        self.player_thread.start()
        self.complete_event: threading.Event = None
        self.save_file = save_file
        if self.save_file:
            self.out_file = open('result.pcm', 'wb')

    def decoder_loop(self):
        """解码线程：将 base64 音频数据解码为 PCM 原始数据"""
        while self.status != 'stop':
            recv_audio_b64 = None
            with contextlib.suppress(queue.Empty):
                recv_audio_b64 = self.b64_audio_buffer.get(timeout=0.1)
            if recv_audio_b64 is None:
                continue
            recv_audio_raw = base64.b64decode(recv_audio_b64)
            # push raw audio data into queue by chunk
            for i in range(0, len(recv_audio_raw), self.chunk_size_bytes):
                chunk = recv_audio_raw[i:i + self.chunk_size_bytes]
                self.raw_audio_buffer.put(chunk)
                if self.save_file:
                    self.out_file.write(chunk)

    def player_loop(self):
        """播放线程：将 PCM 数据写入音频输出设备"""
        while self.status != 'stop':
            recv_audio_raw = None
            with contextlib.suppress(queue.Empty):
                recv_audio_raw = self.raw_audio_buffer.get(timeout=0.1)
            if recv_audio_raw is None:
                if self.complete_event:
                    self.complete_event.set()
                continue
            # write chunk to pyaudio audio player, wait until finish playing this chunk.
            self.player_stream.write(recv_audio_raw)

    def cancel_playing(self):
        """取消播放：清空所有缓冲队列"""
        self.b64_audio_buffer.queue.clear()
        self.raw_audio_buffer.queue.clear()

    def add_data(self, data):
        """添加 base64 编码的音频数据到播放队列"""
        self.b64_audio_buffer.put(data)

    def wait_for_complete(self):
        """等待播放完成"""
        self.complete_event = threading.Event()
        self.complete_event.wait()
        self.complete_event = None

    def shutdown(self):
        """关闭播放器并释放资源"""
        self.status = 'stop'
        self.decoder_thread.join()
        self.player_thread.join()
        self.player_stream.close()
        if self.save_file:
            self.out_file.close()

# ==================== 音频管理器 ====================
class AudioManager:
    """管理音频输入输出资源"""

    def __init__(self):
        self.pya: Optional[pyaudio.PyAudio] = None
        self.mic_stream: Optional[pyaudio.Stream] = None
        self.player: Optional[PCMPlayer] = None

    def initialize(self) -> None:
        """初始化音频设备"""
        print('初始化音频设备...')
        self.pya = pyaudio.PyAudio()
        self.mic_stream = self.pya.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=AUDIO_SAMPLE_RATE,
            input=True
        )
        self.player = PCMPlayer(self.pya, sample_rate=OUTPUT_AUDIO_SAMPLE_RATE)
        print('音频设备初始化完成')

    def read_audio_chunk(self) -> Optional[bytes]:
        """读取音频数据块"""
        if not self.mic_stream:
            return None
        try:
            return self.mic_stream.read(AUDIO_CHUNK_SIZE, exception_on_overflow=False)
        except Exception as e:
            print(f'[Error] 读取音频数据失败: {e}')
            return None

    def cleanup(self) -> None:
        """清理音频资源"""
        print('清理音频资源...')
        if self.player:
            self.player.shutdown()
        if self.mic_stream:
            self.mic_stream.close()
        if self.pya:
            self.pya.terminate()
        print('音频资源清理完成')

# ==================== 回调处理器 ====================
class OmniCallback(OmniRealtimeCallback):
    """Omni 实时对话回调处理器"""

    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager
        self.tool_calls: Dict[str, Dict[str, Any]] = {}
        self.all_response_text: str = ''
        self.last_package_time: float = 0
        self.is_first_text: bool = True
        self.is_first_audio: bool = True
        self.conversation: Optional[OmniRealtimeConversation] = None

    def set_conversation(self, conversation: OmniRealtimeConversation) -> None:
        """设置对话实例引用"""
        self.conversation = conversation

    def on_open(self) -> None:
        """连接建立时的回调"""
        print('连接已建立')
        self.audio_manager.initialize()
        self.last_package_time = time.time() * 1000
        self.is_first_text = True
        self.is_first_audio = True
        self.tool_calls = {}
        self.all_response_text = ''

    def on_close(self, close_status_code: int, close_msg: str) -> None:
        """连接关闭时的回调"""
        print(f'连接已关闭: code={close_status_code}, msg={close_msg}')
        self.audio_manager.cleanup()
        sys.exit(0)

    def on_event(self, response: Dict[str, Any]) -> None:
        """处理事件回调"""
        try:
            event_type = response.get('type', '')

            # 会话创建
            if event_type == 'session.created':
                print(f'会话已启动: {response["session"]["id"]}')

            # 语音转文本完成
            elif event_type == 'conversation.item.input_audio_transcription.completed':
                print(f'用户问题: {response.get("transcript", "")}')

            # 文本增量响应
            elif event_type in ('response.audio_transcript.delta', 'response.text.delta'):
                if self.is_first_text:
                    self.is_first_text = False
                    latency = time.time() * 1000 - self.last_package_time
                    print(f'首字延迟 (VAD结束): {latency:.0f} ms')

                text = response.get('delta', '')
                self.all_response_text += text

            # 音频增量响应
            elif event_type == 'response.audio.delta':
                if self.is_first_audio:
                    self.is_first_audio = False
                    latency = time.time() * 1000 - self.last_package_time
                    print(f'首音延迟 (VAD结束): {latency:.0f} ms')

                audio_interval = time.time() * 1000 - self.last_package_time
                print(f'音频间隔: {audio_interval:.0f} ms')
                self.last_package_time = time.time() * 1000

                recv_audio_b64 = response.get('delta', '')
                if self.audio_manager.player:
                    self.audio_manager.player.add_data(recv_audio_b64)

            # VAD 检测到语音开始
            elif event_type == 'input_audio_buffer.speech_started':
                print('====== VAD 检测到语音开始 ======')
                if self.audio_manager.player:
                    self.audio_manager.player.cancel_playing()

            # VAD 检测到语音结束
            elif event_type == 'input_audio_buffer.speech_stopped':
                print('====== VAD 检测到语音结束 ======')
                self.last_package_time = time.time() * 1000
                self.is_first_text = True
                self.is_first_audio = True
                self.tool_calls = {}

            # 函数调用参数完成
            elif event_type == 'response.function_call_arguments.done':
                print('====== 收到工具调用请求 ======')
                call_id = response.get('call_id', '')
                self.tool_calls[call_id] = response.copy()
                self.tool_calls[call_id]['processed'] = False

            # 响应完成
            elif event_type == 'response.done':
                print('====== 响应完成 ======')
                print(f'完整回复: {self.all_response_text}')

                if self.conversation:
                    response_id = self.conversation.get_last_response_id()
                    text_delay = self.conversation.get_last_first_text_delay()
                    audio_delay = self.conversation.get_last_first_audio_delay()

                    # 只有当所有指标都可用时才打印详细指标
                    if response_id is not None and text_delay is not None and audio_delay is not None:
                        print(f'[Metric] 响应ID: {response_id}, '
                              f'首字延迟: {text_delay:.0f}ms, '
                              f'首音延迟: {audio_delay:.0f}ms')
                    else:
                        print('[Metric] 指标信息暂不可用（可能是工具调用后的响应）')

                self.all_response_text = ''

        except Exception as e:
            print(f'[Error] 处理事件异常: {e}')
            traceback.print_exc()

    def process_pending_tool_calls(self) -> bool:
        """
        处理待处理的工具调用

        Returns:
            是否有新的工具调用需要响应
        """
        has_pending = False

        for call_id, tool_call in self.tool_calls.items():
            if not tool_call.get('processed', False):
                has_pending = True
                tool_call['processed'] = True

                # 处理工具调用
                result = handle_tool_call(tool_call)

                # 发送结果到服务端
                if self.conversation:
                    send_tool_call_response(self.conversation, result)

        return has_pending

# ==================== 主程序 ====================
def main():
    """主函数"""
    print('正在初始化 Omni 实时对话...')

    # 创建音频管理器
    audio_manager = AudioManager()

    # 创建回调处理器
    callback = OmniCallback(audio_manager)

    # 创建对话实例
    conversation = OmniRealtimeConversation(
        api_key=dashscope.api_key,
        url=WS_URL,
        model=MODEL,
        callback=callback,
    )

    # 设置回调中的对话引用
    callback.set_conversation(conversation)

    # 建立连接
    conversation.connect()

    # 配置会话参数
    omni_output_modalities = [MultiModality.AUDIO, MultiModality.TEXT]

    conversation.update_session(
        output_modalities=omni_output_modalities,
        voice=VOICE,
        input_audio_format=AudioFormat.PCM_16000HZ_MONO_16BIT,
        output_audio_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
        enable_input_audio_transcription=True,
        enable_turn_detection=True,
        turn_detection_type='server_vad',
        tools=TOOLS,
    )

    # 设置信号处理
    def signal_handler(sig, frame):
        print('\n接收到 Ctrl+C，正在停止...')
        conversation.close()
        audio_manager.cleanup()
        print('Omni 实时对话已停止')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    print("按 Ctrl+C 停止对话...\n")

    # 主循环：持续发送音频并检查工具调用
    try:
        while True:
            # 处理待处理的工具调用
            has_tool_calls = callback.process_pending_tool_calls()

            if has_tool_calls:
                print("*** 工具调用完成，创建新响应 ***")
                conversation.create_response(
                    instructions=None,
                    output_modalities=omni_output_modalities
                )
                print('====== 工具调用处理完成 ======\n')

            # 读取并发送音频数据
            audio_data = audio_manager.read_audio_chunk()
            if audio_data:
                audio_b64 = base64.b64encode(audio_data).decode('ascii')
                conversation.append_audio(audio_b64)
            else:
                break

    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f'[Error] 主循环异常: {e}')
        traceback.print_exc()
    finally:
        conversation.close()
        audio_manager.cleanup()

if __name__ == '__main__':
    main()
```

DashScope Java SDK

```
// DashScope Java SDK v2.22.15
import com.alibaba.dashscope.audio.omni.*;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import javax.sound.sampled.*;
import java.nio.ByteBuffer;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Function;

public class Main {

    public static void main(String[] args) {
        try {
            // 初始化组件
            AudioPlayer audioPlayer = new AudioPlayer();
            ToolRegistry toolRegistry = new ToolRegistry();
            ConversationHandler handler = new ConversationHandler(audioPlayer, toolRegistry);

            // 创建并配置会话
            OmniRealtimeParam param = OmniRealtimeParam.builder()
                    .model("qwen3.5-omni-plus-realtime")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    // 如果需要访问新加坡地域，请url将替换为：wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime
                    .url("wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime")
                    .build();

            OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, handler);
            conversation.connect();

            // 配置会话参数
            configureSession(conversation, toolRegistry);

            // 启动音频采集
            startAudioCapture(conversation, handler);

            // 清理资源
            cleanup(conversation, audioPlayer);

        } catch (NoApiKeyException e) {
            System.err.println("未找到API KEY: 请设置环境变量 DASHSCOPE_API_KEY");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void configureSession(OmniRealtimeConversation conversation, ToolRegistry toolRegistry) {
        HashMap<String, Object> additionalConfig = new HashMap<>();
        additionalConfig.put("tools", toolRegistry.buildToolsDefinition());

        conversation.updateSession(OmniRealtimeConfig.builder()
                .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
                .voice("Tina")
                .enableTurnDetection(true)
                .enableInputAudioTranscription(true)
                .parameters(additionalConfig)
                .build());

        System.out.println("工具调用已开启，请开始说话（按Ctrl+C退出）...");
    }

    private static void startAudioCapture(OmniRealtimeConversation conversation, ConversationHandler handler)
            throws LineUnavailableException {
        AudioFormat format = new AudioFormat(16000, 16, 1, true, false);
        TargetDataLine mic = AudioSystem.getTargetDataLine(format);
        mic.open(format);
        mic.start();

        ByteBuffer buffer = ByteBuffer.allocate(3200);
        while (!handler.getShouldStop().get()) {
            int bytesRead = mic.read(buffer.array(), 0, buffer.capacity());
            if (bytesRead > 0) {
                conversation.appendAudio(Base64.getEncoder().encodeToString(buffer.array()));

                // 检查并处理待处理的工具调用
                if (handler.hasPendingToolCalls()) {
                    System.out.println("*** create response after call tools");
                    handler.processPendingToolCalls(conversation);
                    conversation.createResponse(null, Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT));
                    System.out.println("======TOOL CALL END======");
                }
            }
            try {
                Thread.sleep(20);
            } catch (InterruptedException ignored) {}
        }

        mic.close();
    }

    private static void cleanup(OmniRealtimeConversation conversation, AudioPlayer audioPlayer) {
        try {
            conversation.close(1000, "正常结束");
            audioPlayer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 音频播放器 - 负责音频数据的顺序播放
     */
    static class AudioPlayer {
        private final SourceDataLine line;
        private final Queue<byte[]> audioQueue = new ConcurrentLinkedQueue<>();
        private final Thread playerThread;
        private final AtomicBoolean shouldStop = new AtomicBoolean(false);

        public AudioPlayer() throws LineUnavailableException {
            AudioFormat format = new AudioFormat(24000, 16, 1, true, false);
            line = AudioSystem.getSourceDataLine(format);
            line.open(format);
            line.start();

            playerThread = new Thread(this::playLoop, "AudioPlayer");
            playerThread.start();
        }

        private void playLoop() {
            while (!shouldStop.get()) {
                byte[] audio = audioQueue.poll();
                if (audio != null) {
                    line.write(audio, 0, audio.length);
                } else {
                    try {
                        Thread.sleep(10);
                    } catch (InterruptedException ignored) {}
                }
            }
        }

        public void play(String base64Audio) {
            audioQueue.add(Base64.getDecoder().decode(base64Audio));
        }

        public void close() {
            shouldStop.set(true);
            try {
                playerThread.join(1000);
            } catch (InterruptedException ignored) {}
            line.drain();
            line.close();
        }
    }

    /**
     * 工具注册表 - 管理可用的工具及其实现
     */
    static class ToolRegistry {
        private final Map<String, Function<JsonObject, String>> tools = new ConcurrentHashMap<>();
        private final Map<String, JsonObject> pendingToolCalls = new ConcurrentHashMap<>();

        public ToolRegistry() {
            registerDefaultTools();
        }

        private void registerDefaultTools() {
            registerTool("get_current_weather", this::getCurrentWeather);
            registerTool("get_flight_price", this::getFlightPrice);
            registerTool("get_train_price", this::getTrainPrice);
        }

        public void registerTool(String name, Function<JsonObject, String> handler) {
            tools.put(name, handler);
        }

        /**
         * 构建工具定义（OpenAI 格式）
         */
        public List<Map<String, Object>> buildToolsDefinition() {
            List<Map<String, Object>> definitions = new ArrayList<>();

            definitions.add(createFunctionDefinition(
                    "get_current_weather",
                    "当你想查询指定城市的天气时非常有用。",
                    createParamsSchema(
                            Collections.singletonMap("location",
                                    createProperty("string", "城市或县区，比如北京市、杭州市、余杭区等。")),
                            Collections.singletonList("location")
                    )
            ));

            Map<String, Object> flightProps = new HashMap<>();
            flightProps.put("src", createProperty("string", "飞机起飞的城市，比如北京市、杭州市等。"));
            flightProps.put("dst", createProperty("string", "飞机降落的城市，比如北京市、杭州市区等。"));
            definitions.add(createFunctionDefinition(
                    "get_flight_price",
                    "当你想查询飞机票价格时非常有用。",
                    createParamsSchema(flightProps, Arrays.asList("src", "dst"))
            ));

            Map<String, Object> trainProps = new HashMap<>();
            trainProps.put("src", createProperty("string", "火车出发的城市，比如北京市、杭州市等。"));
            trainProps.put("dst", createProperty("string", "火车到达的城市，比如北京市、杭州市区等。"));
            definitions.add(createFunctionDefinition(
                    "get_train_price",
                    "当你想查询火车票价格时非常有用。",
                    createParamsSchema(trainProps, Arrays.asList("src", "dst"))
            ));

            return definitions;
        }

        private Map<String, Object> createFunctionDefinition(String name, String description, Map<String, Object> parameters) {
            Map<String, Object> function = new HashMap<>();
            function.put("name", name);
            function.put("description", description);
            function.put("parameters", parameters);

            Map<String, Object> tool = new HashMap<>();
            tool.put("type", "function");
            tool.put("function", function);
            return tool;
        }

        private Map<String, Object> createParamsSchema(Map<String, Object> properties, List<String> required) {
            Map<String, Object> schema = new HashMap<>();
            schema.put("type", "object");
            schema.put("properties", properties);
            schema.put("required", required);
            return schema;
        }

        private Map<String, Object> createProperty(String type, String description) {
            Map<String, Object> prop = new HashMap<>();
            prop.put("type", type);
            prop.put("description", description);
            return prop;
        }

        /**
         * 添加工具调用到待处理队列
         */
        public void addPendingToolCall(String callId, JsonObject toolCall) {
            pendingToolCalls.put(callId, toolCall);
        }

        /**
         * 检查是否有待处理的工具调用
         */
        public boolean hasPendingToolCalls() {
            return !pendingToolCalls.isEmpty();
        }

        /**
         * 处理所有待处理的工具调用
         */
        public void processPendingToolCalls(OmniRealtimeConversation conversation) {
            if (pendingToolCalls.isEmpty()) {
                return;
            }

            for (Map.Entry<String, JsonObject> entry : pendingToolCalls.entrySet()) {
                String callId = entry.getKey();
                JsonObject toolCall = entry.getValue();

                String result = executeTool(toolCall);
                sendToolResult(conversation, callId, result);
            }

            pendingToolCalls.clear();
        }

        private String executeTool(JsonObject toolCall) {
            String functionName = toolCall.get("name").getAsString();
            JsonObject arguments = new Gson().fromJson(
                    toolCall.get("arguments").getAsString(),
                    JsonObject.class
            );

            System.out.println("[Tool Call] start handling: " + functionName + ", args: " + arguments);

            Function<JsonObject, String> handler = tools.get(functionName);
            if (handler == null) {
                return "client没有找到这个工具，调用失败。";
            }

            String result = handler.apply(arguments);
            System.out.println("[Tool Call] response: " + result);
            return result;
        }

        private void sendToolResult(OmniRealtimeConversation conversation, String callId, String output) {
            JsonObject item = new JsonObject();
            item.addProperty("id", "item_" + UUID.randomUUID().toString().replace("-", ""));
            item.addProperty("type", "function_call_output");
            item.addProperty("call_id", callId);
            item.addProperty("output", output);

            conversation.createItem(item);
        }

        // ===== 工具实现 =====

        private String getCurrentWeather(JsonObject args) {
            String location = args.get("location").getAsString();
            return location + "今天天气为霾转晴，气温4/-4℃，微风";
        }

        private String getFlightPrice(JsonObject args) {
            String src = args.get("src").getAsString();
            String dst = args.get("dst").getAsString();
            return src + "到" + dst + "的机票价格为200~300美元。";
        }

        private String getTrainPrice(JsonObject args) {
            String src = args.get("src").getAsString();
            String dst = args.get("dst").getAsString();
            return "invalid apikey error";
        }
    }

    /**
     * 会话处理器 - 处理 WebSocket 事件
     */
    static class ConversationHandler extends OmniRealtimeCallback {
        private final AudioPlayer audioPlayer;
        private final ToolRegistry toolRegistry;
        private final AtomicBoolean shouldStop = new AtomicBoolean(false);
        private final AtomicReference<StringBuilder> responseTextRef = new AtomicReference<>(new StringBuilder());

        private long lastPackageTime = 0;
        private boolean isFirstText = true;
        private boolean isFirstAudio = true;

        public ConversationHandler(AudioPlayer audioPlayer, ToolRegistry toolRegistry) {
            this.audioPlayer = audioPlayer;
            this.toolRegistry = toolRegistry;
        }

        public AtomicBoolean getShouldStop() {
            return shouldStop;
        }

        @Override
        public void onOpen() {
            System.out.println("连接已建立");
        }

        @Override
        public void onClose(int code, String reason) {
            System.out.println("连接已关闭");
            shouldStop.set(true);
        }

        @Override
        public void onEvent(JsonObject message) {
            String type = message.get("type").getAsString();

            switch (type) {
                case "session.created":
                    handleSessionCreated(message);
                    break;
                case "conversation.item.input_audio_transcription.completed":
                    handleTranscriptionCompleted(message);
                    break;
                case "response.audio_transcript.delta":
                case "response.text.delta":
                    handleTextDelta(message);
                    break;
                case "response.audio.delta":
                    handleAudioDelta(message);
                    break;
                case "input_audio_buffer.speech_started":
                    handleSpeechStarted();
                    break;
                case "input_audio_buffer.speech_stopped":
                    handleSpeechStopped();
                    break;
                case "response.function_call_arguments.done":
                    handleFunctionCall(message);
                    break;
                case "response.done":
                    handleResponseDone();
                    break;
                default:
                    break;
            }
        }

        private void handleSessionCreated(JsonObject message) {
            String sessionId = message.get("session").getAsJsonObject().get("id").getAsString();
            System.out.println("start session: " + sessionId);
        }

        private void handleTranscriptionCompleted(JsonObject message) {
            System.out.println("question: " + message.get("transcript").getAsString());
        }

        private void handleTextDelta(JsonObject message) {
            if (isFirstText) {
                isFirstText = false;
                System.out.println("first text latency from vad end: " +
                        (System.currentTimeMillis() - lastPackageTime) + " ms");
            }
            String text = message.get("delta").getAsString();
            responseTextRef.get().append(text);
        }

        private void handleAudioDelta(JsonObject message) {
            if (isFirstAudio) {
                isFirstAudio = false;
                System.out.println("first audio latency from vad end: " +
                        (System.currentTimeMillis() - lastPackageTime) + " ms");
            }
            System.out.println("audio interval: " + (System.currentTimeMillis() - lastPackageTime) + " ms");
            lastPackageTime = System.currentTimeMillis();
            audioPlayer.play(message.get("delta").getAsString());
        }

        private void handleSpeechStarted() {
            System.out.println("======VAD Speech Start======");
        }

        private void handleSpeechStopped() {
            System.out.println("======VAD Speech End======");
            lastPackageTime = System.currentTimeMillis();
            isFirstText = true;
            isFirstAudio = true;
        }

        private void handleFunctionCall(JsonObject message) {
            System.out.println("======TOOL CALL======");
            String callId = message.get("call_id").getAsString();
            toolRegistry.addPendingToolCall(callId, message);
        }

        private void handleResponseDone() {
            System.out.println("======RESPONSE DONE======");
            System.out.println("all response text: " + responseTextRef.get());
            responseTextRef.set(new StringBuilder());
        }

        /**
         * 检查是否有待处理的工具调用
         */
        public boolean hasPendingToolCalls() {
            return toolRegistry.hasPendingToolCalls();
        }

        /**
         * 处理所有待处理的工具调用
         */
        public void processPendingToolCalls(OmniRealtimeConversation conversation) {
            toolRegistry.processPendingToolCalls(conversation);
        }
    }
}
```

WebSocket(Python)

```
import asyncio
import json
import base64
import os
import pyaudio
import websockets

# ==================== 常量定义 ====================
API_KEY = os.getenv("DASHSCOPE_API_KEY")
# 如果需要访问新加坡地域，请替换为：
# wss://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api-ws/v1/realtime
URL = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime"
MODEL = "qwen3.5-omni-plus-realtime"
VOICE = "Ethan"

# ==================== 工具定义 ====================
def get_current_weather(location):
    """查询指定城市天气"""
    return f"{location}今天天气为霾转晴，气温4/-4℃，微风"

def get_flight_price(src, dst):
    """查询飞机票价格"""
    return f"{src}到{dst}的机票价格为200~300美元。"

def get_train_price(src, dst):
    """查询火车票价格"""
    return f"{src}到{dst}的火车票价格为100~200元。"

# 工具名称到函数的映射
TOOL_FUNCTIONS = {
    "get_current_weather": get_current_weather,
    "get_flight_price": get_flight_price,
    "get_train_price": get_train_price,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                    }
                },
                "required": ["location"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_flight_price",
            "description": "当你想查询飞机票价格时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "src": {
                        "type": "string",
                        "description": "飞机起飞的城市，比如北京市、杭州市等。",
                    },
                    "dst": {
                        "type": "string",
                        "description": "飞机降落的城市，比如北京市、杭州市区等。",
                    },
                },
                "required": ["src", "dst"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_train_price",
            "description": "当你想查询火车票价格时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "src": {
                        "type": "string",
                        "description": "火车出发的城市，比如北京市、杭州市等。",
                    },
                    "dst": {
                        "type": "string",
                        "description": "火车到达的城市，比如北京市、杭州市区等。",
                    },
                },
                "required": ["src", "dst"],
            },
        },
    },
]

# ==================== 工具调用处理 ====================
def handle_tool_call(name, arguments_str):
    """
    处理工具调用请求

    Args:
        name: 工具函数名称
        arguments_str: JSON 格式的入参字符串

    Returns:
        工具执行结果字符串
    """
    try:
        arguments = json.loads(arguments_str)
        print(f'[工具调用] 开始处理: name={name}, args={arguments}')

        func = TOOL_FUNCTIONS.get(name)
        if func is None:
            result = f"客户端未找到工具: {name}"
            print(f'[工具调用] 错误: {result}')
            return result

        result = func(**arguments)
        print(f'[工具调用] 完成: {result}')
        return result

    except Exception as e:
        error_msg = f"工具调用失败: {str(e)}"
        print(f'[工具调用] 异常: {error_msg}')
        return error_msg

# ==================== 主程序 ====================
async def main():
    """主函数：建立 WebSocket 连接并进行语音对话"""
    pya = pyaudio.PyAudio()
    speaker = pya.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    # 建立 WebSocket 连接
    headers = {
        "Authorization": f"bearer {API_KEY}",
        "X-DashScope-OmniRealtime": "true",
    }
    async with websockets.connect(
        f"{URL}?model={MODEL}", additional_headers=headers,
    ) as ws:
        await ws.recv()

        # 配置会话参数
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": VOICE,
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "instructions": "你是个人助理小云",
                "turn_detection": {"type": "server_vad"},
                "input_audio_transcription": {"model": "qwen3-asr-flash-realtime"},
                "tools": TOOLS,
            },
        }))
        await ws.recv()

        # 音频采集协程
        async def send_audio():
            mic = pya.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
            try:
                while True:
                    data = mic.read(3200, exception_on_overflow=False)
                    await ws.send(json.dumps({
                        "type": "input_audio_buffer.append",
                        "audio": base64.b64encode(data).decode(),
                    }))
                    await asyncio.sleep(0.01)
            except asyncio.CancelledError:
                mic.close()

        pending = {}
        all_response_text = ""
        send_task = asyncio.create_task(send_audio())
        print("工具调用已启用，对着麦克风说话 (Ctrl+C 退出)...")

        # 事件处理循环
        async for raw in ws:
            msg = json.loads(raw)
            t = msg["type"]

            # 会话创建
            if t == "session.created":
                print(f"会话已启动: {msg['session']['id']}")

            # 播放音频
            elif t == "response.audio.delta":
                speaker.write(base64.b64decode(msg["delta"]))

            # 文本增量响应
            elif t in ("response.audio_transcript.delta", "response.text.delta"):
                all_response_text += msg.get("delta", "")

            # 用户语音转文本
            elif t == "conversation.item.input_audio_transcription.completed":
                print(f"[用户] {msg['transcript']}")

            # VAD 检测到语音开始
            elif t == "input_audio_buffer.speech_started":
                print("====== VAD 检测到语音开始 ======")

            # VAD 检测到语音结束
            elif t == "input_audio_buffer.speech_stopped":
                print("====== VAD 检测到语音结束 ======")

            # 收到工具调用请求
            elif t == "response.function_call_arguments.done":
                print("====== 收到工具调用请求 ======")
                pending[msg["call_id"]] = {
                    "name": msg["name"],
                    "arguments": msg["arguments"],
                }

            # 响应完成
            elif t == "response.done":
                if pending:
                    # 执行待处理的工具调用
                    for cid, info in pending.items():
                        result = handle_tool_call(info["name"], info["arguments"])
                        # 发送工具执行结果
                        await ws.send(json.dumps({
                            "type": "conversation.item.create",
                            "item": {
                                "type": "function_call_output",
                                "call_id": cid,
                                "output": result,
                            },
                        }))
                    pending.clear()
                    # 触发服务端继续生成回复
                    await ws.send(json.dumps({
                        "type": "response.create",
                        "response": {"modalities": ["text", "audio"]},
                    }))
                    print("====== 工具调用处理完成 ======")
                else:
                    # 普通响应完成，打印完整回复
                    if all_response_text:
                        print(f"[模型] {all_response_text}")
                    all_response_text = ""

        send_task.cancel()
        speaker.close()
        pya.terminate()

asyncio.run(main())
```

### 深度思考模型的工具调用

深度思考模型在输出工具调用信息前先进行推理，提升决策的可解释性与可靠性。

1.  **思考过程**
    
    模型逐步分析用户意图、识别所需工具、验证参数合法性，并规划调用策略；
    
2.  **工具调用**
    
    模型以结构化格式输出一个或多个函数调用请求。
    
    > 支持并行工具调用。
    

以下展示流式调用深度思考模型的工具调用示例。

> 文本生成思考模型请参见： 深度思考 ；多模态思考模型请参见： 图像与视频理解 、 非实时（Qwen-Omni） 。

> 开启思考模式（`enable_thinking=True`）时，`tool_choice` 不支持设置为 `"required"` 或 object 形式，同时设置会报错（`The tool_choice parameter does not support being set to required or object in thinking mode`），两者不兼容。如需在思考模式下稳定进行工具调用（如 MCP 调用），建议改用 Responses API 接入 MCP，参见 MCP。

#### OpenAI兼容

#### Python

### 示例代码

```
import os
from openai import OpenAI

# 初始化OpenAI客户端，配置阿里云DashScope服务
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 从环境变量读取API密钥
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 定义可用工具列表
tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # 无需参数
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]  # 必填参数
            }
        }
    }
]

messages = [{"role": "user", "content": input("请输入问题：")}]

# 多模态模型的 message示例
# messages = [{
#     "role": "user",
#     "content": [
#              {"type": "image_url","image_url": {"url": "https://img.alicdn.com/imgextra/i4/O1CN014CJhzi20NOzo7atOC_!!6000000006837-2-tps-2048-1365.png"}},
#              {"type": "text", "text": "根据图像上的地点，请问该地点当前的天气"}]
#     }]

completion = client.chat.completions.create(
    # 此处以qwen3.8-max为例，可更换为其它深度思考模型
    model="qwen3.8-max",
    messages=messages,
    extra_body={
        # 开启深度思考
        "enable_thinking": True
    },
    tools=tools,
    parallel_tool_calls=True,
    stream=True,
    # 解除注释后，可以获取到token消耗信息
    # stream_options={
    #     "include_usage": True
    # }
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
tool_info = []          # 存储工具调用信息
is_answering = False   # 判断是否结束思考过程并开始回复
print("="*20+"思考过程"+"="*20)
for chunk in completion:
    if not chunk.choices:
        # 处理用量统计信息
        print("\n"+"="*20+"Usage"+"="*20)
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 处理AI的思考过程（链式推理）
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None:
            reasoning_content += delta.reasoning_content
            print(delta.reasoning_content,end="",flush=True)  # 实时输出思考过程

        # 处理最终回复内容
        else:
            if not is_answering:  # 首次进入回复阶段时打印标题
                is_answering = True
                print("\n"+"="*20+"回复内容"+"="*20)
            if delta.content is not None:
                answer_content += delta.content
                print(delta.content,end="",flush=True)  # 流式输出回复内容

            # 处理工具调用信息（支持并行工具调用）
            if delta.tool_calls is not None:
                for tool_call in delta.tool_calls:
                    index = tool_call.index  # 工具调用索引，用于并行调用

                    # 动态扩展工具信息存储列表
                    while len(tool_info) <= index:
                        tool_info.append({})

                    # 收集工具调用ID（用于后续函数调用）
                    if tool_call.id:
                        tool_info[index]['id'] = tool_info[index].get('id', '') + tool_call.id

                    # 收集函数名称（用于后续路由到具体函数）
                    if tool_call.function and tool_call.function.name:
                        tool_info[index]['name'] = tool_info[index].get('name', '') + tool_call.function.name

                    # 收集函数参数（JSON字符串格式，需要后续解析）
                    if tool_call.function and tool_call.function.arguments:
                        tool_info[index]['arguments'] = tool_info[index].get('arguments', '') + tool_call.function.arguments

print(f"\n"+"="*19+"工具调用信息"+"="*19)
if not tool_info:
    print("没有工具调用")
else:
    print(tool_info)
```

### 返回结果

输入“四个直辖市的天气”，得到以下返回结果：

```
====================思考过程====================
好的，用户问的是“四个直辖市的天气”。首先，我需要明确四个直辖市是哪几个。根据中国的行政区划，直辖市包括北京、上海、天津和重庆。所以用户想知道这四个城市的天气情况。

接下来，我需要检查可用的工具。提供的工具中有get_current_weather函数，参数是location，类型字符串。每个城市需要单独查询，因为函数一次只能查一个地点。因此，我需要为每个直辖市调用一次这个函数。

然后，我需要考虑如何生成正确的工具调用。每个调用应该包含城市名称作为参数。比如，第一个调用是北京，第二个是上海，依此类推。确保参数名称是location，值是正确的城市名。

另外，用户可能希望得到每个城市的天气信息，所以需要确保每个函数调用都正确无误。可能需要连续调用四次，每次对应一个城市。不过，根据工具的使用规则，可能需要分多次处理，或者一次生成多个调用。但根据示例，可能每次只调用一个函数，所以可能需要逐步进行。

最后，确认是否有其他需要考虑的因素，比如参数是否正确，城市名称是否准确，以及是否需要处理可能的错误情况，比如城市不存在或API不可用。但目前看来，四个直辖市都是明确的，应该没问题。
====================回复内容====================

===================工具调用信息===================
[{'id': 'call_767af2834c12488a8fe6e3', 'name': 'get_current_weather', 'arguments': '{"location": "北京市"}'}, {'id': 'call_2cb05a349c89437a947ada', 'name': 'get_current_weather', 'arguments': '{"location": "上海市"}'}, {'id': 'call_988dd180b2ca4b0a864ea7', 'name': 'get_current_weather', 'arguments': '{"location": "天津市"}'}, {'id': 'call_4e98c57ea96a40dba26d12', 'name': 'get_current_weather', 'arguments': '{"location": "重庆市"}'}]
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';

const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

const tools = [
    {
        type: "function",
        function: {
            name: "get_current_time",
            description: "当你想知道现在的时间时非常有用。",
            parameters: {}
        }
    },
    {
        type: "function",
        function: {
            name: "get_current_weather",
            description: "当你想查询指定城市的天气时非常有用。",
            parameters: {
                type: "object",
                properties: {
                    location: {
                        type: "string",
                        description: "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                required: ["location"]
            }
        }
    }
];

async function main() {
    const rl = readline.createInterface({ input, output });
    const question = await rl.question("请输入您的问题：");
    rl.close();

    const messages = [{ role: "user", content: question }];
    // 多模态模型的 message示例
    // const messages= [{
    //     role: "user",
    //     content: [{type: "image_url", image_url: {url: "https://img.alicdn.com/imgextra/i2/O1CN01FbTJon1ErXVGMRdsN_!!6000000000405-0-tps-1024-683.jpg"}},
    //               {type: "text", text: "图中地点的天气？"}]
    //   }];
    let reasoningContent = "";
    let answerContent = "";
    const toolInfo = [];
    let isAnswering = false;

    console.log("=".repeat(20) + "思考过程" + "=".repeat(20));

    try {
        const stream = await openai.chat.completions.create({
            // 此处以qwen3.8-max为例，可更换为其它深度思考模型
            model: "qwen3.8-max",
            messages,
            // 开启深度思考
            enable_thinking: true,
            tools,
            stream: true,
            parallel_tool_calls: true
        });

        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log("\n" + "=".repeat(20) + "Usage" + "=".repeat(20));
                console.log(chunk.usage);
                continue;
            }

            const delta = chunk.choices[0]?.delta;
            if (!delta) continue;

            // 处理思考过程
            if (delta.reasoning_content) {
                reasoningContent += delta.reasoning_content;
                process.stdout.write(delta.reasoning_content);
            }
            // 处理回复内容
            else {
                if (!isAnswering) {
                    isAnswering = true;
                    console.log("\n" + "=".repeat(20) + "回复内容" + "=".repeat(20));
                }
                if (delta.content) {
                    answerContent += delta.content;
                    process.stdout.write(delta.content);
                }
                // 处理工具调用
                if (delta.tool_calls) {
                    for (const toolCall of delta.tool_calls) {
                        const index = toolCall.index;

                        // 确保数组长度足够
                        while (toolInfo.length <= index) {
                            toolInfo.push({});
                        }

                        // 更新工具ID
                        if (toolCall.id) {
                            toolInfo[index].id = (toolInfo[index].id || "") + toolCall.id;
                        }

                        // 更新函数名称
                        if (toolCall.function?.name) {
                            toolInfo[index].name = (toolInfo[index].name || "") + toolCall.function.name;
                        }

                        // 更新参数
                        if (toolCall.function?.arguments) {
                            toolInfo[index].arguments = (toolInfo[index].arguments || "") + toolCall.function.arguments;
                        }
                    }
                }
            }
        }

        console.log("\n" + "=".repeat(19) + "工具调用信息" + "=".repeat(19));
        console.log(toolInfo.length ? toolInfo : "没有工具调用");

    } catch (error) {
        console.error("发生错误:", error);
    }
}

main();
```

### 返回结果

输入“四个直辖市的天气”，得到以下返回结果：

```
请输入您的问题：四个直辖市的天气
====================思考过程====================
好的，用户问的是四个直辖市的天气。首先，我需要明确中国的四个直辖市分别是哪几个。北京、上海、天津和重庆，对吧？接下来，我需要为每个城市调用天气查询功能。

但是用户的问题可能需要我分别获取这四个城市的天气情况。每个城市都需要调用一次get_current_weather函数，参数是各自的城市名称。我需要确保参数正确，比如直辖市的全名，比如“北京市”、“上海市”、“天津市”和“重庆市”。

然后，我需要按照顺序依次调用这四个城市的天气接口。每个调用都需要单独的tool_call。用户可能希望得到每个城市的当前天气信息，所以需要确保每个调用都正确无误。可能需要注意每个城市的正确拼写和名称，避免出现错误。例如，重庆有时可能被简称为“重庆市”，所以参数里应该用全称。

现在，我需要生成四个tool_call，每个对应一个直辖市。检查每个参数是否正确，然后按顺序排列。这样用户就能得到四个直辖市的天气数据了。
====================回复内容====================

===================工具调用信息===================
[
  {
    id: 'call_21dc802e717f491298d1b2',
    name: 'get_current_weather',
    arguments: '{"location": "北京市"}'
  },
  {
    id: 'call_2cd3be1d2f694c4eafd4e5',
    name: 'get_current_weather',
    arguments: '{"location": "上海市"}'
  },
  {
    id: 'call_48cf3f78e02940bd9085e4',
    name: 'get_current_weather',
    arguments: '{"location": "天津市"}'
  },
  {
    id: 'call_e230a2b4c64f4e658d223e',
    name: 'get_current_weather',
    arguments: '{"location": "重庆市"}'
  }
]
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "messages": [
        {
            "role": "user",
            "content": "杭州天气怎么样"
        }
    ],
    "tools": [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location":{
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
  ],
  "enable_thinking": true,
  "stream": true
}'
```

#### DashScope

#### Python

### 示例代码

```
import dashscope
from dashscope import MultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}  # 因为获取当前时间无需输入参数，因此parameters为空字典
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    # 查询天气时需要提供位置，因此参数设置为location
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# 定义问题
messages = [{"role": "user", "content": [{"text": input("请输入问题：")}]}]

# 多模态模型的 message示例
# messages = [
# {
#     "role": "user",
#     "content": [
#     {"image": "https://img.alicdn.com/imgextra/i2/O1CN01FbTJon1ErXVGMRdsN_!!6000000000405-0-tps-1024-683.jpg"},
#     {"text": "图像地点天气？"}]
# }]

completion = MultiModalConversation.call(
    # 此处以qwen3.8-max为例，可更换为其它深度思考模型
    model="qwen3.8-max",
    messages=messages,
    enable_thinking=True,
    tools=tools,
    parallel_tool_calls=True,
    stream=True,
    incremental_output=True,
    result_format="message"
)

reasoning_content = ""
answer_content = ""
tool_info = []
is_answering = False
print("="*20+"思考过程"+"="*20)

for chunk in completion:
    if chunk.status_code == 200:
        msg = chunk.output.choices[0].message

        # 处理思考过程
        if 'reasoning_content' in msg and msg.reasoning_content:
            reasoning_content += msg.reasoning_content
            print(msg.reasoning_content, end="", flush=True)

        # 处理回复内容
        if 'content' in msg and msg.content:
            if not is_answering:
                is_answering = True
                print("\n"+"="*20+"回复内容"+"="*20)
            answer_content += msg.content
            print(msg.content, end="", flush=True)

        # 处理工具调用
        if 'tool_calls' in msg and msg.tool_calls:
            for tool_call in msg.tool_calls:
                index = tool_call['index']

                while len(tool_info) <= index:
                    tool_info.append({'id': '', 'name': '', 'arguments': ''})  # 初始化所有字段

                # 增量更新工具ID
                if 'id' in tool_call:
                    tool_info[index]['id'] += tool_call.get('id', '')

                # 增量更新函数信息
                if 'function' in tool_call:
                    func = tool_call['function']
                    # 增量更新函数名称
                    if 'name' in func:
                        tool_info[index]['name'] += func.get('name', '')
                    # 增量更新参数
                    if 'arguments' in func:
                        tool_info[index]['arguments'] += func.get('arguments', '')

print(f"\n"+"="*19+"工具调用信息"+"="*19)
if not tool_info:
    print("没有工具调用")
else:
    print(tool_info)
```

### 返回结果

输入“四个直辖市的天气”，得到以下返回结果：

```
请输入问题：四个直辖市的天气
====================思考过程====================
好的，用户问的是四个直辖市的天气。首先，我需要确认中国的四个直辖市分别是哪些。北京、上海、天津和重庆，对吧？接下来，用户需要每个城市的天气情况，所以我需要调用天气查询功能。

不过，问题来了，用户没有指定具体的城市名称，只是说四个直辖市。可能需要我明确每个直辖市的名称，然后分别查询。比如，北京、上海、天津、重庆这四个直辖市。我需要确保每个城市都正确无误。

然后，我要检查可用的工具，用户提供的函数是get_current_weather，参数是location。因此，我需要为每个直辖市调用这个函数，传入对应的城市名称作为参数。比如，第一次调用location是北京市，第二次是上海市，第三次是天津市，第四次是重庆市。

不过，可能需要注意，像重庆这样的直辖市，有时候可能需要更具体的区，但用户可能只需要市级的天气。所以直接使用直辖市名称应该没问题。接下来，我需要生成四个独立的函数调用，每个对应一个直辖市。这样用户就能得到四个城市的天气情况了。

最后，确保每个调用的参数正确，并且没有遗漏。这样用户的问题就能得到完整的回答了。
===================工具调用信息===================
[{'id': 'call_2f774ed97b0e4b24ab10ec', 'name': 'get_current_weather', 'arguments': '{"location": "北京市"}'}, {'id': 'call_dc3b05b88baa48c58bc33a', 'name': 'get_current_weather', 'arguments': '{"location": "上海市"}}'}, {'id': 'call_249b2de2f73340cdb46cbc', 'name': 'get_current_weather', 'arguments': '{"location": "天津市"}'}, {'id': 'call_833333634fda49d1b39e87', 'name': 'get_current_weather', 'arguments': '{"location": "重庆市"}}'}]
```

#### Java

### 示例代码

```
// dashscope SDK的版本 >= 2.19.4
import java.util.Arrays;

import com.alibaba.dashscope.exception.UploadFileException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.tools.ToolFunction;
import com.alibaba.dashscope.tools.FunctionDefinition;
import io.reactivex.Flowable;
import com.fasterxml.jackson.databind.node.ObjectNode;
import java.lang.System;
import com.github.victools.jsonschema.generator.Option;
import com.github.victools.jsonschema.generator.OptionPreset;
import com.github.victools.jsonschema.generator.SchemaGenerator;
import com.github.victools.jsonschema.generator.SchemaGeneratorConfig;
import com.github.victools.jsonschema.generator.SchemaGeneratorConfigBuilder;
import com.github.victools.jsonschema.generator.SchemaVersion;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Collections;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static ObjectNode jsonSchemaWeather;
    private static ObjectNode jsonSchemaTime;
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    static class TimeTool {
        public String call() {
            LocalDateTime now = LocalDateTime.now();
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
            return "当前时间：" + now.format(formatter) + "。";
        }
    }

    static class WeatherTool {
        private String location;

        public WeatherTool(String location) {
            this.location = location;
        }

        public String call() {
            return location + "今天是晴天";
        }
    }

    static {
        SchemaGeneratorConfigBuilder configBuilder = new SchemaGeneratorConfigBuilder(
                SchemaVersion.DRAFT_2020_12, OptionPreset.PLAIN_JSON);
        SchemaGeneratorConfig config = configBuilder
                .with(Option.EXTRA_OPEN_API_FORMAT_VALUES)
                .without(Option.FLATTENED_ENUMS_FROM_TOSTRING)
                .build();
        SchemaGenerator generator = new SchemaGenerator(config);
        jsonSchemaWeather = generator.generateSchema(WeatherTool.class);
        jsonSchemaTime = generator.generateSchema(TimeTool.class);
    }
    private static void handleGenerationResult(GenerationResult message) {
        System.out.println(JsonUtils.toJson(message));
    }

    // 为文本生成模型创建工具调用方法
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }
    // 构建文本生成模型参数，支持工具调用
    private static GenerationParam buildGenerationParam(Message userMsg) {
        FunctionDefinition fdWeather = buildFunctionDefinition(
                "get_current_weather", "获取指定地区的天气", jsonSchemaWeather);
        FunctionDefinition fdTime = buildFunctionDefinition(
                "get_current_time", "获取当前时刻的时间", jsonSchemaTime);

        return GenerationParam.builder()
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .enableThinking(true)
                .messages(Arrays.asList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .incrementalOutput(true)
                .tools(Arrays.asList(
                        ToolFunction.builder().function(fdWeather).build(),
                        ToolFunction.builder().function(fdTime).build()))
                .build();
    }

    // 为多模态模型创建工具调用方法
    public static void streamCallWithMultiModalMessage(MultiModalConversation conv, MultiModalMessage userMsg)
            throws NoApiKeyException, ApiException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(userMsg);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message -> System.out.println(JsonUtils.toJson(message)));
    }

    // 构建多模态模型参数，支持工具调用
    private static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage userMsg) {
        FunctionDefinition fdWeather = buildFunctionDefinition(
                "get_current_weather", "获取指定地区的天气", jsonSchemaWeather);
        FunctionDefinition fdTime = buildFunctionDefinition(
                "get_current_time", "获取当前时刻的时间", jsonSchemaTime);

        return MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-vl-plus")  // 使用多模态模型 Qwen3-VL
                .enableThinking(true)
                .messages(Arrays.asList(userMsg))
                .tools(Arrays.asList(  // 配置工具列表
                        ToolFunction.builder().function(fdWeather).build(),
                        ToolFunction.builder().function(fdTime).build()))
                .build();
    }

    private static FunctionDefinition buildFunctionDefinition(
            String name, String description, ObjectNode schema) {
        return FunctionDefinition.builder()
                .name(name)
                .description(description)
                .parameters(JsonUtils.parseString(schema.toString()).getAsJsonObject())
                .build();
    }

    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg = MultiModalMessage.builder().role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("text", "请告诉我杭州的天气"))).build();
            try {
                streamCallWithMultiModalMessage(conv, userMsg);
            } catch (UploadFileException e) {
                throw new RuntimeException(e);
            }
//             使用文本生成模型进行工具调用时，请解除下列注释
//            Generation gen = new Generation();
//            Message userMessage = Message.builder()
//                    .role(Role.USER.getValue())
//                    .content("请告诉我杭州的天气")
//                    .build();
//            try {
//                streamCallWithMessage(gen, userMessage);
//            } catch (InputRequiredException e) {
//                throw new RuntimeException(e);
//            }
        } catch (ApiException | NoApiKeyException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### 返回结果

```
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":6,"total_tokens":244},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"好的，用户让我"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":12,"total_tokens":250},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"告诉杭州的天气。我"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":16,"total_tokens":254},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"需要先确定是否有"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":22,"total_tokens":260},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"相关的工具可用。查看提供的"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":28,"total_tokens":266},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"工具，发现有一个get_current"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":34,"total_tokens":272},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"_weather函数，参数是location"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":38,"total_tokens":276},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"。所以应该调"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":43,"total_tokens":281},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"用这个函数，参数"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":48,"total_tokens":286},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"设为杭州。不需要"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":52,"total_tokens":290},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"其他工具，因为"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":56,"total_tokens":294},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"用户只问了"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":60,"total_tokens":298},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"天气。接下来构造"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":64,"total_tokens":302},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"tool_call，把"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":68,"total_tokens":306},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"名称和参数填"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":73,"total_tokens":311},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"进去。确保参数是"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":78,"total_tokens":316},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"JSON对象，location是"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":82,"total_tokens":320},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"字符串。检查无"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":88,"total_tokens":326},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"误后返回。"}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":106,"total_tokens":344},"output":{"choices":[{"finish_reason":"null","message":{"role":"assistant","content":"","reasoning_content":"","tool_calls":[{"type":"function","id":"call_ecc41296dccc47baa01567","function":{"name":"get_current_weather","arguments":"{\"location\": \"杭州"}}]}}]}}
{"requestId":"4edb81cd-4647-9d5d-88f9-a4f30bc6d8dd","usage":{"input_tokens":238,"output_tokens":108,"total_tokens":346},"output":{"choices":[{"finish_reason":"tool_calls","message":{"role":"assistant","content":"","reasoning_content":"","tool_calls":[{"type":"function","id":"","function":{"arguments":"\"}"}}]}}]}}
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 如果使用纯文本生成模型，请将url替换为 https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen3.8-max",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [{"text": "杭州天气"}]
            }
        ]
    },
    "parameters": {
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message",
        "tools": [{
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "当你想知道现在的时间时非常有用。",
                "parameters": {}
            }
        },{
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "当你想查询指定城市的天气时非常有用。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                        }
                    },
                    "required": ["location"]
                }
            }
        }]
    }
}'
```

## 应用于生产环境

### 测试工具调用准确率

-   **建立评估体系**：
    
    构建贴近真实业务的测试数据集，定义清晰的评估指标，如工具选择准确率、参数提取准确率、端到端成功率等。
    
-   **优化提示词**
    
    根据测试暴露的具体问题（选错工具、参数错误），针对性优化系统提示词、工具描述和参数描述。
    
-   **升级模型**
    
    提示词调优无法提升性能时，升级到更强的模型版本（如 `qwen3.6-plus`）是最直接有效的方法。
    

### 动态控制工具数量

应用集成的工具数量达到几十甚至上百个时，将全部工具提供给模型会带来以下问题：

-   **性能下降**：模型在庞大的工具集中选择正确工具的难度剧增；
-   **成本与延迟**：大量的工具描述会消耗巨量的输入 Token，导致费用上升和响应变慢；

解决方案：**在调用模型前增加工具路由/检索层**，根据用户查询从工具库中筛选出小而相关的工具子集，再提供给模型。

**实现工具路由的几种主流方法：**

-   **语义检索**
    
    将工具描述信息（`description`）通过 Embedding 模型转化为向量，并存入向量数据库。当用户查询时，将查询向量通过向量相似度搜索，召回最相关的 Top-K 个工具。
    
-   **混合检索**
    
    将语义检索的“模糊匹配”能力与传统关键词或元数据标签的“精确匹配”能力相结合。为工具添加 `tags` 或 `keywords` 字段，检索时同时进行向量搜索和关键词过滤，可以大幅提升高频或特定场景下的召回精准度。
    
-   **轻量级 LLM 路由器**
    
    对于更复杂的路由逻辑，可以使用一个更小、更快、更便宜的模型（如 Qwen-Flash）作为前置“路由模型”。它的任务是根据用户问题输出相关的工具名称列表。
    

**实践建议**

-   **保持候选集精简**：无论使用何种方法，最终提供给主模型的工具数量建议**不超过 20 个**。这是在模型认知负荷、成本、延迟和准确率之间的最佳平衡点。
-   **分层过滤策略**：可以构建一个漏斗式的路由策略。例如，先用成本极低的关键词/规则匹配进行第一轮筛选，过滤掉明显不相关的工具，再对剩余的工具进行语义检索，从而提高效率和质量。

### 工具安全性原则

向大模型开放工具执行能力时，安全是首要考量。核心原则：“最小权限”和“人类确认”。

-   **最小权限原则**：为模型提供的工具集应严格遵守最小权限原则。默认情况下，工具应是只读的（如查询天气、搜索文档），避免直接提供任何涉及状态变更或资源操作的“写”权限。
-   **危险工具隔离**：请勿向大模型直接提供危险工具，例如执行任意代码（`code interpreter`）、操作文件系统（`fs.delete`）、执行数据库删除或更新操作（`db.drop_table`）或涉及资金流转的工具（`payment.transfer`）。
-   **人类参与**：对于所有高权限或不可逆的操作，必须引入人工审核和确认环节。模型可以生成操作请求，但最终的执行“按钮”必须由人类用户点击。例如，模型可以准备好一封邮件，但发送操作需要用户确认。

### 用户体验优化

Function Calling 链路较长，任何环节出问题都可能影响用户体验。

#### 处理工具运行失败

工具运行失败是常见情况，可采取以下策略：

-   **最大重试次数**：设置合理的重试上限（例如 3 次），避免因连续失败导致用户长时间等待或系统资源浪费。
-   **提供兜底话术**：当重试耗尽或遇到无法解决的错误时，应向用户返回清晰、友好的提示信息，例如：“抱歉，我暂时无法查询到相关信息，可能是服务有些繁忙，请您稍后再试。”

#### 应对处理延迟

较高延迟会降低用户满意度，需从前端交互和后端两方面优化。

-   **设置超时时间**：为 Function Calling 的每一步设置独立且合理的超时时间。一旦超时，应立即中断操作并给出反馈。
-   **提供即时反馈**：开始执行 Function Calling 时，建议在界面上给出提示，如“正在为您查询天气...”、“正在搜索相关信息...”，向用户实时反馈处理进度。

## 计费说明

除 messages 数组中的 Token 外，工具描述信息也作为输入 Token 计费。

通过 System Message 传入工具信息

推荐您参考[如何使用](https://help.aliyun.com/zh/model-studio/qwen-function-calling#038e24005c1vt)部分，通过 tools 参数向大模型传入工具信息。如果您需要通过 System Message 传入工具信息，为了模型的最佳效果，请参考以下代码中的提示词模板：

#### OpenAI兼容

#### Python

### 示例代码

```
import os
from openai import OpenAI
import json

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

# 自定义 System prompt，可根据您的需求修改
custom_prompt = "你是一个智能助手，专门负责调用各种工具来帮助用户解决问题。你可以根据用户的需求选择合适的工具并正确调用它们。"

tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# 遍历tools列表，为每个工具构建描述
tools_descriptions = []
for tool in tools:
    tool_json = json.dumps(tool, ensure_ascii=False)
    tools_descriptions.append(tool_json)

# 将所有工具描述组合成一个字符串
tools_content = "\n".join(tools_descriptions)

system_prompt = f"""{custom_prompt}

# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{tools_content}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{{"name": <function-name>, "arguments": <args-json-object>}}
</tool_call>"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "几点了"}
]

completion = client.chat.completions.create(
    model="qwen3.8-max",
    extra_body={"enable_thinking": False},
    messages=messages,
)
print(completion.model_dump_json())
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";

const client = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

// 自定义 System prompt
const customPrompt = "你是一个智能助手，专门负责调用各种工具来帮助用户解决问题。你可以根据用户的需求选择合适的工具并正确调用它们。";

const tools = [
    // 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    // 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
];

// 遍历tools列表，为每个工具构建描述
const toolsDescriptions = [];
for (const tool of tools) {
    const toolJson = JSON.stringify(tool, null, 2);
    toolsDescriptions.push(toolJson);
}

// 将所有工具描述组合成一个字符串
const toolsContent = toolsDescriptions.join("\n");

const systemPrompt = `${customPrompt}

# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
${toolsContent}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{"name": <function-name>, "arguments": <args-json-object>}
</tool_call>`;

const messages = [
    {"role": "system", "content": systemPrompt},
    {"role": "user", "content": "几点了"}
];

async function main() {
    try {
        const completion = await client.chat.completions.create({
            model: "qwen3.8-max",
            enable_thinking: false,
            messages: messages,
        });

        console.log(JSON.stringify(completion, null, 2));
    } catch (error) {
        console.error("Error:", error);
    }
}

main();
```

#### DashScope

#### Python

### 示例代码

```
import os
from dashscope import MultiModalConversation
import json
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 自定义 System prompt
custom_prompt = "你是一个智能助手，专门负责调用各种工具来帮助用户解决问题。你可以根据用户的需求选择合适的工具并正确调用它们。"

tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# 遍历tools列表，为每个工具构建描述
tools_descriptions = []
for tool in tools:
    tool_json = json.dumps(tool, ensure_ascii=False)
    tools_descriptions.append(tool_json)

# 将所有工具描述组合成一个字符串
tools_content = "\n".join(tools_descriptions)

system_prompt = f"""{custom_prompt}

# Tools

You may call one or more functions to assist with the user query.

You are provided with function signatures within <tools></tools> XML tags:
<tools>
{tools_content}
</tools>

For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
<tool_call>
{{"name": <function-name>, "arguments": <args-json-object>}}
</tool_call>"""

messages = [
    {"role": "system", "content": [{"text": system_prompt}]},
    {"role": "user", "content": [{"text": "几点了"}]}
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.8-max",
    enable_thinking=False,
    messages=messages,
    result_format="message",  # 将输出设置为message形式
)

print(response)
```

#### Java

### 示例代码

```
// Copyright (c) Alibaba, Inc. and its affiliates.
// version >= 2.12.0

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void main(String[] args) {
        try {
            callToolWithCustomPrompt();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(String.format("Exception: %s", e.getMessage()));
        } catch (Exception e) {
            System.out.println(String.format("Exception: %s", e.getMessage()));
        }
        System.exit(0);
    }

    public static void callToolWithCustomPrompt()
            throws NoApiKeyException, ApiException, UploadFileException {

        // 自定义 System prompt
        String customPrompt = "你是一个智能助手，专门负责调用各种工具来帮助用户解决问题。你可以根据用户的需求选择合适的工具并正确调用它们。";

        // 构建工具描述
        String[] toolsDescriptions = {
                // 工具1 获取当前时刻的时间
                "{\n" +
                        "    \"type\": \"function\",\n" +
                        "    \"function\": {\n" +
                        "        \"name\": \"get_current_time\",\n" +
                        "        \"description\": \"当你想知道现在的时间时非常有用。\",\n" +
                        "        \"parameters\": {}\n" +
                        "    }\n" +
                        "}",
                // 工具2 获取指定城市的天气
                "{\n" +
                        "    \"type\": \"function\",\n" +
                        "    \"function\": {\n" +
                        "        \"name\": \"get_current_weather\",\n" +
                        "        \"description\": \"当你想查询指定城市的天气时非常有用。\",\n" +
                        "        \"parameters\": {\n" +
                        "            \"type\": \"object\",\n" +
                        "            \"properties\": {\n" +
                        "                \"location\": {\n" +
                        "                    \"type\": \"string\",\n" +
                        "                    \"description\": \"城市或县区，比如北京市、杭州市、余杭区等。\"\n" +
                        "                }\n" +
                        "            },\n" +
                        "            \"required\": [\"location\"]\n" +
                        "        }\n" +
                        "    }\n" +
                        "}"
        };

        // 将所有工具描述组合成一个字符串
        String toolsContent = String.join("\n", toolsDescriptions);

        // 构建系统提示词
        String systemPrompt = String.format("%s\n\n" +
                        "# Tools\n\n" +
                        "You may call one or more functions to assist with the user query.\n\n" +
                        "You are provided with function signatures within <tools></tools> XML tags:\n" +
                        "<tools>\n%s\n</tools>\n\n" +
                        "For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:\n"
                        +
                        "<tool_call>\n" +
                        "{\"name\": <function-name>, \"arguments\": <args-json-object>}\n" +
                        "</tool_call>",
                customPrompt, toolsContent);

        // 构建消息列表
        MultiModalMessage systemMsg = MultiModalMessage.builder()
                .role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", systemPrompt)))
                .build();

        MultiModalMessage userMsg = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "几点了")))
                .build();

        List<MultiModalMessage> messages = new ArrayList<>(Arrays.asList(systemMsg, userMsg));

        // 构建请求参数
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen3.8-max")
                .enableThinking(false)
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .messages(messages)
                .build();

        // 调用多模态对话接口
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationResult result = conv.call(param);

        // 输出结果
        System.out.println(JsonUtils.toJson(result));
    }
}
```

> 运行以上代码后，可以使用 XML 解析器提取 `<tool_call>` 和 `</tool_call>` 之间的工具调用信息，包括函数名和入参。

## 错误码

如果模型调用失败并返回报错信息，请参见错误码进行解决。
