# 插件

插件是百炼平台用于扩展大模型能力的核心机制，通过将外部工具（如 API、计算服务或生成服务）封装为标准化、可被大模型理解与自主调用的功能单元，弥补其在实时检索、精确计算、代码执行、多模态生成等场景下的固有局限。

## 在百炼平台的不同场景中，这个概念如何使用

插件在百炼平台中并非单一功能模块，而是贯穿三大应用范式的通用能力载体，使用方式因场景而异：

- **智能体（Agent）应用**：插件作为“工具”参与 LLM 的自主规划链路。在 Agent 2.0 中，插件与知识库、MCP 工具统一纳入工具空间，模型根据用户意图动态选择、参数化调用并整合结果；调用过程可追溯、可调试。官方插件（如 `calculator`、`quark_search`）开箱即用，自定义插件需先发布为 MCP 服务后绑定至智能体。

- **工作流（Workflow）应用**：插件以独立节点形式显式编排在画布中，执行顺序、输入来源、错误分支均由开发者确定，不依赖模型决策。适用于需强流程控制、确定性调度或组合多个插件的复杂业务逻辑（例如：先搜索 → 再解析 → 最后生成报告）。

- **API 集成（Assistant API / DashScope SDK）**：通过在请求的 `tools` 字段中声明插件 schema（支持 OpenAPI Spec 或 Function Calling 格式），由模型自动完成意图识别、参数抽取与调用编排。对含业务透传参数或用户级鉴权的插件，必须通过 `biz_params` 显式注入，不可依赖 Header 透传（仅 `Authorization` 头被保留）。

> ✅ 提示：插件能力当前仅在 `qwen-turbo`、`qwen-plus`、`qwen-max`、`qwen-vl-plus`、`qwen-vl-max` 等模型上可用；`qwen2` 系列部分模型已在控制台实测支持，建议以实际调用结果为准。

## 关键参数和配置

插件调用的可靠性与准确性高度依赖以下核心参数配置，尤其在自定义插件开发与集成时必须严格遵循：

- **工具 ID（`tool_id`）**：全局唯一字符串标识符（如 `text_to_image`），用于在请求中指定目标插件。可在控制台插件详情页点击悬浮图标一键复制。

- **输入参数（Input Parameters）**：
  - `传参方式`：必须明确设为 **大模型识别**（LLM 从用户语句中抽取）或 **业务透传**（由外部系统通过 `biz_params` 注入）；
  - `参数名称` 与 `参数描述`：需语义清晰、无歧义，直接影响 LLM 参数提取准确率；Object 类型子属性不可为空。

- **输出参数（Output Parameters）**：定义插件响应 JSON 中哪些字段将被 LLM 提取并用于生成最终回答；所有字段均为必填，缺失将导致结果截断或解析失败。

- **鉴权配置（仅自定义插件）**：
  - `Location`：支持 `Header` 或 `Query`；
  - `Type`：可选 `basic`（`Basic <token>`）、`bearer`（`Bearer <token>`）、`appcode`（`AppCode <token>`）；
  - `Token`：服务级固定凭据；用户级鉴权需通过 `biz_params` 动态传入。

- **其他约束**：
  - 单个智能体应用最多绑定 10 个插件；
  - 自定义插件 endpoint 必须可公网访问，响应需符合 JSON Schema 协议；
  - 所有插件调用均需主账号或具备权限的 RAM 用户授权服务关联角色 `AliyunServiceRoleForSFMAccessCloudAPI`。

## 面向开发者，简洁实用

- ✅ **快速验证**：优先使用控制台「插件市场」添加官方插件，无需配置即可测试调用效果。
- ✅ **自定义开发**：按 [自定义插件文档](../../raw/application-user-guide/plug-in/custom-plug-ins.md) 定义 URL、Schema 和鉴权，务必完成「在线测试 → 保存草稿 → 发布」三步，否则无法在应用中使用。
- ✅ **API 调用注意**：
  - 使用 `biz_params` 传递业务透传参数或用户级 [Token](token.md)；
  - 不要尝试设置自定义 Header（除 `Authorization` 外均被丢弃）；
  - 建议开启 `stream=True` + `incremental_output=True` 实现低延迟、可中断的流式响应。
- ⚠️ **避坑提醒**：
  - `code_interpreter` 禁止网络访问与文件上传，仅支持预装依赖（`pandas`, `matplotlib`, `requests` 等已内置）；
  - `quark_search` 和 `github_search` 仅返回摘要与链接，**不支持抓取网页正文或仓库详情页内容**；
  - RAM 子账号首次使用插件市场前，主账号须授予 `ram:CreateServiceLinkedRole` 权限，否则报错 `140052`。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [application support](../guides/application-support.md)
- [llm application](../guides/llm-application.md)
- [overview](../guides/overview.md)
- [skill](../guides/skill.md)


