# 更新日志

阿里云百炼 CLI 的版本更新记录

## 2.10.4 | 2026-11-20

-   新增 `bl finetune rl` 命令组，覆盖百炼强化学习训练的端到端链路：`authorize` 检查准入白名单、服务关联角色与业务开通状态，绝不自动创建角色，缺失时中止并给出双语手动授权指引；`run` 通过 flag 或 YAML 规格提交训练任务并打包 Rollout/Reward 函数代码，在托管 OS 沙箱 Python 运行时内执行（仅 macOS/Linux），创建任务消耗计费的 MTU 算力；`get` / `list` / `watch` / `logs` / `cancel` / `delete` 经共享 fine-tunes 后端管理任务。
-   新增 `bl finetune opd` 命令组，使用平台登记的教师模型进行纯模型在线蒸馏：支持 `authorize` / `run` / `params` / `get` / `watch` / `logs` / `cancel` / `delete`，`run` 可用 `--dry-run` 预览任务规格，`params` 查询学生基座模型支持的超参数。
-   新增 `bl finetune runtime prepare` / `doctor` / `clean` 命令，管理 RL/OPD 沙箱运行时：`prepare` 按多源清单下载固定版本 CPython + dashscope 运行时并逐源 SHA256 校验；`doctor` 验证沙箱隔离并探测宿主出站网络可达性；`clean` 回收孤儿任务目录与旧版本运行时。
-   新增沙箱网络拒绝提示：连接级网络拒绝（`EPERM` / `EACCES` / `ENETUNREACH` / `EHOSTUNREACH`）给出双语提示，说明执行环境可能阻断出站网络，并引导放行网络、改在普通终端执行或设置 `HTTPS_PROXY`。
-   变更代理环境变量：大写变量未设置时，小写 `http_proxy` / `https_proxy` / `no_proxy` 作为兜底生效，大写仍优先。

## 2.10.3 | 2026-11-18

-   修复 `bl workspace list` 现在返回全部可访问的业务空间，不再只返回网关默认的第一页（10 个）。遥测、告警、日志、数据集、文件与部署命令使用的控制台工作空间解析同样覆盖第一页之外的空间。

## 2.10.2 | 2026-11-17

-   变更 `bl monitor delivery enable` 与 `bl log audit/inference enable` 不再自动创建服务关联角色，改为检查角色状态，缺失时以双语指引中止并指向模型可观测文档，避免静默授予跨服务权限。

## 2.10.1 | 2026-11-13

-   修复 `--output` 仅接受 `text` 或 `json`，其他取值会在命令执行前被拒绝。
-   修复 `bl usage free` 与 `bl usage freetier` 在针对全部模型、且尚未解析出模型列表时，试运行结果会标明范围为全部模型且尚未解析，避免被当成已经确定的模型集合。
-   修复 API Key 登录密钥校验改为遵循已配置的请求超时，不再在固定的短时限处中断。

## 2.10.0 | 2026-11-13

-   新增 `bl flow-agent` 命令组，通过控制台网关管理百炼应用。`bl flow-agent create` / `get` / `update` / `publish` / `delete` / `copy` / `versions` 管理智能体与工作流；`delete` 为高风险操作，需 `--yes`。`bl flow-agent workflow get` / `save` / `publish` / `export` 管理工作流画布；`save` 整幅替换草稿并带乐观锁版本，`publish` 按控制台编辑器逻辑规范化触发器。
-   智能体配置更新先读取当前草稿，再合并 `--model` / `--instructions` / `--config-json` / `--config-file`。
-   `bl flow-agent list --type workflow` 按控制台排除法列出工作流。
-   `bl app call` / `bl app list` 已废弃，请改用 `bl flow-agent call` / `bl flow-agent list`，将在未来版本移除。

## 2.9.0 | 2026-11-12

