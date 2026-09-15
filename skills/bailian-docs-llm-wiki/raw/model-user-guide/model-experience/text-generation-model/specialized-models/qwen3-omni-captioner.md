# 音频理解（Qwen3-Omni-Captioner）

Qwen3-Omni-Captioner是以千问3-Omni为基座的开源模型，无需任何提示，自动为复杂语音、环境声、音乐、影视声效等生成精准、全面的描述，能识别说话人的情绪、音乐元素（如风格、乐器）、敏感信息等，适用于音频内容分析、安全审核、意图识别、音频剪辑等多个领域。当前模型不支持音色、音调、语气语调等细粒度声学特征分析。

## 支持的模型

#### 华北2（北京）

**模型名称**

**上下文长度**

**最大输入**

**最大输出**

**输入成本**

**输出成本**

**免费额度**

[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#977b13081ab56)

**（Token数）**

**（每百万Token）**

qwen3-omni-30b-a3b-captioner

65,536

32,768

32,768

15.8元

12.7元

100万Token

有效期：阿里云百炼开通后90天内

#### 新加坡

**模型名称**

**上下文长度**

**最大输入**

**最大输出**

**输入成本**

**输出成本**

**免费额度**

[（注）](https://help.aliyun.com/zh/model-studio/new-free-quota#977b13081ab56)

**（Token数）**

**（每百万Token）**

qwen3-omni-30b-a3b-captioner

65,536

32,768

32,768

27.962元

22.458元

无免费额度

> 音频转换为Token的规则：`总 Tokens 数 = 音频时长（单位：秒）* 12.5`，若音频时长不足1秒，则按 1 秒计算。

## 快速开始

**前提条件**

-   需要已[配置 API Key](raw/model-api-reference/preparations/get-api-key.md)并[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)。
-   如果通过 SDK 进行调用，需安装[最新版SDK](raw/model-api-reference/preparations/install-sdk.md)。

Qwen3-Omni-Captioner模型仅支持通过API调用，暂不支持在阿里云百炼的控制台在线体验。

以下是理解在线音频（通过URL指定，非本地音频）的示例代码。了解[如何传入本地文件](https://help.aliyun.com/zh/model-studio/qwen3-omni-captioner#572995b8e2hmp)和[音频文件的限制](https://help.aliyun.com/zh/model-studio/qwen3-omni-captioner#765fa30b81nss)。

#### OpenAI兼容

#### Python

```
import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-omni-30b-a3b-captioner",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"
                    }
                }
            ]
        }
    ]
)
print(completion.choices[0].message.content)
```

响应结果

```
The audio clip begins with a sudden, loud, metallic clanking that dominates the soundstage, immediately indicating an industrial or workshop environment. The clanking is rhythmic, consistent, and has a sharp, resonant quality, suggestive of metal tools striking metal surfaces—likely a hammer, wrench, or similar instrument being used on a hard metal object. The sound is harsh and slightly distorted, with audible clipping on each impact, likely due to the microphone’s proximity and the high volume of the sound.
As the initial clanking fades, a male voice enters, speaking in Mandarin Chinese with a tone of exasperation and complaint. His voice is clear, close-mic’d, and free from distortion. He says: “哎呀，这样我还怎么安静工作啊？” (“Oh my, how can I possibly work quietly like this?”). His intonation is conversational, informal, and marked by a rising, questioning inflection, typical of everyday speech rather than performance or formal address. The accent is standard Putonghua, with no strong regional markers, suggesting he is a native Mandarin speaker from the northern or central regions of China.
During the speaker’s utterance, the metallic clanking resumes, overlapping with his voice. The timing and nature of these sounds indicate the speaker is directly reacting to the ongoing noise—likely caused by another person in the same space. The environment is acoustically “dry” with minimal echo, implying a small or medium-sized room with sound-absorbing materials, further supporting the workshop or industrial setting. There are no other background noises, music, or ambient sounds, and no evidence of a public or commercial space.
The recording quality is moderate: the microphone captures both the low-end thuds and the sharp metallic transients, but the loud clanking causes digital clipping, resulting in a harsh, “crunchy” distortion during the impacts. The speaker’s voice, however, remains clear and intelligible. The overall impression is of a candid, real-world interaction—possibly a worker or office employee complaining about an interruption in a noisy environment.
In summary, the audio depicts a Mandarin-speaking man in a workshop or industrial setting, reacting with frustration to ongoing metallic clanking that disrupts his work. The recording is informal, clear, and grounded in a context of manual labor or technical work, with no evidence of scripted performance, music, or extraneous activity.
```

#### Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
       // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
       // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
const completion = await openai.chat.completions.create({
    model: "qwen3-omni-30b-a3b-captioner",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "input_audio",
                "input_audio": {
                    "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"
                     }
            }]
        }]
});

