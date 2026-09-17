# 联网搜索

大模型的训练数据存在知识截止日期，无法回答实时问题。启用联网搜索后，模型可从网络获取实时数据，准确回答股票价格、天气预报、最新新闻等时效性问题。

## 使用方式

联网搜索支持以下四种API调用方式，启用参数各有不同：

#### OpenAI 兼容-Responses API

通过 `tools` 参数添加 `web_search` 工具即可启用联网搜索。

> Responses API 仅支持部分模型，支持的模型请参见[Responses API的联网搜索](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)。

```
# 导入依赖与创建客户端...
response = client.responses.create(
    model="qwen3.8-max",
    input="杭州天气",
    tools=[
        {"type": "web_search"},
        {"type": "web_extractor"},
        {"type": "code_interpreter"}
    ],
    extra_body={"enable_thinking": True}
)
```

#### OpenAI 兼容-Chat Completions API

设置 `enable_search: true` 即可启用联网搜索。

```
# 导入依赖与创建客户端...
completion = client.chat.completions.create(
    # 需使用支持联网搜索的模型
    model="qwen-plus",
    messages=[{"role": "user", "content": "杭州明天天气如何"}],
    # 由于 enable_search 非 OpenAI 标准参数，使用 Python SDK 需要通过 extra_body 传入（使用Node.js SDK 需作为顶层参数传入）
    extra_body={"enable_search": True}
)
```

#### DashScope

设置 `enable_search: true` 即可启用联网搜索。

```
# 导入依赖...
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 需使用支持联网搜索的模型
    model="qwen-plus",
    messages=[{"role": "user", "content": "杭州明天天气如何"}],
    # 通过 enable_search 参数开启联网搜索
    enable_search=True,
    result_format="message"
)
```

#### Anthropic 兼容

在 `tools` 参数中添加 Anthropic 服务端的联网搜索工具（`name` 为 `web_search`）即可启用联网搜索。请求地址为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/apps/anthropic`。

> 该方式面向 Claude Code 等 Anthropic 官方客户端。在客户端中直接用自然语言提问即可触发联网搜索，无需额外配置。

> 使用 Anthropic SDK 或 HTTP 直接调用时，需在 `system` 中传入客户端标识 `x-anthropic-billing-header: cc_entrypoint=cli;`，否则联网搜索不生效。

> **关于工具版本号**：`type` 中的日期后缀（例如 `web_search_20250305`）由 Anthropic 官方客户端的版本决定，客户端升级后可能改用其他日期的版本号。百炼按工具类别识别该工具，不校验具体的日期后缀，因此无需将 `type` 固定为某一版本，与客户端实际发送的值保持一致即可。

```
# 导入依赖与创建客户端...
message = client.messages.create(
    model="qwen3.8-max",
    max_tokens=2048,
    # 传入客户端标识
    system=[{"type": "text", "text": "x-anthropic-billing-header: cc_entrypoint=cli;"}],
    messages=[{"role": "user", "content": "杭州明天天气如何"}],
    tools=[
        {
            # 日期后缀由客户端版本决定，此处以 Claude Code 当前使用的版本为例
            "type": "web_search_20250305",
            "name": "web_search",
            # 可选，单次请求最多检索次数
            "max_uses": 8
        }
    ]
)
```

模型的检索过程通过 `server_tool_use`（检索请求）和 `web_search_tool_result`（检索结果）内容块返回，检索次数记录在 `usage.server_tool_use.web_search_requests` 中。

### 多模态模型的联网搜索

Qwen3.8 Max、Flash 与开源系列、Qwen3.7-Flash、Qwen3.7-Plus、Qwen3.6 系列、Qwen3.5 系列（含 qwen3.5-plus、qwen3.5-flash、qwen3.5-omni 系列与千问开源模型）等模型支持图片、视频等多模态输入，属于多模态模型。这类模型需通过**多模态接口**（`multimodal-generation` 端点）调用：Python 与 Java 使用 `MultiModalConversation`，而不能使用面向纯文本模型的 `Generation`（`text-generation` 端点）。多模态模型的基础调用方式可参见《视觉推理》《图像与视频理解》文档。

搜索策略因系列而异：qwen3.5-omni 系列仅支持 `agent` 策略；`qwen3.8-max`、`qwen3.8-max-0902`、`qwen3.8-flash`、`qwen3.8-2.4t-a95b` 和 `qwen3.8-27b` 在多模态接口下不支持 `agent` 策略（使用默认的 `turbo` 或 `max`），如需对 Qwen3.8 使用 agent 检索，请改用 [Responses API 的联网搜索](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)；本节列出的其余模型支持 `turbo`、`max`、`agent` 策略。

> 若使用 `Generation`（`text-generation` 端点）调用上述多模态模型，会返回 `400 url error, please check url`，请改用 `MultiModalConversation`（`multimodal-generation` 端点）。Java SDK 的 `MultiModalConversationParam` 提供 `enableSearch(true)` 用于开启联网搜索，但未提供 `searchOptions()` 方法，需通过通用参数 `parameter("search_options", ...)` 注入搜索策略等配置；Python 的 `MultiModalConversation.call` 可直接传入 `search_options`。多模态模型开启联网搜索时需使用**流式调用**（Java 使用 `streamCall`，Python 设置 `stream=True`），否则会返回 `Non-streaming mode does not support Web Search` 报错。

Python

```
import os
import dashscope
from dashscope import MultiModalConversation
# 以下为新加坡地域配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1"
responses = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 需使用支持联网搜索的多模态模型
    model="qwen3.5-plus",
    messages=[{"role": "user", "content": [{"text": "杭州今天天气如何"}]}],
    # 多模态接口可直接传入 enable_search 与 search_options
    enable_search=True,
    search_options={
        # qwen3.5-omni 系列需设为 agent；Qwen3.8 系列在多模态接口下不支持 agent，保持默认即可
        "search_strategy": "agent",
        "enable_source": True,
    },
    # 多模态模型开启联网搜索时需使用流式调用
    stream=True,
    incremental_output=True,
)
for response in responses:
    print(response.output.choices[0].message.content)
```

Java

```
// dashscope SDK 版本 >= 2.19.0
import java.util.Arrays;
import java.util.Collections;
import io.reactivex.Flowable;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.aigc.generation.SearchOptions;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为新加坡地域配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    static { Constants.baseHttpApiUrl = "https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1"; }
    public static void main(String[] args) throws Exception {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMsg = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "杭州今天天气如何")))
                .build();
        SearchOptions searchOptions = SearchOptions.builder()
                // qwen3.5-omni 系列需设为 agent；Qwen3.8 系列不支持 agent，保持默认即可
                .searchStrategy("agent")
                .enableSource(true)
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 需使用支持联网搜索的多模态模型
                .model("qwen3.5-plus")
                .messages(Arrays.asList(userMsg))
                // 原生方法：开启联网搜索
                .enableSearch(true)
                // MultiModalConversationParam 未提供 searchOptions() 方法，需通过通用 parameter() 注入 search_options
                .parameter("search_options", searchOptions)
                .incrementalOutput(true)
                .build();
        // 多模态模型开启联网搜索时需使用流式调用
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(message ->
                System.out.print(message.getOutput().getChoices().get(0).getMessage().getContent()));
    }
}
```

## 支持的模型

`qwen3.8-omni-flash` 支持通过 Chat Completions 和 Responses API 联网搜索。Chat Completions 使用 `enable_search`；Responses 使用 `tools=[{"type": "web_search"}]`。

支持联网搜索的模型如下。支持多模态输入的模型（Qwen3.8 Max、Flash 与开源系列、Qwen3.7-Flash/Plus、Qwen3.6 系列、Qwen3.5 系列及千问开源模型等）需通过多模态接口调用，参见[多模态模型的联网搜索](https://help.aliyun.com/zh/model-studio/web-search#ws_mm_search_h3a)。

#### 华北2（北京）

-   **千问**
    
    -   Qwen3.8 系列：qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash、qwen3.8-2.4t-a95b、qwen3.8-27b（`search_strategy` 不支持 `agent`；如需 agent 检索，请通过 [Responses API](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y) 使用 `web_search` 工具）
    -   Qwen3.7 系列：qwen3.7-max、qwen3.7-max-preview、qwen3.7-max-2026-05-17及之后的快照版本、qwen3.7-plus、qwen3.7-plus-2026-05-26及之后的快照版本、qwen3.7-flash、qwen3.7-flash-2026-07-15及之后的快照版本
    -   Qwen3.6 系列：qwen3.6-max-preview、qwen3.6-plus、qwen3.6-plus-2026-04-02及之后的快照版本、qwen3.6-flash、qwen3.6-flash-2026-04-16及之后的快照版本、qwen3.6-27b、qwen3.6-35b-a3b
    -   Qwen3.5 系列：qwen3.5-plus、qwen3.5-plus-2026-02-15及之后的快照版本、qwen3.5-flash、qwen3.5-flash-2026-02-23及之后的快照版本、qwen3.5-27b、qwen3.5-35b-a3b、qwen3.5-122b-a10b、qwen3.5-397b-a17b
    -   Qwen3-Max：qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23及之后的快照版本
    -   Qwen-Max：qwen-max及之后的快照版本
    -   Qwen-Plus：qwen-plus、qwen-plus-latest、qwen-plus-2025-07-14及之后的快照版本
    -   Qwen-Flash：qwen-flash、qwen-flash-2025-07-28及之后的快照版本
    -   Qwen-Turbo：qwen-turbo
    -   QwQ：qwq-plus（仅支持默认搜索策略，不能设置 `search_strategy`）
    -   千问Omni：qwen3.5-omni-plus、qwen3.5-omni-plus-2026-03-15、qwen3.5-omni-flash、qwen3.5-omni-flash-2026-03-15（搜索策略需设为 `agent`）
    -   千问Omni-Realtime：qwen3.5-omni-plus-realtime、qwen3.5-omni-plus-realtime-2026-03-15、qwen3.5-omni-flash-realtime、qwen3.5-omni-flash-realtime-2026-03-15（搜索策略需设为 `agent`）
    -   角色扮演：qwen-plus-character、qwen-flash-character、qwen-flash-character-2026-02-26（不支持 `agent` 策略）
    
    2025 年 7 月后发布的千问Max、千问Plus、千问Flash 模型都自动支持联网搜索。
    
-   **第三方模型**
    -   DeepSeek：deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1、deepseek-r1-0528、deepseek-r1、deepseek-v3（其中 deepseek-v4 系列同时支持[Responses API](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)）
    -   GLM：glm-5.2（仅支持通过[Responses API](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)联网搜索）
    -   Kimi：Moonshot-Kimi-K2-Instruct、kimi-k3（kimi-k3 仅支持通过[Responses API](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)联网搜索）
    -   MiniMax：MiniMax-M2.1（不支持 `agent` 策略）

#### 新加坡

-   **千问**
    -   Qwen3.8 系列：qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash、qwen3.8-2.4t-a95b、qwen3.8-27b（`search_strategy` 不支持 `agent`；如需 agent 检索，请通过 [Responses API](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y) 使用 `web_search` 工具）
    -   Qwen3.7 系列：qwen3.7-max、qwen3.7-max-2026-05-20及之后的快照版本、qwen3.7-plus、qwen3.7-plus-2026-05-26及之后的快照版本、qwen3.7-flash、qwen3.7-flash-2026-07-15及之后的快照版本
    -   Qwen3.6 系列：qwen3.6-max-preview、qwen3.6-plus、qwen3.6-plus-2026-04-02及之后的快照版本、qwen3.6-flash、qwen3.6-flash-2026-04-16及之后的快照版本、qwen3.6-27b、qwen3.6-35b-a3b
    -   Qwen3.5 系列：qwen3.5-plus、qwen3.5-plus-2026-02-15及之后的快照版本、qwen3.5-flash、qwen3.5-flash-2026-02-23及之后的快照版本、qwen3.5-27b、qwen3.5-35b-a3b、qwen3.5-122b-a10b、qwen3.5-397b-a17b
    -   Qwen3-Max：qwen3-max、qwen3-max-2025-09-23及之后的快照版本
    -   千问Omni：qwen3.5-omni-plus、qwen3.5-omni-plus-2026-03-15、qwen3.5-omni-flash、qwen3.5-omni-flash-2026-03-15（搜索策略需设为 `agent`）
    -   千问Omni-Realtime：qwen3.5-omni-plus-realtime、qwen3.5-omni-plus-realtime-2026-03-15、qwen3.5-omni-flash-realtime、qwen3.5-omni-flash-realtime-2026-03-15（搜索策略需设为 `agent`）
-   **第三方模型**
    -   DeepSeek：deepseek-v4-pro、deepseek-v4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2（其中 deepseek-v4 系列同时支持[Responses API](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)）
    -   GLM：glm-5.2（仅支持通过[Responses API](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)联网搜索）
    -   Kimi：kimi-k3（仅支持通过[Responses API](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)联网搜索）

#### 全球

美国（弗吉尼亚）、中国香港、日本（东京）、德国（法兰克福）地域支持以下模型。其中中国香港、日本（东京）、德国（法兰克福）需使用服务部署范围为**全球**的业务空间调用，参见[选择地域、服务部署范围和接入域名](raw/model-user-guide/get-started-with-models/regions.md)。

-   **千问**
    -   Qwen3.8 系列：qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash

## 快速开始

以下示例通过联网搜索查询天气信息。

#### OpenAI 兼容

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "杭州明天天气如何"},
    ],
    extra_body={"enable_search": True}
)
print(completion.choices[0].message.content)
```

###### 响应示例

```
根据现有资料，2025年9月17日（明天）杭州市的天气情况如下：

- **天气状况**：多云转晴，部分地区可能有小雨。
- **气温**：白天最高气温约30℃至34℃，夜间最低气温约24℃至26℃。
- **风力**：风力较小，一般为东风、东南风或西风，风速小于3级。
- **湿度**：相对湿度约77%。
- **空气质量**：良好，空气质量指数约为34至38。
- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。

此外，冷空气将于明天午后到夜里抵达浙江，开始逐渐带来降温，但高温仍会持续到当天午后。从18日开始，全省范围的高温将彻底缓解。

请注意根据天气变化及时调整出行和穿衣安排。
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "杭州明天天气如何" }
        ],
        enable_search:true
    });
    console.log(completion.choices[0].message.content);
}

main();
```

###### 响应示例

```
根据现有资料，2025年9月17日（明天）杭州市的天气情况如下：

- **天气状况**：多云转晴，部分地区可能有小雨。
- **气温**：白天最高气温约30℃至34℃，夜间最低气温约24℃至26℃。
- **风力**：风力较小，一般为东风、东南风或西风，风速小于3级。
- **湿度**：相对湿度约77%。
- **空气质量**：良好，空气质量指数约为34至38。
- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。

此外，冷空气将于明天午后到夜里抵达浙江，开始逐渐带来降温，但高温仍会持续到当天午后。从18日开始，全省范围的高温将彻底缓解。

请注意根据天气变化及时调整出行和穿衣安排。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "杭州明天天气如何"
        }
    ],
    "enable_search": true
}'
```

#### DashScope

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "杭州明天天气是什么？"},
]
response = dashscope.Generation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=messages,
    enable_search=True,
    result_format="message"
)
print(response["output"]["choices"][0]["message"]["content"])
```

###### 响应示例

```
根据现有资料，2025年9月17日（明天）杭州市的天气情况如下：

- **天气状况**：多云转晴，部分地区可能有小雨。
- **气温**：白天最高气温约30℃至34℃，夜间最低气温约24℃至26℃。
- **风力**：风力较小，一般为东风、东南风或西风，风速小于3级。
- **湿度**：相对湿度约77%。
- **空气质量**：良好，空气质量指数约为34至38。
- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。

此外，冷空气将于明天午后到夜里抵达浙江，开始逐渐带来降温，但高温仍会持续到当天午后。从18日开始，全省范围的高温将彻底缓解。

请注意根据天气变化及时调整出行和穿衣安排。
```

#### Java

```
// 建议 dashscope SDK的版本 >= 2.19.4
import java.util.Arrays;
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
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
        Generation gen = new Generation();
        Message systemMsg = Message.builder()
                .role(Role.SYSTEM.getValue())
                .content("You are a helpful assistant.")
                .build();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("明天杭州什么天气？")
                .build();
        GenerationParam param = GenerationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .messages(Arrays.asList(systemMsg, userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .enableSearch(true)
                .build();
        return gen.call(param);
    }
    public static void main(String[] args) {
        try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("An error occurred while calling the generation service: " + e.getMessage());
        }
    }
}
```

###### 响应示例

```
根据现有资料，2025年9月17日（明天）杭州市的天气情况如下：

