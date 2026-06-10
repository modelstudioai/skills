# preparations

阿里云百炼平台的 API 调用前需要完成三项准备：获取 API Key、配置环境变量、安装 SDK。本文汇总从控制台创建密钥到各语言 SDK 安装的完整流程，并给出常见错误码的定位思路。

## 1. 获取 API Key

API Key 是调用百炼服务的鉴权凭证，需使用主账号或具备 `管理员` / `API-Key` 页面权限的子账号在控制台创建。不同地域入口略有差异：

- **华北2（北京）**：[API Key 页面](https://bailian.console.aliyun.com/?tab=model#/api-key) 创建时可选择**全部**或**自定义**权限，自定义权限支持配置最多 20 条 IPv4/IPv6 的 IP 访问白名单。
- **新加坡 / 美国（弗吉尼亚）/ 德国（法兰克福）**：创建后立即弹窗展示完整 Key，关闭后无法再次查看，需马上复制保存。

创建后的 API Key 永久有效，手动删除即失效。如需临时授权可使用[临时 API Key](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)（60 秒有效期）。

> **注意**：[Coding Plan](https://help.aliyun.com/zh/model-studio/coding-plan) 使用专属 API Key（格式 `sk-sp-xxxxx`），与本文介绍的通用 Key（格式 `sk-xxxxx`）不同，请勿混用。

详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

## 2. API Key 权限与使用

API Key 的调用权限由其**归属[业务空间](../concepts/workspace.md)**决定，同一空间内权限相同，无需为文生文、文生图、语音合成等不同模型创建多把 Key：

- **默认[业务空间](../concepts/workspace.md)**的 Key：可调用所有标准模型及默认空间内的应用。
- **子[业务空间](../concepts/workspace.md)**的 Key：仅可调用该空间已授权的标准模型及空间内应用。
- **调优后的模型**：部署后仅能由其所在业务空间的 Key 调用，无需额外授权。

### Base URL 对照

在第三方工具（Chatbox、Cline、Claude Code、Dify 等）中调用时需填入对应地域的 Base URL：

| 地域 | Base URL |
| --- | --- |
| 华北2（北京） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| 新加坡 | `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1` |
| 美国（弗吉尼亚） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| 德国（法兰克福） | `https://{WorkspaceId}.eu-central-1.maas.aliyuncs.com/compatible-mode/v1` |

新加坡与法兰克福地域需把 `WorkspaceId` 替换为真实的业务空间 ID。

## 3. 配置环境变量

为避免 API Key 硬编码导致泄露，建议写入环境变量 `DASHSCOPE_API_KEY`，各 SDK 默认从此变量读取。

### Linux / macOS

- **永久生效**：写入 shell 配置文件（`~/.bashrc`、`~/.zshrc` 或 `~/.bash_profile`），再 `source` 使其生效。
- **临时生效**：当前会话 `export DASHSCOPE_API_KEY="YOUR_DASHSCOPE_API_KEY"`。

### Windows

- **系统属性**：永久生效，需管理员权限，修改后需重启 IDE / 终端。
- **CMD**：`setx DASHSCOPE_API_KEY "..."`（永久）或 `set DASHSCOPE_API_KEY=...`（临时）。
- **PowerShell**：`[Environment]::SetEnvironmentVariable(...)`（永久）或 `$env:DASHSCOPE_API_KEY = "..."`（临时）。

> **注意**：`echo` 显示设置成功但代码仍提示找不到 Key，通常是三种原因：仅设了临时变量、未重启 IDE/应用、或通过 `sudo` 运行导致变量未继承（可用 `sudo -E`）。详见 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

## 4. 安装 SDK

百炼提供两种接入方式：官方 DashScope SDK（Python、Java）与 OpenAI 兼容的多语言 SDK（Python、Node.js、Java、Go）。

### Python（需 `>= 3.8`）

```bash
pip install -U openai       # OpenAI Python SDK
pip install -U dashscope    # DashScope Python SDK
```

### Java

通过 Maven / Gradle 引入：

```xml
<!-- DashScope -->
<dependency>
  <groupId>com.alibaba</groupId>
  <artifactId>dashscope-sdk-java</artifactId>
  <version>the-latest-version</version>
</dependency>

<!-- OpenAI（推荐 3.5.0+，需 Java 8+）-->
<dependency>
  <groupId>com.openai</groupId>
  <artifactId>openai-java</artifactId>
  <version>the-latest-version</version>
</dependency>
```

### Node.js

```bash
npm install --save openai
# 或 yarn add openai
```

### Go（需 `Go 1.22+`）

```bash
go get 'github.com/openai/openai-go/v3'
```

如服务器访问超时，可设置阿里云镜像：`go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

## 5. 常见错误码定位

调用失败时推荐先使用[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)输入报错信息获取诊断。高频错误分类如下：

### 参数类（400 InvalidParameter）

| 错误信息 | 原因与解决 |
| --- | --- |
| `parameter.enable_thinking must be set to false for non-streaming calls` | 思考模式模型必须使用[流式输出](../concepts/streaming-output.md)，或将 `enable_thinking` 设为 `false` |
| `This model only support stream mode` | 改用[流式输出](../concepts/streaming-output.md) |
| `Range of input length should be [1, xxx]` | messages Token 数超限，精简输入或开启新对话 |
| `Range of max_tokens should be [1, xxx]` | 按模型列表调整 `max_tokens` |
| `Temperature should be in [0.0, 2.0)` | `temperature` 取值范围 |
| `Range of top_p should be (0.0, 1.0]` | `top_p` 取值范围 |
| `'messages' must contain the word 'json'...` | 使用结构化输出时提示词需包含 `json` 关键词 |
| `Json mode response is not supported when enable_thinking is true` | 结构化输出与思考模式互斥，需关闭 `enable_thinking` |
| `Model not exist.` | 检查 `model` 拼写与大小写，勿混用开源模型名与百炼 ID |

### 文件 / 多模态类

- `File [id:file-fe-***] format is not supported.`：Qwen-Long 仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD，不处理图片，图片分析请用 Qwen-VL。
- `Too many files provided.`：file-id 数量需 < 100。
- `File exceeds size limit.`：文件 < 150 MB；多模态本地图像 Base64 后 < 10 MB。
- `Exceeded limit on max bytes per data-uri item`：Qwen3-VL/qwen-vl-max 视频 ≤ 2GB，qwen-vl-plus ≤ 1GB。

### 鉴权与账户类

- `Arrearage`：账号欠费，前往费用与成本页面充值。
- `Access denied`：检查 API Key 归属业务空间、RAM 用户是否被删除（删除后该用户创建的所有 Key 立即失效）。

### 数量限制

- 北京 / 新加坡 / 法兰克福：每个主账号在每个地域最多 **50** 把 Key。
- 美国（弗吉尼亚）：每个归属账号最多 **20** 把 Key。

完整错误码列表见 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


