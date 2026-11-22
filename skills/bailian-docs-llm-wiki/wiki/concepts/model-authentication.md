# 模型鉴权与认证

模型鉴权与认证是百炼平台对调用方身份进行核验、权限进行校准的核心安全机制，确保只有合法授权的开发者或应用能够访问模型服务（如大语言模型、[多模态](multi-modal.md)模型、嵌入模型等）及配套能力（如智能体、沙箱、安全策略、结构化解析等）。该机制通过 API Key 或 AccessKey 等凭证，在请求链路中完成身份识别、作用域验证与访问控制。

## 在百炼平台的不同场景中，这个概念如何使用

模型鉴权与认证并非单一技术实现，而是根据**服务类型、接口层级与安全边界**采用差异化策略：

- **模型推理类 API（如 `qwen-max`、`text-embedding-v1`、`qwen-vl-plus`）**：统一使用 `DASHSCOPE_API_KEY`，通过 `Authorization: Bearer <API Key>` Header 传递。SDK（如 `dashscope` Python 包）自动注入该凭证，无需手动拼接；环境变量 `DASHSCOPE_API_KEY` 是首选配置方式。

- **ParseX 结构化解析与字段抽取 API**：同样基于 `DASHSCOPE_API_KEY`，但需注意其 Base URL 为工作空间专属域名（如 `{workspaceId}.cn-beijing.maas.aliyuncs.com`），且所有请求必须携带 `Authorization: Bearer ...`，不支持其他认证方式。

- **Security API（安全策略管理）**：采用独立的长期凭证体系，使用 `X-Api-Key` Header（值为控制台「API 密钥管理」中创建的密钥），**不兼容 `Bearer` 格式**。该设计隔离了模型调用与基础设施管控权限，符合最小权限原则。

- **Flow Agent API（智能体/工作流）**：存在**双轨鉴权**：
  - 应用调用（如 `/apps/{app_id}/completion`）：使用 `Authorization: Bearer <DASHSCOPE_API_KEY>`；
  - 组件管理（如 Prompt 模板、[长期记忆](long-term-memory.md)）：使用阿里云标准 `AccessKey ID/Secret` 签名（`ACS3-HMAC-SHA256`），需通过阿里云 SDK 或 OpenAPI Explorer 构造签名，**不可用 API Key 替代**。

- **Sandbox API（沙箱环境）**：回归统一模型调用范式，使用 `Authorization: Bearer <DASHSCOPE_API_KEY>`，且明确要求该 Key 必须在百炼控制台创建（而非阿里云主账号 AK/SK），强调沙箱作为“AI 原生执行环境”的业务归属一致性。

> ✅ 共性总结：所有场景均**拒绝匿名访问**；所有凭证均需**安全存储**（禁用硬编码）；所有请求均需显式声明 `Content-Type: application/json`；超时、限流、错误响应格式虽有差异，但鉴权失败统一返回 `401 Unauthorized`。

## 关键参数和配置

| 参数/配置项 | 说明 | 是否必需 | 注意事项 |
|-------------|------|----------|----------|
| `DASHSCOPE_API_KEY` | 百炼平台颁发的模型调用密钥，用于 DashScope 网关类 API（模型推理、ParseX、Sandbox、Flow Agent 应用调用） | 是（对应场景） | • 从 [百炼控制台 → API 密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建<br>• 生产环境必须通过环境变量或密钥管理服务注入，**严禁硬编码**<br>• 不同工作空间可复用同一 Key（权限由 Key 绑定的 IAM 策略控制） |
| `X-Api-Key` | Security API 专用长期密钥，与 `DASHSCOPE_API_KEY` 独立生成 | 是（Security API） | • 控制台路径：「API 密钥管理」→ 「Security API 密钥」<br>• 仅用于 `api.bailian.aliyuncs.com` 域名下的 Security 接口<br>• 不支持 `Bearer` 前缀，Header 名严格为 `X-Api-Key` |
| `AccessKey ID / Secret` | 阿里云主账号或 RAM 子账号凭证，用于 Flow Agent 的组件类 OpenAPI | 是（Prompt/记忆等组件接口） | • 必须启用 `ACS3-HMAC-SHA256` 签名<br>• 推荐使用阿里云官方 SDK（如 `aliyun-openapi-python-sdk`）自动处理签名<br>• 不可用于任何 DashScope 网关接口 |
| `DASHSCOPE_BASE_URL` | 自定义网关地址（如私有化部署、特定 Region） | 否（默认已预设） | • 默认值：`https://dashscope.aliyuncs.com/api/v1`<br>• ParseX/Sandbox 等需工作空间域名，**不可复用此配置**，应按文档拼装专属 Endpoint |

## 面向开发者，简洁实用

- ✅ **第一步：选对密钥**  
  - 调模型、跑沙箱、解析文档 → 用 `DASHSCOPE_API_KEY`；  
  - 配安全策略 → 用 `X-Api-Key`；  
  - 改 Prompt 模板、管记忆 → 用阿里云 `AccessKey`。

- ✅ **第二步：配对位置**  
  - `DASHSCOPE_API_KEY` 和 `X-Api-Key`：设为 HTTP Header —— `Authorization: Bearer xxx` 或 `X-Api-Key: xxx`；  
  - `AccessKey`：交由阿里云 SDK 签名，**不要手动构造 Header**。

- ✅ **第三步：防踩坑清单**  
  - ❌ 不要将 `DASHSCOPE_API_KEY` 当作 `AccessKey` 传给 OpenAPI；  
  - ❌ 不要用 `AccessKey` 发送 `Authorization: Bearer ...` 请求；  
  - ❌ 不要在代码中写死任何密钥（包括测试环境）；  
  - ✅ 所有首次调用前，建议用 `dashscope.models.List.list()`（需权限）或最小 payload（如 `qwen-turbo` 空 prompt）快速验证连通性与鉴权有效性；  
  - ✅ 遇到 `401 Unauthorized`，优先检查：Header 名称是否拼错、Key 是否过期、是否误用了其他产品的密钥。

鉴权是模型服务的第一道门。门开对了，后面才是能力本身。

## 关联主题页

- [preparations](../api/preparations.md)
- [api overview](../api/api-overview.md)
- [security api guide](../api/security-api-guide.md)
- [flow agent api](../api/flow-agent-api.md)
- [sandbox api](../api/sandbox-api.md)


