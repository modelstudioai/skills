# llm application

百炼平台的 LLM Application 是面向生产环境的 AI 应用构建体系，提供智能体（Agent）、工作流（Workflow）和高代码应用三类范式，分别覆盖零代码决策、低代码编排与专业级代码开发场景。所有类型均深度集成模型调用、知识库（RAG）、外部工具（MCP/插件）及[多模态](../concepts/multimodal.md)解析能力，支持从快速原型到企业级服务的全生命周期交付。

## 支持的模型与功能

百炼 LLM Application 支持三类核心模型能力：

- **文本大模型**：包括千问系列（Qwen-Plus、Qwen-Max、Qwen3-Coder-Plus 等）、QwQ、开源模型（Qwen2/Qwen2.5）等，用于推理、生成、规划与工具调用；  
- **[多模态](../concepts/multimodal.md)模型**：Qwen-VL 系列（VL-Max、VL-Plus、VL-OCR）支持图文理解与跨模态参数提取，[详见文档](../../raw/application-user-guide/llm-application/file-q-a.md)；  
- **专用模型**：意图分类、参数提取、[多模态](../concepts/multimodal.md)生成等节点内置专用模型，如意图分类节点支持 DeepSeek 等第三方模型，[参见意图分类节点文档](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)。

功能层面统一支持：
- **知识库（RAG）**：通过知识库节点或智能体配置接入文档/表格/图片三类知识库，支持 topK 控制、智能过滤与调试召回效果；
- **工具调用**：涵盖 MCP 服务（高德地图、天气等）、插件（计算器、代码执行）、函数计算（FC）、API 节点及数据连接器，全部在隔离沙箱中运行；
- **多模态解析**：文档、图片、音频、视频解析节点分别支持结构化输出（如 `layout`、`images`、`segments`），且多数解析器暂不计费；
- **动态规划与调度**：Agent 2.0 支持统一工具抽象与“规划-执行-反思”链路，智能体群组节点支持多智能体协同决策。

> **注意**：文档 1（Agent 1.0）与文档 2（Agent 2.0）存在明确版本演进关系，后者将知识库与 MCP 统一为工具并支持完整过程回溯，[新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md) 已成为推荐标准，旧版仅适用于历史兼容场景。

## 关键参数

各节点共性参数保持一致，便于开发者复用经验：

| 参数 | 默认值 | 说明 | 适用节点示例 |
|------|--------|------|--------------|
| `temperature` | `0.70` | 控制输出随机性，范围 `[0, 2)`；值越高越多样，越低越确定 | 大模型节点、意图分类节点、参数提取节点、智能体创建节点等 |
| `top_p` | `0.80` | 核心采样阈值，控制输出多样性 | 大模型节点、意图分类节点等 |
| `max_output_length`（最长回复长度） | `1024`（部分节点为 `1024`，Agent 2.0 中为模型级配置） | 模型生成内容的最大 token 数，不含提示词 | [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)、[智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md) |
| `enable_thinking` | `开启` | 启用思维链（CoT）推理模式，输出中间推理过程 | 所有含该字段的节点（如大模型、意图分类、参数提取）均需模型原生支持 |
| `thinking_budget` | `4000` | 思考模式下允许的最大推理 token 数 | 大模型节点、意图分类节点等 |

此外，Agent 2.0 新增 `enable_thinking`（非 `enable_thinking` 的旧写法）及 `AUTO` 智能路由档位（性能/均衡/经济），而 Agent 1.0 仅支持 `推理模式` 开关，二者参数命名与语义不完全兼容。

## 使用方式

### 1. 选型决策
- **智能体（Agent）**：适合开放式对话与自主决策任务（如客服助手、旅行规划），推荐使用 [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)；
- **工作流（Workflow）**：适合固定流程自动化（如报告生成、订单审批），通过可视化节点编排实现强可控性；
- **高代码应用**：面向专业开发者，基于 Python 项目一键部署为 Serverless 或 K8s 服务，支持 MCP 工具接入与可观测性埋点。

### 2. 快速启动
- **Agent**：控制台 → 应用管理 → 创建应用 → 选择 *智能体应用 > Agent 2.0* → 选模型（如 `千问-Max`）→ 发布；
- **Workflow**：添加开始节点 → 连接知识库/大模型/条件判断等节点 → 配置输入/输出变量 → 设置结束节点 → 发布；
- **高代码**：控制台创建空白高代码应用 → 上传 `.whl` 包或选用模板 → 部署（Serverless/K8s）→ [参考 API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)。

