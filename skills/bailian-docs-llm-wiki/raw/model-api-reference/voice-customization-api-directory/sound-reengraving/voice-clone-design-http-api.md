# 音色复刻 HTTP API 参考

按目标模型查阅创建、查询、更新和删除音色的 HTTP 参数、响应与示例。

本文介绍音色复刻的 HTTP API。根据后续使用音色的目标模型，选择对应字段和示例。每个操作使用统一参数表，字段的类型、必选性和取值差异写在对应模型的说明中。

目标模型

本文提供的操作

Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice

创建音色、查询音色列表、查询音色详情、更新音色、删除音色

Qwen-Omni、Qwen-Omni-Realtime

创建音色、查询音色列表、删除音色

Qwen-LiveTranslate-Realtime

创建预建音色、删除预建音色

MiniMax

创建音色

先[获取 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置环境变量](https://help.aliyun.com/zh/model-studio/get-api-key#20b17d4430qvt)。请求示例读取 `DASHSCOPE_API_KEY`。使用不同 API 管理同一音色时，请使用同一账号。

## 接口地址

### Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice、Qwen-Omni、Qwen-Omni-Realtime

#### 华北2（北京）

`POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization`

#### 新加坡

`POST https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/audio/tts/customization`

将 `{WorkspaceId}` 替换为真实的[Workspace ID](https://help.aliyun.com/zh/model-studio/regions#h2_migrate_domain)，可在百炼控制台的**业务空间详情**页面查看。北京和新加坡的 API Key 不同。

**重要**阿里云百炼为华北2（北京）、新加坡地域推出了业务空间专属域名，能够为推理请求提供卓越的性能和更高的稳定性，建议迁移至新域名：

-   华北2（北京）地域：从 `dashscope.aliyuncs.com` 迁移至 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`。
-   新加坡地域：从 `dashscope-intl.aliyuncs.com` 迁移至 `{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com`。

现有域名仍可正常使用。

### Qwen-LiveTranslate-Realtime

华北2（北京）地域：

`POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization`

### MiniMax

HTTP 请求地址：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK 调用配置的 `base_url`：`https://dashscope.aliyuncs.com/api/v1`。

**说明**第三方模型（MiniMax）目前仅支持通过 `dashscope.aliyuncs.com` 域名调用，暂不支持专属域名。

## 请求头

**参数**

**类型**

**是否必选**

**说明**

Authorization

string

是

鉴权令牌，格式为`Bearer <your_api_key>`，使用时，将"`<your_api_key>`"替换为实际的API Key。

Content-Type

string

是

请求体的媒体类型。按模型系列设置：

-   Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice、Qwen-Omni、Qwen-Omni-Realtime、Qwen-LiveTranslate-Realtime：`application/json`。
-   MiniMax：`application/json; charset=utf-8`。

## 创建音色

### 音频要求与费用

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

参考音频要求见[声音复刻用户指南](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc02_audio_h2)。Qwen-Audio-Realtime 的复刻流程见[实时语音对话音色复刻](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#qar_vc_h3)。Qwen-Audio-Realtime 创建音色免费，模型调用按目标模型计费，详情见[计费说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_billing_h3)，数量限制见[配额说明](https://help.aliyun.com/zh/model-studio/voice-cloning-user-guide#vc07_quota_h2)。

**Qwen-Omni、Qwen-Omni-Realtime：**

输入音频支持 WAV（16bit）、MP3、M4A，推荐 10～20 秒，最长 60 秒，文件小于 10 MB，采样率不低于 24 kHz，且为单声道。音频必须包含至少 3 秒连续清晰朗读，停顿不超过 2 秒；整段音频应避免背景音乐、噪音或其他人声。请使用正常说话音频，不要上传歌曲或唱歌音频。支持的语种与方言见下方 `language` 参数；录制建议见[音频要求](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#fe3daa6c3f7jw)。

复刻步骤、完整示例与费用见[声音复刻用户指南](raw/model-user-guide/model-experience/omni-modal/qwen-omni-voice-cloning-user-guide.md)。

**Qwen-LiveTranslate-Realtime：**

支持 `qwen3.8-livetranslate-flash-realtime` 和 `qwen3.5-livetranslate-flash-realtime`。本节介绍提前创建音色；翻译过程中实时提取输入音色的方式见[音色配置](raw/_short/livetranslate-realtime-voice-cloning-api-508d4787359474b9.md)。提前创建音色另行计费，模型调用仍按 Token 用量计费，见[计费说明](https://help.aliyun.com/zh/model-studio/qwen3-5-livetranslate-flash-realtime#e02a82e668y2c)。参考音频使用公网可访问的 URL。

**MiniMax：**

**说明**音色复刻请求会生成一段试听音频，试听音频按所选模型的同步语音合成单价额外计费。

### 请求体

**model** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

固定为 `voice-enrollment`。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

声音复刻模型，固定为`qwen-voice-enrollment`。

**Qwen-LiveTranslate-Realtime：**

声音复刻模型，使用 `qwen-voice-enrollment`。

**MiniMax（必选）：**

指定合成试听音频使用的语音模型。

支持的模型：

-   MiniMax/speech-2.8-hd
-   MiniMax/speech-02-hd
-   MiniMax/speech-2.8-turbo
-   MiniMax/speech-02-turbo

**input** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

输入参数对象。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

输入参数对象。

**Qwen-LiveTranslate-Realtime：**

输入参数对象。

**MiniMax（必选）：**

输入参数对象。

属性

**action** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

固定为 `create_voice`。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

操作类型，固定为`create`。

**Qwen-LiveTranslate-Realtime：**

创建音色时使用 `create`。

**MiniMax（必选）：**

需要进行的操作，支持设置为：`voice_clone`（声音克隆）

**target\_model** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

驱动音色的目标模型。必须与后续使用该音色的模型一致，否则调用失败。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

驱动音色的全模态模型：

-   qwen3.8-omni-flash-realtime
-   qwen3.5-omni-plus-realtime
-   qwen3.5-omni-flash-realtime
-   qwen3.5-omni-plus
-   qwen3.5-omni-flash

必须与后续调用全模态接口时使用的模型一致，否则合成会失败。

**Qwen-LiveTranslate-Realtime：**

驱动音色的实时翻译模型，须与后续会话使用的模型一致。

**audio** `string` / `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选），类型为 `string`：**

用于复刻音色的参考音频，支持公网可访问的 URL 或 Base64 Data URI，例如 `data:audio/wav;base64,...`。

**说明**兼容旧参数 `url`；使用 `url` 时可不传 `audio`。`url` 将逐步废弃，建议改用 `audio`。

**Qwen-Omni、Qwen-Omni-Realtime（必选），类型为 `object`：**

参考音频对象。

**Qwen-LiveTranslate-Realtime，类型为 `object`：**

参考音频对象。

属性

**data** `string`

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

用于复刻的音频（录制时需遵循[录音操作指南](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#8d342f3949vge)，音频需满足[音频要求](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#fe3daa6c3f7jw)）。

可通过以下两种方式提交音频数据：

1.  [Data URL](https://www.rfc-editor.org/rfc/rfc2397)
    
    格式：`data:<mediatype>;base64,<data>`
    
    -   `<mediatype>`：MIME类型
        
        -   WAV：`audio/wav`
        -   MP3：`audio/mpeg`
        -   M4A：`audio/mp4`
    -   `<data>`：音频转成的Base64编码的字符串
        
        Base64编码会增大体积，请控制原文件大小，确保编码后仍小于10MB
        
    -   示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`
        
2.  音频URL（推荐将音频[上传至OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)）
    
    -   文件大小不超过10MB
    -   URL必须公网可访问且无需鉴权

Data URL 编码示例

python

```
import base64, pathlib

# input.mp3为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
file_path = pathlib.Path("input.mp3")
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f"data:audio/mpeg;base64,{base64_str}"
```

java

```
import java.nio.file.*;
import java.util.Base64;

public class Main {
    /**
     * filePath为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
     */
    public static String toDataUrl(String filePath) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return "data:audio/mpeg;base64," + encoded;
    }

    // 使用示例
    public static void main(String[] args) throws Exception {
        System.out.println(toDataUrl("input.mp3"));
    }
}
```

**Qwen-LiveTranslate-Realtime：**

参考音频的公网 URL。

**prefix** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

音色名称前缀，仅允许数字和英文字母，不超过10个字符。生成的音色名格式：`{target_model}-{prefix}-{唯一标识}`。

**language\_hints** `array[string]`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（可选）：**

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

**max\_prompt\_audio\_length** `float`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（可选）：**

音频预处理后用于声音复刻的参考音频最大时长（秒）。取值范围：\[3.0, 30.0\]。

默认值：10.0。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。

**enable\_preprocess** `boolean`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（可选）：**

是否开启音频预处理（降噪、音频增强、音量规整）。有背景噪音时建议开启；安静环境建议关闭以最大程度还原音色。

默认值：false。

**说明**适用于 qwen-audio-3.1-tts-plus、qwen-audio-3.1-tts-flash、qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、qwen-audio-3.1-realtime-plus、qwen-audio-3.1-realtime-flash、qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash、cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash。

**enable\_volume\_normalization** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（可选）：**

是否对用于声音复刻的样本音频进行音量归一化。取值：

-   `"true"`：开启音量归一化。
-   `"false"`：关闭音量归一化。

开启后，使用所创建音色合成的音频，其音量可能与关闭该参数时创建的音色不同。

默认值：`"false"`。

**preferred\_name** `string`

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

为音色指定一个便于识别的名称（仅允许数字、大小写字母和下划线，不超过16个字符）。建议选用与角色、场景相关的标识。

> 该关键字会在复刻的音色名中出现，例如关键字为“guanyu”，最终音色名为“qwen-omni-vc-guanyu-voice-20250812105009984-838b”

**Qwen-LiveTranslate-Realtime：**

音色名称中的标识。

**text** `string`

**Qwen-Omni、Qwen-Omni-Realtime（可选）：**

与`audio` 对象中的 `data`音频内容相匹配的文本。

传入该参数后，服务端会对比音频与该文本的差异，若差异过大，将返回Audio.PreprocessError。

**MiniMax（必选）：**

复刻声音期望试听的内容。限制 1000 字符以内。

**说明**试听将根据字符数正常收取语音合成费用，收费标准参见[MiniMax模型价格](https://help.aliyun.com/zh/model-studio/model-pricing#8296764fe3l4x)。

-   语气词标签：仅当模型选择 `speech-2.8-hd` 或 `speech-2.8-turbo` 时，支持在文本中插入语气词标签。支持的语气词：`(laughs)`（笑声）、`(chuckle)`（轻笑）、`(coughs)`（咳嗽）、`(clear-throat)`（清嗓子）、`(groans)`（呻吟）、`(breath)`（正常换气）、`(pant)`（喘气）、`(inhale)`（吸气）、`(exhale)`（呼气）、`(gasps)`（倒吸气）、`(sniffs)`（吸鼻子）、`(sighs)`（叹气）、`(snorts)`（喷鼻息）、`(burps)`（打嗝）、`(lip-smacking)`（咂嘴）、`(humming)`（哼唱）、`(hissing)`（嘶嘶声）、`(emm)`（嗯）、`(whistles)`（口哨）、`(sneezes)`（喷嚏）、`(crying)`（抽泣）、`(applause)`（鼓掌）

**language** `string`

**Qwen-Omni、Qwen-Omni-Realtime（可选）：**

`audio` 对象中的 `data`音频对应的语种。

支持`zh`（中文）、`en`（英文）、`de`（德语）、`it`（意大利语）、`pt`（葡萄牙语）、`es`（西班牙语）、`ja`（日语）、`ko`（韩语）、`fr`（法语）、`ru`（俄语）、`th`（泰语）、`id`（印尼语）、`ar`（阿拉伯语）、`cs`（捷克语）、`da`（丹麦语）、`nl`（荷兰语）、`fi`（芬兰语）、`he`（希伯来语）、`hi`（印地语）、`is`（冰岛语）、`ms`（马来语）、`no`（挪威语）、`fa`（波斯语）、`pl`（波兰语）、`sv`（瑞典语）、`tl`（他加禄语）、`tr`（土耳其语）、`ur`（乌尔都语）、`vi`（越南语）。

中文方言：`Dongbei`（东北话）、`Shannxi`（陕西话）、`Sichuan`（四川话）、`Henan`（河南话）、`Changsha`（长沙话）、`Tianjin`（天津话）、`Hangzhou`（杭州话）、`Liaoning`（辽宁话）、`Shenyang`（沈阳话）、`Anshan`（鞍山话）。

若使用该参数，设置的语种要和实际用于复刻的音频的语种一致。

**audio\_url** `string`

**MiniMax（必选）：**

需要复刻的音频文件 URL，音频需符合以下规范：

-   音频格式需为：mp3、m4a、wav 格式
-   音频的时长最少应不低于 10 秒，最长应不超过 5 分钟
-   音频文件大小需不超过 20 MB

**clone\_prompt** `object`

**MiniMax（可选）：**

音色复刻示例音频，提供本参数将有助于增强语音合成的音色相似度和稳定性。若使用本参数，需准备一小段示例音频。

属性

**prompt\_audio** `string`

**MiniMax（可选）：**

示例音频文件 URL，音频需符合以下规范：

-   音频格式需为：mp3、m4a、wav 格式
-   音频时长小于 8 秒
-   音频文件大小需不超过 20 MB

**prompt\_text** `string`

**MiniMax（可选）：**

示例音频的对应文本，需确保和音频内容一致，句末需有标点符号做结尾。

**voice\_id** `string`

**MiniMax（必选）：**

克隆音色的 voice\_id，正确示例："MiniMax001"。用户进行自定义 voice\_id 时需注意：

-   自定义的 voice\_id 长度范围\[8,256\]
-   首字符必须为英文字母
-   允许数字、字母、-、\_
-   末位字符不可为 -、\_
-   voice\_id 不可与已有 id 重复，否则会报错

**说明**该参数全局唯一，建议使用时间戳等个性化信息命名。

**language\_boost** `enum<string>`

**MiniMax（可选）：**

默认值：null。

是否增强对指定的小语种和方言的识别能力。可设置为 `auto` 让模型自主判断。

可用选项

`Chinese`, `Chinese,Yue`, `English`, `Arabic`, `Russian`, `Spanish`, `French`, `Portuguese`, `German`, `Turkish`, `Dutch`, `Ukrainian`, `Vietnamese`, `Indonesian`, `Japanese`, `Italian`, `Korean`, `Thai`, `Polish`, `Romanian`, `Greek`, `Czech`, `Finnish`, `Hindi`, `Bulgarian`, `Danish`, `Hebrew`, `Malay`, `Persian`, `Slovak`, `Swedish`, `Croatian`, `Filipino`, `Hungarian`, `Norwegian`, `Slovenian`, `Catalan`, `Nynorsk`, `Tamil`, `Afrikaans`,`auto`

**need\_noise\_reduction** `boolean`

**MiniMax（可选）：**

默认值：false。

音频复刻参数，表示是否开启降噪，默认值为 false。

**need\_volume\_normalization** `boolean`

**MiniMax（可选）：**

默认值：false。

是否开启音量归一化。

**aigc\_watermark** `boolean`

**MiniMax（可选）：**

默认值：false。

是否在合成试听音频的末尾添加音频节奏标识。

**parameters** `object`

**Qwen-Omni、Qwen-Omni-Realtime：**

配置参数对象。

属性

**voice\_clone\_mode** `string`

**Qwen-Omni、Qwen-Omni-Realtime（条件必选）：**

声音复刻模式。使用qwen3.8-omni系列模型时必传，不传时默认回退到qwen3.5-omni talker system instruct模式（兼容旧服务）。

可选值：

-   `normal`：普通模式
-   `dialect`：方言模式
-   `crosslingual`：跨语言模式

该参数需放在`parameters`中。

**skip\_audio\_process** `boolean`

**Qwen-Omni、Qwen-Omni-Realtime（可选）：**

默认值：`false`。

是否跳过音频预处理。默认为`false`。该参数需放在`parameters`中。

### 请求示例

#### qwen-audio-3.1-tts-plus

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

声音复刻

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

#### qwen-audio-3.1-realtime-plus

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

声音复刻

```
curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "qwen-audio-3.1-realtime-plus",
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

#### qwen3.8-omni-flash-realtime

cURL 示例使用音频 URL，请将 `https://xxx.wav` 替换为实际地址。Python 和 Java 示例读取本地音频，请将 `input.mp3` 替换为实际文件路径。

cURL

```
# 未配置环境变量时，将下方 $DASHSCOPE_API_KEY 替换为实际 API Key。
# ======= 重要提示 =======
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "create",
        "target_model": "qwen3.8-omni-flash-realtime",
        "preferred_name": "chinese",
        "audio": {
            "data": "https://xxx.wav"
        }
    },
    "parameters": {
        "skip_audio_process": false,
        "voice_clone_mode": "normal"
    }
}'
```

Python

```
import os
import requests
import base64, pathlib

target_model = "qwen3.8-omni-flash-realtime"
preferred_name = "guanyu"
audio_mime_type = "audio/mpeg"

file_path = pathlib.Path("input.mp3")
base64_str = base64.b64encode(file_path.read_bytes()).decode()
data_uri = f"data:{audio_mime_type};base64,{base64_str}"

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization"

payload = {
    "model": "qwen-voice-enrollment", # 不要修改这个值
    "parameters": {"voice_clone_mode": "normal"},
    "input": {
        "action": "create",
        "target_model": target_model,
        "preferred_name": preferred_name,
        "audio": {
            "data": data_uri
        }
    }
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 发送 POST 请求
resp = requests.post(url, json=payload, headers=headers)

if resp.status_code == 200:
    data = resp.json()
    voice = data["output"]["voice"]
    print(f"生成的 voice 参数为: {voice}")
else:
    print("请求失败:", resp.status_code, resp.text)
```

Java

```
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.file.*;
import java.util.Base64;

public class Main {
    private static final String TARGET_MODEL = "qwen3.8-omni-flash-realtime";
    private static final String PREFERRED_NAME = "guanyu";
    private static final String AUDIO_FILE = "input.mp3";
    private static final String AUDIO_MIME_TYPE = "audio/mpeg";

    public static String toDataUrl(String filePath) throws Exception {
        byte[] bytes = Files.readAllBytes(Paths.get(filePath));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
    }

    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx";
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        String apiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization";

        try {
            // 构造 JSON 请求体（注意内部的引号需转义）
            String jsonPayload =
                    "{"
                            + "\"model\": \"qwen-voice-enrollment\"," // 不要修改该值
                            + "\"parameters\": {\"voice_clone_mode\": \"normal\"},"
                            + "\"input\": {"
                            +     "\"action\": \"create\","
                            +     "\"target_model\": \"" + TARGET_MODEL + "\","
                            +     "\"preferred_name\": \"" + PREFERRED_NAME + "\","
                            +     "\"audio\": {"
                            +         "\"data\": \"" + toDataUrl(AUDIO_FILE) + "\""
                            +     "}"
                            + "}"
                            + "}";

            HttpURLConnection con = (HttpURLConnection) new URL(apiUrl).openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Authorization", "Bearer " + apiKey);
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            // 发送请求体
            try (OutputStream os = con.getOutputStream()) {
                os.write(jsonPayload.getBytes("UTF-8"));
            }

            int status = con.getResponseCode();
            InputStream is = (status >= 200 && status < 300)
                    ? con.getInputStream()
                    : con.getErrorStream();

            StringBuilder response = new StringBuilder();
            try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
                String line;
                while ((line = br.readLine()) != null) {
                    response.append(line);
                }
            }

            System.out.println("HTTP 状态码: " + status);
            System.out.println("返回内容: " + response.toString());

            if (status == 200) {
                // 解析 JSON
                Gson gson = new Gson();
                JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                String voice = jsonObj.getAsJsonObject("output").get("voice").getAsString();
                System.out.println("生成的 voice 参数为: " + voice);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### qwen3.8-livetranslate-flash-realtime

```
POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization
Authorization: Bearer <your_api_key>
Content-Type: application/json
```
```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen-voice-enrollment",
    "input": {
      "action": "create",
      "target_model": "qwen3.8-livetranslate-flash-realtime",
      "preferred_name": "tmtest381103",
      "audio": {
        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/cosyvoice-zeroshot-sample.wav"
      }
    }
  }'
```

#### MiniMax/speech-2.8-turbo

**说明**第三方模型（MiniMax）目前仅支持通过`dashscope.aliyuncs.com`域名调用，暂不支持专属域名

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d '{
    "input": {
      "action": "voice_clone",
      "voice_id": "bailian-test-voice-22",
      "audio_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/cosyvoice/cosyvoice-zeroshot-sample.wav",
      "text": "今天天气怎么样？"
    },
    "model": "MiniMax/speech-2.8-turbo"
  }'
```

### 返回体

**request\_id** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

本次调用的唯一标识符。

**Qwen-Omni、Qwen-Omni-Realtime：**

Request ID。

**Qwen-LiveTranslate-Realtime：**

请求 ID。

**MiniMax：**

本次调用的唯一标识符。

**output** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

模型返回的数据。

**Qwen-Omni、Qwen-Omni-Realtime：**

输出参数对象。

**Qwen-LiveTranslate-Realtime：**

输出参数对象。

**MiniMax：**

输出参数对象。

属性

**voice\_id** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

音色 ID。Qwen-Audio-TTS、CosyVoice 将其设置为语音合成接口的 `voice` 参数。Qwen-Audio-Realtime 在 `session.update` 事件的 `session` 对象中设置 `voice`，见[音色配置](https://help.aliyun.com/zh/model-studio/audio-realtime-voice-cloning-api#%E5%9C%A8%E5%AE%9E%E6%97%B6%E5%AF%B9%E8%AF%9D%E4%B8%AD%E4%BD%BF%E7%94%A8%E9%9F%B3%E8%89%B2)。

**voice** `string`

**Qwen-Omni、Qwen-Omni-Realtime：**

音色名称，可用于后续 Omni 接口的 `voice` 参数。

**Qwen-LiveTranslate-Realtime：**

创建的音色 ID，在后续翻译会话的 `voice` 中使用。

**target\_model** `string`

**Qwen-Omni、Qwen-Omni-Realtime：**

驱动音色的全模态模型：

-   qwen3.8-omni-flash-realtime
    
-   qwen3.5-omni-plus-realtime
    
-   qwen3.5-omni-flash-realtime
    
-   qwen3.5-omni-plus
    
-   qwen3.5-omni-flash
    

必须与后续调用全模态接口时使用的模型一致，否则合成会失败。

**Qwen-LiveTranslate-Realtime：**

创建音色时指定的目标模型。

**input\_sensitive** `boolean`

**MiniMax：**

输入音频是否命中风控。

**input\_sensitive\_type** `integer`

**MiniMax：**

输入音频命中风控的类型，取值为以下其一：

-   0：正常
-   1：严重违规
-   2：色情
-   3：广告
-   4：违禁
-   5：谩骂
-   6：暴恐
-   7：其他

**demo\_audio** `string`

**MiniMax：**

链接形式的试听音频。

**base\_resp** `object`

**MiniMax：**

属性

**status\_code** `integer`

**MiniMax：**

状态码

-   0: 请求结果正常
-   1000：未知错误
-   1001：超时
-   1002：触发限流
-   1004：鉴权失败
-   1013：服务内部错误
-   2013：输入格式信息不正常
-   2038：无复刻权限，请检查账号认证状态

**status\_msg** `string`

**MiniMax：**

状态详情

**usage** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

本次请求用量信息。

**Qwen-Omni、Qwen-Omni-Realtime：**

用量信息。

**MiniMax：**

本次请求的字符用量。

属性

**count** `integer`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

创建的音色数量，固定为1。

**Qwen-Omni、Qwen-Omni-Realtime：**

本次请求实际计入费用的“创建音色”次数，本次请求的费用为 count × 0.01元。

创建音色时，count恒为1。

**characters** `integer`

**MiniMax：**

输入文本的字符数。

### 响应示例

#### qwen-audio-3.1-tts-plus

声音复刻

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

#### qwen-audio-3.1-realtime-plus

声音复刻

```
{
    "output": {
        "voice_id": "qwen-audio-3.1-realtime-plus-myvoice-xxxxxx"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

#### qwen3.8-omni-flash-realtime

#### 响应结构

```
{
    "output": {
        "voice": "yourVoice",
        "target_model": "qwen3.8-omni-flash-realtime"
    },
    "usage": {
        "count": 1
    },
    "request_id": "yourRequestId"
}
```

#### 返回示例

```
{"output":{"target_model":"qwen3.8-omni-flash-realtime","voice":"qwen-omni-vc-chinese-voice-20260911161744020-3f9d"},"usage":{"count":1},"request_id":"7a36a3cb-be34-9be8-a127-df2449d51ab2"}
```

#### qwen3.8-livetranslate-flash-realtime

以下响应示例为节选。

```
{
  "output": {
    "voice": "VOICE_ID",
    "target_model": "qwen3.8-livetranslate-flash-realtime"
  },
  "request_id": "REQUEST_ID"
}
```

#### MiniMax/speech-2.8-turbo

```
{
    "output": {
        "base_resp": {
            "status_code": 0,
            "status_msg": "success"
        },
        "demo_audio": "https://minimax-algeng-chat-tts.oss-cn-wulanchabu.aliyuncs.com/audio%2Feffect%2F05fdf023562aea84632d2a8c01c2366f_1773059375796_1311.mp3?Expires=1773232175&OSSAccessKeyId=YOUR_ACCESS_KEY_ID&Signature=YOUR_SIGNATURE",
        "input_sensitive": false,
        "input_sensitive_type": 0
    },
    "usage": {
        "characters": 18
    },
    "request_id": "b1160386-ebf1-913f-9275-ef176c5e1c91"
}
```

## 查询音色列表

本节参数与示例对应以下模型：Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice；Qwen-Omni、Qwen-Omni-Realtime。

**说明**MiniMax 不支持通过本接口查询音色列表。MiniMax 的可用音色 ID（包括系统音色和复刻音色）请参见[声音管理](https://help.aliyun.com/zh/model-studio/sound-management#b447040127fbt)。

### 请求体

**model** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

固定为 `voice-enrollment`。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

声音复刻模型，固定为`qwen-voice-enrollment`。

**input** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

输入参数对象。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

输入参数对象。

属性

**action** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

固定为 `list_voice`。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

操作类型，固定为`list`。

**prefix** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（可选）：**

按前缀筛选音色。

**page\_index** `integer`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（可选）：**

页码索引。

**Qwen-Omni、Qwen-Omni-Realtime（可选）：**

默认值：`0`。

页码索引。取值范围：\[0, 1000000\]。

**page\_size** `integer`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（可选）：**

每页包含数据条数。

**Qwen-Omni、Qwen-Omni-Realtime（可选）：**

默认值：`10`。

每页包含数据条数。取值范围：\[0, 1000000\]。

**重要**`model`：声音复刻模型，固定为`qwen-voice-enrollment`，请勿修改。

### 请求示例

#### voice-enrollment（语音合成示例）

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

查询音色列表

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

#### voice-enrollment（实时对话示例）

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

查询音色列表

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

#### qwen-voice-enrollment（全模态示例）

cURL

```
# 未配置环境变量时，将下方 $DASHSCOPE_API_KEY 替换为实际 API Key。
# ======= 重要提示 =======
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "list",
        "page_size": 10,
        "page_index": 0
    }
}'
```

Python

```
import os
import requests

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization"

payload = {
    "model": "qwen-voice-enrollment", # 不要修改该值
    "input": {
        "action": "list",
        "page_size": 10,
        "page_index": 0
    }
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("HTTP 状态码:", response.status_code)

if response.status_code == 200:
    data = response.json()
    voice_list = data["output"]["voice_list"]

    print("查询到的音色列表：")
    for item in voice_list:
        print(f"- 音色: {item['voice']}  创建时间: {item['gmt_create']}  模型: {item['target_model']}")
else:
    print("请求失败:", response.text)
```

Java

```
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main {
    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx";
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        String apiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization";

        // JSON 请求体（旧版本 Java 无 """ 多行字符串）
        String jsonPayload =
                "{"
                        + "\"model\": \"qwen-voice-enrollment\"," // 不要修改该值
                        + "\"input\": {"
                        +     "\"action\": \"list\","
                        +     "\"page_size\": 10,"
                        +     "\"page_index\": 0"
                        + "}"
                        + "}";

        try {
            HttpURLConnection con = (HttpURLConnection) new URL(apiUrl).openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Authorization", "Bearer " + apiKey);
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            try (OutputStream os = con.getOutputStream()) {
                os.write(jsonPayload.getBytes("UTF-8"));
            }

            int status = con.getResponseCode();
            BufferedReader br = new BufferedReader(new InputStreamReader(
                    status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(), "UTF-8"));

            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
            br.close();

            System.out.println("HTTP 状态码: " + status);
            System.out.println("返回 JSON: " + response.toString());

            if (status == 200) {
                Gson gson = new Gson();
                JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                JsonArray voiceList = jsonObj.getAsJsonObject("output").getAsJsonArray("voice_list");

                System.out.println("\n 查询到的音色列表：");
                for (int i = 0; i < voiceList.size(); i++) {
                    JsonObject voiceItem = voiceList.get(i).getAsJsonObject();
                    String voice = voiceItem.get("voice").getAsString();
                    String gmtCreate = voiceItem.get("gmt_create").getAsString();
                    String targetModel = voiceItem.get("target_model").getAsString();

                    System.out.printf("- 音色: %s  创建时间: %s  模型: %s\n",
                            voice, gmtCreate, targetModel);
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 返回体

**request\_id** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

本次调用的唯一标识符。

**Qwen-Omni、Qwen-Omni-Realtime：**

Request ID。

**output** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

模型返回的数据。

**Qwen-Omni、Qwen-Omni-Realtime：**

输出参数对象。

属性

**voice\_list** `array[object]`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

查询到的音色列表。

**Qwen-Omni、Qwen-Omni-Realtime：**

属性

**voice\_id** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

音色 ID。Qwen-Audio-TTS、CosyVoice 将其设置为语音合成接口的 `voice` 参数。Qwen-Audio-Realtime 在 `session.update` 事件的 `session` 对象中设置 `voice`，见[音色配置](https://help.aliyun.com/zh/model-studio/audio-realtime-voice-cloning-api#%E5%9C%A8%E5%AE%9E%E6%97%B6%E5%AF%B9%E8%AF%9D%E4%B8%AD%E4%BD%BF%E7%94%A8%E9%9F%B3%E8%89%B2)。

**gmt\_create** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

创建时间。

**Qwen-Omni、Qwen-Omni-Realtime：**

创建音色的时间。

**gmt\_modified** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

修改时间。

**status** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

音色状态，取值参见"音色状态说明"。

**voice** `string`

**Qwen-Omni、Qwen-Omni-Realtime：**

音色名称，可用于后续 Omni 接口的 `voice` 参数。

**target\_model** `string`

**Qwen-Omni、Qwen-Omni-Realtime：**

驱动音色的全模态模型：

-   qwen3.8-omni-flash-realtime
    
-   qwen3.5-omni-plus-realtime
    
-   qwen3.5-omni-flash-realtime
    
-   qwen3.5-omni-plus
    
-   qwen3.5-omni-flash
    

必须与后续调用全模态接口时使用的模型一致，否则合成会失败。

**usage** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

本次请求用量信息。

**Qwen-Omni、Qwen-Omni-Realtime：**

用量信息。

属性

**count** `integer`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

固定为 1。

**Qwen-Omni、Qwen-Omni-Realtime：**

本次请求实际计入费用的“创建音色”次数，本次请求的费用为count × 0.01元。

查询音色不计费，因此`count`恒为0。

### 响应示例

#### voice-enrollment（语音合成示例）

查询音色列表

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

#### voice-enrollment（实时对话示例）

查询音色列表

```
{
    "output": {
        "voice_list": [
            {
                "voice_id": "qwen-audio-3.1-realtime-plus-myvoice-xxxxxx",
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

#### qwen-voice-enrollment（全模态示例）

```
{
    "output": {
        "voice_list": [
            {
                "voice": "yourVoice1",
                "gmt_create": "2025-08-11 17:59:32",
                "target_model": "qwen3.5-omni-plus-realtime"
            },
            {
                "voice": "yourVoice2",
                "gmt_create": "2025-08-11 17:38:10",
                "target_model": "qwen3.5-omni-plus-realtime"
            }
        ]
    },
    "usage": {
        "count": 0
    },
    "request_id": "yourRequestId"
}
```

## 查询音色详情

本节参数与示例对应以下模型：Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice。

**说明**MiniMax 不支持通过本接口查询音色详情。

### 请求体

**model** `string`

**（必选）：**

固定为 `voice-enrollment`。

**input** `object`

**（必选）：**

输入参数对象。

属性

**action** `string`

**（必选）：**

固定为`query_voice`。

**voice\_id** `string`

**（必选）：**

要查询的音色ID。

### 请求示例

#### voice-enrollment（语音合成示例）

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

#### 查询音色详情

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

#### voice-enrollment（实时对话示例）

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

#### 查询音色详情

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

### 返回体

**request\_id** `string`

本次调用的唯一标识符。

**output** `object`

模型返回的数据。

属性

**resource\_link** `string`

音频文件的URL地址。

**gmt\_create** `string`

创建时间。

**gmt\_modified** `string`

修改时间。

**status** `string`

音色状态，取值参见"音色状态说明"。

**target\_model** `string`

驱动音色的目标模型（语音合成或实时语音对话）。

**usage** `object`

本次请求用量信息。

属性

**count** `integer`

固定为1。

### 响应示例

#### voice-enrollment（语音合成示例）

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

#### voice-enrollment（实时对话示例）

```
{
    "output": {
        "gmt_create": "2024-12-11 13:38:02",
        "resource_link": "https://yourAudioFileUrl",
        "target_model": "qwen-audio-3.1-realtime-plus",
        "gmt_modified": "2024-12-11 13:38:02",
        "status": "OK"
    },
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## 更新音色

本节参数与示例对应以下模型：Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice。

**说明**MiniMax 不支持通过本接口更新音色。

### 请求体

**model** `string`

**（必选）：**

固定为 `voice-enrollment`。

**input** `object`

**（必选）：**

输入参数对象。

属性

**action** `string`

**（必选）：**

固定为`update_voice`。

**voice\_id** `string`

**（必选）：**

要更新的音色ID。

**audio** `string`

**（必选）：**

新的参考音频，支持公网可访问的 URL 或 Base64 Data URI，例如 `data:audio/wav;base64,...`。

**说明**兼容旧参数 `url`；使用 `url` 时可不传 `audio`。`url` 将逐步废弃，建议改用 `audio`。

### 请求示例

#### voice-enrollment（语音合成示例）

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

#### voice-enrollment（实时对话示例）

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

### 返回体

**request\_id** `string`

本次调用的唯一标识符。

**output** `object`

模型返回的数据，更新操作返回空对象。

**usage** `object`

本次请求用量信息。

属性

**count** `integer`

固定为1。

### 响应示例

#### voice-enrollment（语音合成示例）

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

#### voice-enrollment（实时对话示例）

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

## 删除音色

本节参数与示例对应以下模型：Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice；Qwen-Omni、Qwen-Omni-Realtime；Qwen-LiveTranslate-Realtime。

Qwen-Omni、Qwen-Omni-Realtime 删除音色后会释放对应的音色额度。

**说明**MiniMax 不支持通过本接口删除音色。MiniMax 音色的删除请参见[声音管理](https://help.aliyun.com/zh/model-studio/sound-management#62828c090dkbi)。

### 请求体

**model** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

固定为 `voice-enrollment`。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

声音复刻模型，固定为`qwen-voice-enrollment`。

**Qwen-LiveTranslate-Realtime：**

固定为 `qwen-voice-enrollment`。

**input** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

输入参数对象。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

输入参数对象。

**Qwen-LiveTranslate-Realtime：**

输入参数对象。

属性

**action** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

固定为 `delete_voice`。

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

操作类型，固定为`delete`。

**Qwen-LiveTranslate-Realtime：**

删除预建音色时使用 `delete`。

**voice\_id** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice（必选）：**

要删除的音色ID。

**voice** `string`

**Qwen-Omni、Qwen-Omni-Realtime（必选）：**

待删除的音色。

**重要**`model`：声音复刻模型，固定为`qwen-voice-enrollment`，请勿修改。

**Qwen-LiveTranslate-Realtime：**

待删除的预建音色 ID。

### 请求示例

#### voice-enrollment（语音合成示例）

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

删除音色

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

#### voice-enrollment（实时对话示例）

以下为华北2（北京）地域的配置，调用时请将"{WorkspaceId}"替换为真实的业务空间ID，各地域的配置不同。

删除音色

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

#### qwen-voice-enrollment（全模态示例）

将 `yourVoice` 替换为要删除的音色名称。

cURL

```
# 未配置环境变量时，将下方 $DASHSCOPE_API_KEY 替换为实际 API Key。
# ======= 重要提示 =======
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl --location --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
    "model": "qwen-voice-enrollment",
    "input": {
        "action": "delete",
        "voice": "yourVoice"
    }
}'
```

Python

```
import os
import requests

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
api_key = os.getenv("DASHSCOPE_API_KEY")
# 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization"

voice_to_delete = "yourVoice"  # 要删除的音色（替换为真实值）

payload = {
    "model": "qwen-voice-enrollment", # 不要修改该值
    "input": {
        "action": "delete",
        "voice": voice_to_delete
    }
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("HTTP 状态码:", response.status_code)

if response.status_code == 200:
    data = response.json()
    request_id = data["request_id"]

    print(f"删除成功")
    print(f"Request ID: {request_id}")
else:
    print("请求失败:", response.text)
```

Java

```
import com.google.gson.Gson;
import com.google.gson.JsonObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class Main {
    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx";
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        // 以下为华北2（北京）地域的URL。请将 {WorkspaceId} 替换为您的百炼业务空间ID，各地域的URL不同。
        String apiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/tts/customization";
        String voiceToDelete = "yourVoice"; // 要删除的音色（替换为真实值）

        // 构造 JSON 请求体（字符串拼接，兼容 Java 8）
        String jsonPayload =
                "{"
                        + "\"model\": \"qwen-voice-enrollment\"," // 不要修改该值
                        + "\"input\": {"
                        +     "\"action\": \"delete\","
                        +     "\"voice\": \"" + voiceToDelete + "\""
                        + "}"
                        + "}";

        try {
            // 建立 POST 连接
            HttpURLConnection con = (HttpURLConnection) new URL(apiUrl).openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Authorization", "Bearer " + apiKey);
            con.setRequestProperty("Content-Type", "application/json");
            con.setDoOutput(true);

            // 发送请求体
            try (OutputStream os = con.getOutputStream()) {
                os.write(jsonPayload.getBytes("UTF-8"));
            }

            int status = con.getResponseCode();
            BufferedReader br = new BufferedReader(new InputStreamReader(
                    status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(), "UTF-8"));

            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                response.append(line);
            }
            br.close();

            System.out.println("HTTP 状态码: " + status);
            System.out.println("返回 JSON: " + response.toString());

            if (status == 200) {
                Gson gson = new Gson();
                JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                String requestId = jsonObj.get("request_id").getAsString();

                System.out.println("删除成功");
                System.out.println("Request ID: " + requestId);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

#### qwen-voice-enrollment（预建翻译音色）

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "qwen-voice-enrollment",
    "input": {"action": "delete", "voice": "VOICE_ID"}
  }'
```

### 返回体

**request\_id** `string`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

本次调用的唯一标识符。

**Qwen-Omni、Qwen-Omni-Realtime：**

Request ID。

**output** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

模型返回的数据，为空对象。

**usage** `object`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

本次请求用量信息。

**Qwen-Omni、Qwen-Omni-Realtime：**

用量信息。

属性

**count** `integer`

**Qwen-Audio-TTS、Qwen-Audio-Realtime、CosyVoice：**

固定为1。

**Qwen-Omni、Qwen-Omni-Realtime：**

本次请求实际计入费用的“创建音色”次数，本次请求的费用为count × 0.01元。

删除音色不计费，因此`count`恒为0。

### 响应示例

#### voice-enrollment（语音合成示例）

删除音色

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

#### voice-enrollment（实时对话示例）

删除音色

```
{
    "output": {},
    "usage": {
        "count": 1
    },
    "request_id": "xxxx-xxxx-xxxx"
}
```

#### qwen-voice-enrollment（全模态示例）

```
{
    "usage": {
        "count": 0
    },
    "request_id": "yourRequestId"
}
```

## 音色状态说明

以下状态对应 Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 的 `voice-enrollment` 接口。

音色创建后会经过审核流程。以下状态适用于 Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice。

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

## 在模型调用中使用音色

-   [Qwen-Audio-Realtime 音色配置](https://help.aliyun.com/zh/model-studio/audio-realtime-voice-cloning-api#%E5%9C%A8%E5%AE%9E%E6%97%B6%E5%AF%B9%E8%AF%9D%E4%B8%AD%E4%BD%BF%E7%94%A8%E9%9F%B3%E8%89%B2)。
-   [Qwen-Omni、Qwen-Omni-Realtime 复刻流程与完整示例](https://help.aliyun.com/zh/model-studio/qwen-omni-voice-cloning-user-guide#bb60d81324wsu)。
-   [Qwen-LiveTranslate-Realtime 音色配置](https://help.aliyun.com/zh/model-studio/livetranslate-realtime-voice-cloning-api#livetranslate-voice-configuration)。

Qwen-Audio-TTS、Qwen-Audio-Realtime 和 CosyVoice 的 SDK 定义另见 [Java SDK](raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-java-sdk.md) 和 [Python SDK](raw/model-api-reference/voice-customization-api-directory/sound-reengraving/voice-clone-python-sdk.md)。
