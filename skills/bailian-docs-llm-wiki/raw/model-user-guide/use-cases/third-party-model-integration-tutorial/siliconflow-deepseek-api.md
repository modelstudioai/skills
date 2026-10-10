# DeepSeek-硅基流动

本文档介绍硅基流动 DeepSeek 模型的服务开通、接入地址、调用参数、响应字段、功能支持与计费信息。

> 阿里云百炼提供两个推理服务供应商的DeepSeek模型服务，硅基流动供应商支持更长上下文；[阿里云百炼](raw/model-user-guide/use-cases/third-party-model-integration-tutorial/deepseek-api.md)供应商限流条件更宽松，且支持联网搜索与上下文缓存功能。

**重要**本文档仅适用于华北2（北京）地域。如需使用模型，需使用华北2（北京）地域的[API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)。

## 服务开通

1.  前往[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)，搜索 deepseek，找到 SiliconFlow DeepSeek 模型卡片，单击立即开通；
2.  在弹窗内确认开通及授权。

完成以上步骤即可调用硅基流动提供的 DeepSeek 模型服务。

## 调用前准备

调用模型前，需要先[获取与配置 API Key](raw/model-api-reference/preparations/get-api-key.md)，并[将 API Key 配置到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。如果通过 SDK 调用，还需要[安装 SDK](raw/model-api-reference/preparations/install-sdk.md)。

## 服务接入地址

本文档仅适用于华北2（北京）地域。调用时，将 `{WorkspaceId}` 替换为真实的业务空间 ID。

调用方式

SDK `base_url`

HTTP 请求地址

OpenAI 兼容

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions`

DashScope

`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/text-generation/generation`

## 调用说明

OpenAI 兼容方式支持通过 OpenAI Python SDK、Node.js SDK 或 HTTP 请求调用。`enable_thinking` 不是 OpenAI 标准参数：Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。

DashScope 方式支持通过 Python SDK、Java SDK 或 HTTP 请求调用。Java SDK 版本需要不低于 2.19.4。

## 参数说明

参数

说明

`model`

要调用的模型 ID。

`messages`

输入消息列表。

`enable_thinking`

控制支持该参数的模型是否开启思考模式。

`stream`

设置为 `true` 时开启流式输出。

`stream_options.include_usage`

设置为 `true` 时在流式响应中返回 Token 消耗信息。

`incremental_output`

DashScope 调用中设置为 `true` 时开启增量输出。

`result_format`

DashScope 调用中设置为 `message` 时，以消息格式返回结果。

## 响应字段说明

字段

说明

`reasoning_content`

完整思考过程。

`content`

完整回复内容。

`usage`

Token 消耗信息。

## 其它功能

**模型**

[多轮对话](raw/model-user-guide/model-experience/text-generation-model/multi-round-conversation.md)

[Function Calling](raw/model-user-guide/model-experience/text-generation-model/tool-calls/qwen-function-calling.md)

[前缀续写](raw/model-user-guide/model-experience/text-generation-model/partial-mode.md)

[联网搜索](raw/model-user-guide/model-experience/text-generation-model/tool-calls/web-search.md)

[上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)

[结构化输出](raw/model-user-guide/model-experience/text-generation-model/qwen-structured-output.md)

siliconflow/deepseek-v3.1-terminus

支持

支持

支持

> 仅非思考模式

不支持

不支持

不支持

siliconflow/deepseek-v3-0324

支持

支持

支持

不支持

不支持

不支持

## 参数默认值

**模型**

**temperature**

**top\_p**

**repetition\_penalty**

**presence\_penalty**

siliconflow/deepseek-v3.1-terminus

1.0

1.0

\-

\-

siliconflow/deepseek-v3-0324

1.0

1.0

\-

\-

“-” 表示没有默认值，也不支持设置。

## 模型列表与计费

硅基流动基于自研推理引擎，为DeepSeek模型提供低延迟、高稳定性的推理服务。

-   混合思考模型（通过`enable_thinking`参数控制是否思考）：siliconflow/deepseek-v3.1-terminus
-   非思考模型：siliconflow/deepseek-v3-0324

模型上下文长度与价格信息请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/market)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## 错误码

如果执行报错，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