console.log(completion.choices[0].message.content)
```

响应结果

```
The audio clip begins with a sudden, loud, metallic clanking that dominates the soundstage, immediately indicating an industrial or workshop environment. The clanking is rhythmic, consistent, and has a sharp, resonant quality, suggestive of metal tools striking metal surfaces—likely a hammer, wrench, or similar instrument being used on a hard metal object. The sound is harsh and slightly distorted, with audible clipping on each impact, likely due to the microphone’s proximity and the high volume of the sound.
As the initial clanking fades, a male voice enters, speaking in Mandarin Chinese with a tone of exasperation and complaint. His voice is clear, close-mic’d, and free from distortion. He says: “哎呀，这样我还怎么安静工作啊？” (“Oh my, how can I possibly work quietly like this?”). His intonation is conversational, informal, and marked by a rising, questioning inflection, typical of everyday speech rather than performance or formal address. The accent is standard Putonghua, with no strong regional markers, suggesting he is a native Mandarin speaker from the northern or central regions of China.
During the speaker’s utterance, the metallic clanking resumes, overlapping with his voice. The timing and nature of these sounds indicate the speaker is directly reacting to the ongoing noise—likely caused by another person in the same space. The environment is acoustically “dry” with minimal echo, implying a small or medium-sized room with sound-absorbing materials, further supporting the workshop or industrial setting. There are no other background noises, music, or ambient sounds, and no evidence of a public or commercial space.
The recording quality is moderate: the microphone captures both the low-end thuds and the sharp metallic transients, but the loud clanking causes digital clipping, resulting in a harsh, “crunchy” distortion during the impacts. The speaker’s voice, however, remains clear and intelligible. The overall impression is of a candid, real-world interaction—possibly a worker or office employee complaining about an interruption in a noisy environment.
In summary, the audio depicts a Mandarin-speaking man in a workshop or industrial setting, reacting with frustration to ongoing metallic clanking that disrupts his work. The recording is informal, clear, and grounded in a context of manual labor or technical work, with no evidence of scripted performance, music, or extraneous activity.
```

#### curl

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-omni-30b-a3b-captioner",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_audio",
          "input_audio": {
            "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"
          }
        }
      ]
    }
  ]
}'
```

响应结果

