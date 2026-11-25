# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、环境准备和请求基础设施设置。开发者需先获取并安全配置 API Key，再根据目标模型选择合适的 SDK 版本与 Base URL，方可发起合法请求。所有准备工作均需严格遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档的规范流程。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼开放模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但不同模型对 SDK 版本和 Base URL 有明确要求：  
- Qwen2/Qwen3 等新版本大模型**仅支持 DashScope SDK 2.x+**，不兼容 [SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中的初始化方式；  
- 多模态模型（如 Qwen-VL）需额外确认 Base URL 是否启用 `/multimodal` 路径前缀，详见 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)。

> **注意**：[SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 文档中提及的“自动模型路由”功能在 v2.12.0 后已弃用，实际请求仍需显式指定 `model` 参数，避免因隐式路由导致 404 错误。

## 关键参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `api_key` | 是 | 通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取的密钥，须通过 HTTP Header `Authorization: Bearer <api_key>` 或 SDK 初始化传入 |
| `base_url` | 否（推荐显式指定） | 默认为 `https://dashscope.aliyuncs.com/api/v1`，但部分区域或灰度模型需覆盖为 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md) 所列专用地址 |
| `timeout` | 否 | 建议设为 ≥60s，尤其对长上下文或流式响应场景 |

## 使用方式

1. **获取密钥**：登录百炼控制台，在「API 密钥管理」中创建并复制 `api_key`；  
2. **安装 SDK**：执行 `pip install dashscope>=2.15.0`（强制要求 ≥2.15.0，旧版存在 token 刷新缺陷）；  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   # 或显式传入 base_url（如调用国际站模型）
   dashscope.base_url = "https://dashscope-intl.aliyuncs.com/api/v1"
   ```

## 限制和注意事项

- 单个 `api_key` 默认限流 10 QPS（每秒查询数），超限返回 `429 Too Many Requests`，详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；  
- `api_key` **不可硬编码在前端代码或公开仓库中**，必须通过服务端环境变量注入；  
- Windows 系统下若出现 SSL 证书验证失败，请先执行 `pip install --upgrade certifi`，否则可能中断 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 步骤。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