-   新增应用控制面命令：通过控制台网关在命令行管理百炼应用。`bl app create` / `get` / `update` / `publish` / `delete` / `copy` / `versions` 管理智能体与工作流；`delete` 为高风险操作，需 `--yes`。`bl app workflow get` / `save` / `publish` / `export` 管理工作流画布。
-   新增 `bl app list --type workflow`，按控制台排除法列出工作流。
-   `bl omni` 默认模型改为 `qwen3.8-omni-flash`（原 `qwen3.5-omni-plus`）。
-   修复免费额度模型操作的确认闸门与错误处理；恢复操作保持在确认闸门之后。
-   修复 API Key 回退后保留显式 `--config` 配置 profile，并为命名 profile 追加 `--config` 提示。

## 2.8.6 | 2026-11-12

-   新增 `bl dataset groups`，支持分页和名称筛选；新增 `bl dataset version`，通过 `--dataset-group-id` 列出组内版本，或通过 `--dataset-id` 查询单版本详情，可选 `--include-status` 补充状态。
-   新增 `bl file url --file-key`，将 Console 文件键解析为下载 URL，不自动下载文件。
-   新增 `bl deploy instances`，支持分页、关键词和模型服务 ID 筛选。
-   修复 Console 响应处理：正确解析嵌套成功与失败响应，保留服务端错误消息、错误码及请求 ID，避免将有效工作空间列表误判为空。
-   修复工作空间参数校验：拒绝显式传入空白 `--workspace-id`，避免静默回退到其他已配置工作空间。

## 2.8.5 | 2026-11-10

-   修复精调任务创建时上传前查询权威超参配置，只校验用户显式覆盖且有明确约束的参数；查询或校验失败时不上传数据、不提交任务，未指定参数不再由本地填充或裁剪。
-   修复部署删除时显式部署计划优先于残留的 PTU 特征字段；无法可靠判断计划类型时拒绝提交删除请求。
-   修复 `bl text chat` 支持 `--enable-thinking=false`，同时保持省略参数和裸参数的原有行为；关闭思考时不再发送 `thinking_budget`。
-   修复模型调用示例仅返回精确匹配型号的示例代码，不再回退到同系列其他型号。
-   修复数据集上传帮助中不受支持的 `evaluation` purpose 示例已删除，默认值仍为 `fine-tune`。

## 2.8.4 | 2026-11-06

-   新增 `bl finetune params`，查询基础模型的训练超参配置，支持 `--training-type`、`--param-type`、`--mtu-spec-code` 筛选及 `--modality` / `--reasoning-mode` 动态训练选项。
-   新增 `bl finetune metrics`，查询微调任务的训练指标，支持 `--page` / `--page-size` 显式分页。

## 2.8.3 | 2026-11-06

-   `bl search web` 新增模型搜索模式（`--mode model`），并改为默认实现：通过 Chat Completions 的 `enable_search` 由模型联网作答；`--mode mcp` 仍调用 DashScope MCP WebSearch 服务。
-   `bl text chat` 新增 `--enable-search`，支持模型内置联网搜索；qwen3.8-max 默认开启，可用 `--enable-search false` 关闭。
-   Profile 可按搜索模式（`model` / `mcp`）声明凭证，切换搜索模式时自动选择对应 Profile 凭证。

## 2.8.2 | 2026-11-04

-   内部维护：完善 CLI 使用统计。

## 2.8.1 | 2026-11-04

-   新增 Linux ARM64 二进制安装包（glibc），支持独立安装和二进制更新。
-   修复异步并发图片生成和编辑任务未完整保留图片结果的问题，兼容不同任务使用不同响应格式的情况。
-   修复 Chat Completions 提前断流被误判为成功的问题；结构化输出保留完整 `tool_calls` 并返回 `finish_reason`。
-   避免待发送的遥测请求拖延 CLI 退出，并在遥测初始化失败时保留已排队事件。

## 2.8.0 | 2026-11-03

