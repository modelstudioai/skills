# model deployment index

百炼平台提供多种模型部署方式，支持从轻量级按量调用到高保障独占算力的全场景需求。开发者可根据延迟敏感度、吞吐稳定性、成本结构及模型私有化要求，选择最适配的部署模式。所有部署方案均通过统一 API 接口调用，兼容标准 OpenAI 格式。

## 支持的模型/功能

- **专属部署**：为指定模型分配独立实例，适用于对隔离性、冷启延迟和数据合规性有严格要求的场景，支持自定义镜像与 VPC 网络策略。  
- **PTU 预置吞吐部署**：基于预置 Token Unit（PTU）保障稳定 QPS，适合长上下文、高并发但流量可预测的业务，详见 [PTU 预置吞吐部署](../../raw/model-user-guide/model-deployment-index/ptu-long-input-and-cache.md)。  
- **DTU 独占算力部署**：以 DTU（Dedicated Token Unit）为单位预留 GPU 算力，完全独占物理资源，适用于低延迟、高 SLA 要求的关键业务，其规格与计费逻辑在 [DTU 独占算力部署](../../raw/model-user-guide/model-deployment-index/dtu-model-deployment.md) 中明确定义。  
- **Token 按量部署**：无预付费、按实际 Token 消耗计费，适合流量波动大或验证阶段的模型服务，具体计费粒度与限流策略参见 [Token 按量部署](../../raw/model-user-guide/model-deployment-index/model-deployment-token.md)。  
- **智能路由**：自动将请求分发至最优可用模型实例（含多版本、多地域、多部署类型），支持权重灰度、故障自动降级与自定义路由规则。

## 关键参数

| 参数 | 说明 | 是否必需 | 备注 |
|------|------|----------|------|
| `model_id` | 百炼平台内模型唯一标识（如 `qwen-max-20240919`） | 是 | 必须已在 [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md) 中可见或已导入 |
| `deployment_type` | 取值：`exclusive` / `ptu` / `dtu` / `token` / `routing` | 是 | 不同类型对应不同资源配置与计费模型，不可混用 |
| `region` | 部署所在地域（如 `cn-shanghai`） | 否（默认 `cn-shanghai`） | DTU 部署必须显式指定，且不支持跨地域共享算力 |
| `max_concurrency` | 最大并发请求数（仅 exclusive / dtu 有效） | 否 | 超出时返回 `429 Too Many Requests` |

> **注意**：原始文档中 `model-deployment-quick-start.md` 描述的 API 部署流程仍以旧版 `/v1/models/deploy` 路径为例，而当前生产环境已统一迁移至 `/v1/deployments` RESTful 接口；请以 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) 的最新修订版为准，避免使用已废弃的字段如 `instance_type`。

## 使用方式

1. 在控制台「模型中心」→「我的模型」完成模型导入或启用内置模型；  
2. 进入「部署管理」→「新建部署」，选择部署类型并填写参数；  
3. 调用时在请求 Header 中携带 `Authorization: Bearer <api_key>`，Endpoint 格式为：  
   `https://dashscope.aliyuncs.com/api/v1/deployments/{deployment_id}/chat/completions`  
   （其中 `deployment_id` 由创建后返回，非 `model_id`）

## 限制和注意事项

- 所有部署类型均**不支持运行时动态切换模型权重或修改基础架构参数**（如 GPU 型号、显存大小）；变更需重建部署。  
- PTU 部署的预置吞吐量按小时结算，未用完的 PTU 不累计、不退款；DTU 部署的算力预留按分钟计费，但最小计费周期为 1 小时。  
- 模型导入功能仅支持 ONNX、Triton、PyTorch（`.pt`）格式，且必须满足 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md) 中声明的框架版本与算子兼容性约束。  
- 智能路由暂不支持跨账号模型调度，路由策略仅对同一主账号下的已部署模型生效。

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-index.md)


