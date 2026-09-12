# more about models

本文档汇总了百炼平台模型服务的进阶能力与管理接口，涵盖模型发现、权限控制、限流配置、异步任务处理及 SDK 高级用法等开发者常用功能。所有能力均通过 Model Studio API 或 DashScope SDK 提供，适用于需要精细化管控模型调用行为的生产场景。详细实现请参考 [原文标题](../../raw/model-api-reference/more-about-models.md)。

## 支持的模型与功能

- 查询可用模型列表：调用 `GET /v1/models` 获取当前账号可访问的全部模型（含状态、类型、输入/输出限制）  
- 管理模型权限：支持为子业务空间或 RAM 角色配置细粒度模型调用授权，详见 [原文标题](../../raw/model-api-reference/more-about-models.md) 中的“查询模型授权”与“更新模型授权”  
- 异步任务支持：对长耗时模型（如视频生成、大文件解析）启用异步模式，配合回调配置实现可靠结果获取，相关接口见 [原文标题](../../raw/model-api-reference/more-about-models.md)

## 关键参数

- `model`: 必填，模型标识符（如 `qwen-max`, `qwen-vl-plus`），需与 [查询模型列表](https://help.aliyun.com/zh/model-studio/list-models) 返回的 `id` 严格一致  
- `async`: 布尔值，设为 `true` 启用异步模式，此时响应体返回 `task_id` 而非直接结果  
- `callback_url`: 异步任务回调地址，需提前在控制台配置白名单，且必须使用 HTTPS 协议  
- `workspace_id`: 子业务空间调用时必填，用于路由至对应隔离环境（参见 [子业务空间的模型调用](https://help.aliyun.com/zh/model-studio/model-calling-in-sub-workspace)）

## 使用方式

1. **获取临时 API Key**：推荐使用短期凭证降低密钥泄露风险，生成方式见 [原文标题](../../raw/model-api-reference/more-about-models.md)  
2. **初始化 SDK**：启用连接复用可显著提升高并发场景性能，需显式配置 `connection_pool_size` 和 `keep_alive` 参数（参考 [DashScope SDK连接复用配置](https://help.aliyun.com/zh/model-studio/connection-multiplexing-configuration)）  
3. **上传文件预处理**：对含图片/文档的[多模态](../concepts/multi-modal.md)请求，先调用 `POST /v1/files` 获取临时 URL，再将该 URL 传入模型请求（如 `{"image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/..."}`）

## 限制和注意事项

- 模型限流策略按 `model + workspace_id + caller_ip` 维度独立生效，需通过 [查询模型限流](https://help.aliyun.com/zh/model-studio/list-quotas) 接口确认当前配额  
- 异步任务默认保留结果 7 天，超期后 `GET /v1/tasks/{task_id}` 将返回 `404`；若需延长，须联系技术支持  
> **注意**：文档中“上传文件获取临时URL”接口返回的 URL 有效期为 15 分钟，但部分旧版 SDK 示例代码误设为 30 分钟，实际调用应以接口响应中的 `expires_at` 字段为准  
- 所有回调请求均携带 `X-DashScope-Signature` 签名头，服务端必须校验以防范伪造请求

## 来源文档

- [更多](../../raw/model-api-reference/more-about-models.md)



