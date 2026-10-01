# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效，无需额外开通；高级防护则需完成服务授权后按需启用，当前处于限时免费阶段。安全能力通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」形成闭环，保护提示词、内容、工具调用、知识与记忆等关键资产。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景分层覆盖，所有防护均基于平台原生集成，不依赖外部插件或 SDK：

- **Flow Agent**：输入/输出内容安全检测（含提示词攻击识别）、记忆读写内容安全  
- **Managed Agent**：运行时沙箱隔离、工具调用拦截、凭证隔离、Session 生命周期治理  
- **RAG**：上传文件预扫描、知识库内容安全检测、RAG 数据投毒检测（高级防护）  
- **Memory**：记忆内容安全检测、知识库与记忆窃取检测（高级防护）  
- **Store（MCP/Skill）**：供应链静态扫描（恶意代码、风险依赖）、组件安全检测  

> **注意**：文档 7 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md) 明确指出“当前高级防护主要支持策略配置与风险监测，暂不支持自动阻断或拦截风险”，而文档 3 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md) 中“风险拦截”卡片描述了“拦截次数为累计值”，二者存在表述差异——实际拦截行为仅发生在默认防护层（如内容安全 I/O 拦截），高级防护目前仅生成风险事件供审计，不触发实时阻断。

## 关键参数

| 参数类别 | 说明 | 来源 |
|----------|------|------|
| **风险等级** | 高/中/低三级，由风险置信度与危害程度联合研判生成，用于筛选与优先级排序 | [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) |
| **Credit 消耗** | 高级防护用量计量单位，1 Credit ≈ 对应 Token 量的内容检测消耗；每个席位每日默认 300 Credits，超量按 0.0015 元/Credit 计费 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **Agent 席位** | 指“处于运行中且启用高级防护”的 Agent 实例，按小时计费（0.42 元/席位·小时）；未运行时不计费 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |

## 使用方式

### 控制台操作
- **默认防护**：无需操作，Agent 使用 RAG、Memory 等模块后自动启用（见 [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)）  
- **高级防护开通**：导航至 **Security > 高级防护 > 安全策略** → 点击 **立即开通** → 同意协议并确认授权（自动创建 `AliyunServiceRoleForSFMSecurity` 等角色）  
- **策略调整**：开通后在安全策略页手动开启/关闭 7 项策略（**内容安全**需单独开启）  

### CLI 调用
安装并鉴权后，使用以下命令快速获取安全数据：
```bash
bl agents security overview          # 查询防护统计与资产分布
bl agents security alerts --risk-level high  # 查询高风险告警
```
完整命令参考见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

### API 集成
Security 模块提供 7 个 RESTful 接口，前缀 `/api/v1/agentstudio/security`，支持：
- `GET /overview`：防护总览（无分页）  
- `GET /asset_summary`：Agent 资产摘要（无分页）  
- `GET /agent_logs`：告警列表（游标分页）  
- `POST /export_agent_logs`：导出告警记录  
详细参数与错误码见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)。

## 限制和注意事项

- **全局策略作用域**：安全策略配置对账号下**全部 Agent 全局生效**，不区分业务空间；修改前须评估影响范围（见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）。  
- **资产统计规则**：仅纳管 Flow Agent（发布态）与 Managed Agent（发布态+归档态）；外部 Agent 不计入资产清单（见 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）。  
- **高级防护能力边界**：当前版本**不支持自动处置风险**（如阻断请求、隔离 Agent），仅提供风险事件与审计日志；风险处理需人工介入（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。  
- **数据时效性**：防护总览页面数据约每 2 分钟刷新一次，非实时；风险与审计数据延迟通常 ≤ 5 分钟。  
- **服务授权依赖**：开通高级防护需创建多个服务关联角色（如 `AliyunServiceRoleForSasAI`），若账号权限不足将导致开通失败（错误码 `12000092`，见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)）。

## 来源文档

- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)