- **天气状况**：多云转晴，部分地区可能有小雨。
- **气温**：白天最高气温约30℃至34℃，夜间最低气温约24℃至26℃。
- **风力**：风力较小，一般为东风、东南风或西风，风速小于3级。
- **湿度**：相对湿度约77%。
- **空气质量**：良好，空气质量指数约为34至38。
- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。

此外，冷空气将于明天午后到夜里抵达浙江，开始逐渐带来降温，但高温仍会持续到当天午后。从18日开始，全省范围的高温将彻底缓解。

请注意根据天气变化及时调整出行和穿衣安排。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
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
                "content": "明天杭州天气如何？"
            }
        ]
    },
    "parameters": {
        "enable_search": true,
        "result_format": "message"
    }
}'
```

## 核心能力

联网搜索除基础搜索外，还支持强制搜索、搜索策略设置、搜索来源返回等进阶功能。DashScope 协议支持全部功能。OpenAI 兼容协议因协议限制，不支持搜索来源返回和角标标注等功能，具体差异见下表。

**功能特性**

**DashScope**

**OpenAI 兼容-Chat Completions**

**OpenAI 兼容-Responses**

基础联网搜索

支持

支持

支持

强制联网搜索

支持

支持

不支持

设置搜索量级策略

支持

支持

不支持

开启垂域搜索

支持

支持

不支持

设置搜索时效性

支持

支持

不支持

限定搜索来源站点

支持

支持

不支持

通过自然语言干预检索范围

支持

支持

不支持

返回搜索来源

支持

不支持

不支持

角标引用标注

支持

不支持

不支持

提前返回搜索来源

支持

不支持

不支持

图文混合输出

支持

支持

不支持

### 设置搜索量级策略

通过`search_strategy`参数可在成本、质量和响应速度之间取得平衡。

`search_strategy`**可选值**:

-   `turbo` （默认）: 兼顾响应速度与搜索效果，适用于大多数场景。
    
-   `max`: 采用更全面的搜索策略，可调用多源搜索引擎，以获取更详尽的搜索结果，但响应时间可能更长。
    
-   `agent`：可多次调用联网搜索工具与大模型，实现多轮信息检索与内容整合。
    
    > 该策略适用于 Qwen3-Max 系列（qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23及之后的快照版本）、Qwen3.5 系列（含开源模型与 Omni 系列）、Qwen3.6 系列、Qwen3.7 系列模型，通过 text 端点调用时需使用流式调用。`qwen3.8-max`、`qwen3.8-max-0902`、`qwen3.8-flash`、`qwen3.8-2.4t-a95b` 和 `qwen3.8-27b` 在 Chat Completions/DashScope 协议下不支持 `search_strategy: agent`，但可通过 [Responses API 的联网搜索](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y) 使用 `web_search` 工具实现 agent 式多轮检索。MiniMax-M2.1、Moonshot-Kimi-K2-Instruct 与角色扮演模型不支持 `agent` 策略。
    
    > 启用该策略时，仅支持 **返回搜索来源** （ `enable_source: true` ），其他联网搜索功能不可用。
    
    > 启用该策略时，每次调用额外收费，参见 [计费说明](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599) 。
    
-   `agent_max`：在`agent`策略基础上支持网页抓取，参见：[网页抓取](raw/model-user-guide/model-experience/text-generation-model/tool-calls/web-extractor.md)。
    
    > 该策略仅适用于qwen3-max、qwen3-max-2026-01-23的思考模式。
    
    > 启用该策略时，仅支持 **返回搜索来源** （ `enable_source: true` ），其他联网搜索功能不可用。
    
    > 启用该策略时，每次调用额外收费，参见 [计费说明](https://help.aliyun.com/zh/model-studio/web-search#92ce83df3a599) 。
    

日常查询建议使用默认的 `turbo` 策略。对于需要高精度、多源交叉验证的研究或报告生成场景，可选择 `max`或`agent` 策略。英文场景推荐使用`agent`。

不同模型处理时效性数据的能力存在差异。qwen3-max 具备日期推理能力，能识别非交易日并提示无数据；qwen-max 不具备该能力，会直接返回搜索获取的股价数据。股票等强时效性查询建议使用 qwen3-max 或更新版本的模型。

#### OpenAI 兼容

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "Qwen 2025年9月份发布了哪些模型"},
    ],
    extra_body={
        "enable_search": True,
        "search_options": {
            "search_strategy": "max"  # 配置搜索策略为高性能模式
        }
    }
)
print(completion.choices[0].message.content)
```

###### 响应示例

```
根据已有的知识库内容，阿里云千问团队在2025年9月份发布了以下模型：

1. **Qwen3-Next**：这是下一代基础模型架构，采用了高稀疏度混合专家（MoE）架构。该模型总参数量达800亿，但在每次推理时仅激活30亿参数，从而显著降低了推理成本，同时性能可以媲美2350亿参数的Qwen3旗舰版。

2. **Qwen3-Next-80B-A3B系列模型**：这是基于Qwen3-Next架构开发的模型系列，具有更高的计算效率和更低的训练成本。其训练成本相比密集模型Qwen3-32B下降了超过90%。

3. **Qwen3-Max-Preview**：该模型的参数量超过1万亿，支持最长256K tokens的上下文窗口，并覆盖超过100种语言。它在指令跟随和检索等方面进行了升级。

这些模型的发布标志着阿里云在人工智能领域的进一步突破，特别是在模型效率、性能和多语言支持方面。
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",
        messages: [
            { role: "user", content: "Qwen 2025年9月份发布了哪些模型" }
        ],
        enable_search: true,
        search_options: {
            search_strategy: "max" // 配置搜索策略为高性能模式
        }
    });
    console.log(completion.choices[0].message.content);
}

main();
```

###### 响应示例

```
根据已有的知识库内容，阿里云千问团队在2025年9月份发布了以下模型：
1. **Qwen3-Next**：这是下一代基础模型架构，采用了高稀疏度混合专家（MoE）架构。该模型总参数量达800亿，但在每次推理时仅激活30亿参数，从而显著降低了推理成本，同时性能可以媲美2350亿参数的Qwen3旗舰版。

2. **Qwen3-Next-80B-A3B系列模型**：这是基于Qwen3-Next架构开发的模型系列，具有更高的计算效率和更低的训练成本。其训练成本相比密集模型Qwen3-32B下降了超过90%。

3. **Qwen3-Max-Preview**：该模型的参数量超过1万亿，支持最长256K tokens的上下文窗口，并覆盖超过100种语言。它在指令跟随和检索等方面进行了升级。

这些模型的发布标志着阿里云在人工智能领域的进一步突破，特别是在模型效率、性能和多语言支持方面。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user",
            "content": "Qwen 2025年9月份发布了哪些模型"
        }
    ],
    "enable_search": true,
    "search_options": {
        "search_strategy": "max"
    }
}'
```

###### 响应示例

```
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "根据已有的知识库信息，阿里巴巴在2025年9月份发布了以下模型：\n\n1. **Qwen3-Max-Preview**：\n   - 发布时间：2025年9月5日。\n   - 特点：这是Qwen系列中首个参数量超过**1万亿**的模型，标志着中国AI技术在超大规模模型领域的重要突破。\n   - 其他功能：支持最长256K tokens的上下文窗口，并覆盖超过100种语言。\n\n2. **Qwen3-Next**：\n   - 发布时间：2025年9月12日。\n   - 架构特点：采用了**高稀疏度混合专家（MoE）架构**，总参数量为800亿（80B），但每次推理仅激活30亿参数，显著降低推理成本。\n   - 性能表现：性能媲美Qwen3旗舰版的2350亿参数模型，同时训练成本较此前密集模型（Qwen3-32B）下降超过90%。\n   - 技术创新：引入了混合注意力机制、多token预测机制等，显著提升长文本处理效率和推理速度（在32K+上下文场景下，速度是Qwen3-32B的10倍以上）。\n\n3. **Qwen3-Next-80B-A3B系列模型**：\n   - 基于Qwen3-Next架构开发，同步开源。\n   - 特点：支持百万tokens超长上下文，适用于复杂任务和大规模数据处理。\n\n总结：\n- **Qwen3-Max-Preview** 是一个超大规模模型，专注于参数量的突破。\n- **Qwen3-Next** 及其系列模型（如 Qwen3-Next-80B-A3B）则是通过架构创新，在性能、效率和成本之间取得了更好的平衡。"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 1789,
    "completion_tokens": 412,
    "total_tokens": 2201,
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "created": 1758011574,
  "system_fingerprint": null,
  "model": "qwen-plus",
  "id": "chatcmpl-c87a80cc-8d89-4de8-9e50-370bc45fdd51"
}
```

#### DashScope

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "Qwen 2025年9月份发布了哪些模型?"}],
    enable_search=True,
    search_options={
        "search_strategy": "max",  # 配置搜索策略为高性能模式
        "enable_source": True
    },
    result_format="message",
)
print("="*20 + "搜索结果" + "="*20)
for web in response.output.search_info["search_results"]:
    print(f"[{web['index']}]: [{web['title']}]({web['url']})")
