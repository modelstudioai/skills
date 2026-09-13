# model deployment 1

本页介绍百炼平台 Model Deployment 1（MD1）能力的核心部署模式与使用规范，适用于需在生产环境稳定调用模型的开发者。MD1 提供多种算力隔离与计费策略组合，支持从轻量级 API 快速上线到高 SLA 独占资源部署。具体实现细节请参考 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md)。

## 支持的模型/功能

- **专属部署**：为单个模型分配独立服务实例，保障资源独占与低延迟  
- **PTU 预置吞吐部署**：基于预估 QPS 预分配 PTU（Processing Throughput Unit），适用于流量可预测场景  
- **独占算力部署（MU/DTU）**：通过 MU（Model Unit）或 DTU（Dedicated Throughput Unit）锁定物理 GPU 资源，满足合规与性能硬性要求  
- **[Token](../concepts/token.md) 按量部署**：按实际 token 输入/输出计费，无预置成本，适合突发或低频调用  
- **模型导入与路由集成**：支持从 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center) 导入自定义模型，并通过 [模型路由](https://help.aliyun.com/zh/model-studio/model-routing) 实现多版本灰度分发  

> **注意**：文档中列出的 [API 部署指南](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start) 当前指向旧版 Quick Start 流程，其 CLI 参数与 v2.3+ SDK 不兼容；请以 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 中的 `bailian deploy` 命令为准。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deployment_type` | string | 是 | 取值：`dedicated`（专属）、`ptu`、`dtu`、`token_based` |
| `instance_type` | string | 否（仅 `dedicated`/`dtu` 必填） | 如 `ecs.gn7i-c16g1.4xlarge`，需与模型显存需求匹配 |
| `min_replicas` / `max_replicas` | int | 否（`ptu`/`token_based` 默认自动扩缩） | 仅 `dedicated` 支持固定副本数 |
| `ptu_capacity` | int | 仅 `ptu` 必填 | 最小 10，单位 PTU；1 PTU ≈ 10 QPS（输入 512 token + 输出 256 token 场景基准） |

## 使用方式

1. 确认模型已发布至 [我的模型](https://help.aliyun.com/zh/model-studio/my-model-center) 并获取 `model_id`  
2. 执行部署命令（以 PTU 模式为例）：
   ```bash
   bailian deploy \
     --model-id your-model-abc123 \
     --deployment-type ptu \
     --ptu-capacity 50 \
     --region cn-shanghai
   ```
3. 部署成功后，通过返回的 `endpoint` 和 `api_key` 调用（详见 [API 部署指南](https://help.aliyun.com/zh/model-studio/model-deployment-quick-start)）  
4. 监控指标请访问控制台「[模型部署](../concepts/model-deployment.md)」页，或调用 `/v1/deployments/{id}/metrics` 接口  

注意：所有部署操作均需模型处于 `Published` 状态，草稿模型不可部署 —— 此限制在 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 中明确说明。

## 限制和注意事项

- 单账号默认最多创建 20 个活跃部署实例（含各类型），配额需提工单申请  
- `token_based` 模式不支持流式响应（`stream: true`）与长上下文（>32k token）场景  
- `dtu` 部署绑定特定 GPU 型号，切换实例类型需先删除再重建  
- 模型版本更新后，已有部署**不会自动升级**，必须手动触发 `bailian deploy --update` 或重建  
- 所有部署均强制启用 HTTPS，不支持 HTTP 回调或内网直连（VPC 对等连接需额外配置）  

> **注意**：原始文档中 [PTU 预置吞吐部署](https://help.aliyun.com/zh/model-studio/ptu-long-input-and-cache) 提及“支持缓存加速”，但当前 MD1 版本（v2.5.0）尚未开放该能力，实际部署时 `cache_enabled` 参数将被忽略 —— 请以 [模型部署 (raw/model-user-guide/model-deployment-1.md)](../../raw/model-user-guide/model-deployment-1.md) 的功能矩阵表为准。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-1.md)


