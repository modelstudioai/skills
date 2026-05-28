# 录音文件识别（Qwen-ASR）API参考

本文介绍 Qwen-ASR 模型的输入与输出参数。可通过OpenAI 兼容或DashScope协议调用 API。

**用户指南：**模型介绍和选型请参见[录音文件识别-千问](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide)。

## **模型接入方式**

不同[模型](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#b8c8c0483153o)支持的接入方式不同，请根据下表选择正确的方式进行集成。

**模型**

**接入方式**

千问3-ASR-Flash-Filetrans

仅支持[DashScope异步调用](#9937e8884002q)方式

千问3-ASR-Flash

[OpenAI 兼容](#d397bcc41eu3q)和[DashScope同步调用](#1afc6b20a29ie)两种方式

## **OpenAI 兼容**

### **URL**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

HTTP请求地址：`POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

SDK调用配置的base\_url：`https://dashscope.aliyuncs.com/compatible-mode/v1`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，数据存储位于**新加坡接入地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

HTTP请求地址：`POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions`

SDK调用配置的base\_url：`https://dashscope-intl.aliyuncs.com/compatible-mode/v1`

### **请求体**

### 输入内容：音频文件URL

#### Python SDK

```
from openai import OpenAI
import os

try:
    client = OpenAI(
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    

    stream_enabled = False  # 是否开启流式输出
    completion = client.chat.completions.create(
        model="qwen3-asr-flash",
        messages=[
            {
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                        }
                    }
                ],
                "role": "user"
            }
        ],
        stream=stream_enabled,
        # stream设为False时，不能设置stream_options参数
        # stream_options={"include_usage": True},
        extra_body={
            "asr_options": {
                # "language": "zh",
                "enable_itn": False
            }
        }
    )
    if stream_enabled:
        full_content = ""
        print("流式输出内容为：")
        for chunk in completion:
            # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
            print(chunk)
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
        print(f"完整内容为：{full_content}")
    else:
        print(f"非流式输出内容为：{completion.choices[0].message.content}")
except Exception as e:
    print(f"错误信息：{e}")
```

#### Node.js SDK

```
// 运行前的准备工作:
// Windows/Mac/Linux 通用:
// 1. 确保已安装 Node.js (建议版本 >= 14)
// 2. 运行以下命令安装必要的依赖: npm install openai

import OpenAI from "openai";

const client = new OpenAI({
  // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1", 
});

async function main() {
  try {
    const streamEnabled = false; // 是否开启流式输出
    const completion = await client.chat.completions.create({
      model: "qwen3-asr-flash",
      messages: [
        {
          role: "user",
          content: [
            {
              type: "input_audio",
              input_audio: {
                data: "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
              }
            }
          ]
        }
      ],
      stream: streamEnabled,
      // stream设为False时，不能设置stream_options参数
      // stream_options: {
      //   "include_usage": true
      // },
      extra_body: {
        asr_options: {
          // language: "zh",
          enable_itn: false
        }
      }
    });

    if (streamEnabled) {
      let fullContent = "";
      console.log("流式输出内容为：");
      for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
        if (chunk.choices && chunk.choices.length > 0) {
          const delta = chunk.choices[0].delta;
          if (delta && delta.content) {
            fullContent += delta.content;
          }
        }
      }
      console.log(`完整内容为：${fullContent}`);
    } else {
      console.log(`非流式输出内容为：${completion.choices[0].message.content}`);
    }
  } catch (err) {
    console.error(`错误信息：${err}`);
  }
}

main();
```

#### cURL

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl -X POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-asr-flash",
    "messages": [
        {
            "content": [
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    }
                }
            ],
            "role": "user"
        }
    ],
    "stream":false,
    "asr_options": {
        "enable_itn": false
    }
}'
```

### 输入内容：Base64编码的音频文件

可输入Base64编码数据（[Data URL](https://www.rfc-editor.org/rfc/rfc2397)），格式为：`data:<mediatype>;base64,<data>`。

-   `<mediatype>`：MIME类型
    
    因音频格式而异，例如：
    
    -   WAV：`audio/wav`
        
    -   MP3：`audio/mpeg`
        
-   `<data>`：音频转成的Base64编码的字符串
    
    Base64编码会增大体积，请控制原文件大小，确保编码后仍符合输入音频大小限制（10MB）
    
-   示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`
    
    **点击查看示例代码**
    
    Python
    
    ```
    import base64, pathlib
    
    # input.mp3为用于声音复刻的本地音频文件，请替换为自己的音频文件路径，确保其符合音频要求
    file_path = pathlib.Path("input.mp3")
    base64_str = base64.b64encode(file_path.read_bytes()).decode()
    data_uri = f"data:audio/mpeg;base64,{base64_str}"
    ```
    
    Java
    
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
    

#### Python SDK

示例中用到的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260105/wotsae/welcome.mp3)。

