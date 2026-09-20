# 插件机制

插件机制是百炼平台用于扩展大模型能力的核心架构设计，通过将外部工具（如 API、计算服务、搜索接口等）封装为标准化、可被大模型语义理解与自主规划调用的工具单元，弥补模型在实时信息获取、精确计算、代码执行、多模态生成等方面的固有局限。它不是对模型能力的替代，而是以“能力即服务”（Capability-as-a-Service）方式实现安全、可控、低侵入的能力增强。

## 在百炼平台的不同场景中如何使用

插件机制在三大核心应用范式中统一支持，但集成方式与控制粒度不同：

- **智能体应用（Agent）**：插件作为“工具”参与模型自主规划链路。模型根据用户问题和 `plugin_description` / `tool_description` 的语义匹配，自动决定是否调用、调用哪个插件及传入哪些参数。适用于需动态决策的开放域任务（如“用夸克搜索最近的AI会议，并用代码解释器整理成表格”）。新版 Agent 2.0 将插件、知识库、MCP 服务统一纳入工具空间，支持完整展示“规划-执行-反思”过程。

- **工作流应用（Workflow）**：插件以独立节点形式拖入画布，由开发者显式编排调用时机、输入来源（可来自前置节点输出）和错误处理逻辑。不依赖模型自动触发，适合确定性流程（如“先调用 GitHub 搜索 → 提取仓库 URL → 再调用 text_to_image 生成项目架构图”）。每个插件节点仅绑定一个工具，支持参数硬编码或变量透传。

- **API 调用（Assistant API / DashScope SDK）**：通过 `tools` 字段在请求体中声明可用插件列表（含 `tool_id` 和参数 schema），平台在推理过程中自动完成工具选择、参数提取、调用与结果注入。适用于集成到自有系统或第三方客户端的场景；若涉及业务级鉴权（如用户 token），需通过 `biz_params` 字段透传。

> ✅ 注意：官方插件（如 `code_interpreter`, `quark_search`）仅能与**同业务空间**内的智能体/工作流关联；子业务空间首次使用需完成插件授权操作。

## 关键参数和配置

插件机制的配置分为两个层级，均需在控制台插件管理页完成定义与发布：

### 插件级参数（Plugin-level）
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `plugin_url` | string | 是 | 插件根域名（如 `https://api.example.com`），所有工具路径以此为基础拼接 |
| `is_auth_required` | boolean | 否（默认 `false`） | 是否启用鉴权；若为 `true`，需进一步配置 `auth_type`（`header` 或 `query`）、`auth_key`（如 `Authorization`）、`auth_value`（支持 KMS 加密凭证） |
| `plugin_description` | string | 是 | 自然语言描述（建议含典型使用场景和限制），直接影响模型是否识别并触发该插件 |

### 工具级参数（Tool-level，每个插件可含多个工具）
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `tool_name` | string | 是 | 工具唯一标识（如 `search_web`），全小写+下划线，不可重复 |
| `tool_description` | string | 是 | 功能说明，**必须含自然语言示例**（如：“搜索网页摘要，例如：搜索‘量子计算最新进展’”），质量直接决定召回准确率 |
| `tool_path` | string | 是 | 以 `/` 开头的相对路径（如 `/v1/search`），拼接 `plugin_url` 构成完整调用地址 |
| `in_params` | array | 否（无参数可为空） | 输入参数列表，每项含：<br>• `parameter_name`（必填）<br>• `description`（必填，自然语言说明）<br>• `type`（`string`/`number`/`boolean`/`object`，**Object 类型子属性不能为空**）<br>• `passing_method`（`model_recognition`：由模型提取；`biz_pass_through`：由业务层透传） |
| `out_params` | array | 否 | 输出参数结构定义，用于指导模型解析响应（字段名、类型、说明） |
| `advanced_config.value` | object | 否 | 可选调用示例（如 `{ "query": "通义千问开源地址" }`），显著提升复杂参数场景下的参数提取准确率 |

> ⚠️ 重要限制：  
> - GET 请求**不支持 `object` 类型输入参数**；如需嵌套结构，必须使用 POST + `application/json`；  
> - 自定义插件**仅支持透传 `Authorization` header**，不支持其他自定义 Header（如 `X-Api-Key`）；  
> - 所有工具必须处于“已发布”且“启用”状态才可被调用；修改 `plugin_url` 或鉴权配置后，须重新测试并发布。

## 面向开发者：简洁实用指南

- **快速起步**：优先使用官方插件（`code_interpreter`, `calculator`, `text_to_image` 等），无需配置即可在智能体中启用；  
- **调试技巧**：在智能体对话测试页，开启「显示思考过程」可查看模型是否识别插件、如何提取参数；工具 ID 可在插件详情页悬停复制，用于日志追踪；  
- **自定义开发**：遵循 OpenAPI 规范设计后端 API → 控制台创建插件 → 逐个定义工具 → 填写高质量 `tool_description`（含正/反例）→ 发布；  
- **错误排查**：常见失败码：`130040`（参数 `description` 缺失）、`130022`（Object 子属性为空或 GET 含 Object 参数），按提示修正后重试；  
- **生产注意**：单次请求最多调用 10 个工具（跨插件累加）；`code_interpreter` 运行于沙箱，禁止网络访问与文件上传；`quark_search` / `github_search` 仅返回标题、关键词、摘要，**不支持访问原始网页/仓库详情**。

## 关联主题页

- [plug in](../guides/plug-in.md)
- [model context protocol](../guides/model-context-protocol.md)
- [application support](../guides/application-support.md)
- [llm application](../guides/llm-application.md)
- [skill](../guides/skill.md)