-   支持通过 `aliyun bl` 调用，帮助、示例、操作指引和结构化命令适配对应入口。
-   新增 AK/SK 鉴权：支持 `BAILIAN_ACCESS_KEY_ID`、`BAILIAN_ACCESS_KEY_SECRET` 和可选的 `BAILIAN_SECURITY_TOKEN`。控制台令牌缺失或过期时，可通过 AK/SK 自动获取。
-   新增 `bl cmodel base-models/import/get/list/watch/delete`，支持从 OSS 导入自定义模型、查询可导入基础模型、跟踪导入任务，以及查询或删除已导入模型。导入 API 当前仅在北京地域开放。
-   JSON 模式返回完整业务结果，警告、诊断和错误以 JSONL 单独写入 stderr。
-   quiet 模式只隐藏进度和过程提示，保留完整结果、警告及错误；支持 `DASHSCOPE_QUIET=1`。原先依赖 quiet 提取 ID、路径或回答的脚本，需改为读取 JSON 字段。
-   AK/SK 按“命令参数 → 百炼环境变量 → 百炼配置 → 阿里云环境变量”解析。
-   模型推荐关闭思考模式，`--no-thinking` 保持兼容。
-   交互式登录、本地 UI、Pipeline 事件流和语音流式输出明确各自支持的格式：原生交互模式与 Pipeline JSONL 事件使用 text 输出，语音流式 JSON 输出需指定 `--out`。
-   修复语音识别 JSON 输出未保留完整响应和转写结果的问题；空转写结果仍返回任务信息。
-   quiet 和 JSON 模式保留 Managed Agent SDK 警告。
-   使用缓存结果时仍能显示可升级通知。
-   避免重复错误信息，完善模型推荐和精调费用查询的请求诊断。

## 2.7.2 | 2026-10-30

-   `bl image generate`、`bl image edit`、`bl video generate`、`bl speech synthesize` 和 `bl speech recognize` 新增 `--model auto`，通过百炼自研 MCP 实现 AIGC 模型自动路由。
-   自研 SSE MCP 客户端替换为官方 MCP SDK。

## 2.7.1 | 2026-10-29

-   `bl usage token-plan` 支持展示接口返回的全部配额窗口；JSON 输出新增 `hasQuotaData`，用于区分无配额数据与正常结果。

## 2.7.0 | 2026-10-29

-   新增 `bl parsex parse submit/result`，支持文档及音视频解析、结果查询和 Markdown 输出。
-   新增 `bl parsex extract submit/result`，支持按 JSON Schema 从文档或已有解析结果中抽取字段，并返回原文引用。
-   `bl config show` 展示 API Key 与 Base URL 的生效来源，两者来自不同配置源时给出提示。
-   修复 `bl auth login` 在 MaaS Endpoint 上拒绝有效工作空间 API Key 的问题。
-   API Key 校验保留服务端及网络错误，不再把全部失败统一报告为 Key 无效。

## 2.6.2 | 2026-10-28

-   `bl alert`、`bl monitor` 和 `bl log` 的业务结果统一默认 JSON，即使 Profile 配置为 text。依赖文本输出的脚本需显式传入 `--output text` 或设置 `DASHSCOPE_OUTPUT=text`。
-   遥测命令根据选定空间自动解析控制台身份，预检、业务请求、异步轮询及后续请求使用同一身份，修复 `--workspace-id` 过滤失效及跨空间结果异常。
-   审计日志规范化时间、模型、请求 ID、工作空间及用量字段，修复缺失字段、NaN 时间及异常计数展示，并拒绝空间不匹配的审计结果。
-   `log audit count` 和 `log inference count` 使用对应列表接口的 `totalCount`，修复列表非空而计数为 0 的问题。
-   推理计数保留多模型、多 API Key 过滤，去重后按单值组合查询并汇总；支持异步轮询，仅全部成功后输出。
-   dry-run 展示工作空间身份解析计划和实际计数请求组合，不发送业务请求。

## 2.6.1 | 2026-10-28

