# preparations

在调用阿里云百炼的大模型或应用前，需要完成三项准备工作：获取 [API Key](../concepts/api-key.md)、将 [API Key](../concepts/api-key.md) 配置到环境变量、安装对应语言的 SDK。本文汇总了从零开始接入百炼 API 的前置步骤，并列举调用过程中常见的错误码与排查方式，便于开发者快速定位问题。

## 一、获取 [API Key](../concepts/api-key.md)

API Key 是调用百炼服务的鉴权凭证。需使用主账号，或具备 `管理员`/`API-Key` 页面权限的子账号操作。不同地域入口略有差异：

- **华北2（北京）、新加坡、日本（东京）、德国（法兰克福）**：在[百炼控制台](https://bailian.console.aliyun.com/?tab=model#/api-key)右上角选择对应地域后创建。
- **美国（弗吉尼亚）**：前往 [modelstudio 控制台](https://modelstudio.console.aliyun.com/us-east-1) 创建，且需额外选择"归属账号"。

创建时可选权限配置：

- **全部**：可调用所有模型与应用。
- **自定义**：可配置 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）和可访问模型范围。美国（弗吉尼亚）地域不支持自定义配置。

创建成功后弹窗仅展示一次完整 API Key，关闭后无法再次查看明文，丢失需重置或重建。详情参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### API Key 安全升级

百炼已对按量付费 API Key 的生成与存储机制进行安全升级（美国（弗吉尼亚）地域除外）。升级后新建的 API Key 统一以 `sk-ws` 开头，长度更长，且仅在创建时展示一次明文；升级前以 `sk-` 开头的旧 Key 可继续使用，功能不受影响，但建议逐步替换为新格式。

> **注意**：[Token](../concepts/token.md) Plan 与 Coding Plan 不使用本文所述的按量付费 API Key，应使用以 `sk-sp-` 开头的专属 API Key。

### 时效性与配额

- API Key 无失效日期，手动删除后即失效。
- 临时访问可生成有效期 60 秒的临时 API Key，避免暴露长期密钥。
- 单个主账号在华北2/新加坡/日本/德国地域每个地域最多 50 个 API Key；美国（弗吉尼亚）地域每个归属账号最多 20 个。
- RAM 用户被禁用或删除后，其创建的 API Key 全部失效。

## 二、配置 API Key 到环境变量

为避免在代码中硬编码 API Key 导致泄露，建议将其配置到环境变量 `DASHSCOPE_API_KEY`。配置方式因操作系统和 Shell 而异，详见 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

### Linux / macOS

- **永久生效**：将 `export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"` 追加到对应 Shell 配置文件（Bash 用 `~/.bashrc` 或 `~/.bash_profile`，Zsh 用 `~/.zshrc`），然后 `source` 使其生效。
- **临时生效**：直接在当前会话执行 `export DASHSCOPE_API_KEY="..."`，关闭终端后失效。

### Windows

- **系统属性**：通过"编辑系统环境变量"界面在"系统变量"中新建，永久生效，需重启命令行/IDE 才能加载。
- **CMD**：永久用 `setx DASHSCOPE_API_KEY "..."`，临时用 `set DASHSCOPE_API_KEY=...`。
- **PowerShell**：永久用 `[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY","...",[EnvironmentVariableTarget]::User)`，临时用 `$env:DASHSCOPE_API_KEY = "..."`。

### 常见排查

`echo` 能读到环境变量但代码仍报找不到 API Key，常见原因：

1. 只设了临时变量，IDE/应用未重启加载。
2. 通过 `systemd`、`supervisord` 等服务管理器启动的应用需在服务配置文件中显式添加环境变量。
3. 使用 `sudo` 运行脚本时默认不继承用户环境变量，应改用 `sudo -E` 或直接以当前用户执行。

## 三、安装 SDK

百炼支持两条接入路径：阿里云官方 DashScope SDK（Python、Java），以及通过 OpenAI 多语言 SDK 调用百炼的 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)。安装方式详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### Python

需 `python >= 3.8`。

```
# OpenAI Python SDK
pip install -U openai

# DashScope Python SDK
pip install -U dashscope
```

### Java

- **DashScope Java SDK**：通过 Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java`。
- **OpenAI Java SDK**：需 Java 8+，引入 `com.openai:openai-java`（推荐 `3.5.0` 及以上）。

### Node.js

```
npm install --save openai
# 或
yarn add openai
```

安装失败可临时切换镜像源：`npm config set registry https://registry.npmmirror.com/`。

### Go

需 `Go 1.22+`，使用 OpenAI Go SDK：

```
go get 'github.com/openai/openai-go/v3'
```

访问超时可设置阿里云镜像代理：`go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 四、常见错误码与排查

调用失败时建议优先使用阿里云 AI 助理，输入完整报错信息获取解决方案。以下按类别归纳高频错误，完整列表参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

### 参数校验类（400 InvalidParameter）

| 错误信息 | 原因 / 解决方案 |
| --- | --- |
| `enable_thinking must be set to false for non-streaming calls` | 思考模式模型需流式调用，或将 `enable_thinking` 设为 `false` |
| `thinking_budget parameter must be a positive integer...` | `thinking_budget` 需在模型最大思维链长度范围内且大于 0 |
| `This model does not support enable_search` | 当前模型不支持联网搜索，换用支持该能力的模型 |
| `Temperature should be in [0.0, 2.0)` | temperature 须为 `[0, 2)` 的浮点数 |
| `Range of top_p should be (0.0, 1.0]` | top_p 须为 `(0, 1]` 的浮点数 |
| `top_k be greater than or equal to 0` | top_k 须大于等于 0 |
| `Repetition_penalty should be greater than 0.0` | repetition_penalty 须大于 0 |
| `Presence_penalty should be in [-2.0, 2.0]` | presence_penalty 须在 `[-2, 2]` |
| `Range of n should be [1, 4]` | n 须在 `[1, 4]` |
| `Range of max_tokens should be [1, xxx]` | max_tokens 不超过模型最大输出 [Token](../concepts/token.md) 数 |
| `Range of input length should be [1, xxx]` | 输入超长，控制 messages [Token](../concepts/token.md) 数或开启新对话 |

### 模型与调用方式类

- **`Model not exist.`**：`model` 参数名错误或混用了开源社区模型名（如 `Qwen/Qwen3-235B-A22B-Instruct-2507`），应使用百炼模型 ID（如 `qwen3-235b-a22b-instruct-2507`），注意大小写与空格。
- **`This model only support stream mode...`**：模型仅支持[流式输出](../concepts/streaming-output.md)，需启用 `stream=true`。
- **`'audio' output only support with stream=true`**：Qwen-Omni 须流式调用。
- **`The tool call is not supported.`**：当前模型不支持 Function Calling，换用支持的 Qwen 或 DeepSeek 模型。
- **`Tool names are not allowed to be [search]`**：工具名称不能为 `search`。
- **`tool_choice is one of the strings that should be ["none", "auto"]`**：tool_choice 只能为 `auto` 或 `none`。

### 结构化输出与思考模式

- **`'messages' must contain the word 'json'...`**：使用 `response_format=json_object` 时提示词中需包含 `json` 关键词。
- **`Json mode response is not supported when enable_thinking is true`**：结构化输出与思考模式互斥，需将 `enable_thinking` 设为 `false`。
- **`The result_format parameter must be "message" when enable_thinking is true`**：思考模式须 `result_format="message"`。
- **`The incremental_output parameter must be "true" when enable_thinking is true`**：开启思考模式时须同时开启增量输出。

### [多模态](../concepts/multimodal.md)与文件类

- **`The provided URL does not appear to be valid.`**：URL 须以 `http://`、`https://`、`data:` 开头；本地路径须以 `file://` 开头；临时 URL 通过 HTTP 调用需在 Header 加 `X-DashScope-OssResourceResolve: enable`，且仅 DashScope SDK 支持。
- **`Exceeded limit on max bytes per data-uri item: 10485760`**：Base64 编码后单文件不超过 10 MB；图像 URL 不超过 10 MB，视频按模型分别为 2GB/1GB/150MB。
- **`The video modality input does not meet the requirements...`**：Qwen3-VL/Qwen2.5-VL 需 4-512 张图片，其他模型需 4-80 张。
- **`File [id:...] format is not supported.`**：Qwen-Long 仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD 纯文本，图片内容需用千问 VL。
- **`File [id:...] exceeds size limit.`** / **`exceeds page limits (15000 pages).`**：单文件小于 150 MB、页数少于 15000。
- **`Too many files provided.`**：file-id 数量须小于 100。

### 工具调用循环

**`Repetitive tool calls detected...`**：对话历史中名称与参数完全相同的工具调用在多轮连续重复，模型可能陷入循环。应在每轮工具调用后将执行结果以 Tool Message 追加到 messages 数组；必要时在应用侧增加调用次数上限或终止逻辑。

## 五、安全注意事项

- API Key 是账号身份凭证，任何持有者都能以您的身份发起请求并产生费用，切勿公开或提交到代码仓库。
- 建议通过环境变量或密钥管理服务注入，而非硬编码。
- 为不同环境/团队使用子[业务空间](../concepts/workspace.md)隔离权限与成本，子[业务空间](../concepts/workspace.md)下的 API Key 仅能调用该空间已授权的模型与应用。
- 调用百炼调优后的模型时，仅能用其所在[业务空间](../concepts/workspace.md)的 API Key，无需额外授权。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)



