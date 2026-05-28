# 音乐生成Fun-Music API参考

本文介绍音乐生成 Fun-Music 模型的 API 参数详情。

**用户指南**：关于模型介绍和选型建议请参见[音乐生成](https://help.aliyun.com/zh/model-studio/fun-music)。

**重要**

该模型目前处于邀测阶段，您需要前往[模型广场](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/detail/fun-music-v1)申请开通后方可使用。该功能仅在[中国内地部署范围](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)（北京地域）下可用。

## **前提条件**

已获取 API Key。获取方式请参见[获取 API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## **服务端点**

POST `https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation`

通信协议：HTTPS。流式输出支持 SSE（Server-Sent Events）。

## **请求头**

**参数名**

**类型**

**必填**

**说明**

Authorization

string

是

`Bearer {api-key}`，请替换为您的 API Key

Content-Type

string

是

`application/json`

X-DashScope-SSE

string

否

设为 `enable` 启用 SSE 流式输出

## **请求体**

## 非流式输出

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "fun-music-v1",
    "input": {
        "prompt": "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐",
        "gender": "female"
    }
}'
```

## 流式输出

```
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-H "X-DashScope-SSE: enable" \
-d '{
    "model": "fun-music-v1",
    "input": {
        "prompt": "节奏感强的电子舞曲，合成器音效，充满能量，适合健身运动场景",
        "gender": "male"
    }
}'
```

**model** `_string_` **（必选）**

模型名称，固定为 `fun-music-v1`。

**input** `_object_` **（必选）**

输入参数对象**。**

**属性**

**lyrics** `_string_` **（条件必选）**

歌词内容。与 `prompt` 二选一，至少传入其中之一。

字符限制：

-   非流式模式：中文 5~350 字符，英文 5~2000 字符
    
-   流式模式：中文 300~350 字，英文 200~250 词
    

**说明**

当同时传入 `lyrics` 和 `prompt` 时，仅 `lyrics` 生效，`prompt` 将被忽略。

**prompt** `_string_` **（条件必选）**

提示词内容，模型将根据提示词自动创作歌词并生成歌曲。与 `lyrics` 二选一。

字符限制：

-   非流式模式：1~2000 字符
    
-   流式模式：5~1000 个中文汉字或英文单词
    

**gender** `_string_` （可选） 默认值为 `female`

演唱声音的性别。可选值：

-   `male`：男声
    
-   `female`：女声
    

**format** `_string_` （可选） 默认值为 `mp3`

音频编码格式。可选值：

-   `mp3`：适合网络传输和存储
    
-   `wav`：适合后期处理和高质量播放
    

**enable\_aigc\_watermark** `_boolean_` （可选） 默认值为 `false`

AIGC 水印开关。开启后，会在生成的音频末尾追加表示“AI”的摩尔斯电码音频信号（·— ··），用于标识该音频为 AI 生成内容。开启水印会增加音频时长。

## **返回对象**

## 非流式输出

```
{
    "output": {
        "audio": {
            "data": "",
            "expires_at": 1774936147,
            "id": "audio_46c51288-7ed6-95cc-a119-xxxxxxxxxxxx",
            "url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/fun-music/20260330/xxxxxxxx/a8db24cc-d35f-961b-af81-a9e8d8b01f67.mp3?xxx"
        },
        "extra_info": {
            "channels": 2,
            "lyrics": "[verse]\n清晨的阳光穿过窗帘,\n咖啡的香气弥漫房间.\n翻开昨天未读完的书,\n时光就这样悄悄流转.\n\n[chorus]\n慢慢来不着急,\n生活本该如此惬意.\n把烦恼都丢进风里,\n拥抱每一个晴天雨季.",
            "sample_rate": 48000
        },
        "finish_reason": "stop"
    },
    "usage": {
        "duration": 200
    },
    "request_id": "46c51288-7ed6-95cc-a119-xxxxxxxxxxxx"
}
```

## 流式输出（中间消息）

```
{
    "output": {
        "audio": {
            "data": "base64 音频数据",
            "expires_at": 1774937185,
            "id": "audio_a8db24cc-d35f-961b-af81-xxxxxxxxxxxx"
        },
        "finish_reason": "null"
    },
    "request_id": "a8db24cc-d35f-961b-af81-xxxxxxxxxxxx"
}
```

## 流式输出（最终消息）

```
{
    "output": {
        "audio": {
            "expires_at": 1774937185,
            "id": "audio_a8db24cc-d35f-961b-af81-xxxxxxxxxxxx",
            "data": "",
            "url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/fun-music/20260330/xxxxxxxx/a8db24cc-d35f-961b-af81-a9e8d8b01f67.mp3?xxx"
        },
        "extra_info": {
            "channels": 2,
            "sample_rate": "48000",
            "lyrics": "[verse]\n清晨的阳光穿过窗帘,\n咖啡的香气弥漫房间.\n翻开昨天未读完的书,\n时光就这样悄悄流转.\n\n[chorus]\n慢慢来不着急,\n生活本该如此惬意.\n把烦恼都丢进风里,\n拥抱每一个晴天雨季.",
        },
        "finish_reason": "stop"
    },
    "usage": {
        "duration": 200
    },
    "request_id": "a8db24cc-d35f-961b-af81-xxxxxxxxxxxx"
}
```

**request\_id** `_string_`

请求 ID，用于问题排查和日志追踪。

**output** `_object_`

模型的输出。

**属性**

**audio** `_object_`

模型输出的音频信息。

**属性**

**data** `_string_`

流式输出时的 Base64 音频数据片段。非流式输出时为空字符串。

**url** `_string_`

完整音频文件的 OSS URL，有效期 24 小时。非流式模式下直接返回；流式模式下仅在最终消息中出现。

**id** `_string_`

音频文件 ID。

**expires\_at** `_integer_`

音频 URL 过期时间戳（Unix timestamp）。

**extra\_info** `_object_`

额外信息。包含以下字段：

**属性**

**channels** `_integer_`

音频声道数（如：2 表示立体声）。

**sample\_rate** `_string_`

音频采样率（如："48000"）。

**lyrics** `_string_`

歌词内容。

**finish\_reason** `_string_`

结束原因：

-   `null`：正在生成中
    
-   `stop`：生成自然结束
    

**usage** `_object_`

本次请求的计费信息。

**属性**

**duration** `_integer_`

音乐时长（秒），用于计费。
