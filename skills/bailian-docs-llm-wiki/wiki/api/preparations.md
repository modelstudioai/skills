# preparations

本页汇总使用阿里云百炼 API 前的准备工作，包括获取 API Key、配置环境变量、安装 SDK 以及常见错误码的排查。完成这些步骤后即可开始调用百炼平台上的各类大模型。

## 获取 API Key

API Key 是调用百炼模型和应用的鉴权凭证。在[百炼控制台](https://bailian.console.aliyun.com/)的 **API Key** 页面创建，需使用主账号或具备相应权限的子账号操作。详细流程参见[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 支持的地域

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |

> **注意**：新加坡、日本（东京）、德国（法兰克福）地域的 Base URL 中需要将 `{WorkspaceId}` 替换为实际的[业务空间](../concepts/workspace.md) ID。

### 权限与时效

- API Key 的调用权限由其**归属[业务空间](../concepts/workspace.md)**决定，同一空间内的 API Key 权限相同，无需为不同模型类型分别创建。
- 默认[业务空间](../concepts/workspace.md)的 API Key 可调用所有标准模型；子[业务空间](../concepts/workspace.md)的 API Key 仅可调用已授权的模型。
- API Key 创建后永久有效，手动删除即失效。如需临时授权可生成有效期 60 秒的临时 API Key。
- 华北2（北京）和新加坡地域已完成安全升级，新建 API Key 仅在创建时展示一次明文，关闭弹窗后无法再次查看。
- 每个主账号在华北2（北京）、新加坡、日本（东京）、德国（法兰克福）地域最多可创建 50 个 API Key；美国（弗吉尼亚）地域每个归属账号最多 20 个。

## 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码导致泄漏风险。详细步骤参见[将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

### Linux / macOS

**永久生效**（推荐）：将 `export DASHSCOPE_API_KEY="YOUR_KEY"` 追加到 Shell 配置文件（Linux 用 `~/.bashrc`，macOS Zsh 用 `~/.zshrc`，macOS Bash 用 `~/.bash_profile`），然后 `source` 使其生效。

**临时生效**：直接在终端执行 `export DASHSCOPE_API_KEY="YOUR_KEY"`，仅当前会话有效。

### Windows

- **系统属性**（永久）：通过"编辑系统环境变量"新建变量 `DASHSCOPE_API_KEY`，需重启 IDE 或命令行窗口生效。
- **CMD**（永久）：`setx DASHSCOPE_API_KEY "YOUR_KEY"`，需打开新窗口生效。
- **PowerShell**（永久）：`[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_KEY", [EnvironmentVariableTarget]::User)`。
- 临时变量分别使用 `set`（CMD）或 `$env:DASHSCOPE_API_KEY = "YOUR_KEY"`（PowerShell）。

> **注意**：如果 `echo` 确认环境变量已设置但代码仍提示找不到 API Key，常见原因包括：仅设置了临时变量、未重启 IDE/应用、使用 `sudo` 时未加 `-E` 参数。

## 安装 SDK

百炼支持多种 SDK 接入方式，详见[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### OpenAI 兼容 SDK（推荐）

通过 OpenAI 官方 SDK 调用百炼的 [OpenAI 兼容接口](../concepts/openai-compatible.md)，支持多语言：

| 语言 | 安装命令 | 最低版本要求 |
|------|---------|------------|
| Python | `pip install -U openai` | Python >= 3.8 |
| Node.js | `npm install --save openai` | - |
| Java | Maven/Gradle 添加 `com.openai:openai-java` | Java 8+ |
| Go | `go get 'github.com/openai/openai-go/v3'` | Go 1.22+ |

### [DashScope SDK](../concepts/dashscope-sdk.md)

百炼官方 SDK，支持 Python 和 Java：

- **Python**：`pip install -U dashscope`（Python >= 3.8）
- **Java**：Maven/Gradle 添加 `com.alibaba:dashscope-sdk-java`

## 常见错误码

调用百炼 API 时可能遇到的错误及解决方案，完整列表参见[错误码](../../raw/model-api-reference/preparations/error-code.md)。以下列出高频错误：

### 参数相关（400-InvalidParameter）

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Model not exist.` | 模型名称不存在或格式不正确 | 检查大小写、空格，对照模型列表确认名称 |
| `Range of input length should be [1, xxx]` | 输入内容超过模型 Token 上限 | 控制 messages 数组 Token 数，或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | `max_tokens` 超出范围 | 参照模型列表中的最大输出 Token 数设置 |
| `Temperature should be in [0.0, 2.0)` | temperature 参数越界 | 设置为 [0.0, 2.0) 范围内的值 |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查 JSON 结构（多余逗号、括号未闭合等） |

### 流式与思考模式

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `enable_thinking must be set to false for non-streaming calls` | 非流式调用启用了思考模式 | 设置 `enable_thinking=false` 或改用[流式输出](../concepts/streaming.md) |
| `incremental_output parameter must be "true" when enable_thinking is true` | 思考模式要求增量[流式输出](../concepts/streaming.md) | 设置 `incremental_output=true` |
| `This model only support stream mode` | 模型仅支持[流式输出](../concepts/streaming.md) | 启用 `stream=true` |

### 文件与多模态

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `File [id:file-fe-xxx] format is not supported.` | Qwen-Long 不支持该文件格式 | 仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD |
| `Exceeded limit on max bytes per data-uri item` | 本地文件 Base64 编码后超过 10 MB | 压缩文件或改用 URL 传入 |
| `The provided URL does not appear to be valid` | URL 或本地路径格式不正确 | URL 以 `http://`/`https://`/`data:` 开头，本地路径以 `file://` 开头 |

### 工具调用

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `messages with role "tool" must be a response to a preceeding message with "tool_calls"` | 缺少 Assistant Message | 先将模型返回的 Assistant Message 添加到 messages 数组 |
| `The tool call is not supported.` | 模型不支持 Function Calling | 更换为支持该功能的 Qwen 或 DeepSeek 模型 |
| `Json mode response is not supported when enable_thinking is true` | 结构化输出与思考模式冲突 | 使用结构化输出时关闭思考模式 |

## 来源文档

- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)