```
{
  "choices": [
    {
      "message": {
        "content": "The audio clip is a brief, low-fidelity recording-approximately six seconds long—captured in a small, reverberant indoor space, likely a home office or bedroom. It opens with a rapid, metallic, rhythmic hammering sound, repeating every 0.5 to 0.6 seconds, with each strike slightly uneven and accompanied by a short echo. This sound dominates the left side of the stereo field and is close to the microphone, suggesting the hammering is occurring nearby and slightly to the left.\n\nOverlaid with the hammering, a single male voice speaks in Mandarin Chinese, his tone clearly one of frustration and exasperation. He says, “哎呀，这样我还怎么安静工作啊？” (“Oh, with this, how am I supposed to work quietly?”) His speech is clear despite the poor audio quality, and is delivered in a standard, unaccented Mandarin, indicative of a native speaker from northern or central China.\n\nThe voice is more distant and centered in the stereo field, with more room reverberation than the hammering. The emotional content is palpable: his voice rises slightly at the end, turning the phrase into a rhetorical complaint, underscoring his irritation. No other voices, music, or ambient sounds are present; the only non-speech sounds are the hammering and the faint hiss of the recording device.\n\nThe combination of the environmental sound, the speaker’s language, and his tone strongly suggests a scenario of home office disruption—perhaps someone working from home is being disturbed by renovation or repair work happening nearby. The recording ends abruptly, mid-hammer, further emphasizing the spontaneous and candid nature of the capture.\n\nIn summary, the audio is a realistic, low-fidelity snapshot of a Mandarin-speaking man, likely in China, expressing frustration at being unable to work in peace due to nearby construction or repair activity, captured in a personal, indoor setting.",
        "role": "assistant"
      },
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null
    }
  ],
  "object": "chat.completion",
  "usage": {
    "prompt_tokens": 160,
    "completion_tokens": 387,
    "total_tokens": 547,
    "prompt_tokens_details": {
      "audio_tokens": 152,
      "text_tokens": 8
    },
    "completion_tokens_details": {
      "text_tokens": 387
    }
  },
  "created": 1758002134,
  "system_fingerprint": null,
  "model": "qwen3-omni-30b-a3b-captioner",
  "id": "chatcmpl-f4155bf9-b860-49d6-8ee2-092da7359097"
}
```

#### DashScope

#### Python

```
import dashscope
import os

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"audio": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3-omni-30b-a3b-captioner",
    messages=messages
    )
print("输出结果为：")
print(response["output"]["choices"][0]["message"].content[0]["text"])
```

响应结果

```
The audio clip begins with a sudden, loud, metallic clanking that dominates the soundstage, immediately indicating an industrial or workshop environment. The clanking is rhythmic, consistent, and has a sharp, resonant quality, suggestive of metal tools striking metal surfaces—likely a hammer, wrench, or similar instrument being used on a hard metal object. The sound is harsh and slightly distorted, with audible clipping on each impact, likely due to the microphone’s proximity and the high volume of the sound.
As the initial clanking fades, a male voice enters, speaking in Mandarin Chinese with a tone of exasperation and complaint. His voice is clear, close-mic’d, and free from distortion. He says: “哎呀，这样我还怎么安静工作啊？” (“Oh my, how can I possibly work quietly like this?”). His intonation is conversational, informal, and marked by a rising, questioning inflection, typical of everyday speech rather than performance or formal address. The accent is standard Putonghua, with no strong regional markers, suggesting he is a native Mandarin speaker from the northern or central regions of China.
During the speaker’s utterance, the metallic clanking resumes, overlapping with his voice. The timing and nature of these sounds indicate the speaker is directly reacting to the ongoing noise—likely caused by another person in the same space. The environment is acoustically “dry” with minimal echo, implying a small or medium-sized room with sound-absorbing materials, further supporting the workshop or industrial setting. There are no other background noises, music, or ambient sounds, and no evidence of a public or commercial space.
The recording quality is moderate: the microphone captures both the low-end thuds and the sharp metallic transients, but the loud clanking causes digital clipping, resulting in a harsh, “crunchy” distortion during the impacts. The speaker’s voice, however, remains clear and intelligible. The overall impression is of a candid, real-world interaction—possibly a worker or office employee complaining about an interruption in a noisy environment.
In summary, the audio depicts a Mandarin-speaking man in a workshop or industrial setting, reacting with frustration to ongoing metallic clanking that disrupts his work. The recording is informal, clear, and grounded in a context of manual labor or technical work, with no evidence of scripted performance, music, or extraneous activity.
```

#### Java

