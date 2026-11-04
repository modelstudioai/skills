# 提升识别准确率

通过热词（即时热词、预编译热词）和上下文增强，改善人名、产品名、行业术语等词汇的语音识别效果。

## 选择优化方式

人名、产品名和行业术语可能与常用词发音相近，识别时容易出现同音字或词语错误。热词和上下文增强可为模型补充这些词汇的准确写法或相关背景，帮助改善识别效果。

选择优化方式时，先看业务已有的信息：有明确的术语清单，可使用热词；已有对话历史或业务说明，可使用上下文增强。热词再按词表是否需要跨请求复用，分为即时热词和预编译热词。使用前确认[支持的模型与地域](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#supported-models)。

**方式**

**适用情况**

**使用方法**

[即时热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_instant_h3)

待识别的人名、产品名等随请求变化，或只有少量临时术语，不需要保存和管理词表。

在每次识别请求中直接传入“词语：权重”对象。应用需准备待识别词语的准确写法，可通过权重调整模型对这些词语的偏好。

[预编译热词](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw_precompiled_h3)

已有业务词库，或一组术语会在多次识别中反复使用，希望统一维护词表。

先创建包含词语、权重和可选语种的热词列表，识别时引用列表 ID。词库有变化时更新列表，无需在每个识别请求中重复提交词条。

[上下文增强](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#ctx_enhance_h2)

应用已保存前几轮对话、业务说明或领域文本，希望直接利用这些内容辅助识别。

将相关文本作为上下文消息随音频传入，无需先提取词条或逐词设置权重。上下文应包含待识别术语的准确写法；只有明确的术语清单时，也可以使用热词解决同类问题。

## 使用热词

运行示例前，请先下载[示例音频](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav)并准备 API Key（可在[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)获取）。音频内容：“请把祺元项目的报告发给洛柯，下周我们要上线璇枢系统。”

### 即时热词

即时热词适合随请求变化的词语。在识别请求的 `parameters.vocabulary` 中传入 JSON 对象：键为热词文本（`string`），值为权重（`integer`），无需预先创建词表。

1.  **不配置热词，识别原始音频**
    
    未配置热词时，本例中的三个名称识别不准确。原始识别结果可通过以下请求获取。
    
    ```
    curl --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: disable" \
      --data '
    {
      "model": "qwen-audio-3.1-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": 16000
      }
    }
    '
    ```
    
2.  **随请求加入即时热词**
    
    在相同请求中加入“祺元”“洛柯”“璇枢”，权重均设为 4，其余输入保持一致。权重范围和调整方法参见[调整热词权重](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw08_weight_h3)。
    
    ```
    curl --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: disable" \
      --data '
    {
      "model": "qwen-audio-3.1-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": 16000,
        "vocabulary": {
          "祺元": 4,
          "洛柯": 4,
          "璇枢": 4
        }
      }
    }
    '
    ```
    

配置前后的识别文本示例如下：

**配置**

**识别文本示例**

未配置

请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。

配置后

请把祺元项目的报告发给洛柯，下周我们要上线璇枢系统。

### 预编译热词

预编译热词适合需要跨请求复用的业务词表。预先创建热词列表后，在识别请求中传入 `vocabulary_id`，无需每次重复提交词条。

创建时以 JSON 数组提交词条，每个元素的字段如下：

**字段**

**类型**

**必填**

**说明**

`text`

string

是

实际词语，语种须在所选模型的支持范围内。长度要求参见[热词文本规范](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw10_limit_h2)。

`weight`

integer

是

普通热词取值为 1～5，推荐从 4 起调。部分模型支持超级热词权重 50，详见[调整热词权重](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw08_weight_h3)。

`lang`

string

否

语种代码，限定词条作用的语种；语种未知时可省略。与识别接口 `language_hints` 的关系参见[组织与维护词表](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw08_design_h3)。

创建热词列表时指定的目标模型须与实际识别模型一致。

**说明**热词管理与语音识别必须使用同一账号，否则识别接口无法访问对应的热词列表。

#### HTTP / cURL

1.  **创建热词列表**
    
    以下示例使用 `qwen-audio-3.1-asr-flash`，通过 `target_model` 指定目标模型。保存响应中 `output.vocabulary_id` 的值。
    
    ```
    curl --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --data @- <<EOF
    {
      "model": "speech-biasing",
      "input": {
        "action": "create_vocabulary",
        "target_model": "qwen-audio-3.1-asr-flash",
        "prefix": "testpfx",
        "vocabulary": [
          {
            "text": "祺元",
            "weight": 4,
            "lang": "zh"
          },
          {
            "text": "洛柯",
            "weight": 4,
            "lang": "zh"
          },
          {
            "text": "璇枢",
            "weight": 4,
            "lang": "zh"
          }
        ]
      }
    }
    EOF
    ```
    
2.  **确认列表可用**
    
    将 `<vocabulary_id>` 替换为创建接口返回的列表 ID，再查询状态。确认响应中的 `output.status` 为 `OK` 后进行识别。
    
    ```
    export VOCABULARY_ID="<vocabulary_id>"
    
    curl --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --data @- <<EOF
    {
      "model": "speech-biasing",
      "input": {
        "action": "query_vocabulary",
        "vocabulary_id": "$VOCABULARY_ID"
      }
    }
    EOF
    ```
    
3.  **在识别请求中引用列表**
    
    在识别请求中通过 `parameters.vocabulary_id` 引用该列表，无需重复传入词条。
    
    ```
    curl --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: disable" \
      --data @- <<EOF
    {
      "model": "qwen-audio-3.1-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": 16000,
        "vocabulary_id": "$VOCABULARY_ID"
      }
    }
    EOF
    ```
    
4.  **复用或删除列表**
    
    后续请求可继续引用同一 ID。仅在不再需要此列表时调用以下删除接口，释放列表配额。
    
    ```
    curl --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/audio/asr/customization' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --data @- <<EOF
    {
      "model": "speech-biasing",
      "input": {
        "action": "delete_vocabulary",
        "vocabulary_id": "$VOCABULARY_ID"
      }
    }
    EOF
    ```
    

#### SDK

**说明**SDK 示例使用 DashScope Python SDK 2.0.1 及以上版本或 Java SDK 2.22.23 及以上版本，安装方法参见[安装 SDK](raw/model-api-reference/preparations/install-sdk.md)。

以下 Java、Python 示例使用 `qwen-audio-3.1-asr-flash-streaming`，完成创建、状态查询、识别和删除。`finally` 中的删除用于清理演示资源；生产环境需要复用时，保留列表及其 ID。

Java

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.utils.Constants;
import java.io.File;
import java.util.Arrays;
import com.alibaba.dashscope.audio.asr.vocabulary.Vocabulary;
import com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

public class Main {
    public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        String model = "qwen-audio-3.1-asr-flash-streaming";
        JsonArray words = new JsonArray();
        for (String text : Arrays.asList("祺元", "洛柯", "璇枢")) {
            JsonObject word = new JsonObject();
            word.addProperty("text", text);
            word.addProperty("weight", 4);
            words.add(word);
        }
        VocabularyService service = new VocabularyService(apiKey);
        // targetModel must match the model used for recognition.
        Vocabulary vocabulary = service.createVocabulary(model, "testpfx", words);
        try {
            if (!"OK".equals(service.queryVocabulary(vocabulary.getVocabularyId()).getStatus())) {
                throw new IllegalStateException("Vocabulary is not ready");
            }
            Recognition recognizer = new Recognition();
            try {
                RecognitionParam param = RecognitionParam.builder()
                        .model(model).apiKey(apiKey).format("wav").sampleRate(16000)
                        .vocabularyId(vocabulary.getVocabularyId()).build();
                System.out.println(recognizer.call(param, new File("asr-accuracy-example.wav")));
            } finally {
                recognizer.getDuplexApi().close(1000, "bye");
            }
        } finally {
            service.deleteVocabulary(vocabulary.getVocabularyId());
        }
        System.exit(0);
    }
}
```

Python

```
import os
import dashscope

client = dashscope.Client(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
model = "qwen-audio-3.1-asr-flash-streaming"
vocabulary = client.audio.vocabularies.create(
    prefix="testpfx",
    target_model=model,
    vocabulary=[{"text": word, "weight": 4} for word in ["祺元", "洛柯", "璇枢"]],
)
try:
    if client.audio.vocabularies.get(vocabulary.vocabulary_id).status != "OK":
        raise RuntimeError("Vocabulary is not ready")
    for event in client.audio.asr.recognize_file(
        "asr-accuracy-example.wav", model=model, format="wav", sample_rate=16000,
        vocabulary_id=vocabulary.vocabulary_id,
    ):
        sentence = ((event.get("payload") or {}).get("output") or {}).get("sentence") or {}
        if sentence.get("text") and not sentence.get("heartbeat"):
            print(sentence["text"])
finally:
    client.audio.vocabularies.delete(vocabulary.vocabulary_id)
```

## 使用上下文增强

上下文增强可以直接利用已有对话历史或领域文本。与热词要求应用提供词语和权重不同，上下文以文本消息传入，不需要先把业务资料拆成词条。两种方式都可能改善专有名词的识别，应根据应用已有的信息选择。

### 准备上下文

沿用上述音频：如果应用已有“祺元项目、璇枢系统、同事洛柯”的业务信息，可直接传入包含这些准确名称的文本。常见的上下文来源有以下两种。

#### 业务背景或领域文本

例如已有的项目说明或行业资料。将相关文本放入 `role=user`、`type=input_text` 的消息中，无需为此构造对话或添加回复。以下数组可作为上下文传入：

```
[
  {
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "我在祺元项目工作，负责璇枢系统。我的同事叫洛柯。"
      }
    ]
  }
]
```

#### 历史对话

使用已有的用户识别文本和大模型回复：用户文本使用 `role=user`、`type=input_text`，回复使用 `role=assistant`、`type=text`。以下对话中已出现待识别名称，可直接作为后续识别的背景：

```
[
  {
    "role": "user",
    "content": [
      {
        "type": "input_text",
        "text": "我在祺元项目工作，负责璇枢系统。我的同事叫洛柯。"
      }
    ]
  },
  {
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "好的，我们继续讨论祺元项目、璇枢系统和洛柯的工作。"
      }
    ]
  }
]
```

**说明**`assistant` 消息可省略。使用历史对话时，按轮次排列，每轮 `user` 在对应 `assistant` 之前。文本长度和保留轮数参见[使用限制](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw10_limit_h2)。

### 配置与调用

使用准备好的上下文识别同一段音频，按模型系列选择调用示例。

#### Qwen-Audio-ASR

以下示例使用 `qwen-audio-3.1-asr-flash`，在 `input.messages` 中按顺序放入上下文消息，并将包含 `input_audio` 的当前音频消息放在最后。

```
curl --request POST 'https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --header "X-DashScope-SSE: disable" \
  --data '
{
  "model": "qwen-audio-3.1-asr-flash",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_text",
            "text": "我在祺元项目工作，负责璇枢系统。我的同事叫洛柯。"
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "好的，我们继续讨论祺元项目、璇枢系统和洛柯的工作。"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
            }
          }
        ]
      }
    ]
  },
  "parameters": {
    "format": "wav",
    "sample_rate": 16000
  }
}
'
```

#### Qwen-Audio-ASR-Message / Qwen-Audio-ASR-Streaming

以下示例使用 `qwen-audio-3.1-asr-flash-streaming`（也可替换为 `qwen-audio-3.1-asr-flash-message`），在启动任务时通过 `input.context` 传入上下文。

**说明**SDK 示例使用 DashScope Python SDK 2.0.1 及以上版本或 Java SDK 2.22.23 及以上版本，安装方法参见[安装 SDK](raw/model-api-reference/preparations/install-sdk.md)。

Java

```
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.utils.Constants;
import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

