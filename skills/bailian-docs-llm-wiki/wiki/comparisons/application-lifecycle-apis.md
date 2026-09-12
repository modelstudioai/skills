# 应用全生命周期管理 API 对比

为帮助开发者在百炼平台中高效构建、发布、观测与管控大模型应用，本文系统对比四大核心能力所对应的 API 接口体系：**应用调用（Calling）**、**应用发布与分享（Publishing & Sharing）**、**应用监控（Monitoring）** 和 **应用权限管理（Permission Management）**。这些 API 共同构成应用从开发完成到生产落地的完整生命周期支撑链路。本对比聚焦技术实现细节，面向工程化集成场景，旨在为 API 选型、系统架构设计及运维策略制定提供客观、可落地的技术参考。

---

## 关键维度对比表

| 维度 | 应用调用 API（`/apps/{app_id}/chat`） | 应用发布与分享 API（`/applications/{app_id}/publish`） | 应用监控 API（控制台集成 + SDK 透传） | 应用权限管理 API（RAM 策略驱动） |
|------|----------------------------------------|--------------------------------------------------------|------------------------------------------|------------------------------------|
| **输入格式** | JSON 请求体，含 `input`（用户数据）、`parameters`（运行时参数）、`session_id`（可选） | JSON 请求体，含 `publish_type`（`web_app`/`component`/`api`）、`access_control`、`ui_config` 或 `component_input_schema` | 无独立请求体；通过 SDK 方法参数（如 `trace_id`, `env`）或 HTTP Header（如 `X-Bailian-Trace-ID`）透传元数据 | 无直接调用 API；通过 RAM 控制台或 OpenAPI（`ram:CreatePolicy` 等）配置策略 JSON，声明 `Resource`、`Action`、`Condition` |
| **输出格式** | 标准化 JSON 响应，含 `output.text`（智能体）或 `output.choices[0].message.content`（工作流），支持 `stream` 流式响应头 | JSON 响应，含 `publish_id`、`endpoint_url`（Web/API）、`component_ref_id`（组件）、`status` 及生效时间戳 | 无实时返回；数据通过控制台「监控」页可视化呈现，支持 CSV 导出；原始指标需对接 SLS 查询 | 无运行时返回；权限校验由百炼服务端在每次调用（如 `/apps/{app_id}/chat`）前自动执行，失败时返回 `403 Forbidden` 及 `AccessDenied` 错误码 |
| **支持模型** | 所有已绑定至该应用的托管模型（Qwen-Max/Plus/2-VL/3、RAG 引擎、自定义微调模型等），模型选择由应用定义决定 | 仅支持百炼平台**托管模型**；不支持第三方非托管模型（如用户自建 VLLM 服务）直接发布为 `api` 或 `web_app`；私有模型需满足网络可达性要求 | 支持所有通过百炼 SDK / REST API 调用的**托管模型应用**；不监控用户自建后端封装层（如 FastAPI 封装） | 与模型无关，覆盖所有百炼平台上的应用资源（无论其底层是 Qwen、RAG 还是工作流），权限作用于 `application` 资源抽象层 |
| **API 端点** | `POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/chat` | `POST https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/publish` | **无独立端点**；监控能力内嵌于调用链路（如 `chat_completions` SDK 方法自动上报）；SLS 查询需使用 `sls:GetLogs` 等独立 OpenAPI | **无百炼专属端点**；完全基于阿里云 RAM OpenAPI（如 `ram:CreatePolicy`, `ram:AttachPolicyToUser`），策略生效后由百炼服务端统一鉴权 |
| **计费方式** | 按实际调用产生的 **[Token](../concepts/token.md) 消耗量** 计费（输入+输出），模型单价依所绑定模型而定；调用本身不额外收费 | **发布行为免费**；但发布后的 `web_app` 访问、`api` 调用、`component` 执行均触发对应模型 [Token](../concepts/token.md) 计费；`web_app` 的 CDN/域名解析等基础设施费用另计 | 监控数据采集与基础图表展示**免费**；历史数据超过 30 天或需长期存储分析时，需开通 SLS 并按日志写入/查询量计费 | 权限策略配置与鉴权服务**免费**；RAM 资源本身无额外费用（标准用量下） |
| **典型场景** | - 第三方系统集成（CRM/ERP 中嵌入 AI 助手）<br>- 自动化工作流触发（如定时摘要邮件）<br>- 实时对话服务（客服机器人） | - 向业务方交付独立 AI 应用（带品牌 UI 的 Web 页面）<br>- 构建低代码平台能力中心（复用为可拖拽组件）<br>- 对接企业内部 API 网关（发布为标准化 REST 接口） | - 定位高延迟请求根因（关联 Trace ID 查看各节点耗时）<br>- 分析 [Token](../concepts/token.md) 成本分布（识别低效 [prompt](../guides/prompt.md) 或冗余输出）<br>- 设置 P95 延迟 >2s 告警（保障 SLA） | - 为测试人员授予 `InvokeApplication` 权限（禁止修改配置）<br>- 为运维团队授予 `ListApplicationLogs` + `DescribeApplication` 权限<br>- 为外部合作方创建最小权限角色（仅允许调用指定 `app-id`） |