```
import java.util.Arrays;
import java.util.Collections;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("audio", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav")))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-omni-30b-a3b-captioner")
                .message(userMessage)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println("输出结果为：\n" + result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

响应结果

```
The audio clip begins with a sudden, loud, metallic clanking that dominates the soundstage, immediately indicating an industrial or workshop environment. The clanking is rhythmic, consistent, and has a sharp, resonant quality, suggestive of metal tools striking metal surfaces—likely a hammer, wrench, or similar instrument being used on a hard metal object. The sound is harsh and slightly distorted, with audible clipping on each impact, likely due to the microphone’s proximity and the high volume of the sound.
As the initial clanking fades, a male voice enters, speaking in Mandarin Chinese with a tone of exasperation and complaint. His voice is clear, close-mic’d, and free from distortion. He says: “哎呀，这样我还怎么安静工作啊？” (“Oh my, how can I possibly work quietly like this?”). His intonation is conversational, informal, and marked by a rising, questioning inflection, typical of everyday speech rather than performance or formal address. The accent is standard Putonghua, with no strong regional markers, suggesting he is a native Mandarin speaker from the northern or central regions of China.
During the speaker’s utterance, the metallic clanking resumes, overlapping with his voice. The timing and nature of these sounds indicate the speaker is directly reacting to the ongoing noise—likely caused by another person in the same space. The environment is acoustically “dry” with minimal echo, implying a small or medium-sized room with sound-absorbing materials, further supporting the workshop or industrial setting. There are no other background noises, music, or ambient sounds, and no evidence of a public or commercial space.
The recording quality is moderate: the microphone captures both the low-end thuds and the sharp metallic transients, but the loud clanking causes digital clipping, resulting in a harsh, “crunchy” distortion during the impacts. The speaker’s voice, however, remains clear and intelligible. The overall impression is of a candid, real-world interaction—possibly a worker or office employee complaining about an interruption in a noisy environment.
In summary, the audio depicts a Mandarin-speaking man in a workshop or industrial setting, reacting with frustration to ongoing metallic clanking that disrupts his work. The recording is informal, clear, and grounded in a context of manual labor or technical work, with no evidence of scripted performance, music, or extraneous activity.
```

#### curl

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-omni-30b-a3b-captioner",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"audio": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"}
                ]
            }
        ]
    }
}'
```

响应结果

```
{
  "output":{
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            {
              "text": "The audio clip is a 6-second, high-fidelity recording set in a quiet, indoor environment. The primary sound is a male speaker, likely in his late teens to mid-20s, speaking Mandarin Chinese in a tone of mild exasperation. His speech is clear and natural, delivered in a conversational manner: “哎呀，这样我还怎么安静工作啊？” (“Oh, how can I possibly work quietly like this?”). His voice is close to the microphone, and the room is acoustically neutral, with no noticeable echo or background noise, suggesting a small, well-furnished space.\n\nOverlaying the speech is a persistent, rhythmic mechanical sound—a series of sharp, metallic clicks or clatters that repeat every 0.6 seconds. The sound is dry and lacks any reverberation, further supporting the inference that it is produced by a mechanical device very close to the microphone. The regularity and timbre of the sound suggest a small, metallic object (such as a key, coin, or pen) being repeatedly tapped or struck on a hard surface, rather than a larger or more complex machine.\n\nThe speaker’s complaint is a direct response to the mechanical noise, expressing frustration at being unable to concentrate or work in peace due to the disturbance. The tone is not angry or urgent, but rather one of resigned annoyance, typical of someone encountering a minor, persistent annoyance in a personal or domestic setting.\n\nThere are no other voices, music, or environmental cues present. The overall impression is of a brief, candid moment—perhaps a student, office worker, or someone in a quiet home environment—caught on microphone while complaining (to themselves or a nearby companion) about a distracting, repetitive noise. The recording is technically clean and focused, with all attention on the speaker and the mechanical sound, making it highly plausible that the clip was captured intentionally, possibly for a voice note, social media post, or as a sample for a sound effect library."
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "input_tokens_details": {
      "audio_tokens": 152,
      "text_tokens": 8
    },
    "total_tokens": 559,
    "output_tokens": 399,
    "input_tokens": 160,
    "output_tokens_details": {
      "text_tokens": 399
    }
  },
  "request_id": "d532f72c-e75b-4ffb-a1ef-d2465e758958"
}
```

## 工作方式

-   **单轮交互：**模型不支持多轮对话。每次请求都是一次独立的分析任务。
    
-   **固定任务**：模型的核心任务是生成音频描述（仅为英文描述），无法通过指令（如 System Message）改变其行为，例如控制输出格式或内容重点。
    
