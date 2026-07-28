# 地域与接入点

地域（Region）是阿里云百炼服务部署和数据存储的地理位置，接入点（Base URL / 域名）则是调用该地域服务的网络入口。两者共同决定了你使用哪个 API Key、能调用哪些模型、按什么价格计费，以及数据在哪个国家/地区境内处理。

## 核心规则

- **各地域完全隔离**：API Key、可用模型列表、价格、[业务空间](workspace.md)在不同地域之间相互独立，**API Key 不能跨地域使用**。
- **Base URL 与 API Key 必须配套**：Base URL 必须与同一地域、同一计费方案的 API Key 搭配使用，否则返回 401/403 鉴权失败，或意外走按量计费通道。
- **部分能力仅限特定地域**：选型前务必确认目标能力在目标地域是否可用。

## 支持的地域

| 地域 | Region ID | 说明 |
| --- | --- | --- |
| 华北2（北京） | `cn-beijing` | 功能最全，DeepSeek 等部分第三方模型仅此地域提供 |
| 新加坡 | `ap-southeast-1` | 国际站主力地域 |
| 日本（东京） | `ap-northeast-1` | 需先创建[业务空间](workspace.md)并选择服务部署范围（全球/日本） |
| 德国（法兰克福） | `eu-central-1` | 需先创建[业务空间](workspace.md)并选择服务部署范围（全球/欧盟） |
| 美国（弗吉尼亚） | `us-east-1` | 暂不支持业务空间专属域名；用带 `-us` 后缀的模型名（如 `qwen-plus-us`）限定美国境内推理 |

## 三种接入域名（按量付费）

| 域名类型 | 格式 | 适用场景 | 请求超时 |
| --- | --- | --- | --- |
| 业务空间专属域名（推荐） | `{WorkspaceId}.{region}.maas.aliyuncs.com` | 生产环境，高并发、流量隔离，SLA 99.9% | 3600 秒 |
| Dashscope 域名 | `dashscope.aliyuncs.com` 等 | 存量业务兼容，建议迁移 | 600 秒 |
| 试用域名 | `trial.{region}.maas.aliyuncs.com` | 快速验证，RPM 固定 1000，无 SLA | 600 秒 |

接口规范与路径的对应关系（以专属域名为例）：

- OpenAI 兼容：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`
- DashScope 原生：路径换为 `/api/v1`
- Anthropic 兼容：路径换为 `/apps/anthropic`

使用北京、新加坡、东京、法兰克福地域的专属域名时，需要在 Base URL 中填入业务空间 ID（WorkspaceId），可在控制台业务空间管理页面查看。

## 订阅制产品的专属接入点

Token Plan / Coding Plan 与按量付费是三套完全隔离的体系，各有专属 Key 和域名：

- **Token Plan**：仅支持华北2（北京）地域，Key 以 `sk-sp-` 开头，Base URL 为 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Anthropic 兼容为 `/apps/anthropic`）。
- **Coding Plan**：专属 Key + `https://coding.dashscope.aliyuncs.com/v1`。
- **按量付费**：通用 `sk-` Key + 上文各地域域名。

三者不可混用，混用会导致鉴权失败或意外扣费。

## 各场景的地域限制速查

| 场景 | 地域限制 |
| --- | --- |
| 模型微调（全部模态） | 仅华北2（北京），必须使用北京地域的 API Key |
| 数据管理 / 数据清洗与增强 | 仅华北2（北京） |
| 日志回流 | 华北2（北京）和新加坡 |
| 微调数据集 OSS 挂载 | Bucket 仅支持 `cn-beijing` 和 `ap-southeast-1` |
| Token Plan 订阅 | 仅华北2（北京），需在控制台左上角切换地域后购买 |
| DeepSeek 等部分第三方模型 | 仅华北2（北京） |

## 开发者实践建议

1. **先定地域再拿 Key**：根据数据合规要求（如欧盟、日本、美国境内处理）和所需模型/功能选定地域，再在该地域创建 API Key 与业务空间。
2. **生产用专属域名**：业务空间专属域名提供更高超时（3600 秒）、流量隔离和 SLA 保障；试用域名仅用于快速验证。
3. **将地域信息写入配置**：Base URL、WorkspaceId、API Key 建议通过环境变量（如 `DASHSCOPE_API_KEY`）管理，避免硬编码和跨地域误用。
4. **权限按地域规划**：业务空间不能跨地域存在，不同地域的默认业务空间也是不同空间；RAM 权限和空间级[限流](rate-limit.md)需按地域分别配置。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [token plan guide](../guides/token-plan-guide.md)
- [fine tuning](../guides/fine-tuning.md)
- [model data overview](../guides/model-data-overview.md)
- [security and compliance](../guides/security-and-compliance.md)