print("="*20 + "回复内容" + "="*20)
print(response.output.choices[0].message.content)
```

###### 响应示例

```
====================搜索结果====================
[1]: [阿里持续迭代QWEN3模型,恒生科技指数ETF(159742)持续拉升涨超1.5%,冲击7连涨](https://baijiahao.baidu.com/s?id=1843294702563736079&wfr=spider&for=pc)
[2]: [阿里推出下一代模型架构;宇树王兴兴谈后悔的事丨新鲜早科技](https://baijiahao.baidu.com/s?id=1843023858158066280&wfr=spider&for=pc)
[3]: [千问发布Qwen3-Max-Preview，参数量超1万亿](https://wallstreetcn.com/articles/3755053)
[4]: [富瑞：阿里巴巴-W推新一代Qwen模型再创里程碑AI主题开启 ...](https://finance.sina.com.cn/stock/hkstock/hkgg/2025-09-08/doc-infpumzk6212010.shtml?cre=tianyi&mod=pchp&loc=7&r=0&rfunc=52&tj=cxvertical_pc_hp&tr=12)
[5]: [富瑞：阿里巴巴-W推新一代Qwen模型再创里程碑AI主题开启 ...](https://finance.sina.com.cn/stock/hkstock/hkgg/2025-09-08/doc-infpumzk6212010.shtml?cre=tianyi&mod=pchp&loc=9&r=0&rfunc=64&tj=cxvertical_pc_hp&tr=12)
[6]: [行业观察|85天两次重大迭代,阿里大模型为什么死磕全球速度?](https://baijiahao.baidu.com/s?id=1838706037923454039&wfr=spider&for=pc)
[7]: [Qwen-Image完整指南：2025年最强文本渲染AI图像生成模型 ...](https://www.cnblogs.com/sing1ee/p/19022727/2025-qwen-image)
[8]: [阿里Qwen3-Next大模型深度解析:80B参数3B激活,成本降低10倍,速度提升10倍!](https://zhuanlan.zhihu.com/p/1950159852463687349)
[9]: [《2025大模型服务商能力榜》发布:涵盖20 余家大模型服务商的数百个模型服务](https://baijiahao.baidu.com/s?id=1843140062741335131&wfr=spider&for=pc)
[10]: [Qwen模型发布时间线: 2023-2025](https://mylens.ai/space/zc02520s-workspace-hclkbo/qwen%E6%A8%A1%E5%9E%8B%E5%8F%91%E5%B8%83%E6%97%B6%E9%97%B4%E7%BA%BF-jenflw)
====================回复内容====================
根据2025年9月的公开信息，阿里巴巴千问（Qwen）团队发布了以下重要模型：

1.  **Qwen3-Next系列模型 (9月12日发布)**：
    *   阿里千问在9月12日发布了下一代基础模型架构 **Qwen3-Next**，并开源了基于该架构的 **Qwen3-Next-80B-A3B** 系列模型。
    *   该模型采用创新的混合注意力机制和高稀疏度MoE结构，总参数达800亿（80B），但每次推理仅激活30亿（3B）参数，显著降低了计算成本。
    *   其核心优势在于效率的大幅提升：训练成本较之前的密集模型降低超90%，长文本推理吞吐量提升10倍以上，并支持百万Tokens的超长上下文。

此外，虽然发布时间在9月初，但也属于近期的重要更新：

*   **Qwen3-Max-Preview模型 (9月5日上线)**：
    *   该模型参数量超过1万亿，支持最长256K tokens的上下文窗口，已上线阿里云百炼平台供API调用。

综上所述，2025年9月，Qwen最核心的发布是**9月12日推出的革命性高效架构Qwen3-Next及其Qwen3-Next-80B-A3B系列模型**。
```

#### Java

```
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.SearchOptions;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import java.util.Arrays;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void main(String[] args) {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("Qwen 2025年9月份发布了哪些模型？")
                .build();

        SearchOptions searchOptions = SearchOptions.builder()
                .searchStrategy("max") // 配置搜索策略为高性能模式
                .enableSource(true)
                .build();

        GenerationParam param = GenerationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .messages(Arrays.asList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .enableSearch(true)
                .searchOptions(searchOptions)
                .build();
        try {
            GenerationResult result = gen.call(param);
            System.out.println("=".repeat(20)+"搜索结果"+"=".repeat(20));
            System.out.println(result.getOutput().getSearchInfo().getSearchResults());
            System.out.println("=".repeat(20)+"回复内容"+"=".repeat(20));
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

###### 响应示例

```
====================搜索结果====================
[SearchInfo.SearchResult(siteName=知乎, icon=https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=493147230,3096476255&fm=195&app=88&f=JPEG?w=200&h=200, index=1, title=阿里Qwen3-Next技术解析:高稀疏度混合专家架构引领大模型新趋势!, url=https://zhuanlan.zhihu.com/p/1950881062403184335), SearchInfo.SearchResult(siteName=知乎, icon=https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=493147230,3096476255&fm=195&app=88&f=JPEG?w=200&h=200, index=2, title=Qwen3-Next:阿里千问挥舞“魔法棒”,点石成金打造AI新基石!, url=https://zhuanlan.zhihu.com/p/1949926096301696837), SearchInfo.SearchResult(siteName=搜狐网, icon=https://b.bdstatic.com/searchbox/mappconsole/image/20190429/a68f8bb8-95b8-406a-8463-b6d029c66170.jpg, index=3, title=阿里巴巴发布Qwen3-Next系列模型,四大架构创新引领AI新潮流 , url=https://www.sohu.com/a/934235058_121956424), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=4, title=阿里持续迭代QWEN3模型,恒生科技指数ETF(159742)持续拉升涨超1.5%,冲击7连涨, url=https://baijiahao.baidu.com/s?id=1843294702563736079&wfr=spider&for=pc), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=5, title=阿里推出下一代模型架构;宇树王兴兴谈后悔的事丨新鲜早科技, url=https://baijiahao.baidu.com/s?id=1843023858158066280&wfr=spider&for=pc), SearchInfo.SearchResult(siteName=, icon=, index=6, title=千问发布Qwen3-Max-Preview，参数量超1万亿, url=https://wallstreetcn.com/articles/3755053), SearchInfo.SearchResult(siteName=搜狐网, icon=https://b.bdstatic.com/searchbox/mappconsole/image/20190429/a68f8bb8-95b8-406a-8463-b6d029c66170.jpg, index=7, title=Qwen3-Next发布!昇腾强力支持,AI模型新纪元开启 , url=https://news.sohu.com/a/934399340_122004016), SearchInfo.SearchResult(siteName=新浪网, icon=https://img.alicdn.com/imgextra/i2/O1CN01mvEkNg1mbgbrppM5C_!!6000000004973-55-tps-32-32.svg, index=8, title=富瑞：阿里巴巴-W推新一代Qwen模型再创里程碑AI主题开启 ..., url=https://finance.sina.com.cn/stock/hkstock/hkgg/2025-09-08/doc-infpumzk6212010.shtml?cre=tianyi&mod=pchp&loc=7&r=0&rfunc=52&tj=cxvertical_pc_hp&tr=12), SearchInfo.SearchResult(siteName=新浪网, icon=https://img.alicdn.com/imgextra/i2/O1CN01mvEkNg1mbgbrppM5C_!!6000000004973-55-tps-32-32.svg, index=9, title=富瑞：阿里巴巴-W推新一代Qwen模型再创里程碑AI主题开启 ..., url=https://finance.sina.com.cn/stock/hkstock/hkgg/2025-09-08/doc-infpumzk6212010.shtml?cre=tianyi&mod=pchp&loc=9&r=0&rfunc=64&tj=cxvertical_pc_hp&tr=12), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=10, title=杰富瑞:阿里推新一代Qwen模型再创里程碑, url=https://baijiahao.baidu.com/s?id=1842683950982961781&wfr=spider&for=pc)]
====================回复内容====================
2025年9月份，Qwen（阿里千问）发布了以下模型：

1. **Qwen3-Max-Preview**
   - 发布时间：2025年9月5日
   - 特点：这是Qwen系列中首个参数量超过**1万亿**的模型，支持最长256K tokens的上下文窗口，并覆盖超过100种语言。它在多项主流权威基准测试中表现卓越，标志着中国AI技术在超大规模模型领域的重大突破。

2. **Qwen3-Next**
   - 发布时间：2025年9月12日
   - 特点：作为下一代基础模型架构，Qwen3-Next采用了革命性的**高稀疏度混合专家（MoE）架构**，总参数量达800亿，但每次推理仅需激活30亿参数，大幅降低了计算成本。性能方面，其表现可与2350亿参数的Qwen3旗舰版相媲美，训练成本却下降超过90%。

3. **Qwen3-Next-80B-A3B系列模型**
   - 发布时间：2025年9月12日
   - 特点：基于Qwen3-Next架构构建，支持超长上下文（百万Tokens级别），推理吞吐量提升10倍以上。采用了创新的**混合注意力机制**，在长文本处理上实现了速度与效果的平衡，并且推理效率显著提高。

这些模型的发布标志着Qwen在AI大模型领域的技术迭代和突破，推动了AI在多个领域的应用发展。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "Qwen 2025年9月份发布了哪些模型？"
            }
        ]
    },
    "parameters": {
        "enable_search": true,
        "search_options": {
            "search_strategy": "max",
            "enable_source": true
        },
        "result_format": "message"
    }
}'
```

###### 响应示例

```
{
  "output": {
    "choices": [
      {
        "message": {
          "content": "根据提供的资料，2025年9月份阿里巴巴的千问(Qwen)系列发布了以下模型：\n\n1. **Qwen3-Next**：这是下一代基础模型架构，具有革命性的高稀疏度混合专家（MoE）架构。Qwen3-Next的总参数量达到了800亿，但在每次推理时仅激活30亿参数，显著降低了训练成本，并提升了推理效率。\n\n2. **Qwen3-Next-80B-A3B系列模型**：包括了Qwen3-Next-80B-A3B-Instruct与Qwen3-Next-80B-A3B-Thinking两个模型。这两个模型均基于Qwen3-Next-80B-A3B-Base模型训练而来，Base模型拥有800亿参数，30亿激活参数。\n\n3. **Qwen3-Max-Preview**：这是一个参数量超过1万亿的模型，支持最长256K tokens的上下文窗口，并覆盖超过100种语言。此模型已上线阿里云百炼平台，可通过API调用，并且Qwen Chat也同步上线了新模型，支持免费使用。\n\n这些模型的发布体现了阿里巴巴在大模型领域的持续创新和技术进步，尤其是在提高模型效率和降低训练成本方面取得了显著成就。",
          "role": "assistant"
        },
        "finish_reason": "stop"
      }
    ],
    "search_info": {
      "extra_tool_info": [],
      "search_results": [
        {
          "icon": "https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=493147230,3096476255&fm=195&app=88&f=JPEG?w=200&h=200",
          "site_name": "知乎",
          "index": 1,
          "title": "阿里Qwen3-Next技术解析:高稀疏度混合专家架构引领大模型新趋势!",
          "url": "https://zhuanlan.zhihu.com/p/1950881062403184335"
        },
        {
          "icon": "https://baijiahao.baidu.com/favicon.ico",
          "site_name": "百家号",
          "index": 2,
          "title": "阿里推出下一代模型架构;宇树王兴兴谈后悔的事丨新鲜早科技",
          "url": "https://baijiahao.baidu.com/s?id=1843023858158066280&wfr=spider&for=pc"
        },
        {
          "icon": "",
          "site_name": "",
          "index": 3,
          "title": "千问发布Qwen3-Max-Preview，参数量超1万亿",
          "url": "https://wallstreetcn.com/articles/3755053"
        },
        {
          "icon": "https://img.alicdn.com/imgextra/i2/O1CN01mvEkNg1mbgbrppM5C_!!6000000004973-55-tps-32-32.svg",
          "site_name": "新浪网",
          "index": 4,
          "title": "富瑞：阿里巴巴-W推新一代Qwen模型再创里程碑AI主题开启 ...",
          "url": "https://finance.sina.com.cn/stock/hkstock/hkgg/2025-09-08/doc-infpumzk6212010.shtml?cre=tianyi&mod=pchp&loc=7&r=0&rfunc=52&tj=cxvertical_pc_hp&tr=12"
        },
        {
          "icon": "https://img.alicdn.com/imgextra/i2/O1CN01mvEkNg1mbgbrppM5C_!!6000000004973-55-tps-32-32.svg",
          "site_name": "新浪网",
          "index": 5,
          "title": "富瑞：阿里巴巴-W推新一代Qwen模型再创里程碑AI主题开启 ...",
          "url": "https://finance.sina.com.cn/stock/hkstock/hkgg/2025-09-08/doc-infpumzk6212010.shtml?cre=tianyi&mod=pchp&loc=9&r=0&rfunc=64&tj=cxvertical_pc_hp&tr=12"
        },
        {
          "icon": "https://baijiahao.baidu.com/favicon.ico",
          "site_name": "百家号",
          "index": 6,
          "title": "行业观察|85天两次重大迭代,阿里大模型为什么死磕全球速度?",
          "url": "https://baijiahao.baidu.com/s?id=1838706037923454039&wfr=spider&for=pc"
        },
        {
          "icon": "https://img.alicdn.com/imgextra/i2/O1CN01FzHbv01o253A3z2Gd_!!6000000005166-55-tps-32-32.svg",
          "site_name": "博客园",
          "index": 7,
          "title": "Qwen-Image完整指南：2025年最强文本渲染AI图像生成模型 ...",
          "url": "https://www.cnblogs.com/sing1ee/p/19022727/2025-qwen-image"
        },
        {
          "icon": "https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=493147230,3096476255&fm=195&app=88&f=JPEG?w=200&h=200",
          "site_name": "知乎",
          "index": 8,
          "title": "阿里Qwen3-Next大模型深度解析:80B参数3B激活,成本降低10倍,速度提升10倍!",
          "url": "https://zhuanlan.zhihu.com/p/1950159852463687349"
        },
        {
          "icon": "https://developer.aliyun.com/favicon.ico",
          "site_name": "阿里云.",
          "index": 9,
          "title": "# Qwen3-8B 与 Qwen3-14B 的 TTFT 性能对比与底层原理详解",
          "url": "https://developer.aliyun.com/article/1672506"
        },
        {
          "icon": "",
          "site_name": "",
          "index": 10,
          "title": "Qwen模型发布时间线: 2023-2025",
          "url": "https://mylens.ai/space/zc02520s-workspace-hclkbo/qwen%E6%A8%A1%E5%9E%8B%E5%8F%91%E5%B8%83%E6%97%B6%E9%97%B4%E7%BA%BF-jenflw"
        }
      ]
    }
  },
  "usage": {
    "total_tokens": 2614,
    "output_tokens": 280,
    "input_tokens": 2334,
    "plugins": {
      "search": {
        "count": 1
      }
    },
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "request_id": "9fe63fe8-d274-4e6b-9249-5783449dc27a"
}
```

### 强制联网搜索

默认情况下，模型自行判断是否需要联网搜索。业务场景强依赖实时信息时，可设置 `forced_search` 参数为`true`，强制执行联网搜索。

`forced_search`**可选值**：

-   `true`: 强制联网搜索。
-   `false` (默认): 模型判断是否需要联网。

#### OpenAI 兼容

#### Python

**说明**Python SDK需通过`extra_body`传递`enable_search`，Node.js SDK在顶层传递。

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "杭州明天天气如何"},
    ],
    extra_body={
        "enable_search": True,
        "search_options": {
            "forced_search": True  # 强制联网搜索
        }
    }
)
print(completion.choices[0].message.content)
```

###### 响应示例

```
根据现有资料，2025年9月17日（明天）杭州市的天气情况如下：

- **天气状况**：多云转晴，部分地区可能有小雨。
- **气温**：白天最高气温约30℃至34℃，夜间最低气温约24℃至26℃。
- **风力**：风力较小，一般为东风、东南风或西风，风速小于3级。
- **湿度**：相对湿度约77%。
- **空气质量**：良好，空气质量指数约为34至38。
- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。

此外，冷空气将于明天午后到夜里抵达浙江，开始逐渐带来降温，但高温仍会持续到当天午后。从18日开始，全省范围的高温将彻底缓解。

请注意根据天气变化及时调整出行和穿衣安排。
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",
        messages: [
            { role: "user", content: "杭州明天天气如何" }
        ],
        enable_search: true,
        search_options: {
            forced_search: true // 强制联网搜索
        }
    });
    console.log(completion.choices[0].message.content);
}

main();
```

###### 响应示例

```
根据现有资料，2025年9月17日（明天）杭州市的天气情况如下：

- **天气状况**：多云转晴，部分地区可能有小雨。
- **气温**：白天最高气温约30℃至34℃，夜间最低气温约24℃至26℃。
- **风力**：风力较小，一般为东风、东南风或西风，风速小于3级。
- **湿度**：相对湿度约77%。
- **空气质量**：良好，空气质量指数约为34至38。
- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。

此外，冷空气将于明天午后到夜里抵达浙江，开始逐渐带来降温，但高温仍会持续到当天午后。从18日开始，全省范围的高温将彻底缓解。

请注意根据天气变化及时调整出行和穿衣安排。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user",
            "content": "杭州明天天气如何"
        }
    ],
    "enable_search": true,
    "search_options": {
        "forced_search": true
    }
}'
```

###### 响应示例

```
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "根据已有资料，2025年9月17日（星期三）杭州的天气情况如下：\n\n- **天气状况**：多云转晴\n- **气温**：24℃ 至 30℃\n- **空气质量**：优\n- **风向与风力**：东风或东南风，1级\n- **湿度**：相对湿度60%（部分区域如拱墅、西湖等）或62%（下城）\n- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。\n- **其他提示**：当天午后到夜里，冷空气将抵达浙江，开始逐渐降温，但白天最高气温仍可达30℃左右。\n\n总体来看，9月17日杭州的天气较为舒适，白天以多云为主，夜间转晴，注意适时调整衣物。"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 3175,
    "completion_tokens": 188,
    "total_tokens": 3363,
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "created": 1758007390,
  "system_fingerprint": null,
  "model": "qwen-plus",
  "id": "chatcmpl-b709e5ff-ba5d-4afe-a93d-33b6962e232a"
}
```

#### DashScope

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "杭州明天天气是什么？"}],
    enable_search=True,
    search_options={
        "forced_search": True  # 强制联网搜索
    },
    result_format="message"
)
print(response["output"]["choices"][0]["message"]["content"])
```

###### 响应示例

```
根据现有资料，2025年9月17日（明天）杭州市的天气情况如下：

- **天气状况**：多云转晴，部分地区可能有小雨。
- **气温**：白天最高气温约30℃至34℃，夜间最低气温约24℃至26℃。
- **风力**：风力较小，一般为东风、东南风或西风，风速小于3级。
- **湿度**：相对湿度约77%。
- **空气质量**：良好，空气质量指数约为34至38。
- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。

此外，冷空气将于明天午后到夜里抵达浙江，开始逐渐带来降温，但高温仍会持续到当天午后。从18日开始，全省范围的高温将彻底缓解。

请注意根据天气变化及时调整出行和穿衣安排。
```

#### Java

```
// 建议 dashscope SDK的版本 >= 2.19.4
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.aigc.generation.SearchOptions;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import java.util.Arrays;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void main(String[] args) {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("明天杭州什么天气？")
                .build();

        SearchOptions searchOptions = SearchOptions.builder()
                .forcedSearch(true) // 强制联网搜索
                .build();

        GenerationParam param = GenerationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .messages(Arrays.asList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .enableSearch(true)
                .searchOptions(searchOptions)
                .build();
        try {
            GenerationResult result = gen.call(param);
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

###### 响应示例

```
根据现有资料，2025年9月17日（明天）杭州市的天气情况如下：

- **天气状况**：多云转晴，部分地区可能有小雨。
- **气温**：白天最高气温约30℃至34℃，夜间最低气温约24℃至26℃。
- **风力**：风力较小，一般为东风、东南风或西风，风速小于3级。
- **湿度**：相对湿度约77%。
- **空气质量**：良好，空气质量指数约为34至38。
- **穿衣建议**：建议穿棉麻面料的衬衫、薄长裙、薄T恤等清凉透气的衣服。

此外，冷空气将于明天午后到夜里抵达浙江，开始逐渐带来降温，但高温仍会持续到当天午后。从18日开始，全省范围的高温将彻底缓解。

请注意根据天气变化及时调整出行和穿衣安排。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "明天杭州天气如何？"
            }
        ]
    },
    "parameters": {
        "enable_search": true,
        "search_options": {
            "forced_search": true
        },
        "result_format": "message"
    }
}'
```

###### 响应示例

```
{
  "output": {
    "choices": [
      {
        "message": {
          "content": "根据现有资料，2025年9月17日（明天）杭州的天气预计将出现明显变化。冷空气将于17日午后到夜里抵达浙江，开始逐渐带来降温。虽然当天最高气温仍然较高，但已经开始降雨并伴随降温。\n\n具体预报如下：\n- **天气状况**：多云转小雨，部分地区可能会有明显阵雨或雷雨。\n- **气温**：白天最高气温预计在30℃至36℃之间，夜间开始降温。\n- **风力**：东北风或东风，风力较小，大约1-2级。\n- **空气质量**：良好，空气质量指数在30-38之间。\n- **穿衣建议**：建议穿轻薄透气的衣物，如棉麻面料的衬衫、短袖、薄长裙等。\n\n总体来看，17日将是天气由炎热转向凉爽的转折点，需要注意气温变化并适当调整衣物。",
          "role": "assistant"
        },
        "finish_reason": "stop"
      }
    ]
  },
  "usage": {
    "total_tokens": 4051,
    "output_tokens": 197,
    "input_tokens": 3854,
    "plugins": {
      "search": {
        "count": 1
      }
    },
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "request_id": "1b328f53-21d1-4b64-a543-201d367617b4"
}
```

### 获取并标注引用来源

联网搜索支持在响应中返回搜索来源链接，并通过角标标注引用出处，增强信息可追溯性。

1.  **开启返回搜索来源**: 设置 `enable_source: true`，响应的 `search_info` 字段将包含搜索结果列表。
    
2.  **开启角标标注**: 在 `enable_source` 为 `true` 的前提下，设置 `enable_citation: true`，模型回复内容中将出现类似 `[1]` 的角标。
    
3.  **设置角标样式**: 通过`citation_format`参数设置，可选值：
    
    -   `"[<number>]"` (默认): 样式为 `[1]`
    -   `"[ref_<number>]"`: 样式为 `[ref_1]`

**以上 enable\_source、enable\_citation、citation\_format 参数仅支持 DashScope 调用方式。**

> [Responses API 的联网搜索](https://help.aliyun.com/zh/model-studio/web-search#7b82860922v0y)：其搜索来源会在响应中自动返回（参见 [获取搜索来源](https://help.aliyun.com/zh/model-studio/web-search#ws_resp_get_sources)），但 Responses API 暂不支持上述 enable\_citation 角标标注（不会在回复内容中自动插入 `[1]` 角标）。

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "杭州明天天气是什么？"}],
    enable_search=True,
    search_options={
        "enable_source": True,       # 必须开启才能使用角标标注
        "enable_citation": True,     # 开启角标标注
        "citation_format": "[ref_<number>]", # 设置角标样式
    },
    result_format="message"
)

print("="*20 + "搜索结果" + "="*20)
for web in response.output.search_info["search_results"]:
    print(f"[{web['index']}]: [{web['title']}]({web['url']})")
print("="*20 + "回复内容" + "="*20)
print(response.output.choices[0].message.content)
```

###### 响应示例

```
====================搜索结果====================
[1]: [直降近10℃!刚刚确认:冷空气即将抵达,这波很猛](https://cj.sina.com.cn/articles/view/1665450974/6344c3de01901avjw)
[2]: [直降近10℃!刚刚确认:冷空气即将抵达,这波很猛](https://hznews.hangzhou.com.cn/chengshi/content/2025-09/15/content_9083259.htm)
[3]: [杭州市2025年9月份天气查询](https://www.ip.cn/tianqi/zhejiang/hangzhou/202509.html)
[4]: [40天天气预报](http://uc.src.weather.com.cn/mweather40d/index.shtml?10121010103A)
[5]: [杭州天气预报杭州2025年09月18日天气](https://tianqi.eastday.com/tianqi/hangzhou/20250918.html)
[6]: [杭州市2024年9月份天气查询](https://www.ip.cn/tianqi/zhejiang/hangzhou/202409.html)
[7]: [风里有了秋的味道,杭州人盼望已久的第一缕桂花香终于来了](https://baijiahao.baidu.com/s?id=1843471369098538519&wfr=spider&for=pc)
[8]: [余杭区2024年9月份天气历史记录](https://www.ip.cn/tianqi/zhejiang/hangzhou/yuhang/202409.html)
====================回复内容====================
根据最新的天气信息，杭州明天（2025年9月18日）的天气预计会是阴转多云，最高气温为28℃，最低气温24℃，风力较弱，有来自东北方向的风，风速约为2级。此外，空气湿度相对适中，紫外线强度弱，空气质量良好，适合外出活动，但建议关注最新的天气预报以获取更准确的信息[ref_5]。
```

#### Java

```
import com.alibaba.dashscope.aigc.generation.*;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import java.util.Arrays;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    public static void main(String[] args) {
        Generation gen = new Generation();
        Message userMsg = Message.builder()
                .role(Role.USER.getValue())
                .content("明天杭州什么天气？")
                .build();

        SearchOptions searchOptions = SearchOptions.builder()
                .enableSource(true)       // 必须开启才能使用角标标注
                .enableCitation(true)     // 开启角标标注
                .citationFormat("[ref_<number>]") // 设置角标样式
                .build();

        GenerationParam param = GenerationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .messages(Arrays.asList(userMsg))
                .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                .enableSearch(true)
                .searchOptions(searchOptions)
                .build();
        try {
            GenerationResult result = gen.call(param);
            System.out.println("=".repeat(20)+"搜索结果"+"=".repeat(20));
            System.out.println(result.getOutput().getSearchInfo().getSearchResults());
            System.out.println("=".repeat(20)+"回复内容"+"=".repeat(20));
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

###### 响应示例

```
====================搜索结果====================
[SearchInfo.SearchResult(siteName=新浪网, icon=https://mbs1.bdstatic.com/searchbox/mappconsole/image/20220307/88eb511c-5c51-448a-a9b5-df6b24cda8c7.png, index=1, title=直降近10℃!刚刚确认:冷空气即将抵达,这波很猛, url=https://cj.sina.com.cn/articles/view/1665450974/6344c3de01901avjw), SearchInfo.SearchResult(siteName=杭州网, icon=https://img.alicdn.com/imgextra/i1/O1CN01FcFnjf25PIbhq2c3q_!!6000000007518-73-tps-16-16.ico, index=2, title=直降近10℃!刚刚确认:冷空气即将抵达,这波很猛, url=https://hznews.hangzhou.com.cn/chengshi/content/2025-09/15/content_9083259.htm), SearchInfo.SearchResult(siteName=厦门时空科技有限公司, icon=http://www.ip.cn/favicon.ico, index=3, title=杭州市2025年9月份天气查询, url=https://www.ip.cn/tianqi/zhejiang/hangzhou/202509.html), SearchInfo.SearchResult(siteName=eastday, icon=https://img.alicdn.com/imgextra/i3/O1CN01kr9teP1wlRD8OH6TO_!!6000000006348-73-tps-16-16.ico, index=4, title=杭州天气预报杭州2025年09月18日天气, url=https://tianqi.eastday.com/tianqi/hangzhou/20250918.html), SearchInfo.SearchResult(siteName=无, icon=https://img.alicdn.com/imgextra/i2/O1CN01MJh8gM28s6MYPHsm6_!!6000000007987-2-tps-32-32.png, index=5, title=40天天气预报, url=http://uc.src.weather.com.cn/mweather40d/index.shtml?10121010103A), SearchInfo.SearchResult(siteName=厦门时空科技有限公司, icon=http://www.ip.cn/favicon.ico, index=6, title=杭州市2024年9月份天气查询, url=https://www.ip.cn/tianqi/zhejiang/hangzhou/202409.html), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=7, title=风里有了秋的味道,杭州人盼望已久的第一缕桂花香终于来了, url=https://baijiahao.baidu.com/s?id=1843471369098538519&wfr=spider&for=pc), SearchInfo.SearchResult(siteName=厦门时空科技有限公司, icon=http://www.ip.cn/favicon.ico, index=8, title=余杭区2024年9月份天气历史记录, url=https://www.ip.cn/tianqi/zhejiang/hangzhou/yuhang/202409.html)]
====================回复内容====================
根据最新天气预报，明天（2025年9月18日）杭州的天气将有明显变化。

受冷空气影响，杭州气温将大幅下降，预计最高气温仅28℃左右，与近日36℃的高温相比直降近10℃[ref_1][ref_5]。天气方面，预计会有一次明显的阵雨或雷雨过程，之后转为小雨转阴 [ref_3]。空气质量等级为优-良，首要污染物为臭氧（O3）[ref_无]。气象条件较一般，建议注意行车安全，并且不太适宜洗车[ref_无]。此外，紫外线强度较弱，但出门前仍建议涂擦防晒护肤品[ref_无]。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "明天杭州天气如何？"
            }
        ]
    },
    "parameters": {
        "enable_search": true,
        "search_options": {
            "enable_source": true,
            "enable_citation": true,
            "citation_format": "[ref_<number>]"
        },
        "result_format": "message"
    }
}'
```

###### 响应示例

```
{
  "output": {
    "choices": [
      {
        "message": {
          "content": "根据现有的信息，明天（2025年9月18日）杭州的天气预计会经历一次明显的降温，最高气温将下降近10℃，预计最高气温仅为28℃，甚至可能更低。不过，另一份资料指出当天的气温范围可能在24℃至34℃之间，天气状况为阴转多云，建议穿着清凉透气的衣物，如棉麻面料的衬衫、薄长裙或薄T恤等[ref_1][ref_5]。需要注意的是，尽管气温有所下降，但湿度较高，可能会感觉较为闷热。此外，由于之前几天的高温，这将是近期较为凉爽的一天。",
          "role": "assistant"
        },
        "finish_reason": "stop"
      }
    ],
    "search_info": {
      "extra_tool_info": [],
      "search_results": [
        {
          "icon": "https://mbs1.bdstatic.com/searchbox/mappconsole/image/20220307/88eb511c-5c51-448a-a9b5-df6b24cda8c7.png",
          "site_name": "新浪网",
          "index": 1,
          "title": "直降近10℃!刚刚确认:冷空气即将抵达,这波很猛",
          "url": "https://cj.sina.com.cn/articles/view/1665450974/6344c3de01901avjw"
        },
        {
          "icon": "https://img.alicdn.com/imgextra/i1/O1CN01FcFnjf25PIbhq2c3q_!!6000000007518-73-tps-16-16.ico",
          "site_name": "杭州网",
          "index": 2,
          "title": "直降近10℃!刚刚确认:冷空气即将抵达,这波很猛",
          "url": "https://hznews.hangzhou.com.cn/chengshi/content/2025-09/15/content_9083259.htm"
        },
        {
          "icon": "http://www.ip.cn/favicon.ico",
          "site_name": "厦门时空科技有限公司",
          "index": 3,
          "title": "杭州市2025年9月份天气查询",
          "url": "https://www.ip.cn/tianqi/zhejiang/hangzhou/202509.html"
        },
        {
          "icon": "https://img.alicdn.com/imgextra/i2/O1CN01MJh8gM28s6MYPHsm6_!!6000000007987-2-tps-32-32.png",
          "site_name": "无",
          "index": 4,
          "title": "40天天气预报",
          "url": "http://uc.src.weather.com.cn/mweather40d/index.shtml?10121010103A"
        },
        {
          "icon": "https://img.alicdn.com/imgextra/i3/O1CN01kr9teP1wlRD8OH6TO_!!6000000006348-73-tps-16-16.ico",
          "site_name": "eastday",
          "index": 5,
          "title": "杭州天气预报杭州2025年09月18日天气",
          "url": "https://tianqi.eastday.com/tianqi/hangzhou/20250918.html"
        },
        {
          "icon": "http://www.ip.cn/favicon.ico",
          "site_name": "厦门时空科技有限公司",
          "index": 6,
          "title": "杭州市2024年9月份天气查询",
          "url": "https://www.ip.cn/tianqi/zhejiang/hangzhou/202409.html"
        },
        {
          "icon": "https://baijiahao.baidu.com/favicon.ico",
          "site_name": "百家号",
          "index": 7,
          "title": "风里有了秋的味道,杭州人盼望已久的第一缕桂花香终于来了",
          "url": "https://baijiahao.baidu.com/s?id=1843471369098538519&wfr=spider&for=pc"
        },
        {
          "icon": "http://www.ip.cn/favicon.ico",
          "site_name": "厦门时空科技有限公司",
          "index": 8,
          "title": "余杭区2024年9月份天气历史记录",
          "url": "https://www.ip.cn/tianqi/zhejiang/hangzhou/yuhang/202409.html"
        }
      ]
    }
  },
  "usage": {
    "total_tokens": 3907,
    "output_tokens": 144,
    "input_tokens": 3763,
    "plugins": {
      "search": {
        "count": 1
      }
    },
    "prompt_tokens_details": {
      "cached_tokens": 0
    }
  },
  "request_id": "ae118381-a74b-4bda-8ef9-c451b5240e82"
}
```

### 开启垂域搜索

天气、股票等垂直领域查询对数据精度要求较高，通用网页搜索结果可能不够精确。

开启垂域搜索后，模型优先参考垂直领域数据源，返回更精准的结果。

设置`enable_search_extension`为`true`以开启此功能。

**可选值**:

-   `true`: 开启。
-   `false` （默认）: 不开启。

**支持的领域**：

**领域**

**说明**

**示例问题**

汇率

提供多币种间的最新汇率转换，支持标准货币代码。

人民币与美元的汇率

天气

提供实时、未来几天及历史天气数据。

杭州天气

股票

支持 A 股、港股、美股，可获取实时股价、前一交易日收盘价、历史趋势、30 日收盘价、股票代码或指数对应股价。

沪指昨天收盘点数

油价查询

实时查询全国各地区最新汽柴油价格，每日更新。

杭州油价

万年历

基于指定日期，提供农历、节气、节日及传统黄历中的吉凶宜忌等信息。

今天是农历几号

金价

提供最新价、开盘价、最高价、最低价等实时行情。

金价多少钱了

银价

提供最新价、开盘价、最高价、最低价等实时行情。

银价多少钱了

彩票

支持双色球、大乐透、排列3、排列5、七星彩、快乐8、3D 等主流彩票类型。

最新一期双色球开奖结果

电视剧

提供主流平台的电视剧资讯。

近期热播电视剧

电影

提供主流电影平台的最新资讯。

最近上映了哪些电影

车牌限行

根据车牌号查询当日限行规则。

浙Axxxxxx，今天是否在杭州限行

足球赛事

支持英超、西甲、德甲、意甲、法甲、中超、苏超等联赛的赛程与积分榜。

英超现在哪支球队排名第一

垂域搜索优先使用垂直领域数据源，但不能替代模型的日期推理能力。若在非交易日查询股价仍返回股价数据，需更换为 qwen3-max 或更新版本的模型。

#### OpenAI 兼容

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "阿里股价如何"},
    ],
    extra_body={
        "enable_search": True,
        "search_options": {"enable_search_extension": True},
    }
)
print(completion.choices[0].message.content)
```

