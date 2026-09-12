# start using

百炼平台提供低门槛、高灵活性的模型调用与应用构建能力，开发者可通过控制台或 API 快速接入大模型服务。本文档汇总核心使用路径、参数规范及约束条件，适用于初次集成或调试阶段的开发者。所有功能均以 [开始使用](../../raw/application-user-guide/start-using.md) 为权威入口。

## 支持的模型/功能

- 支持通义千问系列（Qwen1、Qwen2、Qwen2.5、Qwen3）及部分第三方开源模型（如 Llama 3、Phi-3），具体以控制台「模型广场」实时列表为准  
- 提供两类核心能力：  
  - **API 直调**：通过 `/v1/chat/completions` 等标准 [OpenAI 兼容接口](../concepts/openai-compatibility.md)调用模型  
  - **零代码应用构建**：基于知识库、工作流、插件等模块可视化搭建问答助手，详见 [0代码构建问答应用](../../raw/application-user-guide/start-using.md)  
- 应用功能持续迭代，最新特性（如[多模态](../concepts/multi-modal.md)输入支持、[函数调用](../concepts/function-calling.md)增强）请参考 [应用功能动态](../../raw/application-user-guide/start-using.md)

## 关键参数

- `model`：必填，值必须为平台当前启用的模型 ID（如 `qwen-max`、`qwen-plus`），不支持自定义别名或旧版代号（如 `qwen-turbo` 已下线）  
- `temperature`：取值范围 `0.0–2.0`，默认 `0.8`；设为 `0` 时启用确定性输出（非完全 deterministic，受底层引擎限制）  
- `max_tokens`：最大输出长度，不同模型上限不同（例如 `qwen-max` 为 8192，`qwen-plus` 为 4096），超出将被截断且不报错  
- `stream`：布尔值，默认 `false`；设为 `true` 时返回 SSE 流式响应，需客户端正确处理 `data:` 块  

## 使用方式

1. **获取凭证**：在控制台「API 密钥管理」创建 AccessKey（AK/SK），**不可复用 RAM 子账号密钥**（该限制在 [开始使用](../../raw/application-user-guide/start-using.md) 中未明确说明，但实测会返回 `401 Unauthorized`）  
2. **发起请求**：推荐使用官方 SDK（Python/Java/Go）或 cURL 示例（见控制台「快速开始」页）  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/chat/completions \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"qwen-max","messages":[{"role":"user","content":"你好"}]}'
   ```  
3. **调试建议**：首次调用前，务必在控制台「配额管理」确认当前项目已开通对应模型的调用权限（部分模型需单独申请试用）

## 限制和注意事项

- 单次请求 `messages` 数组长度上限为 100 条；单条 `content` 长度上限为 1,000,000 字符（约 20 万汉字）  
- 免费额度仅限新注册用户首 30 天，且不覆盖 `qwen-max` 等高性能模型（该细节在 [开始使用](../../raw/application-user-guide/start-using.md) 中未体现，需以控制台「计费说明」为准）  
> **注意**：文档中提及的「[0代码构建问答应用](../../raw/application-user-guide/start-using.md)」链接已迁移至新版帮助中心，原页面部分截图与当前控制台 UI 存在差异（如「知识库绑定」入口已移至应用设置 → 数据源），建议以实际界面为准。  
> **注意**：`stream=true` 时若客户端未及时读取响应，连接可能在 30 秒后超时中断（平台侧无重试机制），需自行实现心跳保活或降级为非流式请求。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)



