# Prompt 工程

Prompt 工程是系统化设计、验证、迭代和部署 Prompt 的方法论与实践体系，旨在通过结构化模板、上下文增强、样例驱动优化及可观测评估等手段，持续提升大模型在具体业务场景中的输出质量、稳定性与可控性。它不是一次性指令编写，而是覆盖开发、调试、评测、上线与监控的全生命周期工程活动。

## 在百炼平台的不同场景中，这个概念如何使用

- **智能体（Agent）构建**：在应用组件 API 或智能体工作流中，Prompt 工程体现为 `system` 消息的精细化编排（如角色设定、约束规则、输出格式规范），并结合 RAG 表格库实现动态上下文注入；`has_thoughts=true` 可实时观测 Prompt 实际填充内容与召回片段，支撑调试闭环。  
- **模板化生产交付**：通过控制台「提示词」页面创建文本/图像生成类 Prompt 模板，支持 ICIO、CRISPE 等主流框架引导式搭建，并绑定变量（如 `topic`, `tone`）实现一次定义、多处复用；所有模板仅在华北2（北京）地域可用。  
- **自动化评测与优化**：借助 `agenteval` 模块，将线上 Trace 中沉淀的用户请求与模型响应作为评测数据集，通过多维评估器（相关性、正确性、格式合规等）量化 Prompt 效果；再基于人工反馈或 A/B 对比，生成优化建议并手动采纳至模板或应用配置中。  
- **多模态生成场景**：在万相（Wanx）文生图/文生视频调用中，Prompt 工程体现为严格遵循领域指南的结构组织（如正向 prompt + negative prompt 分隔、`aspect_ratio` 字段化而非参数化），确保生成结果符合视觉语义预期。  
- **资产中心统一管理**：Prompt 模板作为一类核心资产（`asset_type=prompt`）纳入资产中心，支持版本管理、权限控制、调用日志溯源与灰度发布，实现 Prompt 与模型、RAG 知识源的协同演进。

## 关键参数和配置

| 参数 | 说明 | 开发者须知 |
|------|------|------------|
| `promptTemplateId` | 模板唯一标识符，用于 API 获取与填充 | 控制台模板卡片上直接复制；调用 `GetPromptTemplate` 后需解析其 `variables` 字段以确认必填变量名 |
| `variables` | 模板中声明的占位变量列表（如 `["product", "audience"]`） | 填充时必须提供全部变量值，缺失任一将导致生成失败；建议在 SDK 封装层做变量完整性校验 |
| `has_thoughts` | 应用 API 请求参数，启用后响应中返回 `thoughts` 字段 | 调试阶段必开，可查看实际注入的 RAG 片段、样例匹配详情及 token 消耗分布；线上环境建议关闭以减少响应体积 |
| `recall_count` | RAG 表格库召回片段数量（替代已下线的样例库） | 默认 5，最大 10；增加召回数会提升上下文丰富度但显著增加输入 token，需权衡效果与成本 |
| `workspaceId` | 业务空间 ID，所有 Prompt 相关 API 的必需凭证 | 必须通过控制台或 API 显式获取，不可复用 APP ID；跨 workspace 调用将报错 |

> ⚠️ 注意：Prompt 样例库功能已全面下线，所有新项目必须使用 RAG 表格库替代；自动优化（控制台功能）无对应 API，优化结果需手动保存为模板复用。

## 面向开发者，简洁实用

- **起步建议**：从预置模板开始（如“营销文案生成”），在控制台调试界面开启 `RAG 调试`，观察变量填充与召回效果，再逐步迁移到自定义模板。  
- **调试黄金组合**：API 请求中设置 `has_thoughts=true` + `stream=false`，解析 `thoughts.recall_results` 和 `thoughts.prompt_content`，精准定位上下文注入问题。  
- **变量安全填充**：对用户输入的变量值（如 `topic`）务必做长度截断（≤50 字符）与敏感词过滤，避免 Prompt 注入攻击或超长输入触发截断。  
- **效果验证三步法**：① 用典型 query 手动调试；② 构建 5–10 条基础评测集跑 `agenteval` 自动评分；③ 对低分 case 添加人工反馈，驱动 Prompt 迭代。  
- **生产注意事项**：Prompt 模板本身不计费，但 RAG 注入内容计入输入 token；单次请求总 token（含 system prompt + user input + RAG 片段）不得超过 32768；图像/视频生成 prompt 长度另有更严限制（≤1000 / ≤500 字符）。

## 关联主题页

- [prompt](../guides/prompt.md)
- [agenteval](../guides/agenteval.md)
- [use cases](../guides/use-cases.md)
- [application component api reference](../api/application-component-api-reference.md)
- [asset center page](../guides/asset-center-page.md)