-   新增 `bl batch convert/create/list/get/cancel/download`，支持 CSV 转 JSONL、创建 Chat 或 Embedding 批量任务、跟踪进度、取消任务及下载结果和错误文件，可选导出 CSV。
-   `bl text chat --batch` 支持单次非流式请求，与异步文件批量任务分开使用，支持 60–3600 秒请求超时。
-   `bl advisor recommend` 新增 `--top`、`--model`、`--no-agent`、`--trace`、`--think` 和 `--no-thinking`。
-   模型推荐升级意图分析、路由、候选召回、评分及排序流程；交互终端支持 Agent 澄清与多步骤推荐，推荐结果保留原有 JSON 主结构。
-   移除旧的推荐流程库接口（BREAKING），包括 `getModels`、`recallCandidates`、`recallSemantic` 和 `rankModels`。库调用方需适配新的推荐引擎；旧类型通过 `LegacyIntentProfile`、`LegacyModelProfile` 和 `LegacyRecommendResult` 导出。
-   临时文件上传根据当前模型 Endpoint 选择上传服务，修复新加坡地域及 Prime 视频上传误用北京地址的问题；官方临时上传仅支持北京和新加坡，不支持的地域及 Token Plan 明确报错。
-   修复 Node.js 26 下 fetch 与 dispatcher 不兼容及代理初始化问题。
-   正确识别嵌套业务错误，保留非 JSON 错误正文及请求 ID，避免把错误响应当作成功结果。

## 2.6.0 | 2026-10-27

-   新增 `bl knowledge init`，串联样例上传、建库、检索服务创建及首次检索验证，支持恢复和资源复用。
-   新增 `bl knowledge doc sync` 和 `bl knowledge doc import`，支持同步本地目录及导入已有文件。
-   支持音视频知识库、解析配置、流式上传、纯图片检索及在线检索过滤配置。
-   新增 `--introspect` 结构化命令说明和 `bailian-knowledge` Skill；Knowledge Studio CLI 同步提供对应能力。
-   知识库问答的结构化输出区分最终答案、阶段、工具、来源和用量；quiet 模式只输出最终答案。
-   建库提示补充计费说明、资源记录与清理指引。
-   拒绝知识库命令中的空白必填参数。
-   切片批量删除失败时，明确报告已完成批次、结果未确认批次及未执行部分。

## 2.5.1 | 2026-10-23

-   控制台登录支持 `--no-browser` 手动打开登录地址，以及 `--token-stdin` 从标准输入导入并校验控制台凭证。
-   支持声明 Agent 来源、Skill 名称和版本；未声明来源记为未知。
-   修复浏览器快速回调时的登录完成判定；未收到凭证时明确报告超时。
-   修复控制台凭证刷新的地域选择，刷新后验证请求成功再保存凭证。

## 2.5.0 | 2026-10-20

新增 Memory 管理命令：

-   `bl memory node show`：查看单个记忆节点详情
-   `bl memory skill export`：导出技能记忆节点
-   `bl memory profile list` / `show` / `update` / `delete`：列出、查看、更新和删除画像模板

`bl memory search` 支持按多个记忆片段规则召回（`--project-ids`），并可通过 `--plan-version` 选择 pro 或 lite 策略；`bl memory add` 和 `bl memory update` 支持技能记忆元数据；`bl memory add` 支持仅抽取用户画像（`--extract-mode profile_only`）。

Memory 命令的不兼容变更：

-   Memory 命令改用业务空间专属端点，需通过 `--workspace-id`、环境变量 `BAILIAN_WORKSPACE_ID` 或配置项 `workspace_id` 提供业务空间 ID。
-   支持记忆库参数的命令将 `--memory-library-id` 改为 `--library-id`。
-   `bl memory update` 和 `bl memory delete` 移除 `--user-id`；删除记忆节点需传入 `--yes` 确认。
-   `bl memory add` 改为提交异步抽取任务，默认最多等待 120 秒，`--wait 0` 只提交不等待；JSON 输出需改为读取 `event_id` 和 `events`，提交回执不代表抽取完成。

修复 `bl memory add` 的完成判定：空事件列表或缺少事件 ID 时不再误报完成，部分任务失败时返回非零退出码。

使用方法见 [Memory](raw/cli/capabilities/agent-infrastructure/memory.md)。

## 2.4.0 | 2026-10-19