-   **仅支持音频输入：**模型仅接收音频作为输入，无需传入文本提示，`message`参数格式固定。
    
    message 格式示例
    
    OpenAI 兼容
    
    ```
    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"
                        }
                    }
                ]
            }
        ]
    ```
    
    DashScope
    
    ```
    messages = [
        {
            "role": "user",
            "content": [
                {"audio": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"}
            ]
        }
    ]
    ```
    

## 流式输出

大模型接收到输入后，会逐步生成中间结果，最终结果由这些中间结果拼接而成。这种一边生成一边输出中间结果的方式称为流式输出。采用流式输出时，您可以在模型进行输出的同时阅读，减少等待模型回复的时间。

#### OpenAI兼容

通过 OpenAI 兼容方式开启流式输出十分方便，只需在请求参数中设置`stream`参数为`true`即可。

Python

```
import os
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="qwen3-omni-30b-a3b-captioner",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"
                    }
                }
            ]
        }
    ],
    stream=True,
    stream_options={"include_usage": True},

)
for chunk in completion:
    # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
    if chunk.choices and chunk.choices[0].delta.content != "":
        print(chunk.choices[0].delta.content,end="")
```

Node.js

```
import OpenAI from "openai";

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：apiKey: "sk-xxx",
       // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
       // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);
const completion = await openai.chat.completions.create({
    model: "qwen3-omni-30b-a3b-captioner",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "input_audio",
                "input_audio": {
                    "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"
                     },
            }]
        }],
    stream: true,
    stream_options: {
        include_usage: true
    },
});

for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        console.log(chunk.choices[0].delta.content);
    } else {
        console.log(chunk.usage);
    }
}
```

curl

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-omni-30b-a3b-captioner",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_audio",
          "input_audio": {
            "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"
          }
        }
      ]
    }
  ],
    "stream":true,
    "stream_options":{
        "include_usage":true
    }
}'
```

#### DashScope

可通过DashScope SDK或HTTP方式调用千问VL模型，体验流式输出的功能。根据不同的调用方式需设置相应的参数来实现流式输出：

-   Python SDK方式：设置`stream`参数为True。
-   Java SDK方式：需要通过`streamCall`接口调用。
-   HTTP方式：需要在Header中指定`X-DashScope-SSE`为`enable`。

> 流式输出的内容默认是非增量式（即每次返回的内容都包含之前生成的内容），如果您需要使用增量式流式输出，请设置`incremental_output`（Java 为`incrementalOutput`）参数为 `true` 。

Python

```
import dashscope
import os

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

