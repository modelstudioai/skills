# 工作流

工作流（Workflow）是百炼平台三种核心应用构建模式之一，通过可视化节点编排将复杂任务拆解为有序步骤，逻辑确定、稳定可复现，适合流程固定、要求可复现的业务场景。

## 在百炼平台中的定位

百炼提供智能体、工作流、高代码应用三种互补的应用构建模式。工作流对应"可视化节点编排（低代码）"路线，由预定义节点精确控制流程，适合 IT 运维、业务分析师构建报告生成、订单处理、审批流等场景。与由大模型自主规划的智能体不同，工作流强调开发者对流程的显式控制，输出可复现、可调试。

## 核心节点

工作流画布由以下节点类型组成：

- **开始 / 结束节点**：定义输入与输出参数。开始节点预置 `query`（用户输入）、`historyList`（对话历史）、`imageList`（图片）等变量，可在下游节点中引用。
- **大模型节点**：执行 LLM 推理，配置模型、提示词、用户提示词、记忆等。
- **意图分类节点**：根据输入分流到不同下游分支，支持多意图。
- **变量处理节点**：用于文本输出或变量加工。
- **智能体群组节点**：将任务分解给多个已发布的子智能体协同完成。

## 会话变量

会话变量作为全局变量在工作流全生命周期内记录参数，可在各节点中引用，在画布右上角配置。适合跨节点传递状态、累积上下文信息。

## 典型案例

- **诈骗信息识别**：开始 → 大模型（提示词判定诈骗嫌疑）→ 结束。
- **智能导购**：意图分类节点将输入分流到手机 / 电视 / 冰箱等大模型分支，未命中分支走变量处理节点。
- **日程管理助手**：通过智能体群组节点串联"信息收集"与"数据整理"两个子智能体。

## 创建与发布流程

1. 控制台 → 应用管理 → 创建应用 → 工作流应用。
2. 在画布上拖拽编排节点，配置各节点的模型、提示词、变量引用关系。
3. 右侧对话框调试。
4. 右上角"发布"——发布是后续 API 调用与集成的前提。

## API 调用

工作流应用与智能体应用共用同一套调用接口，区别仅在应用内部的编排逻辑。发布后通过 `APP_ID` 调用：

- **DashScope 原生 API**：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，请求体为 `{"input": {"prompt": "..."}, "parameters": {}, "debug": {}}`，响应中业务侧主要消费 `output.text`。
- **OpenAI 兼容 Responses API**：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，可复用现有 OpenAI 生态代码库，支持同步 / 异步、流式、多模态。
- **SDK**：Python 使用 `dashscope.Application.call`，Java 使用 `com.alibaba.dashscope.app.Application`，Node.js 可直接以 `axios` 发起 POST。

调用前需在控制台获取应用 ID 与 API Key（推荐写入 `DASHSCOPE_API_KEY` 环境变量）；若应用位于子业务空间，还需提供 Workspace ID。

## 多轮对话

工作流应用支持多轮对话，有两种实现方式：

- **使用 `session_id`**：系统自动从云端加载历史对话，实现简单。`session_id` 有效期 1 小时，最多支持 50 轮。
- **自行管理 `messages`（推荐）**：手动维护消息列表，灵活性更高，不受 session 有效期限制。

## 评测

工作流应用可作为评测任务的被测对象。在新版应用评测中，评测集支持智能体、工作流、自定义三种类型，按所选应用的出入参形式自动生成数据模板。评测任务可关联工作流应用，由 LLM 评估器或 Code 评估器自动评分，也可人工标注。

## 发布与分享

工作流应用支持多种发布渠道：UI 应用（通过 UI 设计器构建自定义界面）、钉钉机器人、微信公众号、组件化复用（将工作流作为其他智能体或工作流的子组件）、音视频实时互动（仅限图文对话类）。需要注意的是，官方网页版分享当前只支持智能体应用，不支持工作流应用。

## 关键限制与注意事项

- 工作流应用若配置了文件类型的自定义参数，在 UI 设计器中需指定 `{{{file_name:files[0]}}}`（将 `file_name` 替换为实际变量名），否则应用无法正确读取用户上传的文件。
- 旧版"智能体编排"应用已被工作流应用替代，新建应用请直接选择工作流。
- 工作流与智能体调用接口一致，但可附加的扩展能力（如自定义参数传递）取决于应用内部编排逻辑。

## 关联主题页

- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [application evaluation](../guides/application-evaluation.md)
- [application publishing and sharing](../guides/application-publishing-and-sharing.md)


