# 翻译能力（Qwen-MT）

Qwen-MT模型是基于Qwen3模型优化的机器翻译大语言模型，支持92个语种（包括中、英、日、韩、法、西、德、泰、印尼、越、阿等）互译，且提供了术语干预、领域提示、记忆库等能力，提升模型在复杂应用场景下的翻译效果。

## 工作方式

1.  **传入待翻译内容**：`messages` 数组中有且仅有一个 `role` 为 `user` 的消息，其 `content` 为待翻译文本。
    
2.  **设置语种**：参考[支持的语言](https://help.aliyun.com/zh/model-studio/machine-translation#038d2865bbydc)，在 `translation_options` 中设置源语种 (`source_lang`) 和目标语种 (`target_lang`)。若需自动检测源语种，可将 `source_lang` 设为 `auto`。
    
    > 指明源语种有利于提升翻译准确率。
    
    > Qwen-MT 模型也支持通过 [自定义提示词](https://help.aliyun.com/zh/model-studio/machine-translation#42ac4e67d6bnf) 设置语种。
    

以下以 OpenAI 兼容和 DashScope 的 Python SDK为例，演示 Qwen-MT 的基本调用方式。所有翻译配置均通过 `translation_options` 参数传入。

OpenAI 兼容

```
# 导入依赖与创建客户端...
completion = client.chat.completions.create(
    model="qwen-mt-flash",    # 选择模型
    # messages 有且仅有一个 role 为 user 的消息，其 content 为待翻译文本
    messages=[{"role": "user", "content": "我看到这个视频后没有笑"}],
    # 由于 translation_options 非 OpenAI 标准参数，需要通过 extra_body 传入
    extra_body={"translation_options": {"source_lang": "Chinese", "target_lang": "English"}},
)
```

DashScope

```
# 导入依赖...
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-mt-flash",  # 选择模型
    messages=[{"role": "user", "content": "我看到这个视频后没有笑"}],  # messages: role为user, content为待翻译文本
    translation_options={"source_lang": "Chinese", "target_lang": "English"},  # 配置翻译选项
    result_format="message"
)
```

OpenAI 兼容

```
import os
from openai import OpenAI
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为新加坡地域URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-mt-flash",
    # messages 有且仅有一个 role 为 user 的消息，其 content 为待翻译文本
    messages=[
        {
            "role": "user",
            "content": "我看到这个视频后没有笑"
        }
    ],
    # 由于 translation_options 非 OpenAI 标准参数，需要通过 extra_body 传入
    extra_body={
        # 配置翻译选项
        "translation_options": {
            "source_lang": "Chinese",
            "target_lang": "English"
        }
    },
)
```

DashScope

```
import os
import dashscope
# 以下为新加坡地域URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = 'https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1'

response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-mt-flash",
    # messages 有且仅有一个 role 为 user 的消息，其 content 为待翻译文本
    messages=[
        {
            "role": "user",
            "content": "我看到这个视频后没有笑"
        }
    ],
    # 配置翻译选项
    translation_options={
        "source_lang": "auto",
        "target_lang": "English",
    },
    result_format="message"
)
print(response.output.choices[0].message.content)
```

通过 `translation_options`也可实现[术语干预](https://help.aliyun.com/zh/model-studio/machine-translation#2bf54a5ab5voe)、[翻译记忆](https://help.aliyun.com/zh/model-studio/machine-translation#17e15234e7gfp)、[领域提示](https://help.aliyun.com/zh/model-studio/machine-translation#4af23a31db7lf)等翻译定制功能。

**使用限制：**

-   **仅支持单轮翻译**：模型专为翻译任务设计，不支持多轮对话。
-   **不支持设置 System Message**：不支持通过 `system` 角色的消息来设定全局行为。翻译配置通过 `translation_options` 中定义。

## 模型选型

-   **通用场景**首选 `qwen-mt-flash`，在翻译质量、速度和成本之间取得最佳平衡，支持增量流式输出。
-   **最高翻译质量**（专业文献、正式文书）选 `qwen-mt-plus`。
-   **最低延迟**（实时聊天等简单场景）选 `qwen-mt-lite`。

各模型详细对比如下：

**模型**

**推荐场景**

**效果**

**速度**

**成本**

**支持的语言**

**支持增量流式输出**

qwen-mt-plus

专业领域、正式文书、论文、技术报告等对译文质量要求高的场景

最好

标准

较高

92种

不支持

qwen-mt-flash

**通用首选**，适用于网站/App内容、商品描述、日常沟通、博客文章等场景

较好

较快

较低

92种

支持

> qwen-mt-turbo

turbo模型后续不再更新，建议选用效果与功能均更优的flash模型

良好

较快

较低

92种

不支持

qwen-mt-lite

实时聊天、弹幕翻译等对延迟敏感的简单场景

基础

最快

最低

31种

支持

各模式支持模型的上下文、价格等信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)；并发限流条件请参考[限流](https://help.aliyun.com/zh/model-studio/rate-limit#19090eae8arxa)；翻译模型计费详情请参见[模型调用价格](https://help.aliyun.com/zh/model-studio/model-pricing#d4d9ec4242oj7)。

## 快速开始

以下示例将 `“我看到这个视频后没有笑”` 翻译为英文。

您需要已[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过OpenAI SDK或DashScope SDK进行调用，还需要[安装SDK](raw/model-api-reference/preparations/install-sdk.md)。请将示例代码中的 `DASHSCOPE_API_HOST` 替换为获取的 API Host。

#### OpenAI兼容

**请求示例**

python

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
messages = [
    {
        "role": "user",
        "content": "我看到这个视频后没有笑"
    }
]
translation_options = {
    "source_lang": "auto",
    "target_lang": "English"
}

completion = client.chat.completions.create(
    model="qwen-mt-flash",
    messages=messages,
    extra_body={
        "translation_options": translation_options
    }
)
print(completion.choices[0].message.content)
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-mt-flash",
    "messages": [{"role": "user", "content": "我看到这个视频后没有笑"}],
    "translation_options": {
      "source_lang": "auto",
      "target_lang": "English"
      }
}'
```

**响应示例**
```
I didn't laugh after watching this video.
```

#### DashScope

**请求示例**

**重要**DashScope Java SDK版本需要不低于 2.20.6。

python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [
    {
        "role": "user",
        "content": "我看到这个视频后没有笑"
    }
]
translation_options = {
    "source_lang": "auto",
    "target_lang": "English",
}
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-mt-flash",
    messages=messages,
    result_format='message',
    translation_options=translation_options
)
print(response.output.choices[0].message.content)
```

java

```
// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("我看到这个视频后没有笑")
                .build();
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang("auto")
                .targetLang("English")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-mt-flash")
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
            e.printStackTrace();
        } finally {
            System.exit(0);
        }
    }
}
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "qwen-mt-flash",
  "input": {
    "messages": [
      {
        "content": "我看到这个视频后没有笑",
        "role": "user"
      }
    ]
  },
  "parameters": {
    "translation_options": {
      "source_lang": "auto",
      "target_lang": "English"
    }
  }
}'
```

**响应示例**
```
I didn't laugh after watching this video.
```

## 流式输出

流式输出可实时返回翻译内容，减少用户等待时间。`qwen-mt-flash` 和 `qwen-mt-lite` 支持增量流式输出，通过 `incremental_output` 参数开启，每次仅返回新生成的内容。`qwen-mt-plus` 和 `qwen-mt-turbo` 仅支持非增量流式输出，每次返回当前已生成的完整序列。详情请参见[流式输出](raw/model-user-guide/model-experience/text-generation-model/stream.md)。

#### OpenAI兼容

**请求示例**

python

```
import os
from openai import OpenAI

client = OpenAI(
    # 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
messages = [{"role": "user", "content": "我看到这个视频后没有笑"}]
translation_options = {"source_lang": "Chinese", "target_lang": "English"}

completion = client.chat.completions.create(
    model="qwen-mt-flash",
    messages=messages,
    stream=True,
    stream_options={"include_usage": True},
    extra_body={"translation_options": translation_options},
)
for chunk in completion:
    if chunk.choices:
        content = chunk.choices[0].delta.content or ""
        print(content, end="", flush=True)
    else:
        print("\n"+"="*20+"usage 消耗"+"="*20)
        print(chunk.usage)
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-mt-flash",
    "messages": [{"role": "user", "content": "我看到这个视频后没有笑"}],
    "stream": true,
    "translation_options": {
      "source_lang": "Chinese",
      "target_lang": "English"
      }
}'
```

**响应示例**
```
I didn’t laugh after watching this video.
====================usage 消耗====================
CompletionUsage(completion_tokens=9, prompt_tokens=56, total_tokens=65, completion_tokens_details=None, prompt_tokens_details=None)
```

#### DashScope

**请求示例**

python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [
    {
        "role": "user",
        "content": "我看到这个视频后没有笑"
    }
]
translation_options = {
    "source_lang": "Chinese",
    "target_lang": "English",
}
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-mt-flash",
    messages=messages,
    result_format='message',
    stream=True,
    # 推荐设置incremental_output为True以获取增量输出，当前仅qwen-mt-flash和qwen-mt-lite支持
    incremental_output=True,
    translation_options=translation_options
)
for chunk in response:
    print(chunk.output.choices[0].message.content, end="", flush=True)
```

java

```
// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import java.util.Arrays;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import io.reactivex.Flowable;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static void handleGenerationResult(GenerationResult message) {
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();
        System.out.print(content);
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang("auto")
                .targetLang("English")
                .build();
        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-mt-flash")
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                // 开启增量输出，当前仅qwen-mt-flash和qwen-mt-lite支持
                .incrementalOutput(true)
                .messages(Arrays.asList(userMsg))
                .build();
    }
    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("我看到这个视频后没有笑").build();
            streamCallWithMessage(gen, userMsg);
        } catch (ApiException | NoApiKeyException | InputRequiredException  e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
  "model": "qwen-mt-flash",
  "input": {
    "messages": [
      {
        "content": "我看到这个视频后没有笑",
        "role": "user"
      }
    ]
  },
  "parameters": {
    "translation_options": {
      "source_lang": "Chinese",
      "target_lang": "English"
    },
    "incremental_output": true
  }
}'
```

**响应示例**
```
I didn't laugh after watching this video.
```

> qwen-mt-plus、qwen-mt-turbo模型不支持增量式流式输出。

## 提升翻译效果

标准翻译能满足日常沟通需求，但在专业场景中可能出现以下问题：

-   **术语不统一**：产品名或行业术语翻译错误。
-   **风格不匹配**：译文风格不符合法律、营销等特定领域的规范。

以下三种方式可针对性地解决这些问题：

### 术语干预

当文本包含品牌名、产品名或专业术语时，为保证翻译的准确性和一致性，可通过 `terms` 字段提供一个术语表，引导模型参考术语表进行翻译。

使用步骤：

1.  **定义术语**
    
    创建JSON数组，赋值给 `terms` 字段。每个对象代表一条术语：
    

```
{
    "source": "术语",
    "target": "提前翻译好的术语"
}
```

2.  **传入术语**
    
    通过 `translation_options` 参数传入 `terms` 数组。
    

#### OpenAI兼容

**请求示例**

python

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

messages = [
    {
        "role": "user",
        "content": "而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。"
    }
]

# --- 第一次请求：不使用 terms 参数 ---
print("--- [不使用 terms] 的翻译结果 ---")
translation_options_without_terms = {
    "source_lang": "auto",
    "target_lang": "English"
}

completion_without_terms = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=messages,
    extra_body={
        "translation_options": translation_options_without_terms
    }
)
print(completion_without_terms.choices[0].message.content)

print("\n" + "="*50 + "\n") # 用于分割，方便对比

# --- 第二次请求：使用 terms 参数 ---
print("--- [使用 terms] 的翻译结果 ---")
translation_options_with_terms = {
    "source_lang": "Chinese",
    "target_lang": "English",
    "terms": [
        {
            "source": "生物传感器",
            "target": "biological sensor"
        },
        {
            "source": "身体健康状况",
            "target": "health status of the body"
        }
    ]
}

completion_with_terms = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=messages,
    extra_body={
        "translation_options": translation_options_with_terms
    }
)
print(completion_with_terms.choices[0].message.content)
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "qwen-mt-plus",
  "messages": [
    {
      "role": "user",
      "content": "而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。"
    }
  ],
  "translation_options": {
    "source_lang": "Chinese",
    "target_lang": "English",
    "terms": [
      {
        "source": "生物传感器",
        "target": "biological sensor"
      },
      {
        "source": "身体健康状况",
        "target": "health status of the body"
      }
    ]
  }
}'
```