###### 响应示例

```
截至2025年9月15日，阿里巴巴美股的收盘价为158.470美元。而在9月16日的实时信息中，阿里巴巴美股的价格为158.040美元，显示出股价在当天略有下降，日环比为1.92%。此外，与上个月相比，股价上涨了17.07%。

如果你需要更具体的实时股价信息，建议查看专业的股票市场平台或财经网站。
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",
        messages: [
            { role: "user", content: "阿里股价如何" }
        ],
        enable_search: true,
        search_options: {
            enable_search_extension: true
        }
    });
    console.log(completion.choices[0].message.content);
}

main();
```

###### 响应示例

```
截至2025年9月15日，阿里巴巴美股的收盘价为158.470美元。而在9月16日的实时信息中，阿里巴巴美股的价格为158.040美元，显示出股价在当天略有下降，日环比为1.92%。此外，与上个月相比，股价上涨了17.07%。

如果你需要更具体的实时股价信息，建议查看专业的股票市场平台或财经网站。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user",
            "content": "阿里股价如何"
        }
    ],
    "enable_search": true,
    "search_options": {
        "enable_search_extension": true
    }
}'
```

###### 响应示例

```
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "截至2025年9月16日，阿里巴巴股价表现强劲，持续创下阶段性新高，显示出市场对其未来发展的高度信心。\n\n**美股方面：**\n*   **实时股价**：根据最新数据，阿里巴巴美股（BABA）实时价格为 **158.040美元**。\n*   **近期表现**：上个交易日（9月15日）收盘价为155.060美元，当日上涨约1.92%。自9月10日以来，股价呈现加速上涨趋势，从约143.93美元一路攀升。\n*   **长期涨幅**：今年以来，阿里美股涨幅已超过90%，展现出远超大盘的强劲势头。\n\n**港股方面：**\n*   **股价新高**：在2025年9月15日，阿里巴巴港股（09988.HK）股价一度飙升至**156.8港元**，创下自2021年11月以来的最高点，盘中涨幅超过2%。\n*   **市场带动效应**：阿里股价的强势表现有效带动了整个港股科技板块的上扬，相关ETF基金也受到投资者热捧。\n\n**推动股价上涨的主要因素包括：**\n\n1.  **“高德扫街榜”引爆市场**：2025年9月10日，高德地图推出基于真实行程数据的“高德扫街榜”，上线首日用户数即突破4000万，被视为激活线下餐饮等实体商业的新解法，极大地提振了市场对阿里本地生活业务前景的预期。\n2.  **AI领域领先地位**：根据沙利文机构报告，阿里千问大模型在企业级应用中的调用量位居中国市场第一，占比达17.7%，彰显了其在人工智能领域的强大实力和商业化潜力。\n3.  **南向资金持续加码**：内地投资者通过港股通渠道对阿里巴巴进行了大额净买入。仅在9月1日至8日期间，净买入额就高达近187亿港元，位居所有港股标的之首，显示了强大的资金支持。\n4.  **宏观环境利好**：美联储降息预期升温，全球资金重新流向新兴市场，为以阿里为代表的中概股提供了有利的外部环境。\n\n综上所述，阿里巴巴股价正处于一个强劲的上升通道中，受产品创新、技术领先、资本青睐和宏观利好等多重因素驱动，被广泛视为当前港股科技板块的“领头羊”。"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 3500,
    "completion_tokens": 539,
    "total_tokens": 4039
  },
  "created": 1758018466,
  "system_fingerprint": null,
  "model": "qwen-plus",
  "id": "chatcmpl-d33caa81-34d8-472d-a201-9320124759d3"
}
```

#### DashScope

不支持通过DashScope Java SDK开启垂域搜索。

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "阿里巴巴股价多少"}],
    enable_search=True,
    search_options={
        "enable_search_extension": True,  # 开启垂域搜索
        "enable_source": True,
    },
    result_format="message"
)
# 增强信息在 search_info 的 extra_tool_info 字段中返回
print("="*20 + "垂域搜索结果" + "="*20)
for info in response.output.search_info["extra_tool_info"]:
    print(info["result"])
print("="*20 + "通用搜索结果" + "="*20)
for web in response.output.search_info["search_results"]:
    print(f"[{web['index']}]: [{web['title']}]({web['url']})")
