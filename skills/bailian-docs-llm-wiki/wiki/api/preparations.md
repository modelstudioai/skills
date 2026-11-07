# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖认证凭证获取、SDK 集成、请求地址配置等关键环节。所有 API 调用均依赖于此阶段的正确设置，缺失或错误配置将导致鉴权失败或连接异常。开发者应严格遵循各子文档指引完成初始化，尤其注意 SDK 版本与 Base URL 的匹配性。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼平台 API 提供的模型服务（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），不区分模型类型或模态。其核心功能聚焦于**客户端环境就绪性保障**，而非模型能力本身。具体支持范围详见 [使用 API](../../raw/model-api-reference/preparations.md) 文档中列出的子项。

## 关键参数

- `api_key`：必填，用于身份认证，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储  
- `base_url`：可选但强烈建议显式指定，避免因默认地址变更引发故障；不同地域/环境对应不同 endpoint，详见 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)  
- `timeout` / `max_retries`：SDK 层推荐配置，影响请求鲁棒性，具体值需结合业务场景调整  

> **注意**：`dashscope-1x-legacy-reference.md` 中描述的 `api_key` 传入方式（如全局变量 `dashscope.api_key`）在 SDK 2.x+ 已废弃，新项目必须使用实例化时传参或环境变量 `DASHSCOPE_API_KEY`，详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥  
2. **安装 SDK**：执行 `pip install dashscope`（推荐最新稳定版），旧项目迁移请参考 [SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)  
3. **初始化客户端**：显式传入 `api_key` 和 `base_url`（如需），避免隐式依赖  
4. **发起调用**：后续模型请求均基于此已准备好的客户端实例  

## 限制和注意事项

- 单个 API Key 默认有调用频率与并发数限制，超限将返回 `429 Too Many Requests` 错误，详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)  
- `base_url` 必须与所选模型部署区域一致（如 `https://dashscope.aliyuncs.com/api/v1` 为公共云通用地址，金融云需使用专属域名）  
- 不支持在浏览器前端直接使用 `api_key` —— 所有敏感凭证必须经后端代理转发，防止密钥泄露

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


