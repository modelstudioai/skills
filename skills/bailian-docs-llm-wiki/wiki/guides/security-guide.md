# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外开通；高级防护需完成服务授权后启用，当前处于限时免费阶段。安全能力通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」形成闭环，保护提示词、内容、工具调用、知识库与记忆等关键资产。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景深度集成，支持以下模块的原生防护：

- **Flow Agent**：输入/输出内容安全检测（含提示词与模型响应）  
- **Managed Agent**：运行时行为安全，包括沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：知识库内容安全，含上传文件预扫描、知识库内容检测与 RAG 数据投毒识别  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：供应链静态扫描，检测恶意代码、风险依赖与组件安全问题  

> **注意**：文档 5 中“防护范围”明确将 `Managed Agent` 列为支持运行时行为安全，但文档 6 的“统计规则”仅将 Managed Agent 的发布态与归档态纳入资产统计，未涵盖草稿态；而 Flow Agent 明确包含草稿态。该差异表明资产盘点与防护生效范围存在粒度不一致，建议以实际运行态为准，开发调试阶段仍需关注草稿态风险。  
> 文档 8 和文档 12 均指出高级防护当前**不支持自动阻断或拦截风险**，仅提供监测与告警能力，这与文档 2 中“挡 · 拦截与防护”的表述存在语义偏差——此处“拦截”特指默认防护层的实时阻断（如内容安全 I/O 拦截），高级防护层暂无阻断能力。详见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)。

## 关键参数

| 参数类别 | 名称 | 说明 | 来源 |
|----------|------|------|------|
| **计费单元** | Agent 防御席位 | 一个处于运行中且启用高级防护的 Agent 实例，按小时计费 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **资源配额** | Credit | 每席位每日默认 300 Credits，按检测内容 [Token](../concepts/token.md) 量换算消耗；超限部分按 0.0015 元/Credit 计费 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **API 路径前缀** | `/api/v1/agentstudio/security` | 所有 Security 模块接口统一前缀，含 `/overview`、`/asset_summary`、`/policies` 等共 7 个接口 | [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md) |
| **CLI 命令** | `bl agents security overview`<br>`bl agents security alerts` | 查询防护统计与风险告警的核心 CLI 命令，支持 `--risk-level` 等过滤参数 | [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md) |

## 使用方式

### 控制台操作
- **默认防护**：无需操作，Agent 使用 RAG、Memory 或 Managed Agent 等模块后自动启用。入口见控制台 **Security > 默认防护 > 防护总览** 或 **Agent 资产**。  
- **高级防护**：需先完成服务授权。入口为 **Security > 高级防护 > 安全策略** → 点击 **立即开通**，同意协议并创建服务关联角色（如 `AliyunServiceRoleForSFMSecurity`）。开通后默认启用前 6 项策略，“内容安全”需手动开启。  

### CLI 快速查询
```bash
bl agents security overview          # 查看防护全景与拦截统计
bl agents security alerts --risk-level high  # 获取高风险告警列表
```
所有命令支持 `--help` 查看完整参数。CLI 依赖已安装并鉴权的百炼 CLI，详见 [阿里云百炼 CLI 安装与鉴权](https://help.aliyun.com/zh/model-studio/cli/installation)。

### API 集成
Security 提供 7 个 RESTful 接口，全部返回标准 JSON 结构（`{"success": true, "data": {...}}`）。关键接口包括：
- `GET /api/v1/agentstudio/security/overview`：获取防护总览（无分页）  
- `GET /api/v1/agentstudio/security/asset_summary`：获取 Agent 资产摘要  
- `GET /api/v1/agentstudio/security/agent_logs`：分页查询风险告警（游标分页）  
详细参数与错误码见 [Security API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 限制和注意事项

- **全局策略作用域**：安全策略配置对账号下**全部 Agent 全局生效**，不区分业务空间。修改前须评估影响范围，避免误关关键防护项。  
- **资产统计范围**：Agent 资产页面仅统计百炼纳管的 Flow Agent（草稿+发布态，但重复时仅计发布态）与 Managed Agent（发布+归档态），**不包含外部接入的 Agent**，也不支持当前版本下钻查看节点详情。  
- **高级防护能力边界**：当前高级防护仅提供风险监测与审计能力，**不支持自动处置、阻断或修复**。风险事件需人工确认处理（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 页面“操作”列）。  
- **数据时效性**：防护总览页面数据约每 2 分钟刷新一次；审计日志与风险事件为异步检测结果，可能存在数秒至数分钟延迟。  
- **权限依赖**：开通高级防护需自动创建多个服务关联角色（如 `AliyunServiceRoleForSasAI`），开通前必须同意《百炼安全服务关联角色授权》，否则无法完成授权流程。

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
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)


