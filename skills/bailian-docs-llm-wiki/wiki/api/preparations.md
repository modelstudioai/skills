# preparations

调用阿里云百炼平台的模型 API 前，需要完成三项准备工作：获取 API Key、配置环境变量、安装 SDK。本文汇总这些步骤的要点及常见错误码，帮助开发者快速完成接入准备。

## 获取 API Key

API Key 是调用百炼服务的唯一鉴权凭证。在百炼控制台的 **API Key** 页面即可创建，需使用主账号或具备相应页面权限的子账号操作。详细流程参见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 多地域支持

百炼目前在以下地域提供服务，每个地域有独立的控制台入口和 Base URL：

| 地域 | Base URL |
|------|----------|
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

其中新加坡和德国（法兰克福）地域的 Base URL 需将 `{WorkspaceId}` 替换为实际的[业务空间](../concepts/workspace.md) ID。

### 权限与配额

- API Key 的调用权限由**归属[业务空间](../concepts/workspace.md)**决定。默认[业务空间](../concepts/workspace.md)下的 API Key 可调用所有标准模型；子业务空间的 API Key 仅限已授权的模型。
- 华北2（北京）地域支持为 API Key 配置 IP 访问白名单（IPv4/IPv6，最多 20 条）。
- 每个主账号在每个地域最多可创建 50 个 API Key（美国弗吉尼亚地域为每个归属账号 20 个）。
- API Key 无失效日期，删除后即失效。如需临时授权，可生成有效期 60 秒的临时 API Key。

> **注意**：Coding Plan 使用专属 API Key（格式 `sk-sp-xxxxx`），与本文介绍的百炼通用 API Key（格式 `sk-xxxxx`）不同。

## 配置环境变量

建议将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码导致泄露。不同操作系统的配置方式参见 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

### 快速参考

**Linux / macOS（永久生效）：**

```bash
# Bash
echo "export DASHSCOPE_API_KEY='your-api-key'" >> ~/.bashrc
source ~/.bashrc

# Zsh（macOS 默认）
echo "export DASHSCOPE_API_KEY='your-api-key'" >> ~/.zshrc
source ~/.zshrc
```

**Windows（CMD 永久生效）：**

```cmd
setx DASHSCOPE_API_KEY "your-api-key"
```

**Windows（PowerShell 永久生效）：**

```powershell
[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY", "your-api-key", [EnvironmentVariableTarget]::User)
```

配置后需重启 IDE、终端或应用程序才能加载新的环境变量。使用 `sudo` 运行脚本时，需加 `-E` 参数以继承当前用户的环境变量。

## 安装 SDK

百炼同时提供 DashScope SDK 和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，开发者可根据语言偏好选择。完整安装说明参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

| 语言 | DashScope SDK | OpenAI SDK |
|------|--------------|------------|
| Python（≥3.8） | `pip install -U dashscope` | `pip install -U openai` |
| Java | Maven/Gradle 引入 `com.alibaba:dashscope-sdk-java` | Maven/Gradle 引入 `com.openai:openai-java`（推荐 ≥3.5.0，需 Java 8+） |
| Node.js | - | `npm install --save openai` |
| Go（≥1.22） | - | `go get github.com/openai/openai-go/v3` |

Node.js 安装失败时可先配置镜像源：`npm config set registry https://registry.npmmirror.com/`。Go 超时可设置代理：`go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 常见错误码

调用失败时，API 会返回错误码和描述信息。以下列出高频错误及解决思路，完整列表参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

### 参数类错误（400-InvalidParameter）

| 错误信息关键词 | 原因 | 解决方案 |
|---------------|------|---------|
| `Model not exist` | 模型名称拼写错误或大小写不对 | 核对模型列表，注意使用百炼模型 ID 而非开源社区名称 |
| `Range of input length should be [1, xxx]` | 输入 Token 超过模型上限 | 缩减 messages 长度或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | `max_tokens` 超出模型最大输出 | 参考模型列表中的最大输出 Token 数 |
| `enable_thinking must be set to false for non-streaming calls` | 思考模式仅支持[流式输出](../concepts/streaming.md) | 设置 `stream=true` 或关闭 `enable_thinking` |
| `Required body invalid` | 请求体 JSON 格式错误 | 检查 JSON 结构，注意多余逗号、未闭合括号等 |
| `messages with role "tool" must be a response to...` | 工具调用时缺少 Assistant Message | 先将模型的 tool_calls 响应加入 messages，再追加 Tool Message |

### 文件类错误

| 错误信息关键词 | 原因 | 解决方案 |
|---------------|------|---------|
| `Invalid file` | file-id 无效或不属于当前账号 | 通过 File 接口确认或重新上传 |
| `File format is not supported` | 文件格式不受支持 | Qwen-Long 仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD |
| `exceeds size limit` | 文件超过 150 MB | 压缩或拆分文件 |
| `Exceeded limit on max bytes per data-uri item` | Base64 编码的本地文件超过 10 MB | 压缩文件或改用 URL 方式传入 |

### 多模态类错误

| 错误信息关键词 | 原因 | 解决方案 |
|---------------|------|---------|
| `image length and width do not meet` | 图像尺寸不合规 | 宽高均 ≥10px，宽高比不超过 200:1 |
| `range of sequence images should be (4, 512)` | 视频帧数量不符合要求 | Qwen3-VL/Qwen2.5-VL 需 4-512 张，其他模型 4-80 张 |
| `URL does not appear to be valid` | 输入的 URL 或本地路径格式错误 | URL 以 `http(s)://` 或 `data:` 开头，本地路径以 `file://` 开头 |

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)



