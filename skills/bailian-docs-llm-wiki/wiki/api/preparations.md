# preparations

在调用阿里云百炼平台的大模型 API 之前，需要完成几项准备工作：获取 API Key 作为鉴权凭证、安装对应语言的 SDK、了解常见错误码以便排障，以及可选地安装百炼 CLI 命令行工具。本文汇总了这些前置步骤的关键信息。

## 获取 API Key

API Key 是调用百炼模型服务的唯一鉴权凭证。创建时需要主账号或具备相应页面权限的子账号操作。

**创建流程：**

1. 进入[百炼控制台](https://bailian.console.aliyun.com) API Key 管理页面
2. 选择归属[业务空间](../concepts/workspace.md)（建议选择默认[业务空间](../concepts/workspace.md)）
3. 配置权限（全部 / 自定义 IP 白名单和模型范围）
4. 创建后立即复制保存，关闭弹窗后无法再次查看明文

**权限模型：** API Key 的调用权限由其归属[业务空间](../concepts/workspace.md)决定。同一空间内的 API Key 权限相同，无需为不同模型类型（文生文、文生图、语音合成等）分别创建。子业务空间的 API Key 仅可调用该空间已授权的模型。

**安全要点：**

- 升级后新创建的 Key 以 `sk-ws` 开头，仅创建时展示一次明文
- [Token](../concepts/token.md) Plan 使用专属 Key（以 `sk-sp-` 开头），获取方式不同
- 建议配置到环境变量，避免硬编码泄露风险
- 每个主账号每个地域最多可创建 50 个 API Key（美国地域为每账号 20 个）

详细操作步骤和环境变量配置方法参见[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

## 安装 SDK

百炼支持两套 SDK 体系：

| SDK | 语言支持 | 安装方式 |
|-----|---------|---------|
| OpenAI SDK（推荐） | Python、Node.js、Java、Go | 各语言标准包管理器安装 |
| [DashScope SDK](../concepts/dashscope-sdk.md) | Python、Java | pip / Maven / Gradle |

**Python（OpenAI SDK）：**

```bash
pip install -U openai
```

**Python（[DashScope SDK](../concepts/dashscope-sdk.md)）：**

```bash
pip install -U dashscope
```

**Node.js：**

```bash
npm install --save openai
```

**Java（OpenAI SDK，Maven）：**

```xml
<dependency>
  <groupId>com.openai</groupId>
  <artifactId>openai-java</artifactId>
  <version>the-latest-version</version>
</dependency>
```

**Go：**

```bash
go get 'github.com/openai/openai-go/v3'
```

> **注意**：Go SDK 需要 Go 1.22+，Java OpenAI SDK 需要 Java 8+，Python 需要 3.8+。Node.js 安装失败时可配置镜像源 `npm config set registry https://registry.npmmirror.com/`。

完整安装说明和后续步骤参见[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

## 百炼 CLI

百炼 CLI（`bl` 命令）是面向 AI Agent 的命令行工具，支持文本对话、图像/视频生成、语音合成等全部百炼能力。

**安装：**

```bash
# 需要 Node.js >= 22.12.0
npm install -g bailian-cli

# 安装 Skills
npx skills add modelstudioai/cli --all -g
```

**认证方式：**

- 控制台登录（推荐）：`bl auth login --console`
- API Key 登录：`bl auth login --api-key sk-xxx`
- 环境变量 / 配置文件 / 临时传入

**核心命令：**

- `bl text chat` — 文本对话
- `bl image generate / edit` — 图像生成与编辑
- `bl video generate / edit / ref` — 视频生成与编辑
- `bl speech synthesize` — 语音合成
- `bl vision describe` — 视觉理解
- `bl omni` — 全模态对话

详细命令参考和使用场景参见[使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

## 常见错误码与排障

调用失败时，API 会返回结构化的错误信息。以下是高频错误及处理方式：

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| `Model not exist` | 模型名称拼写错误或大小写不对 | 对照模型列表确认名称，勿用开源社区名 |
| `Range of input length should be [1, xxx]` | 输入 [Token](../concepts/token.md) 超过模型上限 | 缩减 messages 长度或开启新对话 |
| `enable_thinking must be set to false for non-streaming` | 思考模式不支持非流式调用 | 设为 `false` 或改用[流式输出](../concepts/streaming.md) |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查括号闭合、多余逗号等 |
| `Arrearage` | 账号欠费 | 前往费用中心充值 |

更多错误码、参数范围限制及详细解决方案参见[错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 环境变量配置速查

将 API Key 配置到环境变量 `DASHSCOPE_API_KEY` 是推荐做法：

| 系统 | 永久生效命令 |
|------|------------|
| Linux (Bash) | `echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.bashrc && source ~/.bashrc` |
| macOS (Zsh) | `echo 'export DASHSCOPE_API_KEY="sk-xxx"' >> ~/.zshrc && source ~/.zshrc` |
| Windows (CMD) | `setx DASHSCOPE_API_KEY "sk-xxx"` |
| Windows (PowerShell) | `[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "sk-xxx", "User")` |

配置后需重启 IDE 或终端窗口才能生效。使用 `sudo` 运行脚本时需加 `-E` 参数以继承环境变量。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)