-   Managed Agent 新增 Memory Store、记忆内容和历史版本管理，并可将记忆挂载到 Session。
-   新增工作空间级 Webhook 管理：创建、更新、启停、测试、重置签名密钥和查询投递事件。
-   创建 Agent 时可通过 `--environment`、`--vault` 和 `--mcp` 绑定默认 Environment、Vault 及 MCP 市场服务。
-   创建 Session、运行 Session 和创建 Deployment 时可重复传入 `--environment_variables KEY=VALUE`。

## 2.3.3 | 2026-10-19

-   修复二进制 CLI 的模型 API 请求失败问题，包括语音和视频生成。
-   修复核心 API 长请求提前超时的问题；补充流式响应空闲保护，并在流结束时释放连接。
-   修复 Windows 打开浏览器时控制台登录链接的查询参数丢失问题。
-   控制台登录后或执行 `bl auth status` 时，若未配置模型 API Key，会提示模型调用仍需配置 Key。

## 2.3.2 | 2026-10-16

-   `bl update` 在升级失败或无法获取最新版本时返回非零退出码，便于脚本和 Agent 识别失败。

## 2.3.1 | 2026-10-16

-   设置超过 300 秒的请求超时后，不再被默认的响应头超时提前中断。

## 2.3.0 | 2026-10-14

-   新增 Pi 支持：`bl config agent` 和 `bl mcp connect` / `bl mcp disconnect` 支持 `--agent pi`。
-   支持在完整命令路径前使用全局参数，例如 `bl --config token-plan auth status`；命令专属参数和鉴权参数需放在路径后。
-   帮助和版本查询会校验已传入的参数；未知参数、缺少参数值或参数值非法时返回用法错误退出码 2，解析错误提示跟随 Profile 语言。
-   本地文件上传到临时 OSS 时，`--timeout` 可设置传输超时。

## 2.2.2 | 2026-10-14

-   新增 `bl finetune compress templates/create/list/get/watch/logs/cancel/delete`，支持全参微调模型的量化压缩，包含 dry-run 预览、状态轮询、日志查询和安全删除确认。
-   `bl config agent` 与 `bl mcp connect` / `bl mcp disconnect` 新增支持 Pi，写入其原生配置并保留已有设置。
-   全局参数既可放在命令之后，也可放在命令之前；两种写法都只对本次调用选择 Profile，不修改 `active_config`。
-   新增 `bl decision`，通过工作空间专属 Endpoint 调用 TypeSafe System One，支持 `choice` / `noul` / `score` 校验、JSON 与文本输出、复用训练样本、北京/新加坡地域路由及 dry-run 预览。
-   只接受命令已定义的参数；未知参数、缺少参数值或参数值非法时返回用法错误退出码 2。
-   本地文件上传到临时 OSS 时遵循 `--timeout`，不再固定为 120 秒。

## 2.2.1 | 2026-10-12

-   `bl config agent --agent hermes` 改为写入 Hermes 实际读取的位置：`$HERMES_HOME/config.yaml`，或平台原生默认路径（Windows 为 `%LOCALAPPDATA%\hermes`，其他平台为 `~/.hermes`）。

## 2.2.0 | 2026-10-12

-   `bl usage token-plan` 只展示月度额度（使用百分比与重置时间），不再显示 5 小时和 1 周窗口。

## 2.1.0 | 2026-09-28

`bl finetune text create` 新增任务名、优先级、LoRA、评估、Checkpoint 保存、数据集切分与数据增强等高级参数；`bl finetune get` 返回更完整的任务元数据与超参数。

修复 Windows 下 Skill 安装：兼容传统路径长度限制，运行中的 Agent 占用目录时原地更新已安装的 Skill。

## 2.0.1 | 2026-09-22

新增吞吐预留容量管理：

-   `bl deploy capacity list`：列出吞吐预留容量实例
-   `bl deploy capacity get`：查看指定容量实例详情
-   `bl deploy capacity create`：为 ModelCode 购买额外容量实例
-   `bl deploy capacity scale`：调整单个预留实例的绝对容量
-   `bl deploy capacity renew`：续费预付费容量实例，可同时变更容量
-   `bl deploy capacity delete`：释放容量实例，不删除其 ModelCode
-   `bl deploy capacity unsubscribe`：生成预付费容量实例的退订链接，跳转计费控制台
-   `bl deploy overflow`：设置吞吐预留 ModelCode 的溢出策略
-   `bl deploy operation get`：查询一次容量操作的状态
-   `bl deploy operation wait`：等待容量操作完成并刷新确认后的容量

