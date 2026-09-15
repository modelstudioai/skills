# 应用核心组件能力对比：应用调用、组件API与沙箱

本文档面向百炼平台开发者，旨在清晰区分三种核心能力——`application call`（应用调用）、`application component API`（应用组件 API）与 `sandbox API`（沙箱 API）——在技术定位、使用边界、能力范畴及工程实践中的关键差异。三者虽同属百炼开放能力体系，但设计目标迥异：  
- **应用调用** 面向「业务结果交付」，以终态应用为单位封装完整 AI 流程；  
- **应用组件 API** 面向「能力原子复用」，提供可组合的对话、检索、工作流等标准化服务单元；  
- **沙箱 API** 面向「运行时环境管控」，聚焦代码/Agent 所需的安全隔离执行环境的全生命周期管理。  
正确理解三者分层关系，是构建高可用、可演进 AI 应用架构的技术前提。

## 关键维度对比

| 维度 | [application call](../api/application-call.md) | application component API | [sandbox](../guides/sandbox.md) API |
|------|------------------|----------------------------|--------------|
| **核心定位** | 调用已部署的**完整业务应用**（含模型+工具+RAG+会话状态） | 调用平台提供的**可复用原子能力组件**（如 chat、retrieve、run_workflow） | 管理**安全隔离的代码执行环境**（沙箱实例与模版） |
| **输入格式** | `{"app_id": "...", "input": {"text": "..."}, "parameters": {...}}`（统一结构） | 因接口而异：<br>• `chat`: `{"messages": [...]}`<br>• `retrieve`: `{"query": "...", "top_k": 5}`<br>• `run_workflow`: `{"inputs": {...}}` | 按操作类型严格定义：<br>• 创建实例：`{"templateID": "...", "timeout": 300, "network": {...}}`<br>• 创建模版：`{"cpuCount": 2, "memoryMB": 4096, "envConfig": {...}}` |
| **输出格式** | 统一封装为百炼标准响应体：<br>`{"output": {...}, "usage": {...}, "request_id": "..."}`（同步）<br>或 SSE 流式事件（DashScope 原生） | RESTful JSON 响应，**无统一外层包装**：<br>• `chat`: `{"choices": [...], "usage": {...}}`（类 OpenAI）<br>• `retrieve`: `{"results": [{"content": "...", "score": 0.92}...]}`<br>• `run_workflow`: `{"status": "success", "outputs": {...}}` | **原生 E2B 风格响应**，无百炼 `Result<T>` 封装：<br>• 实例创建：`{"id": "sbx-xxx", "status": "running", "domain": "..."}`<br>• 模版构建：`{"status": "ready", "build_id": "bld-xxx"}` |
| **支持模型/能力** | ✅ 所有已发布应用（Qwen/GLM/Llama/自定义微调）<br>✅ 内置[函数调用](../concepts/function-calling.md)、RAG、多轮会话（`conversation_id`）<br>❌ 不暴露底层模型选择权 | ✅ 显式指定 `model_id`（如 `qwen-max`）<br>✅ 对话（`chat`）、知识检索（`retrieve`）、工作流（`run_workflow`）<br>❌ 不支持[函数调用](../concepts/function-calling.md)（需上层应用封装） | ❌ **不提供任何模型推理能力**<br>✅ 沙箱实例生命周期管理（创建/暂停/恢复/释放）<br>✅ 模版构建与配置（网络策略、资源规格、自动伸缩）<br>✅ 支持 Python/Node.js 等运行时环境 |
| **API 端点** | • DashScope 原生：`POST /api/v1/applications/{app_id}/call`<br>• OpenAI 兼容：`POST /v1/chat/completions`（需配置路由） | `POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/{chat|retrieve|run_workflow}` | `POST https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/sandbox/sandboxes`<br>（地域固定为 `cn-beijing`） |
| **鉴权方式** | `Authorization: Bearer <api_key>`（API Key） | `Authorization: Bearer <access_token>`（RAM 角色短期 [Token](../concepts/token.md) 或 OAuth2 Access [Token](../concepts/token.md)） | `Authorization: Bearer <api_key>`（API Key）<br>⚠️ 不支持 `X-API-Key`（E2B 兼容头仅作格式兼容） |
| **计费方式** | 按**应用调用次数 + 输出 token 数量**计费（与所选应用绑定的计费策略一致） | 按**各组件调用次数 + token/请求量**独立计费：<br>• `chat`: token 用量<br>• `retrieve`: 请求次数 + 返回片段数<br>• `run_workflow`: 工作流执行次数 | 按**沙箱实例运行时长（秒） + 资源规格（vCPU/内存）** 计费<br>• 暂停状态不计费，释放后停止计费<br>• 模版构建免费 |
| **典型场景** | • 客服机器人前端集成<br>• 企业微信/钉钉 Bot 的消息响应<br>• 低代码平台中嵌入预训练应用 | • 自研对话系统中动态切换模型与检索源<br>• 构建混合 RAG+LLM 的分析看板<br>• 可视化工作流引擎的 API 编排层 | • 运行用户上传的 Python 脚本进行数据清洗<br>• 托管自主决策 Agent（需访问外部 API）<br>• 安全沙箱化执行第三方代码（如插件、工具函数） |
| **流式支持** | ✅ DashScope 原生接口支持 SSE（`enable_stream: "true"`）<br>✅ [OpenAI 兼容接口](../concepts/openai-compatible-api.md)支持 `stream: true` | ✅ `chat` 与 `run_workflow` 支持 `stream=true`（SSE）<br>❌ `retrieve` 为同步批量返回 | ❌ **不提供流式响应**<br>• 实例连接后通过独立 `exec`/`ws` 接口实现交互式流式通信 |

