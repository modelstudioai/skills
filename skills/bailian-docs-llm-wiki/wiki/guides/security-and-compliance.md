# security and compliance

阿里云百炼提供覆盖数据传输、模型调用、权限管控及应用合规的全链路安全与隐私保护能力。平台内置AI内容审核、端到端传输加密、VPC私网隔离访问及空间级精细化权限控制，满足企业级数据合规与监管要求。本文档面向开发者汇总核心安全功能、关键配置参数、标准接入流程及生产环境注意事项。

## 支持的模型/功能
- **AI 输入输出护栏**：自动匹配文本与图像类模型，基于 `cip` 规则对 Prompt 与模型生成结果进行涉黄、涉政、广告等敏感内容识别与拦截。
- **传输加密推理**：支持请求体 `input` 字段的混合加密（AES 数据加密 + RSA 密钥加密），保障高敏数据在公网传输时的机密性与完整性。
- **私网与安全存储隔离**：通过 [[private-link]] 实现 VPC 内网直连百炼推理 API；提供 [[secure-storage-workspace]]，允许在客户自有私有网络内配置隔离的 OSS、AnalyticDB 与 Elasticsearch 实例，数据读写全程不出网。
- **精细化权限管控**：基于业务空间实现角色隔离（超级管理员/空间管理员/普通用户），支持模型调用/训练/部署授权、控制台页面权限管控、[[ram-policy]] 策略绑定及 API Key 生命周期管理。详细说明可参考[权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)。
- **合规资质与备案支撑**：平台已通过 SOC 2 Type II 无保留意见审计，数据落盘与传输采用 AES-256 加密。针对应用上架需求，提供千问/万相等底层模型的《互联网信息服务算法备案》信息与查询路径，辅助开发者完成监管合规。备案指引详见[千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)。

## 关键参数
| 功能模块 | 参数/字段名 | 类型 | 取值/格式说明 |
|:---|:---|:---|:---|
| AI 护栏 | `X-DashScope-DataInspection` | HTTP Header | JSON 字符串，如 `{"input":"cip","output":"cip"}` |
| 传输加密 | `X-DashScope-EncryptionKey` | HTTP Header | JSON 字符串，含 `public_key_id`、`encrypt_key`、`iv` |
| 传输加密 (SDK) | `enable_encryption` / `enableEncrypt` | Boolean | Python 设为 `True`，Java 设为 `true` |
| 公钥获取接口 | `GET /api/v1/public-keys/latest` | REST API | Header 需携带 `Authorization: Bearer <API_KEY>`，返回 `public_key_id` 与 RSA `public_key` |
| 数据权限策略 | `AliyunBailianDataFullAccess` | RAM Policy | 授予应用/知识库/Prompt 工程等 OpenAPI 的全量调用权限 |
| 数据权限策略 | `AliyunBailianDataReadOnlyAccess` | RAM Policy | 授予仅查询类 API（如文件状态、知识库任务状态）权限 |
| 安全存储网络 | `安全组入方向规则` | Network Config | 源 IP 需填 MSE 网关节点 VIP 或交换机网段，端口 `1-65535` 或按需放通 `80/443` |

## 使用方式
### 1. 接入 AI 安全护栏
无需改造核心业务逻辑，仅需在调用大模型时附加特定 Header。平台会自动根据路由模型匹配对应的护栏服务版本。
**DashScope / OpenAI Python SDK 示例：**
```python
extra_headers = {"X-DashScope-DataInspection": '{"input":"cip","output":"cip"}'}
# 调用 chat.completions.create 时传入 extra_headers 参数
```
> **注意**：护栏拦截触发时，服务端将直接返回 `HTTP 400` 及错误码 `data_inspection_failed`，不会返回模型推理结果，客户端需捕获该异常并做降级或提示处理。

