# 安全与合规

安全与合规是百炼平台内生、统一、可配置的核心横切能力，贯穿模型调用、Agent 运行、知识管理、工具集成与数据流转全生命周期。它既提供开箱即用的默认防护（如输入输出内容过滤、运行时沙箱隔离），也支持企业级精细化管控（如传输加密、私网访问、权限策略、模型备案与审计留痕），确保开发者在满足《生成式人工智能服务管理暂行办法》等监管要求的前提下，安全、可控、可追溯地构建和运营 AI 应用。

## 在百炼平台的不同场景中，这个概念如何使用

安全与合规不是独立模块，而是深度嵌入以下关键场景的底层能力：

- **Agent 开发与运行**：  
  - Flow Agent 自动启用输入/输出内容安全检测（含提示词注入识别）；  
  - Managed Agent 默认启用运行时沙箱、工具调用拦截、凭证隔离与 Session 生命周期治理；  
  - 所有 Agent 的[记忆](memory.md)（Memory）读写内容均经安全检测，防止恶意[记忆](memory.md)污染。

- **RAG 与知识管理**：  
  - 文件上传时自动预扫描（病毒、敏感信息、格式异常）；  
  - 知识库内容入库前执行安全检测，阻断投毒风险；  
  - RAG 检索结果返回前进行输出合规性校验。

- **模型调用与推理**：  
  - 支持 AES-256+RSA 混合加密传输（通过 `X-DashScope-EncryptionKey` 头），保护 `input` 和 `output`；  
  - 启用 `X-DashScope-DataInspection` 请求头，触发双路（输入/输出）AI 安全护栏，实时拦截违法、违规、高危内容；  
  - 所有上架模型均完成国家网信办算法备案与大模型备案，并公示备案号。

- **网络与数据访问**：  
  - 通过 PrivateLink 实现 VPC 内网直连，流量全程不经过公网；  
  - 安全存储业务空间支持反向终端节点 + MSE 网关，实现对客户私有 OSS/ADB/ES 等资源的安全、可控访问。

- **权限与治理**：  
  - 基于 RBAC 的细粒度应用权限管理，支持按模型、RAG、Workflow 等资源维度授权 `invoke`/`configure`/`update_knowledge` 等操作；  
  - 全链路审计日志（含工具调用、知识库访问、模型请求）统一归集至「风险与审计」中心，支持按风险等级、资产类型、时间范围检索与导出。

## 关键参数和配置

| 参数/配置项 | 作用域 | 说明 | 开发者须知 |
|-------------|--------|------|------------|
| `X-DashScope-DataInspection` | HTTP 请求头（模型/Agent 调用） | 启用增强版内容安全检测，值为 JSON 字符串（如 `'{"input":"cip","output":"cip"}'`） | 需先在控制台开通高级防护并完成服务授权；检测失败返回 `400` + `data_inspection_failed` 错误码，无模型响应体 |
| `enable_encryption` / `enableEncrypt` | SDK 调用参数（Python/Java） | 启用传输加密开关 | 推荐使用 SDK 自动模式（≥Python 1.14.0 / Java 2.12.0），SDK 自动处理密钥获取、AES 加密、RSA 封装与解密 |
| `X-DashScope-EncryptionKey` | HTTP 请求头 | RSA 加密后的 AES 密钥（Base64 编码） | 仅当手动实现加密时需设置；公钥 ID 通过 `/api/v1/public-keys/latest` 获取 |
| 全局安全策略开关 | 控制台 / API（`/policies`） | 控制 11 条高级策略（含内容安全、工具调用拦截、知识库扫描等）的启用状态 | 策略对账号下所有 Agent 全局生效；默认防护不可关闭，高级策略需显式开通 |
| `risk_level`（`high`/`medium`/`low`） | API 查询参数（`/agent_logs`）、CLI 命令选项 | 筛选告警风险等级 | 高风险事件需优先处置；CLI 示例：`bl agents security alerts --risk-level high` |
| `asset_type`（`agent`/`tool`/`knowledge_base`/`channel`） | API 查询参数（`/agent_logs`, `/export_agent_logs`） | 按资产类型过滤告警或导出范围 | `channel` 表示发布渠道（排除已删除、已过期），非通用资产类型，慎用于告警筛选 |

> ⚠️ 注意：  
> - 默认防护无开关，随功能模块（RAG、Memory、Managed Agent）自动启用；  
> - 高级防护当前**不支持自动拦截/阻断**，仅提供监测、告警与审计能力；  
> - 所有 Security API Endpoint 必须使用 `cn-beijing` 地域，格式为 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security`；  
> - API Key 需绑定对应地域，且必须携带 `Authorization: Bearer <API_KEY>` 头。

## 面向开发者，简洁实用

- ✅ **快速启用基础防护**：无需任何配置，只要使用 RAG、Memory 或发布 Managed Agent，即自动获得输入输出检测、沙箱隔离、文件扫描等默认防护。  
- ✅ **一键开通增强能力**：进入控制台 **Security > 高级防护 > 安全策略**，点击“立即开通”并完成服务授权，即可配置自定义敏感词库、细粒度拦截规则。  
- ✅ **程序化监控与响应**：用 CLI 或 API 实时拉取高风险告警：  
  ```bash
  bl agents security alerts --risk-level high
  # 或
  curl -H "Authorization: Bearer sk-xxx" \
       "https://your-workspace.cn-beijing.maas.aliyuncs.com/api/v1/agentstudio/security/agent_logs?risk_level=high&order_by=check_time&order=desc"
  ```  
- ✅ **安全集成到生产调用链**：  
  - 用 SDK 自动加密：`client.chat.completions.create(..., enable_encryption=True)`；  
  - 用请求头启用护栏：`headers={"X-DashScope-DataInspection": '{"input":"cip","output":"cip"}'}`；  
  - 用私网域名替换 base_url，实现 VPC 内网调用。  
- ✅ **审计闭环**：所有风险事件自动留痕，支持通过 `/export_agent_logs` 提交导出任务，轮询 `/export_status` 获取 Excel 下载链接，满足合规报告需求。

## 关联主题页

- [security guide](../guides/security-guide.md)
- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [managed agents](../guides/managed-agents.md)
- [llm application](../guides/llm-application.md)
- [application permission management](../guides/application-permission-management.md)


