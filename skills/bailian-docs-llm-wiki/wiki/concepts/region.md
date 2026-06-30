# 地域与可用区

地域（Region）是百炼平台在物理地理上划分的部署区域，决定接入点位置、数据存储位置与推理执行位置；可用区是地域内相互隔离的物理设施单元。在百炼中，"地域"主要与**服务部署范围**和**接入域名**共同决定调用路径、数据驻留约束与服务保障等级。

## 可用地域

百炼当前支持的地域及其 Region ID：

| 地域 | Region ID | 数据驻留约束 |
| --- | --- | --- |
| 华北2（北京） | `cn-beijing` | 数据不出中国内地 |
| 新加坡 | `ap-southeast-1` | 数据不经过中国内地 |
| 美国（弗吉尼亚） | — | 数据不出美国 |
| 德国（法兰克福） | `eu-central-1` | 数据不出欧盟 |
| 日本（东京） | `ap-northeast-1` | 数据不出日本 |

若对驻留无限制但追求更大推理资源池，可选择美国/德国/日本的全球部署范围。

## 三个关键概念

调用前需同时确认**地域**、**服务部署范围**、**接入域名**：

- **地域**：决定接入点与数据存储位置。
- **服务部署范围**：决定推理执行位置（数据是否跨域流转）。
- **接入域名**：影响并发上限、超时、SLA 等服务保障。

三者在控制台或 Base URL 中体现，**各地域的接入域名、API Key、模型列表不能跨地域混用**。

## 接入域名类型

| 域名类型 | 格式 | 适用场景 | 关键指标 |
| --- | --- | --- | --- |
| 专属域名 | `{WorkspaceId}.{region}.maas.aliyuncs.com` | 生产环境 | SLA 99.9%、超时 3600 秒、支持 HTTP/SSE/WebSocket/WebRTC |
| 共享域名 | `dashscope.aliyuncs.com` | 存量兼容 | — |
| 试用域名 | `trial.{region}.maas.aliyuncs.com` | 快速体验 | 不建议生产 |

从共享域名迁移到专属域名只需替换 Base URL 中的域名部分，业务逻辑代码无需修改。

## 各地域调用差异

- **华北2（北京）**：默认推荐地域，专属域名 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。知识库、[模型部署](model-deployment.md)、数据管理、Prompt 模板、模型调优等大量能力仅在此地域开放。
- **新加坡**：专属域名 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1`。
- **美国（弗吉尼亚）**：使用带 `-us` 后缀的模型名（如 `qwen-plus-us`）可限定美国境内推理；共享接入域名 `https://dashscope-us.aliyuncs.com/compatible-mode/v1`。
- **德国（法兰克福）/日本（东京）**：通过业务空间区分全球/欧盟或全球/日本部署范围，调用前需先在业务空间管理页面创建并选择对应业务空间。

## 业务空间与 WorkspaceId

使用北京、新加坡、日本、德国等地域时，需在 Base URL 中填入 WorkspaceId。WorkspaceId 可在控制台「业务空间管理」页面查看。子账号需加入对应业务空间并获得相应策略后方可操作该空间下的资源。

## 地域相关能力约束

部分能力仅在特定地域可用：

| 能力 | 可用地域 |
| --- | --- |
| 知识库（标准版/旗舰版） | 仅华北2（北京） |
| [模型部署](model-deployment.md)（资源专享推理） | 仅华北2（北京） |
| 数据管理（训练集/[评测](evaluation.md)集/数据流） | 仅华北2（北京） |
| Prompt 模板 | 仅华北2（北京） |
| `qwen-deep-research` | 仅华北2（北京），且仅支持 Python DashScope SDK |
| `qwen-mt-plus` / `qwen3.5-ocr` | 北京、新加坡、美国（弗吉尼亚） |
| `gui-plus` | 华北2（北京） |

## 选择建议

1. 明确数据驻留要求（是否允许数据出境）。
2. 确认所需模型/能力是否在目标地域开放。
3. 生产环境统一使用专属域名，避免使用试用域名。
4. 同一业务的所有调用、API Key、模型列表保持在同一地域，不要混用。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [knowledge base](../guides/knowledge-base.md)
- [model deployment 1](../guides/model-deployment-1.md)
- [prompt](../guides/prompt.md)
- [model data overview](../guides/model-data-overview.md)
- [more models](../api/more-models.md)