**响应示例**

加入术语后，翻译结果与传入的术语一致：“**生物传感器**”（biological sensor）和“**身体健康状况**”（the health status of the body）。

```
--- [不使用 terms] 的翻译结果 ---
This set of biosensors uses graphene, a new material, whose target substance is chemical elements. Its sensitive "sense of smell" allows it to more deeply and accurately reflect one's health condition.

==================================================

--- [使用 terms] 的翻译结果 ---
This biological sensor uses a new material called graphene. Its target is chemical elements, and its sensitive "sense of smell" enables it to reflect the health status of the body more deeply and accurately.
```

#### DashScope

**请求示例**

python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [
    {
        "role": "user",
        "content": "而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。"
    }
]
translation_options = {
    "source_lang": "Chinese",
    "target_lang": "English",
    "terms": [
        {
            "source": "生物传感器",
            "target": "biological sensor"
        },
        {
            "source": "身体健康状况",
            "target": "health status of the body"
        }
    ]
}
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-mt-plus",
    messages=messages,
    result_format='message',
    translation_options=translation_options
)
print(response.output.choices[0].message.content)
```

java

```
// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.aigc.generation.TranslationOptions.Term;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。")
                .build();
        Term term1 = Term.builder()
                .source("生物传感器")
                .target("biological sensor")
                .build();
        Term term2 = Term.builder()
                .source("身体健康状况")
                .target("health status of the body")
                .build();
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang("auto")
                .targetLang("English")
                .terms(Arrays.asList(term1, term2))
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-mt-flash")
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
        }
        System.exit(0);
    }
}
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen-mt-plus",
  "input": {
    "messages": [
      {
        "content": "而这套生物传感器运用了石墨烯这种新型材料，它的目标物是化学元素，敏锐的“嗅觉”让它能更深度、准确地体现身体健康状况。",
        "role": "user"
      }
    ]
  },
  "parameters": {
    "translation_options": {
      "source_lang": "Chinese",
      "target_lang": "English",
      "terms": [
        {
          "source": "生物传感器",
          "target": "biological sensor"
        },
        {
          "source": "身体健康状况",
          "target": "health status of the body"
        }
      ]
    }
  }
}'
```

**响应示例**
```
This biological sensor uses graphene, a new material, and its target is chemical elements. Its sensitive "nose" can more deeply and accurately reflect the health status of the human body.
```

### 翻译记忆

需要模型遵循特定翻译风格或句式时，可通过 `tm_list` 字段提供"源文-译文"句对作为参考。模型将在当次翻译任务中模仿这些示例的风格，适合维护大型文档集的术语一致性，或沿用企业已有的写作规范。

1.  **定义翻译记忆**
    
    创建JSON数组赋值给 `tm_list`，每个对象包含源语句与对应译文：
    

```
{
    "source": "源语句",
    "target": "已翻译的语句"
}
```

2.  **传入翻译记忆**
    
    通过 `translation_options` 参数传入翻译记忆数组。
    

可参考以下代码实现翻译记忆功能。

#### OpenAI兼容

**请求示例**

python

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
messages = [
    {
        "role": "user",
        "content": "通过如下命令可以看出安装thrift的版本信息；"
    }
]
translation_options = {
    "source_lang": "Chinese",
    "target_lang": "English",
    "tm_list": [
        {
            "source": "您可以通过如下方式查看集群的内核版本信息:",
            "target": "You can use one of the following methods to query the engine version of a cluster:"
        },
        {
            "source": "我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;",
            "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."
        },
        {
            "source": "您可以通过PyPI来安装SDK,安装命令如下:",
            "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"
        }
    ]
}

completion = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=messages,
    extra_body={
        "translation_options": translation_options
    }
)
print(completion.choices[0].message.content)
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "qwen-mt-plus",
  "messages": [
    {
      "role": "user",
      "content": "通过如下命令可以看出安装thrift的版本信息；"
    }
  ],
  "translation_options": {
    "source_lang": "Chinese",
    "target_lang": "English",
    "tm_list":[
          {"source": "您可以通过如下方式查看集群的内核版本信息:", "target": "You can use one of the following methods to query the engine version of a cluster:"},
          {"source": "我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;", "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."},
          {"source": "您可以通过PyPI来安装SDK,安装命令如下:", "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"}
    ]
  }
}'
```

