# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外接入；高级防护则需服务授权后开通，提供策略配置与风险监测能力。整体形成「量·发现与盘点—挡·拦截与防护—记·审计与留痕」的安全闭环。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景差异化覆盖，当前支持以下模块的原生防护：

- **Flow Agent**：输入/输出内容安全检测（含提示词、模型响应）  
- **Managed Agent**：运行时行为安全，包括沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：知识库内容安全，含上传文件预扫描、知识库文本检测  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：Skill 组件供应链静态扫描、恶意代码与风险依赖检测  

> **注意**：文档 5（[防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)）明确列出各模块防护范围，而文档 7（[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）中“RAG 数据投毒”“知识库与记忆窃取”等策略属于**高级防护层**，不等同于默认防护能力——二者在检测深度、响应机制和启用方式上存在本质差异，不可混为一谈。

## 关键参数

- **防护粒度**：默认防护以模块为单位自动启用（如启用 RAG 即触发知识库内容安全）；高级防护策略全局生效，作用于账号下所有 Agent，**不区分业务空间**（见 [概述](../../raw/application-user-guide/security-guide/section-gs/security.md)）。  
- **风险等级**：风险事件按置信度与危害程度划分为高、中、低三档，用于优先级排序与处置决策（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。  
- **Credit 消耗**：高级防护正式计费后，按 [Token](../concepts/token.md) 量换算 Credit，每席位每日默认 300 Credits，超额部分按 0.0015 元/Credit 计费（见 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）。  

## 使用方式

- **默认防护**：无需操作，Agent 使用对应模块（如接入知识库、启用 Memory）后自动生效。  
- **高级防护开通**：在控制台导航栏点击 **Security → 高级防护 > 安全策略**，点击 **立即开通**，完成服务授权（自动创建 `AliyunServiceRoleForSFMSecurity` 等角色）即可启用（默认开通前 6 项策略，内容安全需手动开启）。  
- **CLI 查询**：安装并鉴权百炼 CLI 后，可执行：  
  ```bash
  bl agents security overview      # 查看防护统计与资产分布
  bl agents security alerts --risk-level high  # 查询高风险告警
  ```  
  详见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。  
- **API 集成**：Security 模块提供 7 个 RESTful 接口，路径前缀 `/api/v1/agentstudio/security`，支持查询防护总览（`/overview`）、资产摘要（`/asset_summary`）、策略状态（`/policies`）、告警列表（`/agent_logs`）等（见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)）。

## 限制和注意事项

- **作用域限制**：安全策略配置与风险审计数据均**全局生效或全局可见**，不支持按业务空间隔离（[概述](../../raw/application-user-guide/security-guide/section-gs/security.md) 与 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 均强调此点）。  
- **能力边界**：  
  - 默认防护仅提供实时拦截，不提供风险分析与留痕；  
  - 高级防护当前**仅支持风险监测与告警，不支持自动阻断或处置**（见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）；  
  - 风险与审计页面暂不支持自动处置，仅支持人工处理或忽略（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。  
- **资产识别范围**：仅纳管由百炼托管的 Flow Agent 和 Managed Agent 及其关联资源；外部自建 Agent 不被自动识别为资产（见 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）。  
- **时效性**：防护总览页面数据约每 2 分钟刷新一次；Credit 有效期为 24 小时（自然日），到期不结转（见 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md) 与 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）。

## 来源文档

- [概述](../../raw/application-user-guide/security-guide/section-gs/security.md)
- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)