### 2. 启用传输加密推理
- **DashScope SDK（推荐）**：初始化请求参数时开启加密开关。SDK 自动完成密钥拉取、AES 加密、Header 拼装及响应解密，业务侧直接获取明文。
```python
response = dashscope.Generation.call(model="qwen-plus", messages=[...], enable_encryption=True)
```
- **HTTP 手动调用**：需先调取公钥接口，本地生成随机 AES Key 与 IV → 加密 `input` 字段 → RSA 加密 AES Key → 构造 `X-DashScope-EncryptionKey` 发起 POST。响应 payload 需使用原 AES Key 解密。完整加解密时序与示例代码请参考[以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)。

### 3. 私网与安全存储网络搭建
标准生产配置流程如下：
1. **创建终端节点**：在 VPC 控制台创建接口终端节点（指向 `com.aliyuncs.dashscope`）或反向终端节点（用于安全存储）。
2. **配置可用区 IP**：创建 MSE 云原生网关，获取各可用区 NLB VIP 与交换机网段，回填至百炼控制台。
3. **初始化存储资源**：按规范创建 OSS/ADB/ES 实例。OSS 需绑定标签 `bailian-safe-workspace-oss-access:ReadAndWrite` 并配置 CORS；ES 需放行交换机网段白名单。
4. **路由与激活**：在 MSE 配置服务域名与路由规则，返回百炼控制台完成安全存储空间激活。

## 限制和注意事项
- **加密机制兼容性限制**：传输加密功能仅对 DashScope 原生 Endpoint 生效，OpenAI 兼容模式（`/compatible-mode/v1/chat/completions`）目前不支持该加解密链路。若业务强依赖 [[openai-compatible-api|OpenAI 兼容接口]]，建议前置独立的安全代理网关或在应用层实现端到端加密。
- **地域与架构约束**：PrivateLink 私网访问仅支持华北2（北京）与新加坡，弗吉尼亚地域暂不可用。安全存储业务空间的 VPC 必须位于华北2（北京），且必须包含指定可用区（G/H/L）的交换机，否则终端节点连接将失败。
> **注意**：部分早期文档提及默认业务空间支持限流配置，实际上默认业务空间**无法设置**模型调用开关与限流策略。生产环境务必新建独立业务空间实施配额隔离与策略管控。
- **API Key 归属与生命周期**：RAM 子账号被移出空间或主账号执行删除操作时，关联 API Key 将立即失效且不可恢复。自 2026-03-25 起，华北2（北京）新创建的 API Key 将统一归属阿里云主账号。建议通过 [[api-key-management]] 结合环境变量注入，并建立定期轮换机制。
- **合规责任界定**：平台提供的算法备案号、合作协议模板仅作技术侧对接支持。开发者作为实际《生成式人工智能服务管理暂行办法》定义的“服务提供者”，须独立承担内容审核、用户身份标识、数据出境安全评估等法定义务。面向具有舆论属性或社会动员能力的 C 端应用，不可仅依赖平台备案信息，需自行完成安全评估报告与算法备案。

## 来源文档

- [权限管理](../../raw/model-user-guide/security-and-compliance/permission-management-overview.md)
- [输⼊输出AI安全护栏](../../raw/model-user-guide/security-and-compliance/content-security.md)
- [合规资质与隐私说明](../../raw/model-user-guide/security-and-compliance/privacy-notice.md)
- [千问大模型应用上架及合规备案](../../raw/model-user-guide/security-and-compliance/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model.md)
- [以加密的方式接入模型推理功能](../../raw/model-user-guide/security-and-compliance/transmission-security/encrypted-access-to-model-inference.md)
- [获取RSA的公钥](../../raw/model-user-guide/security-and-compliance/transmission-security/model-interface-aes-encryption.md)
- [通过终端节点私网访问阿里云百炼模型或应用 API](../../raw/model-user-guide/security-and-compliance/transmission-security/access-model-studio-through-privatelink.md)
- [配置终端节点并发起连接](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-an-endpoint-and-initiate-a-connection.md)
- [配置MSE云原生网关](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-mse.md)
- [配置可用区IP](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-zone-ip.md)
- [配置私有网络中的资源](../../raw/model-user-guide/security-and-compliance/secure-storage/configure-resources-in-private-network.md)