messages = [
    {
        "role": "user",
        "content": [
            {"audio": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"}
        ]
    }
]

response = dashscope.MultiModalConversation.call(
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="qwen3-omni-30b-a3b-captioner",
    messages=messages,
    stream=True,
    incremental_output=True
    )

full_content = ""
print("流式输出内容为：")
for response in response:
    if response["output"]["choices"][0]["message"].content:
        print(response["output"]["choices"][0]["message"].content[0]["text"])
        full_content += response["output"]["choices"][0]["message"].content[0]["text"]
print(f"完整内容为：{full_content}")
```

Java

```
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import io.reactivex.Flowable;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static void streamCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                // qwen3-omni-30b-a3b-captioner仅支持输入1个音频文件
                .content(Arrays.asList(
                        new HashMap<String, Object>(){{put("audio", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav");}}
                )).build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                 // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-omni-30b-a3b-captioner")
                .message(userMessage)
                .incrementalOutput(true)
                .build();
        Flowable<MultiModalConversationResult> result = conv.streamCall(param);
        result.blockingForEach(item -> {
            try {
                List<com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult.Output.Choice.Message.Content> content = item.getOutput().getChoices().get(0).getMessage().getContent();
                // 判断content是否存在且不为空
                if (content != null &&  !content.isEmpty()) {
                    System.out.println(content.get(0).get("text"));
                }
            } catch (Exception e){
                System.exit(0);
            }
        });
    }

    public static void main(String[] args) {
        try {
            streamCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

curl

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-H 'X-DashScope-SSE: enable' \
-d '{
    "model": "qwen3-omni-30b-a3b-captioner",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"audio": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240916/xvappi/%E8%A3%85%E4%BF%AE%E5%99%AA%E9%9F%B3.wav"}
                ]
            }
        ]
    },
    "parameters": {
      "incremental_output": true
    }
}'
```

## 传入本地文件（Base64 编码或文件路径）

模型提供两种本地文件上传方式：

-   Base64 编码上传
-   文件路径直接上传（**传输更稳定，推荐方式**）

**上传方式：**

#### 文件路径传入

直接向模型传入文件路径。仅 DashScope Python 和 Java SDK 支持，不支持 HTTP 方式。请您参考下表，结合您的编程语言与操作系统指定文件的路径。

指定文件的路径

**系统**

**SDK**

**传入的文件路径**

**示例**

Linux或macOS系统

Python SDK

file://{文件的绝对路径}

file:///home/images/test.mp3

Java SDK

Windows系统

Python SDK

file://{文件的绝对路径}

file://D:/images/test.mp3

Java SDK

file:///{文件的绝对路径}

file:///D:/images/test.mp3

#### Base64 编码传入

Base64 编码，将文件转换为 Base64 编码字符串，再传入模型。

传入 Base64 编码字符串的步骤

1.  文件编码：将本地音频文件转换为 Base64 编码；
    
    音频转换为 Base64 编码的示例代码
    
    ```
    import base64
    
    # 编码函数：将本地文件转换为 Base64 编码的字符串
    def encode_audio(audio_path):
        with open(audio_path, "rb") as audio_file:
            return base64.b64encode(audio_file.read()).decode("utf-8")
    
    # 将xxxx/test.mp3替换为你本地音频的绝对路径
    base64_audio = encode_audio("xxxx/test.mp3")
    ```
    
2.  构建[Data URL](https://www.rfc-editor.org/rfc/rfc2397)，格式如下：`data:;base64,{base64_audio}`，`base64_audio`为上一步生成的 Base64 字符串；
    
3.  调用模型：通过`audio`（DashScope SDK）或`input_audio`（OpenAI 兼容 SDK）参数传递`Data URL`并调用模型。
    

**使用限制：**

-   **建议优先选择文件路径上传（传输更稳定）**，1MB以下的文件也可使用 Base64 编码；
-   直接传入文件路径时，音频本身需小于 10MB；
-   Base64编码方式传入时，由于 Base64 编码会增加数据体积，需保证编码后的 Base64 字符串需小于 10MB。

#### 文件路径传入

> 传入文件路径仅支持 DashScope Python 和 Java SDK方式调用，不支持 HTTP 方式。

Python

```
import os
import dashscope

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 将 ABSOLUTE_PATH/welcome.mp3 替换为本地音频的绝对路径，
# 本地文件的完整路径必须以 file:// 为前缀，以保证路径的合法性，例如：file:///home/images/test.mp3
audio_file_path = "file://ABSOLUTE_PATH/welcome.mp3"
messages = [
    {
        "role": "user",
        # 在 audio 参数中传入以 file:// 为前缀的文件路径
        "content": [{"audio": audio_file_path}],
    }
]

response = dashscope.MultiModalConversation.call(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
            # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            model="qwen3-omni-30b-a3b-captioner",
            messages=messages)
print("输出结果为：")
print(response["output"]["choices"][0]["message"].content[0]["text"])
```

Java

```
import java.util.Arrays;
import java.util.HashMap;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.dashscope.utils.Constants;