**响应示例**
```
You can run the following command to view the version of Thrift that is installed:
```

#### DashScope

**请求示例**

python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [
    {
        "role": "user",
        "content": "通过如下命令可以看出安装thrift的版本信息；"
    }
]
translation_options = {
    "source_lang": "Chinese",
    "target_lang": "English",
    "tm_list": [
        {
            "source": "您可以通过如下方式查看集群的内核版本信息:",
            "target": "You can use one of the following methods to query the engine version of a cluster:"
        },
        {
            "source": "我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;",
            "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."
        },
        {
            "source": "您可以通过PyPI来安装SDK,安装命令如下:",
            "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"
        }
    ]}
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-mt-plus",
    messages=messages,
    result_format='message',
    translation_options=translation_options
)
print(response.output.choices[0].message.content)
```

java

```
// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.aigc.generation.TranslationOptions.Tm;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("通过如下命令可以看出安装thrift的版本信息；")
                .build();
        Tm tm1 = Tm.builder()
                .source("您可以通过如下方式查看集群的内核版本信息:")
                .target("You can use one of the following methods to query the engine version of a cluster:")
                .build();
        Tm tm2 = Tm.builder()
                .source("我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;")
                .target("The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website.")
                .build();
        Tm tm3 = Tm.builder()
                .source("您可以通过PyPI来安装SDK,安装命令如下:")
                .target("You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:")
                .build();
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang("auto")
                .targetLang("English")
                .tmList(Arrays.asList(tm1, tm2, tm3))
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-mt-plus")
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
        }
        System.exit(0);
    }
}
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen-mt-plus",
  "input": {
    "messages": [
      {
        "content": "通过如下命令可以看出安装thrift的版本信息；",
        "role": "user"
      }
    ]
  },
  "parameters": {
    "translation_options": {
      "source_lang": "Chinese",
      "target_lang": "English",
      "tm_list":[
          {"source": "您可以通过如下方式查看集群的内核版本信息:", "target": "You can use one of the following methods to query the engine version of a cluster:"},
          {"source": "我们云HBase的thrift环境是0.9.0,所以建议客户端的版本也为 0.9.0,可以从这里下载thrift的0.9.0 版本,下载的源码包我们后面会用到,这里需要先安装thrift编译环境,对于源码安装可以参考thrift官网;", "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."},
          {"source": "您可以通过PyPI来安装SDK,安装命令如下:", "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"}
      ]
    }
  }
}'
```

**响应示例**
```
You can use the following commands to check the version information of thrift installed;
```

### 领域提示

若需要译文风格符合特定领域（如法律文书要求严肃正式，社交内容要求口语化），可通过 `translation_options` 参数传入领域提示语句。

**重要**领域提示语句当前只支持英文。

#### OpenAI兼容

**请求示例**

python

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
messages = [
    {
        "role": "user",
        "content": "第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。"
    }
]

# --- 第一次请求：不使用 domains 参数 ---
print("--- [不使用 domains] 的翻译结果 ---")
translation_options_without_domains = {
    "source_lang": "Chinese",
    "target_lang": "English",
}

completion_without_domains = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=messages,
    extra_body={
        "translation_options": translation_options_without_domains
    }
)
print(completion_without_domains.choices[0].message.content)

print("\n" + "="*50 + "\n") # 用于分割，方便对比

# --- 第二次请求：使用 domains 参数 (您的原始代码) ---
print("--- [使用 domains] 的翻译结果 ---")
translation_options_with_domains = {
    "source_lang": "Chinese",
    "target_lang": "English",
    "domains": "The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
}

completion_with_domains = client.chat.completions.create(
    model="qwen-mt-plus",
    messages=messages,
    extra_body={
        "translation_options": translation_options_with_domains
    }
)
print(completion_with_domains.choices[0].message.content)
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "qwen-mt-plus",
  "messages": [
    {
      "role": "user",
      "content": "第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。"
    }
  ],
  "translation_options": {
    "source_lang": "Chinese",
    "target_lang": "English",
    "domains": "The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
  }
}'
```

