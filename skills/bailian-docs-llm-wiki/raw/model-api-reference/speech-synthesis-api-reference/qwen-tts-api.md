# 非实时语音合成（Qwen-TTS）API参考

非实时语音合成（Qwen-TTS）API 的请求参数与返回字段说明。

> 模型的使用方法请参见 [非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide) 。

## **请求体**

## 非流式输出

## Python

> DashScope Python SDK中的`SpeechSynthesizer`接口已统一为`MultiModalConversation`，使用方法和参数保持完全一致。

```
# 请安装 DashScope SDK 的最新版本
    import os
    import dashscope

    # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    text = "那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。"
    # SpeechSynthesizer接口使用方法：dashscope.audio.qwen_tts.SpeechSynthesizer.call(...)
    response = dashscope.MultiModalConversation.call(
        # 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash
        model="qwen3-tts-flash",
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice="Cherry"
        # 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash
        # instructions='语速较快，带有明显的上扬语调，适合介绍时尚产品。',
        # optimize_instructions=True
    )
    print(response)
```

## Java

```
// 请安装 DashScope SDK 的最新版本
import com.alibaba.dashscope.aigc.multimodalconversation.AudioParameters;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 如需使用指令控制功能，请将MODEL替换为qwen3-tts-instruct-flash
    private static final String MODEL = "qwen3-tts-flash";
    public static void call() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model(MODEL)
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .text("Today is a wonderful day to build something people love!")
                .voice(AudioParameters.Voice.CHERRY)
                .languageType("English")
                // 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash
                // .parameter("instructions","语速较快，带有明显的上扬语调，适合介绍时尚产品。")
                // .parameter("optimize_instructions",true)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        try {
            call();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将$DASHSCOPE_API_KEY替换为：sk-xxx。
# === 执行时请删除该注释 ===

curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-tts-flash",
    "input": {
        "text": "那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。",
        "voice": "Cherry",
        "language_type": "Chinese"
    }
}'
```

## 流式输出

## Python

> DashScope Python SDK中的`SpeechSynthesizer`接口已统一为`MultiModalConversation`，使用新接口只需替换名称即可，其他参数完全兼容。

```
# DashScope SDK 版本不低于 1.24.5
    import os
    import dashscope

    # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    text = "那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。"
    # SpeechSynthesizer接口使用方法：dashscope.audio.qwen_tts.SpeechSynthesizer.call(...)
    response = dashscope.MultiModalConversation.call(
        # 如需使用指令控制功能，请将model替换为qwen3-tts-instruct-flash
        model="qwen3-tts-flash",
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice="Cherry",
        # 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash
        # instructions='语速较快，带有明显的上扬语调，适合介绍时尚产品。',
        # optimize_instructions=True,
        stream=True
    )
    for chunk in response:
        print(chunk)
```

## Java

```
// DashScope SDK 版本需要不低于 2.19.0
import com.alibaba.dashscope.aigc.multimodalconversation.AudioParameters;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;
import io.reactivex.Flowable;

public class Main {
    // 如需使用指令控制功能，请将MODEL替换为qwen3-tts-instruct-flash
    private static final String MODEL = "qwen3-tts-flash";
    public static void streamCall() throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model(MODEL)
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .text("Today is a wonderful day to build something people love!")
                .voice(AudioParameters.Voice.CHERRY)
                .languageType("English")
                // 如需使用指令控制功能，请取消下方注释，并将model替换为qwen3-tts-instruct-flash
                // .parameter("instructions","语速较快，带有明显的上扬语调，适合介绍时尚产品。")
                // .parameter("optimize_instructions",true)
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(r -> {System.out.println(JsonUtils.toJson(r));
        });
    }
    public static void main(String[] args) {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## curl

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用阿里云百炼API Key将$DASHSCOPE_API_KEY替换为：sk-xxx。
# === 执行时请删除该注释 ===

curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3-tts-flash",
    "input": {
        "text": "那我来给大家推荐一款T恤，这款呢真的是超级好看，这个颜色呢很显气质，而且呢也是搭配的绝佳单品，大家可以闭眼入，真的是非常好看，对身材的包容性也很好，不管啥身材的宝宝呢，穿上去都是很好看的。推荐宝宝们下单哦。",
        "voice": "Cherry",
        "language_type": "Chinese"
    }
}'
```

