# 配置与工具

阿里云百炼 CLI 鉴权配置、Profile 管理、模型市场、文件上传等通用工具命令速查。

在终端管理 CLI 鉴权配置、切换 Profile、浏览模型市场、上传文件以及使用其他通用工具。

> **重要**
>
> 任意命令追加 `--help` 可查看完整参数说明，例如 `bl config show --help`。全部接受文件 URL 的参数也接受本地路径——CLI 会自动上传到临时存储（有效期 48 小时），无需手动托管为 URL。全局参数可放在完整命令路径之前，例如 `bl --config token-plan auth status`；命令专属参数和凭证参数仍需放在命令路径之后。本文命令明细以 bl 2.8.0 为基准核实。

<a id="鉴权管理"></a>

## 鉴权管理

<a id="bl-auth-login"></a>

### bl auth login

使用 API Key、控制台浏览器登录或 OpenAPI AK/SK 进行认证（多种凭证可共存）。无需鉴权。

**语法**

<a id="code-block"></a>

```bash
bl auth login --api-key <key> | --console [--no-browser | --token-stdin --console-region <region>] | --open-api --access-key-id <id> --access-key-secret <secret>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--api-key <key>` | string | 否 | 要校验并保存的模型 API Key |
| `--base-url <url>` | string | 否 | 与 --api-key 一并校验并保存的模型 API Base URL |
| `--console` | switch | 否 | 通过浏览器登录（默认中国站；国际站使用 --console-site international）。需要时会创建普通 API Key；订阅计划必须使用 --api-key 登录 |
| `--no-browser` | switch | 否 | 与 --console 同用，只打印登录链接，不自动打开浏览器 |
| `--token-stdin` | switch | 否 | 与 --console 同用，从标准输入读取并校验一个控制台访问令牌；需要 --console-region，不拉起浏览器或本地服务 |
| `--console-region <region>` | string | 否 | 控制台网关地域，例如 cn-beijing、ap-southeast-1 |
| `--console-site <site>` | string | 否 | 控制台站点：domestic、international |
| `--open-api` | switch | 否 | 保存阿里云 OpenAPI AK/SK 凭证 |
| `--access-key-id <id>` | string | 否 | 要保存的阿里云 Access Key ID |
| `--access-key-secret <secret>` | string | 否 | 要保存的阿里云 Access Key Secret |

**示例**：通过浏览器登录并创建 API Key

<a id="code-block-2"></a>

```bash
bl auth login --console
```

-   无法拉起浏览器时，可使用 `bl auth login --console --no-browser` 打印登录链接，或通过 `--token-stdin` 从标准输入导入访问令牌。
-   OpenAPI AK/SK 按“命令参数 → `BAILIAN_ACCESS_KEY_ID` / `BAILIAN_ACCESS_KEY_SECRET` → 百炼配置 → `ALIBABA_CLOUD_ACCESS_KEY_ID` / `ALIBABA_CLOUD_ACCESS_KEY_SECRET`”的顺序整组解析，不跨来源拼接字段。STS 令牌使用同一来源的 `BAILIAN_SECURITY_TOKEN`、配置项 `security_token` 或 `ALIBABA_CLOUD_SECURITY_TOKEN`。
-   控制台业务命令不接受临时 AK/SK 参数。控制台令牌缺失或过期时，CLI 会用可用的 AK/SK 自动获取令牌；每个请求最多换取一次。

<a id="bl-auth-status"></a>

### bl auth status

显示当前认证状态。无需鉴权。

**语法**

<a id="code-block-3"></a>

```bash
bl auth status
```

该命令仅支持全局参数。

**示例**：以 JSON 输出当前认证状态

<a id="code-block-4"></a>

```bash
bl auth status --output json
```

<a id="bl-auth-logout"></a>

### bl auth logout

清除已保存的凭证；完整退出还会清除模型 Base URL。无需鉴权。

