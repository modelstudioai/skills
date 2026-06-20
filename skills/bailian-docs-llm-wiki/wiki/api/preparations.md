# preparations

在调用阿里云百炼平台的大模型 API 之前，需要完成几项准备工作：获取 API Key 作为鉴权凭证、将其配置到环境变量以避免硬编码泄露、安装对应语言的 SDK，并了解常见错误码以便排查问题。本文汇总了这些前置步骤的关键信息。

## 获取 API Key

API Key 是调用百炼服务的唯一鉴权凭证。需使用主账号或具备相应权限的子账号，在百炼控制台的 API Key 管理页面创建。详细流程参见[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

**不同地域的 Base URL：**

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |
| 日本（东京） | `https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1` |

**权限说明：**

- API Key 的调用权限由其归属业务空间决定，同一空间内的 API Key 权限相同。
- 默认业务空间的 API Key 可调用所有标准模型及该空间内的应用。
- 子业务空间的 API Key 仅可调用已授权的模型和该空间内的应用。
- 华北2（北京）地域支持 IP 访问白名单等精细权限控制。
- API Key 创建后永久有效，手动删除后即失效。如需临时授权可生成有效期 60 秒的临时 API Key。

> **注意**：华北2（北京）和新加坡地域已对 API Key 进行安全升级，新建的 API Key 仅在创建时展示一次明文，关闭弹窗后无法再查看。请务必立即保存。

## 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY` 中，避免在代码里硬编码。具体操作参见[将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

**各平台快速设置：**

- **Linux/macOS**：将 `export DASHSCOPE_API_KEY="your-key"` 追加到 `~/.bashrc`（Linux）或 `~/.zshrc`（macOS Zsh），然后执行 `source` 使其生效。
- **Windows CMD**：使用 `setx DASHSCOPE_API_KEY "your-key"` 设置永久变量，或 `set DASHSCOPE_API_KEY=your-key` 设置临时变量。
- **Windows PowerShell**：使用 `[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-key", [EnvironmentVariableTarget]::User)` 设置永久变量。

> **注意**：设置永久环境变量后，需要重启 IDE、命令行工具或应用程序才能生效。使用 `sudo` 运行脚本时，需加 `-E` 参数以继承环境变量。

## 安装 SDK

百炼支持 DashScope 官方 SDK 和 OpenAI 兼容 SDK 两种方式。完整安装说明参见[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

**各语言安装方式：**

| 语言 | [DashScope SDK](../concepts/dashscope-sdk.md) | OpenAI 兼容 SDK |
|------|--------------|-----------------|
| Python (>=3.8) | `pip install -U dashscope` | `pip install -U openai` |
| Java | Maven/Gradle 添加 `com.alibaba:dashscope-sdk-java` | Maven/Gradle 添加 `com.openai:openai-java`（推荐 3.5.0+） |
| Node.js | - | `npm install --save openai` |
| Go (>=1.22) | - | `go get 'github.com/openai/openai-go/v3'` |

> **注意**：Node.js 安装失败时可配置镜像源 `npm config set registry https://registry.npmmirror.com/`；Go 超时可设置代理 `go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 常见错误码

调用 API 时如遇到报错，可参考[错误码](../../raw/model-api-reference/preparations/error-code.md)进行排查。以下是高频错误及解决思路：

**参数相关（400-InvalidParameter）：**

| 错误信息 | 原因与解决方案 |
|---------|--------------|
| `Model not exist` | 模型名称错误或大小写不匹配，需对照模型列表确认 |
| `Range of input length should be [1, xxx]` | 输入 Token 超过模型上限，需精简输入或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | `max_tokens` 超出模型最大输出限制 |
| `enable_thinking must be set to false for non-streaming calls` | 思考模式仅支持[流式输出](../concepts/streaming.md)，需设置 `stream=true` 或关闭 `enable_thinking` |
| `Required body invalid` | 请求体 JSON 格式错误，检查逗号、括号等 |
| `messages with role "tool" must be a response to a preceeding message with "tool_calls"` | 工具调用时未在 messages 中添加 Assistant Message |

**文件相关：**

| 错误信息 | 原因与解决方案 |
|---------|--------------|
| `Invalid file` | file-id 无效或不属于当前账号 |
| `File format is not supported` | Qwen-Long 仅支持纯文本格式（TXT/DOCX/PDF/EPUB/MOBI/MD） |
| `Exceeded limit on max bytes per data-uri item` | Base64 编码后单文件不得超过 10 MB |

**多模态相关：**

| 错误信息 | 原因与解决方案 |
|---------|--------------|
| `The video modality input does not meet the requirements` | 图像列表数量需在 4-512 张（Qwen3-VL/Qwen2.5-VL）或 4-80 张（其他模型） |
| `The image length and width do not meet the model restrictions` | 图像宽高需不小于 10px，宽高比不超过 200:1 |
| `The provided URL does not appear to be valid` | URL 需以 `http://`/`https://`/`data:` 开头，本地路径需以 `file://` 开头 |

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


