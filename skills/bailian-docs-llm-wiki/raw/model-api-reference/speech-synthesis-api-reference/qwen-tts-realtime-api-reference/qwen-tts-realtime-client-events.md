# 客户端事件

本文介绍 Qwen-TTS Realtime API 的客户端事件。

> 相关文档：[实时语音合成-千问](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide)。

## **session.update**

用于更新会话配置。在WebSocket连接建立成功后，可立即发送此事件作为交互的第一步。如果未发送，系统将使用默认配置。服务端成功处理此事件后，会返回`session.updated`事件作为确认。

**event\_id** `_string_` **（必选）**

客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。

```
{
    "event_id": "event_123",
    "type": "session.update",
    "session": {
        "voice": "Cherry",
        "mode": "server_commit",
        "language_type": "Chinese",
        "response_format": "pcm",
        "sample_rate": 24000,
        "instructions": "",
        "optimize_instructions": false
    }
}
```

**type** `_string_` **（必选）**

事件类型，固定为`session.update`。

**session** `_object_` （可选）

会话配置。

**属性**

**voice** `_string_` **（必选）**

语音合成所使用的音色。参见[支持的音色](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#bac280ddf5a1u)。

支持系统音色和专属音色：

-   **系统音色**：仅限千问3-TTS-Instruct-Flash-Realtime、千问3-TTS-Flash-Realtime和千问-TTS-Realtime系列模型。音色效果请参见：[支持的音色](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#bac280ddf5a1u)。
    
-   **专属音色**
    
    -   [声音复刻（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-cloning)功能定制的音色：仅限千问3-TTS-VC-Realtime系列模型
        
    -   [声音设计（Qwen）](https://help.aliyun.com/zh/model-studio/qwen-tts-voice-design)功能定制的音色：仅限千问3-TTS-VD-Realtime系列模型
        

**mode** `_string_` （可选）

交互模式，可选值：

-   `server_commit`（默认）：服务端自动判断合成时机，平衡延迟与质量，推荐大多数场景使用
    
-   `commit`：客户端手动触发合成，延迟最低，但需自行管理句子完整性
    

**language\_type** `_string_` （可选）

指定合成音频的语种，默认为 `Auto`。

-   `Auto`：适用无法确定文本的语种或文本包含多种语言的场景，模型会自动为文本中的不同语言片段匹配各自的发音，但无法保证发音完全精准。
    
-   指定语种：适用于文本为单一语种的场景，此时指定为具体语种，能显著提升合成质量，效果通常优于 `Auto`。可选值包括：
    
    -   `Chinese`
        
    -   `English`
        
    -   `German`
        
    -   `Italian`
        
    -   `Portuguese`
        
    -   `Spanish`
        
    -   `Japanese`
        
    -   `Korean`
        
    -   `French`
        
    -   `Russian`
        

**response\_format** `_string_` （可选）

模型输出音频的格式。

支持的格式：

-   `pcm`（默认）
    
-   `wav`
    
-   `mp3`
    
-   `opus`
    

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）仅支持`pcm`。

**sample\_rate** `_integer_` （可选）

模型输出音频的采样率（Hz）。

支持的采样率：

-   8000
    
-   16000
    
-   24000（默认）
    
-   48000
    

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）仅支持24000。

**speech\_rate** `_float_` （可选）

音频的语速。1.0为正常语速，小于1.0为慢速，大于1.0为快速。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

**volume** `_integer_` （可选）

音频的音量。

默认值：50。

取值范围：\[0, 100\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

**pitch\_rate** `_float_` （可选）

合成音频的语调。

默认值：1.0。

取值范围：\[0.5, 2.0\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

**bit\_rate** `_integer_` （可选）

指定音频的[码率](https://opus-codec.org/)（kbps）。码率越大，音质越好，音频文件体积越大。仅在音频格式（`response_format`）为`opus`时可用。

默认值：128。

取值范围：\[6, 510\]。

千问-TTS-Realtime（参见[支持的模型](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#a1686e997aquv)）不支持该参数。

**instructions** `_string_` （可选）

设置指令，参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

默认值：无默认值，不设置不生效。

长度限制：长度不得超过 1600 Token。

支持语言：仅支持中文和英文。

适用范围：该功能仅适用于千问3-TTS-Instruct-Flash-Realtime系列模型。

**optimize\_instructions** `_boolean_` （可选）

是否对 `instructions` 进行优化，以提升语音合成的自然度和表现力。

默认值：false。

行为说明：当设置为 true 时，系统将对 `instructions` 的内容进行语义增强与重写，生成更适合语音合成的内部指令。

适用场景：推荐在追求高品质、精细化语音表达的场景下开启。

依赖关系：此参数依赖于 `instructions` 参数被设置。如果 `instructions` 为空，此参数不生效。

适用范围：该功能仅适用于千问3-TTS-Instruct-Flash-Realtime系列模型。

## **input\_text\_buffer.append**

用于将待合成文本追加到文本缓冲区。在server\_commit模式中，文本将追加到服务端的文本缓冲区；在commit模式中，文本将追加到客户端的文本缓冲区。

**event\_id** `_string_` **（必选）**

客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。

```
{
  "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
  "type": "input_text_buffer.append",
  "text": "您好，我是千问。"
}
```

**type** `_string_` **（必选）**

事件类型，固定为`input_text_buffer.append`。

**text** `_string_` **（必选）**

待合成文本。

## **input\_text\_buffer.commit**

用于提交用户输入文本缓冲区，从而在对话中创建新的用户消息项。 如果输入的文本缓冲区为空，此事件将产生错误。处于“server\_commit”模式时，用户提交此事件，表示立即合成之前的所有文本，服务器不再缓存文本。处于“commit”模式时，客户端必须提交文本缓冲区才能创建用户消息项。提交输入文本缓冲区不会从模型创建响应，服务器将返回 `input_text_buffer.committed` 事件进行响应。

**event\_id** `_string_` **（必选）**

客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。

```
{
  "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
  "type": "input_text_buffer.commit"
}
```

**type** `_string_` **（必选）**

事件类型，固定为`input_text_buffer.commit`。

## **input\_text\_buffer.clear**

用于清除缓冲区中的文本。服务端返回`input_text_buffer.cleared` 事件进行响应。

**event\_id** `_string_` **（必选）**

客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。

```
{
  "event_id": "event_2728",
  "type": "input_text_buffer.clear"
}
```

**type** `_string_` **（必选）**

事件类型，固定为`input_text_buffer.clear`。

## session.finish

客户端发送 `session.finish` 事件通知服务端不再有文本输入，服务端将剩余音频返回，随后关闭连接。

**event\_id** `_string_` **（必选）**

客户端生成的唯一事件ID。在单次WebSocket连接会话中必须保持唯一。强烈建议使用 UUID（通用唯一标识符）。

```
{
  "event_id": "event_2239",
  "type": "session.finish"
}
```

**type** `_string_` **（必选）**

事件类型，固定为`session.finish`。
