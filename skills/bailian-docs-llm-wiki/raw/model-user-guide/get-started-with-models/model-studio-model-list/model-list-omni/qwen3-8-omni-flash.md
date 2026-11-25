# qwen3.8-omni-flash

面向音视频理解和内容分析，支持文本、图片、音频、视频输入及文本输出。

<a id="推理服务供应商"></a>

## 推理服务供应商

`qwen3.8-omni-flash` 模型的推理服务供应商为阿里云百炼。

<a id="模型能力"></a>

## 模型能力

支持地域：华北2（北京）、新加坡、中国香港、日本（东京）、德国（法兰克福）、美国（弗吉尼亚）。需使用对应地域的 [API Key](../../../../model-api-reference/preparations/get-api-key.md)。

| 能力项 | 支持情况 | 能力项 | 支持情况 |
| --- | --- | --- | --- |
| 输入模态 | 文本、图片、音频、视频 | 输出模态 | 文本 |
| Function Calling | 支持[自定义工具调用](../../../model-experience/text-generation-model/tool-calls/qwen-function-calling.md) | 深度思考 | 默认开启，支持调节思考强度，详见[深度思考](../../../model-experience/text-generation-model/deep-thinking.md) |
| 联网搜索 | 支持[联网搜索](../../../model-experience/text-generation-model/tool-calls/web-search.md)；Responses 内置工具为 `web_search` | 上下文缓存 | 支持自动生效的[隐式缓存](../../../model-experience/text-generation-model/context-cache.md#2317ea09cfxok)及[Responses Session缓存](../../../../model-api-reference/toolkits-and-frameworks/compatibility-with-openai-responses-api.md#example-session-cache-title) |
| 音频输入语种 | 113 种语言和方言，与 Qwen3.5-Omni 一致，完整列表见[模型选型](../../../model-experience/omni-modal/qwen-omni.md#d54e85c641oux) | 多通道音频 | 支持空间音频输入；Chat Completions 通过 `use_multichannel` 开启 |

通过 Chat Completions 或 Responses 调用，示例见[非实时调用指南](../../../model-experience/omni-modal/qwen-omni.md#qwen38-offline)。

<a id="上下文限制"></a>

## 上下文限制

| 参数 | 值 | 参数 | 值 |
| --- | --- | --- | --- |
| 上下文长度 | 1M Token | 最大输入长度（非思考模式） | 991808 Token |
| 最大输入长度（思考模式） | 983616 Token | 最大输出长度 | 131072 Token |

<a id="模型价格"></a>

## 模型价格

模型调用价格请参见[模型价格](../../../test-1/model-pricing.md#4c2e910ce4pcq)。

<a id="限流"></a>

## 限流

模型调用的限流说明请参见[限流](../../rate-limit.md#5b7c656e788u8)。

<a id="调用方式"></a>

<a id="invocation"></a>

## 调用方式

-   [接入指南](../../../model-experience/omni-modal/qwen-omni.md#qwen38-offline)
-   [Chat Completions API 参考](../../../../model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)
-   [Responses API 参考](../../../../model-api-reference/qwen-api-reference/openai-compatible-responses/qwen-api-via-openai-responses.md)
