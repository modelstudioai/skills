# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外开通；高级防护则需完成服务授权后按需启用，当前处于限时免费阶段。安全能力通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」闭环实现资产可视、风险可控、行为可溯。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景差异化覆盖，不依赖特定模型，而是与平台能力深度耦合：

- **Flow Agent**：输入/输出内容安全检测（含提示词注入识别）、身份签发  
- **Managed Agent**：运行时沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：上传文件预扫描、知识库内容安全检测、RAG 数据投毒识别  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：Skill 供应链静态扫描（恶意代码、风险依赖检测）  

> **注意**：文档 6 明确指出“当前高级防护主要支持策略配置与风险监测，暂不支持自动阻断或拦截风险”，而文档 3 描述防护总览中“内容安全 I/O 拦截”等条目为“拦截”，二者存在表述矛盾。实际行为以控制台实时反馈为准——默认防护具备实时拦截能力，高级防护当前仅提供检测与告警，不执行阻断动作。

## 关键参数

| 参数类别 | 说明 | 来源 |
|----------|------|------|
| **防护范围粒度** | 默认防护按模块（Flow/Managed/RAG/Memory/Store）自动激活；高级防护策略全局生效，作用于账号下全部 Agent，不区分业务空间 | [概述](../../raw/application-user-guide/security-guide/section-gs/security.md) |
| **风险等级** | 分为高、中、低三档，由风险置信度与危害程度联合研判生成 | [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) |
| **Credit 消耗规则** | 高级防护按 Token 换算 Credit，每席位每日默认 300 Credits，超额部分按 0.0015 元/Credit 计费（限时免费期暂不计费） | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **API 响应结构** | 统一返回 `{"success": true/false, "data": {...}}`；单项数据不可用时返回 `null` 或 `available: false`，不影响整体响应 | [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md) |

## 使用方式

### 控制台操作
- **默认防护**：无需操作，Agent 接入 RAG、启用 Memory 或发布 Managed Agent 后自动激活  
- **高级防护开通**：导航至 **Security > 高级防护 > 安全策略** → 点击 **立即开通** → 完成服务授权与协议确认（默认开通前 6 项策略，`内容安全`需手动开启）  
- **资产与风险查看**：  
  - 资产盘点：**Security > 默认防护 > Agent 资产**  
  - 风险分析：**Security > 高级防护 > 风险与审计**（支持按等级、节点类型筛选及 Trace 查看）  

### CLI 工具
安装并鉴权后，使用以下命令快速获取安全数据：
```bash
bl agents security overview      # 查询防护统计与资产分布
bl agents security alerts --risk-level high  # 查询高风险告警详情
```
完整命令参考见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

### API 集成
Security 模块提供 7 个 RESTful 接口，路径前缀 `/api/v1/agentstudio/security`，覆盖防护总览、资产摘要、策略状态、告警列表与导出等能力。所有接口均支持标准 HTTP 认证与错误码处理，详见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)。

## 限制和注意事项

- **全局策略影响**：安全策略配置对账号下全部 Agent 全局生效，修改前须评估跨业务空间影响  
- **审计范围限制**：风险与审计页面展示该账号下**全部 Agent** 的事件，不支持按业务空间过滤；Agent 资产页面仅展示**当前业务空间**内的资产  
- **高级防护能力边界**：当前版本高级防护仅提供检测、告警与审计能力，**不支持自动阻断**（如拦截工具调用、终止会话等），处置需人工介入  
- **资产纳管范围**：仅纳管百炼原生或托管的 Flow/Managed Agent；外部接入的 Agent 不自动纳入资产盘点  
- **数据时效性**：防护总览页面数据约每 2 分钟刷新一次，非实时流式更新  
- **服务授权依赖**：开通高级防护需创建多个服务关联角色（如 `AliyunServiceRoleForSFMSecurity`），开通前须确保主账号具备 RAM 权限并同意相关协议

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/security.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)