**响应示例**
```
--- [不使用 domains] 的翻译结果 ---
The second SELECT statement returns a number indicating how many rows the first SELECT statement would return without the LIMIT clause.

==================================================

--- [使用 domains] 的翻译结果 ---
The second SELECT statement returns a number that indicates how many rows the first SELECT statement would have returned if it had not included a LIMIT clause.
```

#### DashScope

**请求示例**

python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": "第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。"
    }
]
translation_options = {
    "source_lang": "Chinese",
    "target_lang": "English",
    "domains": "The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
}
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-mt-plus",
    messages=messages,
    result_format='message',
    translation_options=translation_options
)
print(response.output.choices[0].message.content)
```

java

```
// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.TranslationOptions;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。")
                .build();
        TranslationOptions options = TranslationOptions.builder()
                .sourceLang("auto")
                .targetLang("English")
                .domains("The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style.")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-mt-plus")
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .translationOptions(options)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
        }
        System.exit(0);
    }
}
```

bash

```
# ======= 重要提示 =======
# 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
  "model": "qwen-mt-plus",
  "input": {
    "messages": [
      {
        "content": "第二个SELECT语句返回一个数字，表示在没有LIMIT子句的情况下，第一个SELECT语句返回了多少行。",
        "role": "user"
      }
    ]
  },
  "parameters": {
    "translation_options": {
      "source_lang": "Chinese",
      "target_lang": "English",
      "domains": "The sentence is from Ali Cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
    }
  }
}'
```

**响应示例**
```
The second SELECT statement returns a number that indicates how many rows were returned by the first SELECT statement without a LIMIT clause.
```

## 自定义提示词

Qwen-MT 支持通过自定义提示词（如指定语种、风格）引导翻译。`translation_options` 参数与自定义提示词可同时传入，但当两者同时设置时，`translation_options` 中的配置（如 `target_lang`、`source_lang` 等）优先级高于自定义提示词中的对应设置，会覆盖自定义提示词中的语种或风格指定。

> 推荐优先使用 `translation_options` 参数配置翻译选项，以获得最佳翻译效果。

以下以法律领域的汉译英为例：

#### OpenAI兼容

python

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

prompt_template = """
# 角色
你是一名专业的法律翻译专家，精通中文和英文，尤其擅长处理商业合同和法律文件。

# 任务
我需要你将以下中文法律文本翻译成专业、精准、正式的英文。

# 翻译要求
1.  **忠实原文**：严格按照原文的含义和法律意图进行翻译，不得添加或删减信息。
2.  **术语精准**：使用英美法系（Common law）通用的标准法律术语。例如，“甲方”应翻译为 "Party A"，“乙方”应翻译为 "Party B"，“不可抗力”应翻译为 "Force Majeure"。
3.  **语气正式**：保持法律文件固有的严谨、客观和正式的语体。
4.  **语句清晰**：译文必须清晰、无歧义，符合英文法律文书的表达习惯。
5.  **格式保留**：保持原文的段落、编号和基本格式。

# 待翻译文本
{text_to_translate}
"""

# --- 2. 准备待翻译的法律文本 ---
chinese_legal_text = "本合同自双方签字盖章之日起生效，有效期为一年。"
final_prompt = prompt_template.format(text_to_translate=chinese_legal_text)

# --- 3. 构建messages ---
messages = [{"role": "user", "content": final_prompt}]

# --- 4. 发起API请求 ---
completion = client.chat.completions.create(model="qwen-mt-plus", messages=messages)

# --- 5. 打印模型的翻译结果 ---
translation_result = completion.choices[0].message.content
print(translation_result)
```

