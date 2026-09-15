# 多轮对话

通义千问 API 是无状态的，不会保存对话历史。要实现多轮对话，需在每次请求中显式传入历史对话消息，并可结合截断、摘要、召回等策略，高效管理上下文，减少 Token 消耗。

> 本文介绍如何通过 OpenAI 兼容的 Chat Completion 接口或 DashScope 接口实现多轮对话。 Responses API 可更便捷地实现多轮对话，参见：[OpenAI兼容-Responses](raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md)。

## 工作原理

实现多轮对话的核心是维护一个 `messages` 数组。每一轮对话都需要将用户的最新提问和模型的回复追加到此数组中，并将其作为下一次请求的输入。

以下示例为多轮对话时 `messages` 的状态变化：

1.  **第一轮对话**
    
    向`messages` 数组添加用户问题。
    

```
// 使用文本模型
[
    {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"}
]

// 使用多模态模型，以 Qwen-VL 为例
// {"role": "user",
//       "content": [{"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"}},
//                   {"type": "text", "text": "请问图片展现了有哪些商品？"}]
// }
```

2.  **第二轮对话**
    
    向`messages`数组添加大模型回复内容与用户的最新提问。
    

```
// 使用文本模型
[
    {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"},
    {"role": "assistant", "content": "我推荐《xxx》，这是一部经典的科幻作品。"},
    {"role": "user", "content": "这部电影的导演是谁？"}
]

// 使用多模态模型，以 Qwen-VL 为例
//[
//    {"role": "user", "content": [
//                    {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"}},
//                   {"type": "text", "text": "请问图片展现了有哪些商品？"}]},
//    {"role": "assistant", "content": "图片展示了三件商品：一件浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"},
//    {"role": "user", "content": "它们属于什么风格？"}
//]
```

## 快速开始

#### OpenAI兼容

Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=messages
    )
    return completion.choices[0].message.content

# 初始化 messages
messages = []

# 第 1 轮
messages.append({"role": "user", "content": "推荐一部关于太空探索的科幻电影。"})
print("第1轮")
print(f"用户：{messages[0]['content']}")
assistant_output = get_response(messages)
messages.append({"role": "assistant", "content": assistant_output})
print(f"模型：{assistant_output}\n")

# 第 2 轮
messages.append({"role": "user", "content": "这部电影的导演是谁？"})
print("第2轮")
print(f"用户：{messages[-1]['content']}")
assistant_output = get_response(messages)
messages.append({"role": "assistant", "content": assistant_output})
print(f"模型：{assistant_output}\n")
```

Node.js

```
import OpenAI from "openai";

// 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
const BASE_URL = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1";
// 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
const openai = new OpenAI({
  // 若没有配置环境变量，请将下行替换为：apiKey:"sk-xxx",
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: BASE_URL,
});

async function getResponse(messages) {
  const completion = await openai.chat.completions.create({
    model: "qwen3.8-max",
    messages: messages,
  });
  return completion.choices[0].message.content;
}

async function runConversation() {
  const messages = [];

  // 第 1 轮
  messages.push({ role: "user", content: "推荐一部关于太空探索的科幻电影。" });
  console.log("第1轮");
  console.log("用户：" + messages[0].content);

  let assistant_output = await getResponse(messages);
  messages.push({ role: "assistant", content: assistant_output });
  console.log("模型：" + assistant_output + "\n");

  // 第 2 轮
  messages.push({ role: "user", content: "这部电影的导演是谁？" });
  console.log("第2轮");
  console.log("用户：" + messages[messages.length - 1].content);

  assistant_output = await getResponse(messages);
  messages.push({ role: "assistant", content: assistant_output });
  console.log("模型：" + assistant_output + "\n");
}

runConversation();
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "messages":[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "你好"
        },
        {
            "role": "assistant",
            "content": "你好啊，我是通义千问。"
        },
        {
            "role": "user",
            "content": "你有哪些技能？"
        }
    ]
}'
```

#### DashScope

#### Python

示例代码以手机商店导购为例，导购与顾客会进行多轮对话来采集购买意向，采集完成后会结束会话。

```
import os
from dashscope import Generation
import dashscope
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