print("="*20 + "回复内容" + "="*20)
print(response.output.choices[0].message.content)
```

###### 响应示例

```
====================垂域搜索结果====================
阿里巴巴美股：
实时价格162.210USD
上个交易日收盘价158.040USD
日环比%2.64%
月环比%20.16
日同比%96.14
月同比%55.79
历史价格列表[{"date":"2025-09-15","endPri":"158.040"},{"date":"2025-09-12","endPri":"155.060"},{"date":"2025-09-11","endPri":"155.440"},{"date":"2025-09-10","endPri":"143.930"},{"date":"2025-09-09","endPri":"147.100"},{"date":"2025-09-08","endPri":"141.200"},{"date":"2025-09-05","endPri":"135.580"},{"date":"2025-09-04","endPri":"130.920"},{"date":"2025-09-03","endPri":"136.450"},{"date":"2025-09-02","endPri":"138.550"},{"date":"2025-08-29","endPri":"135.000"},{"date":"2025-08-28","endPri":"119.570"},{"date":"2025-08-27","endPri":"122.230"},{"date":"2025-08-26","endPri":"124.190"},{"date":"2025-08-25","endPri":"124.350"},{"date":"2025-08-22","endPri":"122.940"},{"date":"2025-08-21","endPri":"118.090"},{"date":"2025-08-20","endPri":"119.490"},{"date":"2025-08-19","endPri":"119.990"},{"date":"2025-08-18","endPri":"121.400"},{"date":"2025-08-15","endPri":"121.260"},{"date":"2025-08-14","endPri":"122.280"},{"date":"2025-08-13","endPri":"126.860"},{"date":"2025-08-12","endPri":"122.420"},{"date":"2025-08-11","endPri":"118.640"},{"date":"2025-08-08","endPri":"120.360"},{"date":"2025-08-07","endPri":"120.960"},{"date":"2025-08-06","endPri":"120.860"},{"date":"2025-08-05","endPri":"117.040"},{"date":"2025-08-04","endPri":"117.500"}]

====================通用搜索结果====================
[1]: [-2025年09月10日,美股周二收盘,公司涨4.18%,收报147.10美元。近来,](https://xueqiu.com/9745910102/351820091)
[2]: [阿里巴巴暴涨超7%!港股科技50ETF(159750)高开涨超2%](https://baijiahao.baidu.com/s?id=1843045561840113640&wfr=spider&for=pc)
[3]: [A股震荡调整,成交缩水3000亿,恒指盘中突破26000点,百亿南向资金涌入阿里巴巴](https://baijiahao.baidu.com/s?id=1842797735656596493&wfr=spider&for=pc)
[4]: [2025阿里股价暴涨近90%原因解析](http://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_4372375544123651227)
[5]: [阿里巴巴美股大涨8% 业内认为后市仍有上涨空间](https://baijiahao.baidu.com/s?id=1843028040477540041&wfr=spider&for=pc)
[6]: [阿里巴巴-W盘中触及158.3港元,创近4年新高!机构为何集体看](http://finance.sina.com.cn/tech/roll/2025-09-12/doc-infqfnmi7601457.shtml)
[7]: [2025年09月10日阿里巴巴概念涨停板梳理](https://cj.sina.com.cn/articles/view/3240851740/c12b791c00101h5z8)
[8]: [阿里巴巴股价继续新高,珍惜港股科技右侧时间](https://baijiahao.baidu.com/s?id=1843297157083806691&wfr=spider&for=pc)
[9]: [港股异动|阿里巴巴-W(09988)涨超3%续刷近四年新高 月内股价已累涨近35%](https://baijiahao.baidu.com/s?id=1843300524259847917&wfr=spider&for=pc)
[10]: [2025年09月10日[阿里巴巴概念]涨停板金字塔](https://cj.sina.com.cn/articles/view/3240851740/c12b791c00101h5xk)
====================回复内容====================
根据最新的实时数据，截至2025年9月17日：

*   **阿里巴巴美股 (BABA)** 的实时价格为 **162.210美元**。

此外，相关股价信息还包括：
*   **上个交易日（9月15日）收盘价**：158.040美元
*   **日涨幅**：2.64%
*   **月涨幅**：20.16%

近期，阿里巴巴股价表现强劲，持续创下阶段性新高。其港股（09988.HK）也同步走强，在9月15日盘中一度涨至156.2港元，刷新了近四年来的高点。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "阿里巴巴的股价"
            }
        ]
    },
    "parameters": {
        "enable_search": true,
        "search_options": {
            "enable_search_extension": true,
            "enable_source": true
        },
        "result_format": "message"
    }
}'
```

###### 响应示例

```
{
  "output": {
    "choices": [
      {
        "message": {
          "content": "截至2025年9月16日，阿里巴巴的股价表现持续强劲，主要市场股价均创下近年来新高。\n\n**美股方面：**\n*   **实时价格**：158.040美元\n*   **上个交易日（9月15日）收盘价**：155.060美元\n*   **日内涨幅**：+1.92%\n*   **本月累计涨幅**：约17.07%\n*   **年内涨幅**：高达93.68%\n\n近期，阿里巴巴美股股价一路攀升。在9月15日早盘，股价一度触及158.47美元，刷新了自2022年以来的阶段高点。\n\n**港股方面 (阿里巴巴-W, 09988)：**\n*   根据最新数据（9月15日），港股阿里股价最高触及156.8港元，续刷近四年新高。\n*   当日报收于156.2港元，单日上涨3.38%。\n*   仅在9月份内，股价已累计上涨近35%。\n\n**股价上涨驱动因素：**\n1.  **强劲财报表现**：公司2025年第二季度（截至6月30日）财报显示，营收同比增长2%，净利润同比大幅增长76%，达到423.82亿元，超出市场预期。\n2.  **机构普遍看好**：摩根大通、花旗等多家国际投行集体上调阿里巴巴目标价，其中最高目标价被看至198美元，显示出对后市的乐观预期。\n3.  **资金持续流入**：南向资金（内地投资者通过港股通）在9月初连续多个交易日大举净买入阿里巴巴，六个交易日内净买入额高达186.93亿港元，位居所有标的之首，为股价提供了强有力的支撑。\n4.  **市场情绪回暖**：阿里巴巴股价的强势反弹也带动了整个“阿里巴巴概念股”板块的活跃，并引领港股科技板块整体走强。\n\n综上所述，阿里巴巴股价在2025年下半年迎来了显著的估值修复和强劲上涨，无论是从基本面、机构观点还是资金流向来看，都呈现出积极的态势。",
          "role": "assistant"
        },
        "finish_reason": "stop"
      }
    ],
    "search_info": {
      "extra_tool_info": [
        {
          "result": "阿里巴巴美股：\n实时价格158.040USD\n上个交易日收盘价155.060USD\n日环比%1.92%\n月环比%17.07\n日同比%93.68\n月同比%51.79\n历史价格列表[{\"date\":\"2025-09-15\",\"endPri\":\"158.470\"},{\"date\":\"2025-09-12\",\"endPri\":\"155.060\"},{\"date\":\"2025-09-11\",\"endPri\":\"155.440\"},{\"date\":\"2025-09-10\",\"endPri\":\"143.930\"},{\"date\":\"2025-09-09\",\"endPri\":\"147.100\"},{\"date\":\"2025-09-08\",\"endPri\":\"141.200\"},{\"date\":\"2025-09-05\",\"endPri\":\"135.580\"},{\"date\":\"2025-09-04\",\"endPri\":\"130.920\"},{\"date\":\"2025-09-03\",\"endPri\":\"136.450\"},{\"date\":\"2025-09-02\",\"endPri\":\"138.550\"},{\"date\":\"2025-08-29\",\"endPri\":\"135.000\"},{\"date\":\"2025-08-28\",\"endPri\":\"119.570\"},{\"date\":\"2025-08-27\",\"endPri\":\"122.230\"},{\"date\":\"2025-08-26\",\"endPri\":\"124.190\"},{\"date\":\"2025-08-25\",\"endPri\":\"124.350\"},{\"date\":\"2025-08-22\",\"endPri\":\"122.940\"},{\"date\":\"2025-08-21\",\"endPri\":\"118.090\"},{\"date\":\"2025-08-20\",\"endPri\":\"119.490\"},{\"date\":\"2025-08-19\",\"endPri\":\"119.990\"},{\"date\":\"2025-08-18\",\"endPri\":\"121.400\"},{\"date\":\"2025-08-15\",\"endPri\":\"121.260\"},{\"date\":\"2025-08-14\",\"endPri\":\"122.280\"},{\"date\":\"2025-08-13\",\"endPri\":\"126.860\"},{\"date\":\"2025-08-12\",\"endPri\":\"122.420\"},{\"date\":\"2025-08-11\",\"endPri\":\"118.640\"},{\"date\":\"2025-08-08\",\"endPri\":\"120.360\"},{\"date\":\"2025-08-07\",\"endPri\":\"120.960\"},{\"date\":\"2025-08-06\",\"endPri\":\"120.860\"},{\"date\":\"2025-08-05\",\"endPri\":\"117.040\"},{\"date\":\"2025-08-04\",\"endPri\":\"117.500\"}]\n\n",
          "tool": "stock"
        }
      ],
      "search_results": [
        {
          "site_name": "无",
          "icon": "https://b.bdstatic.com/searchbox/mappconsole/image/20190805/1239163c-77cc-449e-b91f-9bb1d27e43a7.png",
          "index": 1,
          "title": "-2025年09月10日,美股周二收盘,公司涨4.18%,收报147.10美元。近来,",
          "url": "https://xueqiu.com/9745910102/351820091"
        },
        {
          "site_name": "百家号",
          "icon": "https://baijiahao.baidu.com/favicon.ico",
          "index": 2,
          "title": "阿里巴巴暴涨超7%!港股科技50ETF(159750)高开涨超2%",
          "url": "https://baijiahao.baidu.com/s?id=1843045561840113640&wfr=spider&for=pc"
        },
        {
          "site_name": "百家号",
          "icon": "https://baijiahao.baidu.com/favicon.ico",
          "index": 3,
          "title": "阿里巴巴美股大涨8% 业内认为后市仍有上涨空间",
          "url": "https://baijiahao.baidu.com/s?id=1843028040477540041&wfr=spider&for=pc"
        },
        {
          "site_name": "百家号",
          "icon": "https://baijiahao.baidu.com/favicon.ico",
          "index": 4,
          "title": "A股震荡调整,成交缩水3000亿,恒指盘中突破26000点,百亿南向资金涌入阿里巴巴",
          "url": "https://baijiahao.baidu.com/s?id=1842797735656596493&wfr=spider&for=pc"
        },
        {
          "site_name": "百度",
          "icon": "https://mbs1.bdstatic.com/searchbox/mappconsole/image/20220222/0e49bbbc-0ab7-475f-ad6b-cab96f47cf42.png",
          "index": 5,
          "title": "2025阿里股价暴涨近90%原因解析",
          "url": "http://mbd.baidu.com/newspage/data/dtlandingsuper?nid=dt_4372375544123651227"
        },
        {
          "site_name": "百家号",
          "icon": "https://baijiahao.baidu.com/favicon.ico",
          "index": 6,
          "title": "阿里巴巴股价继续新高,珍惜港股科技右侧时间",
          "url": "https://baijiahao.baidu.com/s?id=1843297157083806691&wfr=spider&for=pc"
        },
        {
          "site_name": "新浪网",
          "icon": "https://mbs1.bdstatic.com/searchbox/mappconsole/image/20220307/88eb511c-5c51-448a-a9b5-df6b24cda8c7.png",
          "index": 7,
          "title": "2025年09月10日[阿里巴巴概念]涨停板金字塔",
          "url": "https://cj.sina.com.cn/articles/view/3240851740/c12b791c00101h5xk"
        },
        {
          "site_name": "新浪网",
          "icon": "https://mbs1.bdstatic.com/searchbox/mappconsole/image/20220307/88eb511c-5c51-448a-a9b5-df6b24cda8c7.png",
          "index": 8,
          "title": "2025年09月10日阿里巴巴概念涨停板梳理",
          "url": "https://cj.sina.com.cn/articles/view/3240851740/c12b791c00101h5z8"
        },
        {
          "site_name": "新浪网",
          "icon": "https://mbs1.bdstatic.com/searchbox/mappconsole/image/20230828/6ad81bbb-a34d-468e-9756-bcf9c370a8a4.png",
          "index": 9,
          "title": "阿里巴巴-W盘中触及158.3港元,创近4年新高!机构为何集体看",
          "url": "http://finance.sina.com.cn/tech/roll/2025-09-12/doc-infqfnmi7601457.shtml"
        },
        {
          "site_name": "百家号",
          "icon": "https://baijiahao.baidu.com/favicon.ico",
          "index": 10,
          "title": "港股异动|阿里巴巴-W(09988)涨超3%续刷近四年新高 月内股价已累涨近35%",
          "url": "https://baijiahao.baidu.com/s?id=1843300524259847917&wfr=spider&for=pc"
        }
      ]
    }
  },
  "usage": {
    "total_tokens": 2664,
    "output_tokens": 486,
    "input_tokens": 2178,
    "plugins": {
      "search": {
        "count": 1
      }
    }
  },
  "request_id": "f52d05cc-36a6-45c2-adfe-dfcb9b7fea56"
}
```

### 设置搜索时效性

查询近期新闻或最新动态时，可通过 `freshness` 参数限制搜索时间范围，过滤过期网页。

**可选值**:

-   `7`: 仅检索最近 7 天内的内容
-   `30`: 仅检索最近 30 天内的内容
-   `180`: 仅检索最近 180 天内的内容
-   `365`: 仅检索最近 365 天内的内容
-   不设置（默认）: 不限制时间范围

**生效条件**:

-   仅对 `search_strategy: turbo` 生效
-   支持模型：qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23、qwen-plus、qwen-flash、qwen-plus-character、qwen-flash-character、qwen-flash-character-2026-02-26

#### OpenAI 兼容

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "最近AI领域有哪些重大新闻?"},
    ],
    extra_body={
        "enable_search": True,
        "search_options": {
            "search_strategy": "turbo",
            "freshness": 7  # 仅检索最近7天内的内容
        }
    }
)
print(completion.choices[0].message.content)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",
        messages: [
            { role: "user", content: "最近AI领域有哪些重大新闻?" }
        ],
        enable_search: true,
        search_options: {
            search_strategy: "turbo",
            freshness: 7  // 仅检索最近7天内的内容
        }
    });
    console.log(completion.choices[0].message.content);
}

main();
```

curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen-plus",
  "messages": [
    {
      "role": "user",
      "content": "最近AI领域有哪些重大新闻?"
    }
  ],
  "enable_search": true,
  "search_options": {
    "search_strategy": "turbo",
    "freshness": 7
  }
}'
```

#### DashScope

不支持通过DashScope Java SDK设置搜索时效性。

Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "最近AI领域有哪些重大新闻?"}],
    enable_search=True,
    search_options={
        "search_strategy": "turbo",
        "enable_source": True,
        "freshness": 7  # 仅检索最近7天内的内容
    },
    result_format="message"
)
print("="*20 + "搜索结果" + "="*20)
for web in response.output.search_info["search_results"]:
    print(f"[{web['index']}]: [{web['title']}]({web['url']})")
print("="*20 + "回复内容" + "="*20)
print(response.output.choices[0].message.content)
```

curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen-plus",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": "最近AI领域有哪些重大新闻?"
      }
    ]
  },
  "parameters": {
    "enable_search": true,
    "search_options": {
      "search_strategy": "turbo",
      "enable_source": true,
      "freshness": 7
    },
    "result_format": "message"
  }
}'
```

### 限定搜索来源站点

需要将搜索限定在特定网站（如官方站点或权威媒体）时，可使用 `assigned_site_list` 参数限定来源。启用后，搜索将严格限于指定网站列表。

**功能限制**：

-   仅在 `search_strategy` 设为 `turbo` 时生效；
    
-   适用于以下模型：
    
    -   千问 Max 系列：`qwen3-max`、`qwen3-max-preview`、`qwen3-max-2025-09-23` 及之后的快照版本
    -   千问 Plus 系列：`qwen-plus`
    -   千问 Flash 系列：`qwen-flash`
    -   角色扮演模型：`qwen-plus-character`、`qwen-flash-character`、`qwen-flash-character-2026-02-26`
-   最多配置25个站点。
    

`assigned_site_list` 参数默认值为`[]`，表示不限制来源。

> 当指定站点内无相关内容时，搜索结果可能为空，模型将使用自身知识回答。

#### OpenAI 兼容

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "北京有哪些热门新闻？"},
    ],
    extra_body={
        "enable_search": True,
        "search_options": {
            "search_strategy": "turbo",
            "assigned_site_list": ["baidu.com", "sina.cn"]  # 仅从指定站点检索
        }
    }
)
print(completion.choices[0].message.content)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",
        messages: [
            { role: "user", content: "北京有哪些热门新闻？" }
        ],
        enable_search: true,
        search_options: {
            search_strategy: "turbo",
            assigned_site_list: ["baidu.com", "sina.cn"]  // 仅从指定站点检索
        }
    });
    console.log(completion.choices[0].message.content);
}

main();
```

curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen-plus",
  "messages": [
    {
      "role": "user",
      "content": "北京有哪些热门新闻？"
    }
  ],
  "enable_search": true,
  "search_options": {
    "search_strategy": "turbo",
    "assigned_site_list": ["baidu.com", "sina.cn"]
  }
}'
```

#### DashScope

不支持通过DashScope Java SDK限定搜索来源站点。

Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "北京有哪些热门新闻？"}],
    enable_search=True,
    search_options={
        "search_strategy": "turbo",
        "enable_source": True,
        "assigned_site_list": ["baidu.com", "sina.cn"]  # 仅从指定站点检索
    },
    result_format="message"
)
print("="*20 + "搜索结果" + "="*20)
for web in response.output.search_info["search_results"]:
    print(f"[{web['index']}]: [{web['title']}]({web['url']})")
print("="*20 + "回复内容" + "="*20)
print(response.output.choices[0].message.content)
```

curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen-plus",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": "北京有哪些热门新闻？"
      }
    ]
  },
  "parameters": {
    "enable_search": true,
    "search_options": {
      "search_strategy": "turbo",
      "enable_source": true,
      "assigned_site_list": ["baidu.com", "sina.cn"]
    },
    "result_format": "message"
  }
}'
```

### 通过自然语言控制检索范围

通过 `prompt_intervene` 参数，可用自然语言指定搜索范围（如仅检索特定主题或地域），系统据此进行针对性检索。

**支持模型**：qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23、qwen-plus、qwen-flash、qwen-plus-character、qwen-flash-character、qwen-flash-character-2026-02-26

`prompt_intervene` 只能指定检索范围，无法弥补模型推理能力的不足。若在非交易日查询股价仍返回股价数据，需更换模型解决。

#### OpenAI 兼容

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "智能科技发展现状"},
    ],
    extra_body={
        "enable_search": True,
        "search_options": {
            "search_strategy": "turbo",
            "intention_options": {
                "prompt_intervene": "仅检索AI技术相关内容"
            }
        }
    }
)
print(completion.choices[0].message.content)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus",
        messages: [
            { role: "user", content: "智能科技发展现状" }
        ],
        enable_search: true,
        search_options: {
            search_strategy: "turbo",
            intention_options: {
                prompt_intervene: "仅检索AI技术相关内容"
            }
        }
    });
    console.log(completion.choices[0].message.content);
}

main();
```

curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen-plus",
  "messages": [
    {
      "role": "user",
      "content": "智能科技发展现状"
    }
  ],
  "enable_search": true,
  "search_options": {
    "search_strategy": "turbo",
    "intention_options": {
      "prompt_intervene": "仅检索AI技术相关内容"
    }
  }
}'
```

#### DashScope

不支持DashScope Java SDK。

Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "智能科技发展现状"}],
    enable_search=True,
    search_options={
        "search_strategy": "turbo",
        "enable_source": True,
        "intention_options": {
            "prompt_intervene": "仅检索AI技术相关内容"
        }
    },
    result_format="message"
)
print("="*20 + "搜索结果" + "="*20)
for web in response.output.search_info["search_results"]:
    print(f"[{web['index']}]: [{web['title']}]({web['url']})")
print("="*20 + "回复内容" + "="*20)
print(response.output.choices[0].message.content)
```

curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "model": "qwen-plus",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": "智能科技发展现状"
      }
    ]
  },
  "parameters": {
    "enable_search": true,
    "search_options": {
      "search_strategy": "turbo",
      "enable_source": true,
      "intention_options": {
        "prompt_intervene": "仅检索AI技术相关内容"
      }
    },
    "result_format": "message"
  }
}'
```

### 提前返回搜索来源

流式输出场景下，搜索结果就绪到首个数据块发送之间通常有 0.5 秒以上延迟。启用此功能可在搜索完成后立即返回搜索来源，降低首包延时。设置 `prepend_search_result` 为 `true`以启用此功能。

**可选值**:

-   `true`：首个数据包仅包含搜索来源，模型回复在后续数据包中。
-   `false` (默认）：首个数据包会包含搜索来源和模型回复的起始部分。

不支持 OpenAI 兼容方式与 DashScope Java SDK调用。

#### Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
responses = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "杭州明天天气是什么？"}],
    enable_search=True,
    search_options={
        "enable_source": True,
        "prepend_search_result": True,  # 首包只返回搜索来源
    },
    result_format="message",
    stream=True,
    incremental_output=True
)

first_chunk = True
for resp in responses:
    if first_chunk:
        search_info = resp.output.get("search_info", {})
        if search_info:
            print("=" * 20 + f"已阅读{len(search_info['search_results'])}个页面" + "=" * 20)
            for web in search_info["search_results"]:
                print(f"[{web['index']}]: [{web['title']}]({web['url']})")
            first_chunk = False
            print("=" * 20 + "回复内容" + "=" * 20)

    content = resp.output.choices[0].message.content
    print(content, end='')
```

##### 响应示例

```
====================已阅读8个页面====================
[1]: [直降近10℃!刚刚确认:冷空气即将抵达,这波很猛](https://cj.sina.com.cn/articles/view/1665450974/6344c3de01901avjw)
[2]: [直降近10℃!刚刚确认:冷空气即将抵达,这波很猛](https://hznews.hangzhou.com.cn/chengshi/content/2025-09/15/content_9083259.htm)
[3]: [杭州市2025年9月份天气查询](https://www.ip.cn/tianqi/zhejiang/hangzhou/202509.html)
[4]: [40天天气预报](http://uc.src.weather.com.cn/mweather40d/index.shtml?10121010103A)
[5]: [杭州天气预报杭州2025年09月18日天气](https://tianqi.eastday.com/tianqi/hangzhou/20250918.html)
[6]: [杭州市2024年9月份天气查询](https://www.ip.cn/tianqi/zhejiang/hangzhou/202409.html)
[7]: [风里有了秋的味道,杭州人盼望已久的第一缕桂花香终于来了](https://baijiahao.baidu.com/s?id=1843471369098538519&wfr=spider&for=pc)
[8]: [余杭区2024年9月份天气历史记录](https://www.ip.cn/tianqi/zhejiang/hangzhou/yuhang/202409.html)
====================回复内容====================
根据2025年9月17日的天气信息，杭州明天（9月18日）的天气情况如下：

**小雨转阴，气温较低。**
*   **天气状况**: 白天有小雨，之后转为阴天。
*   **气温**: 最高气温约 **26℃**，最低气温约 **22℃**。
*   **风力**: 白天有东北风。

**天气特点**：
受冷空气影响，杭州将迎来一次明显的降温过程。与前几日35℃以上的高温相比，明天最高气温将大幅下降近10℃，体感会凉爽许多。预计这次降温后，直到25日之前都不会再出现高温天气了。
```

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "明天杭州天气如何？"
            }
        ]
    },
    "parameters": {
        "enable_search": true,
        "incremental_output": true,
        "result_format": "message",
        "search_options": {
            "enable_source": true,
            "prepend_search_result": true
        }
    }
}'
```

##### 响应示例

```
id:1
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","role":"assistant"},"finish_reason":"null"}],"search_info":{"search_results":[{"site_name":"百家号","icon":"https://baijiahao.baidu.com/favicon.ico","index":1,"title":"全年高温日数可能创新高,杭州何时能“熄火”?","url":"https://baijiahao.baidu.com/s?id=1843390963791748953&wfr=spider&for=pc"},{"site_name":"eastday","icon":"https://img.alicdn.com/imgextra/i3/O1CN01kr9teP1wlRD8OH6TO_!!6000000006348-73-tps-16-16.ico","index":2,"title":"杭州天气预报杭州2025年09月17日天气","url":"https://tianqi.eastday.com/tianqi/hangzhou/20250917.html"},{"site_name":"百家号","icon":"https://baijiahao.baidu.com/favicon.ico","index":3,"title":"就在这一天,冷空气带来降温,高温终于要彻底终结","url":"https://baijiahao.baidu.com/s?id=1843310716677051952&wfr=spider&for=pc"},{"site_name":"eastday","icon":"https://img.alicdn.com/imgextra/i3/O1CN01kr9teP1wlRD8OH6TO_!!6000000006348-73-tps-16-16.ico","index":4,"title":"下城天气预报杭州下城2025年09月17日天气","url":"https://tianqi.eastday.com/tianqi/xiachengqu/20250917.html"},{"site_name":"eastday","icon":"https://img.alicdn.com/imgextra/i3/O1CN01kr9teP1wlRD8OH6TO_!!6000000006348-73-tps-16-16.ico","index":5,"title":"江干天气预报杭州江干2025年09月17日天气","url":"https://tianqi.eastday.com/tianqi/jiangganqu/20250917.html"},{"site_name":"无","icon":"","index":6,"title":"杭州今日天气小雨转晴 2025年9月17日杭州市天气预报","url":"http://m.tqw5.com/shenghuo_8076477/"},{"site_name":"eastday","icon":"https://img.alicdn.com/imgextra/i3/O1CN01kr9teP1wlRD8OH6TO_!!6000000006348-73-tps-16-16.ico","index":7,"title":"拱墅天气预报杭州拱墅2025年09月17日天气","url":"https://tianqi.eastday.com/tianqi/gongshuqu/20250917.html"},{"site_name":"eastday","icon":"https://img.alicdn.com/imgextra/i3/O1CN01kr9teP1wlRD8OH6TO_!!6000000006348-73-tps-16-16.ico","index":8,"title":"西湖天气预报杭州西湖2025年09月17日天气","url":"https://tianqi.eastday.com/tianqi/xihu/20250917.html"},{"site_name":"网易","icon":"https://ss1.baidu.com/6ONXsjip0QIZ8tyhnq/it/u=1534926245,1016405979&fm=195&app=88&f=JPEG?w=200&h=200","index":9,"title":"杭州三日游攻略|宋韵茶香与湖山秘境","url":"https://www.163.com/dy/article/K9GSR7HE0556F537.html"},{"site_name":"百家号","icon":"https://baijiahao.baidu.com/favicon.ico","index":10,"title":"确认了!冷空气赶来,萧山终于要降温了!","url":"http://baijiahao.baidu.com/s?id=1843333073020602778&wfr=spider&for=pc"}]}},"usage":{},"request_id":"785ed962-fa29-4c7e-bed2-7fe0fdbfdc6c"}

id:2
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"根据","role":"assistant"},"finish_reason":"null"}],"search_info":{"extra_tool_info":[],"search_results":[]}},"usage":{"total_tokens":2941,"output_tokens":1,"input_tokens":2940,"plugins":{"search":{"count":1}},"prompt_tokens_details":{"cached_tokens":0}},"request_id":"785ed962-fa29-4c7e-bed2-7fe0fdbfdc6c"}

id:3
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"现有","role":"assistant"},"finish_reason":"null"}],"search_info":{"extra_tool_info":[],"search_results":[]}},"usage":{"total_tokens":2942,"output_tokens":2,"input_tokens":2940,"plugins":{"search":{"count":1}},"prompt_tokens_details":{"cached_tokens":0}},"request_id":"785ed962-fa29-4c7e-bed2-7fe0fdbfdc6c"}

...

id:64
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"建议根据天气变化调整","role":"assistant"},"finish_reason":"null"}],"search_info":{"extra_tool_info":[],"search_results":[]}},"usage":{"total_tokens":3221,"output_tokens":281,"input_tokens":2940,"plugins":{"search":{"count":1}},"prompt_tokens_details":{"cached_tokens":0}},"request_id":"785ed962-fa29-4c7e-bed2-7fe0fdbfdc6c"}

id:65
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"出行安排。","role":"assistant"},"finish_reason":"null"}],"search_info":{"extra_tool_info":[],"search_results":[]}},"usage":{"total_tokens":3224,"output_tokens":284,"input_tokens":2940,"plugins":{"search":{"count":1}},"prompt_tokens_details":{"cached_tokens":0}},"request_id":"785ed962-fa29-4c7e-bed2-7fe0fdbfdc6c"}

id:66
event:result
:HTTP_STATUS/200
data:{"output":{"choices":[{"message":{"content":"","role":"assistant"},"finish_reason":"stop"}],"search_info":{"extra_tool_info":[],"search_results":[]}},"usage":{"total_tokens":3224,"output_tokens":284,"input_tokens":2940,"plugins":{"search":{"count":1}},"prompt_tokens_details":{"cached_tokens":0}},"request_id":"785ed962-fa29-4c7e-bed2-7fe0fdbfdc6c"}
```

### 图文混合输出

设置 `enable_text_image_mixed: true` 可启用图文混合输出。启用后，模型会在回复中嵌入相关图片。

**示例效果**：

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6728878671/p1045875.png)

**支持的模型**：qwen-max、qwen-plus-latest、qwen-flash

**该参数与 enable\_search 相互独立，无需同时启用。**

**图片返回格式**：模型返回的图片以 HTML `<img>` 标签形式嵌入回复内容中。如需在前端展示，可直接渲染 HTML，或将其转换为 Markdown 格式。

```
<!-- 模型返回的图片格式示例 -->
<p align="center">
<img src="https://example.com/image.jpg" alt="图片描述" width="400" height="auto">
</p>
```

以下示例代码展示如何启用图文混合输出功能。

#### OpenAI 兼容

Python

```
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
completion = client.chat.completions.create(
    model="qwen-plus-latest",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "介绍一下杭州西湖"},
    ],
    # 启用图文混合输出
    extra_body={"enable_text_image_mixed": True}
)
print(completion.choices[0].message.content)
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const completion = await openai.chat.completions.create({
        model: "qwen-plus-latest",
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "介绍一下杭州西湖" }
        ],
        // 启用图文混合输出
        enable_text_image_mixed: true
    });
    console.log(completion.choices[0].message.content);
}

main();
```

curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus-latest",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "介绍一下杭州西湖"
        }
    ],
    "enable_text_image_mixed": true
}'
```

#### DashScope

不支持DashScope Java SDK。

Python

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus-latest",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "介绍一下杭州西湖"},
    ],
    # 启用图文混合输出
    enable_text_image_mixed=True,
    result_format="message"
)
print(response["output"]["choices"][0]["message"]["content"])
```

curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus-latest",
    "input": {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "介绍一下杭州西湖"
            }
        ]
    },
    "parameters": {
        "enable_text_image_mixed": true,
        "result_format": "message"
    }
}'
```

## 思考模型的联网搜索

前文的示例中，模型获取搜索结果后直接回复。这适用于事实性强、时效要求高的简单查询（如“杭州明天天气如何”）。但面对行业趋势分析、多源信息整合或报告撰写等复杂任务，模型难以给出高质量回答。可改用深度思考模型：获取检索内容后，先推理，再生成回复，可显著提升复杂任务的回答质量。

推理路径对用户可见，便于理解回复如何从检索信息中推导得出。

支持联网搜索，且具有深度思考能力的模型包括：

-   **千问**
    -   千问Max**：**qwen3-max、qwen3-max-2026-01-23、qwen3-max-preview
    -   千问Plus：qwen-plus、qwen-plus-latest、qwen-plus-2025-07-14及之后的快照版本
    -   千问Flash：qwen-flash、qwen-flash-2025-07-28及之后的快照版本
    -   千问Turbo：qwen-turbo
    -   QwQ：qwq-plus
-   **DeepSeek**：deepseek-v4-pro、deepseek-v4-flash、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1、deepseek-r1-0528、deepseek-r1
    

> 思考模型详情参见： [深度思考](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md) 。

#### OpenAI兼容

#### Python

### 示例代码

