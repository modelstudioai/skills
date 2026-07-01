# preparations

阿里云百炼平台提供大模型 API 调用能力，在开始调用前需要完成 [API Key](../concepts/api-key.md) 获取、SDK 安装等准备工作。本页汇总了接入前的必要步骤及常见错误码，帮助开发者快速完成环境搭建并排查调用异常。

## 获取 [API Key](../concepts/api-key.md)

[API Key](../concepts/api-key.md) 是调用百炼大模型服务的鉴权凭证。需使用主账号或具备相应页面权限的子账号，在[百炼控制台](https://bailian.console.aliyun.com/)的 API Key 页面创建。

### 创建流程

1. 进入控制台，选择目标地域（华北2（北京）、新加坡、日本（东京）、德国（法兰克福）或美国（弗吉尼亚））
2. 在 API Key 页面点击"创建 API Key"
3. 选择归属[业务空间](../concepts/workspace.md)（建议默认空间）和权限配置（全部或自定义）
4. 创建成功后**立即复制保存**明文密钥，关闭弹窗后无法再次查看

详细操作步骤及不同地域的差异请参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 权限与安全

- API Key 权限由其归属[业务空间](../concepts/workspace.md)决定，同一空间内的 Key 权限相同
- 支持自定义 IP 白名单（最多 20 个 IPv4/IPv6 地址或网段）和可访问模型范围
- 升级后新创建的 Key 以 `sk-ws` 开头，仅创建时展示一次明文
- API Key 无过期时间，手动删除后即失效；如需临时授权可生成有效期 60 秒的临时 API Key
- 每个主账号在每个地域最多可创建 50 个 API Key（美国地域每个归属账号最多 20 个）

### 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免在代码中硬编码：

```bash
# Linux / macOS (Zsh)
echo "export DASHSCOPE_API_KEY='YOUR_DASHSCOPE_API_KEY'" >> ~/.zshrc
source ~/.zshrc

# Windows PowerShell（永久）
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "YOUR_DASHSCOPE_API_KEY", [EnvironmentVariableTarget]::User)
```

> **注意**：设置环境变量后需重启 IDE 或终端窗口才能生效。使用 `sudo` 运行脚本时需加 `-E` 参数以继承环境变量。

## 安装 SDK

百炼支持通过 [DashScope SDK](../concepts/dashscope-sdk.md)（Python / Java）或 OpenAI 兼容 SDK（Python / Node.js / Java / Go）调用模型。详细安装说明参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

### Python

```bash
# OpenAI SDK（推荐，兼容性好）
pip install -U openai

# DashScope SDK
pip install -U dashscope
```

要求 Python >= 3.8。

### Java

通过 Maven 或 Gradle 引入依赖：

- **[DashScope SDK](../concepts/dashscope-sdk.md)**：`com.alibaba:dashscope-sdk-java`
- **OpenAI SDK**：`com.openai:openai-java`（推荐 3.5.0+，需 Java 8+）

### Node.js

```bash
npm install --save openai
```

### Go

```bash
go get 'github.com/openai/openai-go/v3'
```

需要 Go 1.22+。如访问超时可设置阿里云镜像代理。

## 常见错误码

调用失败时 API 会返回结构化错误信息。完整错误码列表及解决方案请参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。以下列出高频错误：

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `Model not exist` | model 参数名称或大小写错误 | 对照模型列表检查模型名称，勿使用开源社区名 |
| `Range of input length should be [1, xxx]` | 输入 [Token](../concepts/token.md) 超过模型上限 | 控制 messages 长度，连续对话时开启新会话 |
| `parameter.enable_thinking must be set to false for non-streaming calls` | 非流式调用思考模式 | 设置 `enable_thinking=false` 或改用流式输出 |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查 JSON 格式（多余逗号、括号未闭合等） |
| `Range of max_tokens should be [1, xxx]` | max_tokens 超出模型限制 | 参考模型列表的最大输出 [Token](../concepts/token.md) 数设置 |
| `This model does not support enable_search` | 模型不支持联网搜索 | 更换支持搜索能力的模型 |

### 参数取值范围速查

| 参数 | 取值范围 |
|------|---------|
| `temperature` | [0.0, 2.0) |
| `top_p` | (0.0, 1.0] |
| `top_k` | >= 0 |
| `repetition_penalty` | > 0 |
| `presence_penalty` | [-2.0, 2.0] |
| `n` | [1, 4] |
| `seed`（DashScope 协议） | [0, 9223372036854775807] |

## 后续步骤

完成 API Key 获取和 SDK 安装后，可以：

- 调用文本生成、图像生成、视频生成、语音合成/识别、向量/排序等模型
- 在第三方工具（Chatbox、Cline、Claude Code、Dify 等）中配置使用
- 了解与 OpenAI API 的兼容性详情

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


