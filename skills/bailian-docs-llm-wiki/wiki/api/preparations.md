# preparations

调用阿里云百炼平台的模型 API 前，需要完成三项准备工作：获取 API Key、将 API Key 配置到环境变量、安装 SDK。本文汇总了这些准备步骤的要点，并整理了常见错误码及其解决方案，帮助开发者快速上手。

## 获取 API Key

API Key 是调用百炼大模型和应用的鉴权凭证。创建 API Key 需要使用主账号，或具备`管理员`或`API-Key`页面权限的子账号。详细操作请参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 地域与 Base URL

百炼支持多个地域，不同地域的控制台入口和 Base URL 不同：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

其中新加坡和德国地域需将 `{WorkspaceId}` 替换为实际的[业务空间](../concepts/workspace.md) ID。

### 权限与[业务空间](../concepts/workspace.md)

- API Key 的调用权限由其**归属[业务空间](../concepts/workspace.md)**决定，同一空间内的 API Key 权限相同，无需为不同模型类型（文生文、文生图、语音合成等）分别创建。
- 默认业务空间下的 API Key 可调用所有标准模型及该空间内的应用；子业务空间下的 API Key 仅可调用已授权的模型。
- 目前仅华北2（北京）地域支持为 API Key 配置 IP 访问白名单等精细权限控制。

### 时效性与安全

- API Key 创建后无失效日期，手动删除后即失效。
- 如需临时访问权限，可生成有效期 60 秒的临时 API Key。
- RAM 用户被禁用或删除后，其创建的所有 API Key 均将失效。
- 每个主账号在华北2（北京）、新加坡、德国（法兰克福）地域各最多可创建 50 个 API Key；美国（弗吉尼亚）地域每个归属账号最多 20 个。

> **注意**：Coding Plan 使用专属 API Key（格式 `sk-sp-xxxxx`），与百炼通用 API Key（格式 `sk-xxxxx`）不同，请勿混用。

## 配置环境变量

为避免在代码中硬编码 API Key 导致泄漏风险，建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`。详细的分平台操作步骤请参见 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

### 各平台快速配置

**Linux（永久生效）**：

```bash
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.bashrc
source ~/.bashrc
```

**macOS（Zsh，永久生效）**：

```bash
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
source ~/.zshrc
```

**Windows（CMD，永久生效）**：

```cmd
setx DASHSCOPE_API_KEY "YOUR_DASHSCOPE_API_KEY"
```

**Windows（PowerShell，永久生效）**：

```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_DASHSCOPE_API_KEY", [EnvironmentVariableTarget]::User)
```

### 常见问题

设置环境变量后代码仍提示找不到 API Key，常见原因包括：

- 仅设置了临时环境变量，未设置永久性环境变量
- 未重启 IDE、命令行工具或应用程序
- 使用 `sudo` 运行脚本时未加 `-E` 参数传递环境变量
- 应用通过服务管理器（如 systemd）启动，需在其配置文件中添加环境变量

## 安装 SDK

百炼支持两套 SDK 体系：阿里云官方的 DashScope SDK（Python、Java）和 OpenAI 官方的多语言 SDK（Python、Node.js、Java、Go）。完整安装指南请参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### SDK 安装速查

| 语言 | DashScope SDK | OpenAI SDK | 最低版本要求 |
|------|---------------|------------|-------------|
| Python | `pip install -U dashscope` | `pip install -U openai` | Python >= 3.8 |
| Java | Maven/Gradle: `com.alibaba:dashscope-sdk-java` | Maven/Gradle: `com.openai:openai-java`（推荐 3.5.0） | Java 8+ |
| Node.js | — | `npm install --save openai` | — |
| Go | — | `go get github.com/openai/openai-go/v3` | Go 1.22+ |

安装完成后即可使用对应 SDK 调用文本生成、图像生成、视频生成、语音合成、语音识别、向量模型、排序模型等各类模型。

## 常见错误码

调用模型 API 失败时，可根据返回的错误码排查问题。完整列表请参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。以下列出最常见的几类。

### 参数校验类（400 InvalidParameter）

| 错误信息关键词 | 原因 | 解决方案 |
|---------------|------|---------|
| `Model not exist.` | 模型名称错误或格式不正确 | 核对模型列表中的名称，注意大小写和空格，勿混用开源社区模型名与百炼模型 ID |
| `Range of input length should be [1, xxx]` | 输入 Token 超过模型上限 | 缩短 messages 内容或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | `max_tokens` 超出模型最大输出 Token 数 | 参考模型列表调整取值 |
| `Temperature should be in [0.0, 2.0)` | temperature 参数越界 | 设置为 [0.0, 2.0) 范围内的数字 |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查 JSON 结构是否完整（多余逗号、括号未闭合等） |

### 流式与思考模式

| 错误信息关键词 | 原因 | 解决方案 |
|---------------|------|---------|
| `enable_thinking must be set to false for non-streaming calls` | 思考模式仅支持[流式输出](../concepts/streaming-output.md) | 启用 `stream` 或将 `enable_thinking` 设为 `false` |
| `incremental_output parameter must be "true"` | 思考模式要求增量[流式输出](../concepts/streaming-output.md) | 设置 `incremental_output=true` |
| `Json mode response is not supported when enable_thinking is true` | 结构化输出与思考模式不兼容 | 关闭 `enable_thinking` |
| `This model only support stream mode` | 模型仅支持流式调用 | 启用 `stream` 参数 |

### 文件与多模态

| 错误信息关键词 | 原因 | 解决方案 |
|---------------|------|---------|
| `Invalid file [id:file-fe-xxx]` | file-id 无效或不属于当前账号 | 确认 file-id 有效，或重新上传文件获取新 ID |
| `File format is not supported` | Qwen-Long 仅支持纯文本格式 | 使用 TXT/DOCX/PDF/EPUB/MOBI/MD 格式 |
| `File exceeds size limit` | 文件超过 150 MB | 压缩文件至 150 MB 以内 |
| `Exceeded limit on max bytes per data-uri item` | 本地文件 Base64 编码后超过 10 MB | 压缩文件或改用 URL 方式传入 |
| `image length and width do not meet the model restrictions` | 图像尺寸不符合要求 | 确保宽高均 >= 10px，宽高比不超过 200:1 |
| `The provided URL does not appear to be valid` | URL 格式不正确 | URL 需以 `http://`、`https://` 或 `data:` 开头；本地路径需以 `file://` 开头 |

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


