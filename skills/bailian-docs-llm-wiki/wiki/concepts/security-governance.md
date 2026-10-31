# 安全与治理

安全与治理是百炼平台面向 AI 应用全生命周期构建的统一防护与合规管控体系，涵盖数据安全、内容风控、访问控制、行为审计、策略执行与合规备案等核心能力。它不是单一功能模块，而是贯穿模型调用、Agent 运行、应用部署及运维审计各环节的横切能力集合，通过 API 参数、运行时配置与控制台策略三层协同实现可编程、可观测、可审计的治理实践。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用层**：默认启用输入/输出内容安全检测（如敏感词、涉政、暴恐、色情识别），可通过 `enable_content_safety`（布尔值）和 `content_safety_level`（`strict`/`balanced`/`relaxed`）精细调控；私网访问（VPC）、TLS 1.2+ 传输加密、RBAC 权限控制为所有模型通用底座能力。  
- **Agent 运行层**：需显式启用 `governance_config` 对象，按模块启用安全防护（`security`）与行为进化评估（`evolution`）。仅 `qwen-max` 和 `qwen-plus` 支持完整能力（含工具调用白名单、执行沙箱、响应重写）；`qwen-turbo` 仅支持基础输出过滤。注意：必须搭配 `agent_runtime_v2` 运行时，`v1` 不兼容。  
- **安全运营与审计层**：通过 Security API 统一获取工作空间维度的安全态势——包括防护总览（`/overview`）、Agent 资产分布（`/asset_summary`）、11 条预置策略启用状态（`/policies`，按 `risk_domain` 分为模型交互、运行环境、知识记忆、身份凭证、配置组件五类），以及告警全生命周期管理（`/agent_logs` 查询、`/export_agent_logs` 异步导出）。所有接口均基于工作空间 ID 与 `cn-beijing` 地域拼装 Endpoint，需 API Key 鉴权。  
- **应用合规层**：面向中国大陆公众服务的 AI 应用，需完成模型备案信息公示（只读接口 `GET /v1/model/filing`）与应用合规备案（通过阿里云合规门户人工审核），该能力不开放 API 提交，但备案状态直接影响服务上线流程。

## 关键参数和配置

| 参数名 | 所属场景 | 类型 | 必填 | 说明 |
|--------|----------|------|------|------|
| `enable_content_safety` | 模型调用 | bool | 否（默认 `true`） | 控制是否启用输入/输出内容安全检测；不可关闭，仅可调节强度 |
| `content_safety_level` | 模型调用 | string | 否（默认 `balanced`） | 取值 `strict`/`balanced`/`relaxed`；影响检测覆盖率与误拦率，部分模型不支持全部档位 |
| `vpc_endpoint` | 模型调用 | string | 否 | 私网访问域名，需在控制台提前绑定 VPC；启用后自动绕过公网，提升传输安全性 |
| `governance_config` | Agent 运行 | object | 否 | 治理策略根对象，最大 8KB；子字段见下 |
| `governance_config.security.enable_input_filter` | Agent 运行 | bool | 否（默认 `false`） | 启用输入内容过滤（如 blocklist 匹配） |
| `governance_config.security.enable_output_filter` | Agent 运行 | bool | 否（默认 `false`） | 启用输出内容过滤（如敏感词拦截、响应重写） |
| `governance_config.security.blocklist` | Agent 运行 | string[] | 否 | 自定义屏蔽词数组，建议精简合并以降低延迟（启用后平均 +120–350ms） |
| `governance_config.evolution.eval_template_id` | Agent 运行 | string | 是（若启用 `evolution`） | 引用预置的 Evolution 评估模板 ID；空值将导致 `400 Bad Request` |
| `governance_config.evolution.eval_interval` | Agent 运行 | integer | 否（默认 `1`） | 每 N 轮对话触发一次行为评估（仅 `stream=false` 时生效） |
| `Authorization: Bearer <api-key>` | Security API | header | 是 | 所有 Security API 请求必需，格式严格为 `Bearer <your-api-key>` |
| `workspace_id` & `region` | Security API | host | 是 | Endpoint 主机名组成部分，例如 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com`；`region` 当前仅支持 `cn-beijing` |

> ⚠️ 注意事项：  
> - `enable_content_safety` 为强制开启项，关闭参数无效；实际生效依赖底层模型能力，非所有模型支持 `content_safety_level` 调整。  
> - `governance_config` 为覆盖式更新，不支持局部 patch；动态调整需调用 `update_agent` 并传入完整对象。  
> - Security API 的 `/agent_logs` 支持多值筛选，使用 `status_list=["unhandled","intercepted"]`（数组），而非单值 `status` 字符串；其他文档存在参数名不一致，请以本页为准。  
> - 所有安全与治理能力均默认按最小权限原则设计，生产环境请务必通过 RAM 策略授予 `AliyunBailianFullAccess` 或自定义精细化权限。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [agent governance](../guides/agent-governance.md)
- [application support](../guides/application-support.md)


