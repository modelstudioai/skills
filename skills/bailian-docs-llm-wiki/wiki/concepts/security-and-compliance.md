# 安全与合规

安全与合规是百炼平台面向企业级生产环境构建的核心横切能力，指通过技术手段与管理机制的协同，在模型调用、Agent 运行、数据流转、权限控制等全生命周期环节中，保障系统机密性、完整性、可用性，并满足《生成式人工智能服务管理暂行办法》等国内监管要求及行业合规标准（如金融、政务场景的数据本地化、审计留痕、内容安全等）。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用层**：默认启用输入/输出双路 AI 安全护栏（通过 `X-DashScope-DataInspection` 控制），支持传输加密（AES-256+RSA 混合加密）、私网访问（PrivateLink）、敏感词掩码或拦截；所有托管模型均内置涉政、暴恐、色情等基础内容审核能力。  
- **Agent 与工作流层**：提供 Agent 全生命周期安全态势感知（通过 Security API 查询防护开关、策略状态、实时告警），支持对工具调用、记忆存储、RAG 检索结果进行实时内容过滤与脱敏，并可绑定细粒度安全策略（如 `baseline_check`、`vulnerability_scan`）。  
- **数据与存储层**：高合规场景可选用“安全存储业务空间”，通过反向终端节点 + MSE 网关 + 专有网络资源（OSS/ADB/ES）构建全链路私有化数据平面，确保训练/推理数据不出域。  
- **权限与治理层**：基于业务空间（Workspace）实现最小权限管控——模型调用/调优/部署需显式开通，API Key 权限继承自空间配置（与用户控制台角色解耦），支持 QPM/TPM 限流、IP 白名单、操作审计日志（`enable_audit_log`）等治理能力。  
- **可观测与响应层**：模型监控（`/v1/monitoring/*`）与 Security API（`/agentstudio/security/*`）共同构成安全运营闭环：前者跟踪延迟、错误率等运行指标，后者提供风险告警、策略配置、资产分布等安全治理数据，支持自动化集成与告警导出。

## 关键参数和配置

| 参数/配置项 | 作用 | 是否必填 | 典型值/说明 |
|-------------|------|----------|-------------|
| `X-DashScope-DataInspection` | 启用输入/输出内容安全检测 | 否（默认启用基础策略） | `'{"input":"cip","output":"cip"}'`（启用全部检测） |
| `X-DashScope-EncryptionKey` | 传输加密时封装的 AES 密钥（Base64） | 启用加密时自动填充 | SDK 自动处理，手动调用需先获取公钥并加密 |
| `Authorization: Bearer <api_key>` | 所有安全相关 API 的统一认证凭证 | 是 | 必须配置在环境变量中，禁止硬编码 |
| `security_policy_id` | 绑定到模型或 Agent 的安全策略 ID | 否（默认 `default`） | 可通过控制台创建自定义策略，支持关键词库（≤10MB） |
| `enable_audit_log` | 开启操作审计日志（记录 [prompt](../guides/prompt.md)、response、策略匹配结果） | 否（默认 `false`） | 启用后延迟增加 50–200ms，日志保留 90 天 |
| `risk_level`（Security API） | 告警筛选等级 | 否（默认返回全部） | `high` / `medium` / `low` |
| `current_page` / `page_size`（Security API） | 告警列表分页参数 | 否（默认 `1` / `20`） | 使用游标分页，响应含 `next_page` 字段 |
| `params`（Security API 导出接口） | 导出查询条件（JSON 字符串化） | 是（POST 请求体中） | `"\"RiskLevel\":\"high\",\"OrderBy\":\"CheckTime\""` |

> ⚠️ 注意：  
> - 所有 API Key 仅在其归属业务空间的地域（如 `cn-beijing`）生效，不跨地域复用；  
> - 安全策略与运行时防护模块独立配置：`/policies` 查策略启停，`/overview` 查实际生效模块（如 `flow_agent`, `memory`），二者需分别确认；  
> - 生产环境务必使用**非默认业务空间**——默认空间无权限开关、无限流能力，不符合合规基线要求。

## 面向开发者，简洁实用

- ✅ **快速启用基础防护**：无需任何配置，所有模型调用默认受内容安全检测保护；添加 `X-DashScope-DataInspection` 即可定制检测范围。  
- ✅ **加密接入一步到位**：Python/Java SDK 调用时传入 `enable_encryption=True`，自动完成公钥获取、AES 加密、密钥封装与响应解密（需 `dashscope>=1.14.0` 或 `dashscope-sdk-java>=2.12.0`）。  
- ✅ **私网访问三步开通**：控制台 → 管理 > 网络配置 → 开通 PrivateLink → 关联业务空间 → 替换 API `base_url` 为私网域名。  
- ✅ **审计与告警自动化**：调用 Security API 的 `/export_agent_logs` 提交导出任务，轮询 `/export_status` 获取下载链接，无缝对接 SIEM 或内部风控平台。  
- ✅ **权限最小化实践**：为每个生产应用创建独立业务空间，超级管理员关闭无关模型开关，业务空间管理员按需分配 RAM 用户权限，API Key 严格绑定最小必要角色。  

安全与合规不是附加选项，而是百炼平台的默认基线。从第一次 API 调用开始，你已在受保护的环境中运行。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [security guide](../guides/security-guide.md)
- [application permission management](../guides/application-permission-management.md)
- [model monitoring](../guides/model-monitoring.md)


