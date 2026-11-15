# 模型路由与选型

模型路由与选型是百炼平台的核心横切能力，指平台根据开发者显式指定或隐式声明的模型标识、能力需求、地域约束、权限状态及运行时上下文，自动将请求分发至最匹配的后端模型实例，并确保调用符合配额、限流与服务可用性要求的过程。它不是单一 API，而是贯穿模型发现、授权、调用、异步调度与多模态适配的统一决策层。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速接入（Get Started）**：开发者在 API 调用中直接传入 `model`（如 `qwen4-max-preview`），平台依据该 ID 进行精确路由；若未指定，则默认路由至工作空间内已授权且支持当前请求类型（如 `chat`）的最优模型（如 `qwen3`），但**不推荐依赖默认行为**，应始终显式选型以保障可复现性与稳定性。  
- **模型管理（Model Management）**：通过 `/api/v1/models` 查询时，可按 `capabilities=TG&context_window>=32768&providers=qwen` 等条件筛选候选模型列表，为人工选型提供数据支撑；路由决策本身则依赖该接口返回的 `service_site`（如 `cn-beijing`）、`supports`（如 `["stream", "function_calling"]`）等元信息进行实时校验。  
- **业务场景落地（Use Cases）**：在多源混用场景（如同时调用 `qwen3-vl-plus` 图文理解 + `kimi/kimi-k3.1-pro` 深度推理），选型需兼顾模态兼容性与地域一致性——所有模型必须部署在同一地域（如北京），否则路由失败；思考模式（`enable_thinking`）等非标参数也需在选型时确认目标模型是否支持。  
- **进阶调用（More About Models）**：异步任务（图像/视频生成）和多模态输入（上传文件）会触发二级路由：先路由至文件预处理服务获取临时 URL，再将带 `X-DashScope-OssResourceResolve: enable` 头的请求路由至对应多模态模型；子业务空间调用则需在路由前完成 workspace-aware 的鉴权与地域绑定。  
- **统一抽象层（Model Experience）**：所有模型均通过 `/v1/models/{model_id}/invoke` 统一路由入口接入，`model_id` 是路由的唯一键；平台在此层完成 OpenAI 兼容参数到原生能力的自动映射（如 `temperature` → `parameters.temperature`），并拦截不支持 `stream` 的向量模型请求，实现“同接口、多模型、零适配”。

## 关键参数和配置

- **必选标识**：  
  - `model`（旧版 API）或 `model_id`（Model Experience 新版）：严格匹配控制台「服务 ID」，大小写敏感，不可模糊（如 `qwen3` ≠ `Qwen3`）；  
  - `region` / `service_site`：必须与目标模型部署地域一致（如 `cn-beijing`），跨地域请求直接拒绝，不降级路由。  

- **能力约束参数（用于筛选与校验）**：  
  - `input.messages.role`（文本）、`input.image_url`（视觉）等：决定路由至哪类模态处理器；  
  - `parameters.enable_thinking`、`parameters.reasoning_effort`：仅对标注 `features: ["reasoning"]` 的模型生效，路由时校验失败将返回 `ModelNotReady`；  
  - `stream: true`：路由层检查模型是否在 `supports` 中声明 `"stream"`，不支持则静默忽略或报错（依接口版本而定）。  

- **环境与权限配置**：  
  - `Authorization: Bearer <api_key>`：绑定主账号与业务空间，路由前校验该 Key 是否已获 `inference` 权限；  
  - `workspace_id`（HTTP Path 或 SDK 配置）：决定路由作用域，子空间无权限的模型不会出现在可选列表中；  
  - `X-DashScope-OssResourceResolve: enable`（多模态必需）：触发文件资源解析路由分支，缺失则返回 `InvalidParameter`。

## 面向开发者，简洁实用

- ✅ **始终显式指定 `model_id`**：避免依赖默认路由，尤其在灰度发布新模型（如 `qwen4-max-preview`）时，显式选型可精准控制流量。  
- ✅ **选型前查元信息**：首次集成前，用 `GET /v1/models/{model_id}` 确认 `status=ACTIVE`、`service_site` 匹配、`supports` 包含所需能力（如 `["function_calling"]`）。  
- ✅ **地域强一致**：同一业务流中调用多个模型时，务必确保它们均支持且部署于同一 `service_site`，否则路由链路中断。  
- ❌ **勿混用新旧标识**：`model_id`（如 `qwen2-72b-chat`）与旧版 `model`（如 `qwen-plus`）不可互换，新版 Model Experience 接口已废弃别名兼容。  
- ⚠️ **注意三方模型限制**：Kimi、GLM、Stepfun 等模型仅在北京地域可用，且需专用域名（`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），通用 `dashscope.aliyuncs.com` 域名将路由失败。  
- 🔧 **调试技巧**：遇到 `400 BadRequest` 或 `404 ModelNotReady`，优先检查 `model_id` 拼写、地域头、API Key 权限（`GET /api/v1/models/permissions`）及模型当前状态（控制台「模型管理」页）。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [model management](../api/model-management.md)
- [use cases](../guides/use-cases.md)
- [more about models](../api/more-about-models.md)
- [model experience](../guides/model-experience.md)