public class Main {
    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    public static void callWithLocalFile()
            throws ApiException, NoApiKeyException, UploadFileException {

        // 请将 ABSOLUTE_PATH/welcome.mp3 替换为本地音频文件的绝对路径
        // 本地文件的完整路径必须以 file:// 为前缀，以保证路径的合法性，例如：file:///home/images/test.mp3
        // 当前测试系统为macOS。如果您使用Windows系统，请用"file:///ABSOLUTE_PATH/welcome.mp3"代替

        String localFilePath = "file://ABSOLUTE_PATH/welcome.mp3";
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        new HashMap<String, Object>(){{put("audio", localFilePath);}}
                ))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3-omni-30b-a3b-captioner")
                .message(userMessage)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println("输出结果为：\n" + result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            callWithLocalFile();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### Base64 编码传入

#### OpenAI兼容

#### Python

```
import os
from openai import OpenAI
import base64

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    # 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)

def encode_audio(audio_path):
    with open(audio_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

# 请将 ABSOLUTE_PATH/welcome.mp3 替换为本地音频的绝对路径
audio_file_path = "xxx/ABSOLUTE_PATH/welcome.mp3"
base64_audio = encode_audio(audio_file_path)

completion = client.chat.completions.create(
    model="qwen3-omni-30b-a3b-captioner",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        # 以 Base64 编码方式传入本地文件时，必须要以data:为前缀，以保证文件 URL 的合法性。
                        # 在 Base64 编码数据（base64_audio）前需要包含"base64"，否则也会报错。
                        "data": f"data:;base64,{base64_audio}"
                    },
                }
            ],
        },
    ]
)
print(completion.choices[0].message.content)
```

#### Node.js

```
import OpenAI from "openai";
import { readFileSync } from 'fs';

const openai = new OpenAI(
    {
        // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx"
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        apiKey: process.env.DASHSCOPE_API_KEY,
        // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
        baseURL: "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    }
);

const encodeAudio = (audioPath) => {
    const audioFile = readFileSync(audioPath);
    return audioFile.toString('base64');
};
//  请将 ABSOLUTE_PATH/welcome.mp3 替换为本地音频的绝对路径
const base64Audio = encodeAudio("xxx/ABSOLUTE_PATH/welcome.mp3")

const completion = await openai.chat.completions.create({
    model: "qwen3-omni-30b-a3b-captioner",
    messages: [
        {
            "role": "user",
            "content": [{
                "type": "input_audio",
                "input_audio": { "data": `data:;base64,${base64Audio}`}
            }]
        }]
});

console.log(completion.choices[0].message.content);
```

#### curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](raw/model-user-guide/model-experience/text-generation-model/specialized-models/qwen3-omni-captioner.md)；
-   为了便于展示，代码中的`"data:;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5...."` Base64 字符串已截断，实际使用时请传入完整编码。

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-omni-30b-a3b-captioner",
    "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "input_audio",
          "input_audio": {
            "data": "data:;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5...."
          }
        }
      ]
    }
  ]
}'
```

#### DashScope

#### Python

```
import os
import base64
import dashscope
from dashscope import MultiModalConversation

# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
dashscope.base_http_api_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"

# 编码函数： 将本地文件转换为 Base64 编码的字符串
def encode_audio(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

# 请将 ABSOLUTE_PATH/welcome.mp3 替换为本地音频的绝对路径
audio_file_path = "xxx/ABSOLUTE_PATH/welcome.mp3"
base64_audio = encode_audio(audio_file_path)

messages = [
    {
        "role": "user",
        # 以 Base64 编码方式传入本地文件时，必须要以data:为前缀，以保证文件 URL 的合法性。
        # 在 Base64 编码数据（base64_audio）前需要包含"base64"，否则也会报错。
        "content": [{"audio":f"data:;base64,{base64_audio}"}],
    }
]

response = MultiModalConversation.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-omni-30b-a3b-captioner",
    messages=messages,

    )
print(response.output.choices[0].message.content[0]["text"])
```

#### Java

```
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import java.util.Arrays;
import java.util.Base64;
import java.util.HashMap;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;

public class Main {

    // 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
    static {Constants.baseHttpApiUrl="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";}

    private static String encodeAudioToBase64(String audioPath) throws IOException {
        Path path = Paths.get(audioPath);
        byte[] audioBytes = Files.readAllBytes(path);
        return Base64.getEncoder().encodeToString(audioBytes);
    }

