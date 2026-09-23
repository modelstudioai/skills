# 安全与合规

安全与合规是百炼平台内生、贯穿 AI 应用全生命周期的核心横切能力，旨在保障数据不泄露、交互不越界、运行不失控、行为可审计、服务可备案，满足《生成式人工智能服务管理暂行办法》等国内监管要求及企业级生产环境的安全治理标准。

## 在百炼平台的不同场景中，这个概念如何使用

安全与合规能力按“防护层”与“治理层”双轨落地，覆盖开发、运行、数据、网络、权限与合规申报六大维度：

- **开发阶段**：通过 Flow Agent / Managed Agent / RAG / Memory 等模块的**默认原生防护**自动启用内容安全检测（输入/输出过滤、知识库投毒识别、记忆读写审查），无需代码改造；开发者仅需接入对应能力模块（如绑定知识库、启用 Memory），即获得基础级风险拦截。
- **运行阶段**：Managed Agent 自动启用沙箱隔离、工具调用拦截与凭证隔离；RAG 文件上传时触发预扫描；所有模型交互支持通过 `X-DashScope-DataInspection` 请求头开启 AI 安全护栏（涉政、涉黄、广告等实时识别）。
- **数据传输**：敏感数据场景下，可通过 DashScope SDK 启用 AES-256+RSA 混合加密（`enable_encryption=True`），或手动在请求头携带 `X-DashScope-EncryptionKey`，实现端到端密文传输。
- **网络访问**：支持两种私网方案——通用型 PrivateLink（控制台自助开通，VPC 内直连）与高安全等级“安全存储空间”（需商务开通，全链路私有云资源隔离），确保流量不出公网。
- **权限治理**：以业务空间为最小单元，通过 RAM 集成实现模型调用/调优/部署的开关管控、API Key 的地域+空间强绑定、IP 白名单（仅北京地域）、QPM/[Token](token.md) 限流等策略，杜绝越权与滥用。
- **合规申报**：所有上架模型均完成国家网信办算法备案及大模型备案，备案信息实时公示；平台提供结构化审计日志（含风险等级、资产类型、处置状态），支撑企业自证合规。

> ⚠️ 注意：默认防护自动生效，但高级防护（如增强内容检测、全量审计留痕）需在控制台 **Security > 高级防护 > 安全策略** 中完成服务授权并手动开启；当前高级防护处于限时免费阶段，建议生产环境主动开通。

## 关键参数和配置

| 类别 | 参数/配置项 | 说明 | 开启方式 |
|--------|--------------|------|------------|
| **内容安全** | `X-DashScope-DataInspection` | HTTP 请求头，启用 AI 安全护栏，值为 `{"input":"cip","output":"cip"}` 表示双向检测 | 手动添加至请求头；需提前开通服务 |
| **传输加密** | `enable_encryption`（Python）<br>`enableEncrypt(true)`（Java） | SDK 级开关，自动完成密钥分发与加解密 | 调用 SDK 时传入布尔值 |
| **网络隔离** | 私网域名（如 `{WorkspaceId}-{VpcId}.cn-beijing.maas.aliyuncs.com`） | PrivateLink 方式访问百炼 API 的专用地址 | 控制台开通后替换原 API 域名 |
| **权限控制** | `x-bailian-workspace-id` + `Authorization: Bearer <API_KEY>` | OpenAPI 必需请求头，决定模型可用性、限流策略与权限边界 | 创建 API Key 时绑定业务空间，调用时显式传入 |
| **审计与告警** | `risk_level=high` / `asset_type=knowledge_base` | Security API 查询参数，用于筛选高风险告警或指定资产类型 | 调用 `/agent_logs` 等接口时传入 |
| **高级防护** | `AliyunServiceRoleForSFMSecurity` 角色 | 高级防护开通时自动创建的服务角色，授予必要云资源访问权限 | 控制台点击「立即开通」自动创建 |

- **Credit 消耗**：高级防护中内容检测按 [Token](token.md) 计费，每席位每日默认 300 Credits（超量 0.0015 元/Credit）；
- **风险等级**：告警按 `high`/`medium`/`low` 三级标记，用于优先级排序与处置闭环；
- **审计范围**：风险与审计页面展示**账号级全部 Agent 数据（不区分业务空间）**，而资产统计与防护总览按业务空间组织。

## 面向开发者，简洁实用

- ✅ **快速启用**：  
  - 内容安全：SDK 调用时加 `X-DashScope-DataInspection` 头即可；  
  - 传输加密：升级 DashScope SDK ≥1.14.0（Python）或 ≥2.12.0（Java），传 `enable_encryption=True`；  
  - 私网访问：开通 PrivateLink 后，将 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 替换为私网域名。

- ✅ **可观测与响应**：  
  - CLI 查看概览：`bl agents security overview`；  
  - CLI 获取高风险告警：`bl agents security alerts --risk-level high`；  
  - API 查询告警：`GET /api/v1/agentstudio/security/agent_logs?risk_level=high&status_list=unhandled`；  
  - 导出审计报告：先 `POST /export_agent_logs`，再轮询 `/export_status` 获取下载链接。

- ✅ **权限最小化实践**：  
  - 生产环境务必使用**自定义业务空间**（非默认空间），由超级管理员开启所需模型权限；  
  - RAM 用户仅授予 `AliyunBailianDataReadOnlyAccess` 或 `FullAccess`，禁用全局 `AliyunBailianFullAccess`；  
  - API Key 严格绑定单一地域+单一业务空间，北京地域可额外配置 `ip_whitelist`。

- ❌ **避坑提示**：  
  - 高级防护**不支持自动阻断**，所有告警需人工确认处置；  
  - 控制台页面权限 ≠ API 权限：用户被禁止访问某模型页面，**不影响其 API Key 调用该模型**（只要空间级开关已开）；  
  - Security API 仅支持 `cn-beijing` 地域，其他 region 请求会失败；  
  - 文档中 `"app"` 作为 `asset_type` 是过时描述，实际枚举值为 `agent`/`tool`/`skill`/`knowledge_base`/`memory`/`channel`。

## 关联主题页

- [security guide](../guides/security-guide.md)
- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application permission management](../guides/application-permission-management.md)
- [application support](../guides/application-support.md)


