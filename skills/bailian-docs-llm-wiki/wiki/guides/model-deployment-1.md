# model deployment 1

`model deployment 1` 是百炼平台提供的基础[模型部署](../concepts/model-deployment.md)能力，面向开发者提供多种部署模式以适配不同性能、成本与隔离性需求。它支持从快速验证到生产级服务的全周期部署场景，覆盖模型导入、API 发布、流量路由等关键环节。该能力在 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 中首次系统定义。

## 支持的模型/功能

- **部署模式**：支持专属部署、PTU 预置吞吐部署、独占算力部署（MU/DTU）、[Token](../concepts/token.md) 按量部署四类核心模式；  
- **模型来源**：可部署平台预置模型、用户通过 [模型导入](https://help.aliyun.com/zh/model-studio/model-import) 上传的自定义模型，以及已发布的“我的模型”；  
- **配套能力**：集成模型路由（[模型路由](https://help.aliyun.com/zh/model-studio/model-routing)），支持多版本灰度与 A/B 测试；  
- 所有功能入口和概念说明均汇总于 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md)。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `deployment_type` | 部署类型，必填，取值为 `dedicated` / `ptu` / `mu` / `dtu` / `token` | `"ptu"` |
| `instance_count` | 实例数量（仅 `dedicated`/`mu`/`dtu` 有效） | `2` |
| `ptu_capacity` | PTU 预置吞吐单位（仅 `ptu` 有效），最小 100 | `200` |
| `token_quota` | [Token](../concepts/token.md) 按量配额（仅 `token` 有效），单位：万 tokens/天 | `500` |

> **注意**：`instance_count` 在 `ptu` 模式下无效，但部分旧版 SDK 文档仍将其列为可选参数——请以 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 的接口定义为准，忽略过时字段。

## 使用方式

1. 确认模型已发布至“我的模型”中心（参见 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center)）；  
2. 调用 `POST /v1/deployments` 接口，传入 JSON 请求体（含 `model_id`、`deployment_type` 及对应参数）；  
3. 获取返回的 `deployment_id`，调用 `/v1/deployments/{id}/status` 轮询部署状态；  
4. 状态变为 `active` 后，使用 `endpoint` 和 `api_key` 发起推理请求（详见 [API 部署指南](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start)）。  
完整流程与示例代码见 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md)。

## 限制和注意事项

- [Token](../concepts/token.md) 按量部署不支持流式响应（`stream=true`）；  
- PTU 模式下模型最大上下文长度受限于所选 PTU 规格（如 PTU-200 支持最长 32k tokens）；  
- 独占算力（MU/DTU）部署需提前申请配额，且不支持跨地域迁移；  
- 所有部署操作均受项目级资源配额约束，超限将返回 `429 Too Many Requests`；  
- 若发现文档中关于 DTU 内存规格的描述与控制台实际选项不一致，请以控制台实时配置为准——该差异已在新版 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 中同步修正。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1.md)