### 3. 文件处理
文件问答支持三种模式：
- **全文引用**：直接注入解析后全文（受上下文限制）；
- **切片检索（RAG）**：默认策略，按 [Token](../concepts/token.md) 切片+重叠，检索最相关片段；
- **自定义处理**：关闭预解析，由模型自主调用工具处理 URL 或内容。

> **注意**：文档 33 明确指出“上传的文件仅在**当前会话**中有效”，刷新页面即丢失，生产环境需结合知识库存储或服务端持久化。

## 限制和注意事项

- **上下文与 [Token](../concepts/token.md) 限制**：所有模型均受上下文窗口约束；知识库检索结果占用上下文；Agent 2.0 在上下文超 200K [Token](../concepts/token.md) 时强制路由至“性能”档，避免截断失效。
- **文件限制**：
  - 智能体单会话：≤10 个文件，单文件 ≤10 MB；
  - 工作流节点：文档解析 ≤150 MB / 1.5 万页，图片 ≤20 MB，音视频 ≤512 MB；
  - 所有解析节点**仅支持单文件**，不支持列表批量解析（批处理节点除外）。
- **工具与权限**：
  - MCP/API/FC 节点需提前开通对应服务，并将百炼 IP（`47.93.216.17`, `39.105.109.77`）加入目标服务白名单；
  - 高代码应用部署需授权 FC 与 API 网关角色，权限不足时需联系管理员。
- **模型兼容性**：`enable_thinking`、`enable_search` 等参数仅对支持该能力的模型生效，控制台未显示即表示不支持；Qwen-VL 系列模型即使关闭预解析，仍可直接解析图片/视频。
- **输出格式限制**：变量处理节点的 JSON 输出模式**仅支持单层键值对**，无法生成嵌套 JSON 或数组，复杂结构需下游脚本节点二次处理。

## 来源文档

- [智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)
- [新版智能体应用（Agent 2.0）](../../raw/application-user-guide/llm-application/new-single-agent-application.md)
- [应用类型介绍](../../raw/application-user-guide/llm-application/application-introduction.md)
- [工作流应用](../../raw/application-user-guide/llm-application/workflow-application.md)
- [开始和结束节点](../../raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
- [条件判断节点](../../raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
- [循环节点](../../raw/application-user-guide/llm-application/workflow-application/loop-node.md)
- [批处理节点](../../raw/application-user-guide/llm-application/workflow-application/batch-node.md)
- [流程输出节点](../../raw/application-user-guide/llm-application/workflow-application/process-output-node.md)
- [知识库节点](../../raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
- [大模型节点](../../raw/application-user-guide/llm-application/workflow-application/llm-node.md)
- [意图分类节点](../../raw/application-user-guide/llm-application/workflow-application/intent-node.md)
- [参数提取节点](../../raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
- [智能体创建节点](../../raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
- [多模态生成节点](../../raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
- [智能体群组节点](../../raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)
- [API节点](../../raw/application-user-guide/llm-application/workflow-application/api-node.md)
- [函数计算节点](../../raw/application-user-guide/llm-application/workflow-application/fc-node.md)
- [插件节点](../../raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
- [MCP节点](../../raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
- [脚本节点](../../raw/application-user-guide/llm-application/workflow-application/script-node.md)
- [AppFlow节点](../../raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
- [变量处理节点](../../raw/application-user-guide/llm-application/workflow-application/variable-processing-node.md)
- [应用组件节点](../../raw/application-user-guide/llm-application/workflow-application/component-node.md)
- [变量赋值节点](../../raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
- [文档解析节点](../../raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
- [图片解析节点](../../raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
- [音频解析节点](../../raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
- [视频解析节点](../../raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
- [数据连接器节点](../../raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)
- [API 开发指南](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-app-develop-guide.md)
- [工具接入](../../raw/application-user-guide/llm-application/rich-code-application/rich-code-application-mcp.md)
- [文件问答](../../raw/application-user-guide/llm-application/file-q-a.md)
- [高代码应用](../../raw/application-user-guide/llm-application/rich-code-application.md)