`bl text chat` 与 `bl video generate` 新增 `--prime`，以 Prime 模式通过工作空间专用端点调用，可用 `--workspace-id` 指定工作空间。

## 2.0.0 | 2026-09-22

新增 MCP 原生注册命令：

-   `bl mcp connect`：把百炼 MCP 服务注册进 Agent 原生配置，支持 streamable-http 与 SSE，可指定单个 Agent 或 `--agent all`（Codex、Claude Code、Cursor、Qoder、Qwen Code、Gemini、OpenCode 等）；不覆盖非 CLI 管理的同名配置
-   `bl mcp disconnect`：移除 CLI 注册的 MCP 配置，已被修改的注册项会保留并按冲突报告

Skill 安装与更新扩展到 WorkBuddy、Trae CLI 与 DeepSeek DSH，`bl skill init`、`bl skill add`、`bl skill update`、`bl skill remove` 支持 `--dry-run` 预览。

## 1.28.0 | 2026-09-20

新增 Agent 安全命令：`bl agents security overview` 查看最近 24 小时的防护总览，`bl agents security alerts` 查看告警列表，支持按风险等级、资产类型、状态等筛选。

## 1.27.0 | 2026-09-18

新增 `bl monitor`、`bl log`、`bl alert` 命令组，支持查看模型调用量、Token 用量、调用日志与配置告警；新增 `bl model search` 按相关度搜索模型目录，`bl model code` 获取 SDK 调用示例代码。

## 1.26.0 | 2026-09-17

简化认证方式：默认推荐控制台登录，需要时可自动创建普通 API Key；API Key 保存前自动校验并自动选择可用地域。已有普通 API Key 和 Token Plan 订阅 Key 统一使用 `bl auth login --api-key` 登录。

## 1.25.0 | 2026-09-14

新增 Token Plan harness 权益额度查询（`bl token-plan harness-quota`）。

## 1.24.0 | 2026-09-11

新增 Sandbox 沙箱实例与模版生命周期命令。

## 1.23.0 | 2026-09-10

语音识别支持即时热词（`--vocabulary`）与上下文增强（`--context`），新增语音热词表管理命令。

## 1.22.0 | 2026-09-08

Managed Agent 项目 Build / Publish 流程调整：`project init` 默认在 `./managed-agent` 子目录初始化，`project build` 无需确认，Publish 仍需显式确认。

## 1.21.0 | 2026-09-07

Managed Agent 支持本地目录项目、项目版本管理与 Workbench。

## 1.20.0 | 2026-09-03

Managed Agent 新增 AgentStudio 资源操作命令（Agent、Environment、Skill、Vault、Deployment、Session、File）。

## 1.19.0 | 2026-09-01

高风险操作新增确认机制：未加 `--yes` 时阻断执行（退出码 7），`--dry-run` 可预览。

## 1.18.0 | 2026-08-27

支持 Profile API Key 自动回退；视频生成默认模型升级至 Wan3.0。

## 1.17.0 | 2026-08-18

Managed Agent 支持原生 Deployment；CLI 支持中英文界面切换。

## 1.16.0 | 2026-08-17

新增知识库全生命周期管理命令。

## 1.15.0 | 2026-08-14

新增订阅套餐用量视图（`bl usage token-plan`、`bl usage coding-plan`）。

## 1.14.0 | 2026-08-04

支持免 Node.js 的二进制安装与指定版本更新。

遇到问题或有新想法，欢迎去 [GitHub](https://github.com/modelstudioai/cli/issues) 提交 Issue。阿里云百炼 CLI 的功能更新、优化和问题修复完整记录见 [**CHANGELOG.zh.md**](https://github.com/modelstudioai/cli/blob/main/CHANGELOG.zh.md)。
