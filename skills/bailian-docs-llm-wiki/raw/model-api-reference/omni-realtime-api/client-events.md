# 客户端事件

Qwen-Omni-Realtime API的客户端事件参考。

> 另请参见： [实时（Qwen-Omni-Realtime）](https://help.aliyun.com/zh/model-studio/realtime) 。

## **session.update**

建立 WebSocket 连接后，发送此事件更新会话的默认配置。服务端收到 `session.update` 事件后校验参数，若参数不合法则返回错误，若参数合法则应用更改并返回完整配置。

**type** `_string_`**（必选）**

事件类型，固定为 `session.update`。

```
{
    "event_id": "event_ToPZqeobitzUJnt3QqtWg",
    "type": "session.update",
    "session": {
        "modalities": [
            "text",
            "audio"
        ],
        "voice": "Chelsie",
        "input_audio_format": "pcm",
        "output_audio_format": "pcm",
        "instructions": "你是某五星级酒店的AI客服专员，请准确且友好地解答客户关于房型、设施、价格、预订政策的咨询。请始终以专业和乐于助人的态度回应，杜绝提供未经证实或超出酒店服务范围的信息。",
        "turn_detection": {
            "type": "server_vad",
            "threshold": 0.5,
            "silence_duration_ms": 800
        },
        "enable_search": true,
        "search_options": {
            "enable_source": true
        },
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "get_current_weather",
                    "description": "当你想查询指定城市的天气时非常有用。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                            }
                        },
                        "required": ["location"]
                    }
                }
            }
        ],
        "seed": 1314,
        "max_tokens": 16384,
        "repetition_penalty": 1.05,
        "presence_penalty": 0.0,
        "top_k": 50,
        "top_p": 1.0,
        "temperature": 0.9
    }
}
```

**session** `_object_`（可选）

会话配置。

**属性**

**modalities** `_array_`（可选）

模型输出模态设置，可选值：

-   \["text"\]
    
    仅输出文本。
    
-   \["text","audio"\]（默认值）
    
    同时输出文本和音频。
    

**voice** `_string_`（可选）

模型生成音频的音色，支持的音色参见[音色列表](https://help.aliyun.com/zh/model-studio/realtime#f9c68d860a3rs)。

默认音色：

-   Qwen3.5-Omni-Realtime 系列：`Tina`
    
-   Qwen3-Omni-Flash-Realtime：`Cherry`
    
-   Qwen-Omni-Turbo-Realtime：`Chelsie`
    

**input\_audio\_format** `_string_`（可选）

用户输入音频的格式，当前仅支持设为`pcm`。输入音频要求为16 kHz采样率的PCM音频流。

**output\_audio\_format** `_string_`（可选）

模型输出音频的格式，当前仅支持设为`pcm`。输出音频为24 kHz采样率的PCM音频流。当前不支持自定义输出采样率。

**smooth\_output** `_boolean｜null_`（可选）

**仅在使用 Qwen3-Omni-Flash-Realtime 系列模型时生效。**

控制回复风格。可选值：

-   `true`（默认值）：口语化风格。
    
-   `false`：书面化、正式风格。
    
    > 难以朗读的内容可能效果不好。
    
-   `null`：模型自动选择口语化或书面化风格。
    

**instructions** `_string_`（可选）

系统消息，用于设定模型的目标或角色。

**turn\_detection** `_object_`（可选）

语音活动检测（VAD）配置。设为 `null` 可禁用 VAD，改为手动触发模型响应。若不提供此字段，系统将使用默认参数启用 VAD。

**属性**

**type** `_string_`（可选）

VAD 类型，可选值：

-   `server_vad`（默认值）：基于声学特征检测语音结束。
    
-   `semantic_vad`：基于语义有效性检测语音结束，可过滤回应语、背景音等无意义声音。仅 `qwen3.5-omni-realtime` 模型支持。
    

**threshold** `_float_`（可选）

VAD 灵敏度。值越低，VAD 越灵敏，越容易将微弱声音（包括背景噪音）识别为语音；值越高，越不灵敏，需要更清晰、音量更大的语音才能触发。

取值范围：`[-1.0, 1.0]`，默认值为 0.5。

**silence\_duration\_ms** `_integer_`（可选）

语音结束后需保持静音的最短时间（毫秒），超时即触发模型响应。值越低，响应越快，但可能在短暂停顿时误触发。

取值范围：\[200, 6000\]，默认值为 800。

**enable\_search** `_boolean_`（可选）

**仅在使用 Qwen3.5-Omni-Realtime 模型时生效。**

是否启用联网搜索。设为 `true` 启用，默认为 `false`。启用后，模型可自主判断是否需要联网搜索来回答用户问题。

> tools 和 enable\_search 不兼容，不可同时开启。

**search\_options** `_object_`（可选）

联网搜索选项配置，需先启用 `enable_search` 才生效。

**属性**

**enable\_source** `_boolean_`（可选）

是否在响应中返回搜索结果来源列表。设为 `true` 启用。

**tools** `_array_`（可选）

工具定义列表。配置后模型可根据用户输入自主决定是否调用工具。

**属性**

**type** `_string_`（必选）

固定为 `function`。

**function.name** `_string_`（必选）

工具函数名称，建议与函数名保持一致，例如 `get_current_weather` 或 `get_current_time`。

**function.description** `_string_`（可选）

对工具函数功能的描述，模型据此判断是否调用该工具。

**function.parameters** `_object_`（可选）

对工具函数入参的描述，模型据此提取所需入参。若函数无需入参，可不指定。

**属性**

**type** `_string_`（必选）

固定为 `object`。

**properties** `_object_`（可选）

描述各入参的名称、数据类型与说明。Key 为入参名称，Value 为包含数据类型（`type`）和描述（`description`）的对象。

**required** `_array_`（可选）

指定哪些入参为必填项。

**temperature** `_float_`（可选）

采样温度，控制输出内容的多样性。值越高，输出越多样；值越低，输出越确定。

取值范围：\[0, 2)。

由于 temperature 和 top\_p 均可控制多样性，建议只设置其中一个。

默认值：

-   `qwen3.5-omni-realtime` 系列：0.7
    
-   `qwen3-omni-flash-realtime` 系列：0.9
    
-   `qwen-omni-turbo-realtime` 系列：1.0
    

> `qwen-omni-turbo` 系列模型**不支持修改**。

**top\_p** `_float_`（可选）

核采样概率阈值，控制输出内容的多样性。值越高，输出越多样；值越低，输出越确定。

取值范围：(0, 1.0\]。

由于 temperature 和 top\_p 均可控制多样性，建议只设置其中一个。

默认值：

-   `qwen3.5-omni-realtime` 系列：0.8
    
-   `qwen3-omni-flash-realtime` 系列：1.0
    
-   `qwen-omni-turbo-realtime` 系列：0.01
    

> `qwen-omni-turbo` 系列模型**不支持修改**。

**top\_k** `_integer_`（可选）

采样候选集大小。例如设为 50 时，每步生成仅从得分最高的 50 个 Token 中采样。值越大，随机性越高；值越小，确定性越高。设为 `null` 或大于 100 时，禁用 top\_k 策略，仅 `top_p` 生效。

取值需大于或等于 0。

默认值：

-   `qwen3.5-omni-realtime` 系列：20
    
-   `qwen3-omni-flash-realtime` 系列：50
    
-   `qwen-omni-turbo-realtime` 系列：20
    

> `qwen-omni-turbo` 系列模型**不支持修改**。

**max\_tokens** `_integer_`（可选）

本次请求返回的最大 Token 数。

> `max_tokens` 不影响模型的生成过程。若模型生成的 Token 数超过 `max_tokens`，响应将被截断。

默认值和最大值均为模型的最大输出长度，各模型的最大输出长度参见[模型列表](https://help.aliyun.com/zh/model-studio/models#9f8890ce29g5u)。

适用于需要限制输出长度的场景，如生成摘要或关键词、控制成本、缩短响应时间等。

> `qwen-omni-turbo` 系列模型**不支持修改**。

**repetition\_penalty** `_float_`（可选）

控制生成内容中连续序列的重复度。值越高，重复惩罚越强；1.0 表示不做惩罚。取值需大于 0，无严格上限。

默认值：

-   `qwen3.5-omni-realtime` 系列：1.0
    
-   `qwen3-omni-flash-realtime` 系列：1.05
    
-   `qwen-omni-turbo-realtime` 系列：1.05
    

> `qwen-omni-turbo` 系列模型**不支持修改**。

**presence\_penalty** `_float_`（可选）

控制生成内容的重复度。

取值范围：\[-2.0, 2.0\]。正数降低重复度，负数增加重复度。

默认值：

-   `qwen3.5-omni-realtime` 系列：1.5
    
-   `qwen3-omni-flash-realtime` 系列：0.0
    
-   `qwen-omni-turbo-realtime` 系列：0.0
    

适用场景：

较高值适合创意写作、头脑风暴等需要多样性和创造性的场景。

较低值适合技术文档等需要一致性和专业术语的场景。

> `qwen-omni-turbo` 系列模型**不支持修改**。

**seed** `_integer_`（可选）

提高生成过程的确定性，常用于在相同参数下复现相同结果。

每次调用时传入相同的 seed 值并保持其他参数不变，模型将尽可能返回相同的结果。

取值范围：0 到 231−1，默认值为 -1。

> `qwen-omni-turbo` 系列模型**不支持修改**。

## **response.create**

`response.create` 事件用于指示服务端生成模型响应。VAD 模式下，服务端会自动生成响应，无需发送此事件。工具调用场景中，客户端通过 `conversation.item.create` 回传工具结果后，需发送此事件触发模型生成最终响应。

服务端以 `response.created` 事件开始响应，随后发送一个或多个项和内容事件（如 `conversation.item.created` 和 `response.content_part.added`），最后以 `response.done` 事件表示响应完成。

**type** `_string_`（必选）

事件类型，固定为 `response.create`。

```
{
    "type": "response.create",
    "event_id": "event_1718624400000"
}
```

## **response.cancel**

客户端发送此事件取消正在进行的响应。若当前无响应可取消，服务端将返回错误事件。

**type** `_string_`（必选）

事件类型，固定为 `response.cancel`。

```
{
    "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
    "type": "response.cancel"
}
```

## **input\_audio\_buffer.append**

将音频字节追加到输入音频缓冲区。

**type** `_string_`（必选）

事件类型，固定为 `input_audio_buffer.append`。

```
{
    "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
    "type": "input_audio_buffer.append",
    "audio": "UklGR..."
}
```

**audio** `_string_`（必选）

Base64 编码的音频数据。

## **input\_audio\_buffer.commit**

提交输入音频缓冲区，在对话中创建新的用户消息项。若音频缓冲区为空，服务端将返回错误事件。

-   [VAD 模式](https://help.aliyun.com/zh/model-studio/realtime#68d826b358q1r)：服务端自动提交音频缓冲区，客户端无需发送此事件。
    
-   [Manual 模式](https://help.aliyun.com/zh/model-studio/realtime#3dbb650fb3ird)：客户端必须提交音频缓冲区才能创建用户消息项。
    

提交音频缓冲区不会触发模型响应，服务端将以 `input_audio_buffer.committed` 事件响应。

> 若客户端已发送过 [input\_image\_buffer.append](#c28ed38410nfw) 事件，input\_audio\_buffer.commit 事件将同时提交图像缓冲区。

**type** `_string_`（必选）

事件类型，固定为 `input_audio_buffer.commit`。

```
{
    "event_id": "event_B4o9RHSTWobB5OQdEHLTo",
    "type": "input_audio_buffer.commit"
}
```

## **input\_audio\_buffer.clear**

清除音频缓冲区中的字节。服务端以 `input_audio_buffer.cleared` 事件响应。

**type** `_string_`（必选）

事件类型，固定为 `input_audio_buffer.clear`。

```
{
    "event_id": "event_xxx",
    "type": "input_audio_buffer.clear"
}
```

## **input\_image\_buffer.append**

将图像数据添加到图像缓冲区。图像可来自本地文件，也可从视频流实时采集。

图片输入限制如下：

-   图像格式必须为 JPG 或 JPEG。建议分辨率为 480p 或 720p 以获得最佳性能，最高不超过 1080p。
    
-   单张图片经Base64编码后不得超过256KB，建议编码前原始图片大小不超过190KB。
    
-   图片数据需经过 Base64 编码。
    
-   建议以 1 张/秒的频率向服务端发送图像。
    
-   发送 input\_image\_buffer.append 事件前，至少已发送过一次 input\_audio\_buffer.append 事件。
    

> 图像缓冲区与音频缓冲区通过 [input\_audio\_buffer.commit](#1cbea5fa7fkfl) 事件一起提交。

**type** `_string_`（必选）

事件类型，固定为 `input_image_buffer.append`。

```
{
    "event_id": "event_xxx",
    "type": "input_image_buffer.append",
    "image": "xxx"
}
```

**image** `_string_`（必选）

Base64 编码的图像数据。

## **conversation.item.create**

客户端发送此事件，将工具函数的执行结果回传给服务端。模型触发工具调用后，客户端在本地执行工具函数，通过此事件将结果发回，再发送 `response.create` 触发模型生成最终响应。

**说明**

当前仅支持 `function_call_output` 类型的 item。

**type** `_string_`（必选）

事件类型，固定为 `conversation.item.create`。

```
{
    "event_id": "event_55099cddb51b4f208cb95d1a994eef80",
    "type": "conversation.item.create",
    "item": {
        "id": "item_2a80d7682b4e473c9c2154da135041e9",
        "type": "function_call_output",
        "call_id": "call_62c24725afdb4c2680ac54",
        "output": "北京今天天气为霾转晴，气温4/-4℃，微风"
    }
}
```

**item** `_object_`（必选）

要创建的对话项，不能为空。

**属性**

**id** `_string_`（可选）

对话项 ID。可预先指定以对齐本地状态；若未提供，由服务端生成。

**type** `_string_`（必选）

对话项类型，当前仅支持 `function_call_output`。

**call\_id** `_string_`（必选）

`response.function_call_arguments.done` 事件中返回的 `call_id`。

**output** `_string_`（必选）

工具函数的执行结果。

/ _支持吸顶_ /

div:has(.aliyun-docs-content),

.aliyun-docs-content .markdown-body {

overflow: visible;

}

.stick-top {

position: sticky;

top: 46px;

}

.aliyun-docs-content .one-codeblocks pre {

max-height: calc(80vh - 136px) !important;

height: auto;

}

.tab-item {

font-size: 12px !important;

/ _你可以根据需要调整字体大小_ /

padding: 0px 5px !important;

}

.expandable-content {

border-left: none !important;

border-right: none !important;

border-bottom: none !important;

}