public class Main {
    public static void main(String[] args) throws Exception {
        Constants.baseHttpApiUrl = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1";
        Constants.baseWebsocketApiUrl = "wss://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference";
        Map<String, Object> userContent = new HashMap<>();
        userContent.put("type", "input_text");
        userContent.put("text", "我在祺元项目工作，负责璇枢系统。我的同事叫洛柯。");
        Map<String, Object> user = new HashMap<>();
        user.put("role", "user");
        user.put("content", Arrays.asList(userContent));
        Map<String, Object> assistantContent = new HashMap<>();
        assistantContent.put("type", "text");
        assistantContent.put("text", "好的，我们继续讨论祺元项目、璇枢系统和洛柯的工作。");
        Map<String, Object> assistant = new HashMap<>();
        assistant.put("role", "assistant");
        assistant.put("content", Arrays.asList(assistantContent));
        Map<String, Object> input = new HashMap<>();
        input.put("context", Arrays.asList(user, assistant));
        RecognitionParam param = RecognitionParam.builder()
                .model("qwen-audio-3.1-asr-flash-streaming")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .format("wav").sampleRate(16000).input(input).build();
        Recognition recognizer = new Recognition();
        try {
            System.out.println(recognizer.call(param, new File("asr-accuracy-example.wav")));
        } finally {
            recognizer.getDuplexApi().close(1000, "bye");
        }
        System.exit(0);
    }
}
```

Python

```
import os
import time
import dashscope
from concurrent.futures import ThreadPoolExecutor