```
import base64
from openai import OpenAI
import os
import pathlib

try:
    # 请替换为实际的音频文件路径
    file_path = "welcome.mp3"
    # 请替换为实际的音频文件MIME类型
    audio_mime_type = "audio/mpeg"

    file_path_obj = pathlib.Path(file_path)
    if not file_path_obj.exists():
        raise FileNotFoundError(f"音频文件不存在: {file_path}")

    base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
    data_uri = f"data:{audio_mime_type};base64,{base64_str}"

    client = OpenAI(
        # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    

    stream_enabled = False  # 是否开启流式输出
    completion = client.chat.completions.create(
        model="qwen3-asr-flash",
        messages=[
            {
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": data_uri
                        }
                    }
                ],
                "role": "user"
            }
        ],
        stream=stream_enabled,
        # stream设为False时，不能设置stream_options参数
        # stream_options={"include_usage": True},
        extra_body={
            "asr_options": {
                # "language": "zh",
                "enable_itn": False
            }
        }
    )
    if stream_enabled:
        full_content = ""
        print("流式输出内容为：")
        for chunk in completion:
            # 如果stream_options.include_usage为True，则最后一个chunk的choices字段为空列表，需要跳过（可以通过chunk.usage获取 Token 使用量）
            print(chunk)
            if chunk.choices and chunk.choices[0].delta.content:
                full_content += chunk.choices[0].delta.content
        print(f"完整内容为：{full_content}")
    else:
        print(f"非流式输出内容为：{completion.choices[0].message.content}")
except Exception as e:
    print(f"错误信息：{e}")
```

#### Node.js SDK

示例中用到的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260105/wotsae/welcome.mp3)。

```
// 运行前的准备工作:
// Windows/Mac/Linux 通用:
// 1. 确保已安装 Node.js (建议版本 >= 14)
// 2. 运行以下命令安装必要的依赖: npm install openai

import OpenAI from "openai";
import { readFileSync } from 'fs';

const client = new OpenAI({
  // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
  // 若没有配置环境变量，请用百炼API Key将下行替换为：apiKey: "sk-xxx",
  apiKey: process.env.DASHSCOPE_API_KEY,
  // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
  baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1", 
});

const encodeAudioFile = (audioFilePath) => {
    const audioFile = readFileSync(audioFilePath);
    return audioFile.toString('base64');
};

// 请替换为实际的音频文件路径
const dataUri = `data:audio/mpeg;base64,${encodeAudioFile("welcome.mp3")}`;

async function main() {
  try {
    const streamEnabled = false; // 是否开启流式输出
    const completion = await client.chat.completions.create({
      model: "qwen3-asr-flash",
      messages: [
        {
          role: "user",
          content: [
            {
              type: "input_audio",
              input_audio: {
                data: dataUri
              }
            }
          ]
        }
      ],
      stream: streamEnabled,
      // stream设为False时，不能设置stream_options参数
      // stream_options: {
      //   "include_usage": true
      // },
      extra_body: {
        asr_options: {
          // language: "zh",
          enable_itn: false
        }
      }
    });

    if (streamEnabled) {
      let fullContent = "";
      console.log("流式输出内容为：");
      for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
        if (chunk.choices && chunk.choices.length > 0) {
          const delta = chunk.choices[0].delta;
          if (delta && delta.content) {
            fullContent += delta.content;
          }
        }
      }
      console.log(`完整内容为：${fullContent}`);
    } else {
      console.log(`非流式输出内容为：${completion.choices[0].message.content}`);
    }
  } catch (err) {
    console.error(`错误信息：${err}`);
  }
}

main();
```

**model** `_string_` **（必选）**