**语法**

<a id="code-block-5"></a>

```bash
bl auth logout [--console | --open-api] [--dry-run]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--console` | switch | 否 | 仅清除控制台 access\_token，保留 api\_key |
| `--open-api` | switch | 否 | 仅清除 OpenAPI AK/SK/STS 凭证，保留其他凭证 |

**示例**：仅清除控制台凭证

<a id="code-block-6"></a>

```bash
bl auth logout --console
```

<a id="bl-auth-generate-access-token"></a>

### bl auth generate-access-token

使用 OpenAPI AK/SK 生成 CLI Access Token。无需鉴权。

**语法**

<a id="code-block-7"></a>

```bash
bl auth generate-access-token --access-key-id <id> --access-key-secret <secret> --security-token <token>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--access-key-id <id>` | string | 是 | 阿里云 Access Key ID |
| `--access-key-secret <secret>` | string | 是 | 阿里云 Access Key Secret |
| `--security-token <token>` | string | 否 | 要保存的阿里云 STS Security Token（可选） |

**示例**：使用 AK/SK 生成 CLI 访问令牌

<a id="code-block-8"></a>

```bash
bl auth generate-access-token --access-key-id LTAIxxxxx --access-key-secret xxxxx --security-token <token>
```

<a id="配置管理"></a>

## 配置管理

<a id="bl-config-set"></a>

### bl config set

设置配置项。无需鉴权。

**语法**

<a id="code-block-9"></a>

```bash
bl config set --key <key> --value <value>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--key <key>` | string | 是 | 配置项名称（language、base\_url、output、output\_dir、timeout、watermark、api\_key、api\_key\_capabilities、access\_token、access\_key\_id、access\_key\_secret、security\_token、default\_\*\_model、workspace\_id） |
| `--value <value>` | string | 是 | 要设置的值 |

**示例**：设置语言为中文

<a id="code-block-10"></a>

```bash
bl config set --key language --value zh-CN
```

<a id="bl-config-show"></a>

### bl config show

显示当前配置。无需鉴权。

**语法**

<a id="code-block-11"></a>

```bash
bl config show
```

该命令仅支持全局参数。

**示例**：以 JSON 输出当前配置

<a id="code-block-12"></a>

```bash
bl config show --output json
```

-   展示 API Key 与 Base URL 的生效来源。请求使用的两者来自不同配置源时，会给出提示。

<a id="bl-config-list"></a>

### bl config list

列出配置 Profile 并显示当前激活项。无需鉴权。

**语法**

<a id="code-block-13"></a>

```bash
bl config list
```

该命令仅支持全局参数。

**示例**：以 JSON 输出配置概览

<a id="code-block-14"></a>

```bash
bl config list --output json
```

<a id="bl-config-use"></a>

### bl config use

设置当前激活的配置 Profile。无需鉴权。

**语法**

<a id="code-block-15"></a>

```bash
bl config use --name <name>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--name <name>` | string | 是 | 已有 Profile 名称，或 default |

**示例**：切换到指定配置文件

<a id="code-block-16"></a>

```bash
bl config use --name token-plan
```

<a id="bl-config-ui"></a>

### bl config ui

打开用于管理配置 Profile 的本地 Web UI。无需鉴权。

**语法**

<a id="code-block-17"></a>

```bash
bl config ui [--port <port>] [--no-open]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--port <port>` | number | 否 | 监听端口（默认：随机可用端口） |
| `--no-open` | switch | 否 | 不自动打开浏览器 |

**示例**：启动本地配置管理界面

<a id="code-block-18"></a>

```bash
bl config ui --port 8787
```

<a id="bl-config-agent"></a>

### bl config agent

配置编程 Agent 使用 DashScope API。无需鉴权。

**语法**

<a id="code-block-19"></a>