## 各方案适用场景建议

| 场景描述 | 推荐方案 | 理由说明 |
|----------|----------|-----------|
| **快速上线一个端到端 AI 功能（如智能合同审核、HR 面试助手）** | ✅ `application call` | 无需关心模型选型、工具集成、上下文维护等细节，直接调用已调试完成的应用，开发成本最低，交付最快。 |
| **构建高度定制化的 AI 应用（如多源知识融合问答系统），需灵活组合不同模型、检索器与工作流** | ✅ `application component API` | 提供细粒度能力解耦：可独立调用 `retrieve` 获取知识片段，再用 `chat` 注入上下文生成答案；支持按需指定 `model_id`，便于 A/B 测试与灰度发布。 |
| **需要执行不可信代码、调用外部私有 API、或运行计算密集型脚本（如 Pandas 数据分析）** | ✅ `sandbox API` | 提供硬件级隔离、网络白名单、超时熔断等安全机制，确保用户代码无法影响主服务，且能精确控制资源消耗与生命周期。 |
| **将已有 OpenAI 生态应用无缝迁移到百炼** | ✅ `application call`（OpenAI 兼容层） | 复用现有 SDK 与请求逻辑，仅需替换 endpoint 和 API Key，最小化迁移改造。 |
| **在自研 Agent 框架中集成百炼能力，同时要求模型可插拔与环境可控** | ⚠️ **组合使用**：<br>• `application component API` 调用 `chat`/`retrieve`<br>• `sandbox API` 托管 Agent 的规划与执行模块 | 组件 API 提供语义层能力，沙箱 API 提供执行层保障，二者协同实现“思考-行动”分离架构。 |

## 技术选型参考指南（致开发者）

- **优先选择 `application call` 当**：  
  你的需求是“调用一个功能明确、已上线验证的应用”，且对底层技术栈无定制诉求。这是百炼最成熟、文档最完善、SLA 最高的能力入口，适合 80% 的业务集成场景。

- **选择 `application component API` 当**：  
  你需要**解耦能力与编排逻辑**，例如：  
  • 在同一应用中，对不同用户群体启用不同模型（`model_id` 动态路由）；  
  • 构建带 fallback 机制的检索链（先 `retrieve`，失败则 `chat` 生成兜底回答）；  
  • 将百炼作为能力底座，嵌入自研的 LangChain / LlamaIndex 工程栈。  
  > 💡 注意：该 API 要求你自行管理会话状态（如 `conversation_id` 需上层传递），不提供开箱即用的多轮上下文抽象。

- **必须使用 `sandbox API` 当**：  
  你的用例涉及**代码执行安全边界**，包括但不限于：  
  • 用户可提交任意 Python 代码并期望其被安全执行；  
  • Agent 需调用企业内网 API（需配置 `allowOut` 白名单）；  
  • 需要 GPU 加速的推理后处理（如图像生成后的 OpenCV 处理）。  
  > ⚠️ 警告：沙箱 API **不替代模型推理**！它只提供环境，模型调用仍需通过 `application call` 或 `component API` 完成。

- **避免混淆的关键红线**：  
  • ❌ 不要用 `sandbox API` 替代 `application call` 来做文本生成——性能差、成本高、无模型优化；  
  • ❌ 不要用 `application call` 实现复杂工作流编排——缺乏错误重试、分支判断等控制流能力；  
  • ❌ 不要用 `application component API` 的 `retrieve` 替代应用内 RAG——它不感知应用配置的默认知识库，需显式传参。

通过本对比，开发者可依据自身架构层级（业务层 → 能力层 → 运行时层）精准匹配百炼能力，避免过度设计或能力错配，提升研发效率与系统健壮性。

## 被对比主题页

- [application call](../api/application-call.md)
- [application component api reference](../api/application-component-api-reference.md)
- [sandbox api](../api/sandbox-api.md)