[模型](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#b8c8c0483153o)名称。仅适用于千问3-ASR-Flash模型。

**messages** `_array_` **（必选）**

消息列表。

**消息类型**

System Message `_object_`（可选）

模型的目标或角色。如果设置系统消息，请放在messages列表的第一位。

**属性**

**role** `_string_` **（必选）**

固定为`system`。

User Message `_object_`**（必选）**

用户发送给模型的消息。

**属性**

**content** `_array_` **（必选）**

用户消息的内容。仅允许设置一组消息。

**属性**

**type** `_string_`**（必选）**

固定为`input_audio`，代表输入的是音频。

**input\_audio** `_string_`**（必选）**

待识别音频。具体用法请参见[快速开始](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)。

千问3-ASR-Flash模型在OpenAI兼容模式下支持两种输入形式：Base64编码的文件和公网可访问的待识别文件URL。

使用SDK时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，不支持使用以 `oss://`为前缀的临时 URL。

使用RESTful API时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，支持使用以 `oss://`为前缀的临时 URL。但需注意：

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    

**role** `_string_` **（必选）**

用户消息的角色，固定为`user`。

**asr\_options** `_object_` （可选）

用来指定某些功能是否启用。

> `asr_options`非OpenAI标准参数，若使用OpenAI SDK，请通过`extra_body`传入。

**属性**

**language** _string_（可选）无默认值

若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率。

只能指定一个语种。

若音频语种不确定，或包含多种语种（例如中英日韩混合），请勿指定该参数。

**取值范围**

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    
-   cs：捷克语
    
-   da：丹麦语
    
-   fil：菲律宾语
    
-   fi：芬兰语
    
-   is：冰岛语
    
-   ms：马来语
    
-   no：挪威语
    
-   pl：波兰语
    
-   sv：瑞典语
    

**enable\_itn** `_boolean_`（可选）默认值为`false`

是否启用ITN（Inverse Text Normalization，逆文本标准化）。该功能仅适用于中文和英文音频。

参数值：

-   true：开启；
    
-   false：关闭。
    

**stream** `_boolean_` （可选）默认值为`false`

是否以流式输出方式回复。相关文档：[流式输出](https://help.aliyun.com/zh/model-studio/stream)

可选值：

-   `false`：模型生成全部内容后一次性返回；
    
-   `true`：边生成边输出，每生成一部分内容即返回一个数据块（chunk）。需实时逐个读取这些块以拼接完整回复。
    

推荐设置为`true`，可提升阅读体验并降低超时风险。

**stream\_options** `_object_` （可选）

流式输出的配置项，仅在 `stream` 为 `true` 时生效。

**属性**

**include\_usage** `_boolean_` （可选）默认值为`false`

是否在响应的最后一个数据块包含Token消耗信息。

可选值：

-   `true`：包含；
    
-   `false`：不包含。
    

> 流式输出时，Token 消耗信息仅可出现在响应的最后一个数据块。

### **返回体**

## 非流式输出

```
{
    "choices": [
        {
            "finish_reason": "stop",
            "index": 0,
            "message": {
                "annotations": [
                    {
                        "emotion": "neutral",
                        "language": "zh",
                        "type": "audio_info"
                    }
                ],
                "content": "欢迎使用阿里云。",
                "role": "assistant"
            }
        }
    ],
    "created": 1767683986,
    "id": "chatcmpl-487abe5f-d4f2-9363-a877-xxxxxxx",
    "model": "qwen3-asr-flash",
    "object": "chat.completion",
    "usage": {
        "completion_tokens": 12,
        "completion_tokens_details": {
            "text_tokens": 12
        },
        "prompt_tokens": 42,
        "prompt_tokens_details": {
            "audio_tokens": 42,
            "text_tokens": 0
        },
        "seconds": 1,
        "total_tokens": 54
    }
}
```

## 流式输出

```
data: {"model":"qwen3-asr-flash","id":"chatcmpl-3fb97803-d27f-9289-8889-xxxxx","created":1767685989,"object":"chat.completion.chunk","usage":null,"choices":[{"logprobs":null,"index":0,"delta":{"content":"","role":"assistant"}}]}

data: {"model":"qwen3-asr-flash","id":"chatcmpl-3fb97803-d27f-9289-8889-xxxxx","choices":[{"delta":{"annotations":[{"type":"audio_info","language":"zh","emotion":"neutral"}],"content":"欢迎","role":null},"index":0}],"created":1767685989,"object":"chat.completion.chunk","usage":null}

data: {"model":"qwen3-asr-flash","id":"chatcmpl-3fb97803-d27f-9289-8889-xxxxx","choices":[{"delta":{"annotations":[{"type":"audio_info","language":"zh","emotion":"neutral"}],"content":"使用","role":null},"index":0}],"created":1767685989,"object":"chat.completion.chunk","usage":null}

data: {"model":"qwen3-asr-flash","id":"chatcmpl-3fb97803-d27f-9289-8889-xxxxx","choices":[{"delta":{"annotations":[{"type":"audio_info","language":"zh","emotion":"neutral"}],"content":"阿里","role":null},"index":0}],"created":1767685989,"object":"chat.completion.chunk","usage":null}

data: {"model":"qwen3-asr-flash","id":"chatcmpl-3fb97803-d27f-9289-8889-xxxxx","choices":[{"delta":{"annotations":[{"type":"audio_info","language":"zh","emotion":"neutral"}],"content":"云","role":null},"index":0}],"created":1767685989,"object":"chat.completion.chunk","usage":null}

data: {"model":"qwen3-asr-flash","id":"chatcmpl-3fb97803-d27f-9289-8889-xxxxx","choices":[{"delta":{"annotations":[{"type":"audio_info","language":"zh","emotion":"neutral"}],"content":"。","role":null},"index":0}],"created":1767685989,"object":"chat.completion.chunk","usage":null}

data: {"model":"qwen3-asr-flash","id":"chatcmpl-3fb97803-d27f-9289-8889-xxxxx","choices":[{"delta":{"role":null},"index":0,"finish_reason":"stop"}],"created":1767685989,"object":"chat.completion.chunk","usage":null}

data: [DONE]
```

**id** `_string_`

本次调用的唯一标识符。

**choices** `_array_`

模型的输出信息。

**属性**

**finish\_reason** `_string_`

有三种情况：

-   正在生成时为null；
    
-   因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；
    
-   因生成长度过长而结束为length。
    

**index** `_integer_`

当前对象在`choices`数组中的索引。

**message** `_object_`

模型输出的消息对象。

**属性**

**role** `_string_`

输出消息的角色，固定为assistant。

**content** `_array_`

语音识别结果。

**annotations** `_array_`

输出标注信息（如语种）

**属性**

**language** `_string_`

被识别音频的语种。当请求参数`language`已指定语种时，该值与所指定的参数一致。

**取值范围**

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    
-   cs：捷克语
    
-   da：丹麦语
    
-   fil：菲律宾语
    
-   fi：芬兰语
    
-   is：冰岛语
    
-   ms：马来语
    
-   no：挪威语
    
-   pl：波兰语
    
-   sv：瑞典语
    

**type** `_string_`

固定为`audio_info`，表示音频信息。

**emotion** `_string_`

被识别音频的情感。支持的情感如下：

-   `surprised`：惊讶
    
-   `neutral`：平静
    
-   `happy`：愉快
    
-   `sad`：悲伤
    
-   `disgusted`：厌恶
    
-   `angry`：愤怒
    
-   `fearful`：恐惧
    

**created** `_integer_`

请求创建时的 Unix 时间戳（秒）。

**model** `_string_`

本次请求使用的模型。

**object** `_string_`

始终为`chat.completion`。

**usage** `_object_`

本次请求的Token消耗信息。

**属性**

**completion\_tokens** `_integer_`

模型输出的 Token 数。

**completion\_tokens\_details** `_object_`

模型输出的 Token 细粒度详情。

**属性**

**text\_tokens** `_integer_`

模型输出文本的Token数。

**prompt\_tokens** `_object_`

输入的Token数。

**prompt\_tokens\_details** `_object_`

输入的 Token 细粒度详情。

**属性**

**audio\_tokens** `_integer_`

输入音频长度（Token）。音频转换Token规则：每秒音频转换为25个Token，不足1秒按1秒计算。

**text\_tokens** `_integer_`

无需关注该参数。

**seconds** `_integer_`

音频时长（秒）。

**total\_tokens** `_integer_`

输入和输出总Token数（`total_tokens = completion_tokens + prompt_tokens`）。

## **DashScope同步调用**

### **URL**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

HTTP请求地址：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://dashscope.aliyuncs.com/api/v1`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，数据存储位于**新加坡接入地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

HTTP请求地址：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://dashscope-intl.aliyuncs.com/api/v1`

## 美国

服务部署范围为[美国](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，数据存储位于**美国（弗吉尼亚）接入地域**，模型推理计算资源仅限于美国境内。

HTTP请求地址：`POST https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`

SDK调用配置的base\_url：`https://dashscope-us.aliyuncs.com/api/v1`

### **请求体**

以下示例为音频 URL 识别；本地音频文件识别示例请参见[快速开始](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)。

## cURL

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation
# 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若使用美国地域的模型，需要加us后缀
# === 执行时请删除该注释 ===

curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "qwen3-asr-flash",
    "input": {
        "messages": [
            {
                "content": [
                    {
                        "text": ""
                    }
                ],
                "role": "system"
            },
            {
                "content": [
                    {
                        "audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    }
                ],
                "role": "user"
            }
        ]
    },
    "parameters": {
        "asr_options": {
            "enable_itn": false
        }
    }
}'
```

## Java

```
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;

public class Main {
    public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
        MultiModalConversation conv = new MultiModalConversation();
        MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3")))
                .build();

        Map<String, Object> asrOptions = new HashMap<>();
        asrOptions.put("enable_itn", false);
        // asrOptions.put("language", "zh"); // 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
                .model("qwen3-asr-flash")
                .message(userMessage)
                .parameter("asr_options", asrOptions)
                .build();
        MultiModalConversationResult result = conv.call(param);
        System.out.println(JsonUtils.toJson(result));
    }
    public static void main(String[] args) {
        try {
            // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
            simpleMultiModalConversationCall();
        } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
        }
        System.exit(0);
    }
}
```

## Python

```
import os
import dashscope

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1，若使用美国地域的模型，需将url替换为：https://dashscope-us.aliyuncs.com/api/v1
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

messages = [
    {"role": "user", "content": [{"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}]}
]

response = dashscope.MultiModalConversation.call(
    # 新加坡/美国地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 若使用美国地域的模型，需在模型后面加上“-us”后缀，例如qwen3-asr-flash-us
    model="qwen3-asr-flash",
    messages=messages,
    result_format="message",
    asr_options={
        # "language": "zh", # 可选，若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率
        "enable_itn":False
    }
)
print(response)
```

**model** `_string_` **（必选）**

[模型](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#b8c8c0483153o)名称。仅适用于千问3-ASR-Flash模型。

**messages** `_array_` **（必选）**

消息列表。

> 通过HTTP调用时，请将**messages** 放入 **input** 对象中。

**消息类型**

System Message `_object_`（可选）

模型的目标或角色。如果设置系统消息，请放在messages列表的第一位。

仅千问3-ASR-Flash支持该参数。

**属性**

**role** `_string_` **（必选）**

固定为`system`。

User Message `_object_`**（必选）**

用户发送给模型的消息。

**属性**

**content** `_array_` **（必选）**

用户消息的内容。仅允许设置一组消息。

**属性**

**audio** `_string_`**（必选）**

待识别音频。具体用法请参见[快速开始](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)。

千问3-ASR-Flash模型在DashScope调用方式下支持三种输入形式：Base64编码的文件、本地文件绝对路径、公网可访问的待识别文件URL。

使用SDK时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，不支持使用以 `oss://`为前缀的临时 URL。

使用RESTful API时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，支持使用以 `oss://`为前缀的临时 URL。但需注意：

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    

**role** `_string_` **（必选）**

用户消息的角色，固定为`user`。

**asr\_options** `_object_` （可选）

用来指定某些功能是否启用。

仅千问3-ASR-Flash支持该参数。

**属性**

**language** _string_（可选）无默认值

若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率。

只能指定一个语种。

若音频语种不确定，或包含多种语种（例如中英日韩混合），请勿指定该参数。

**取值范围**

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    
-   cs：捷克语
    
-   da：丹麦语
    
-   fil：菲律宾语
    
-   fi：芬兰语
    
-   is：冰岛语
    
-   ms：马来语
    
-   no：挪威语
    
-   pl：波兰语
    
-   sv：瑞典语
    

**enable\_itn** `_boolean_`（可选）默认值为`false`

是否启用ITN（Inverse Text Normalization，逆文本标准化）。该功能仅适用于中文和英文音频。

参数值：

-   true：开启；
    
-   false：关闭。
    

### **返回体**

```
{
    "output": {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {
                    "annotations": [
                        {
                            "language": "zh",
                            "type": "audio_info",
                            "emotion": "neutral"
                        }
                    ],
                    "content": [
                        {
                            "text": "欢迎使用阿里云。"
                        }
                    ],
                    "role": "assistant"
                }
            }
        ]
    },
    "usage": {
        "input_tokens_details": {
            "text_tokens": 0
        },
        "output_tokens_details": {
            "text_tokens": 6
        },
        "seconds": 1
    },
    "request_id": "568e2bf0-d6f2-97f8-9f15-a57b11dc6977"
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

> Java SDK返回参数为**requestId。**

**output** `_object_`

调用结果信息。

**属性**

**choices** `_array_`

模型的输出信息。当result\_format为message时返回choices参数。

**属性**

**finish\_reason** `_string_`

有三种情况：

-   正在生成时为null；
    
-   因模型输出自然结束，或触发输入参数中的stop条件而结束时为stop；
    
-   因生成长度过长而结束为length。
    

**message** `_object_`

模型输出的消息对象。

**属性**

**role** `_string_`

输出消息的角色，固定为assistant。

**content** `_array_`

输出消息的内容。

**属性**

**text** `_string_`

语音识别结果。

**annotations** `_array_`

输出标注信息（如语种）

**属性**

**language** `_string_`

被识别音频的语种。当请求参数`language`已指定语种时，该值与所指定的参数一致。

**取值范围**

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    
-   cs：捷克语
    
-   da：丹麦语
    
-   fil：菲律宾语
    
-   fi：芬兰语
    
-   is：冰岛语
    
-   ms：马来语
    
-   no：挪威语
    
-   pl：波兰语
    
-   sv：瑞典语
    

**type** `_string_`

固定为`audio_info`，表示音频信息。

**emotion** `_string_`

被识别音频的情感。支持的情感如下：

-   `surprised`：惊讶
    
-   `neutral`：平静
    
-   `happy`：愉快
    
-   `sad`：悲伤
    
-   `disgusted`：厌恶
    
-   `angry`：愤怒
    
-   `fearful`：恐惧
    

**usage** `_object_`

本次请求的Token消耗信息。

**属性**

**input\_tokens\_details** `_object_`

千问3-ASR-Flash输入内容长度（Token）。

**属性**

**text\_tokens** `_integer_`

无需关注该参数。

**output\_tokens\_details** `_object_`

千问3-ASR-Flash输出内容长度（Token）。

**属性**

**text\_tokens** `_integer_`

千问3-ASR-Flash输出的识别结果文本长度（Token）。

**seconds** `_integer_`

千问3-ASR-Flash音频时长（秒）。

## **DashScope异步调用**

### **流程说明**

与OpenAI兼容模式或DashScope同步调用（均为一次请求、立即返回结果）不同，异步调用专为处理长音频文件或耗时较长的任务设计，该模式采用“提交-轮询”的两步式流程，避免了因长时间等待而导致的请求超时：

1.  第一步：提交任务
    
    -   客户端发起一个异步处理请求。
        
    -   服务器验证请求后，不会立即执行任务，而是返回一个唯一的 `task_id`，表示任务已成功创建。
        
2.  第二步：获取结果
    
    -   客户端使用获取到的 `task_id`，通过轮询方式反复调用结果查询接口。
        
    -   当任务处理完成后，结果查询接口将返回最终的识别结果。
        

您可以根据集成环境选择使用SDK或直接调用RESTful API。

-   使用 SDK（示例代码请参见[快速开始](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)，请求参数请参见[提交任务](#88657039c4x0g)的[请求体](#1a2369eebaueh)，返回结果请参见[异步调用识别结果说明](#2c27ad3e80p4y)）
    
    SDK封装了底层的API调用细节，提供了更便捷的编程体验。
    
    1.  提交任务：调用 `async_call()` (Python) 或 `asyncCall()` (Java) 方法提交任务。此方法将返回一个包含 `task_id` 的任务对象。
        
    2.  获取结果：使用上一步返回的任务对象或 `task_id`，调用 `fetch()` 方法获取结果。SDK内部会自动处理轮询逻辑，直到任务完成或超时。
        
-   2\. 使用 RESTful API
    
    直接调用HTTP接口提供了最大的灵活性。
    
    1.  [提交任务](#88657039c4x0g)，如果请求成功，[返回体](#eca6c7d3f35hn)中将包含一个 `task_id`。
        
    2.  使用上一步获取的 `task_id`，[获取任务执行结果](#f9109f6ea3di2)。
        

### **提交任务**

#### **URL**

## 中国内地

服务部署范围为[中国内地](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，数据存储位于**北京接入地域**，模型推理计算资源仅限于中国内地。

HTTP请求地址：`POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription`

SDK调用配置的base\_url：`https://dashscope.aliyuncs.com/api/v1`

## 国际

服务部署范围为[国际](https://help.aliyun.com/zh/model-studio/regions/#080da663a75xh)时，数据存储位于**新加坡接入地域**，模型推理计算资源在全球范围内动态调度（不含中国内地）。

HTTP请求地址：`POST https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription`

SDK调用配置的base\_url：`https://dashscope-intl.aliyuncs.com/api/v1`

#### **请求体**

## cURL

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "Content-Type: application/json" \
--header "X-DashScope-Async: enable" \
--data '{
    "model": "qwen3-asr-flash-filetrans",
    "input": {
        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
    },
    "parameters": {
        "channel_id":[
            0
        ],
        "enable_itn": false
    }
}'
```

## Java

SDK示例请参见[快速开始](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)。

```
import com.google.gson.Gson;
import com.google.gson.annotations.SerializedName;
import okhttp3.*;

import java.io.IOException;

public class Main {
    // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription
    private static final String API_URL = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription";

    public static void main(String[] args) {
        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx"
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        OkHttpClient client = new OkHttpClient();
        Gson gson = new Gson();

        /*String payloadJson = """
                {
                    "model": "qwen3-asr-flash-filetrans",
                    "input": {
                        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    },
                    "parameters": {
                        "channel_id": [0],
                        "enable_itn": false,
                        "language": "zh",
                        "corpus": {
                            "text": ""
                        }
                    }
                }
                """;*/
        String payloadJson = """
                {
                    "model": "qwen3-asr-flash-filetrans",
                    "input": {
                        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                    },
                    "parameters": {
                        "channel_id": [0],
                        "enable_itn": false
                    }
                }
                """;

        RequestBody body = RequestBody.create(payloadJson, MediaType.get("application/json; charset=utf-8"));
        Request request = new Request.Builder()
                .url(API_URL)
                .addHeader("Authorization", "Bearer " + apiKey)
                .addHeader("Content-Type", "application/json")
                .addHeader("X-DashScope-Async", "enable")
                .post(body)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                String respBody = response.body().string();
                // 用 Gson 解析 JSON
                ApiResponse apiResp = gson.fromJson(respBody, ApiResponse.class);
                if (apiResp.output != null) {
                    System.out.println("task_id: " + apiResp.output.taskId);
                } else {
                    System.out.println(respBody);
                }
            } else {
                System.out.println("task failed! HTTP code: " + response.code());
                if (response.body() != null) {
                    System.out.println(response.body().string());
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class ApiResponse {
        @SerializedName("request_id")
        String requestId;

        Output output;
    }

    static class Output {
        @SerializedName("task_id")
        String taskId;

        @SerializedName("task_status")
        String taskStatus;
    }
}
```

## Python

SDK示例请参见[快速开始](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)。

```
import requests
import json
import os

# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/services/audio/asr/transcription
url = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"

# 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：DASHSCOPE_API_KEY = "sk-xxx"
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

headers = {
    "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
    "Content-Type": "application/json",
    "X-DashScope-Async": "enable"
}

payload = {
    "model": "qwen3-asr-flash-filetrans",
    "input": {
        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
    },
    "parameters": {
        "channel_id": [0],
        # "language": "zh",
        "enable_itn": False
        # "corpus": {
        #     "text": ""
        # }
    }
}

response = requests.post(url, headers=headers, data=json.dumps(payload))
if response.status_code == 200:
    print(f"task_id: {response.json()["output"]["task_id"]}")
else:
    print("task failed!")
    print(response.json())
```

**model** `_string_` **（必选）**

[模型](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#b8c8c0483153o)名称。仅适用于千问3-ASR-Flash-Filetrans模型。

**input** `_object_` **（必选）**

**属性**

**file\_url** `_string_`**（必选）**

待识别音频文件URL，URL必须公网可访问。

使用SDK时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，不支持使用以 `oss://`为前缀的临时 URL。

使用RESTful API时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，支持使用以 `oss://`为前缀的临时 URL。但需注意：

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    

**parameters** `_object_` （可选）

**属性**

**language** _string_（可选）无默认值

若已知音频的语种，可通过该参数指定待识别语种，以提升识别准确率。

只能指定一个语种。

若音频语种不确定，或包含多种语种（例如中英日韩混合），请勿指定该参数。

**取值范围**

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    
-   cs：捷克语
    
-   da：丹麦语
    
-   fil：菲律宾语
    
-   fi：芬兰语
    
-   is：冰岛语
    
-   ms：马来语
    
-   no：挪威语
    
-   pl：波兰语
    
-   sv：瑞典语
    

**enable\_itn** `_boolean_`（可选）默认值为`false`

是否启用ITN（Inverse Text Normalization，逆文本标准化）。该功能仅适用于中文和英文音频。

参数值：

-   true：开启；
    
-   false：关闭。
    

**enable\_words** `_boolean_` （可选）默认值为`false`

控制是否返回字级别时间戳：

-   `false`：返回句级时间戳
    
-   `true`：返回字级时间戳
    
    字级别时间戳仅支持以下语种：中文、英语、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语、俄语，其他语种可能无法保证准确性
    

同时，该参数还影响断句规则：

-   `false`：基于 VAD（语音活动检测）断句
    
-   `true`：基于 VAD + 标点符号断句
    

**channel\_id** `_array_` （可选）默认值为`[0]`

指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，\[0\] 表示识别第一个音轨，\[0, 1\] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。

**重要**

指定的每一个音轨都将独立计费。例如，为单个文件请求 \[0, 1\] 会产生两笔独立的费用。

#### **返回体**

```
{
    "request_id": "92e3decd-0c69-47a8-************",
    "output": {
        "task_id": "8fab76d0-0eed-4d20-************",
        "task_status": "PENDING"
    }
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

调用结果信息。

**属性**

**task\_id** `_string_`

任务ID。该ID在查询语音识别任务接口中作为请求参数传入。

**task\_status** `_string_`

任务状态：

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   UNKNOWN：任务不存在或状态未知
    

### **获取任务执行结果**

#### **URL**

## 中国内地

HTTP请求地址：`GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`

SDK调用配置的base\_url：`https://dashscope.aliyuncs.com/api/v1`

## 国际

HTTP请求地址：`GET https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}`

SDK调用配置的base\_url：`https://dashscope-intl.aliyuncs.com/api/v1`

#### **请求体**

## cURL

```
# ======= 重要提示 =======
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}，注意，将{task_id}替换为待查询任务ID
# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# === 执行时请删除该注释 ===

curl --location --request GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header "X-DashScope-Async: enable" \
--header "Content-Type: application/json"
```

## Java

SDK示例请参见[快速开始](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)。

```
import okhttp3.*;

import java.io.IOException;

public class Main {
    public static void main(String[] args) {
        // 替换为实际的task_id
        String taskId = "xxx";
        // 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
        // 若没有配置环境变量，请用百炼API Key将下行替换为：String apiKey = "sk-xxx"
        String apiKey = System.getenv("DASHSCOPE_API_KEY");

        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}，注意，将{task_id}替换为待查询任务ID
        String apiUrl = "https://dashscope.aliyuncs.com/api/v1/tasks/" + taskId;

        OkHttpClient client = new OkHttpClient();

        Request request = new Request.Builder()
                .url(apiUrl)
                .addHeader("Authorization", "Bearer " + apiKey)
                .addHeader("X-DashScope-Async", "enable")
                .addHeader("Content-Type", "application/json")
                .get()
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.body() != null) {
                System.out.println(response.body().string());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

## Python

SDK示例请参见[快速开始](https://help.aliyun.com/zh/model-studio/non-realtime-speech-recognition-user-guide#7818a3bc466d6)。

```
import os
import requests

# 新加坡地域和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
# 若没有配置环境变量，请用百炼API Key将下行替换为：DASHSCOPE_API_KEY = "sk-xxx"
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

# 替换为实际的task_id
task_id = "xxx"
# 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1/tasks/{task_id}，注意，将{task_id}替换为待查询任务ID
url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"

headers = {
    "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
    "X-DashScope-Async": "enable",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)
print(response.json())
```

**task\_id** `_string_` **（必选）**

任务ID。将[提交任务](#88657039c4x0g)返回结果中的task\_id作为参数传入，查询语音识别结果。

#### **返回体**

## RUNNING

```
{
    "request_id": "6769df07-2768-4fb0-ad59-************",
    "output": {
        "task_id": "9be1700a-0f8e-4778-be74-************",
        "task_status": "RUNNING",
        "submit_time": "2025-10-27 14:19:31.150",
        "scheduled_time": "2025-10-27 14:19:31.233",
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 0,
            "FAILED": 0
        }
    }
}
```

## SUCCEEDED

```
{
    "request_id": "1dca6c0a-0ed1-4662-aa39-************",
    "output": {
        "task_id": "8fab76d0-0eed-4d20-929f-************",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-10-27 13:57:45.948",
        "scheduled_time": "2025-10-27 13:57:46.018",
        "end_time": "2025-10-27 13:57:47.079",
        "result": {
            "transcription_url": "http://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/pre/pre-funasr-mlt-v1/20251027/13%3A57/7a3a8236-ffd1-4099-a280-0299686ac7da.json?Expires=1761631066&OSSAccessKeyId=LTAI**************&Signature=1lKv4RgyWCarRuUdIiErOeOBnwM%3D&response-content-disposition=attachment%3Bfilename%3D7a3a8236-ffd1-4099-a280-0299686ac7da.json"
        }
    },
    "usage": {
        "seconds": 3
    }
}
```

## FAILED

```
{
    "request_id": "3d141841-858a-466a-9ff9-************",
    "output": {
        "task_id": "c58c7951-7789-4557-9ea3-************",
        "task_status": "FAILED",
        "submit_time": "2025-10-27 15:06:06.915",
        "scheduled_time": "2025-10-27 15:06:06.967",
        "end_time": "2025-10-27 15:06:07.584",
        "code": "FILE_403_FORBIDDEN",
        "message": "FILE_403_FORBIDDEN"
    }
}
```

**request\_id** `_string_`

本次调用的唯一标识符。

**output** `_object_`

调用结果信息。

**属性**

**task\_id** `_string_`

任务ID。该ID在查询语音识别任务接口中作为请求参数传入。

**task\_status** `_string_`

任务状态：

-   PENDING：任务排队中
    
-   RUNNING：任务处理中
    
-   SUCCEEDED：任务执行成功
    
-   FAILED：任务执行失败
    
-   UNKNOWN：任务不存在或状态未知
    

**result** `_object_`

语音识别结果。

**属性**

**transcription\_url** `_string_`

识别结果文件的下载 URL，链接有效期为 24 小时。过期后无法查询任务，也无法通过先前的 URL 下载结果。  
识别结果以 JSON 文件保存，可通过该链接下载文件，或直接使用 HTTP 请求读取文件内容。

详情参见[异步调用识别结果说明](#2c27ad3e80p4y)。

**submit\_time** `_string_`

任务提交时间。

**schedule\_time** `_string_`

任务调度时间，即开始执行时间。

**end\_time** `_string_`

任务结束时间。

**task\_metrics** `_object_`

任务指标，包含子任务状态的统计信息。

**属性**

**TOTAL** `_integer_`

子任务总数。

**SUCCEEDED** `_integer_`

子任务成功数。

**FAILED** `_integer_`

子任务失败数。

**code** `_string_`

错误码，仅在任务失败时返回。

**message** `_string_`

错误信息，仅任务失败时返回。

**usage** `_object_`

本次请求的Token消耗信息。

**属性**

**seconds** `_integer_`

千问3-ASR-Flash音频时长（秒）。

### **异步调用识别结果说明**

```
{
    "file_url": "https://***.mp3",
    "audio_info": {
        "format": "mp3",
        "sample_rate": 22050
    },
    "transcripts": [
        {
            "channel_id": 0,
            "text": "欢迎使用阿里云。",
            "sentences": [
                {
                    "sentence_id": 0,
                    "begin_time": 0,
                    "end_time": 1440,
                    "language": "zh",
                    "emotion": "neutral",
                    "text": "欢迎使用阿里云。",
                    "words": [
                        {
                            "begin_time": 0,
                            "end_time": 160,
                            "text": "欢",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 160,
                            "end_time": 320,
                            "text": "迎",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 320,
                            "end_time": 640,
                            "text": "使",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 640,
                            "end_time": 720,
                            "text": "用",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 880,
                            "end_time": 960,
                            "text": "阿",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 1040,
                            "end_time": 1120,
                            "text": "里",
                            "punctuation": ""
                        },
                        {
                            "begin_time": 1120,
                            "end_time": 1440,
                            "text": "云",
                            "punctuation": "。"
                        }
                    ]
                }
            ]
        }
    ]
}
```

**file\_url** `_string_`

被识别的音频文件URL。

**audio\_info** `_object_`

被识别音频文件相关信息。

**属性**

**format** `_string_`

音频格式。

**sample\_rate** `_integer_`

音频采样率。

**transcripts** `_array_`

完整的识别结果列表，每个元素对应一条音轨的识别内容。

**属性**

**channel\_id** `_integer_`

音轨索引，以0为起始。

**text** `_string_`

识别结果文本。

**sentences** `_object_`

句子级别的识别结果列表。

**属性**

**begin\_time**`_integer_`

句子开始时间戳（毫秒）。

**end\_time**`_integer_`

句子结束时间戳（毫秒）。

**text** `_string_`

识别结果文本。

**sentence\_id** `_integer_`

句子索引，以0为起始。

**language** `_string_`

被识别音频的语种。当请求参数`language`已指定语种时，该值与所指定的参数一致。

**取值范围**

-   zh：中文（普通话、四川话、闽南语、吴语）
    
-   yue：粤语
    
-   en：英文
    
-   ja：日语
    
-   de：德语
    
-   ko：韩语
    
-   ru：俄语
    
-   fr：法语
    
-   pt：葡萄牙语
    
-   ar：阿拉伯语
    
-   it：意大利语
    
-   es：西班牙语
    
-   hi：印地语
    
-   id：印尼语
    
-   th：泰语
    
-   tr：土耳其语
    
-   uk：乌克兰语
    
-   vi：越南语
    
-   cs：捷克语
    
-   da：丹麦语
    
-   fil：菲律宾语
    
-   fi：芬兰语
    
-   is：冰岛语
    
-   ms：马来语
    
-   no：挪威语
    
-   pl：波兰语
    
-   sv：瑞典语
    

**emotion** `_string_`

被识别音频的情感。支持的情感如下：

-   `surprised`：惊讶
    
-   `neutral`：平静
    
-   `happy`：愉快
    
-   `sad`：悲伤
    
-   `disgusted`：厌恶
    
-   `angry`：愤怒
    
-   `fearful`：恐惧
    

**words** `_object_`

词级别的识别结果列表。当请求参数`enable_words`设为`true`时展示该结果。

**属性**

**begin\_time**`_integer_`

开始时间戳（毫秒）。

**end\_time**`_integer_`

结束时间戳（毫秒）。

**text** `_string_`

识别结果文本。

**punctuation** `_string_`

标点符号。
