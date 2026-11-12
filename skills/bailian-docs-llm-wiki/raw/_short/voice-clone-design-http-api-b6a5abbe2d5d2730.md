# Qwen-Audio 与 CosyVoice 音色复刻 HTTP API 参考

创建、查询、更新和删除 Qwen-Audio 与 CosyVoice 复刻音色。

本文适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice。

先[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置环境变量](https://help.aliyun.com/zh/model-studio/get-api-key#20b17d4430qvt)。请求示例读取 `DASHSCOPE_API_KEY`。使用不同 API 管理同一音色时，请使用同一账号。

SDK 定义另见 [Java SDK](raw/_short/voice-clone-java-sdk-d83b31cde2e2050b.md) 和 [Python SDK](raw/_short/voice-clone-python-sdk-e1dda5eb4e730d8e.md)。

## 接口地址

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`

将 `{WorkspaceId}` 替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)，可在百炼控制台的**业务空间详情**页面查看。北京和新加坡的 API Key 不同。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。

现有域名仍可正常使用。

## 请求头

`Authorization`string是否必选: 是

鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将"`<your_api_key>`"替换为实际的API Key。

`Content-Type`string是否必选: 是

固定为 `application/json`。

## 音频要求与费用

参考音频要求见[声音复刻用户指南](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc02_audio_h2)。Qwen-Audio-Realtime 的复刻流程见[实时语音对话音色复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#qar_vc_h3)。Qwen-Audio-Realtime 创建音色免费，模型调用按目标模型计费，详情见[计费说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_billing_h3)，数量限制见[配额说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。

## 请求体

`model`string（必选）

固定为 `voice-enrollment`。

`input`object（必选）

属性

`action`string（必选）

操作类型：

-   `create_voice`：创建音色。
-   `list_voice`：查询音色列表。
-   `query_voice`：查询音色详情。
-   `update_voice`：更新音色。
-   `delete_voice`：删除音色。

`target_model`string（创建时必选）

后续使用音色的目标模型。必须与后续调用时使用的模型一致，否则调用失败。

目标模型可选择支持声音复刻的 Qwen-Audio-TTS、Qwen-Audio-Realtime 或 CosyVoice 型号，具体模型与地域见[支持模型](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc01_scope_h2)。

`audio`string（创建或更新时，未传 `url` 则必选）

创建时提供参考音频，更新时提供新的参考音频。支持公网可访问的 URL 或 Base64 Data URI，例如 `data:audio/wav;base64,...`。

**说明**兼容旧参数 `url`；使用 `url` 时可不传 `audio`。`url` 将逐步废弃，建议改用 `audio`。

`prefix`string（创建时必选，查询列表时可选）

创建时：音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：`{target_model}-{prefix}-{唯一标识}`。

查询列表时：按前缀筛选音色。

`language_hints`array\[string\]（创建时可选）

辅助模型识别样本音频的语种，从而更准确地提取音色特征，提升复刻效果。若设置的语种与实际音频语种不符（例如为中文音频设置 `en`），系统将忽略该设置并自动检测语种。

此参数为数组，长度必须为 1。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash。

点击查看各模型支持的语言

-   qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash：
    
    -   zh：中文
    -   en：英语
    -   fr：法语
    -   de：德语
    -   ja：日语
    -   ko：韩语
    -   ru：俄语
    -   pt：葡萄牙语
    -   th：泰语
    -   id：印尼语
    -   vi：越南语
    -   it：意大利语
    -   es：西班牙语
    -   ms：马来西亚语
    -   fil：菲律宾语
    -   ar：阿拉伯语
-   cosyvoice-v3-plus：
    
    -   zh：中文
    -   en：英文
    -   fr：法语
    -   de：德语
    -   ja：日语
    -   ko：韩语
    -   ru：俄语
-   cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash：
    
    -   zh：中文
    -   en：英文
    -   fr：法语
    -   de：德语
    -   ja：日语
    -   ko：韩语
    -   ru：俄语
    -   pt：葡萄牙语
    -   th：泰语
    -   id：印尼语
    -   vi：越南语

默认值：\["zh"\]。

`max_prompt_audio_length`float（创建时可选）

音频预处理后用于声音复刻的参考音频最大时长（秒）。取值范围：\[3.0, 30.0\]。

默认值：10.0。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。

`enable_preprocess`boolean（创建时可选）

是否开启音频预处理（降噪、音频增强、音量规整）。有背景噪音时建议开启；安静环境建议关闭以最大程度还原音色。

默认值：false。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。

`enable_volume_normalization`string（创建时可选）

是否对用于声音复刻的样本音频进行音量归一化。取值：

-   `"true"`：开启音量归一化。
-   `"false"`：关闭音量归一化。

开启后，使用所创建音色合成的音频，其音量可能与关闭该参数时创建的音色不同。

默认值：`"false"`。

`page_index`integer（查询列表时可选）

页码索引。

`page_size`integer（查询列表时可选）

每页包含数据条数。

`voice_id`string（查询详情、更新或删除时必选）

要查询、更新或删除的音色 ID。

### 请求示例

#### 创建

示例使用 `qwen-audio-3.1-tts-plus`，请将 `input` 中的 `target_model` 替换为实际目标模型 ID。

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "qwen-audio-3.1-tts-plus",
        "prefix": "myvoice",
        "audio": "https://your-audio-url.wav",
        "language_hints": ["zh"],
        "enable_volume_normalization": "false"
    }
}'
```

使用本地 WAV 音频时，可通过以下代码生成 Base64 Data URI，并将 `audio` 的值填入创建或更新请求的 `input` 对象中的 `audio` 字段。将 `sample.wav` 替换为本地音频路径。

```
import base64
from pathlib import Path

audio = "data:audio/wav;base64," + base64.b64encode(
    Path("sample.wav").read_bytes()
).decode("ascii")
```

#### 查询列表

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "list_voice",
        "prefix": "myvoice",
        "page_size": 10,
        "page_index": 0
    }
}'
```

#### 查询详情

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "query_voice",
        "voice_id": "yourVoiceId"
    }
}'
```