client = dashscope.Client(
    api_key=os.environ["DASHSCOPE_API_KEY"],
    workspace="{WorkspaceId}",
    region="cn-beijing",
)
context = [
    {
        "role": "user",
        "content": [
            {
                "type": "input_text",
                "text": "我在祺元项目工作，负责璇枢系统。我的同事叫洛柯。"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "好的，我们继续讨论祺元项目、璇枢系统和洛柯的工作。"
            }
        ]
    }
]

def receive_events(recognition):
    for event in recognition.events():
        sentence = ((event.get("payload") or {}).get("output") or {}).get("sentence") or {}
        if sentence.get("text") and not sentence.get("heartbeat"):
            print(sentence["text"])

with client.audio.asr.recognize(
    model="qwen-audio-3.1-asr-flash-streaming",
    format="wav", sample_rate=16000,
    input={"context": context},
) as recognition:
    with ThreadPoolExecutor(max_workers=1) as pool:
        receiver = pool.submit(receive_events, recognition)
        try:
            with open("asr-accuracy-example.wav", "rb") as audio:
                while True:
                    chunk = audio.read(3200)
                    if not chunk:
                        break
                    recognition.send_audio_frame(chunk)
                    time.sleep(0.1)
            recognition.stop()
            receiver.result()
        finally:
            recognition.close()
