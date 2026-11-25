# bailian application calling

百炼应用调用是将已发布的智能体应用或工作流应用通过 API 集成至业务系统的标准方式，支持同步完成（`/completion`）接口，适用于对话、任务执行等场景。调用需使用 DashScope SDK 或原生 HTTP 请求，依赖有效的 API Key 和应用 ID，并可透传业务参数以驱动插件或自定义节点逻辑。

## 支持的模型/功能

- **应用类型**：支持两类应用调用：
  - **智能体应用（Agent 1.0）**：基于大模型自主规划与[工具调用](../concepts/tool-calling.md)的轻量级智能体，适用于简单问答、工具协同等场景 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)；
  - **工作流应用（Flow Agent）**：支持可视化编排的复杂流程，包含条件分支、循环、多模态节点及插件节点，适用于结构化任务（如审批流、内容生成流水线） [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
- **核心能力**：
  - 同步响应式调用（`/completion`），返回 `output.text` 与 `usage` 统计；
  - 自定义插件参数透传（仅限智能体应用与工作流应用中的插件节点），通过 `biz_params.user_defined_params` 传递 [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)；
  - 工作流异步任务提交（共享单应用 QPS 配额，非本文档覆盖范围）。

> **注意**：文档 4 明确声明“百炼工作流不支持使用文生图大模型”，而文档 2 和 4 均未提及该限制；实际调用中若在工作流中配置了文生图节点，将直接失败。请以文档 4 的说明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)页面获取。 |
| `prompt` | string | 是 | 用户输入的初始指令或上下文，作为应用执行的起点。 |
| `biz_params` | object | 否 | 业务扩展参数对象，当前唯一受支持的子字段为 `user_defined_params`（用于插件参数透传）。格式：`{"user_defined_params": {"<plugin_code>": {"param1": value1}}}`。 |
| `parameters` | object | 否 | 空对象 `{}` 即可；暂不支持透传模型级参数（如 `temperature`），该能力由应用内部配置决定。 |
| `debug` | object | 否 | 空对象 `{}` 即可；调试信息需在百炼控制台开启，API 不接受 debug 配置。 |

> **注意**：`biz_params` 是插件参数透传的**唯一合法路径**。文档 1 中示例均严格使用 `user_defined_params` 结构；文档 2 和 4 的基础调用示例中未使用 `biz_params`，符合其“无插件”场景定位，无矛盾。

## 使用方式

### 1. 准备工作
- 获取并配置 [API Key](../../raw/model-api-reference/preparations/get-api-key.md)，推荐设为环境变量 `DASHSCOPE_API_KEY`；
- 确认应用状态为“已发布”，并复制 `APP_ID`；
- （可选）安装对应语言的 DashScope SDK（Python/Java/Node.js 等），HTTP 调用无需 SDK。

### 2. 发起调用（统一接口）
所有应用类型均使用同一 REST 接口：
```
POST https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion
```

#### Python SDK 示例（含插件参数）
```python
import os
import dashscope
client = dashscope.Client(api_key=os.getenv("DASHSCOPE_API_KEY"))

biz_params = {
    "user_defined_params": {
        "your_plugin_code": {"article_index": 2}  # 替换为真实插件ID及参数
    }
}

response = client.apps.completions.create(
    app_id='YOUR_APP_ID',
    prompt='寝室公约内容',
    biz_params=biz_params  # 仅当需透传插件参数时设置
)
print(response.text)
```

#### HTTP curl 示例（基础调用）
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

完整多语言示例（含 Java、PHP、Node.js、C#、Go）见 [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md) 与 [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。

## 限制和注意事项

- **地域限制**：工作流应用调用**仅支持华北2（北京）地域**，智能体应用无此限制（文档 4 明确标注，文档 2 未提及，属工作流特有约束）。
- **限流规则**（双维度独立生效）：
  - **单应用并发**：按 `app_id` 统计，**默认 100 QPS**；
  - **账号总流量**：同主账号下所有应用请求合并统计，**默认 15000 QPM**；
  - 触发时返回 HTTP 429 + 错误码 `Throttling.RateQuota`，建议实现指数退避重试 [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)。
- **插件参数要求**：
  - 插件工具的输入参数**传参方式必须设为“业务透传”**（文档 1 强调）；
  - 插件 ID 需与 `biz_params.user_defined_params` 中的 key 完全一致；
  - 插件描述与参数描述需用自然语言撰写，直接影响大模型调用决策。
- **安全提示**：API Key **严禁硬编码**，务必通过环境变量或密钥管理服务注入。

## 来源文档

- [应用的自定义参数传递](../../raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)
- [调用智能体应用](../../raw/application-user-guide/bailian-application-calling/call-single-agent-application.md)
- [应用限流](../../raw/application-user-guide/bailian-application-calling/flow-agent-rate-limiting.md)
- [调用工作流应用](../../raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)


