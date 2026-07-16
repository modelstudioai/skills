# preparations

本页汇总在阿里云百炼平台调用模型 API 前的准备工作，涵盖获取鉴权凭证（API Key）、安装官方或兼容 SDK、使用百炼 CLI 快速集成，以及常见错误码的排查思路。面向开发者，帮助你从零完成环境搭建并稳定发起第一次调用。

## 获取并配置 API Key

调用模型或应用前，需先获取 API Key 作为鉴权凭证。需使用主账号，或具备 `管理员` / `API-Key` 页面权限的子账号，在[阿里云百炼控制台](https://bailian.console.aliyun.com/)对应地域的 **API Key** 页面创建。详见 [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)。

创建时的关键选项：

- **归属业务空间**：决定该 Key 的调用权限。同一空间内的 Key 权限相同，无需为不同模态（文生文、文生图、语音等）分别创建。默认业务空间的 Key 可调用所有标准模型及默认空间内的应用；子业务空间的 Key 只能调用已授权的模型及本空间应用。
- **权限**：可选 **全部**（调用所有模型与应用），或 **自定义**（配置 IP 白名单最多 20 个 IPv4/IPv6 地址或网段，以及可访问的模型/应用范围）。

> **注意**：百炼已对按量付费 API Key 做安全升级（美国（弗吉尼亚）地域除外）。升级后新建的 Key 以 `sk-ws` 开头，且**仅在创建时展示一次明文**，关闭弹窗后无法再次查看，务必立即复制保存；升级前 `sk-` 开头的旧 Key 仍可正常使用。此外，Token Plan / Coding Plan 使用以 `sk-sp-` 开头的专属 Key，不同于本文的按量付费 Key。

推荐将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免硬编码泄漏。各系统配置方式（`~/.bashrc`、`~/.zshrc`、`~/.bash_profile`、Windows 系统属性 / `setx` / PowerShell）参见原文。调用时除 API Key 外，还需指定**服务端点** `base_url`（即创建弹窗中的 API Host），且 OpenAI 兼容协议与 Anthropic 兼容协议的 `base_url` 不同、随地域变化，请以对应接口文档为准。

除控制台外，百炼还提供 OpenAPI（`CreateApiKey` / `GetApiKey` / `ListApiKeys` / `UpdateApiKey` / `DeleteApiKey` / `EnableApiKey` / `DisableApiKey` / `ResetApiKey`）以编程方式管理 Key，调用需使用阿里云账号 AccessKey 签名认证并具备相应 RAM 权限。

## 安装 SDK

百炼同时支持官方 **DashScope SDK**（Python、Java）与通过 **[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)**调用的多语言 SDK。详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。

- **Python**（需 `python >= 3.8`）：`pip install -U openai` 或 `pip install -U dashscope`
- **Java**：DashScope 用 `com.alibaba:dashscope-sdk-java`；OpenAI 用 `com.openai:openai-java`（需 Java 8+，推荐 `3.5.0`），均通过 Maven / Gradle 引入。
- **Node.js**：`npm install --save openai`（或 `yarn add openai`）；安装失败可配置镜像源 `npm config set registry https://registry.npmmirror.com/`。
- **Go**（需 `Go 1.22+`）：`go get 'github.com/openai/openai-go/v3'`；超时可设 `go env -w GOPROXY=https://mirrors.aliyun.com/goproxy/,direct`。

安装后即可调用文本生成、图像生成、视频生成、语音合成/识别、向量、排序等模型。

## 使用百炼 CLI

百炼 CLI（npm 包 `bailian-cli`，命令 `bl` / `bailian`）是面向 AI Agent 的命令行工具，可将平台能力集成到各类 AI 工具中。安装前置要求 **Node.js ≥ 22.12.0**，且**仅支持 npm 安装**（勿用 pnpm / yarn 安装该包）。详见 [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)。

```bash
# 1. 安装 CLI
npm install -g bailian-cli
# 2. 安装 Skills（注册能力描述文件到各 Agent）
npx skills add modelstudioai/cli --all -g
# 3. 验证
bl --version
```

**认证方式**（可组合使用，互不覆盖）：

| 方式 | 命令 | 适用场景 |
| --- | --- | --- |
| 控制台登录（推荐） | `bl auth login --console` | 模型调用 + 应用管理（浏览器 OAuth） |
| API Key | `bl auth login --api-key sk-xxx` | 模型调用；会先校验 Key 有效性 |
| 环境变量 | 配置 API Key 环境变量 | CI/CD、无界面环境 |
| 配置文件 | `bl config set --key api_key --value sk-xxx` | 持久化，**不校验** Key 有效性 |
| 临时传入 | `bl text chat --api-key sk-xxx ...` | 单次调用，不落盘 |

常用全局参数：`--region <cn|us|intl>`（默认 cn）、`--base-url`、`--output <text|json>`、`--non-interactive`（Agent/CI）、`--dry-run`、`--concurrent <n>` 等。子命令覆盖文本对话（`bl text chat`）、全模态（`bl omni`）、图像（`bl image generate/edit`）、视频（`bl video generate/edit/ref`）、视觉理解（`bl vision describe`）、语音合成（`bl speech synthesize`）等。

> **注意**：CLI 文档中示例默认模型（如 `qwen3.7-max`、`qwen3.5-omni-plus`、`qwen-image-2.0`、`happyhorse-1.0-t2v` 等）为工具内置默认值，可能随版本变化；实际可用模型请以模型列表 / 控制台为准。安全约束上，禁止将真实 API Key 写入仓库、日志、Skill 或聊天记录的可公开部分。

## 常见错误码与排查

调用过程中的报错多为 **400-InvalidParameter** 类的参数问题，可对照错误信息定位。完整清单见 [错误码](../../raw/model-api-reference/preparations/error-code.md)，以下为高频场景：

- **思考模式相关**：思考模式模型需 `enable_thinking=true` 时配合[流式输出](../concepts/streaming.md)，并设 `incremental_output=true`、`result_format="message"`；部分模型（如 `qwen3-235b-a22b-thinking-2507`）不允许将 `enable_thinking` 设为 `false`。
- **参数取值范围**：`temperature` ∈ [0.0, 2.0)、`top_p` ∈ (0.0, 1.0]、`top_k` ≥ 0、`presence_penalty` ∈ [-2.0, 2.0]、`n` ∈ [1, 4]；`max_tokens` 与输入长度上限以模型列表为准。
- **模型不存在（Model not exist）**：核对 `model` 名称大小写与空格，勿混用开源社区名与百炼模型 ID（用 `qwen3-235b-a22b-instruct-2507` 而非 `Qwen/Qwen3-235B-A22B-Instruct-2507`）。
- **content 类型错误**：纯文本模型的 `content` 必须为字符串，不能传数组或图片等多模态元素；需要图片输入请改用 Qwen-VL / Qwen3-VL 等多模态模型。
- **结构化输出**：使用 `response_format` 的 `json_object` 时，提示词须包含 `json` 关键词，且不能同时开启思考模式。
- **文件类（Qwen-Long）**：仅支持纯文本格式（TXT/DOCX/PDF/EPUB/MOBI/MD），单文件 < 150 MB、< 15000 页，file-id 数量 < 100。
- **账号状态（Arrearage）**：账号欠费会导致访问被拒绝，需在费用与成本页面充值后等待系统更新。

排障时可借助[阿里云 AI 助理](https://www.aliyun.com/ai-assistant/)，直接粘贴报错信息即可获得原因与解决方案。

## 来源文档

- [获取API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [使用百炼 CLI](../../raw/model-api-reference/preparations/use-model-studio-cli.md)



