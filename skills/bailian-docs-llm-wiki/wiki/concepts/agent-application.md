# 智能体应用

智能体应用（Agent Application）是百炼平台的核心应用形态之一，通过自然语言配置（零代码）构建，由大模型根据系统提示词自主规划工具调用顺序，实现知识问答、任务处理等场景。开发者无需编写编排逻辑，只需定义角色、挂载工具与知识库，模型即可基于 ReAct 循环完成多步推理与执行。

## 两代架构

百炼提供两代智能体应用，**推荐优先使用 Agent 2.0**：

- **Agent 2.0**：将知识库、MCP 等统一为工具，由模型基于 ReAct 循环自主规划调用时机与顺序，完整暴露"思考-执行-反思"链路。2025 年 12 月 26 日上线。
- **Agent 1.0**：先命中知识库再决策是否调用其他工具，仅展示最终结果。

> 两代基于不同技术架构，**不支持直接升级或迁移**，切换需重新创建应用。

## 关键配置

| 配置项 | 说明 |
| --- | --- |
| 模型 | 推荐 `千问-Max` 系列以保障多步工具调用效果；支持 `enable_thinking`（仅思考模型可配）、`temperature`、最长回复长度 |
| 系统提示词 | 定义角色、输出格式、约束和工具使用指引；支持自定义变量（通过 `/` 引用） |
| 知识库（RAG） | 作为工具由 Agent 2.0 自主调用；支持按标签过滤检索范围；可开启"展示回答来源"以角标形式返回 |
| MCP 与插件 | Agent 2.0 全部外部工具统一走 MCP 协议；插件可一键转换为 MCP |
| 内置工具 | `bash` / `write` / `read` / `edit` / `glob` / `grep` / `download_file`，沙箱内运行，默认关闭 |
| 预解析文件 | 控制上传文件是否由平台预置解析器提取文本；关闭时文件 URL 作为上下文透传 |
| ReAct 最大轮次 | 1–50，超限后强制生成最终回复 |
| 短期记忆 | 0–30 轮上下文 |

## 文件问答

智能体支持三种文件处理模式：

| 模式 | 机制 | 适用场景 |
| --- | --- | --- |
| 全文引用 | 平台解析后将文件整体注入 Prompt（受上下文长度限制） | 全文总结、翻译、润色 |
| 切片检索（RAG） | 平台解析并切片，按相关性召回若干片段 | 长文档问答、来源定位 |
| 自定义处理 | 只把文件 URL 或原始内容交给模型，由模型调用工具处理 | 图像风格转换、视频分析 |

- 单会话上传上限 **10 个文件**，单文件 **≤ 10 MB**。
- 页面上传的文件仅当前会话有效；生产场景推荐通过文件上传 API 换取 `session_file_id`（有效期约 24 小时）。
- API 调用时**无法**动态切换处理模式，取决于应用发布时的配置。
- 文件问答共享所属智能体应用的限流：**默认 100 次/分钟**。

## 调用方式

通过 DashScope SDK 或 HTTP API 调用，接口为 `POST /apps/{APP_ID}/completion`：

```python
import os
from http import HTTPStatus
from dashscope import Application

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id='YOUR_APP_ID',
    prompt='你是谁？'
)
if response.status_code == HTTPStatus.OK:
    print(response.output.text)
```

响应结构为 `{"output": {"finish_reason", "session_id", "text"}, "usage": {...}, "request_id": "..."}`，业务侧主要消费 `output.text`。2025 年 11 月起还支持通过 Responses API 调用，提供同步与异步两种模式。

## 发布与分享

- **Agent 1.0** 支持多种分享渠道：UI 应用/魔笔、钉钉、微信公众号、组件化发布、音视频实时互动。临时体验二维码与 UI 体验链接有效期均为 24 小时。
- **Agent 2.0** 仅支持通过 API 调用，不支持上述分享渠道。

智能体或[工作流](workflow.md)应用可发布为模块化组件供其他应用复用，组件预设系统参数 `query` 和 `imageList`（不可删除，可隐藏）。接入方支持智能体应用（作为工具，模型自动调用）和[工作流](workflow.md)应用（作为组件节点，手动传参）。

## 评测与监控

- **评测**：支持自动评测（基于知识库自动生成评测集并评分）和手动评测（人工标注）。单应用评测深度评估表现，多应用横向评测最多对比 8 个应用。新版评测系统通过评估器（LLM / Code）和标签管理构建多维评测闭环。
- **监控**：应用观测功能可端到端追踪调用链路，提供延时、[Token](token.md) 量等分钟级指标。支持 Root Span / All Span / Model Span 筛选模式，可将 Span 数据直接加入评测集。观测覆盖智能体应用、[工作流](workflow.md)应用和高代码应用。

## 与其他形态的对比

| 维度 | 智能体应用 | 工作流应用 | 高代码应用 |
| --- | --- | --- | --- |
| 开发方式 | 自然语言配置（零代码） | 可视化节点编排（低代码） | Python 项目（专业代码） |
| 控制方式 | 模型自主规划 | 预定义节点顺序 | 代码完全控制 |
| 适合人群 | 业务/产品/运营 | 业务分析师/IT 实施 | AI 工程师 |
| 典型场景 | 客服、知识问答、任务助理 | 报告生成、审批流、数据标注 | 私有算法、复杂系统集成 |

与 Managed Agents 的区别：智能体应用为无状态调用（应用侧维护上下文），Managed Agents 由服务端托管会话状态、沙箱环境与工具执行，支持中断与续接，适合长时运行的多步工具调用任务。

## 关联主题页

- [start using](../guides/start-using.md)
- [llm application](../guides/llm-application.md)
- [application publishing and sharing](../guides/application-publishing-and-sharing.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [application evaluation](../guides/application-evaluation.md)
- [application monitoring](../guides/application-monitoring.md)
- [application permission management](../guides/application-permission-management.md)
- [application use cases](../guides/application-use-cases.md)
- [skill](../guides/skill.md)
- [managed agents](../guides/managed-agents.md)