    public static void callWithLocalFile()
            throws ApiException, NoApiKeyException, UploadFileException,IOException{
        // 请将 ABSOLUTE_PATH/welcome.mp3 替换为本地文件的实际路径
        String localFilePath = "ABSOLUTE_PATH/welcome.mp3";
        String base64Audio = encodeAudioToBase64(localFilePath);

        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                // 以 Base64 编码方式传入本地文件时，必须要以data:为前缀，以保证文件 URL 的合法性。
                // 在 Base64 编码数据（base64_audio）前需要包含"base64"，否则也会报错。
                .content(Arrays.asList(
                        new HashMap<String, Object>(){{put("audio", "data:;base64," + base64Audio);}}
                ))
                .build();
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .model("qwen3-omni-30b-a3b-captioner")
                // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .message(userMessage)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println("输出结果为：\n" + result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
    }
    public static void main(String[] args) {
        try {
            callWithLocalFile();
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

#### curl

-   将文件转换为 Base64 编码的字符串的方法可参见[示例代码](raw/model-user-guide/model-experience/text-generation-model/specialized-models/qwen3-omni-captioner.md)；
-   为了便于展示，代码中的`"data:;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5...."` Base64 字符串已截断，实际使用时请传入完整编码。

```
# ======= 重要提示 =======
# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 以下为华北2（北京）地域的URL，调用时请将WorkspaceId替换为真实的业务空间ID，各地域的URL不同。
# === 执行时请删除该注释 ===

curl -X POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json' \
-d '{
    "model": "qwen3-omni-30b-a3b-captioner",
    "input":{
        "messages":[
            {
                "role": "user",
                "content": [
                    {"audio": "data:;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5...."}
                ]
            }
        ]
    }
}'
```

## API参考

关于千问3-Omni-Captioner的输入输出参数，请参见[文本生成](raw/model-api-reference/qwen-api-reference.md)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。

## 常见问题

如何压缩音频文件到满足要求的大小？

-   在线工具：使用 [Compresss](https://www.compresss.com/cn/compress-audio.html) 等在线工具压缩音频文件。
-   代码实现：使用FFmpeg工具，更多用法请参见[FFmpeg官网](https://ffmpeg.org/download.html)。

```
# 基础转换命令（万能模板）
# -i，作用：输入文件路径，常用值示例：input.mp3

# -b:a，作用： 设置音频比特率 ，
  # 一般取值有64kbps(低质量，适合语音、低带宽流媒体)、128k（中等质量，适合日常音频、播客）、192kbps（高质量，适合音乐、广播）
  # 比特率越高，音质越好，文件体积越大

# -ar，作用：设置音频采样率，表示每秒采样的次数，
 # 一般取值为8000Hz、22050Hz、44100 Hz(标准采样率)
 # 采样率越高，文件体积越大

# -ac，作用：设置音频通道数。一般取值有 1（单声道），2（立体声），单声道文件体积更小

# -y，作用：覆盖已存在文件(无需值)# output.mp3，作用：输出文件路径

ffmpeg -i input.mp3 -b:a 128k -ar 44100 -ac 1 output.mp3 -y
```

## 限制

模型对音频文件的限制如下：

-   **时长限制：**时长需小于或等于 40 分钟
    
-   **文件数量：**每次请求仅支持1个音频文件
    
-   **文件格式**：支持AMR、 WAV（CodecID: GSM\_MS）、 WAV（PCM）、 3GP、 3GPP、 AAC、 MP3等主流格式
    
-   **文件输入方式：**公网可访问的音频URL、 Base64 编码、本地文件路径
    
-   **文件大小：**
    
    -   公网URL传入：不超过 1GB
    -   传入文件路径：音频本身需小于 10MB
    -   Base64编码传入：需确保编码后 Base64 字符串小于 10MB，详情请参见[如何传入本地文件](https://help.aliyun.com/zh/model-studio/qwen3-omni-captioner#572995b8e2hmp)
    
    > 如需压缩文件请参见[如何压缩音频文件到满足要求的大小？](raw/model-user-guide/model-experience/text-generation-model/specialized-models/qwen3-omni-captioner.md)