def get_response(messages):
    response = Generation.call(
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        model="qwen-plus",
        messages=messages,
        result_format="message",
    )
    return response

# 初始化一个 messages 数组
messages = [
    {
        "role": "system",
        "content": """你是一名阿里云百炼手机商店的店员，你负责给用户推荐手机。手机有两个参数：屏幕尺寸（包括6.1英寸、6.5英寸、6.7英寸）、分辨率（包括2K、4K）。
        你一次只能向用户提问一个参数。如果用户提供的信息不全，你需要反问他，让他提供没有提供的参数。如果参数收集完成，你要说：我已了解您的购买意向，请稍等。""",
    }
]

assistant_output = "欢迎光临阿里云百炼手机商店，您需要购买什么尺寸的手机呢？"
print(f"模型输出：{assistant_output}\n")
while "我已了解您的购买意向" not in assistant_output:
    user_input = input("请输入：")
    # 将用户问题信息添加到messages列表中
    messages.append({"role": "user", "content": user_input})
    assistant_output = get_response(messages).output.choices[0].message.content
    # 将大模型的回复信息添加到messages列表中
    messages.append({"role": "assistant", "content": assistant_output})
    print(f"模型输出：{assistant_output}")
    print("\n")
```

#### Java

```
import java.util.ArrayList;
import java.util.List;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.util.Scanner;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {
        Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
    }
    public static GenerationParam createGenerationParam(List<Message> messages) {
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                .model("qwen-plus")
                .messages(messages)
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
    }
    public static GenerationResult callGenerationWithMessages(GenerationParam param) throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            List<Message> messages = new ArrayList<>();
            messages.add(createMessage(Role.SYSTEM, "You are a helpful assistant."));
            for (int i = 0; i < 3;i++) {
                Scanner scanner = new Scanner(System.in);
                System.out.print("请输入：");
                String userInput = scanner.nextLine();
                if ("exit".equalsIgnoreCase(userInput)) {
                    break;
                }
                messages.add(createMessage(Role.USER, userInput));
                GenerationParam param = createGenerationParam(messages);
                GenerationResult result = callGenerationWithMessages(param);
                System.out.println("模型输出："+result.getOutput().getChoices().get(0).getMessage().getContent());
                messages.add(result.getOutput().getChoices().get(0).getMessage());
            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            e.printStackTrace();
        }
        System.exit(0);
    }
    private static Message createMessage(Role role, String content) {
        return Message.builder().role(role.getValue()).content(content).build();
    }
}
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "你好"
            },
            {
                "role": "assistant",
                "content": "你好啊，我是通义千问。"
            },
            {
                "role": "user",
                "content": "你有哪些技能？"
            }
        ]
    }
}'
```

## 多模态模型的多轮对话

多模态模型支持在对话中加入图片、音频等内容，其多轮对话的实现方式与文本模型主要有以下不同：

-   **用户消息（user message）的构造方式**：多模态模型的用户消息不仅包含文本，还包含图片、音频等多模态信息。
-   **DashScope SDK接口：**使用 DashScope Python SDK 时，需调用 `MultiModalConversation` 接口；如需异步调用，请使用`AioMultiModalConversation`接口。使用DashScope Java SDK 时，需调用 `MultiModalConversation` 类。

> 多模态模型请参见：[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)、[界面交互](raw/model-user-guide/model-experience/text-generation-model/specialized-models/gui-automation.md)、[Kimi](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/kimi-api.md)。`Qwen-Omni`的实现方法请参见[非实时（Qwen-Omni）](raw/model-user-guide/model-experience/omni-modal/qwen-omni.md)。Qwen-VL-OCR、Qwen3-Omni-Captioner是为特定单轮任务设计的模型，不支持多轮对话。

#### OpenAI兼容

Python

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
messages = [
        {
        "role": "user",
        "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
                },
            },
            {"type": "text", "text": "请问图片展现了有哪些商品？"},
        ],
    }
]

completion = client.chat.completions.create(
    model="qwen3-vl-plus",  # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages,
    )

print(f"第一轮输出：{completion.choices[0].message.content}")

assistant_message = completion.choices[0].message
messages.append(assistant_message.model_dump())
messages.append({
        "role": "user",
        "content": [
        {
            "type": "text",
            "text": "它们属于什么风格？"
        }
        ]
    })
completion = client.chat.completions.create(
    model="qwen3-vl-plus",
    messages=messages,
    )

print(f"第二轮输出：{completion.choices[0].message.content}")
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
       // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

let messages = [
    {
        role: "user",
	content: [
        { type: "image_url", image_url: { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png" } },
        { type: "text", text: "请问图片展现了有哪些商品？" },
    ]
}]
async function main() {
    let response = await openai.chat.completions.create({
        model: "qwen3-vl-plus",  // 可按需更换为其它多模态模型，并修改相应的 messages
        messages: messages
    });
    console.log(`第一轮输出：${response.choices[0].message.content}`);
    messages.push(response.choices[0].message);
    messages.push({"role": "user", "content": "它们属于什么风格？"});
    response = await openai.chat.completions.create({
        model: "qwen3-vl-plus",
        messages: messages
    });
    console.log(`第二轮输出：${response.choices[0].message.content}`);
}

main()
```

curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen3-vl-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "image_url",
          "image_url": {
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
          }
        },
        {
          "type": "text",
          "text": "请问图片展现了有哪些商品？"
        }
      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "图片展示了三件商品：一件浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "它们属于什么风格？"
        }
      ]
    }
  ]
}'
```

#### DashScope

#### Python

```
import os
import dashscope
from dashscope import MultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {
                "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
            },
            {"text": "请问图片展现了有哪些商品？"},
        ],
    }
]
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3-vl-plus',   # 可按需更换为其它多模态模型，并修改相应的 messages
    messages=messages)
print(f"模型第一轮输出：{response.output.choices[0].message.content[0]['text']}")

messages.append(response['output']['choices'][0]['message'])
user_msg = {"role": "user", "content": [{"text": "它们属于什么风格？"}]}
messages.append(user_msg)
response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen3-vl-plus',
    messages=messages)

print(f"模型第二轮输出：{response.output.choices[0].message.content[0]['text']}")
```

### 异步调用

如需在异步环境中使用多模态多轮对话，请使用 `AioMultiModalConversation` 接口：

```
import asyncio
import os
import dashscope
from dashscope import AioMultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

async def main():
    messages = [
        {
            "role": "user",
            "content": [
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"},
                {"text": "请问图片展现了有哪些商品？"},
            ],
        }
    ]
    response = await AioMultiModalConversation.call(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3-vl-plus',  # 可按需更换为其它多模态模型，并修改相应的 messages
        messages=messages)
    print(f"模型第一轮输出：{response.output.choices[0].message.content[0]['text']}")

    messages.append(response['output']['choices'][0]['message'])
    user_msg = {"role": "user", "content": [{"text": "它们属于什么风格？"}]}
    messages.append(user_msg)
    response = await AioMultiModalConversation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3-vl-plus',
        messages=messages)
    print(f"模型第二轮输出：{response.output.choices[0].message.content[0]['text']}")

