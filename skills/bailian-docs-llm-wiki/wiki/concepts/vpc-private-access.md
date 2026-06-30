# 私网访问

私网访问（VPC Private Access）是指阿里云百炼平台的模型调用、[模型部署](model-deployment.md)、异步任务通知等能力通过 VPC 内网或私网链路访问，避免公网暴露、提升传输安全性与网络稳定性的接入方式。它是百炼安全合规体系中"传输加密—私网访问"环节的核心抓手，与身份权限、内容安全、合规备案、安全存储共同构成端到端安全链路。

## 在百炼平台中的使用场景

### 1. 模型调用的私网接入

百炼模型调用默认通过公网（`dashscope.aliyuncs.com`）发起，对安全要求高或需统一出口的企业可走 VPC 私网。临时 API Key 可在不可信客户端环境使用，配合 VPC 私网访问可在内网完成调用链路，避免永久 Key 在公网流转。

> 各地域（北京、新加坡、弗吉尼亚）的 API Key 不互通，临时 Key 与生成它的永久 Key 必须属于同一地域，私网链路也需在对应地域内打通。

### 2. 异步任务完成通知的 VPC 回调

图像/视频生成等耗时任务接入事件总线 EventBridge 后，任务完成事件由事件总线推送。HTTP 回调 URL 接收端**支持公网或 VPC 访问**，对安全敏感场景建议使用 VPC 类型的 HTTP 接口作为事件目标，使通知链路全程在内网闭环。

- 事件源：`acs.dashscope`
- 事件类型：`dashscope:System:AsyncTaskFinish`
- 事件总线默认为 `default`（北京地域云服务专用总线）

RocketMQ 消息队列方案同样可部署在 VPC 内，由事件总线投递后业务方在内网消费，支持消息无丢失与失败重试，可靠性更高。

### 3. [模型部署](model-deployment.md)与模型导入的私网通道

[模型部署](model-deployment.md)（PTU、模型单元、按 Token 用量）仅适用于华北二（北京）地域，部署后推理服务可在 VPC 内调用，满足高并发、低延迟及不出公网的诉求。

部署自定义 LoRA 模型时，需将本地训练的 LoRA 模型从阿里云 OSS 导入百炼。OSS Bucket 支持**私有 Bucket**与**内容加密**，并需添加 `bailian-datahub-access` 标签（值为 `read`）。通过 VPC 终端节点或私网访问 OSS，可避免训练产物经公网传输，保障数据安全。

## 关键参数与配置

| 维度 | 关键约束 |
| --- | --- |
| 地域一致性 | API Key、临时 Key、私网链路须同地域；模型部署仅北京 |
| 临时 Key 有效期 | 默认 60 秒，可通过 `expire_in_seconds` 设置，范围 [1, 1800] 秒 |
| 异步任务接口限流 | 20 QPS（按主账号 + 子账号维度）；通知方案不限流 |
| 任务保留时长 | 完成后约 24 小时自动清理 |
| OSS 导入标签 | Bucket 须加 `bailian-datahub-access=read` 标签 |
| OSS 存储类型 | 不支持归档/冷归档/深度冷归档；须使用子目录，非根目录 |
| 授权角色 | OSS 导入需开通 `AliyunServiceRoleForSFMDataHubOSSImport` 服务关联角色 |

## 开发者实践建议

- **生产隔离**：按环境（dev/test/prod）划分业务空间，prod 流量走 VPC 私网，降低公网泄露面。
- **回调优先 VPC**：异步任务通知的 HTTP 回调端点部署在 VPC 内，事件总线直推即可，无需公网暴露。
- **OSS 导入走私网**：LoRA 模型导入使用私有 Bucket + 内容加密，并通过 VPC 终端节点访问 OSS。
- **避免跨地域**：规划业务空间时明确地域，避免因 Key 与链路跨地域导致调用失败。
- **PTU 部署内网化**：高负载生产环境优先 PTU 部署并经 VPC 调用，兼顾稳定吞吐与传输安全。

## 关联主题页

- [security and compliance](../guides/security-and-compliance.md)
- [more about models](../api/more-about-models.md)
- [model deployment 1](../guides/model-deployment-1.md)