javascript

```
import OpenAI from 'openai';

const client = new OpenAI({
    // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
    // 各地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
});

const promptTemplate = `
# 角色
你是一名专业的法律翻译专家，精通中文和英文，尤其擅长处理商业合同和法律文件。

# 任务
我需要你将以下中文法律文本翻译成专业、精准、正式的英文。

# 翻译要求
1.  **忠实原文**：严格按照原文的含义和法律意图进行翻译，不得添加或删减信息。
2.  **术语精准**：使用英美法系（Common law）通用的标准法律术语。例如，“甲方”应翻译为 "Party A"，“乙方”应翻译为 "Party B"，“不可抗力”应翻译为 "Force Majeure"。
3.  **语气正式**：保持法律文件固有的严谨、客观和正式的语体。
4.  **语句清晰**：译文必须清晰、无歧义，符合英文法律文书的表达习惯。
5.  **格式保留**：保持原文的段落、编号和基本格式。

# 待翻译文本
{text_to_translate}
`;

const chineseLegalText = "本合同自双方签字盖章之日起生效，有效期为一年。";
const finalPrompt = promptTemplate.replace('{text_to_translate}', chineseLegalText);

const messages = [{"role": "user", "content": finalPrompt}];

async function main() {
    const completion = await client.chat.completions.create({
        model: "qwen-mt-plus",
        messages: messages
    });

    const translationResult = completion.choices[0].message.content;
    console.log(translationResult);
}

main();
```