asyncio.run(main())
```

#### Java

```
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
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
   static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static final String modelName = "qwen3-vl-plus";  // 可按需更换为其它多模态模型，并修改相应的 messages
    public static void MultiRoundConversationCall() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"),
                        Collections.singletonMap("text", "请问图片展现了有哪些商品？"))).build();
        List<MultiModalMessage> messages = new ArrayList<>();
        messages.add(userMessage);
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model(modelName)
                .messages(messages)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println("第一轮输出："+result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));        // add the result to conversation
        messages.add(result.getOutput().getChoices().get(0).getMessage());
        MultiModalMessage msg = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "它们属于什么风格？"))).build();
        messages.add(msg);
        param.setMessages((List)messages);
        result = conv.call(param);
        System.out.println("第二轮输出："+result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));    }

    public static void main(String[] args) {
        try {
            MultiRoundConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-vl-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"},
                    {"text": "请问图片展现了有哪些商品？"}
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {"text": "图片展示了三件商品：一件浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"text": "它们属于什么风格？"}
                ]
            }
        ]
    }
}'
```

## 思考模型的多轮对话

思考模型返回`reasoning_content`（思考过程）与`content`（回复内容）两个字段。更新 messages 数组时，仅保留`content`字段，忽略`reasoning_content`字段。

```
[
    {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"},
    {"role": "assistant", "content": "我推荐《xxx》，这是一部经典的科幻作品。"}, # 添加上下文时请勿添加reasoning_content字段
    {"role": "user", "content": "这部电影的导演是谁？"}
]
```

> 思考模型详情参见：[深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)、[图像与视频理解](raw/model-user-guide/model-experience/vision-model/vision.md)、[视觉推理](raw/model-user-guide/model-experience/vision-model/visual-reasoning.md)。

> Qwen3-Omni-Flash（思考模式）实现多轮对话请参见[全模态](https://help.aliyun.com/zh/model-studio/qwen-omni#4d96cc766ehhi)。

#### OpenAI兼容

#### Python

### 示例代码

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key = os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

messages = []
conversation_idx = 1
while True:
    reasoning_content = ""  # 定义完整思考过程
    answer_content = ""     # 定义完整回复
    is_answering = False   # 判断是否结束思考过程并开始回复
    print("="*20+f"第{conversation_idx}轮对话"+"="*20)
    conversation_idx += 1
    user_input = input("请输入你的消息（输入 exit 结束对话）：")
    # 输入 exit 结束多轮对话，避免循环无法退出
    if user_input.strip().lower() == "exit":
        print("对话已结束。")
        break
    user_msg = {"role": "user", "content": user_input}
    messages.append(user_msg)
    # 创建聊天完成请求
    completion = client.chat.completions.create(
        # 您可以按需更换为其它深度思考模型
        model="qwen3.8-max",
        messages=messages,
        extra_body={"enable_thinking": True},
        stream=True,
        # stream_options={
        #     "include_usage": True
        # }
    )
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    for chunk in completion:
        # 如果chunk.choices为空，则打印usage
        if not chunk.choices:
            print("\nUsage:")
            print(chunk.usage)
        else:
            delta = chunk.choices[0].delta
            # 打印思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
                print(delta.reasoning_content, end='', flush=True)
                reasoning_content += delta.reasoning_content
            else:
                # 开始回复
                if delta.content != "" and is_answering is False:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                    is_answering = True
                # 打印回复过程
                print(delta.content, end='', flush=True)
                answer_content += delta.content
    # 将模型回复的content添加到上下文中
    messages.append({"role": "assistant", "content": answer_content})
    print("\n")
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";
import process from 'process';
import readline from 'readline/promises';

// 初始化 readline 接口
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// 初始化 openai 客户端
const openai = new OpenAI({
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;
let messages = [];
let conversationIdx = 1;

async function main() {
    while (true) {
        console.log("=".repeat(20) + `第${conversationIdx}轮对话` + "=".repeat(20));
        conversationIdx++;

        // 读取用户输入
        const userInput = await rl.question("请输入你的消息（输入 exit 结束对话）：");
        // 输入 exit 结束多轮对话，避免循环无法退出
        if (userInput.trim().toLowerCase() === "exit") {
            console.log("对话已结束。");
            rl.close();
            break;
        }
        messages.push({ role: 'user', content: userInput });

        // 重置状态
        reasoningContent = '';
        answerContent = '';
        isAnswering = false;

        try {
            const stream = await openai.chat.completions.create({
                // 您可以按需更换为其它深度思考模型
                model: 'qwen3.8-max',
                messages: messages,
                enable_thinking: true,
                stream: true,
                // stream_options:{
                //     include_usage: true
                // }
            });

            console.log("\n" + "=".repeat(20) + "思考过程" + "=".repeat(20) + "\n");

            for await (const chunk of stream) {
                if (!chunk.choices?.length) {
                    console.log('\nUsage:');
                    console.log(chunk.usage);
                    continue;
                }

                const delta = chunk.choices[0].delta;

                // 处理思考过程
                if (delta.reasoning_content) {
                    process.stdout.write(delta.reasoning_content);
                    reasoningContent += delta.reasoning_content;
                }

                // 处理正式回复
                if (delta.content) {
                    if (!isAnswering) {
                        console.log('\n' + "=".repeat(20) + "完整回复" + "=".repeat(20) + "\n");
                        isAnswering = true;
                    }
                    process.stdout.write(delta.content);
                    answerContent += delta.content;
                }
            }

            // 将完整回复加入消息历史
            messages.push({ role: 'assistant', content: answerContent });
            console.log("\n");

        } catch (error) {
            console.error('Error:', error);
        }
    }
}

// 启动程序
main().catch(console.error);
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "messages": [
        {
            "role": "user",
            "content": "你好"
        },
        {
            "role": "assistant",
            "content": "你好！很高兴见到你，有什么我可以帮忙的吗？"
        },
        {
            "role": "user",
            "content": "你是谁？"
        }
    ],
    "stream": true,
    "stream_options": {
        "include_usage": true
    },
    "enable_thinking": true
}'
```

#### DashScope

#### Python

### 示例代码

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = []
conversation_idx = 1
while True:
    print("=" * 20 + f"第{conversation_idx}轮对话" + "=" * 20)
    conversation_idx += 1
    user_input = input("请输入你的消息（输入 exit 结束对话）：")
    # 输入 exit 结束多轮对话，避免循环无法退出
    if user_input.strip().lower() == "exit":
        print("对话已结束。")
        break
    user_msg = {"role": "user", "content": [{"text": user_input}]}
    messages.append(user_msg)
    response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
         # 此处以qwen3.8-max为例，可按需更换为其它深度思考模型
        model="qwen3.8-max",
        messages=messages,
        enable_thinking=True,
        stream=True,
        incremental_output=True
    )
    # 定义完整思考过程
    reasoning_content = ""
    # 定义完整回复
    answer_content = ""
    # 判断是否结束思考过程并开始回复
    is_answering = False
    print("=" * 20 + "思考过程" + "=" * 20)
    for chunk in response:
        # 获取当前chunk的内容
        content_text = ""
        raw_content = chunk.output.choices[0].message.content
        if isinstance(raw_content, list) and raw_content:
            content_text = raw_content[0].get("text", "")
        elif isinstance(raw_content, str):
            content_text = raw_content
        reasoning_text = chunk.output.choices[0].message.reasoning_content or ""
        # 如果思考过程与回复皆为空，则忽略
        if content_text == "" and reasoning_text == "":
            pass
        else:
            # 如果当前为思考过程
            if reasoning_text != "" and content_text == "":
                print(reasoning_text, end="",flush=True)
                reasoning_content += reasoning_text
            # 如果当前为回复
            elif content_text != "":
                if not is_answering:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                    is_answering = True
                print(content_text, end="",flush=True)
                answer_content += content_text
    # 将模型回复的content添加到上下文中
    messages.append({"role": "assistant", "content": [{"text": answer_content}]})
    print("\n")
    # 如果您需要打印完整思考过程与完整回复，请将以下代码解除注释后运行
    # print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
    # print(f"{reasoning_content}")
    # print("=" * 20 + "完整回复" + "=" * 20 + "\n")
    # print(f"{answer_content}")
