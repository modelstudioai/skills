# preparations

在调用阿里云百炼平台的大模型 API 之前，需要完成 API Key 获取、环境变量配置和 SDK 安装三项准备工作。本文汇总了这些前置步骤的关键信息，并整理了常见错误码及其解决方案，帮助开发者快速排障上手。

## 获取与管理 API Key

API Key 是调用百炼模型和应用的唯一鉴权凭证。创建 API Key 需要主账号或具备相应页面权限的子账号操作。详细流程请参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 各地域控制台入口

| 地域 | 控制台地址 | Base URL |
|------|-----------|----------|
| 华北2（北京） | `bailian.console.aliyun.com` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `modelstudio.console.aliyun.com/ap-southeast-1` | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `dashscope-us.aliyuncs.com` | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `bailian.console.aliyun.com/eu-central-1` | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

### 权限与[业务空间](../concepts/workspace.md)

- API Key 的调用权限由其**归属[业务空间](../concepts/workspace.md)**决定，同一空间内的 API Key 权限相同，无需为不同模型类型分别创建。
- 默认[业务空间](../concepts/workspace.md)下的 API Key 可调用所有标准模型；子业务空间下的 API Key 仅可调用已授权的模型。
- 目前仅华北2（北京）地域支持为 API Key 配置 IP 访问白名单等精细权限控制。

### 数量限制

- 华北2（北京）、新加坡、德国（法兰克福）：每个主账号每地域最多 50 个 API Key。
- 美国（弗吉尼亚）：每个归属账号最多 20 个 API Key。

### 安全注意事项

- API Key 创建后永久有效，手动删除后即失效。
- 若需临时访问权限，可生成有效期 60 秒的临时 API Key。
- RAM 用户被禁用或删除后，其创建的所有 API Key 均失效。
- Coding Plan 使用专属 API Key（格式 `sk-sp-xxxxx`），不同于通用 API Key（格式 `sk-xxxxx`）。

## 配置 API Key 到环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码导致泄露。各操作系统的配置方式请参见 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

### 快速配置

**Linux / macOS (Zsh)**：

```bash
echo "export DASHSCOPE_API_KEY='YOUR_KEY'" >> ~/.zshrc
source ~/.zshrc
```

**Linux / macOS (Bash)**：

```bash
echo "export DASHSCOPE_API_KEY='YOUR_KEY'" >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell，永久)**：

```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_KEY", [EnvironmentVariableTarget]::User)
```

### 环境变量不生效的常见原因

1. 仅设置了临时环境变量，IDE 或其他应用未加载。
2. 设置后未重启 IDE、命令行工具或应用服务。
3. 使用 `sudo` 运行脚本时未传递环境变量（可用 `sudo -E` 解决）。
4. 通过 systemd 等服务管理器启动的应用需在其配置文件中单独添加环境变量。

## 安装 SDK

百炼同时支持官方 DashScope SDK 和 OpenAI 兼容 SDK，开发者可根据语言和偏好选择。完整安装说明请参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### 支持的 SDK 一览

| 语言 | DashScope SDK | OpenAI 兼容 SDK |
|------|--------------|----------------|
| Python (>=3.8) | `pip install -U dashscope` | `pip install -U openai` |
| Java (>=8) | Maven/Gradle: `com.alibaba:dashscope-sdk-java` | Maven/Gradle: `com.openai:openai-java`（推荐 3.5.0+） |
| Node.js | - | `npm install --save openai` |
| Go (>=1.22) | - | `go get github.com/openai/openai-go/v3` |

> **注意**：Node.js 安装失败时可配置镜像源 `npm config set registry https://registry.npmmirror.com/`；Go 安装超时可设置代理 `go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 常见错误码速查

调用失败时返回的错误码及解决方案详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)，以下列出高频问题：

### 参数校验类 (400)

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Model not exist` | 模型名称错误或大小写不对 | 对照模型列表检查，勿混用开源社区名与百炼模型 ID |
| `Range of input length should be [1, xxx]` | 输入 Token 超过模型上限 | 缩减 messages 长度或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | `max_tokens` 超出范围 | 参考模型列表中的最大输出 Token 数 |
| `enable_thinking must be set to false for non-streaming calls` | 思考模式仅支持[流式输出](../concepts/streaming.md) | 设置 `enable_thinking=false` 或改用流式调用 |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查括号闭合、多余逗号等 |

### 文件与多模态类

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Exceeded limit on max bytes per data-uri item` | 本地文件 Base64 超 10 MB | 压缩文件或改用 URL 方式传入 |
| `File format is not supported` | Qwen-Long 仅支持纯文本格式 | 图片内容请使用千问 VL 模型 |
| `Too many files provided` | file-id 数量超过 100 | 减少文件数量 |

### 流式与工具调用类

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `This model only support stream mode` | 模型仅支持[流式输出](../concepts/streaming.md) | 启用 `stream=true` |
| `The tool call is not supported` | 模型不支持 Function Calling | 更换为支持 FC 的 Qwen 或 DeepSeek 模型 |
| `messages with role "tool" must be a response to a preceeding message with "tool_calls"` | 缺少 Assistant Message | 先将模型的 tool_calls 响应加入 messages |

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