**响应示例**
```
This Contract shall become effective from the date on which both parties sign and affix their seals, and its term of validity shall be one year.
```

#### DashScope

**请求示例**

python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

prompt_template = """
# 角色
你是一名专业的法律翻译专家，精通中文和英文，尤其擅长处理商业合同和法律文件。

# 任务
我需要你将以下中文法律文本翻译成专业、精准、正式的英文。

# 翻译要求
1.  **忠实原文**：严格按照原文的含义和法律意图进行翻译，不得添加或删减信息。
2.  **术语精准**：使用英美法系（Common law）通用的标准法律术语。例如，“甲方”应翻译为 "Party A"，“乙方”应翻译为 "Party B"，“不可抗力”应翻译为 "Force Majeure"。
3.  **语气正式**：保持法律文件固有的严谨、客观和正式的语体。
4.  **语句清晰**：译文必须清晰、无歧义，符合英文法律文书的表达习惯。
5.  **格式保留**：保持原文的段落、编号和基本格式。

# 待翻译文本
{text_to_translate}
"""

# --- 2. 准备待翻译的法律文本 ---
chinese_legal_text = "本合同自双方签字盖章之日起生效，有效期为一年。"
final_prompt = prompt_template.format(text_to_translate=chinese_legal_text)

# --- 3. 构建messages ---
messages = [
    {
        "role": "user",
        "content": final_prompt
    }
]

