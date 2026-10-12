# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需按顺序完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档的流程指引。

## 支持的模型/功能

当前 `preparations` 流程适用于全部支持 API 调用的百炼模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接交互或 Playground 试用场景**。模型能力边界由实际调用的 endpoint 决定，`preparations` 本身不绑定特定模型，仅提供通用接入基础。具体模型支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK 兼容性说明。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需在请求头 `Authorization: Bearer <api_key>` 中传递  
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼服务地址；若未指定，SDK 自动使用 `https://dashscope.aliyuncs.com/api/v1`  
- `max_retries`（可选）：SDK 默认重试 2 次，可在初始化 Client 时显式设置，详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)

## 使用方式

1. **获取 API Key**：登录百炼控制台 → 进入「API 密钥管理」→ 创建并复制密钥  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言包（参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. **初始化 Client**：
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"  # 或传入 dashscope.Client(api_key=...)
   ```
   > **注意**：部分旧版文档示例中使用 `dashscope.init()`，该方法已于 v1.18.0 起废弃，请统一采用 `api_key` 属性赋值或 Client 构造函数传参，以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 为准。

## 限制和注意事项

- 单个 API Key 默认限流 60 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）  
- API Key 不可跨阿里云主账号共享，且不支持子账号独立生成（控制台权限策略限制）  
- 本地调试时若遇到 `ConnectionError`，需确认是否因企业网络策略拦截了 `dashscope.aliyuncs.com` 域名——此时应联系 IT 部门放行或配置代理，而非修改 SDK 源码  
- 所有 preparatory 操作均不产生计费，计费始于首次成功调用 `/messages` 或 `/chat/completions` 等模型 endpoint

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


