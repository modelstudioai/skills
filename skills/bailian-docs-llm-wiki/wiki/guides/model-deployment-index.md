# model deployment index

[模型部署](../concepts/model-deployment.md)是百炼平台为用户提供的核心能力，支持将大模型以不同资源模式和计费方式部署为可调用的 API 服务。本文档汇总所有部署类型、关键配置项及使用路径，适用于需要稳定推理服务、定制化资源隔离或灵活弹性扩缩容的开发者场景。部署方案的选择直接影响延迟、吞吐、成本与模型兼容性。

## 支持的模型与功能

当前支持部署的模型包括百炼平台预置的主流开源与闭源模型（如 Qwen 系列、GLM 系列），以及用户通过 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md) 功能上传的自定义模型（需符合格式与权限要求）。部署后可启用的功能因方案而异：专属部署支持长上下文与 KV Cache 优化；PTU 预置吞吐部署提供确定性延迟保障；DTU 独占算力部署支持 GPU 显存独占与 CUDA 内核级隔离；[Token](../concepts/token.md) 按量部署则面向低频、突发型请求。智能路由功能允许在多个已部署模型间按策略自动分发请求，详见 [智能路由](../../raw/model-user-guide/model-deployment-index/model-routing.md) 文档。

## 关键参数

- `deployment_type`：必填，取值为 `dedicated`（专属）、`ptu`（预置吞吐）、`dtu`（独占算力）、`token`（按量）  
- `model_id`：目标模型唯一标识，可在 [我的模型](../../raw/model-user-guide/model-deployment-index/my-model-center.md) 中查看  
- `instance_type`：仅 DTU/PTU 部署需指定，如 `ecs.gn7i-c16g1.2xlarge`；专属部署由系统自动匹配  
- `max_tokens` / `temperature` 等推理参数不在此处配置，须在 API 调用时传入  
> **注意**：原始文档中 `ptu-long-input-and-cache.md` 标题暗示 PTU 支持长输入与缓存，但实际 PTU 部署不支持 KV Cache 持久化，该能力仅限专属部署 —— 请以 [专属部署概述](../../raw/model-user-guide/model-deployment-index/model-deployment-introduction.md) 的说明为准。

## 使用方式

1. 在控制台「[模型部署](../concepts/model-deployment.md)」页选择部署类型，填写基础参数并提交  
2. 等待部署状态变为 `active`（通常 2–10 分钟）  
3. 复制生成的 `endpoint` 与 `api_key`，按 [API 部署指南](../../raw/model-user-guide/model-deployment-index/model-deployment-quick-start.md) 调用  
也可通过 OpenAPI（`CreateDeployment`）完成自动化部署，参数结构与控制台一致。

## 限制和注意事项

- [Token](../concepts/token.md) 按量部署不支持流式响应（`stream=true`）与自定义 stop 字符串  
- 所有部署类型均不支持运行时热更换模型权重（需重新部署）  
- DTU 实例一旦创建，`instance_type` 不可变更；PTU 的预置吞吐量调整需停机重启  
- 同一 `model_id` 在同一地域下最多存在 1 个活跃部署（专属/PTU/DTU 互斥，[Token](../concepts/token.md) 部署除外）  
- 自定义模型导入后，仅当通过 [模型导入](../../raw/model-user-guide/model-deployment-index/model-import.md) 完成校验并标记为“可用”，才可进入部署流程

## 来源文档

- [模型部署](../../raw/model-user-guide/model-deployment-index.md)


