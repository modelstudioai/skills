# preparations

`preparations` 是调用百炼平台 `preparations` 相关能力前必需完成的环境与凭证配置步骤，涵盖 API Key 获取、SDK 安装与基础初始化。这些操作是所有模型调用（包括同步/异步推理、流式响应等）的前提条件，不执行将导致 401 或 403 错误。完整流程请参考 [使用 API](../../raw/model-api-reference/preparations.md)。

## 支持的模型/功能

当前 `preparations` 本身不绑定特定模型，而是为所有支持的模型服务，包括但不限于 `qwen-max`、`qwen-plus`、`qwen-turbo` 及 `qwen-vl` 等多模态模型。其核心作用是启用 API 访问权限与 SDK 调用链路，因此适用于全部通过 `/v1/preparations` 接口发起的预处理任务（如文档解析、结构化提取等）。具体模型兼容性详见 [使用 API](../../raw/model-api-reference/preparations.md) 中的“支持模型列表”章节。

## 关键参数

- `api_key`：必填，需通过阿里云控制台申请，不可复用其他产品密钥；  
- `base_url`：可选，默认为 `https://dashscope.aliyuncs.com/api/v1`，若使用私有部署需显式覆盖；  
- `timeout`：建议设为 ≥30 秒，因 `preparations` 操作可能涉及大文件上传或 OCR 等耗时处理；  
- `max_retries`：推荐设为 2，避免因临时网络抖动导致准备失败。  
> **注意**：部分旧版 SDK 文档中将 `model` 参数列为 `preparations` 必填项，但根据最新 [使用 API](../../raw/model-api-reference/preparations.md) 明确说明，该接口不接受 `model` 字段——此为过时信息，请忽略。

## 使用方式

1. **获取 API Key**：登录阿里云控制台，在 Model Studio → API 密钥管理中创建并复制密钥；  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言 SDK，版本需 ≥1.20.0（低于此版本不支持 `preparations` 接口）；  
3. **初始化客户端**：设置 `DASHSCOPE_API_KEY` 环境变量，或在代码中显式传入 `api_key`；  
4. **调用接口**：使用 `dashscope.preparations.create(...)` 方法提交待处理资源（如 PDF URL、Base64 图片等）。详细示例见 [使用 API](../../raw/model-api-reference/preparations.md)。

## 限制和注意事项

- 单次请求最大文件大小为 50 MB（PDF/DOCX）或 10 MB（图片），超限将返回 `InvalidParameter.FileSizeExceeded`；  
- 同一账号下 `preparations` 并发请求数上限为 10，超出将触发 `TooManyRequests` 错误；  
- 准备结果有效期为 24 小时，过期后需重新调用 `create`；  
- 不支持跨区域调用：API Key 所属地域必须与 `base_url` 指向的 endpoint 地域一致（例如华东1区 Key 需配 `dashscope.aliyuncs.com`，而非 `dashscope-intl.aliyuncs.com`）。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


