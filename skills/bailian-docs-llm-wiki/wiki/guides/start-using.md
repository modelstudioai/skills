# start using

百炼平台提供零代码与低代码两种方式快速启动 AI 应用开发，支持从知识库问答构建到模型 API 调用的完整链路。开发者可基于预置模板快速部署应用，或通过 SDK/API 集成自定义逻辑。所有能力均需通过百炼控制台开通对应服务并获取 API Key。

## 支持的模型/功能

- **基础模型调用**：支持 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、Qwen2 系列及部分第三方模型（需单独开通权限）  
- **应用级能力**：知识库问答、工作流编排、Agent 工具调用、RAG 增强检索等，详见 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md)  
- **动态功能更新**：新模型上线、插件能力扩展、界面交互优化等均通过应用功能动态发布，建议定期查阅 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md)

## 关键参数

- `model`: 必填，指定模型 ID（如 `qwen-max`），不支持别名或版本通配符  
- `input`: 必填，结构为 `{ "messages": [...] }`，`messages` 为标准 OpenAI 格式数组，角色仅支持 `system`/`user`/`assistant`  
- `parameters.temperature`: 取值范围 `0.0–1.0`，默认 `0.8`；设为 `0` 时启用确定性采样（注意：[应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 中已明确标注该行为在 qwen-turbo 上存在兼容性差异）  
- `enable_search`: 仅对知识库问答类应用有效，API 调用时需配合 `retrieval_config` 使用  

> **注意**：原始文档中 `input` 的示例曾使用 `{"prompt": "..."}` 格式，但该格式已于 v2.3.0 版本废弃，当前仅接受 `messages` 数组结构——请以 [0代码构建问答应用](../../raw/application-user-guide/start-using/build-knowledge-base-qa-assistant-without-coding.md) 中最新 SDK 示例为准。

## 使用方式

1. **控制台快速启动**：登录百炼控制台 → 创建应用 → 选择模板（如“知识库问答”）→ 上传文档 → 发布  
2. **API 调用**：  
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "qwen-max",
           "input": {"messages": [{"role": "user", "content": "你好"}]},
           "parameters": {"temperature": 0.5}
         }'
   ```
3. **SDK 集成**（Python）：  
   ```python
   from dashscope import Generation
   response = Generation.call(model='qwen-max', messages=[{'role': 'user', 'content': '你好'}])
   ```

## 限制和注意事项

- 免费额度仅限新注册用户首月，后续按用量计费；模型调用频次受 `QPS` 和 `TPM` 双重限制（控制台可查实时配额）  
- 知识库问答应用中，单次上传文档大小上限为 100 MB，且不支持 `.exe`、`.bin` 等可执行文件类型  
- 所有请求必须携带有效 `Authorization` 头，`$API_KEY` 需通过控制台「API 密钥管理」生成，不可复用阿里云主账号 AK/SK  
- 模型输出长度受 `max_tokens` 参数约束（默认 2048），超出部分将被截断，无自动续写能力  

> **注意**：部分旧版教程提及“可通过环境变量 `DASHSCOPE_API_KEY` 自动注入密钥”，但该机制已在 SDK v4.0+ 中移除，强制要求显式传参——请严格参照 [应用功能动态](../../raw/application-user-guide/start-using/application-release-notes.md) 的兼容性说明进行升级。

## 来源文档

- [开始使用](../../raw/application-user-guide/start-using.md)


