# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、[记忆](../concepts/memory.md)与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外接入；高级防护则需服务授权后开通，提供可配置的策略与风险监测能力。安全机制通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」形成闭环，保护提示词、内容、工具调用、知识库与[记忆](../concepts/memory.md)等关键资产。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景差异化覆盖，不依赖特定模型，而是与平台运行时深度集成：

- **Flow Agent**：输入/输出内容安全检测（含提示词攻击识别）  
- **Managed Agent**：运行时沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：上传文件预扫描、知识库内容安全检测、RAG 数据投毒识别  
- **Memory**：[记忆](../concepts/memory.md)读写内容安全检测  
- **Store（MCP/Skill）**：Skill 组件供应链静态扫描、恶意代码与风险依赖检测  

所有防护均基于百炼统一安全引擎，不区分底层模型（如 Qwen 系列、第三方模型接入等），详见 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md) 中的“防护范围”说明。

> **注意**：文档 4（防护总览）称“内容安全 I/O 拦截”覆盖“Agent 输入和模型输出”，而文档 9（安全策略）将“内容安全”列为第 7 项需手动开启的高级策略，且明确其检测范围包含“上传文件、Agent 输入输出、模型调用输入输出”。二者存在范围重叠但层级不一致——实际应以文档 9 的定义为准：**默认防护已包含基础内容安全（如输入输出合规检测），而高级策略中的“内容安全”是增强版，支持更细粒度规则与自定义敏感词库**。该差异在 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md) 页面有明确说明。

## 关键参数

安全能力的启用与行为受以下关键参数/配置控制：

- **全局策略开关**：安全策略配置对账号下全部 Agent 全局生效，不区分业务空间（见 [概述](../../raw/application-user-guide/security-guide/section-gs/security.md)）  
- **风险等级阈值**：风险事件按置信度与危害程度划分为高/中/低三级，影响告警优先级与审计聚焦（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）  
- **Credit 消耗因子**：高级防护中，Credit 消耗按被检测内容 [Token](../concepts/token.md) 数量换算，长文本或高频调用显著增加用量（见 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）  
- **席位定义**：仅当 Agent 处于运行态且显式启用高级防护时，才产生防御席位费（同上）  

CLI 与 API 均支持参数化查询，例如 `bl agents security alerts --risk-level high` 或 `/agent_logs?risk_level=high`。

## 使用方式

### 控制台操作
- **默认防护**：无需操作，Agent 接入 RAG、启用 Memory 或发布 Managed Agent 后自动激活  
- **高级防护开通**：进入 **Security > 高级防护 > 安全策略**，点击“立即开通”，完成服务授权（需同意协议并创建关联角色）  
- **资产与风险查看**：  
  - 资产盘点：**Security > 默认防护 > Agent 资产**  
  - 风险分析：**Security > 高级防护 > 风险与审计**（注意：此页跨业务空间聚合全部 Agent 数据）  

### CLI 快速查询
安装并鉴权百炼 CLI 后，执行：
```bash
bl agents security overview          # 查看防护总览与资产分布
bl agents security alerts --risk-level high  # 查询高风险告警
```
完整命令参考见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

### API 集成
Security 模块提供 7 个 RESTful 接口，前缀为 `/api/v1/agentstudio/security`，包括：
- `GET /overview`（防护总览）  
- `GET /asset_summary`（Agent 资产摘要）  
- `GET /policies`（当前策略状态）  
- `GET /agent_logs`（分页告警列表）  
响应结构统一，失败时返回 `{"success": false, "errorCode": "...", "errorMsg": "..."}`（见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)）。

## 限制和注意事项

- **默认防护无开关控制**：无法关闭，默认随模块使用自动启用；若已发起自建内容安全审批，内容安全项将显示为“关闭”（见 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)）  
- **高级防护暂不支持自动处置**：当前仅提供风险监测、告警与审计能力，不支持自动阻断或拦截（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 和 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）  
- **资产统计范围限定**：仅纳管 Flow Agent（草稿+发布态，重复时仅计发布态）与 Managed Agent（发布+归档态）；外部 Agent 不计入 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)  
- **限时免费与计费过渡**：高级防护当前处于限时免费阶段，正式计费后将按“防御席位费 + 超额 Credits”模式后付费，开通即自动创建多个服务关联角色（见 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）  
- **数据延迟**：防护总览页面数据约每 2 分钟刷新一次，非实时（见 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)）

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/security.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)


