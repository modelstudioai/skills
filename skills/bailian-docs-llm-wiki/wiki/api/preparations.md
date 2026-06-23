# preparations

调用阿里云百炼模型 API 前的准备工作包括：获取并保管 API Key、安装对应语言的 SDK、把 API Key 配置到环境变量以避免硬编码，以及在调用失败时根据错误码定位问题。本文把分散在四篇官方文档中的要点整合为一份开发者快速上手清单。

## 一、获取 API Key

API Key 是调用百炼大模型与应用的鉴权凭证，需使用主账号或具备 `管理员` / `API-Key` 页面权限的子账号操作，详细步骤见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

### 创建入口与地域差异

- **华北2（北京）**：控制台右上角选择地域 → 进入 API Key 页面 → 创建 API Key，可配置权限为「全部」或「自定义」（IP 白名单，最多 20 条 IPv4/IPv6 地址或网段）。
- **新加坡 / 日本（东京）/ 德国（法兰克福）/ 美国（弗吉尼亚）**：切换地域后进入「工作台 → API Key」，权限随归属[业务空间](../concepts/workspace.md)而定，暂不支持 IP 白名单。

### 配额与时效

- 华北2、新加坡、东京、法兰克福：每个主账号在每个地域最多创建 **50** 个 API Key；美国（弗吉尼亚）每个归属账号最多 **20** 个。
- API Key **没有失效日期**，手动删除后失效；如需临时授权，可生成有效期 60 秒的临时 API Key。
- RAM 用户被禁用或删除后，其创建的 API Key 全部失效。

### Key 格式与安全升级

| 对比项 | 升级前 | 升级后 |
| --- | --- | --- |
| 前缀 | `sk-`（约 32 位） | `sk-ws`（更长） |
| 明文查看 | 控制台随时复制 | 仅创建时展示一次 |
| 适用地域 | 除美国（弗吉尼亚）外 | 除美国（弗吉尼亚）外 |

> **注意**：百炼已对按量付费 API Key 做安全升级（美国弗吉尼亚地域除外），升级前的旧 Key 仍可用，但建议创建新 Key 替换以获得更完善的安全保障。

### 权限模型

API Key 的调用权限完全由**归属[业务空间](../concepts/workspace.md)**决定，同一空间内的 Key 权限相同，无需为不同模态（文生文/文生图/语音）分别创建 Key：

- 默认[业务空间](../concepts/workspace.md)下的 Key：可调用所有标准模型及该空间内的应用。
- 子业务空间下的 Key：仅可调用该子空间已授权的标准模型及应用。
- 在百炼调优后的模型：部署成功后仅能用其所在业务空间的 Key 调用，无需额外授权。

## 二、安装 SDK

百炼同时支持阿里云官方 [DashScope SDK](../concepts/dashscope-sdk.md) 和 [OpenAI 兼容接口](../concepts/openai-compatible.md)下的 OpenAI 官方多语言 SDK，具体安装方式见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

| 语言 | [DashScope SDK](../concepts/dashscope-sdk.md) | OpenAI 兼容 SDK | 版本要求 |
| --- | --- | --- | --- |
| Python | `pip install -U dashscope` | `pip install -U openai` | Python ≥ 3.8 |
| Java | `com.alibaba:dashscope-sdk-java` | `com.openai:openai-java`（推荐 3.5.0） | Java ≥ 8 |
| Node.js | — | `npm install --save openai` | — |
| Go | — | `github.com/openai/openai-go/v3` | Go ≥ 1.22 |

