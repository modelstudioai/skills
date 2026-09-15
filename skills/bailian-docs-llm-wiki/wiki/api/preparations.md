# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、开发环境配置及基础依赖安装。开发者需按顺序完成 API Key 获取、SDK 安装与初始化，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档中定义的流程规范。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼平台公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及配套能力（如流式响应、异步任务、文件上传）。不支持私有化部署模型的免鉴权调用；私有化场景需参考 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中的内网鉴权说明。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，建议通过环境变量 `DASHSCOPE_API_KEY` 注入，避免硬编码  
- `base_url`（可选）：用于私有化或代理场景，覆盖默认 `https://dashscope.aliyuncs.com/api/v1`  
- `timeout`（可选）：SDK 默认 60 秒，大模型长文本生成建议设为 ≥120 秒  

> **注意**：部分旧版 SDK 示例中将 `api_key` 作为方法参数传入（如 `Generation.call(..., api_key=...)`），但自 v1.18.0 起已废弃该方式，统一要求通过 `dashscope.api_key = ...` 或环境变量设置——详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的版本兼容性说明。

## 使用方式

1. **获取 API Key**：登录百炼控制台 →「API 密钥管理」→ 创建并复制密钥  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言 SDK（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "sk-..."  # 或设置环境变量
   ```

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误（参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）  
- 免费试用额度仅对新注册账号生效，且不可跨项目共享；额度耗尽后请求将直接失败，无降级策略  
- Windows 系统下若出现 `UnicodeDecodeError`，需确认 Python 文件编码为 UTF-8，并在 SDK 初始化前显式设置 `locale.setlocale(locale.LC_ALL, 'Chinese_China.936')`（仅限中文系统）

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


