# preparations

本页汇总调用阿里云百炼模型 API 前的准备工作：获取并安全配置 API Key、安装 SDK（DashScope 或 OpenAI 兼容）、安装百炼 CLI，以及调用出错时的错误码排查。完成这些步骤后，即可通过代码、第三方工具或命令行调用百炼平台的模型与应用。

## 1. 获取 API Key

API Key 是调用百炼模型和应用的鉴权凭证，详见[获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

- **操作入口**：百炼控制台右上角选择地域（华北2（北京）、新加坡、日本（东京）、德国（法兰克福），或美国（弗吉尼亚）走独立控制台），进入 API Key 页面创建。
- **权限要求**：需主账号，或具备 `管理员` / `API-Key` 页面权限的子账号。
- **关键配置**：
  - **归属[业务空间](../concepts/workspace.md)**：API Key 的调用权限完全由归属[业务空间](../concepts/workspace.md)决定，同一空间内权限相同，无需按模型类型创建多个 Key；子空间 Key 只能调用已授权模型和该空间内的应用；调优后的模型仅能用其所在空间的 Key 调用。
  - **权限**：`全部` 或 `自定义`（IP 白名单最多 20 个 IPv4/IPv6 地址或网段 + 可访问模型范围；美国（弗吉尼亚）地域不支持自定义配置）。
- **安全升级**：新创建的 Key 统一以 `sk-ws` 开头，仅在创建时展示一次明文，关闭弹窗后无法再次查看，丢失需重置或重建；旧的 `sk-` 开头 Key 可继续使用。
- **管理操作**：控制台支持编辑、删除、禁用、重置（禁用/重置在美国（弗吉尼亚）地域不可用）；也可通过 OpenAPI（CreateApiKey / ListApiKeys / ResetApiKey 等，需阿里云 AccessKey 签名而非 API Key）编程管理。

> **注意**：Token Plan / Coding Plan 使用以 `sk-sp-` 开头的专属 API Key，与本文按量付费 API Key 获取方式不同。

### 配置到环境变量

建议将 API Key 配置为环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄露：

- Linux：`echo "export DASHSCOPE_API_KEY='YOUR_KEY'" >> ~/.bashrc && source ~/.bashrc`
- macOS：按 `echo $SHELL` 判断写入 `~/.zshrc` 或 `~/.bash_profile`
- Windows：系统属性图形界面，或 CMD `setx DASHSCOPE_API_KEY "YOUR_KEY"`，或 PowerShell `[Environment]::SetEnvironmentVariable(...)`

调用时除 API Key 外还需指定服务端点（`base_url`）。百炼同时提供 **OpenAI 兼容**与 **Anthropic 兼容**两种协议，`base_url` 不同且随地域变化，以对应接口文档为准。

## 2. 安装 SDK

支持官方 DashScope SDK 与 OpenAI 官方 SDK 两条路线，详见[安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)：

| 语言 | SDK | 安装方式 | 版本要求 |
| --- | --- | --- | --- |
| Python | OpenAI / DashScope | `pip install -U openai` / `pip install -U dashscope` | Python >= 3.8 |
| Java | DashScope / OpenAI | Maven/Gradle 添加 `dashscope-sdk-java` 或 `com.openai:openai-java`（推荐 3.5.0） | Java 8+ |
| Node.js | OpenAI | `npm install --save openai` | — |
| Go | OpenAI | `go get github.com/openai/openai-go/v3` | Go 1.22+ |

网络不畅时可配置国内镜像：npm 用 `registry.npmmirror.com`，Go 用 `GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

## 3. 使用百炼 CLI（可选）

百炼 CLI（npm 包 `bailian-cli`，命令 `bl` / `bailian`）是面向 AI Agent 的命令行工具，详见[使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)：

- **安装**：要求 Node.js >= 22.12.0，仅支持 npm：`npm install -g bailian-cli`，可配套 `npx skills add modelstudioai/cli --all -g` 安装 Skills。
- **认证**：控制台浏览器登录 `bl auth login --console`（推荐，同时打通应用管理能力）、API Key 登录 `bl auth login --api-key sk-xxx`、环境变量、`bl config set --key api_key`（不校验 Key 有效性）、单次 `--api-key` 临时传入。
- **能力**：文本对话（`bl text chat`）、全模态（`bl omni`）、图像生成/编辑（`bl image generate/edit`）、视频生成/编辑/参考生成（`bl video generate/edit/ref`）、视觉理解（`bl vision describe`）、语音合成（`bl speech synthesize`）等。
- **常用全局参数**：`--region cn|us|intl`（默认 cn）、`--output text|json`、`--non-interactive`（Agent/CI 场景）、`--dry-run`、`--concurrent <n>`。
- **验证**：`bl auth status --output json`、`bl text chat --message "ping" --non-interactive --output json`。

> **注意**：切勿把真实 API Key 写入仓库、日志或公开渠道；CI 环境请用密钥管理或环境变量注入。

## 4. 错误码排查

调用失败时可对照[错误码](../../raw/model-api-reference/preparations/error-code.md)排查，也可将报错信息直接粘贴给阿里云 AI 助理分析。常见 400-InvalidParameter 类问题：

- **思考模式相关**：思考模式模型必须流式调用（`enable_thinking=true` 时需 `stream` + `incremental_output=true`，DashScope 协议下 `result_format="message"`）；部分模型（如 `qwen3-235b-a22b-thinking-2507`）不允许 `enable_thinking=false`；结构化输出（`json_object`）不能与思考模式同时开启。
- **参数范围**：`temperature` 在 [0.0, 2.0)、`top_p` 在 (0.0, 1.0]、`top_k >= 0`、`presence_penalty` 在 [-2.0, 2.0]、`n` 在 [1, 4]、`max_tokens` 不超过模型最大输出 Token 数、输入长度不超过模型上限（连续对话超限时开启新对话）。
- **模型与开通**：`Model not exist` 多为模型名大小写/格式错误（使用百炼模型 ID 而非开源社区名称）；`The product is not activated` 需先在模型市场开通目标模型或开通百炼服务。
- **messages 构造**：纯文本模型 `content` 只能是字符串，混入 `image_url` 等[多模态](../concepts/multimodal.md)元素会报错（需改用 Qwen-VL 等[多模态](../concepts/multimodal.md)模型）；Tool Message 前必须先追加含 `tool_calls` 的 Assistant Message；检测到连续重复的相同工具调用会被拦截，需在应用侧增加终止逻辑。
- **文件类**（Qwen-Long 等）：file-id 需有效且属于当前账号、数量小于 100、单文件小于 150 MB、仅支持纯文本格式（TXT/DOCX/PDF/EPUB/MOBI/MD）。
- **欠费**：`Arrearage` 表示账号欠费，需前往费用与成本页面充值。

## 推荐流程

1. 创建 API Key 并立即保存（新 Key 明文只展示一次）。
2. 将 Key 配置到 `DASHSCOPE_API_KEY` 环境变量。
3. 按语言安装 SDK（或安装百炼 CLI），确认对应协议的 `base_url`。
4. 发起首次调用验证，报错时对照错误码文档定位原因。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)