```

#### Java

### 示例代码

```
// dashscope SDK的版本 >= 2.19.4
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import java.util.Collections;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;
import java.lang.System;
import java.util.List;
import java.util.Map;

public class Main {
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean isFirstPrint = true;
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    private static void handleMultiModalConversationResult(MultiModalConversationResult message) {
        if (message != null && message.getOutput() != null
            && message.getOutput().getChoices() != null
            && !message.getOutput().getChoices().isEmpty()
            && message.getOutput().getChoices().get(0) != null
            && message.getOutput().getChoices().get(0).getMessage() != null) {

            String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
            List<Map<String, Object>> contentList = message.getOutput().getChoices().get(0).getMessage().getContent();
            String content = "";
            if (contentList != null && !contentList.isEmpty()) {
                Object textObj = contentList.get(0).get("text");
                if (textObj != null) {
                    content = textObj.toString();
                }
            }

            if (reasoning != null && !reasoning.isEmpty()) {
                reasoningContent.append(reasoning);
                if (isFirstPrint) {
                    System.out.println("====================思考过程====================");
                    isFirstPrint = false;
                }
                System.out.print(reasoning);
            }

            if (content != null && !content.isEmpty()) {
                finalContent.append(content);
                if (!isFirstPrint) {
                    System.out.println("\n====================完整回复====================");
                    isFirstPrint = true;
                }
                System.out.print(content);
            }
        }
    }