```bash
bl config agent --agent <name> (--base-url <url> | --region <region>) (--api-key <key> | --key <encoded>) --model <model>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--agent <name>` | string | 是 | 目标 Agent：claude-code, qwen-code, opencode, openclaw, hermes, codex, pi |
| `--base-url <url>` | string | 否 | API Base URL |
| `--region <region>` | string | 否 | 模型服务地域（例如 cn-beijing、ap-southeast-1）；将转换为 --base-url。仅用于 Token Plan |
| `--api-key <key>` | string | 否 | API Key |
| `--key <encoded>` | string | 否 | 来自 Web 控制台的混淆 API Key（以 "o1\_" 开头）；将解码为 --api-key |
| `--model <model>` | string | 是 | 默认模型名称 |
| `--context-window <tokens>` | number | 否 | 仅 OpenClaw：模型上下文窗口 Token 数（默认：256000） |
| `--wire-api <api>` | string | 否 | 仅 Codex：通信协议（默认：responses）。"chat" 仅适用于旧版 Codex <= 0.80.0 |

**示例**：配置 Agent 使用 DashScope API

<a id="code-block-20"></a>

```bash
bl config agent --agent claude-code --base-url https://dashscope.aliyuncs.com/apps/anthropic --api-key sk-xxxxx --model qwen3-max
```

<a id="输出与诊断"></a>

## 输出与诊断

默认输出格式为 text。使用 `--output json`、`DASHSCOPE_OUTPUT=json` 或在配置中设置 `output` 切换到 JSON。

-   JSON 模式在 stdout 返回完整业务结果。警告、诊断信息和错误以 JSONL 单独写入 stderr，便于脚本和 Agent 分别解析。
-   quiet 模式只隐藏进度和过程提示，保留完整结果、警告及错误。设置 `DASHSCOPE_QUIET=1` 可以开启 quiet。原先依赖 quiet 提取 ID、路径或回答的脚本，改为读取 JSON 字段。
-   `--introspect` 输出机器可读的命令结构（JSON）后退出，便于 Agent 发现命令和参数。
-   `bl alert`、`bl monitor` 和 `bl log` 的业务结果默认使用 JSON，即使 Profile 配置为 text。需要文本输出时显式传入 `--output text` 或设置 `DASHSCOPE_OUTPUT=text`。
-   交互式登录、本地配置 UI 和 Pipeline 事件流使用 text 输出。语音流式输出需要 JSON 时，通过 `--out` 指定保存文件。

<a id="通用工具"></a>

## 通用工具

<a id="bl-file-upload"></a>

### bl file upload

将本地文件上传到 DashScope 临时存储（保留 48 小时）。需要 API Key 鉴权。

**语法**

<a id="code-block-21"></a>

```bash
bl file upload --file <path> --model <model>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--file <path>` | string | 是 | 要上传的本地文件（图片、视频或音频） |
| `--model <model>` | string | 是 | 目标模型名称（文件将与该模型绑定） |

**示例**：上传图片文件并绑定模型

<a id="code-block-22"></a>

```bash
bl file upload --file photo.jpg --model qwen3-vl-plus
```

-   根据当前模型 Endpoint 选择上传服务。官方临时上传仅支持北京和新加坡地域；不支持的地域和 Token Plan 会明确报错。
-   显式指定自定义上传代理时，不再按 Key 类型提前拒绝。
-   本地文件上传到临时 OSS 时遵循 `--timeout`。

<a id="bl-model-list"></a>

### bl model list

浏览百炼模型市场中的模型系列，或查看模型详细信息。无需鉴权。

**语法**

<a id="code-block-23"></a>

