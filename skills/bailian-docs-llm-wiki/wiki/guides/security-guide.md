# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、[记忆](../concepts/memory.md)与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外接入；高级防护则需服务授权后开通，提供策略配置与风险监测能力。安全体系围绕「量·发现与盘点—挡·拦截与防护—记·审计与留痕」形成闭环，保护提示词、内容、工具调用、知识库与[记忆](../concepts/memory.md)等关键资产。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景深度集成，当前支持以下模块的防护：

- **Flow Agent**：输入/输出内容安全检测（含提示词注入识别）  
- **Managed Agent**：运行时行为安全，包括沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：知识库内容安全，含上传文件预扫描、数据投毒检测  
- **Memory**：[记忆](../concepts/memory.md)读写内容安全检测  
- **Store（MCP/Skill）**：Skill 组件供应链静态扫描、恶意代码与风险依赖检测  

> **注意**：文档 5 中“防护范围”表格明确将 `Managed Agent` 列为支持“运行时行为安全”，但文档 6 的“统计规则”仅将 Managed Agent 的发布态与归档态纳入资产盘点，未涵盖草稿态；而 Flow Agent 明确包含草稿态。该差异表明资产盘点范围与实际防护范围不完全对齐，建议以防护总览中实时展示的“已自动防护 X 个 Agent”为准 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)。

## 关键参数

- **防御席位（Agent Defense Seat）**：计费与策略生效的基本单位，定义为“处于运行中且启用高级防护的 Agent 实例”。非运行态 Agent 不产生席位费用，也不触发高级策略检测。  
- **Credit**：高级防护的内容检测配额单位，默认 300 Credits/席位/日，按 [Token](../concepts/token.md) 量换算消耗，有效期 24 小时，不可结转。  
- **风险等级（High/Medium/Low）**：由风险置信度与危害程度联合研判生成，用于风险与审计页面的筛选与优先级排序 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)。  
- **全局策略作用域**：所有安全策略配置对账号下全部 Agent 全局生效，**不区分业务空间**，修改前须评估跨业务影响 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)。

## 使用方式

### 控制台操作
- **默认防护**：无需开通，Agent 接入 RAG、启用 Memory 或部署 Managed Agent 后自动激活。入口见控制台 **Security > 默认防护 > 防护总览**。  
- **高级防护**：需完成服务授权。入口为 **Security > 高级防护 > 安全策略** → 点击“立即开通”，同意协议并确认角色授权（如 `AliyunServiceRoleForSFMSecurity`）。开通后默认启用前 6 项策略，“内容安全”需手动开启。  
- **风险排查**：通过 **Security > 高级防护 > 风险与审计** 查看全账号风险事件，支持按等级、节点类型（Agent/模型/工具/知识库等）筛选，并可导出告警记录。

### CLI 工具
安装百炼 CLI 并完成鉴权后，可执行：
```bash
bl agents security overview        # 查询防护统计与资产分布
bl agents security alerts --risk-level high  # 查询高风险告警
```
完整命令参考见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

### API 集成
Security 模块提供 7 个 RESTful 接口，路径前缀 `/api/v1/agentstudio/security`，支持程序化获取防护总览、资产摘要、策略状态及告警列表（含分页游标）。响应结构统一，失败时返回 `errorCode` 与 `errorMsg` [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)。

## 限制和注意事项

- **默认防护无开关控制**：基础能力（如内容安全 I/O 拦截、上传文件预扫描）随模块使用自动启用，无法关闭；若已发起自建内容安全审批，该能力将显示为“关闭”，但其他默认防护项仍生效。  
- **高级防护暂不支持自动阻断**：当前所有 7 项安全策略仅提供风险监测与告警，**不执行自动拦截或阻断动作**，需人工在风险与审计页面处理 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)。  
- **资产盘点范围有限**：仅纳管百炼原生或托管的 Flow Agent 与 Managed Agent；外部接入的 Agent 不会被识别为资产，亦不纳入防护统计。  
- **限时免费阶段**：高级防护目前免费，但将于 2026 年 9 月后按“防御席位费 + 超额 Credits”计费，正式收费前平台将提前至少一个月通知 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)。  
- **审计日志不分业务空间**：风险与审计页面展示全账号数据，不支持按业务空间过滤，需结合 Agent 名称字段人工区分。

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/security.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)


