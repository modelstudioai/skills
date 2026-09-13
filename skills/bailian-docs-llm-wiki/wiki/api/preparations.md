# preparations

`preparations` 是调用百炼平台 `preparations` 相关能力前必需完成的环境与凭证配置步骤，包括 API Key 获取、SDK 安装与初始化等。这些操作是所有模型调用（如文本生成、向量嵌入、RAG 预处理等）的基础前提。开发者需严格按顺序完成，否则将触发鉴权失败或客户端初始化异常。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 API 调用的模型服务，包括但不限于：`qwen-max`、`qwen-plus`、`text-embedding-v1`、`retrieval-augmentation` 等。其本身不对应独立模型，而是所有下游能力（如 [preparations](../../raw/model-api-reference/preparations.md) 中定义的预处理接口）的通用前置依赖。

## 关键参数

- `api_key`：必填，用于身份认证，需通过阿里云控制台申请并妥善保管；  
- `base_url`（可选）：当使用私有化部署或代理时需显式指定；  
- `timeout`（推荐设置）：建议设为 60s 以上，避免因网络波动导致预处理请求中断；  
- `max_retries`（推荐设置）：建议 ≥ 2，以应对临时性服务抖动。

## 使用方式

1. **获取 API Key**：登录阿里云控制台，在 Model Studio 中创建并复制 API Key；  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言 SDK；  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   ```  
   更多初始化方式详见 [使用 API](../../raw/model-api-reference/preparations.md) 文档。该文档也提供了 [SDK Expert](../../raw/model-api-reference/preparations.md) 的快速配置指引。

## 限制和注意事项

- 单个 API Key 默认 QPS 限制为 5，如需提升请提交工单申请；  
- API Key 不支持跨 Region 复用，华东 1（杭州）密钥无法在华北 2（北京）调用；  
- > **注意**：原始文档中 [错误码](../../raw/model-api-reference/preparations.md) 列表未包含 `429 Too Many Requests` 的详细重试建议，实际开发中应结合 `Retry-After` 响应头实现指数退避；  
- 本地调试时若遇到 `ConnectionResetError`，优先检查是否遗漏 `base_url` 配置（尤其在使用 VPC 内网访问时），该细节在 [使用 API](../../raw/model-api-reference/preparations.md) 中有明确说明。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


