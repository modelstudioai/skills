# preparations

在调用阿里云百炼平台的模型 API 之前，需要完成几项准备工作：获取 API Key、将其安全地配置到环境变量、安装对应语言的 SDK。本文汇总了这些前置步骤的核心要点及常见错误码，帮助开发者快速完成接入准备。

## 获取与管理 API Key

API Key 是调用百炼服务的唯一鉴权凭证。创建 API Key 需要使用主账号，或具备`管理员`/`API-Key`页面权限的子账号。详细流程请参见[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 各地域创建入口

| 地域 | 控制台入口 | 备注 |
|------|-----------|------|
| 华北2（北京） | bailian.console.aliyun.com | 支持 IP 白名单等精细权限控制 |
| 新加坡 | modelstudio.console.aliyun.com | 创建后需立即保存，关闭弹窗后无法再查看 |
| 美国（弗吉尼亚） | dashscope-us.aliyuncs.com | 每个归属账号最多 20 个 API Key |
| 德国（法兰克福） | bailian.console.aliyun.com/eu-central-1 | 创建后需立即保存 |

### 权限与[业务空间](../concepts/workspace.md)

- API Key 的调用权限由其**归属[业务空间](../concepts/workspace.md)**决定，同一空间内的 API Key 权限相同，无需为不同模型类型创建不同的 Key。
- **默认[业务空间](../concepts/workspace.md)**的 Key 可调用所有标准模型；**子业务空间**的 Key 仅可调用已授权的模型。
- 调优后的模型仅能用其所在业务空间的 API Key 调用。
- API Key 创建后永久有效，手动删除后失效。如需临时访问可生成有效期 60 秒的临时 API Key。

### 各地域 Base URL

通过第三方工具或代码调用时，需配合正确的 Base URL：

- **华北2（北京）**：`https://dashscope.aliyuncs.com/compatible-mode/v1`
- **新加坡**：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`
- **美国（弗吉尼亚）**：`https://dashscope-us.aliyuncs.com/compatible-mode/v1`
- **德国（法兰克福）**：`https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1`

> **注意**：新加坡和德国（法兰克福）地域的 Base URL 中需替换 `{WorkspaceId}` 为实际的业务空间 ID。

## 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY` 中，避免硬编码泄露风险。各操作系统的配置方式请参见[将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

### 快速参考

| 系统 | 永久性配置 | 临时配置 |
|------|-----------|---------|
| Linux (Bash) | 追加到 `~/.bashrc`，执行 `source ~/.bashrc` | `export DASHSCOPE_API_KEY="your-key"` |
| macOS (Zsh) | 追加到 `~/.zshrc`，执行 `source ~/.zshrc` | `export DASHSCOPE_API_KEY="your-key"` |
| Windows CMD | `setx DASHSCOPE_API_KEY "your-key"` | `set DASHSCOPE_API_KEY=your-key` |
| Windows PowerShell | `[Environment]::SetEnvironmentVariable(...)` | `$env:DASHSCOPE_API_KEY = "your-key"` |

### 常见问题

- 临时环境变量仅在当前终端会话有效，不会影响已启动的 IDE 或应用。
- 设置永久环境变量后，需重启 IDE、命令行工具或应用服务才能生效。
- 使用 `sudo` 运行脚本时可能丢失环境变量，可改用 `sudo -E` 保留环境变量。

## 安装 SDK

百炼同时支持官方 DashScope SDK 和 OpenAI 兼容 SDK。各语言的安装方式请参见[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### 支持的 SDK 矩阵

| 语言 | DashScope SDK | OpenAI SDK |
|------|--------------|------------|
| Python (≥3.8) | `pip install -U dashscope` | `pip install -U openai` |
| Java | Maven/Gradle: `com.alibaba:dashscope-sdk-java` | Maven/Gradle: `com.openai:openai-java`（推荐 ≥3.5.0） |
| Node.js | - | `npm install --save openai` |
| Go (≥1.22) | - | `go get github.com/openai/openai-go/v3` |

> **注意**：Node.js 安装失败时可配置镜像源 `npm config set registry https://registry.npmmirror.com/`；Go 超时可设置代理 `go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 常见错误码

调用失败时返回的错误码及解决方案详见[错误码](../../raw/model-api-reference/preparations/error-code.md)。以下列出高频错误：

### 参数相关（400-InvalidParameter）

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Model not exist.` | 模型名称错误或大小写不对 | 核对模型列表，注意区分百炼模型 ID 与开源社区名称 |
| `Range of input length should be [1, xxx]` | 输入 Token 超限 | 控制 messages 长度或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | max_tokens 超出范围 | 参考模型最大输出 Token 数 |
| `enable_thinking must be set to false for non-streaming calls` | 思考模式仅支持流式 | 设置 `enable_thinking=false` 或改用[流式输出](../concepts/streaming-output.md) |
| `This model only support stream mode` | 模型仅支持[流式输出](../concepts/streaming-output.md) | 启用[流式输出](../concepts/streaming-output.md) |

### 文件与多模态相关

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Exceeded limit on max bytes per data-uri item` | 本地文件 Base64 超 10MB | 压缩文件或改用 URL 传入 |
| `File format is not supported` | Qwen-Long 仅支持纯文本格式 | 改用 TXT/DOCX/PDF/EPUB/MOBI/MD |
| `Too many files provided` | file-id 数量超限 | 确保 file-id 数量小于 100 |

### 工具调用相关

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `messages with role "tool" must be a response to a preceeding message with "tool_calls"` | 未添加 Assistant Message | 先将模型响应的 Assistant Message 加入 messages |
| `The tool call is not supported` | 模型不支持 Function Calling | 更换为支持的 Qwen 或 DeepSeek 模型 |

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