response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-mt-plus",
    messages=messages,
    result_format='message',
)
print(response.output.choices[0].message.content)
```

java

```
// DashScope SDK 版本需要不低于 2.20.6
import java.lang.System;
import java.util.Collections;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        String promptTemplate = "# 角色\n" +
                "你是一名专业的法律翻译专家，精通中文和英文，尤其擅长处理商业合同和法律文件。\n\n" +
                "# 任务\n" +
                "我需要你将以下中文法律文本翻译成专业、精准、正式的英文。\n\n" +
                "# 翻译要求\n" +
                "1.  **忠实原文**：严格按照原文的含义和法律意图进行翻译，不得添加或删减信息。\n" +
                "2.  **术语精准**：使用英美法系（Common law）通用的标准法律术语。例如，“甲方”应翻译为 \"Party A\"，“乙方”应翻译为 \"Party B\"，“不可抗力”应翻译为 \"Force Majeure\"。\n" +
                "3.  **语气正式**：保持法律文件固有的严谨、客观和正式的语体。\n" +
                "4.  **语句清晰**：译文必须清晰、无歧义，符合英文法律文书的表达习惯。\n" +
                "5.  **格式保留**：保持原文的段落、编号和基本格式。\n\n" +
                "# 待翻译文本\n" +
                "{text_to_translate}";

        String chineseLegalText = "本合同自双方签字盖章之日起生效，有效期为一年。";
        String finalPrompt = promptTemplate.replace("{text_to_translate}", chineseLegalText);

        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content(finalPrompt)
                .build();

        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-mt-plus")
                .messages(Collections.singletonList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
            e.printStackTrace();
        }
        }
    }
