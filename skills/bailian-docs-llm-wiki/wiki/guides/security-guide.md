# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外开通；高级防护需完成服务授权后启用，当前处于限时免费阶段。安全能力通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」闭环，持续保护提示词、内容、工具调用、知识与记忆等关键资产。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景分层覆盖，**默认防护**已深度集成至以下模块：

- **Flow Agent**：输入/输出内容安全检测（含提示词与模型响应）  
- **Managed Agent**：运行时行为安全，包括沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：知识库内容安全，支持上传文件预扫描与知识内容检测  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：供应链静态扫描，检测恶意代码与风险依赖  

> **注意**：文档 5（[防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)）明确说明“如已发起并完成自建内容安全审批，内容安全项将显示为‘关闭’”，而文档 8（[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）指出高级防护中的“内容安全”策略需手动开启。二者逻辑一致——自建审批会覆盖默认内容安全检测，此时该能力在防护总览中不可见，但高级防护仍可独立启用。

所有防护能力均基于 Agent 身份签发实现资产绑定与权限管控，身份标识是资产盘点与审计溯源的基础。

## 关键参数

| 参数类别 | 说明 | 来源依据 |
|----------|------|-----------|
| **防御席位** | 指一个处于运行中且启用了高级防护的 Agent 实例；仅运行时计费，停用或未运行不产生费用 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **Credit 额度** | 每席位每日默认 300 Credits，按 Token 量换算消耗；额度不跨日结转，超限部分按 0.0015 元/Credit 计费 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **风险等级** | 高/中/低三级，由风险置信度与危害程度联合研判生成，用于筛选与优先级排序 | [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) |

## 使用方式

### 控制台操作
- **默认防护**：无需配置，Agent 使用 RAG、Memory 等模块后自动启用。入口：控制台 → **Security** → **默认防护 > 防护总览** 或 **Agent 资产**  
- **高级防护**：需先完成服务授权。入口：控制台 → **Security** → **高级防护 > 安全策略** → 点击 **立即开通**（默认开通前 6 项策略，内容安全需手动开启）  
- **风险分析**：开通高级防护后，访问 **高级防护 > 风险与审计** 查看全账号风险事件与审计日志  

### CLI 工具
安装并鉴权百炼 CLI 后，可执行以下命令：
```bash
bl agents security overview        # 查询防护统计与资产分布
bl agents security alerts --risk-level high  # 查询高风险告警
```
完整命令参考见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

### API 接入
Security 模块提供 7 个 RESTful 接口，路径前缀 `/api/v1/agentstudio/security`，支持查询防护总览、资产摘要、策略状态及导出告警。全部接口返回统一结构，错误码详见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)。

## 限制和注意事项

- **全局策略作用域**：安全策略配置对账号下**全部 Agent 全局生效**，不区分业务空间；修改前须评估影响范围（见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）。  
- **高级防护能力边界**：当前高级防护**仅支持风险监测与告警，不支持自动阻断或拦截**（见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md) 和 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。  
- **资产统计规则**：Flow Agent 仅统计发布态（草稿态不计入），Managed Agent 统计发布态与归档态；外部非纳管 Agent 不会被识别为资产（见 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）。  
- **审计数据范围**：风险与审计页面展示**全账号**数据，不按业务空间隔离；且仅在开通高级防护后才产生风险记录（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。  
- **时效性**：防护总览数据约每 2 分钟刷新一次，非实时；CLI 与 API 返回结果为当前快照，无延迟承诺。

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)


