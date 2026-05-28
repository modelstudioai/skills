# 3d generation

本文档介绍百炼平台基于 Tripo 模型的 3D 内容生成能力，支持文生 3D、单图生 3D 及多图生 3D 等多种输入模态。该服务采用全异步任务架构，开发者需通过标准 HTTP 接口发起任务创建与状态轮询，以获取最终的 GLB 格式模型及渲染预览图。完整接口契约与示例代码详见 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。

## 支持的模型/功能
平台当前提供两款 Tripo 模型，分别面向高精度与高性能场景：
- `Tripo/Tripo-H3.1`：高精度生成，输出面数最高 200 万，对应官方 API `v3.1-20260211`。
- `Tripo/Tripo-P1.0`：专业快速版，输出面数最高 2 万，侧重生成速度，对应官方 API `P1-20260311`。

支持三种互斥的输入方式：
- **文生 3D**：通过 `[[prompt|prompt]]`（多语言，最大 1024 字符）驱动生成。
- **单图生 3D**：传入单张公网图片 URL 提取几何与贴图。
- **多图生 3D**：传入长度为 4 的对象数组，固定视角顺序为**前、左、后、右**。缺失视角必须传入空对象 `{}`，有效图片数量需为 2~4 张。各图片分辨率与宽高比可不一致。

## 关键参数
请求体 `parameters` 对象控制输出规格，核心配置如下：
- `texture_quality`（贴图质量）：`standard`（默认/标清）或 `detailed`（高清）。
- `geometry_quality`（几何精度）：仅 `H3.1` 支持。`standard`（最高 150 万面，默认）或 `ultra`（最高 200 万面）。
- `pbr` / `texture`（材质开关）：默认均为 `true`，返回 `pbr_model_url`。若需生成无贴图的轻量化基础模型，**必须同时将两者设为 `false`**，此时返回 `base_model_url`。设为 `pbr=true` 时会强制覆盖 `texture` 为 `true`。

## 使用方式
任务流程为异步模式，需提前配置 [[API-Key]]。完整调用逻辑与状态机流转参考 [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)。
1. **创建任务 (POST)**：必须携带请求头 `X-DashScope-Async: enable`，否则将直接拦截报错。成功后返回 `task_id`，请勿重复提交。
2. **轮询状态 (GET)**：使用 `task_id` 查询接口。建议设置 **15 秒**轮询间隔。状态流转：`PENDING`（排队）→ `RUNNING`（处理中）→ `SUCCEEDED` / `FAILED`。查询接口默认限流 20 RPS，高并发场景建议配置 [[异步任务回调]]。
3. **结果下载**：任务成功后返回 `results` 数组。模型文件（`.glb`）与渲染图（`.webp`）链接有效期仅 **2 小时**，需业务侧及时持久化存储。

## 限制和注意事项
> **注意**：接口请求路径中的 `/video-generation/` 为底层网关历史分组命名，实际仅路由至 3D 生成服务，请勿与视频生成业务混淆。

- **地域强依赖**：仅支持中国内地（北京）地域，跨地域调用或混用非北京 [[API-Key]] 将鉴权失败。
- **输入限制**：图片格式限 JPEG/PNG，宽/高范围 `[20, 6000]` 像素，建议边长 > 256px，单文件大小 ≤ 20MB。
- **生命周期管理**：`task_id` 有效期为 **24 小时**，超时后查询返回 `UNKNOWN` 状态且不可恢复。建议结合 [[异步任务管理]] 进行超时清理。
- **计费统计**：仅 `SUCCEEDED` 状态计入 `usage`，返回 `3d_task_type`（任务类型）、`count`（数量）、`texture_quality` 及 `geometry_quality` 等维度。详细错误拦截规则与重试策略请查阅 [[错误码说明]]。

## 来源文档

- [Tripo-3D模型生成](../../raw/model-api-reference/3d-generation/tripo-3d-generation-api-reference.md)

