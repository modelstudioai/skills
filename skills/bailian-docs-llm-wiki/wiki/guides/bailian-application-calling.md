# bailian application calling

百炼平台支持通过 API 方式调用已发布的智能体应用（Agent Application）和工作流应用（Workflow Application），实现与业务系统的集成。调用过程需携带认证凭证、指定应用 ID，并按规范传递输入参数。所有调用均通过统一的 `/v1/applications/{app_id}/invoke` 接口发起。

## 支持的模型/功能

- **智能体应用**：基于大模型构建的对话式应用，支持多轮交互、工具调用与上下文感知，适用于客服、知识问答等场景。  
- **工作流应用**：由多个节点（如 LLM 调用、条件分支、数据处理）编排而成的确定性流程，适合结构化任务（如合同审核、报告生成）。  
- 两类应用均支持参数透传与异步回调，具体能力详见 [应用调用](../../raw/application-user-guide/bailian-application-calling.md)。注意：工作流应用暂不支持流式响应（streaming），该限制在 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling.md) 中有明确说明，而部分旧版 SDK 示例误标为支持，> **注意**：以 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling.md) 文档为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，可在控制台「应用管理」中获取 |
| `input` | object | 是 | 用户输入内容，结构由应用定义；支持文本、文件 URL、结构化字段等，详见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling.md) |
| `stream` | boolean | 否 | 仅对智能体应用有效；设为 `true` 时返回 SSE 流式响应；工作流应用强制忽略该参数 |
| `timeout` | integer | 否 | 超时时间（秒），默认 60，最大 300 |

## 使用方式

1. 获取 API Key（推荐使用短期 [Token](../concepts/token.md)，避免硬编码长期密钥）；  
2. 构造 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/applications/{app_id}/invoke`；  
3. 设置 Header：`Authorization: Bearer <api_key>`，`Content-Type: application/json`；  
4. Body 示例（智能体应用）：
   ```json
   {
     "input": {"query": "今天北京天气如何？"},
     "stream": false
   }
   ```
   工作流应用需严格匹配其定义的 input schema，参见 [应用的参数传递](../../raw/application-user-guide/bailian-application-calling.md)。

## 限制和注意事项

- 单次请求 `input` 总大小上限为 2 MB；  
- 智能体应用最大响应长度为 8192 tokens，工作流应用为 4096 tokens；  
- 调用频率限制为 10 QPS / App ID（企业版可提升），超出将返回 `429 Too Many Requests`；  
- > **注意**：文档 [应用调用](../../raw/application-user-guide/bailian-application-calling.md) 中提及的“支持自定义 HTTP 头透传”功能尚未上线，当前版本忽略所有 `x-*` 自定义 Header，该描述已过时。

## 来源文档

- [应用调用](../../raw/application-user-guide/bailian-application-calling.md)


