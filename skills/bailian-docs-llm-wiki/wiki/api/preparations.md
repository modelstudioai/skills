# preparations

在调用阿里云百炼平台的大模型 API 之前，需要完成三项准备工作：获取 [API Key](../concepts/api-key.md) 作为鉴权凭证、安装对应语言的 SDK、以及了解常见错误码以便快速排障。本文汇总了这些准备步骤的核心要点，帮助开发者快速上手。

## 获取与配置 [API Key](../concepts/api-key.md)

[API Key](../concepts/api-key.md) 是调用百炼服务的唯一鉴权凭证。您需要通过百炼控制台创建 API Key，详细步骤参见[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 创建 API Key

- 操作权限要求：需使用主账号，或具备`管理员`或`API-Key`页面权限的子账号。
- 不同地域的控制台入口不同：华北2（北京）、新加坡、日本（东京）、德国（法兰克福）使用 `bailian.console.aliyun.com`；美国（弗吉尼亚）使用 `modelstudio.console.aliyun.com`。
- 创建时可选择归属[业务空间](../concepts/workspace.md)（建议选默认空间），并配置权限（全部或自定义 IP 白名单 + 模型范围）。
- 升级后新创建的 API Key 以 `sk-ws` 开头，仅在创建时展示一次明文，关闭弹窗后无法再次查看。请立即复制保存。

### 权限与时效

- API Key 的调用权限由其归属[业务空间](../concepts/workspace.md)决定，同一空间内的 API Key 权限相同，无需为不同模型类型分别创建。
- 默认[业务空间](../concepts/workspace.md)的 API Key 可调用所有标准模型；子[业务空间](../concepts/workspace.md)的 API Key 仅可调用已授权的模型。
- API Key 没有失效日期，手动删除后即失效。如需临时授权，可生成有效期 60 秒的临时 API Key。

### 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

- **Linux/macOS**：追加 `export DASHSCOPE_API_KEY="your-key"` 到 `~/.bashrc`（Linux）或 `~/.zshrc`（macOS Zsh），然后 `source` 使其生效。
- **Windows**：通过系统属性设置系统变量，或在 CMD 中用 `setx`、PowerShell 中用 `[Environment]::SetEnvironmentVariable` 设置永久变量。

> **注意**：设置环境变量后，已打开的 IDE 或终端不会自动加载新变量，需要重启相关程序。使用 `sudo` 运行脚本时，默认不继承用户环境变量，需加 `-E` 参数。

## 安装 SDK

百炼支持两类 SDK 接入方式，具体安装方法参见[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### [DashScope SDK](../concepts/dashscope-sdk.md)（官方 SDK）

| 语言 | 安装方式 | 版本要求 |
|------|---------|---------|
| Python | `pip install -U dashscope` | Python >= 3.8 |
| Java | Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java` | - |

### OpenAI 兼容 SDK

百炼提供 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，可直接使用 OpenAI 官方 SDK：

| 语言 | 安装方式 | 版本要求 |
|------|---------|---------|
| Python | `pip install -U openai` | Python >= 3.8 |
| Java | Maven/Gradle 引入 `com.openai:openai-java`（推荐 3.5.0） | Java >= 8 |
| Node.js | `npm install --save openai` | - |
| Go | `go get 'github.com/openai/openai-go/v3'` | Go >= 1.22 |

> **注意**：Node.js 安装失败时可配置镜像源 `npm config set registry https://registry.npmmirror.com/`；Go 访问超时时可设置 `GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 常见错误码

调用 API 失败时，可根据返回的错误码快速定位问题。完整错误码列表参见[错误码](../../raw/model-api-reference/preparations/error-code.md)。以下列出最常见的几类错误：

### 参数校验错误（400）

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Model not exist` | 模型名称错误或格式不正确 | 核对模型列表中的名称，注意大小写，勿混用开源社区名与百炼模型 ID |
| `Range of input length should be [1, xxx]` | 输入 [Token](../concepts/token.md) 数超过模型上限 | 控制 messages 数组中的 [Token](../concepts/token.md) 数；连续对话时注意历史记录累积 |
| `Range of max_tokens should be [1, xxx]` | max_tokens 超出模型最大输出限制 | 参考模型列表中的"最大输出 [Token](../concepts/token.md) 数" |
| `Temperature should be in [0.0, 2.0)` | temperature 参数越界 | 设置为 [0.0, 2.0) 范围内的值 |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查 JSON 字符串：多余逗号、括号未闭合等 |

### 思考模式相关

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `enable_thinking must be set to false for non-streaming calls` | 非流式调用开启了思考模式 | 设为 `false` 或改用流式输出 |
| `incremental_output parameter must be "true" when enable_thinking is true` | 思考模式要求增量流式输出 | 设置 `incremental_output` 为 `true` |
| `Json mode response is not supported when enable_thinking is true` | 思考模式与结构化输出冲突 | 关闭思考模式后再使用结构化输出 |

### [多模态](../concepts/multimodal.md)与文件相关

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Exceeded limit on max bytes per data-uri item` | 本地文件 Base64 编码后超 10MB | 压缩文件或改用 URL 方式传入 |
| `File [id:file-fe-xxx] format is not supported` | Qwen-Long 不支持图片/扫描文档 | 改用千问 VL 模型处理图片内容 |
| `The provided URL does not appear to be valid` | 传入的 URL 或本地路径格式错误 | URL 需以 `http://`/`https://`/`data:` 开头；本地路径以 `file://` 开头 |

### 工具调用相关

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `messages with role "tool" must be a response to a preceeding message with "tool_calls"` | Tool Message 前缺少 Assistant Message | 先将模型响应的 Assistant Message 加入 messages 数组 |
| `Repetitive tool calls detected` | 相同工具调用在连续轮次重复 | 每轮追加工具执行结果；增加调用次数上限或终止逻辑 |

## 快速上手清单

1. 在百炼控制台创建 API Key 并保存到环境变量 `DASHSCOPE_API_KEY`
2. 根据使用语言安装 [DashScope SDK](../concepts/dashscope-sdk.md) 或 OpenAI 兼容 SDK
3. 选择目标模型，参考对应 API 文档发起首次调用
4. 遇到调用报错时，根据错误码对照排查

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)