#### 更新

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "update_voice",
        "voice_id": "yourVoiceId",
        "audio": "https://new-audio-url.wav"
    }
}'
```

#### 删除

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "delete_voice",
        "voice_id": "yourVoiceId"
    }
}'
```

## 返回体

`request_id`string

本次调用的唯一标识符。

`output`object

创建、查询列表或查询详情时返回相应字段；更新或删除时返回空对象。

属性

`voice_id`string（创建时返回）

音色 ID。

`voice_list`array\[object\]（查询列表时返回）

查询到的音色列表。

属性

`voice_id`string

音色 ID。

`gmt_create`string

创建时间。

`gmt_modified`string

修改时间。

`status`string

音色状态，取值参见"音色状态说明"。

`resource_link`string（查询详情时返回）

音频文件的URL地址。

`gmt_create`string（查询详情时返回）

创建时间。

`gmt_modified`string（查询详情时返回）

修改时间。

`status`string（查询详情时返回）

音色状态，取值参见"音色状态说明"。

`target_model`string（查询详情时返回）

驱动音色的目标模型（语音合成或实时语音对话）。

`usage`object

本次请求用量信息。

属性

`count`integer

固定为 1。创建音色时，表示创建的音色数量。

### 响应示例

#### 创建

```
{
    "output": {
        "voice_id": "qwen-audio-3.1-tts-plus-myvoice-xxxxxx"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

#### 查询列表

```
{
    "output": {
        "voice_list": [
            {
                "voice_id": "qwen-audio-3.0-tts-flash-myvoice-xxxxxx",
                "gmt_create": "2024-12-11 13:38:02",
                "gmt_modified": "2024-12-11 13:38:02",
                "status": "OK"
            }
        ]
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

#### 查询详情

```
{
    "output": {
        "gmt_create": "2024-12-11 13:38:02",
        "resource_link": "https://yourAudioFileUrl",
        "target_model": "qwen-audio-3.1-tts-plus",
        "gmt_modified": "2024-12-11 13:38:02",
        "status": "OK"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

#### 更新

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

#### 删除

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## 音色状态说明

音色创建后会经过审核流程。

**状态**

**说明**

DEPLOYING

审核中/处理中。

OK

审核通过，可正常使用。

UNDEPLOYED

审核未通过，不可使用。

## 错误信息

如遇报错问题，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行排查。

旧版 MiniMax 复刻接口说明已移至 [MiniMax HTTP API](https://help.aliyun.com/zh/model-studio/mini-clone-api)。
