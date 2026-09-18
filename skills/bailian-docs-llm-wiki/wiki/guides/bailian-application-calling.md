# bailian [application call](../api/application-call.md)ing

百炼应用调用（bailian [application call](../api/application-call.md)ing）是指通过 DashScope SDK 或标准 HTTP API，将百炼平台创建的智能体应用（Agent 1.0）或工作流应用集成至第三方业务系统的能力。该机制统一使用 `/api/v1/apps/{app_id}/completion` 接口，支持单轮/多轮对话、自定义插件参数透传及调试能力，是生产环境对接百炼应用的核心方式。所有调用均需有效 API Key 和已发布的应用 ID。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - 智能体应用（Agent 1.0），详见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - 工作流应用（Workflow Application），详见 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心功能**：
  - 单轮文本生成（`prompt` 输入 → `output.text` 输出）；
  - 多轮对话支持两种模式：
    - 云端 `session_id` 自动管理（有效期 1 小时，最多 50 轮）；
    - 客户端 `messages` 数组显式传递（推荐，完全可控）；
  - 自定义插件参数透传（通过 `biz_params.user_defined_params` 传递插件专属参数），适用于智能体应用与工作流应用中的插件节点，详见 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 调试信息返回（启用 `debug` 字段可获取中间节点执行详情）。

> **注意**：文档 2 明确声明“百炼工作流不支持使用文生图大模型”，而文档 1 和文档 3 均未提及此限制；实际调用中若涉及多模态节点，请以文档 2 的地域与模型兼容性说明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 百炼控制台应用卡片上复制的唯一 ID，非模型 ID |
| `prompt` | string | 否（若提供 `messages` 则不可填） | 单轮指令文本；若使用 `messages` 模式则必须省略 |
| `messages` | array | 否（若提供则 `prompt` 必须省略） | 格式为 `[{"role": "user/system/assistant", "content": "..."}]`，用于显式管理多轮上下文 |
| `session_id` | string | 否 | 由服务端生成或客户端指定，用于关联历史会话（与 `messages` 同时存在时被忽略） |
| `biz_params` | object | 否 | 用于传递自定义插件参数，结构为 `{"user_defined_params": {"{plugin_code}": {...}}}` |
| `parameters` | object | 否 | 预留扩展字段，当前暂无通用参数；部分应用内节点可能识别特定 key（如 `temperature`），需以应用发布时配置为准 |
| `debug` | object | 否 | 设为空对象 `{}` 即可启用调试模式，返回各节点执行日志 |

## 使用方式

### 1. 前置准备
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 在百炼控制台创建并发布目标应用，获取其 `APP_ID`；
- 若使用 SDK，按语言安装对应版本（Python ≥ 1.14.0，Java ≥ 2.12.0）。

### 2. 调用示例（Python SDK）
```python
from dashscope import Application
import os

response = Application.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    app_id="YOUR_APP_ID",
    prompt="你是谁？"
)
if response.status_code == 200:
    print(response.output.text)
```

### 3. HTTP 调用（curl）
```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/apps/YOUR_APP_ID/completion \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {"prompt": "你是谁？"},
    "parameters": {},
    "debug": {}
  }'
```

### 4. 自定义插件调用（HTTP）
```json
{
  "input": {
    "prompt": "查询寝室公约第3条",
    "biz_params": {
      "user_defined_params": {
        "your_plugin_code": {"article_index": 3}
      }
    }
  }
}
```

## 限制和注意事项

- **地域限制**：工作流应用调用仅支持华北2（北京）地域，智能体应用无明确地域限制，但建议优先使用北京 Region endpoint（`https://dashscope.aliyuncs.com`）；
- **并发与配额**：受账号级 QPS 与 Token 总量配额约束，超出将返回 `429 Too Many Requests`，需自行实现重试与降级；
- **安全要求**：
  - 禁止硬编码 API Key，必须通过环境变量或密钥管理服务注入；
  - `biz_params` 中的插件参数需经业务校验，避免注入恶意值；
- **错误处理**：
  - 所有失败响应均含 `request_id`，用于工单排查；
  - 错误码参考 [错误码文档](https://help.aliyun.com/zh/model-studio/developer-reference/error-code)；
- **版本兼容性**：
  - SDK 版本过低可能导致 `biz_params` 解析失败或 `messages` 不生效，务必遵循各文档标注的最低版本（如文档 3 要求 Python SDK ≥ 1.14.0，文档 1/2 要求 Java SDK ≥ 2.12.0）；
  - 工作流应用不支持文生图类模型，调用含图像生成节点的应用将失败。

## 来源文档

- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)
- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)


