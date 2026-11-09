# voice customization api directory

本目录汇总百炼平台提供的音色定制能力，涵盖音色复刻（voice cloning）与音色设计（voice design）两类核心 API。所有接口均通过统一的 `/api/v1/services/audio/tts/customization` 路径提供，但模型参数、输入结构及支持的操作因目标语音模型而异。开发者需根据所用语音合成模型（如 Qwen-Audio-TTS、CosyVoice、Qwen-Omni 等）严格匹配对应参数和流程。

## 支持的模型/功能

音色定制能力按目标语音模型划分为两类：

- **音色复刻（Voice Cloning）**：基于用户提供的参考音频生成专属音色，适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice、Qwen-Omni、Qwen-Omni-Realtime、Qwen-LiveTranslate-Realtime 和 MiniMax 模型。各模型支持的操作不同：
  - Qwen-Audio-TTS / Qwen-Audio-Realtime / CosyVoice：支持创建、查询列表、查询详情、更新、删除 [音色复刻 (raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)。
  - Qwen-Omni / Qwen-Omni-Realtime：支持创建、查询列表、删除（不支持更新）。
  - Qwen-LiveTranslate-Realtime：仅支持创建预建音色、删除预建音色。
  - MiniMax：仅支持创建（生成试听音频），不支持查询或管理音色生命周期。
- **音色设计（Voice Design）**：通过文本描述（如“沉稳的中年男性”）生成音色，当前仅支持 Qwen-Audio-TTS 和 CosyVoice 模型，支持创建、查询列表、查询详情、删除四类操作，详见 [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)。

> **注意**：文档 2 中将 `Qwen-LiveTranslate-Realtime` 归类为支持“创建音色、查询音色列表、删除音色”，但文档 5 明确其仅支持“创建预建音色、删除预建音色”，且文档 2 的“查询音色列表”表格中未列出该模型。实际行为以文档 5 和控制台行为为准，**Qwen-LiveTranslate-Realtime 不支持查询音色列表或详情**。

## 关键参数

核心参数因模型类型和操作而异，以下为高频必选/关键字段：

| 参数 | 类型 | 适用场景 | 说明 |
|------|------|----------|------|
| `model` | `string` | 全部 | 复刻固定为 `voice-enrollment`（Qwen/CosyVoice）或 `qwen-voice-enrollment`（Qwen-Omni）；设计固定为 `voice-enrollment`；MiniMax 为具体语音模型名（如 `MiniMax/speech-2.8-hd`）。 |
| `input.action` | `string` | 全部 | 复刻：`create_voice`（Qwen/CosyVoice）、`create`（Qwen-Omni）、`voice_clone`（MiniMax）；设计：`create_voice`、`list_voice`、`query_voice`、`delete_voice`。 |
| `target_model` | `string` | 全部 | 必须与后续调用语音合成时使用的模型完全一致，否则失败。例如 `cosyvoice-v3.5-plus`、`qwen3.5-omni-flash-realtime`。 |
| `audio` / `url` / `audio_url` | `string` | 复刻 | 复刻必需：Qwen/CosyVoice/Omni 接受 URL 或 Data URI；MiniMax 仅接受 `audio_url`（公网可访问）。设计不使用此参数。 |
| `voice_prompt` | `string` | 设计 | 必需，500 字符内中文/英文描述音色特征。 |
| `preview_text` | `string` | 设计 | 必需，15–200 字符，用于生成预览音频的文本。 |
| `prefix` | `string` | 复刻（Qwen/CosyVoice） & 设计 | 必需，≤10 字符，英文字母/数字，参与生成音色 ID。设计音色 ID 格式为 `{target_model}-vd-{prefix}-...`。 |
| `preferred_name` | `string` | 复刻（Qwen-Omni） | 必需，≤16 字符，英文字母/数字/下划线，用于标识音色。 |
| `text` | `string` | 复刻（Qwen-Omni） | 可选，与 `audio.data` 内容匹配的文本，用于服务端校验。 |

其他常用可选参数包括 `language_hints`（复刻语种提示）、`max_prompt_audio_length`（复刻最大音频时长）、`enable_preprocess`（是否降噪）、`sample_rate` / `response_format`（设计预览音频格式）等，详见各 SDK 文档。

## 使用方式

### 域名与鉴权
- **推荐域名**：华北2（北京）使用 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1`；新加坡使用 `https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1`。`{WorkspaceId}` 需替换为控制台业务空间详情页获取的实际 ID。
- **旧域名兼容**：`dashscope.aliyuncs.com`（国内）和 `dashscope-intl.aliyuncs.com`（国际）仍可用，但 MiniMax 模型**仅支持旧域名** [音色复刻 HTTP API 参考](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-design-http-api.md)。
- **鉴权**：请求头 `Authorization: Bearer <your_api_key>`，API Key 需与所选地域匹配。

### SDK 快速接入
- **Java**：使用 `VoiceEnrollmentService` 类（包路径 `com.alibaba.dashscope.audio.ttsv2.enrollment`），通过 `createVoice()` 等方法操作音色 [音色复刻 Java SDK 参考](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-java-sdk.md)。
- **Python**：使用 `client.audio.voices` 资源，调用 `create()`、`list()` 等方法，`workspace` 和 `region` 参数决定地域 [音色复刻 Python SDK 参考](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-python-sdk.md)。
- **HTTP**：统一 POST 到 `/api/v1/services/audio/tts/customization`，按模型要求构造 `model` 和 `input` 对象。

### 音频提交方式
- **URL**：推荐上传至 OSS 后提供公网可访问 URL。
- **Data URI**：格式 `data:<mediatype>;base64,<base64_data>`，如 `data:audio/wav;base64,...`。注意 Base64 编码后体积增大，原始文件需 ≤10 MB（Qwen-Omni）或 ≤20 MB（MiniMax）。

## 限制和注意事项

- **配额与计费**：Qwen-Audio-Realtime 复刻免费，其余模型按调用次数或音频时长计费；MiniMax 复刻会额外收取试听音频的语音合成费用 [音色复刻 HTTP API 参考](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-design-http-api.md)。
- **音频要求**：
  - Qwen-Audio/CosyVoice：推荐 10–20 秒清晰朗读，避免背景噪音；Qwen-Omni：10–60 秒，单声道，≥24 kHz 采样率，无音乐/他人声。
  - MiniMax：音频 ≥10 秒且 ≤5 分钟，格式 mp3/m4a/wav，≤20 MB。
- **地域隔离**：不同地域（北京/新加坡/国际）的 Workspace ID 和 API Key **完全独立**，不可混用。
- **音色 ID 唯一性**：MiniMax 要求 `voice_id` 全局唯一且符合命名规范（8–256 字符，首字母开头，末字符非 `-`/`_`）；其他模型由服务端自动生成。
- **状态管理**：音色设计生成后需等待 `status: "OK"` 才可使用；复刻音色创建即生效，无审核状态。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [音色复刻 HTTP API 参考](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-design-http-api.md)
- [音色复刻 Java SDK 参考](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-java-sdk.md)
- [音色复刻 Python SDK 参考](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-python-sdk.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)