> 实时播放Base64 音频的方法请参见：[非实时语音合成](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#c204937c02gsb)。

**model** `_string_` **（必选）**

模型名称，详情请参见[支持的模型](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#d2ad2470a394c)。

**input** `_object_` **（必选）**

输入参数**。**

**属性**

**text** `_string_` **（必选）**

要合成的文本，支持多语种混合输入。最大输入长度：千问-TTS模型为 512 Token，其他模型为 600 字符。

**voice** `_string_` **（必选）**

使用的音色，参见[支持的系统音色](https://help.aliyun.com/zh/model-studio/non-realtime-tts-user-guide#bac280ddf5a1u)。

**language\_type** `_string_` （可选）

合成音频的语种。默认为 `Auto`。

-   `Auto`：适用于文本包含多种语言或语种不确定的场景。模型自动为不同语言片段匹配发音，但无法保证完全精准。
    
-   指定语种：适用于单一语种文本。指定具体语种能显著提升合成质量，效果通常优于 `Auto`。可选值：
    
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
        

**instructions** `_string_` （可选）

设置指令，参见[指令控制](https://help.aliyun.com/zh/model-studio/realtime-tts-user-guide#12884a10929p9)。

默认值：无，不设置时不生效。

最大长度：1600 Token。

支持语言：仅支持中文和英文。

适用范围：该功能仅适用于千问3-TTS-Instruct-Flash-Realtime系列模型。

**optimize\_instructions** `_boolean_` （可选）

对 `instructions` 进行语义优化，以提升语音合成的自然度和表现力。

默认值：false。

行为说明：当设置为 true 时，系统将对 `instructions` 的内容进行语义增强与重写，生成更适合语音合成的内部指令。

推荐在追求高品质、精细化语音表达时开启。

依赖 `instructions` 参数。若 `instructions` 为空，此参数不生效。

适用范围：该功能仅适用于千问3-TTS-Instruct-Flash系列模型。

## **返回对象**（流式与非流式输出格式一致）

## 千问3-TTS-Flash

```
{
    "status_code": 200,
    "request_id": "5c63c65c-cad8-4bf4-959d-xxxxxxxxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": "stop",
        "choices": null,
        "audio": {
            "data": "",
            "url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/1d/ab/20251218/d2033070/39b6d8f2-c0db-4daa-9073-5d27bfb66b78.wav?Expires=1766113409&OSSAccessKeyId=LTAI5xxxxxxxxxxxx&Signature=NOrqxxxxxxxxxxxx%3D",
            "id": "audio_5c63c65c-cad8-4bf4-959d-xxxxxxxxxxxx",
            "expires_at": 1766113409
        }
    },
    "usage": {
        "input_tokens": 0,
        "output_tokens": 0,
        "characters": 195
    }
}
```

## 千问-TTS

```
{
    "status_code": 200,
    "request_id": "f4e8139b-3203-4887-92cb-xxxxxxxxxxxx",
    "code": "",
    "message": "",
    "output": {
        "text": null,
        "finish_reason": "stop",
        "choices": null,
        "audio": {
            "data": "",
            "url": "http://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/1d/50/20251218/e6c1b9cc/9acec74e-e317-4dbd-9e76-745c47bcbf2d.wav?Expires=1766116806&OSSAccessKeyId=LTAxxxxxxxxx&Signature=afYZxxxxxxxxx%2FAX9bk%3D",
            "id": "audio_f4e8139b-3203-4887-92cb-xxxxxxxxxxxx",
            "expires_at": 1766116806
        }
    },
    "usage": {
        "input_tokens": 76,
        "output_tokens": 1045,
        "characters": 0,
        "input_tokens_details": {
            "text_tokens": 76
        },
        "output_tokens_details": {
            "audio_tokens": 1045,
            "text_tokens": 0
        },
        "total_tokens": 1121
    }
}
```

**status\_code** `_integer_`

HTTP状态码。遵循 [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-status-codes)标准定义。例如：  
• `200`：请求成功，正常返回结果  
• `400`：客户端请求参数错误  
• `401`：未授权访问  
• `404`：资源未找到  
• `500`：服务器内部错误。

**request\_id** `_string_`

本次请求的唯一标识，可用于问题排查。

**code** `_string_`

请求失败时展示错误码（参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)）。

**message** `_string_`

请求失败时展示错误信息（参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)）。

**output** `_object_`

模型的输出。

**属性**

**text** `_string_`

始终为null，无需关注该参数。

**choices** `_string_`

始终为null，无需关注该参数。

**finish\_reason** `_string_`

生成状态标识：

-   正在生成时为"null"；
    
-   模型输出自然结束或触发了停止条件时为 "stop"。
    

**audio** `_object_`

模型输出的音频信息。

**属性**

**url** `_string_`

完整音频文件的 URL，有效期 24 小时。

**data** `_string_`

流式输出时的Base64 音频数据。

**id** `_string_`

音频的唯一标识。

**expires\_at** `_integer_`

URL 过期时间的 UNIX 时间戳。

**usage** `_object_`

本次请求的 Token 或字符消耗信息。千问-TTS模型返回Token消耗信息，千问3-TTS-Flash模型返回字符消耗信息

**属性**

**input\_tokens\_details** `_object_`

输入文本的 Token消耗信息。仅千问-TTS模型返回该字段。

**属性**

**text\_tokens** `_integer_`

输入文本的 Token 消耗量。

**total\_tokens** `_integer_`

本次请求总共消耗的 Token 量。仅千问-TTS模型返回该字段。

**output\_tokens** `_integer_`

输出音频的 Token 消耗量。对于千问3-TTS-Flash模型，该字段固定为0。

**input\_tokens** `_integer_`

输入文本的 Token 消耗量。对于千问3-TTS-Flash模型，该字段固定为0。

**output\_tokens\_details** `_object_`

输出的 Token 消耗信息。仅千问-TTS模型返回该字段。

**属性**

**audio\_tokens** `_integer_`

输出音频的 Token 消耗量。

**text\_tokens** `_integer_`

输出文本的 Token 消耗量，当前固定为0。

**characters** `_integer_`

输入文本的字符数。仅千问3-TTS-Flash模型返回该字段。

**request\_id** `_string_`

本次请求的 ID。
