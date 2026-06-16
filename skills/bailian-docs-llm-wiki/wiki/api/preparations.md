# preparations

在调用阿里云百炼平台的大模型 API 之前，需要完成 API Key 获取、环境变量配置和 SDK 安装三项准备工作。本文汇总了这些前置步骤的关键信息及常见错误码的排查方法，帮助开发者快速上手。

## 获取 API Key

API Key 是调用百炼平台所有模型和应用的鉴权凭证。需使用主账号或具备相应页面权限的子账号，在控制台的 API Key 页面创建。详细步骤请参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

百炼目前支持以下地域，各地域的 Base URL 不同：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

### 权限与[业务空间](../concepts/workspace.md)

- API Key 的调用权限由其**归属[业务空间](../concepts/workspace.md)**决定，同一空间内的 API Key 权限相同，无需为不同模型类型分别创建。
- 默认[业务空间](../concepts/workspace.md)的 API Key 可调用所有标准模型；子[业务空间](../concepts/workspace.md)的 API Key 仅能调用已授权的模型。
- 目前仅华北2（北京）地域支持 IP 访问白名单等精细权限控制。

### 数量限制与时效

- 华北2（北京）、新加坡、德国（法兰克福）地域：每个主账号每个地域最多 50 个 API Key。
- 美国（弗吉尼亚）地域：每个归属账号最多 20 个 API Key。
- API Key 创建后永久有效，手动删除即失效。如需临时访问权限，可生成有效期 60 秒的临时 API Key。

> **注意**：Coding Plan 使用专属 API Key（格式 `sk-sp-xxxxx`），与本文介绍的百炼通用 API Key（格式 `sk-xxxxx`）不同。

## 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY` 中，避免硬编码导致泄露。详细操作请参见 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

各系统的永久性配置方式：

- **Linux**：追加 `export DASHSCOPE_API_KEY="your-key"` 到 `~/.bashrc`，然后 `source ~/.bashrc`。
- **macOS**：根据 Shell 类型追加到 `~/.zshrc`（Zsh）或 `~/.bash_profile`（Bash），然后 source 对应文件。
- **Windows**：通过系统属性添加系统变量，或使用 `setx`（CMD）/ `[Environment]::SetEnvironmentVariable`（PowerShell）。

配置后如果代码仍提示找不到 API Key，常见原因包括：仅设置了临时变量、未重启 IDE 或应用、使用 `sudo` 未传递环境变量（可用 `sudo -E` 解决）。

## 安装 SDK

百炼支持两类 SDK：官方 DashScope SDK（Python、Java）和 OpenAI 兼容 SDK（Python、Node.js、Java、Go）。详细安装方法请参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

| 语言 | DashScope SDK | OpenAI SDK |
|------|--------------|------------|
| Python (>= 3.8) | `pip install -U dashscope` | `pip install -U openai` |
| Java (>= 8) | Maven/Gradle 添加 `com.alibaba:dashscope-sdk-java` | Maven/Gradle 添加 `com.openai:openai-java` |
| Node.js | - | `npm install --save openai` |
| Go (>= 1.22) | - | `go get github.com/openai/openai-go/v3` |

如遇网络问题，可配置镜像源：npm 使用 `https://registry.npmmirror.com/`，Go 使用 `https://mirrors.aliyun.com/goproxy/,direct`。

## 常见错误码

调用模型时如遇报错，可参见 [错误码](../../raw/model-api-reference/preparations/error-code.md) 获取完整的错误信息与解决方案。以下列出高频错误：

### 参数类错误（400-InvalidParameter）

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Model not exist` | 模型名称不存在或格式错误 | 检查大小写和空格，使用百炼模型 ID 而非开源社区名称 |
| `Range of input length should be [1, xxx]` | 输入 Token 超过模型上限 | 控制 messages 长度，或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | `max_tokens` 超出范围 | 参考模型列表中的最大输出 Token 数 |
| `Temperature should be in [0.0, 2.0)` | temperature 参数超出范围 | 设置为 [0.0, 2.0) 区间内的值 |
| `enable_thinking must be set to false for non-streaming calls` | 非流式调用使用了思考模式 | 将 `enable_thinking` 设为 `false` 或改用流式输出 |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查 JSON 结构，修复多余逗号或未闭合括号 |

### 文件与多模态错误

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Exceeded limit on max bytes per data-uri item` | 本地文件超出大小限制 | Base64 编码后单个文件不超过 10 MB |
| `File format is not supported` | Qwen-Long 不支持该文件格式 | 仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD |
| `The provided URL does not appear to be valid` | URL 或本地路径格式错误 | URL 需以 `http://`/`https://`/`data:` 开头，本地路径需以 `file://` 开头 |

## 注意事项

- 请勿以任何方式公开 API Key，防止安全风险和资金损失。
- RAM 用户被禁用或删除后，其创建的所有 API Key 均会失效。
- 使用 OpenAI 兼容接口时，新加坡和德国（法兰克福）地域的 Base URL 中需将 `{WorkspaceId}` 替换为实际的业务空间 ID。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)