---

## 各方案适用场景建议

| 方案 | 推荐使用场景 | 不推荐场景 | 关键注意事项 |
|------|--------------|------------|----------------|
| **应用调用 API** | 需要**高频、低延迟、结构化响应**的生产级集成；对会话状态（`session_id`）有明确管理需求；需灵活覆盖模型参数（`temperature`, `max_tokens`） | 需要强一致性上下文管理（如长程多轮协作）且不愿自行维护 session 存储；调用方无法稳定持有有效 `api_key`；需跨地域容灾调用（当前 endpoint 绑定单地域） | 注意输入 token 上限（32768）；工作流中 `parameters` 可能被节点级配置覆盖；流式响应需客户端主动处理 SSE |
| **应用发布与分享 API** | 需要**快速交付终端用户可用界面**（Web App）；构建**可复用能力资产**（Component）；将应用作为**标准化服务契约**对外暴露（OpenAPI） | 需要深度定制前端交互逻辑（如复杂 Canvas 编辑器）；需发布到非百炼托管环境（如私有云 K8s）；需支持动态模型切换（发布后模型绑定即固化） | `web_app` 不支持全球加速；`component` Schema 变更不自动同步；`api` 发布默认关闭流式，需显式启用 |
| **应用监控 API** | 需要**生产环境可观测性基线**；进行成本优化审计（Token 效率分析）；建立 SLO/SLI 体系（如成功率 ≥99.9%） | 用于亚秒级故障实时告警（存在 ≤60s 延迟）；监控用户自建中间件（需自行埋点）；需要自定义指标（如业务转化率）与模型指标关联分析 | 必须在控制台手动开启「启用应用观测」；高吞吐下需用 `env` 标签分流采样；流式未消费完可能导致输出 token 漏计 |
| **应用权限管理 API** | 需要**符合企业合规要求**（如 SOC2、等保）；实施最小权限原则；支持多团队协作（研发/测试/运维/合作方）；需审计权限变更历史 | 临时调试场景（可直接使用主账号）；小型项目无明确分工；需基于应用内容（如 `input.query` 关键词）做动态授权（RAM 不支持内容级条件） | 权限变更最长 5 分钟生效；`DeleteApplication` 已废弃，应使用 `ArchiveApplication`；Web 共享链接 Token 独立于 RAM 体系 |

---

## 技术选型参考指南（面向开发者）

- **优先组合使用，而非单点替代**：  
  典型生产链路 = `发布 API`（交付服务契约） → `调用 API`（集成消费） → `监控 API`（保障质量） → `权限 API`（管控风险）。四者构成闭环，缺一不可。

- **关注“谁在调用”与“调用什么”**：  
  - 若调用方是**自有后端服务** → 重点评估 `调用 API` 的错误重试、流式兼容性、token 截断策略；  
  - 若调用方是**前端浏览器** → 优先选用 `发布为 web_app`（规避 CORS 与密钥泄露风险），而非直连 `调用 API`；  
  - 若调用方是**低代码平台** → `发布为 component` 是最佳实践，获得 Schema 校验与可视化绑定能力。

- **警惕隐式依赖与版本漂移**：  
  - `发布 API` 创建的 `component` 不自动同步源应用 Schema 变更 → 建议在 CI/CD 流程中加入 Schema 兼容性检查；  
  - `监控 API` 数据延迟影响实时诊断 → 高敏感业务需在应用层补充关键路径日志（如 `start_inference`/`end_inference` 时间戳）；  
  - `权限 API` 的 `Resource` ARN 严格绑定地域 → 多地域部署需为每个地域单独配置策略。

- **计费与性能的协同优化**：  
  利用 `监控 API` 的 Token 成本报表，反向指导 `调用 API` 的 `parameters.max_tokens` 设置与 `发布 API` 的 `ui_config` 输入框长度限制，从源头降低无效消耗。

- **安全红线必须遵守**：  
  - 永远不要在前端硬编码 `api_key`；Web 场景务必使用 `web_app` 或后端代理；  
  - `权限 API` 中禁止使用 `Resource: "*"` 生产策略；应精确到 `application/<app-id>`；  
  - `发布 API` 的 `access_control.auth_mode: public` 仅适用于完全公开服务，敏感应用必须设为 `invite_only` 或 `private`。

> **最后建议**：新项目启动时，应同步规划四类 API 的接入——在首个应用开发完成时，即完成发布配置、监控开关启用、最小权限策略部署，并编写调用 SDK 封装层。这将显著降低后期运维复杂度，避免“上线即救火”。

## 被对比主题页

- [bailian application calling](../guides/bailian-application-calling.md)
- [application publishing and sharing](../guides/application-publishing-and-sharing.md)
- [application monitoring](../guides/application-monitoring.md)
- [application permission management](../guides/application-permission-management.md)


