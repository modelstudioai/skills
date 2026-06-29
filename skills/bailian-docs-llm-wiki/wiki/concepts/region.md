# 地域与可用区

地域（Region）是百炼平台在地理层面的资源划分单元，决定了接入点位置、数据存储位置和推理执行位置；可用区则在地域内部提供物理隔离的部署能力。开发者在调用 API、开通功能或部署模型前，必须先确认所选地域是否支持目标能力，并使用对应地域的接入域名、API Key 与业务空间。

## 百炼支持的地域

百炼目前提供五个地域：

| 地域 | Region ID | 服务部署范围 |
| --- | --- | --- |
| 华北2（北京） | `cn-beijing` | 中国内地（固定，无需选择） |
| 新加坡 | `ap-southeast-1` | 国际（固定，无需选择） |
| 美国（弗吉尼亚） | — | 默认全球推理，可用 `-us` 后缀模型限定美国境内 |
| 德国（法兰克福） | `eu-central-1` | 通过业务空间选择部署范围 |
| 日本（东京） | `ap-northeast-1` | 通过业务空间选择部署范围 |

各地域拥有**独立的接入域名、API Key 和模型列表，不能跨地域混用**。德国（法兰克福）和日本（东京）地域通过业务空间（Workspace）区分服务部署范围，调用前需在业务空间管理页面创建业务空间并选择部署范围。

## 服务部署范围与接入域名

除地域外，还需关注两个相关概念：

- **服务部署范围**：决定推理执行位置。无合规需求选「全球」部署范围（推理资源池更大）；有数据合规需求则选特定地理边界（中国内地/美国/欧盟/日本/国际）。华北2（北京）和新加坡地域各仅支持一种部署范围，无需选择。
- **接入域名**：百炼提供专属、共享、试用三种。
  - 专属域名（推荐生产）：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，并发承载更高、网络隔离、超时 3600 秒，支持 HTTP/SSE/WebSocket/WebRTC，提供 99.9% SLA。
  - 共享域名：`dashscope.aliyuncs.com`，兼容存量业务，建议迁移至专属域名。
  - 试用域名：`trial.{region}.maas.aliyuncs.com`，仅用于快速体验。

例如华北2（北京）专属域名为 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`，新加坡为 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`，美国（弗吉尼亚）为 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`。

## 各功能的时效地域约束

百炼的不同能力对地域的支持存在差异，使用前务必确认：

| 能力 | 地域约束 |
| --- | --- |
| 知识库（RAG） | 仅中国站华北2（北京）地域可开通和使用 |
| Prompt 模板（预置/自定义） | 仅适用于华北2（北京）地域 |
| 数据管理（训练集/评测集/数据处理） | 仅适用于华北2（北京）地域，且暂无 API，需在控制台操作 |
| 模型部署（独立资源专享） | 仅适用于华北二（北京）地域 |
| `qwen-deep-research` | 仅华北2（北京）地域，且仅 Python DashScope SDK 调用 |
| `gui-plus` 界面交互模型 | 仅华北2（北京）地域 |
| `qwen-mt-plus` / `qwen3.5-ocr` | 北京 / 新加坡 / 美国（弗吉尼亚） |
| `farui-plus`、`tongyi-intent-detect-v3` | 默认地域 |

实时推理、模型体验、模型监控、传输安全、权限管理在所有地域均支持；批量推理、模型告警、模型调优仅部分地域支持。

## 调用前必做的地域配置

1. 在目标地域创建或选择业务空间（Workspace），记录 WorkspaceId。
2. 在该地域的 API Key 页面创建 API Key（各地域独立，不可跨地域使用）。
3. 将 API Key 配置到环境变量 `DASHSCOPE_API_KEY`，避免代码硬编码。
4. 在 Base URL 中填入对应地域的专属接入域名（含 WorkspaceId）。
5. 若使用美国（弗吉尼亚）地域并要求推理在美国境内执行，选择带 `-us` 后缀的模型名称（如 `qwen-plus-us`）；不带后缀则默认全球推理。

## 选用建议

- 就近选择地域以降低延迟。
- 生产环境优先使用专属接入域名，享受更高并发与 SLA。
- 涉及知识库、Prompt 模板、数据管理、模型部署等能力时，统一规划在华北2（北京）地域。
- 跨境业务按合规要求选择新加坡、美国、德国或日本地域，并通过业务空间控制部署范围。

## 关联主题页

- [knowledge base](../guides/knowledge-base.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [prompt](../guides/prompt.md)
- [model data overview](../guides/model-data-overview.md)
- [more models](../api/more-models.md)
- [get started with models](../guides/get-started-with-models.md)


