# audio api references

百炼平台提供统一的音频类 API 接口，覆盖语音合成、语音识别、音频/音乐生成、语音对话及语音翻译等核心能力。所有接口均通过 RESTful 方式调用，支持流式响应与非流式响应两种模式。开发者需根据具体任务选择对应模型，并严格遵循各接口的参数约束与计费规则。

## 支持的模型与功能

当前支持以下六大音频处理能力，每类对应独立的 API 端点与模型选型：

- **语音合成（TTS）**：支持多语种、多音色、可控语速/语调，模型包括 `qwen2-audio-tts-zh`、`qwen2-audio-tts-en` 等；详见 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md)  
- **语音识别（ASR）**：支持中英文混合识别、带标点恢复、说话人分离（部分模型），推荐使用 `qwen2-audio-asr-v1`；参考 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md)  
- **音频生成**：面向环境音、音效、提示音等非音乐类短音频生成，输入为文本描述；具体能力边界请查阅 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md)  
- **音乐生成**：支持旋律、风格、时长、BPM 等细粒度控制，输出为 WAV/MP3；[音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 文档列出了全部支持的 prompt 指令格式  
- **语音对话**：端到端实时语音交互，含唤醒、VAD、TTS 合成闭环，适用于智能硬件场景；细节见 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md)  
- **语音翻译**：支持语音→目标语言文本、语音→目标语言语音双路径，当前仅开放中英互译；参见 [语音翻译](../../raw/model-api-reference/audio-api-references/speech-translation-api-reference.md)

> **注意**：`qwen2-audio-asr-v1` 在 [语音识别](../../raw/model-api-reference/audio-api-references/speech-recognition-api-reference.md) 中标注为默认模型，但 [语音对话](../../raw/model-api-reference/audio-api-references/voice-conversation-api-references.md) 文档中提及该能力已升级至 `qwen2-audio-asr-v2` 且 v1 将于 2024-Q3 停用。请优先使用 v2 模型并适配新返回字段。

## 关键参数

所有音频 API 共享以下基础参数（必填项标 `*`）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model*` | string | 是 | 模型标识符，如 `qwen2-audio-tts-zh`，必须与所选功能匹配 |
| `input*` | object | 是 | 输入结构体，格式因功能而异（如 ASR 为 `{"audio": "base64..."}`，TTS 为 `{"text": "你好"}`） |
| `parameters` | object | 否 | 可选配置，如 `{"voice": "xiaoyan", "sample_rate": 24000}`；各模型支持字段见对应子文档 |
| `stream` | boolean | 否 | 是否启用流式响应，默认 `false`；仅 TTS、ASR、语音对话支持 `true` |

> **注意**：`parameters.sample_rate` 在 [音频生成](../../raw/model-api-reference/audio-api-references/audio-generation-api.md) 中要求必须为 `44100`，但在 [音乐生成](../../raw/model-api-reference/audio-api-references/music-generation-references.md) 中允许 `22050` 或 `44100`；若混用参数模板，请按目标接口文档校验。

## 使用方式

1. **认证**：在 HTTP Header 中携带 `Authorization: Bearer <api_key>`  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/audio/<endpoint>`，其中 `<endpoint>` 为 `speech-synthesis`、`speech-recognition` 等（与子文档路径末段一致）  
3. **Body 格式**：JSON，`input` 字段需按接口要求编码（如音频需 base64 编码且去除 `data:audio/wav;base64,` 前缀）  
4. **响应解析**：成功时返回 `200`，`output.audio`（TTS/音乐）或 `output.text`（ASR/翻译）为结果主体；流式响应需按 SSE 协议解析事件流  

示例（TTS 调用）：
```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/audio/speech-synthesis" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
        "model": "qwen2-audio-tts-zh",
        "input": {"text": "欢迎使用百炼音频服务"},
        "parameters": {"voice": "xiaoyan"}
      }'
```

## 限制和注意事项

- 单次请求音频时长上限：ASR ≤ 60 秒，TTS ≤ 300 字符（约 90 秒语音），音乐生成 ≤ 30 秒，语音对话单轮 ≤ 15 秒  
- 所有音频输入必须为 PCM/WAV/MP3 格式，采样率建议 16kHz/44.1kHz；MP3 需确保无 DRM 且为标准 CBR/VBR 编码  
- 流式接口不支持重试机制，网络中断将导致连接终止，客户端需自行实现断点续传逻辑（仅语音对话支持 session_id 恢复）  
- 计费按实际输出音频时长（秒）或识别字数（ASR）计算，非按请求次数；详细计费规则见各子文档末尾说明，例如 [语音合成](../../raw/model-api-reference/audio-api-references/speech-synthesis-api-reference.md) 的“计费说明”章节

## 来源文档

- [音频](../../raw/model-api-reference/audio-api-references.md)