```

**响应示例**
```
This Contract shall become effective from the date on which both parties sign and affix their seals, and its term of validity shall be one year.
```

## 应用于生产环境

-   **控制输入 Token 数量**
    
    Qwen-MT 模型的输入 Token 上限为 8,192。输入内容较长时，可参考以下策略：
    
    -   **分段翻译**：按语义边界（段落或完整句子）分割长文本，而非按字符数截断，以保证上下文完整性，提升翻译质量。
    -   **仅传入最相关的参考内容**：术语、翻译记忆和领域提示都会作为输入 Token 拼入提示词。只传入与当前翻译任务直接相关的内容，避免使用大而泛的参考列表。
-   **根据场景设置**`source_lang`
    
    -   不确定源语种时（如多语言混杂的社交聊天场景），将 `source_lang` 设为 `auto`，模型自动识别语种。
    -   语种固定、准确度要求高的场景（如技术文档、操作手册），始终明确指定 `source_lang`，可有效提升翻译准确率。

## 常见问题

### Q：如何接入沉浸式翻译？

A：在最新版插件中添加**自定义翻译服务**，选择 **Qwen MT**。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4898705571/p996954.png)

填入API Key，模型下拉栏选择 `qwen-mt-plus` 或 `qwen-mt-flash`，在左侧边栏将 Qwen MT **设为默认**。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4898705571/p996956.png)

配置完成后，打开任意网页即可使用。以[Qwen3 Technical Report](https://arxiv.org/abs/2505.09388)为例，单击页面右侧插件小球即可开始翻译。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4898705571/p996982.png)

### Q：如何接入其它三方工具？

A：[Dify](https://cloud.dify.ai/apps)的最新版通义千问插件已支持 Qwen-MT 模型。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3414385571/p1000557.png)

> 其它三方工具是否支持以实际情况为准。

## 支持的语言

发起请求时，用下表中的**英文名**或**代码**指定语种。

> 当不确定源语种时，可为 `source_lang` 参数赋值 `auto` 以自动检测。

#### qwen-mt-plus/flash/turbo 支持的语言 (92种)

**语言**

**英文名**

**代码**

英语

English

en

简体中文

Chinese

zh

繁体中文

Traditional Chinese

zh\_tw

俄语

Russian

ru

日语

Japanese

ja

韩语

Korean

ko

西班牙语

Spanish

es

法语

French

fr

葡萄牙语

Portuguese

pt

德语

German

de

意大利语

Italian

it

泰语

Thai

th

越南语

Vietnamese

vi

印度尼西亚语

Indonesian

id

马来语

Malay

ms

阿拉伯语

Arabic

ar

印地语

Hindi

hi

希伯来语

Hebrew

he

缅甸语

Burmese

my

泰米尔语

Tamil

ta

乌尔都语

Urdu

ur

孟加拉语

Bengali

bn

波兰语

Polish

pl

荷兰语

Dutch

nl

罗马尼亚语

Romanian

ro

土耳其语

Turkish

tr

高棉语

Khmer

km

老挝语

Lao

lo

粤语

Cantonese

yue

捷克语

Czech

cs

希腊语

Greek

el

瑞典语

Swedish

sv

匈牙利语

Hungarian

hu

丹麦语

Danish

da

芬兰语

Finnish

fi

乌克兰语

Ukrainian

uk

保加利亚语

Bulgarian

bg

塞尔维亚语

Serbian

sr

泰卢固语

Telugu

te

南非荷兰语

Afrikaans

af

亚美尼亚语

Armenian

hy

阿萨姆语

Assamese

as

阿斯图里亚斯语

Asturian

ast

巴斯克语

Basque

eu

白俄罗斯语

Belarusian

be

波斯尼亚语

Bosnian

bs

加泰罗尼亚语

Catalan

ca

宿务语

Cebuano

ceb

克罗地亚语

Croatian

hr

埃及阿拉伯语

Egyptian Arabic

arz

爱沙尼亚语

Estonian

et

加利西亚语

Galician

gl

格鲁吉亚语

Georgian

ka

古吉拉特语

Gujarati

gu

冰岛语

Icelandic

is

爪哇语

Javanese

jv

卡纳达语

Kannada

kn

哈萨克语

Kazakh

kk

拉脱维亚语

Latvian

lv

立陶宛语

Lithuanian

lt

卢森堡语

Luxembourgish

lb

马其顿语

Macedonian

mk

马加希语

Maithili

mai

马耳他语

Maltese

mt

马拉地语

Marathi

mr

美索不达米亚阿拉伯语

Mesopotamian Arabic

acm

摩洛哥阿拉伯语

Moroccan Arabic

ary

内志阿拉伯语

Najdi Arabic

ars

尼泊尔语

Nepali

ne

北阿塞拜疆语

North Azerbaijani

az

北黎凡特阿拉伯语

North Levantine Arabic

apc

北乌兹别克语

Northern Uzbek

uz

书面语挪威语

Norwegian Bokmål

nb

新挪威语

Norwegian Nynorsk

nn

奥克语

Occitan

oc

奥里亚语

Odia

or

邦阿西楠语

Pangasinan

pag

西西里语

Sicilian

scn

信德语

Sindhi

sd

僧伽罗语

Sinhala

si

斯洛伐克语

Slovak

sk

斯洛文尼亚语

Slovenian

sl

南黎凡特阿拉伯语

South Levantine Arabic

ajp

斯瓦希里语

Swahili

sw

他加禄语

Tagalog

tl

塔伊兹-亚丁阿拉伯语

Ta’izzi-Adeni Arabic

acq

托斯克阿尔巴尼亚语

Tosk Albanian

sq

突尼斯阿拉伯语

Tunisian Arabic

aeb

威尼斯语

Venetian

vec

瓦莱语

Waray

war

威尔士语

Welsh

cy

西波斯语

Western Persian

fa

#### qwen-mt-lite 支持的语言 (31种)

**语言**

**英文名**

**代码**

英语

English

en

简体中文

Chinese

zh

繁体中文

Traditional Chinese

zh\_tw

俄语

Russian

ru

日语

Japanese

ja

韩语

Korean

ko

西班牙语

Spanish

es

法语

French

fr

葡萄牙语

Portuguese

pt

德语

German

de

意大利语

Italian

it

泰语

Thai

th

越南语

Vietnamese

vi

印度尼西亚语

Indonesian

id

马来语

Malay

ms

阿拉伯语

Arabic

ar

印地语

Hindi

hi

希伯来语

Hebrew

he

乌尔都语

Urdu

ur

孟加拉语

Bengali

bn

波兰语

Polish

pl

荷兰语

Dutch

nl

土耳其语

Turkish

tr

高棉语

Khmer

km

捷克语

Czech

cs

瑞典语

Swedish

sv

匈牙利语

Hungarian

hu

丹麦语

Danish

da

芬兰语

Finnish

fi

他加禄语

Tagalog

tl

波斯语

Persian

fa

## API参考

Qwen-MT 模型的输入与输出参数请参考[Qwen-MT 翻译模型](raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