    private static MultiModalConversationParam buildMultiModalConversationParam(List<MultiModalMessage> messages) {
        return MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 此处以 qwen3.8-max 为例，可按需更换模型名称
                .model("qwen3.8-max")
                .enableThinking(true)
                .messages(messages)
                .incrementalOutput(true)
                .build();
    }

    public static void streamCallWithMessage(MultiModalConversation conv, List<MultiModalMessage> messages)
            throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {
        MultiModalConversationParam param = buildMultiModalConversationParam(messages);
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.doOnError(throwable -> logger.error("Error occurred in stream processing: {}", throwable.getMessage(), throwable))
              .blockingForEach(Main::handleMultiModalConversationResult);
    }

    public static void main(String[] args) {
        try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg1 = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("text", "你好")))
                    .build();
            MultiModalMessage assistantMsg = MultiModalMessage.builder()
                    .role(Role.ASSISTANT.getValue())
                    .content(Arrays.asList(Collections.singletonMap("text", "你好！很高兴见到你，有什么我可以帮忙的吗？")))
                    .build();
            MultiModalMessage userMsg2 = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(Collections.singletonMap("text", "你是谁")))
                    .build();
            List<MultiModalMessage> messages = Arrays.asList(userMsg1, assistantMsg, userMsg2);
            streamCallWithMessage(conv, messages);
        } catch (ApiException | NoApiKeyException | InputRequiredException | UploadFileException e) {
            logger.error("An exception occurred: {}", e.getMessage(), e);
        } catch (Exception e) {
            logger.error("Unexpected error occurred: {}", e.getMessage(), e);
        } finally {
            // 确保程序正常退出
            System.exit(0);
        }
    }
}
```

#### HTTP

### 示例代码

#### curl

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
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
                "content": [{"text": "你好"}]
            },
            {
                "role": "assistant",
                "content": [{"text": "你好！很高兴见到你，有什么我可以帮忙的吗？"}]
            },
            {
                "role": "user",
                "content": [{"text": "你是谁？"}]
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message"
    }
}'
```

## 应用于生产环境

多轮对话会带来巨大的 Token 消耗，且容易超出大模型上下文最大长度导致报错。以下策略可帮助您有效管理上下文与控制成本。

### 1\. 上下文管理

`messages` 数组会随对话轮次增加而变长，最终可能超出模型的 Token 限制。建议参考以下内容，在对话过程中管理上下文长度。

#### 1.1. 上下文截断

当对话历史过长时，保留最近的 N 轮对话历史。该方式实现简单，但会丢失较早的对话信息。

#### 1.2. 滚动摘要

为了在不丢失核心信息的前提下动态压缩对话历史，控制上下文长度，可随着对话的进行对上下文进行摘要：

a. 对话历史达到一定长度（如上下文长度最大值的 70%）时，将对话历史中较早的部分（如前一半）提取出来，发起独立 API 调用使大模型对这部分内容生成“记忆摘要”；

b. 构建下一次请求时，用“记忆摘要”替换冗长的对话历史，并拼接最近的几轮对话。

#### 1.3. 向量化召回

滚动摘要会丢失部分信息，为了使模型可以从海量对话历史中“回忆”起相关信息，可将对话管理从“线性传递”转变为“按需检索”：

a. 每轮对话结束后，将该轮对话存入向量数据库；

b. 用户提问时，通过相似度检索相关对话记录；

c. 将检索到的对话记录与最近的用户输入拼接后输入大模型。

### 2\. 成本控制

输入 Token 数会随着对话轮数增加，显著增加使用成本，以下成本管理策略供您参考。

#### 2.1. 减少输入 Token

通过上文介绍的上下文管理策略减少输入 Token，降低成本。

#### 2.2. 使用支持上下文缓存的模型

发起多轮对话请求时，`messages` 部分会重复计算并计费。阿里云百炼对`qwen-max`、`qwen3.8-max`等模型提供了[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)功能，可以降低使用成本并提升响应速度，建议优先使用支持上下文缓存的模型。

> 上下文缓存功能自动开启，无需修改代码。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
