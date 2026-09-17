# omni realtime api

Qwen-Omni-Realtime API 是基于 WebSocket 的低延迟、多模态实时交互接口，支持语音输入/输出、文本生成、图像理解及工具调用等能力。它采用事件驱动模型，客户端通过发送标准化事件（如 `session.update`、`input_audio_buffer.append`）控制会话状态与数据流，服务端通过异步事件（如 `session.created`、`response.audio.delta`）实时反馈处理结果。该 API 专为语音助手、智能客服、实时音视频交互等场景设计。

## 支持的模型/功能

当前支持以下实时系列模型，各模型能力与默认参数存在差异：

- `qwen3.5-omni-plus-realtime`：支持 `semantic_vad`、联网搜索（`enable_search`）、工具调用（`tools`），默认 `voice: "Tina"`  
- `qwen3.5-omni-flash-realtime`：支持 `server_vad`、`smooth_output`、`idle_timeout_ms`，默认 `voice: "Tina"`（文档 1 中明确标注），但 [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 均称其默认 `voice: "Cherry"` —— **注意**：此为文档矛盾，以 [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md) 中的定义为准，即 `qwen3.5-omni-flash-realtime` 默认音色为 `"Tina"`。  
- `qwen3-omni-flash-realtime`：仅支持 `server_vad`，默认 `voice: "Cherry"`（见 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 示例）  
- `qwen-omni-turbo-realtime`：不支持修改 `temperature`/`top_p`/`top_k`/`max_tokens`/`repetition_penalty`/`presence_penalty`/`seed` 等采样参数，仅支持基础对话  

核心功能包括：  
- **多模态 I/O**：支持 `["text"]` 或 `["text","audio"]` 输出；音频输入格式（`pcm`/`wav`）与采样率（`8000`–`48000 Hz`）可配置；输出音频采样率最高支持 `48000 Hz`（文档 1），但 [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md) 明确指出“当前不支持自定义输出采样率”，且示例中固定为 `24000 Hz` —— **注意**：实际可用输出采样率以服务端返回为准，客户端配置 `audio.output.format.sample_rate` 可能被忽略。  
- **语音活动检测（VAD）**：`server_vad`（全模型支持）与 `semantic_vad`（仅 `qwen3.5-omni-realtime` 系列支持）  
- **工具调用（Function Calling）**：模型自主触发函数，客户端回传结果后由服务端生成最终响应  
- **联网搜索（Search）**：仅 `qwen3.5-omni-realtime` 系列支持，与 `tools` 不兼容  
- **声音复刻集成**：需先调用声音复刻 API 创建 `voice` ID，再在 `session.update` 中指定，且 `target_model` 必须与 Omni 实时模型严格一致（见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）

## 关键参数

所有会话级参数均通过 `session.update` 事件或 SDK 的 `update_session()` 方法设置，结构化嵌套于 `session` 对象内：

- **`modalities`**：`["text"]` 或 `["text","audio"]`，决定输出模态  
- **`voice`**：音色名称，必须与所选模型兼容（如 `qwen3.5-omni-plus-realtime` 支持 `"Tina"`）  
- **`audio.input.format` / `audio.output.format`**：推荐使用嵌套结构同时指定 `type`（`pcm`/`wav`）和 `sample_rate`（Hz），历史字段 `input_audio_format`/`output_audio_format` 仍兼容但已不推荐  
- **`instructions`**：系统角色提示词，影响模型行为边界  
- **`turn_detection`**：控制 VAD 行为，含 `type`（`server_vad`/`semantic_vad`）、`threshold`（`[-1.0,1.0]`）、`silence_duration_ms`（`[200,6000]`）及 `idle_timeout_ms`（仅 `qwen3.5-omni-plus-realtime`/`flash-realtime` + `server_vad` 有效）  
- **`enable_search` & `search_options.enable_source`**：仅 `qwen3.5-omni-realtime` 系列可用，启用后模型可自主发起搜索  
- **`tools`**：工具定义数组，每个工具含 `function.name`、`description` 和 `parameters`（遵循 OpenAI Function Calling Schema）  
- **采样参数**：`temperature`、`top_p`、`top_k`、`max_tokens`、`repetition_penalty`、`presence_penalty`、`seed` —— `qwen-omni-turbo-realtime` 系列完全不可修改  

## 使用方式

1. **建立连接**：使用 WebSocket URL（如 `wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/realtime`），[Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md) 和 [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md) 均提供 `connect()` 封装  
2. **初始化会话**：连接后立即发送 `session.update` 事件（或调用 `update_session()`），配置 `modalities`、`voice`、`audio` 等参数  
3. **输入数据**：  
   - **音频**：持续发送 `input_audio_buffer.append`（Base64 PCM/WAV），VAD 模式下由服务端自动提交；Manual 模式下需显式调用 `input_audio_buffer.commit`  
   - **图像**：发送 `input_image_buffer.append`（Base64 JPG/JPEG，≤256KB），与音频缓冲区一同提交  
4. **触发响应**：VAD 模式下服务端自动触发；Manual 模式下需发送 `response.create`  
5. **处理工具调用**：收到 `conversation.item.created`（`type: "function_call"`）后，执行本地工具，再发 `conversation.item.create` 回传结果，最后发 `response.create`  
6. **流式消费输出**：监听 `response.audio.delta`（音频 Base64）、`response.text.delta`（文本）、`response.audio_transcript.delta`（ASR 中间结果）等事件  

## 限制和注意事项

- **音频限制**：输入音频建议 `16000 Hz` PCM，单次 `append` 数据量无硬限但缓冲区总大小受限；输出音频格式/采样率以服务端 `session.updated` 返回为准，客户端配置可能被覆盖  
- **图像限制**：仅 JPG/JPEG，分辨率建议 480p–720p，单图 Base64 ≤256KB，发送频率 ≤1 张/秒  
- **并发与超时**：`idle_timeout_ms` 仅对 `server_vad` + `qwen3.5-omni-plus-realtime`/`flash-realtime` 生效，范围 `[5000,30000]` ms；静默超时后服务端主动发起引导性响应  
- **功能互斥**：`tools` 与 `enable_search` 不可同时启用，否则配置校验失败  
- **模型兼容性**：声音复刻创建的 `voice` ID 必须与 Omni 实时调用的 `model` 完全匹配，否则合成失败（见 [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)）  
- **SDK 差异**：Python SDK 的 `AudioFormatConfig` 与 Java SDK 的 `OmniRealtimeConfig` 均要求通过 `parameters` Map 设置 `temperature` 等采样参数，而直接传参方式仅支持基础字段（如 `voice`、`modalities`）

## 来源文档

- [客户端事件](../../raw/model-api-reference/omni-realtime-api/client-events.md)
- [服务端事件](../../raw/model-api-reference/omni-realtime-api/server-events.md)
- [Python SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-python-sdk.md)
- [Java SDK](../../raw/model-api-reference/omni-realtime-api/omni-realtime-java-sdk.md)
- [实时多模态交互流程](../../raw/model-api-reference/omni-realtime-api/omni-realtime-interaction-process.md)
- [声音复刻API参考](../../raw/model-api-reference/omni-realtime-api/qwen-omni-voice-cloning.md)


