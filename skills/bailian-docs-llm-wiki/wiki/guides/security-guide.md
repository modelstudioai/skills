# security guide

百炼平台为 Agent 提供内生、开箱即用的[安全防护](../concepts/security.md)能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效，无需额外配置；高级防护需完成服务授权后按需开通，支持策略化风险监测与审计追溯。整体形成「量 → 挡 → 记」三层安全闭环。

## 支持的模型/功能

百炼安全能力按防护对象与阶段分为两类：

- **默认防护（原生、免费）**：面向所有使用百炼 Agent Studio 的用户自动启用，覆盖以下 Agent 类型及模块：
  - `Flow Agent`：输入/输出内容安全检测  
  - `Managed Agent`：运行时行为安全（沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理）  
  - `RAG`：知识库内容安全（上传文件预扫描、内容检测）  
  - `Memory`：记忆读写内容安全检测  
  - `Store`：MCP/Skill 组件安全（供应链静态扫描、风险依赖检测）  
  > **注意**：文档 3 明确说明“默认防护随 Agent 使用对应模块自动生效”，而文档 8 中“使用须知”也强调“无需额外开通”；但文档 6 称高级防护“暂不支持自动阻断或拦截风险”，该描述易引发歧义——实际指**高级防护本身不提供拦截动作**，而默认防护中的内容安全、文件预扫描等能力仍具备实时拦截能力。请以[防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)中“风险拦截”卡片的实际拦截统计为准。

- **高级防护（限时免费，后续按量计费）**：需在控制台完成服务授权后开通，全局作用于账号下全部 Agent，当前提供 7 项可独立启停的策略：
  - 提示词攻击、敏感数据外泄、工具调用安全、RAG 数据投毒、知识库与记忆窃取、身份与安全凭证、内容安全（此项需手动开启）  
  全部策略仅提供**风险监测与告警**，不执行自动阻断（见[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)说明）。

## 关键参数

| 参数类别 | 说明 | 来源 |
|----------|------|------|
| **风险等级** | 高/中/低三级，由风险置信度与危害程度联合研判生成，用于筛选与优先级排序 | [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) |
| **Credit 消耗** | 高级防护用量计量单位，1 Credit ≈ 对应 [Token](../concepts/token.md) 量的内容检测消耗；每个席位每日默认 300 Credits，超额部分计费 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **席位（Seat）** | 指处于运行状态且启用高级防护的 Agent 实例；仅运行中计费，停用或未启用时不产生费用 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |

## 使用方式

- **控制台操作**：
  - 默认防护：无操作入口，随 Agent 使用模块自动激活；可通过 **Security > 默认防护 > 防护总览** 或 **Agent 资产** 查看状态与拦截统计。
  - 高级防护：进入 **Security > 高级防护 > 安全策略**，点击“立即开通”完成服务授权（需同意协议并创建关联角色），开通后可调整各策略开关。

- **CLI 工具**：
  - 安装并配置百炼 CLI 后，可执行：
    ```bash
    bl agents security overview          # 查询防护统计与资产分布
    bl agents security alerts --risk-level high  # 查询高风险告警
    ```
  - 所有命令支持 `--help` 查看完整参数，详见[使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

- **API 集成**：
  - Security 模块提供 7 个 RESTful 接口，路径前缀 `/api/v1/agentstudio/security`，包括 `/overview`、`/asset_summary`、`/policies`、`/agent_logs` 等；
  - 响应结构统一，失败时返回 `{"success": false, "errorCode": "...", "errorMsg": "..."}`；
  - 详细参数与认证方式见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)。

## 限制和注意事项

- **作用域限制**：
  - 默认防护按业务空间（workspace）隔离，统计与拦截数据归属对应空间；
  - 高级防护策略配置对**账号下全部 Agent 全局生效**，不区分业务空间（见[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)说明）；
  - [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 页面同样不区分业务空间，展示账号级全量风险与日志。

- **功能限制**：
  - 当前高级防护**不支持自动处置风险**（如阻断请求、隔离 Agent），仅提供监测、告警与审计能力；
  - Agent 资产页面暂不支持下钻查看 Agent 列表与节点详情（见[Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)说明）；
  - 内容安全能力若已通过自建审批流程，则页面显示为“关闭”，此时百炼原生内容检测将不再生效。

- **计费与开通**：
  - 高级防护当前处于**限时免费阶段（截至 2026 年 9 月）**，正式计费前将提前一个月通知；
  - 开通需创建多个服务关联角色（如 `AliyunServiceRoleForSFMSecurity`），权限范围涵盖 AI 安全中心与云安全中心（CSPM）等，开通即视为同意相关协议。

## 来源文档

- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)