```
from openai import OpenAI
import os

# 初始化OpenAI客户端
client = OpenAI(
    # 如果没有配置环境变量，请用阿里云百炼API Key替换：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

reasoning_content = ""  # 定义完整思考过程
answer_content = ""  # 定义完整回复
is_answering = False  # 判断是否结束思考过程并开始回复

# 创建聊天完成请求
completion = client.chat.completions.create(
    # 此处以qwen-plus为例，可更换为其它支持联网搜索的深度思考模型
    model="qwen-plus",
    messages=[{"role": "user", "content": "请你结合近期的AI热点新闻，预测一下AI的发展趋势"}],
    extra_body={
        "enable_thinking": True,
        "enable_search": True,  # 开启联网搜索的参数
        "search_options": {
            "forced_search": True,  # 强制联网搜索的参数
            "search_strategy": "max"
        },
    },
    stream=True,
    stream_options={"include_usage": True}
)

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\n" + "=" * 20 + "Usage" + "=" * 20)
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, "reasoning_content") and delta.reasoning_content != None:
            print(delta.reasoning_content, end="", flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            if delta.content:
                print(delta.content, end="", flush=True)
                answer_content += delta.content

# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(reasoning_content)
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(answer_content)
```

### 返回结果

```
====================思考过程====================

我需要基于知识库中的AI热点新闻来预测AI的发展趋势。让我先分析一下知识库中的内容，找出近期的AI热点新闻和相关趋势。

从知识库中，我可以看到几条与AI相关的新闻：
...
我将基于这些信息，提供一个关于AI发展趋势的预测性回答。
====================完整回复====================

# AI发展趋势预测：从热点新闻看未来方向
根据近期AI热点新闻分析，我认为AI发展将呈现以下重要趋势：
...
AI发展正从"技术驱动"向"需求驱动"转变，更加注重解决实际问题和提升用户体验。随着技术成熟和应用场景拓展，AI将更深入地融入日常生活，但人性化、情感化的设计将成为关键差异化因素。正如"银发+AI"报告所强调的，技术终将服务于人，而非取代人与人之间的情感连接。
未来AI发展的核心将是在提升效率的同时，保持并增强人与人之间的情感纽带，实现技术与人文的和谐共生。
====================Usage====================
CompletionUsage(completion_tokens=1683, prompt_tokens=2688, total_tokens=4371, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=1022, rejected_prediction_tokens=None), prompt_tokens_details=PromptTokensDetails(audio_tokens=None, cached_tokens=0))
```

#### Node.js

### 示例代码

```
import OpenAI from "openai";
import process from 'process';

// 初始化 openai 客户端
const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1'
});

let reasoningContent = '';
let answerContent = '';
let isAnswering = false;

async function main() {
    try {
        const stream = await openai.chat.completions.create({
            model: 'qwen-plus',
            messages: [{ role: 'user', content: '请你结合近期的AI热点新闻，预测一下AI的发展趋势' }],
            enable_thinking: true,
            enable_search: true, // 开启联网搜索的参数
            search_options: {
                forced_search: true // 强制联网搜索的参数
            },
            stream: true,
            stream_options: {
                include_usage: true
            }
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');
        for await (const chunk of stream) {
            if (!chunk.choices?.length) {
                console.log('\n' + '='.repeat(20) + 'usage' + '='.repeat(20) + '\n');
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
            else if (delta.content) {
                if (!isAnswering) {
                    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                    isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
main();
```

### 返回结果

```
====================思考过程====================

我需要基于知识库中的AI热点新闻来预测AI的发展趋势。让我先分析一下知识库中的内容，找出近期的AI热点新闻和相关趋势。

从知识库中，我可以看到几条与AI相关的新闻：
...
我将基于这些信息，提供一个关于AI发展趋势的预测性回答。
====================完整回复====================

# AI发展趋势预测：从热点新闻看未来方向
根据近期AI热点新闻分析，我认为AI发展将呈现以下重要趋势：
...
AI发展正从"技术驱动"向"需求驱动"转变，更加注重解决实际问题和提升用户体验。随着技术成熟和应用场景拓展，AI将更深入地融入日常生活，但人性化、情感化的设计将成为关键差异化因素。正如"银发+AI"报告所强调的，技术终将服务于人，而非取代人与人之间的情感连接。
未来AI发展的核心将是在提升效率的同时，保持并增强人与人之间的情感纽带，实现技术与人文的和谐共生。
====================Usage====================
{
  prompt_tokens: 4268,
  completion_tokens: 2446,
  total_tokens: 6714,
  completion_tokens_details: { reasoning_tokens: 1164 },
  prompt_tokens_details: { cached_tokens: 0 }
}
```

#### HTTP

### 示例代码

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-plus",
    "messages": [
        {
            "role": "user",
            "content": "请你结合近期的AI热点新闻，预测一下AI的发展趋势"
        }
    ],
    "enable_thinking": true,
    "enable_search": true,
    "search_options": {
        "forced_search": true
    },
    "stream": true,
    "stream_options": {
        "include_usage": true
    }
}'
```

#### DashScope

#### Python

### 示例代码

```
import os
import dashscope

# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
messages = [
    {'role': 'user', 'content': '基于近期AI热点新闻，预测AI的发展趋势'}
]

response = dashscope.Generation.call(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen-plus",
    messages=messages,
    enable_thinking = True,
    enable_search = True, # 开启联网搜索的参数
    search_options = {
        "forced_search": True, # 强制开启联网搜索
        "enable_source": True, # 使返回结果包含搜索来源的信息，OpenAI 兼容方式暂不支持返回
        "enable_citation": True, # 开启角标标注功能
        "citation_format": "[ref_<number>]", # 角标形式为[ref_i]
        "search_strategy": "max"
    },
    stream=True,
    incremental_output=True,
    result_format="message",
)

# 定义完整思考过程
reasoning_content = ""
# 定义完整回复
answer_content = ""
# 判断是否结束思考过程并开始回复
is_answering = False
# 判断是否为第一个chunk，便于打印搜索信息
is_first_chunk = True

print("=" * 20 + "搜索信息" + "=" * 20)

for chunk in response:
    if is_first_chunk:
        search_results = chunk.output.search_info["search_results"]
        for web in search_results:
            print(f"[{web['index']}]: [{web['title']}]({web['url']})")
        print("=" * 20 + "思考过程" + "=" * 20)
        reasoning_content += chunk.output.choices[0].message.reasoning_content
        print(chunk.output.choices[0].message.reasoning_content,end="",flush=True)
        is_first_chunk = False
    else:
        # 如果思考过程与回复皆为空，则忽略
        if (chunk.output.choices[0].message.content == "" and
            chunk.output.choices[0].message.reasoning_content == ""):
            pass
        else:
            # 如果当前为思考过程
            if (chunk.output.choices[0].message.reasoning_content != "" and
                chunk.output.choices[0].message.content == ""):
                print(chunk.output.choices[0].message.reasoning_content, end="",flush=True)
                reasoning_content += chunk.output.choices[0].message.reasoning_content
            # 如果当前为回复
            elif chunk.output.choices[0].message.content != "":
                if not is_answering:
                    print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                    is_answering = True
                print(chunk.output.choices[0].message.content, end="",flush=True)
                answer_content += chunk.output.choices[0].message.content

