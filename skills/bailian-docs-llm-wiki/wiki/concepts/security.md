# 安全防护

安全防护是百炼平台内生、分层、可编程的主动式安全能力体系，覆盖 Agent 全生命周期的关键资产（提示词、内容、工具调用、知识、记忆、代码依赖等），通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」闭环实现风险可知、可防、可溯。

## 在百炼平台的不同场景中，这个概念如何使用

安全防护不是单一功能，而是按场景深度集成的默认能力与可扩展的高级能力组合：

- **Flow Agent**：输入/输出内容自动检测（含提示词注入、模型响应越界），无需配置即生效；支持通过 `X-DashScope-DataInspection` 请求头增强检测粒度。
- **Managed Agent**：运行时沙箱隔离 + 工具调用拦截（如 `bash` 命令白名单/审批）+ 凭证隔离 + Session 生命周期治理，所有行为受 Agent 身份绑定管控。
- **RAG**：知识库上传时预扫描（恶意文件、敏感信息）+ 检索内容实时检测（防止知识投毒），检测结果影响召回片段可用性。
- **Memory**：读写记忆内容前强制安全检测，阻断高风险记忆写入或污染性记忆读取。
- **Store（MCP/Skill）**：对上传的 Skill ZIP 包、MCP 插件进行静态代码扫描（含依赖漏洞、恶意[函数调用](function-calling.md)），未通过扫描无法挂载。
- **模型调用层**：通过传输加密（AES+RSA）、私网访问（PrivateLink 或安全存储业务空间）、AI 安全护栏（输入/输出 CIP 检测）提供基础设施级防护。

> ⚠️ 注意：默认防护自动启用，但若已通过自建内容安全审批流程，则对应项在控制台显示为“关闭”；此时仍可通过高级防护独立开启内容安全策略。

## 关键参数和配置

| 参数 | 说明 | 开发者操作要点 |
|------|------|----------------|
| **防御席位（Defense Seat）** | 一个启用高级防护且处于运行中的 Agent 实例；仅运行时计费 | 无需代码配置，控制台开通高级防护后，Agent 发布即占用席位；停用或下线可释放 |
| **Credit 额度** | 每席位每日 300 Credits（1 Credit ≈ 100 tokens），超限按 0.0015 元/Credit 计费 | 无 API 控制开关；可通过 CLI `bl agents security overview` 监控消耗趋势 |
| **风险等级（high/medium/low）** | 由风险置信度与危害程度联合判定，用于告警分级与处置优先级 | 告警接口（`/agent_logs`）支持 `--risk-level high` 过滤，推荐在自动化巡检中优先处理 high 级别事件 |
| `X-DashScope-DataInspection` | HTTP Header，启用输入/输出内容安全检测 | 值为 JSON 字符串，如 `'{"input":"cip","output":"cip"}'`；适用于所有 DashScope 文本/图像模型调用 |
| `enable_encryption=True` | SDK 参数（Python/Java），启用端到端 AES-256 加密传输 | 自动获取公钥、生成密钥、加密封装；敏感数据场景必开，无需手动管理密钥 |
| `prompt_attack`, `rag_poisoning` 等策略名 | `/policies` 接口返回的 11 条策略标识符 | 高级防护策略全局生效，修改前需评估影响；`baseline_check` 和 `vulnerability_scan` 为免费策略，始终启用 |

## 面向开发者，简洁实用

- ✅ **快速启用**：默认防护零配置；高级防护只需控制台一键开通（限时免费），CLI 或 API 可立即查询状态。
- ✅ **精准控制**：  
  - 内容安全：用 `X-DashScope-DataInspection` 按需开启/关闭某次请求的检测；  
  - 传输安全：SDK 一行代码 `enable_encryption=True` 即完成加密接入；  
  - 私网访问：标准场景配 PrivateLink 终端节点，强合规场景选安全存储业务空间。
- ✅ **可观测可集成**：  
  - 所有安全事件通过 `/agent_logs`（告警列表）和 `/agent_logs/{alert_id}`（完整上下文）API 暴露；  
  - 支持导出（`/export_agent_logs`）对接 SIEM 或内部审计系统；  
  - CLI 命令 `bl agents security alerts --risk-level high` 可嵌入 CI/CD 流水线做发布前检查。
- ❌ **注意边界**：高级防护当前**仅提供风险监测与告警，不支持自动拦截或阻断**；如需阻断逻辑，需在应用层基于告警结果自行实现熔断或降级。

> 💡 提示：安全策略对账号下**全部 Agent 全局生效**，不区分业务空间。生产环境修改前，请先在测试账号验证策略效果。

## 关联主题页

- [security guide](../guides/security-guide.md)
- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [llm application](../guides/llm-application.md)
- [application call](../api/application-call.md)
- [managed agents](../guides/managed-agents.md)


