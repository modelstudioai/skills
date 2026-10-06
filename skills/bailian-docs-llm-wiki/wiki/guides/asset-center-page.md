# asset center page

资产中心是百炼平台中统一管理模型资产（如微调模型、推理服务、Prompt 模板等）的核心页面，为开发者提供可视化的资产生命周期操作界面。用户可通过该页面完成资产的创建、部署、版本管理、权限配置及监控查看。所有操作均通过 REST API 或控制台交互触发，底层与 Model Registry 和 Serving Engine 深度集成。

## 支持的模型/功能

- 支持托管以下类型资产：  
  - 微调后的 Qwen 系列模型（Qwen1.5、Qwen2、Qwen2.5）  
  - 自定义 ONNX/Triton 模型（需符合 [asset center](../../raw/model-user-guide/asset-center-page.md) 规定的输入输出 schema）  
  - [Prompt 工程](../concepts/prompt.md)模板（含变量注入、链式调用支持）  
  - 向量模型（仅限 `text-embedding-v3` 及兼容版本）  
- 功能包括：一键部署为 API 服务、多版本灰度发布、资产克隆、访问令牌（API Key）绑定、调用日志溯源（保留 7 天）。  
> **注意**：文档 [asset center](../../raw/model-user-guide/asset-center-page.md) 中提及的“支持 Llama 系列模型上传”已过时；当前仅允许通过模型市场导入官方认证的 Llama 衍生模型，直接上传 `.safetensors` 不被支持。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `asset_type` | string | 是 | 取值：`llm`, `embedding`, `prompt`, `custom` |
| `model_id` | string | 否 | 仅当 `asset_type=llm` 且基于已有基础模型微调时必填（如 `qwen2-7b-instruct`） |
| `runtime_config.max_concurrency` | integer | 否 | 默认 10，最大 200；超过需提工单申请 [原文标题](../../raw/model-user-guide/asset-center-page.md) |
| `serving_config.autoscale_enabled` | boolean | 否 | 默认 `true`；设为 `false` 时将固定使用 1 实例，不响应负载变化 |

## 使用方式

1. **控制台操作**：进入「模型服务」→「资产中心」→ 点击「新建资产」，按向导填写元数据并上传模型包（ZIP 或单文件）；  
2. **API 创建**：调用 `POST /v1/assets`，请求体需符合 [原文标题](../../raw/model-user-guide/asset-center-page.md) 定义的 OpenAPI Schema；  
3. **CLI 部署**（推荐 CI/CD 场景）：  
   ```bash
   baiyan asset create \
     --type llm \
     --model-id qwen2-7b-instruct \
     --path ./my-finetuned-model/ \
     --name "prod-qwen2-ft-v3"
   ```

## 限制和注意事项

- 单个资产最大体积：5 GB（压缩包解压后）；超限需分片上传或启用对象存储预置模式；  
- 模型权重文件必须位于 ZIP 根目录或 `./weights/` 子目录下，否则加载失败；  
- 所有资产默认私有，共享需显式设置 `visibility=public` 并授予目标空间读权限；  
- 资产删除后不可恢复，且关联的 API Endpoint 将立即下线（无 grace period）；  
- 若在部署中修改 `runtime_config`，需重新触发「更新服务」操作，仅保存配置不生效 —— 此行为与 [原文标题](../../raw/model-user-guide/asset-center-page.md) 描述一致。

## 来源文档

- [资产中心](../../raw/model-user-guide/asset-center-page.md)