# 如需打印完整思考和回复，请解除以下代码的注释
# print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
# print(f"{reasoning_content}")
# print("=" * 20 + "完整回复" + "=" * 20 + "\n")
# print(f"{answer_content}")
# 如果您需要打印本次请求的 Token 消耗，请将以下代码解除注释后运行
# print("\n"+"="*20+"Token 消耗"+"="*20)
# print(chunk.usage)
```

### 返回结果

```
====================搜索信息====================
[1]: [「PE/VC洞察」《乘AI风,破周期浪》之一:全球AI行业及投资趋势](https://baijiahao.baidu.com/s?id=1847324495675907878&wfr=spider&for=pc)
[2]: [2025年10月AI技术前沿速览:从通用智能到实体智能](https://baijiahao.baidu.com/s?id=1845923714145562035&wfr=spider&for=pc)
[3]: [2025年中国人工智能(AI)十大趋势](https://mp.weixin.qq.com/s?__biz=MzI1MjQ2OTQ3Ng==&mid=2247658552&idx=2&sn=e49389c0058c72c571e69dbf0d485126&chksm=e89d380f116acb0baf44ce03181bd2d7175ef8c471b7f67135a7d01c5d3578a77280cbd6445e&scene=27)
[4]: [2026年,AI向物理世界挺进](https://www.bjcc.gov.cn/article/600574950.html)
[5]: [AI 大模型的未来发展趋势如何?三大主线改写产业格局,端侧智能开启全民 AI 时代!](https://baijiahao.baidu.com/s?id=1845107629819035324&wfr=spider&for=pc)
[6]: [2025年人工智能十大趋势!未来学家预测→](https://baijiahao.baidu.com/s?id=1813333845939915170&wfr=spider&for=pc)
[7]: [人工智能与机器学习:技术革命下的职业新蓝海](https://baijiahao.baidu.com/s?id=1845336356822347354&wfr=spider&for=pc)
[8]: [2025,人工智能走向何方?我们如何拥抱变化?](http://dsj.guizhou.gov.cn/xwzx/gnyw/202501/t20250114_86624239.html)
[9]: [2025年AI工具大规模落地 国内用户半年多了2.66亿人](https://baijiahao.baidu.com/s?id=1847270652122448223&wfr=spider&for=pc)
[10]: [让AI焕新而非“换人”,2025年AI如何发展?](https://jswx.gov.cn/chuanbo/wangluo/202501/t20250115_3554633.shtml)
====================思考过程====================
我需要基于知识库中的信息，预测AI的发展趋势。首先，我需要整理知识库中关于AI发展趋势的最新信息，然后进行分析总结，给出合理的预测。

让我先梳理一下知识库中的主要信息：

1. 市场规模与增长：
- [ref_1] 提到2025年全球AI市场规模接近4,000亿美元，到2030年预计将突破1.8万亿美元，年复合增长率(CAGR)高达37.3%。
- [ref_1] 2023年全球人工智能市场规模达到1,966亿美元，预计到2030年将增长至1.81万亿美元，约为2023年的9倍。

....

4. 用户普及：AI工具将更加普及，用户群体更加多元化
5. 监管与伦理：AI立法和监管将更加完善，"负责任"和"可持续"的AI将成为重点
6. 产业影响：创造新职业，改变工作方式，但也带来就业挑战

现在，我将基于这些信息整理一个全面的回答，引用知识库中的相关内容。
====================完整回复====================
# AI发展趋势预测：从技术突破到社会变革

根据近期AI热点新闻和行业分析，AI领域正经历从技术突破到社会应用的深刻变革。以下是基于最新数据的关键发展趋势预测：

## 1. 市场规模爆发式增长

...

## 7. 产业变革与就业重塑

AI正在重塑就业市场，催生新职业的同时也改变传统工作方式。到2026年，AI与自动化对工作方式的长期影响将集中显现：一批新兴职业会迅速崛起，而部分传统岗位则不可避免地日渐式微甚至消失[ref_4]。提示词工程师、AI集成专家、伦理治理专家等新兴职位正为企业带来前所未有的价值。

AI与机器学习领域的薪资水平持续领跑科技行业。2025年算法工程师平均月薪达2.1万元，资深专家年薪突破百万；NLP工程师、计算机视觉工程师等细分岗位薪资涨幅达25%-30%[ref_7]。但高薪背后，企业对人才能力的要求也更加"硬核"，需要技术纵深与行业洞察的双重能力。

## 结语

AI已不仅是"科技热点"，更是政策支持、资本追逐和产业升级的交汇点[ref_1]。从"一问一答"到"连续对话"，从"机器学习"到"机器智能"的跃升，AI正在深刻改变我们的生活和工作方式[ref_8]。面对这一变革，关键在于"让AI焕新而非'换人'"，既要充分利用AI带来的效率提升，也要保持人类的创造力和判断力[ref_10]。未来，AI将不再是简单的工具，而是人类工作与生活的智能协作者，共同推动社会进步。
```

#### Java

### 示例代码

```
// dashscope SDK的版本 >= 2.19.4
import java.util.Arrays;
import com.alibaba.dashscope.aigc.generation.SearchInfo;
import com.alibaba.dashscope.aigc.generation.SearchOptions;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.alibaba.dashscope.aigc.generation.Generation;
import com.alibaba.dashscope.aigc.generation.GenerationParam;
import com.alibaba.dashscope.aigc.generation.GenerationResult;
import com.alibaba.dashscope.common.Message;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;

public class Main {
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}
    private static final Logger logger = LoggerFactory.getLogger(Main.class);
    private static StringBuilder reasoningContent = new StringBuilder();
    private static StringBuilder finalContent = new StringBuilder();
    private static boolean hasPrintedReasoningHeader = true;

    private static void handleGenerationResult(GenerationResult message) {
        String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
        String content = message.getOutput().getChoices().get(0).getMessage().getContent();
        SearchInfo searchInfo = message.getOutput().getSearchInfo();
        if (!reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (hasPrintedReasoningHeader) {
                System.out.println("====================搜索信息====================");
                hasPrintedReasoningHeader = false;
                System.out.print(searchInfo.getSearchResults());

                System.out.println("\n====================思考过程====================");
            }
            System.out.print(reasoning);
        }

        if (!content.isEmpty()) {
            finalContent.append(content);
            if (!hasPrintedReasoningHeader) {
                System.out.println("\n====================完整回复====================");
                hasPrintedReasoningHeader = true;
            }
            System.out.print(content);
        }
        if (message.getOutput().getChoices().get(0).getFinishReason().equals("stop") || message.getOutput().getChoices().get(0).getFinishReason().equals("length")){
            System.out.println("\n====================Token 消耗====================");
            System.out.println(message.getUsage());
        }
    }
    private static GenerationParam buildGenerationParam(Message userMsg) {
        // 定义搜索策略
        SearchOptions searchOptions = SearchOptions.builder()
                // 使返回结果中包含搜索信息的来源
                .enableSource(true)
                // 强制开启互联网搜索
                .forcedSearch(true)
                // 开启角标标注
                .enableCitation(true)
                // 设置角标标注样式为[ref_i]
                .citationFormat("[ref_<number>]")
                .searchStrategy("max")
                .build();

        return GenerationParam.builder()
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen-plus")
                .enableThinking(true)
                .messages(Arrays.asList(userMsg))
                // 开启联网搜索的参数
                .enableSearch(true)
                .searchOptions(searchOptions)
                .resultFormat("message")
                .incrementalOutput(true)
                .build();
    }
    public static void streamCallWithMessage(Generation gen, Message userMsg)
            throws NoApiKeyException, ApiException, InputRequiredException {
        GenerationParam param = buildGenerationParam(userMsg);
        Flowable<GenerationResult> result = gen.streamCall(param);
        result.blockingForEach(message -> handleGenerationResult(message));
    }

    public static void main(String[] args) {
        try {
            Generation gen = new Generation();
            Message userMsg = Message.builder().role(Role.USER.getValue()).content("请你结合近期的AI热点新闻，预测一下AI的发展趋势").build();
            streamCallWithMessage(gen, userMsg);
//             打印最终结果
//            if (reasoningContent.length() > 0) {
//                System.out.println("\n====================完整回复====================");
//                System.out.println(finalContent.toString());
//            }
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            logger.error("An exception occurred: {}", e.getMessage());
        }
        System.exit(0);
    }
}
```

### 返回结果

```
====================搜索信息====================
[SearchInfo.SearchResult(siteName=CSDN软件开发网, icon=https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=2005731947,4139443793&fm=195&app=88&f=JPEG?w=200&h=200, index=1, title=2025年AI趋势前瞻:即将到来的智能革命, url=https://blog.csdn.net/2401_85325726/article/details/147161907), SearchInfo.SearchResult(siteName=腾讯网, icon=https://search-operate.cdn.bcebos.com/6a15e3da696bf097938b48d38e132a60.jpeg, index=2, title=2025年中国人工智能(AI)十大趋势, url=https://mp.weixin.qq.com/s?__biz=MzI1MjQ2OTQ3Ng==&mid=2247658552&idx=2&sn=e49389c0058c72c571e69dbf0d485126&chksm=e89d380f116acb0baf44ce03181bd2d7175ef8c471b7f67135a7d01c5d3578a77280cbd6445e&scene=27), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=3, title=2025人工智能十大趋势:这次,AI真的要“动起来”了!, url=https://baijiahao.baidu.com/s?id=1839669810600928968&wfr=spider&for=pc), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=4, title=AI 大模型的未来发展趋势如何?三大主线改写产业格局,端侧智能开启全民 AI 时代!, url=https://baijiahao.baidu.com/s?id=1845107629819035324&wfr=spider&for=pc), SearchInfo.SearchResult(siteName=CSDN软件开发网, icon=https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=2005731947,4139443793&fm=195&app=88&f=JPEG?w=200&h=200, index=5, title=2025 年 AI 发展十大预测:多模态融合、边缘 AI 普及将成核心增长点, url=https://blog.csdn.net/stjiejieto/article/details/151017680), SearchInfo.SearchResult(siteName=CSDN软件开发网, icon=https://ss2.baidu.com/6ONYsjip0QIZ8tyhnq/it/u=2005731947,4139443793&fm=195&app=88&f=JPEG?w=200&h=200, index=6, title=2025年人工智能发展前瞻:揭秘7大趋势,引领未来科技潮流!, url=https://blog.csdn.net/Trb201013/article/details/150769996), SearchInfo.SearchResult(siteName=腾讯网, icon=https://search-operate.cdn.bcebos.com/6a15e3da696bf097938b48d38e132a60.jpeg, index=7, title=2025年的6大人工智能趋势 , url=https://mp.weixin.qq.com/s?__biz=Mzg4MjIwMzQzMA==&mid=2247508799&idx=2&sn=575628bef09b6a8f91297ee56b9a797c&chksm=ceddcbc37eb073d6568611da8dec5e44a6c70f0183c7c803e91c59278ccf0a7399090bb32bb5&scene=27), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=8, title=2025年AI工具大规模落地,国内用户半年多了2.66亿人, url=https://baijiahao.baidu.com/s?id=1847267945526255766&wfr=spider&for=pc), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=9, title=2025年AI工具大规模落地 国内用户半年多了2.66亿人, url=https://baijiahao.baidu.com/s?id=1847270652122448223&wfr=spider&for=pc), SearchInfo.SearchResult(siteName=百家号, icon=https://baijiahao.baidu.com/favicon.ico, index=10, title=人工智能探路深水区——专访中国自动化学会普及工作委员会主任张军平, url=https://baijiahao.baidu.com/s?id=1846757405997456543&wfr=spider&for=pc)]
====================思考过程====================
我需要基于知识库中的内容，分析AI的发展趋势，并引用相关内容。知识库中提供了多篇关于2025年AI趋势预测的文章，这些文章都是在2025年不同时间点发布的(从2025年7月到10月)。我需要整合这些信息，提取出主要的AI发展趋势。

让我梳理一下知识库中提到的主要AI发展趋势：

...

8. **安全与伦理关注**：
   - [ref_6]提到"安全且无偏见的人工智能"
   - [ref_10]提到"数据隐私、算法公平、技术伦理等"挑战

现在，我将整理一个结构化的回答，重点关注2025年AI发展的主要趋势，引用知识库中的相关内容。
====================完整回复====================
# 2025年AI发展趋势预测：从工具到伙伴的智能革命

当前，人工智能正以前所未有的速度发展，根据最新行业报告和专家分析，2025年AI领域将迎来多个关键性突破。结合近期热点新闻，我为您梳理了以下AI发展趋势：

## 1. 自主AI Agent的崛起：从工具到智能伙伴

2025年，AI Agent（智能代理）正从简单的工具转变为能够自主规划、决策和执行任务的智能伙伴，开启"服务即软件"的新纪元。[ref_1] 这些AI Agent具备更强的自主性，能理解复杂用户意图，主动完成任务，无需过多人工干预，并可同时处理多项任务，在不同系统间协同工作。[ref_1]

...

## 挑战与展望

尽管AI发展迅猛，但仍面临数据隐私、算法公平、技术伦理等挑战。[ref_10] 正如复旦大学张军平教授所言："人工智能的边界从来不是技术划定的终点，而是人类探索和创造的起点。"[ref_10]

2025年的AI发展已告别概念炒作，进入了大规模实际应用的黄金时期，全球市场正以年均近29%的速度快速增长，总规模已经达到1850亿美元。[ref_8] 随着技术的不断成熟和应用场景的丰富，AI将继续重塑我们的工作方式和生活方式，开启真正的智能革命。
====================Token 消耗====================
GenerationUsage(inputTokens=5615, outputTokens=2135, totalTokens=7750, outputTokensDetails=GenerationOutputTokenDetails(reasoningTokens=761), promptTokensDetails=GenerationUsage.PromptTokensDetails(cacheType=null, cachedTokens=0, cacheCreationInputTokens=null, cacheCreation=null))
```

#### HTTP

### 示例代码

#### curl

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "qwen-plus",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": "请你结合近期的AI热点新闻，预测一下AI的发展趋势"
            }
        ]
    },
    "parameters":{
        "enable_thinking": true,
        "incremental_output": true,
        "result_format": "message",
        "enable_search": true,
        "search_options": {
            "forced_search": true,
            "enable_source": true,
            "enable_citation": true,
            "citation_format": "[ref_<number>]",
            "search_strategy": "max"
        }
    }
}'
```

## Responses API的联网搜索

通过 `tools` 参数的`tools`数组中添加 `web_search` 工具即可启用联网搜索。

> 通过 `web_search` 工具启用时，模型以 **agent 式多轮检索** 运行——根据问题自主发起多次 `web_search_call`（必要时配合 `web_extractor_call`），最终整合结果作答。

> 支持以下模型：Qwen3.8 Max、Flash 与开源系列、`qwen3.8-omni-flash`；Qwen3.7、Qwen3.5 系列模型（含开源模型，不含Omni）、Qwen3.6-Plus、Qwen3.6-Flash 系列及 qwen3.6-35b-a3b；qwen3-max、qwen3-max-2026-01-23；deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v4-pro、deepseek-v4-pro-0813；glm-5.2；kimi-k3。

> **Qwen3.8 系列的 agent 式检索**：Qwen3.8 系列（qwen3.8-max、qwen3.8-max-0902、qwen3.8-flash、qwen3.8-2.4t-a95b、qwen3.8-27b）在 Chat Completions/DashScope 协议下不支持 `search_strategy: agent`，但通过本节的 Responses API `web_search` 工具即可实现同等的 agent 式多轮检索能力。

> **Responses API 不使用 `search_strategy` 参数**。是否发起联网搜索、以及是否进行多轮检索，均由是否挂载 `web_search` 工具及模型自主决策决定；传入 `search_options.search_strategy` 会被静默忽略，不会触发搜索。

> 对于支持以下工具的模型，建议同时开启 `web_search`、`web_extractor` 和 `code_interpreter`。`qwen3.8-omni-flash` 的内置工具仅支持 `web_search`。

> 关于Responses API的使用说明、代码示例和迁移指南，请参见 [OpenAI兼容-Responses](raw/model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md) 。

python

```
from openai import OpenAI
import os

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.responses.create(
    # Qwen3.8 系列通过 Responses API 的 web_search 工具即可使用 agent 式多轮检索
    model="qwen3.8-max",
    input="杭州明天天气怎么样？",
    tools=[
        {"type": "web_search"},
        {"type": "web_extractor"},
        {"type": "code_interpreter"}
    ],
    extra_body={"enable_thinking": True}
)

print("="*20 + "回复内容" + "="*20)
print(response.output_text)

print("="*20 + "工具调用次数" + "="*20)
usage = response.usage
if hasattr(usage, 'x_tools') and usage.x_tools:
    print(f"联网搜索次数: {usage.x_tools.get('web_search', {}).get('count', 0)}")
    print(f"网页抓取次数: {usage.x_tools.get('web_extractor', {}).get('count', 0)}")

# 打印每一轮 web_search_call 的搜索来源，观察 agent 式多轮检索过程
print("="*20 + "搜索来源" + "="*20)
for item in response.output:
    if item.type == "web_search_call":
        for i, source in enumerate(item.action.sources, start=1):
            print(f"[{i}] {source.url}")
```

javascript

```
import OpenAI from "openai";

const openai = new OpenAI({
    // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
    apiKey: process.env.DASHSCOPE_API_KEY,
    // 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
    baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
});

async function main() {
    const response = await openai.responses.create({
        // Qwen3.8 系列通过 Responses API 的 web_search 工具即可使用 agent 式多轮检索
        model: "qwen3.8-max",
        input: "杭州明天天气怎么样？",
        tools: [
            { type: "web_search" },
            { type: "web_extractor" },
            { type: "code_interpreter" }
        ],
        enable_thinking: true
    });

    console.log("====================回复内容====================");
    console.log(response.output_text);

    console.log("====================工具调用次数====================");
    console.log(`联网搜索次数: ${response.usage?.x_tools?.web_search?.count || 0}`);
    console.log(`网页抓取次数: ${response.usage?.x_tools?.web_extractor?.count || 0}`);

    console.log("====================搜索来源====================");
    for (const item of response.output) {
        if (item.type === "web_search_call") {
            (item.action?.sources || []).forEach((s, i) =>
                console.log(`[${i + 1}] ${s.url}`));
        }
    }
}

main();
```

bash

```
# 以下为华北2（北京）地域的配置，调用时请将 {WorkspaceId} 替换为真实的业务空间ID，各地域的配置不同。
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/responses \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3.8-max",
    "input": "杭州明天天气怎么样？",
    "tools": [
        {"type": "web_search"},
        {"type": "web_extractor"},
        {"type": "code_interpreter"}
    ],
    "enable_thinking": true
}'
```

以 qwen3.8-max 请求 `杭州明天天气怎么样？` 为例，`output` 数组通常包含多次 `web_search_call` 与 `web_extractor_call`，`usage.x_tools.web_search.count` 会大于 1，体现 agent 式多轮检索：

```
{
  "output": [
    { "type": "reasoning" },
    { "type": "web_search_call", "action": { "sources": [ "..." ] } },
    { "type": "web_extractor_call" },
    { "type": "reasoning" },
    { "type": "web_search_call", "action": { "sources": [ "..." ] } },
    { "type": "message", "content": [ "..." ] }
  ],
  "usage": {
    "x_tools": {
      "web_search":    { "count": 2 },
      "web_extractor": { "count": 2 }
    }
  }
}
```

### 获取搜索来源

执行联网搜索后，搜索来源会在响应的 `output` 数组中 `type` 为 `web_search_call` 的元素内返回，其 `action.sources` 字段为搜索来源链接列表。可在上述示例的 `response` 基础上按如下方式提取：

> Responses API 暂不支持 `enable_source`、`enable_citation`、`citation_format` 参数，不会在回复内容中自动插入 `[1]` 角标。如需角标标注，请使用 DashScope 调用方式。

```
# 在上述 response 的基础上提取搜索来源
print("=" * 20 + "搜索来源" + "=" * 20)
for item in response.output:
    if item.type == "web_search_call":
        for i, source in enumerate(item.action.sources, start=1):
            print(f"[{i}] {source.url}")
```

## 计费说明

**说明**本文所述“联网搜索”为模型内置的联网搜索功能，其计费如下方所示，本身不提供免费调用额度。它与百炼 MCP 广场提供的“联网搜索 MCP”服务是相互独立的两个功能，计费也相互独立：联网搜索 MCP 全部用户前 2000 次调用免费，免费额度用尽后按 29 元/千次计费，详情请参见[接入 Harness 工具](raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。

联网搜索的费用包含两部分：

-   **模型调用费用**：联网搜索的网页内容会拼接到提示词中，增加模型的输入 Token，按照模型的标准价格计费。价格详情请参考百炼控制台。使用 Responses API方式时，联网搜索工具的计费和agent 策略相同。
    
-   **搜索策略费用**：
    
    -   **turbo 与 max 策略**：2026年2月27日 00:00 起：正式计费。每调用 1000 次的费用为：turbo 策略 3元，max 策略 4元。该标准仅适用于华北2（北京）地域。
        
    -   **agent 策略**：
        
        -   每调用 1000 次的费用为：
            
            -   华北2（北京）、美国（弗吉尼亚）、中国香港、日本（东京）、德国（法兰克福）地域：4元
            -   新加坡地域 73.392381元。
    -   **agent\_max 策略（限时优惠）：**
        
        包含联网搜索与网页抓取的费用。
        
        -   联网搜索工具每 1000 次调用费用：
            
            -   华北2（北京）、美国（弗吉尼亚）、中国香港、日本（东京）、德国（法兰克福）地域：4元。
            -   新加坡地域： 73.392381元。
        -   网页抓取工具限时免费。
            

## 限流说明

联网搜索限流为 15 RPS（每秒请求数），按阿里云主账号维度计算（所有API Key 的联网搜索请求总和，不区分模型）。超出限制时API不会报错，但搜索链路不会触发。

## 常见问题

### Q：开启联网搜索后，模型为何没有执行网络搜索？

A：可能原因如下：

-   **模型判断无需联网**：模型判断当前问题不涉及实时信息，可直接使用自身知识回答。如需强制联网，请在 `search_options` 中设置 `forced_search: true`。
-   **触发限流**：账号的请求频率超过了 15 RPS。API 不会报错，但会跳过搜索步骤，请控制请求频率。
-   **模型不支持：**调用的模型不支持联网搜索，请参见[支持的模型](https://help.aliyun.com/zh/model-studio/web-search#980e4e9787miv)。

### Q：如何判断是否执行了搜索？

A：根据调用方式判断：

-   **DashScope**
    -   如果执行了搜索，响应会包含 `search_info` 字段，并且 `usage` 中会包含 `plugins` 字段。
    -   如果未执行搜索，响应不包含 `search_info` 字段，`usage` 中不包含 `plugins` 字段。
-   **OpenAI 兼容**
    
    暂无法通过响应明确判断是否执行搜索。可对比`usage`中返回的输入 Token 数量。如果该数值远超问题本身，则说明执行了搜索。
    
    例如：提问“杭州天气”，未联网时输入 Token 为 10，联网搜索后输入 Token 变为 1953。
    

### Q：为何输入英文无法执行联网搜索？

A：平台正在持续优化联网的判定流程对于英文的支持。当前建议使用中文提问，或在输入英文时[强制联网搜索](https://help.aliyun.com/zh/model-studio/web-search#6f83c89f7dw0v)。

### Q：开启联网搜索后，用户的提问内容是否会泄露到外部？

A：不会。系统不会将原始问题直接透传给搜索引擎，而是对查询意图进行深度解析和多层脱敏处理，仅提取可用于检索的关键信息片段。从原始 query 到实际检索会经过多次改写，确保敏感内容不会明文外泄。阿里云采用数据加密和隐私保护措施确保安全，具体请参考[服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)。

### Q：向量化检索是否会导致信息泄露？

A：不会。向量是高维数学表示，不具可读性，外部系统无法从中还原原始文字。向量匹配过程在封闭可信环境中完成，不会暴露给公共搜索引擎。

### Q：联网搜索的搜索判定机制是什么？

A：系统先判断是否需要搜索——不涉及时事的内容通常不会触发。触发搜索的多为时事信息或百科知识类查询，与机密信息重叠度低。每次搜索都经过多次 query 改写后才执行检索。

### Q：联网搜索后模型返回“无法回答”或无响应？

A：联网搜索结果可能包含管控信息，触发内容安全规则，导致模型返回 `DataInspectionFailed` 错误 (HTTP 400)，响应内容为“抱歉，我无法回答这个问题”。排查方法：关闭联网搜索后重新发送相同查询，若模型正常回复，则确认是搜索返回的内容触发了拦截。内容安全拦截为非确定性行为，取决于搜索返回的具体内容，并非所有敏感话题查询都会触发。

### Q：联网搜索查询股票价格时，非交易日仍返回股价数据，如何处理？

A：使用 qwen3-max 或更新版本的模型。qwen3-max 能识别非交易日并提示无收盘价；qwen-max 缺少日期推理能力，会在非交易日返回搜索获取的股价。`enable_search_extension` 与 `prompt_intervene` 无法解决该问题。

### Q：调用 Kimi 系列模型时联网搜索为何不生效？

A：Kimi 系列模型不支持 `enable_search` 参数，无法使用本文所述的模型内置联网搜索。如需让 Kimi 模型获取实时信息，请在百炼控制台创建智能体应用，并通过**工具 > MCP 服务**添加联网搜索 MCP 工具（如 `bailian_web_search`）。添加后，模型将通过该 MCP 工具检索并返回实时搜索结果。联网搜索 MCP 与内置联网搜索是相互独立的两个功能，计费也相互独立，详情请参见[接入 Harness 工具](raw/model-user-guide/token-plan-guide/token-plan-best-practice/token-plan-harness-tool.md)。

## 错误信息

如果执行报错，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