> **注意**：Node.js 安装失败时可配置镜像源 `npm config set registry https://registry.npmmirror.com/`；Go 拉取超时可设置 `go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 三、配置 API Key 到环境变量

为避免在代码中硬编码 API Key 造成泄露，强烈建议将其配置到环境变量 `DASHSCOPE_API_KEY`，完整步骤见 [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)。

### Linux / macOS

- **永久生效**：写入对应 Shell 配置文件后 `source` 使其生效。
  - Linux Bash：`echo "export DASHSCOPE_API_KEY='YOUR_KEY'" >> ~/.bashrc && source ~/.bashrc`
  - macOS Zsh：`echo "export DASHSCOPE_API_KEY='YOUR_KEY'" >> ~/.zshrc && source ~/.zshrc`
  - macOS Bash：写入 `~/.bash_profile` 后 `source`
- **临时生效**（仅当前会话）：`export DASHSCOPE_API_KEY="YOUR_KEY"`

### Windows

- **系统属性**：`Win+Q` 搜索「编辑系统环境变量」→ 新建系统变量 `DASHSCOPE_API_KEY`，永久生效，但需重启已打开的 IDE/命令行才能加载。
- **CMD 永久**：`setx DASHSCOPE_API_KEY "YOUR_KEY"`（新开窗口生效）；**临时**：`set DASHSCOPE_API_KEY=YOUR_KEY`
- **PowerShell 永久**：`[Environment]::SetEnvironmentVariable("DASHSCOPE_API_KEY","YOUR_KEY","User")`；**临时**：`$env:DASHSCOPE_API_KEY = "YOUR_KEY"`

### 常见排错

`echo` 能查到但代码仍报找不到 API Key，通常是以下原因：

1. 只设了临时变量，IDE 或已启动的应用未加载最新环境变量 → 设永久变量并重启程序。
2. 用 `sudo python xx.py` 运行 → 改用 `sudo -E python xx.py`，`-E` 保证环境变量被传递。
3. 由 systemd/supervisord 等服务管理器启动 → 在服务配置文件中显式添加环境变量。

## 四、错误码速查

模型调用失败时，可通过 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档对照解决，也可把完整报错信息提交给阿里云 AI 助理快速定位。常见类别如下。

### 鉴权与额度

- `Arrearage / Access denied`：账号欠费，前往「费用与成本」充值后等待几分钟。
- `Model not exist.`：`model` 参数大小写或空格错误，或混用了开源社区模型名（如 `Qwen/Qwen3-235B-A22B-Instruct-2507`），应使用百炼模型 ID（如 `qwen3-235b-a22b-instruct-2507`）。

### 参数取值范围

| 参数 | 合法范围 |
| --- | --- |
| `temperature` | `[0.0, 2.0)` |
| `top_p` | `(0.0, 1.0]` |
| `top_k` | `≥ 0` |
| `presence_penalty` | `[-2.0, 2.0]` |
| `repetition_penalty` | `> 0.0` |
| `n` | `[1, 4]` |
| `seed`（DashScope 协议） | `[0, 9223372036854775807]` |
| `max_tokens` | `[1, 模型最大输出 Token 数]` |

### 流式与思考模式

- `enable_thinking must be set to false for non-streaming calls`：思考模式模型需用[流式输出](../concepts/streaming-output.md)，或将 `enable_thinking` 设为 `false`。
- `incremental_output parameter must be "true" when enable_thinking is true`：开思考模式时必须 `incremental_output=true`。
- `The value of the enable_thinking parameter is restricted to True.`：部分模型（如 `qwen3-235b-a22b-thinking-2507`）不可关闭思考模式。
- `Json mode response is not supported when enable_thinking is true`：结构化输出与思考模式互斥，需 `enable_thinking=false`。

### 多模态与文件

- 多模态本地文件 Base64 后单个不超过 10 MB；URL 方式下视频上限按模型不同为 150MB / 1GB / 2GB。
- Qwen-Long 仅支持 TXT/DOCX/PDF/EPUB/MOBI/MD，单文件 < 150MB、< 15000 页、file-id 数量 < 100。
- 视觉模型图像尺寸要求宽高均 ≥ 10 像素，宽高比不超过 200:1 或 1:200；视频以图像列表输入时，Qwen3-VL/Qwen2.5-VL 需 4-512 张，其他模型需 4-80 张。
- 传入临时 URL 时，HTTP 调用需在 Header 加 `X-DashScope-OssResourceResolve: enable`，SDK 调用仅 [DashScope SDK](../concepts/dashscope-sdk.md) 支持（OpenAI SDK 不支持）。

### 消息与请求体

- `Either "prompt" or "messages" must exist`：必须指定 `messages`；DashScope-HTTP 下 `messages` 需放入 `input` 对象中，不能与 `model` 并列。
- `messages with role "tool" must be a response to a preceeding message with "tool_calls"`：工具调用时需先把第一轮 Assistant Message 加入 messages 数组，再追加 Tool Message。
- `'messages' must contain the word 'json'`：使用 `response_format=json_object` 时，提示词中必须出现 `json`（不区分大小写）。
- `Tool names are not allowed to be [search]`：工具名不能取 `search`。
- `tool_choice` 仅支持 `"auto"` 或 `"none"`。

### 接口方法与限流

- `Request method 'GET' is not supported.`：接口仅支持 POST 等方法，请查阅接口文档。
- `Value error, batch size is invalid`：Embedding 文本数量超限，参考模型批次大小调整。
- `Range of input length should be [1, xxx]`：输入 Token 超限，连续对话场景请开启新对话。

## 快速上手顺序

1. 在百炼控制台获取 API Key 并立即复制保存（关闭弹窗后不可再查）。
2. 按所用语言安装 DashScope SDK 或 OpenAI 兼容 SDK。
3. 将 API Key 写入环境变量 `DASHSCOPE_API_KEY`，重启 IDE/终端使其生效。
4. 编写首次调用代码，调用失败时按错误码文档或 AI 助理排查。

## 来源文档

- [将API Key配置到环境变量](../../raw/model-api-reference/preparations/configure-api-key-through-environment-variables.md)
- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)


