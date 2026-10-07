# security guide

百炼平台为 Agent 提供内生、开箱即用的[安全防护](../concepts/security.md)能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效，无需额外开通；高级防护则需完成服务授权后按需启用，当前处于限时免费阶段。安全能力通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」闭环实现，支撑资产识别、风险拦截与事件回溯。

## 支持的模型/功能

Security 模块原生支持以下 Agent 类型及关联能力：

- **Flow Agent**：输入/输出内容安全检测（含提示词注入识别）、知识库与记忆内容安全（当接入 RAG 或 Memory 时自动触发）  
- **Managed Agent**：运行时行为安全，包括沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：上传文件预扫描、知识库内容投毒检测（高级防护启用后）  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：供应链静态扫描（检测恶意代码、风险依赖）  

> **注意**：文档 6 中称“默认防护随 Agent 使用自动生效”，而文档 8 明确指出“高级防护暂不支持自动阻断或拦截风险”，二者逻辑一致；但文档 10 的“风险与审计”说明中强调“只有开通了安全策略防护，风险与审计模块才会有数据”，这与文档 4 中“审计留痕”作为三大支柱之一的表述存在表层矛盾——实际含义是：**默认防护可记录基础日志，但完整风险事件（含等级、节点、Trace）仅在高级防护开通后生成**。详见 [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)。

## 关键参数

| 参数 | 说明 | 来源 |
|------|------|------|
| `--risk-level` | CLI 命令中指定风险等级过滤（如 `high`/`medium`/`low`），用于 `bl agents security alerts` | [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md) |
| `available: false` | API 响应中表示某项能力当前不可用（如未开通高级防护时 `/policies` 返回策略列表但 `enabled: false`），不触发整体失败 | [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md) |
| Credit 消耗 | 按被检测内容 [Token](../concepts/token.md) 数换算，每席位每日默认 300 Credits，超额部分按 0.0015 元/Credit 计费 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |

## 使用方式

### 控制台入口
- **默认防护**：导航至 **Security > 默认防护 > 防护总览** 或 **Agent 资产**，查看实时拦截统计与资产分布  
- **高级防护**：导航至 **Security > 高级防护 > 安全策略** 开通服务并配置策略；开通后，风险事件与审计日志统一展示于 **Security > 高级防护 > 风险与审计**（该页面跨业务空间，展示账号下全部 Agent 数据）

### CLI 工具
安装并鉴权阿里云百炼 CLI 后，可执行：
```bash
bl agents security overview          # 查询防护统计与资产分布
bl agents security alerts --risk-level high  # 查询高风险告警
```
所有命令支持 `--help` 查看完整参数，详细参考见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

### API 接入
Security 提供 7 个 RESTful 接口，前缀 `/api/v1/agentstudio/security`，关键接口包括：
- `GET /overview`：获取防护总览（无分页）  
- `GET /asset_summary`：获取资产摘要（无分页）  
- `GET /agent_logs`：分页查询告警列表（游标分页）  
- `POST /export_agent_logs`：导出告警记录  

响应结构统一，失败时返回 `{"success": false, "errorCode": "...", "errorMsg": "..."}`。

## 限制和注意事项

- **全局生效性**：安全策略配置对账号下**全部 Agent 全局生效**，不区分业务空间；修改前须评估影响范围（见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）。  
- **Agent 纳管范围**：仅 Flow Agent（发布态）与 Managed Agent（发布态/归档态）纳入资产盘点；外部未接入百炼纳管的 Agent 不会被识别（见 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）。  
- **高级防护能力边界**：当前版本**不支持自动阻断风险**，仅提供监测、告警与审计能力；处置需人工介入（见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md) 和 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。  
- **数据延迟**：防护总览页面数据约每 2 分钟刷新一次，非实时（见 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)）。  
- **服务授权依赖**：开通高级防护需自动创建多个 `AliyunServiceRoleFor*` 关联角色，开通前须同意《百炼安全服务关联角色授权》（见 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）。

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)