```

#### Qwen-Audio-ASR-Filetrans

以下示例使用 `qwen-audio-3.1-asr-flash-filetrans`，在 `input.file_urls` 中提供音频 URL，在 `input.context` 中提供上下文，然后异步提交任务、查询状态并下载结果。

```
import json
import os
import time
import urllib.request

base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/api/v1"
headers = {"Authorization": "Bearer " + os.environ["DASHSCOPE_API_KEY"]}

def request_json(url, body=None, extra_headers=None):
    request_headers = {**headers, **(extra_headers or {})}
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        request_headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=request_headers)
    with urllib.request.urlopen(req) as response:
        return json.load(response)

body = {
    "model": "qwen-audio-3.1-asr-flash-filetrans",
    "input": {
        "file_urls": [
            "https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/audios/6a4b3c2d1e0f9093.wav"
        ],
        "context": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "我在祺元项目工作，负责璇枢系统。我的同事叫洛柯。"
                    }
                ]
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": "好的，我们继续讨论祺元项目、璇枢系统和洛柯的工作。"
                    }
                ]
            }
        ]
    },
    "parameters": {}
}
task = request_json(
    base_url + "/services/audio/asr/transcription", body,
    {"X-DashScope-Async": "enable"},
)
task_id = task["output"]["task_id"]
while True:
    result = request_json(base_url + "/tasks/" + task_id)
    status = result["output"]["task_status"]
    if status == "SUCCEEDED":
        break
    if status in ("FAILED", "CANCELED"):
        raise RuntimeError(result)
    time.sleep(1)

for item in result["output"]["results"]:
    if item["subtask_status"] != "SUCCEEDED":
        raise RuntimeError(item)
    with urllib.request.urlopen(item["transcription_url"]) as response:
        transcription = json.load(response)
    for transcript in transcription["transcripts"]:
        print(transcript["text"])
