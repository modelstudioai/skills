# preparations

在调用阿里云百炼平台的模型 API 之前，需要完成 API Key 获取、SDK 安装和环境配置等准备工作。本文汇总了开发者接入百炼平台前的必要步骤，以及调用过程中常见错误的排查方法。

## 获取与配置 API Key

API Key 是调用百炼模型和应用的鉴权凭证。前往百炼控制台的 API Key 页面，使用主账号或具备相应权限的子账号创建 API Key。详细步骤参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 创建 API Key

不同地域的创建流程略有差异：

- **华北2（北京）、新加坡、日本（东京）、德国（法兰克福）**：支持配置归属[业务空间](../concepts/workspace.md)、描述和权限（全部或自定义）。自定义权限可设置 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）和可访问模型范围。
- **美国（弗吉尼亚）**：需额外选择归属账号，不支持禁用、重置和自定义权限配置。

创建成功后，新版 API Key 以 `sk-ws` 开头，**仅在创建时展示一次明文**，关闭弹窗后无法再次查看。请立即复制保存。

### API Key 数量限制

- 华北2（北京）等地域：每个主账号每个地域最多 50 个。
- 美国（弗吉尼亚）：每个归属账号最多 20 个。

### 权限与作用域

API Key 的调用权限由其归属[业务空间](../concepts/workspace.md)决定，同一空间内的 API Key 权限相同，无需为不同模型类型分别创建。默认[业务空间](../concepts/workspace.md)的 Key 可调用所有标准模型；子业务空间的 Key 仅可调用已授权的模型。

### 配置到环境变量

建议将 API Key 配置为环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

```bash
# Linux / macOS (Bash)
echo "export DASHSCOPE_API_KEY='your-api-key'" >> ~/.bashrc
source ~/.bashrc

# macOS (Zsh)
echo "export DASHSCOPE_API_KEY='your-api-key'" >> ~/.zshrc
source ~/.zshrc

# Windows CMD（永久）
setx DASHSCOPE_API_KEY "your-api-key"

# Windows PowerShell（永久）
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-api-key", [EnvironmentVariableTarget]::User)
```

> **注意**：设置环境变量后，已打开的 IDE、终端或应用程序需要重启才能加载新值。使用 `sudo` 运行脚本时，需加 `-E` 参数以继承当前用户的环境变量。

## 安装 SDK

百炼支持两套 SDK 体系：DashScope 官方 SDK 和 OpenAI 兼容 SDK。具体安装方式参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### Python

```bash
# OpenAI SDK
pip install -U openai

# DashScope SDK
pip install -U dashscope
```

要求 Python >= 3.8。

### Java

- **[DashScope SDK](../concepts/dashscope-sdk.md)**：Maven 坐标 `com.alibaba:dashscope-sdk-java`
- **OpenAI SDK**：Maven 坐标 `com.openai:openai-java`（推荐 3.5.0+，需 Java 8+）

### Node.js

```bash
npm install --save openai
```

如遇网络问题，可先配置镜像源：`npm config set registry https://registry.npmmirror.com/`

### Go

```bash
go get 'github.com/openai/openai-go/v3'
```

需要 Go 1.22+。如访问超时，可设置阿里云镜像代理。

## 使用百炼 CLI

百炼 CLI（`bailian-cli`）是面向 AI Agent 的命令行工具，可通过一行命令集成百炼平台的文本、图像、视频、语音等 AI 能力。详细用法参见 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

### 安装

```bash
# 安装 CLI（需 Node.js >= 22.12.0，仅支持 npm）
npm install -g bailian-cli

# 安装 Skills
npx skills add modelstudioai/cli --all -g

# 验证
bl --version
```

### 认证

| 方式 | 命令 | 适用场景 |
|------|------|----------|
| 控制台登录（推荐） | `bl auth login --console` | 交互式环境，模型调用 + 应用管理 |
| API Key | `bl auth login --api-key sk-xxx` | 模型调用 |
| 环境变量 | 配置 API Key 环境变量 | CI/CD、无界面环境 |

### 常用命令

- `bl text chat --message "你好"`：文本对话
- `bl image generate --prompt "描述"`：文字生成图像
- `bl video generate --prompt "描述"`：文字生成视频
- `bl speech synthesize --text "文本"`：语音合成
- `bl vision describe --image <path>`：图像理解

支持 `--model` 指定模型、`--output json` 输出 JSON 格式、`--non-interactive` 非交互模式等全局参数。

## 常见错误码

调用模型 API 时可能遇到的典型错误及处理方式，完整列表参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

### 参数类错误（400）

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Model not exist` | 模型名称拼写或大小写错误 | 对照模型列表，使用百炼模型 ID（如 `qwen3-235b-a22b-instruct-2507`） |
| `Range of input length should be [1, xxx]` | 输入 Token 超过模型上限 | 缩减 messages 长度或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | `max_tokens` 超出模型限制 | 参考模型列表中的最大输出 Token 数 |
| `enable_thinking must be set to false for non-streaming calls` | 思考模式仅支持流式调用 | 设置 `enable_thinking=false` 或启用[流式输出](../concepts/streaming.md) |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查 JSON 是否有多余逗号、括号未闭合等问题 |

### 认证与权限类错误

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `Arrearage` | 账号欠费 | 登录阿里云控制台充值 |
| `InvalidApiKey` | API Key 无效或已删除 | 重新创建或重置 API Key |

### 文件相关错误

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `File format is not supported` | Qwen-Long 不支持该文件格式 | 使用 TXT、DOCX、PDF、EPUB、MOBI、MD 格式 |
| `File exceeds size limit` | 文件超过 150 MB | 压缩或拆分文件 |
| `Multimodal file size is too large` | [多模态](../concepts/multimodal.md)文件超限 | 本地文件 Base64 后不超过 10 MB；URL 图像不超过 10 MB |

> **注意**：遇到错误时，也可使用阿里云 AI 助理输入报错信息获取自动诊断和解决方案。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)



