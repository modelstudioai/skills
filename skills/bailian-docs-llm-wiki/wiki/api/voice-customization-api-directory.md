# voice customization api directory

本目录汇总百炼平台支持的音色定制（voice customization）相关 API，涵盖音色复刻（voice cloning）与音色设计（voice design）两类能力。所有接口均通过 `voice-enrollment` 模型统一接入，支持 Qwen-Audio 系列（TTS/Realtime）及 CosyVoice 多版本模型。开发者可通过 HTTP API、Python SDK 或 Java SDK 进行音色的全生命周期管理（创建、查询、更新、删除），无需训练即可快速生成专属语音。

## 支持的模型与功能

当前支持以下两类音色定制方式：

- **音色复刻（Sound Re-engraving）**：基于参考音频（3–30 秒）克隆说话人音色，适用于需保留原始声纹特征的场景。支持模型包括：
  - `qwen-audio-3.0/3.1-tts-plus/flash`、`qwen-audio-3.0/3.1-realtime-plus/flash`
  - `cosyvoice-v3/v3.5-plus/flash`
  - （MiniMax 接口已归档，详见 [MiniMax](https://help.aliyun.com/zh/model-studio/mini-clone-api) 官方文档）

- **音色设计（Voice Design）**：基于文本描述（如“沉稳的中年男性”）生成全新音色，不依赖参考音频。仅支持 `voice-enrollment` 模型，输出含预览音频，适用于创意语音合成场景。

> **注意**：文档 5（[音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)）与文档 6（[Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)）在 `prefix` 命名规则上存在差异：  
> - 文档 5 中音色 ID 格式为 `{target_model}-vd-{prefix}-{id}`（含 `-vd-` 标识）；  
> - 文档 6 及其 SDK 文档（[Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)、[Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)）中为 `{target_model}-{prefix}-{id}`。  
> 实际调用以 SDK 和 HTTP API 文档为准，`-vd-` 仅用于音色设计路径，复刻路径不包含该标识。

## 关键参数

| 参数 | 类型 | 必填 | 说明 | 适用场景 |
|------|------|------|------|----------|
| `target_model` | `string` | 是 | 目标语音合成模型 ID，必须与后续 TTS/Realtime 调用一致，否则失败。 | 所有操作（create/list/query/update/delete） |
| `prefix` | `string` | 是（create）<br>否（list/query） | 音色名称前缀，仅限字母数字，≤10 字符；生成音色 ID 时自动拼接。 | create（必填）、list/query（可选筛选） |
| `audio` / `url` | `string` | 是（create/update） | 参考音频地址：支持公网 URL 或 Base64 Data URI（如 `data:audio/wav;base64,...`）。`url` 已标记为兼容旧参数，建议优先使用 `audio`。 | create、update |
| `language_hints` | `string[]` | 否 | 语种提示数组，长度必须为 1（如 `["zh"]`）。若与实际音频不符，系统自动忽略并检测。默认 `["zh"]`。 | create（复刻）、create（设计） |
| `max_prompt_audio_length` | `float` | 否 | 复刻音频最大有效时长（秒），范围 `[3.0, 30.0]`，默认 `10.0`。 | create（复刻） |
| `enable_preprocess` | `boolean` | 否 | 是否开启降噪/增强/音量规整预处理；嘈杂环境建议 `true`，安静环境建议 `false`。默认 `false`。 | create（复刻） |
| `enable_volume_normalization` | `string`（Java）<br>`bool`（Python/HTTP） | 否 | 音量归一化开关。Java SDK 传 `"true"`/`"false"`；Python/HTTP 传 `true`/`false`。默认 `"false"`（Java）或 `false`（其他）。 | create（复刻） |
| `voice_prompt` | `string` | 是（设计） | 音色描述文本（中/英文），≤500 字符，用于音色设计。 | create（设计） |
| `preview_text` | `string` | 是（设计） | 预览音频对应文本，15–200 字符，中/英文。 | create（设计） |

## 使用方式

### 接口地址
统一使用业务空间专属域名（推荐），格式为：  
- 华北2（北京）：`https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
- 新加坡：`https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`  
> `{WorkspaceId}` 需替换为控制台获取的真实 ID；不同地域 API Key 不互通。

### SDK 初始化示例（Python）
```python
import dashscope
client = dashscope.Client(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    workspace="{WorkspaceId}",  # 替换为真实 Workspace ID
    region="cn-beijing"         # 或 "ap-southeast-1"
)
# 创建复刻音色
voice = client.audio.voices.create(
    target_model="qwen-audio-3.1-tts-plus",
    prefix="myvoice",
    url="https://example.com/ref.wav",
    language_hints=["zh"]
)
```

### HTTP 请求示例（创建复刻音色）
```bash
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "cosyvoice-v3.5-plus",
        "prefix": "announcer",
        "audio": "https://example.com/ref.wav",
        "language_hints": ["zh"]
    }
}'
```

完整 SDK 接口说明请参阅 [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md) 和 [Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)。

## 限制和注意事项

- **地域与鉴权**：华北2（北京）与新加坡地域使用独立 API Key 和 Workspace ID，不可混用；SDK 的 `region` 或 Java 的 `Constants.baseHttpApiUrl` 必须与 Key 匹配。
- **音频要求**：复刻参考音频需清晰、无严重失真，时长 3–30 秒；推荐采样率 16k/24k Hz，格式 WAV/MP3；避免背景音乐与多人对话。
- **配额与计费**：Qwen-Audio-Realtime 复刻免费，但模型调用按目标模型计费；TTS/CosyVoice 复刻按次计费，具体见[配额说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。
- **音色状态**：新创建音色初始状态为 `DEPLOYING`（审核中），约数分钟内变为 `OK`（可用）或 `UNDEPLOYED`（审核失败）。设计类音色同样遵循此流程。
- **命名冲突**：同一 `target_model` + `prefix` 组合多次调用 `create` 将生成多个独立音色（ID 后缀不同），不会覆盖；如需更新，请显式调用 `update`。
- **弃用提示**：旧域名 `dashscope.aliyuncs.com` 和 `dashscope-intl.aliyuncs.com` 仍可用，但官方强烈建议迁移至业务空间专属域名以获得更高性能与稳定性。

## 来源文档

- [音色复刻](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving.md)
- [Qwen-Audio/Cosyvoice](../../raw/model-api-reference/voice-customization-api-directory/sound-reengraving/audio-voice-cloning-api-directory.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Python SDK 参考](../../raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 Java SDK 参考](../../raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md)
- [音色设计 API 参考](../../raw/model-api-reference/voice-customization-api-directory/voice-design-api-references.md)
- [Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考](../../raw/_short/voice-clone-design-http-api-b6a5abbe2d5d2730.md)