```

移除示例中的上下文配置，再识别同一段音频，即可对比配置前后的结果。以下为识别文本示例：

**配置**

**识别文本示例**

未配置

请把漆园项目的报告发给罗科，下周我们要上线玄枢系统。

配置后

请把祺元项目的报告发给洛柯，下周我们要上线璇枢系统。

## 效果调优与排查

使用同一音频对比配置前后的结果，再调整词条、权重或上下文内容。热词调优同时适用于即时热词和预编译热词。

### 调整热词权重

普通热词的权重范围为 1～5，建议从 `weight=4` 起调。权重越高，模型越倾向于输出该词；权重过高可能把其他发音相近的词错误替换为热词。

**权重**

**偏好程度**

**适用情况**

1～2

较弱

与常用词发音相近，需要避免过度纠偏

3～4

较明显

推荐作为大多数场景的起始配置

5

较强

音频中频繁出现、较少与其他词混淆的术语

**超级热词**：Qwen-Audio-ASR-Message、Qwen-Audio-ASR-Streaming、Qwen-Audio-ASR-Filetrans 和 Qwen-Audio-ASR 系列的即时热词、预编译热词还支持 `weight=50`，可提高目标词召回率，每个词表或请求最多 50 个。

### 组织与维护词表

-   **按场景分组**：预编译热词可为不同业务场景创建独立列表，例如分别维护医疗术语和产品名称，减少无关词条。
    
-   **区分词条语种与音频语种**：预编译词表可混入不同语种的词条，通过 `lang` 区分。`language_hints` 属于识别接口，用于声明音频语种；设置后，仅语种匹配的热词生效，其他语种的热词被忽略。
    
-   **定期维护**：按业务需要更新词条，删除不再使用的列表以释放配额。
    

**说明**建议两次热词列表更新至少间隔 5 分钟，否则更新后的热词可能不生效。

### 排查识别效果

先区分是配置未生效、词语纠偏过强，还是音频本身难以识别，再检查相应项目。

**现象**

**检查与处理**

热词未按预期识别

先确认[支持的模型与地域](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#supported-models)。即时热词应位于 `parameters.vocabulary`；预编译热词需核对账号、`vocabulary_id`、`status=OK`，以及创建列表时的 `target_model` 是否与当前模型一致。

在支持范围内调大热词权重，并对比同一音频的结果，判断是否为权重偏低导致。

其他词被误识别为热词

在支持范围内调小热词权重，并按业务场景减少无关词条。检查 `lang` 与识别接口 `language_hints` 是否匹配，避免使用不属于当前语种的词条。

上下文没有改善目标词

检查文本是否包含术语的准确写法，并核对消息角色、类型、顺序和所用接口的传入位置。超过长度或轮数限制的文本可能被截断或丢弃，规则参见[使用限制](https://help.aliyun.com/zh/model-studio/improve-asr-accuracy#hw10_limit_h2)。

普通词也大量识别错误

检查音频格式、采样率是否符合模型要求，并降低背景噪声。单语种音频可通过识别接口的 `language_hints` 声明语种。模型选型与音频要求参见[语音识别概述](raw/model-user-guide/model-experience/speech-and-audio/speech-recognition/asr-model.md)。

## 支持的模型与地域

#### 预编译热词

#### 华北2（北京）

-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
    
-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
    
-   **Qwen-Audio-ASR-Filetrans**：qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
    
-   **Qwen-Audio-ASR**：qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
    
-   **Fun-ASR-Realtime**：fun-asr-realtime、fun-asr-realtime-2026-02-28、fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28
    
-   **Fun-ASR-Flash**：fun-asr-flash-2026-06-15
    
-   **Fun-ASR**：fun-asr
    
-   **Paraformer-Realtime**：paraformer-realtime-v2、paraformer-realtime-8k-v2
    
-   **Paraformer**：paraformer-v2、paraformer-8k-v2
    

#### 新加坡

**说明**新加坡地域的子业务空间暂不支持热词功能。

-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
    
-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
    
-   **Qwen-Audio-ASR-Filetrans**：qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
    
-   **Qwen-Audio-ASR**：qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
    
-   **Fun-ASR-Realtime**：fun-asr-realtime
    
-   **Fun-ASR-Flash**：fun-asr-flash-2026-06-15
    
-   **Fun-ASR**：fun-asr
    

#### 即时热词

#### 华北2（北京）

-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
    
-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
    
-   **Qwen-Audio-ASR-Filetrans**：qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
    
-   **Qwen-Audio-ASR**：qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
    
-   **Fun-ASR**：fun-asr
    

#### 新加坡

**说明**新加坡地域的子业务空间暂不支持热词功能。

-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
    
-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
    
-   **Qwen-Audio-ASR-Filetrans**：qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
    
-   **Qwen-Audio-ASR**：qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
    
-   **Fun-ASR**：fun-asr
    

#### 上下文增强

#### 华北2（北京）

-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
    
-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
    
-   **Qwen-Audio-ASR-Filetrans**：qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
    
-   **Qwen-Audio-ASR**：qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
    
-   **Fun-ASR-Realtime**：fun-asr-realtime
    
-   **Fun-ASR-Flash**：fun-asr-flash-2026-06-15
    

#### 新加坡

-   **Qwen-Audio-ASR-Message**：qwen-audio-3.1-asr-flash-message
    
-   **Qwen-Audio-ASR-Streaming**：qwen-audio-3.1-asr-flash-streaming、qwen-audio-3.0-asr-flash-streaming
    
-   **Qwen-Audio-ASR-Filetrans**：qwen-audio-3.1-asr-flash-filetrans、qwen-audio-3.0-asr-flash-filetrans
    
-   **Qwen-Audio-ASR**：qwen-audio-3.1-asr-flash、qwen-audio-3.0-asr-flash
    
-   **Fun-ASR-Realtime**：fun-asr-realtime
    
-   **Fun-ASR-Flash**：fun-asr-flash-2026-06-15
    

## 使用限制

#### 热词限制

**限制项**

**说明**

热词列表数量

每账号最多 50 个预编译热词列表，所有模型共享。每个列表对应一个 `vocabulary_id`。

热词数量

Qwen-Audio-ASR-Message、Qwen-Audio-ASR-Streaming、Qwen-Audio-ASR-Filetrans、Qwen-Audio-ASR 系列：最多 2000 个。

Fun-ASR-Realtime、Fun-ASR-Flash、Fun-ASR 系列主版本模型：最多 2000 个；上述系列的其他模型以及 Paraformer 系列：最多 500 个。

预编译热词按单个列表计数，即时热词按单次请求计数。

超级热词数量

权重为 50 的词条最多 50 个。

**说明**对于 Qwen-Audio-ASR-Message、Qwen-Audio-ASR-Streaming、Qwen-Audio-ASR-Filetrans 和 Qwen-Audio-ASR 系列模型，同时配置预编译热词和即时热词时，系统会合并两类热词；合并后超过 2000 个时，随机选择 2000 个使用。

#### 热词文本规范

热词须为实际词语，且语种在模型支持范围内；即时热词和预编译热词均遵循以下规范。

#### 包含非 ASCII 字符

包含汉字、日文假名、韩文谚文、西里尔字母等非 ASCII 字符时，与 ASCII 字符合计不超过 15 个字符，空格计入字符数。

**文本**

**计数**

**是否符合长度要求**

`"厄洛替尼盐酸盐"`

7 字符

是

`"EGFR抑制剂"`

7 字符

是

`"こんにちは"`

5 字符

是

`"Фенибут Белфарм"`

15 字符

是

`"Клофелин Белмедпрепараты"`

24 字符

否

#### 仅包含 ASCII 字符

仅包含 ASCII 字符时，按空格切分后不超过 7 个片段。

**文本**

**计数**

**是否符合长度要求**

`"Exothermic reaction"`

2 片段

是

`"Human immunodeficiency virus type 1"`

5 片段

是

`"The effect of temperature variations on enzyme activity in biochemical reactions"`

11 片段

否

#### 上下文限制

**限制项**

**说明**

上下文轮数

最多保留最近 5 轮；`input_text` 和 `text` 类型的上下文消息各最多 5 条，超出时忽略早期消息，不报错。仅传领域文本时也需遵循文本长度限制。

每轮文本长度

同一轮所有 `user` 和 `assistant` 消息的 `text` 字段长度之和不超过 400 个字符。字母、汉字、数字、空格和标点均各计 1 个字符。超出部分从末尾截断，不报错；各轮独立计算。

**说明**Qwen-Audio-ASR-Message 还支持在任务运行中通过 `continue-task` 更新上下文，格式参见[Message 客户端事件](https://help.aliyun.com/zh/model-studio/qwen-asr-message-client-events#h-continue-task)。

## 功能计费

即时热词和预编译热词功能本身免费。使用热词或上下文增强的模型调用费用，请参见[计费规则](raw/model-user-guide/test-1/model-pricing.md)。

## 相关 API

-   热词列表的创建、查询、更新和删除等操作，参见[热词管理 API](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words/vocabulary-http-api.md)。
    
-   热词管理 SDK：[Java SDK](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words/vocabulary-java-sdk.md)、[Python SDK](raw/model-api-reference/audio-api-references/speech-recognition-api-reference/custom-hot-words/vocabulary-python-sdk.md)。
    
-   模型调用 API：[Qwen-Audio-ASR-Message 客户端事件](raw/_short/qwen-asr-message-client-events-0be34a3639cdd40b.md)、[Qwen-Audio-ASR-Streaming 客户端事件](raw/_short/qwen-audio-asr-streaming-client-events-1bae8548d2be6bc5.md)、[Qwen-Audio-ASR-Filetrans HTTP API](raw/_short/qwen-audio-asr-filetrans-http-api-2ccf5d603a3ac5e9.md)、[Qwen-Audio-ASR HTTP API](raw/_short/qwen-audio-asr-http-api-b304ee1b83ae18cd.md)。