```bash
bl model list [--model <model>] [--page <n>] [--page-size <n>] [--provider <p>] [--capability <c>] [--feature <f>] [--input-modality <m>] [--output-modality <m>] [--include-deprecated] [--enrich]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 否 | 显示指定模型系列的完整详情（切换到详情模式） |
| `--page <n>` | number | 否 | 页码（默认：1） |
| `--page-size <n>` | number | 否 | 每页结果数（默认：10） |
| `--provider <p>` | array | 否 | 按提供商筛选（可重复，例如 --provider alibaba --provider deepseek） |
| `--capability <c>` | array | 否 | 按能力代码筛选（TG、Reasoning、VU、IG、VG、TTS、ASR 等） |
| `--feature <f>` | array | 否 | 按特性筛选（function-calling、web-search、structured-outputs 等） |
| `--context-window <w>` | array | 否 | 按上下文窗口范围筛选 |
| `--input-modality <m>` | array | 否 | 限定输入模态（可重复：Text、Image、Video、Audio） |
| `--output-modality <m>` | array | 否 | 限定输出模态（可重复：Text、Image、Video、Audio） |
| `--include-deprecated` | switch | 否 | 包含已下线的模型（默认隐藏） |
| `--enrich` | switch | 否 | 同时获取主干模型的输入参数 Schema（predictConfig，仅详情模式） |

**示例**：筛选阿里云提供的模型

<a id="code-block-24"></a>

```bash
bl model list --provider alibaba
```

-   模型目录和 --enrich 使用的参数 Schema Endpoint 均为公开接口，无需登录控制台。
-   浏览模式会隐藏已下线的模型，可用 --include-deprecated 包含它们；详情模式（--model）始终列出全部版本并标注状态。

<a id="bl-model-search"></a>

### bl model search

按关键词搜索模型目录，按相关度排序。无需鉴权。

**语法**

<a id="code-block-25"></a>

```bash
bl model search --keyword <kw> [--limit <n>] [--provider <p>...] [--capability <c>...] [--feature <f>...] [--context-window <w>...] [--input-modality <m>...] [--output-modality <m>...] [--include-deprecated]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--keyword <kw>` | string | 是 | 与模型 ID、名称、能力、特性和描述匹配的关键词 |
| `--limit <n>` | number | 否 | 最大返回条数（默认：20） |
| `--provider <p>` | array | 否 | 按提供商筛选（可重复，例如 --provider alibaba --provider deepseek） |
| `--capability <c>` | array | 否 | 按能力代码筛选（TG、Reasoning、VU、IG、VG、TTS、ASR 等） |
| `--feature <f>` | array | 否 | 按特性筛选（function-calling、web-search、structured-outputs 等） |
| `--context-window <w>` | array | 否 | 按上下文窗口范围分桶筛选 |
| `--input-modality <m>` | array | 否 | 要求输入模态（Text、Image、Video、Audio） |
| `--output-modality <m>` | array | 否 | 要求输出模态（Text、Image、Video、Audio） |
| `--include-deprecated` | switch | 否 | 包含已下线模型 |

**示例**：搜索名称包含 qwen 的模型

<a id="code-block-26"></a>

```bash
bl model search --keyword qwen
```

-   搜索会扫描完整目录，但默认隐藏已下线模型；传入 --include-deprecated 可包含。
-   模型目录接口公开，无需控制台登录。

<a id="bl-model-code"></a>

### bl model code

输出可直接运行的 SDK 调用示例。无需鉴权。

**语法**

<a id="code-block-27"></a>

```bash
bl model code --model <model> [--sdk <sdk>] [--api <style>] [--lang <lang>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--model <model>` | string | 是 | 要生成示例的模型 |
| `--sdk <sdk>` | string | 否 | SDK 类型：openai（默认）或 dashscope |
| `--api <style>` | string | 否 | API 风格：completions（默认）或 responses |
| `--lang <lang>` | string | 否 | 代码片段语言（默认：python）；传入不支持的值可查看可用列表 |

**示例**：生成 qwen-max 的 Python 示例

<a id="code-block-28"></a>

```bash
bl model code --model qwen-max
```

**示例**：生成 qwen-max 的 curl 示例

<a id="code-block-29"></a>

```bash
bl model code --model qwen-max --lang curl
```

-   文本输出只包含代码片段，可直接重定向到文件；使用 --output json 可同时获取元数据。
-   示例 Base URL 包含 `[workspace-id]` 占位符，需替换为实际 Workspace ID，或设置 BAILIAN\_WORKSPACE\_ID 后使用 DashScope Endpoint。
-   可用组合由模型决定；传入不支持的值可查看该模型的可用列表。

<a id="bl-advisor-recommend"></a>

### bl advisor recommend

为你的使用场景推荐最佳模型（意图分析 → 候选召回 → LLM 排序）。需要 API Key 鉴权。

**语法**

<a id="code-block-30"></a>

```bash
bl advisor recommend --message <text> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--message <text>` | string | 是 | 描述你的需求 |
| `--top <n>` | number | 否 | 推荐数量（默认：3） |
| `--model <model>` | string | 否 | 用于全部阶段的 LLM：Agent、意图分析、评分和解释（默认：qwen-flash-2025-07-28） |
| `--no-agent` | switch | 否 | 跳过 Agent 循环，直接运行确定性推荐引擎 |
| `--trace` | switch | 否 | 把完整的路由和性能追踪写入 stderr |
| `--think` | switch | 否 | 把引擎决策过程写入 stderr |
| `--no-thinking` | switch | 否 | 已弃用的兼容参数，不产生效果；推荐调用始终关闭思考模式 |

**示例**：根据需求预览模型推荐结果

<a id="code-block-31"></a>

```bash
bl advisor recommend --message "我需要一个能够理解图片的聊天机器人"
```

**示例**：跳过 Agent 澄清，直接运行推荐引擎

<a id="code-block-32"></a>

```bash
bl advisor recommend --message "搭建数字人直播" --no-agent
```

-   推荐流程为意图分析 → 路由 → 候选召回 → 评分 → 排序。交互式终端中支持 Agent 澄清和多步骤推荐，推荐结果保留原有 JSON 主结构。
-   `--trace` 和 `--think` 只写入 stderr，不改变 stdout 的推荐结果。

<a id="bl-pipeline-run"></a>

### bl pipeline run

运行 Pipeline 工作流定义。无需鉴权。

**语法**

<a id="code-block-33"></a>

```bash
bl pipeline run --file <path> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--file <path>` | string | 是 | Pipeline 定义文件（YAML/JSON） |
| `--input <json>` | string | 否 | 内联 JSON 格式的运行时输入 |
| `--input-file <path>` | string | 否 | 来自 JSON 文件的运行时输入 |
| `--concurrency <n>` | number | 否 | 最大并行步骤数（默认：1） |
| `--events <format>` | string | 否 | 输出生命周期事件：jsonl |
| `--step-timeout <seconds>` | number | 否 | 默认步骤超时时间，单位为秒 |

**示例**：运行指定工作流定义并传入输入参数

<a id="code-block-34"></a>

```bash
bl pipeline run --file workflow.yaml --input '{"brief":"你好"}'
```

-   `--events jsonl` 使用 text 输出模式，Pipeline 事件流与其他输出格式不能混用。

<a id="bl-pipeline-validate"></a>

### bl pipeline validate

验证 Pipeline 定义但不执行。无需鉴权。

**语法**

<a id="code-block-35"></a>

```bash
bl pipeline validate --file <path>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--file <path>` | string | 是 | Pipeline 定义文件（YAML/JSON） |

**示例**：预览工作流定义验证结果

<a id="code-block-36"></a>

```bash
bl pipeline validate --file workflow.yaml
```

<a id="bl-plugin-install"></a>

### bl plugin install

安装或升级白名单内的 Command Pack。无需鉴权。

**语法**

<a id="code-block-37"></a>

```bash
bl plugin install --package <name[@version]>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--package <name[@version]>` | string | 是 | 白名单内的 Command Pack 包名，以及可选的版本或 Tag |

**示例**：安装指定 Command Pack 包

<a id="code-block-38"></a>

```bash
bl plugin install --package @ali/bailian-plugin-agent
```

<a id="bl-plugin-list"></a>

### bl plugin list

列出已安装的 Command Pack 及其加载状态。无需鉴权。

**语法**

<a id="code-block-39"></a>

```bash
bl plugin list
```

该命令仅支持全局参数。

**示例**：输出已安装插件的 JSON 列表

<a id="code-block-40"></a>

```bash
bl plugin list --output json
```

<a id="bl-plugin-remove"></a>

### bl plugin remove

移除已安装的 Command Pack。无需鉴权。

**语法**

<a id="code-block-41"></a>

```bash
bl plugin remove --name <package>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--name <package>` | string | 是 | 白名单内的 Command Pack 包名 |

**示例**：移除指定 Command Pack 插件

<a id="code-block-42"></a>

```bash
bl plugin remove --name @ali/bailian-plugin-agent
```

<a id="bl-plugin-link"></a>

### bl plugin link

链接白名单内的本地 Command Pack 用于开发。无需鉴权。

**语法**

<a id="code-block-43"></a>

```bash
bl plugin link --path <directory>
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--path <directory>` | string | 是 | 本地 Command Pack 包目录 |

**示例**：链接本地 Command Pack 用于开发

<a id="code-block-44"></a>

```bash
bl plugin link --path ../bailian-plugin-agent
```

<a id="bl-workspace-init"></a>

### bl workspace init

初始化百炼 Workspace 并开通后付费服务。无需鉴权。

**语法**

<a id="code-block-45"></a>

```bash
bl workspace init --access-key-id <id> --access-key-secret <secret> [--security-token <token>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--access-key-id <id>` | string | 否 | 阿里云 Access Key ID |
| `--access-key-secret <secret>` | string | 否 | 阿里云 Access Key Secret |
| `--security-token <token>` | string | 否 | 阿里云 STS Security Token（可选） |

**示例**：使用密钥初始化百炼 Workspace

<a id="code-block-46"></a>

```bash
bl workspace init --access-key-id LTAIxxxxx --access-key-secret xxxxx
```

<a id="bl-workspace-list"></a>

### bl workspace list

列出全部 Workspace。

**语法**

<a id="code-block-47"></a>

```bash
bl workspace list [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--list <n>` | string | 否 | 限制结果数量 |

**示例**：预览前 5 个 Workspace 列表

<a id="code-block-48"></a>

```bash
bl workspace list --list 5
```

<a id="bl-console-call"></a>

### bl console call

通过 CLI Gateway 调用百炼控制台 API。

**语法**

<a id="code-block-49"></a>

```bash
bl console call --api <api> --data <json> [flags]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--api <api>` | string | 是 | API 名称（例如 zeldaEasy.broadscope-bailian.memory-library.getLibraries） |
| `--data <json>` | string | 是 | JSON 字符串格式的请求数据 |

**示例**：调用百炼控制台 API 并传入请求数据

<a id="code-block-50"></a>

```bash
bl console call --api zeldaEasy.bailian-commerce.freeTrial.queryFreeTierQuota --data '{"queryFreeTierQuotaRequest":{"models":["qwen3-max"]}}'
```

<a id="bl-update"></a>

### bl update

将 CLI 更新到最新版本或指定版本。无需鉴权。

**语法**

<a id="code-block-51"></a>

```bash
bl update [--to <version>]
```

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `--to <version>` | string | 否 | 安装指定版本，而不是最新版本 |

**示例**：确认执行 CLI 版本更新到 0.1.14

<a id="code-block-52"></a>

```bash
bl update --to 0.1.14
```

-   升级失败或无法获取最新版本时返回非零退出码，便于脚本和 Agent 检测失败。

运行 `bl --help` 可查看全部命令分组。
