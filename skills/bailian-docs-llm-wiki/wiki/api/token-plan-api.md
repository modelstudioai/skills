# token plan api

[Token](../concepts/token.md)Plan API 是百炼平台用于管理组织级 [Token](../concepts/token.md) 配额计划的核心接口集合，涵盖席位购买、变配、成员与组织管理、API Key 控制及用量订阅等能力。该 API 分属两个底层服务：席位购买与变配由 BssOpenApi 提供，其余功能由 ModelStudio 承载。开发者需根据操作类型选择对应服务端点和鉴权方式。

## 支持的模型/功能

[Token](../concepts/token.md)Plan API **不涉及模型推理**，而是面向平台资源治理的管理型 API，主要功能包括：
- 组织与账号生命周期管理（如创建、停用）[组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md)  
- 成员增删、角色分配与状态同步 [成员管理](../../raw/model-api-reference/token-plan-api/token-plan-api-member.md)  
- 席位（Seat）的创建、释放、升降配（含自动续费开关）[席位购买与变配](../../raw/model-api-reference/token-plan-api/token-plan-api-seat-purchase.md)  
- 邀请链接生成与状态查询 [邀请管理](../../raw/model-api-reference/token-plan-api/token-plan-api-invite.md)  
- API Key 的生成、禁用与权限范围控制 [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md)  

> **注意**：原始文档中明确指出“席位购买与变配接口属于 BssOpenApi（版本 2023-09-30），其余接口属于 ModelStudio（版本 2026-02-10）”，二者认证机制、请求域名与错误码体系不同，混用将导致 `401 Unauthorized` 或 `404 Not Found`，务必按功能归属调用对应服务。

## 关键参数

所有接口均需 `X-Api-Key` 或 `Authorization: Bearer <token>`（取决于服务）。通用关键参数包括：
- `org_id`（必填）：组织唯一标识，从 [组织与账号](../../raw/model-api-reference/token-plan-api/token-plan-api-organization.md) 接口获取  
- `seat_id`（席位类操作必填）：由 `/seats` 创建返回，非全局唯一，仅在 `org_id` 下有效  
- `plan_type`（仅席位变配）：取值 `standard` / `pro` / `enterprise`，需与当前计费周期兼容  
- `effective_time`（可选）：指定变更生效时间戳（秒级 Unix 时间），默认为立即生效  

## 使用方式

1. **鉴权准备**：  
   - ModelStudio 接口：使用组织管理员的长期 API Key（通过 [API Key 管理](../../raw/model-api-reference/token-plan-api/token-plan-api-key.md) 创建）  
   - BssOpenApi 接口：需使用阿里云 STS Token 或主账号 AK/SK 签名（参考 BssOpenApi 官方签名规范）  

2. **典型流程示例（扩容席位）**：  
   ```bash
   # 步骤1：查询当前席位（ModelStudio）
   GET https://dashscope.aliyuncs.com/api/v1/seats?org_id=org-xxx
   
   # 步骤2：调用BssOpenApi变配（需独立签名）
   POST https://business.aliyuncs.com/?Action=ModifySubscription&Version=2023-09-30
   ```

3. **SDK 支持**：  
   官方 Python SDK `dashscope` v1.22.0+ 已封装 ModelStudio 类接口；BssOpenApi 操作需依赖 `alibabacloud_bssopenapi20230930` SDK。

## 限制和注意事项

- 单次席位变配操作最小间隔为 5 分钟，高频请求将触发限流（`429 Too Many Requests`）  
- `org_id` 一旦创建不可修改，删除组织后其下所有 `seat_id` 和 `api_key` 自动失效  
- 订阅变更（如降配）仅对下一个计费周期生效，当期用量不退不补 [订阅与用量](../../raw/model-api-reference/token-plan-api/token-plan-api-subscription.md)  
- > **注意**：文档中 `ModelStudio` 版本标注为 `2026-02-10`，明显为占位符或笔误（当前实际最新版为 `2024-08-15`），请以 [API 文档中心实时版本](https://help.aliyun.com/product/42041.html) 为准，避免依赖该字段做兼容性判断。

## 来源文档

- [TokenPlan](../../raw/model-api-reference/token-plan-api.md)


