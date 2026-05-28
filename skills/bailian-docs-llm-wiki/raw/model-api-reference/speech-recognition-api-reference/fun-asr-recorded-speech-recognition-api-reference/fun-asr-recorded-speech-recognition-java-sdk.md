# Fun-ASR录音文件识别Java SDK

本文介绍Fun-ASR录音文件识别Java SDK的参数和接口细节。

**用户指南：**关于模型介绍和选型建议请参见[录音文件识别-Fun-ASR/Paraformer](https://help.aliyun.com/zh/model-studio/recording-file-recognition)。

## **前提条件**

-   已开通服务并[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。请[配置API Key到环境变量](https://help.aliyun.com/zh/model-studio/configure-api-key-through-environment-variables)，而非硬编码在代码中，防范因代码泄露导致的安全风险。
    
    **说明**
    
    当您需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时鉴权Token](https://help.aliyun.com/zh/model-studio/generate-temporary-api-key)。
    
    与长期有效的 API Key 相比，临时鉴权 Token 具备时效性短（60秒）、安全性高的特点，适用于临时调用场景，能有效降低API Key泄露的风险。
    
    使用方式：在代码中，将原本用于鉴权的 API Key 替换为获取到的临时鉴权 Token 即可。
    
-   [安装最新版DashScope SDK](https://help.aliyun.com/zh/model-studio/install-sdk)。
    

## **模型列表**

参见[支持的模型](https://help.aliyun.com/zh/model-studio/recording-file-recognition#a6ddaaf4b308q)。

## **约束**

服务**不支持本地音视频文件直传（也不支持base64格式音频）**，输入源需为**可通过公网访问的文件URL**（支持HTTP/HTTPS协议，示例：`https://your-domain.com/file.mp3`）。

使用SDK时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，不支持使用以 `oss://`为前缀的临时 URL。

使用RESTful API时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，支持使用以 `oss://`为前缀的临时 URL：

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    

URL通过`fileUrls`参数指定，单次请求最多支持100个URL。

-   **音频格式**
    
    `aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`
    
    **重要**
    
    由于音视频格式及其变种众多，技术上无法穷尽测试，API不能保证所有格式均能够被正确识别。请通过测试验证您所提供的文件能够获得正常的语音识别结果。
    
-   **音频采样率：**任意
    
-   **音频文件大小和时长**
    
    音频文件不超过2GB；时长在12小时以内。如果启用说话人分离功能，建议音频时长不超过2小时。
    
    如果希望处理的文件超过了上述限制，可尝试对文件进行预处理以降低文件尺寸。有关文件预处理的最佳实践可以查阅[预处理视频文件以提高文件转写效率（针对录音文件识别场景）](https://help.aliyun.com/zh/model-studio/paraformer-best-practices#c5dda0a0cf2x9)。
    
-   **批处理音频数目**
    
    单次请求最多支持100个文件URL。
    
-   **可识别语言：**fun-asr 支持中文、英文；fun-asr-mtl-2025-08-25 支持中文， 粤语、英文、日语、 泰语、 越南语、印尼语。
    

## **快速开始**

[核心类（Transcription）](#adcb5e9bddbyq)提供了异步提交任务、同步等待任务结束和异步查询任务执行结果的接口。可通过如下两种调用方式进行录音文件识别：

-   异步提交任务+同步等待任务结束：提交任务后，阻塞当前线程直到任务结束并获取识别结果。
    
-   异步提交任务+异步查询任务执行结果：提交任务后，在需要的时候通过调用查询任务接口获取任务的执行结果。
    

### **异步提交任务+同步等待任务结束**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8169758771/CAEQURiBgMCO2_fRpxkiIDBlNzI4YmMyNTU3ODRlM2Y4NjUxZWU4YmUxNjliMmFl4709861_20241015153444.149.svg)

1.  配置[请求参数](#48ea212b1d08r)。
    
2.  实例化[核心类（Transcription）](#adcb5e9bddbyq)。
    
3.  调用[核心类（Transcription）](#adcb5e9bddbyq)的`asyncCall`方法异步提交任务。
    
    **说明**
    
    -   文件转写服务对通过API提交的任务采取尽力服务原则进行处理。任务提交后将进入排队（`PENDING`）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内。任务开始处理后，语音识别将以数百倍加速完成。
        
    -   每一个任务完成后，识别结果和URL下载链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。
        
    
4.  调用[核心类（Transcription）](#adcb5e9bddbyq)的`wait`方法同步等待任务结束。
    
    任务的状态包括`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`。当任务处于`PENDING`或`RUNNING`状态时，`wait`接口将被阻塞。当任务处于`SUCCEEDED`或`FAILED`状态时，`wait`接口不再阻塞并返回任务的执行结果。
    
    `wait`返回[任务执行结果（TranscriptionResult）](#11a082e1d9ijq)。
    

点击查看完整示例

```
import com.alibaba.dashscope.audio.asr.transcription.*;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.*;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        // 创建转写请求参数
        TranscriptionParam param =
                TranscriptionParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        //.apiKey("apikey")
                        .model("fun-asr") // 此处以fun-asr为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                        .fileUrls(
                                Arrays.asList(
                                        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                                        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"))
                        .build();
        try {
            Transcription transcription = new Transcription();
            // 提交转写请求
            TranscriptionResult result = transcription.asyncCall(param);
            System.out.println("RequestId: " + result.getRequestId());
            // 阻塞等待任务完成并获取结果
            result = transcription.wait(
                    TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
            // 打印结果
            System.out.println(new GsonBuilder().setPrettyPrinting().create().toJson(result.getOutput()));
        } catch (Exception e) {
            System.out.println("error: " + e);
        }
        System.exit(0);
    }
}
```

### **异步提交任务+异步查询任务执行结果**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8169758771/CAEQURiBgIDnxvjRpxkiIGI1NjJjOTgyNTVhMTRiMjM4OWVjYzFmZTExNGZjYzE14709861_20241015153444.149.svg)

1.  配置[请求参数](#48ea212b1d08r)。
    
2.  实例化[核心类（Transcription）](#adcb5e9bddbyq)。
    
3.  调用[核心类（Transcription）](#adcb5e9bddbyq)的`asyncCall`方法异步提交任务。
    
    **说明**
    
    -   文件转写服务对通过API提交的任务采取尽力服务原则进行处理。任务提交后将进入排队（`PENDING`）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内。任务开始处理后，语音识别将以数百倍加速完成。
        
    -   每一个任务完成后，识别结果和URL下载链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。
        
    
4.  循环调用[核心类（Transcription）](#adcb5e9bddbyq)的`fetch`方法直到获取最终的任务结果。
    
    当任务状态为`SUCCEEDED`或`FAILED`时，停止轮询并处理结果。
    
    `fetch`返回[任务执行结果（TranscriptionResult）](#11a082e1d9ijq)。
    

点击查看完整示例

```
import com.alibaba.dashscope.audio.asr.transcription.*;
import com.alibaba.dashscope.common.TaskStatus;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.*;

import java.util.Arrays;

public class Main {
    public static void main(String[] args) {
        // 以下为北京地域url，若使用新加坡地域的模型，需将url替换为：https://dashscope-intl.aliyuncs.com/api/v1
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        // 创建转写请求参数
        TranscriptionParam param =
                TranscriptionParam.builder()
                        // 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
                        // 若没有配置环境变量，请用百炼API Key将下行替换为：.apiKey("sk-xxx")
                        //.apiKey("apikey")
                        .model("fun-asr") // 此处以fun-asr为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/models
                        .fileUrls(
                                Arrays.asList(
                                        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                                        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"))
                        .build();
        try {
            Transcription transcription = new Transcription();
            // 提交转写请求
            TranscriptionResult result = transcription.asyncCall(param);
            System.out.println("RequestId: " + result.getRequestId());
            // 循环获取任务执行结果，直到任务结束
            while (true) {
                result = transcription.fetch(TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
                if (result.getTaskStatus() == TaskStatus.SUCCEEDED || result.getTaskStatus() == TaskStatus.FAILED) {
                    break;
                }
                Thread.sleep(1000);
            }
            // 打印结果
            System.out.println(new GsonBuilder().setPrettyPrinting().create().toJson(result.getOutput()));
        } catch (Exception e) {
            System.out.println("error: " + e);
        }
        System.exit(0);
    }
}
```

## **请求参数**

请求参数通过`TranscriptionParam`的链式方法进行配置。

点击查看示例

```
TranscriptionParam param = TranscriptionParam.builder()
  .model("fun-asr")
  .fileUrls(
          Arrays.asList(
                  "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                  "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"))
  .build();
```

**参数**

**类型**

**默认值**

**是否必须**

**说明**

model

String

\-

是

指定用于音视频文件转写的模型名。参见[模型列表](#47e6ae42d1u1b)。

fileUrls

List<String>

\-

是

音视频文件转写的URL列表，支持HTTP / HTTPS协议，单次请求最多支持100个URL。

若录音文件存储在阿里云OSS，使用SDK方式不支持使用以 oss://为前缀的临时 URL。

vocabularyId

String

\-

否

热词ID，此次语音识别中生效此热词ID对应的热词信息。默认不启用。使用方法请参考[定制热词](https://help.aliyun.com/zh/model-studio/custom-hot-words/)。

channelId

List<Integer>

\[0\]

否

指定在多音轨音频文件中需要识别的音轨索引，索引从 0 开始。例如，\[0\] 表示识别第一个音轨，\[0, 1\] 表示同时识别第一和第二个音轨。如果省略此参数，则默认处理第一个音轨。

**重要**

指定的每一个音轨都将独立计费。例如，为单个文件请求 \[0, 1\] 会产生两笔独立的费用。

specialWordFilter

String

\-

否

指定在语音识别过程中需要处理的敏感词，并支持对不同敏感词设置不同的处理方式。

若未传入该参数，系统将启用系统内置的敏感词过滤逻辑，识别结果中与[阿里云百炼敏感词表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)匹配的词语将被替换为等长的`*`。

若传入该参数，则可实现以下敏感词处理策略：

-   替换为 `*`：将匹配的敏感词替换为等长的 `*`；
    
-   直接过滤：将匹配的敏感词从识别结果中完全移除。
    

该参数的值应为一个 JSON 字符串，其结构如下所示：

```
{
  "filter_with_signed": {
    "word_list": ["测试"]
  },
  "filter_with_empty": {
    "word_list": ["开始", "发生"]
  },
  "system_reserved_filter": true
}
```

JSON字段说明：

-   `filter_with_signed`
    
    -   类型：对象。
        
    -   是否必填：否。
        
    -   描述：配置需替换为`*`的敏感词列表。识别结果中匹配的词语将被等长的 `*` 替代。
        
    -   示例：以上述JSON为例，“帮我测试一下这段代码”的语音识别结果将会是“帮我\*\*一下这段代码”。
        
    -   内部字段：
        
        -   `word_list`: 字符串数组，列出需被替换的敏感词。
            
-   `filter_with_empty`
    
    -   类型：对象。
        
    -   是否必填：否。
        
    -   描述：配置需从识别结果中移除（过滤）的敏感词列表。识别结果中匹配的词语将被完全删除。
        
    -   示例：以上述JSON为例，“比赛这就要开始了吗？”的语音识别结果将会是“比赛这就要了吗”。
        
    -   内部字段：
        
        -   `word_list`: 字符串数组，列出需被完全移除（过滤）的敏感词。
            
-   `system_reserved_filter`
    
    -   类型：布尔值。
        
    -   是否必填：否。
        
    -   默认值：true。
        
    -   描述：是否启用系统预置的敏感词规则。设为`true`时，将同时启用系统内置的敏感词过滤逻辑，识别结果中与[阿里云百炼敏感词表](https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/%E7%99%BE%E7%82%BC%E6%95%8F%E6%84%9F%E8%AF%8D%E5%88%97%E8%A1%A8_20230716.words.txt)匹配的词语将被替换为等长的`*`。
        

diarizationEnabled

Boolean

false

否

自动说话人分离，默认关闭。

仅适用于单声道音频，多声道音频不支持说话人分离。

启用该功能后，识别结果中将显示`speaker_id`字段，用于区分不同说话人。

**说明**

如果启用说话人分离功能，建议音频时长不超过2小时，否则可能导致识别失败或超时。

有关`speaker_id`的示例，请参见[识别结果说明](#a9021178ccl7s)。

speakerCount

Integer

\-

否

说话人数量参考值。取值范围为2至100的整数（包含2和100）。

开启说话人分离功能后（`diarizationEnabled`设置为true）生效。

默认自动判断说话人数量，如果配置此项，只能辅助算法尽量输出指定人数，无法保证一定会输出此人数。

language\_hints

String\[\]

\-

否

设置待识别语言代码。如果无法提前确定语种，可不设置，模型会自动识别语种。

系统仅读取数组中的首个值。多余值将被忽略。

不同模型支持的语言代码如下：

-   fun-asr、fun-asr-2025-11-07、fun-asr-mtl、fun-asr-mtl-2025-08-25：
    
    -   zh: 中文
        
    -   en: 英文
        
    -   ja: 日语
        
    -   ko：韩语
        
    -   vi：越南语
        
    -   th：泰语
        
    -   id：印尼语
        
    -   ms：马来语
        
    -   tl：菲律宾语
        
    -   hi：印地语
        
    -   ar：阿拉伯语
        
    -   fr：法语
        
    -   de：德语
        
    -   es：西班牙语
        
    -   pt：葡萄牙语
        
    -   ru：俄语
        
    -   it：意大利语
        
    -   nl：荷兰语
        
    -   sv：瑞典语
        
    -   da：丹麦语
        
    -   fi：芬兰语
        
    -   no：挪威语
        
    -   el：希腊语
        
    -   pl：波兰语
        
    -   cs：捷克语
        
    -   hu：匈牙利语
        
    -   ro：罗马尼亚语
        
    -   bg：保加利亚语
        
    -   hr：克罗地亚语
        
    -   sk：斯洛伐克语
        
-   fun-asr-2025-08-25：
    
    -   zh: 中文
        
    -   en: 英文
        

**说明**

`language_hints`需要通过`TranscriptionParam`实例的`parameter`方法或者`parameters`方法进行设置：

## 通过parameter设置

```
TranscriptionParam param = TranscriptionParam.builder()
  .model("fun-asr")
  .parameter("language_hints", new String[]{"zh"})
  .build();
```

## 通过parameters设置

```
TranscriptionParam param = TranscriptionParam.builder()
  .model("fun-asr")
  .parameters(Collections.singletonMap("language_hints", new String[]{"zh"}))
  .build();
```

apiKey

String

\-

否

用户API Key。如已将API Key配置到环境变量，则无须在代码中设置。否则一定要在代码中进行设置。

## **响应结果**

### 任务执行结果（`TranscriptionResult`）

`TranscriptionResult`封装了当前任务执行结果。

**接口/方法**

**参数**

**返回值**

**描述**

```
public String getRequestId()
```

无

requestId

获取requestId。

```
public String getTaskId()
```

无

taskId

获取taskId。

```
public TaskStatus getTaskStatus()
```

无

`TaskStatus`，任务状态

获取任务状态。

`TaskStatus`为枚举类，只需关注`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四个状态即可。

**说明**

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

```
public List<TranscriptionTaskResult> getResults()
```

无

[子任务执行结果（TranscriptionTaskResult）](#86b568aa3asuj)

获取[子任务执行结果（TranscriptionTaskResult）](#86b568aa3asuj)。

每个任务对一个或多个音频文件进行识别，不同音频文件在不同的子任务中处理，因此每个任务对应一到多个子任务。

```
public JsonObject getOutput()
```

无

任务执行结果，为JSON格式的数据

获取任务执行结果。

该结果是一个JSON格式的数据，如果您想通过`getOutput`接口获取任务执行结果，请您在获取结果后自行解析。

**点击查看JSON示例**

**正常示例**

```
{
    "task_id":"0795ff8c-b666-4e91-bb8b-xxx",
    "task_status":"SUCCEEDED",
    "submit_time":"2025-02-13 16:12:09.109",
    "scheduled_time":"2025-02-13 16:12:09.128",
    "end_time":"2025-02-13 16:12:10.189",
    "results":[
        {
            "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav",
            "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20250213/16%3A12/34604a7b-579a-4223-8797-5116a49b07ec-1.json?Expires=1739520730&OSSAccessKeyId=yourOSSAccessKeyId&Signature=tMqyH56oB5rDW9%2FFqD8Yo%2F3WaPk%3D",
            "subtask_status":"SUCCEEDED"
        },
        {
            "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
            "transcription_url":"https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20250213/16%3A12/3baafe5f-d09d-46c6-8b01-724927670edb-1.json?Expires=1739520730&OSSAccessKeyId=yourOSSAccessKeyId&Signature=BF7vPxlsJN9hkJlY%2BLReezxOwK8%3D",
            "subtask_status":"SUCCEEDED"
        }
    ],
    "task_metrics":{
        "TOTAL":2,
        "SUCCEEDED":2,
        "FAILED":0
    }
}
```

**异常示例**

“`code`”为错误码，“`message`”为错误信息，只有异常情况才有这两个字段，您可以通过这两个字段，对照[错误码](#a370386972oa4)排查问题。

```
{
    "task_id": "7bac899c-06ec-4a79-8875-xxxxxxxxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2024-12-16 16:30:59.170",
    "scheduled_time": "2024-12-16 16:30:59.204",
    "end_time": "2024-12-16 16:31:02.375",
    "results": [
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3",
            "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20241216/xxxx",
            "subtask_status": "SUCCEEDED"
        },
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_exaple_1.wav",
            "code": "InvalidFile.DownloadFailed",
            "message": "The audio file cannot be downloaded.",
            "subtask_status": "FAILED"
        }
    ],
    "task_metrics": {
        "TOTAL": 2,
        "SUCCEEDED": 1,
        "FAILED": 1
    }
}
```

### 子任务执行结果（`TranscriptionTaskResult`）

`TranscriptionTaskResult`封装了子任务执行结果。子任务对单个音频文件进行识别。

**接口/方法**

**参数**

**返回值**

**描述**

```
public String getFileUrl()
```

无

被识别的音频文件的链接

获取被识别音频文件的链接。

```
public String getTranscriptionUrl()
```

无

识别结果对应的链接

获取识别结果对应的链接。该链接有效期为24小时，超时后无法查询任务或通过先前查询结果中的URL下载结果。

识别结果保存为JSON文件，您可以通过上述链接下载该文件或直接通过HTTP请求读取该文件中的内容。

JSON数据中各字段含义请参见[识别结果说明](#a9021178ccl7s)。

```
public TaskStatus getSubTaskStatus()
```

无

`TaskStatus`，子任务状态

获取子任务状态。

`TaskStatus`为枚举类，只需关注`PENDING`、`RUNNING`、`SUCCEEDED`和`FAILED`这四个状态即可。

```
public String getMessage()
```

无

任务执行过程中关键信息，可能为空

获取任务执行过程中的关键信息。

当任务失败时，可查看该内容分析原因。

### 识别结果说明

识别结果保存为JSON文件。

点击查看识别结果示例

```
{
    "file_url":"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
    "properties":{
        "audio_format":"pcm_s16le",
        "channels":[
            0
        ],
        "original_sampling_rate":16000,
        "original_duration_in_milliseconds":3834
    },
    "transcripts":[
        {
            "channel_id":0,
            "content_duration_in_milliseconds":3720,
            "text":"Hello world, 这里是阿里巴巴语音实验室。",
            "sentences":[
                {
                    "begin_time":100,
                    "end_time":3820,
                    "text":"Hello world, 这里是阿里巴巴语音实验室。",
                    "sentence_id":1,
                    "speaker_id":0, //当开启自动说话人分离功能时才会显示该字段
                    "words":[
                        {
                            "begin_time":100,
                            "end_time":596,
                            "text":"Hello ",
                            "punctuation":""
                        },
                        {
                            "begin_time":596,
                            "end_time":844,
                            "text":"world",
                            "punctuation":", "
                        }
                        // 这里省略其它内容
                    ]
                }
            ]
        }
    ]
}
```

需要关注的参数如下：

**参数**

**类型**

**说明**

audio\_format

string

源文件中音频的格式。

channels

array\[integer\]

源文件中音频的音轨索引信息，对单轨音频返回\[0\]，对双轨音频返回\[0, 1\]，以此类推。

original\_sampling\_rate

integer

源文件中音频的采样率（Hz）。

original\_duration\_in\_milliseconds

integer

源文件中的原始音频时长（ms）。

channel\_id

integer

转写结果的音轨索引，以0为起始。

content\_duration

integer

音轨中被判定为语音内容的时长（ms）。

**重要**

语音识别模型服务仅对音轨中被判定为语音内容的时长进行语音转写，并据此进行计量计费，非语音内容不计量、不计费。通常情况下语音内容时长会短于原始音频时长。由于对是否存在语音内容的判定是由AI模型给出的，可能与实际情况存在一定误差。

transcript

string

段落级别的语音转写结果。

sentences

array

句子级别的语音转写结果。

words

array

词级别的语音转写结果。

begin\_time

integer

开始时间戳（ms）。

end\_time

integer

结束时间戳（ms）。

text

string

语音转写结果。

speaker\_id

integer

当前说话人的索引，以0为起始，用于区分不同的说话人。

仅在启用说话人分离功能时，该字段才会显示于识别结果中。

punctuation

string

预测出的词之后的标点符号（如有）。

## **关键接口**

### **任务查询参数配置类（**`TranscriptionQueryParam`）

`TranscriptionQueryParam`在等待任务完成（调用`Transcription`的`wait`方法）或查询任务执行结果（调用`Transcription`的`fetch`方法）时用到。

通过静态方法`FromTranscriptionParam`创建`TranscriptionQueryParam`实例。

**点击查看示例**

```
// 创建转写请求参数
TranscriptionParam param =
        TranscriptionParam.builder()
                // 若没有将API Key配置到环境变量中，需将apiKey替换为自己的API Key
                //.apiKey("apikey")
                .model("fun-asr")
                .fileUrls(
                        Arrays.asList(
                                "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
                                "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"))
                .build();
try {
    Transcription transcription = new Transcription();
    // 提交转写请求
    TranscriptionResult result = transcription.asyncCall(param);
    System.out.println("RequestId: " + result.getRequestId());
    TranscriptionQueryParam queryParam = TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId());
    
} catch (Exception e) {
    System.out.println("error: " + e);
}
```

**接口/方法**

**参数**

**返回值**

**描述**

```
public static TranscriptionQueryParam FromTranscriptionParam(TranscriptionParam param, String taskId)
```

-   `param`：`TranscriptionParam`实例
    
-   `taskId`：任务ID
    

`TranscriptionQueryParam`实例

创建`TranscriptionQueryParam`实例。

### 核心类（`**Transcription**`**）**

`Transcription`可以通过“`import com.alibaba.dashscope.audio.asr.transcription.*;`”方式引入。它的关键接口如下：

**接口/方法**

**参数**

**返回值**

**描述**

```
public TranscriptionResult asyncCall(TranscriptionParam param)
```

`param`：语音识别相关参数，`TranscriptionParam`实例

[任务执行结果（TranscriptionResult）](#11a082e1d9ijq)

异步提交语音识别任务。

```
public TranscriptionResult wait(TranscriptionQueryParam queryParam)
```

`queryParam`：`TranscriptionQueryParam`实例

[任务执行结果（TranscriptionResult）](#11a082e1d9ijq)

阻塞当前线程直到异步任务结束（任务状态为`SUCCEEDED`或`FAILED`）。

```
public TranscriptionResult fetch(TranscriptionQueryParam queryParam)
```

`queryParam`：`TranscriptionQueryParam`实例

[任务执行结果（TranscriptionResult）](#11a082e1d9ijq)

异步查询当前任务执行结果。

## **其他接口：批量查询任务状态/取消任务**

详情请参见[管理异步任务](https://help.aliyun.com/zh/model-studio/manage-asynchronous-tasks)：支持批量查询24小时内提交的录音文件识别任务，同时支持取消`PENDING`（排队）状态的任务。

## **错误码**

如遇报错问题，请参见[错误信息](https://help.aliyun.com/zh/model-studio/error-code)进行排查。

当任务包含多个子任务时，只要存在任一子任务成功，整个任务状态将标记为`SUCCEEDED`，需通过`subtask_status`字段判断具体子任务结果。

错误返回示例：

```
{
    "task_id": "7bac899c-06ec-4a79-8875-xxxxxxxxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2024-12-16 16:30:59.170",
    "scheduled_time": "2024-12-16 16:30:59.204",
    "end_time": "2024-12-16 16:31:02.375",
    "results": [
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/long_audio_demo_cn.mp3",
            "transcription_url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/prod/paraformer-v2/20241216/xxxx",
            "subtask_status": "SUCCEEDED"
        },
        {
            "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_exaple_1.wav",
            "code": "InvalidFile.DownloadFailed",
            "message": "The audio file cannot be downloaded.",
            "subtask_status": "FAILED"
        }
    ],
    "task_metrics": {
        "TOTAL": 2,
        "SUCCEEDED": 1,
        "FAILED": 1
    }
}
```

## **常见问题**

### **功能特性**

#### **Q：是否支持Base64编码方式的音频？**

不支持Base64编码方式的音频。仅支持可通过公网访问的 URL 所指向的音频的识别，不支持识别二进制流，也不支持直接识别本地文件。

#### **Q：如何将音频文件以公网可访问的URL形式提供？**

通常遵循以下几个步骤（这里为您提供一种思路，具体情况因不同存储产品而异，推荐将音频[上传至阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)）：

1、选择存储和托管方式

如以下这几种：

-   对象存储服务（推荐）：
    
    -   使用云服务商的对象存储服务（如[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)），将音频文件上传到存储桶中，并设置为公开访问。
        
    -   优点：高可用性、支持 CDN 加速、易于管理。
        
-   Web 服务器：
    
    -   将音频文件放置在支持 HTTP/HTTPS 访问的 Web 服务器上（如 Nginx、Apache）。
        
    -   优点：适合小型项目或本地测试。
        
-   内容分发网络（CDN）：
    
    -   将音频文件托管在 CDN 上，通过 CDN 提供的 URL 访问。
        
    -   优点：加速文件传输，适合高并发场景。
        

2、上传音频文件

根据选择的存储/托管方式，将音频上传，如：

-   对象存储服务：
    
    -   登录云服务商的控制台，创建存储桶。
        
    -   上传音频文件，并设置文件权限为“公共读”或生成临时访问链接。
        
-   Web 服务器：
    
    -   将音频文件放置在服务器指定目录下（如 `/var/www/html/audio/`）。
        
    -   确保文件可以通过 HTTP/HTTPS 访问。
        

3、生成公网可访问的URL

例如：

-   对象存储服务：
    
    -   文件上传后，系统会自动生成一个公网访问 URL（通常格式为 `https://<bucket-name>.<region>.aliyuncs.com/<file-name>`）。
        
    -   如果需要更友好的域名，可以绑定自定义域名并开启 HTTPS。
        
-   Web 服务器：
    
    -   文件的访问 URL 通常是服务器地址加上文件路径（如 `https://your-domain.com/audio/file.mp3`）。
        
-   CDN：
    
    -   配置 CDN 加速后，使用 CDN 提供的 URL（如 `https://cdn.your-domain.com/audio/file.mp3`）。
        

4、验证URL的可用性

公网环境下，确保生成的 URL 可以正常访问，例如：

-   在浏览器中打开 URL，检查是否能播放音频文件。
    
-   使用工具（如 `curl` 或 Postman）验证 URL 是否返回正确的 HTTP 响应（状态码 200）。
    

使用SDK时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，不支持使用以 `oss://`为前缀的临时 URL。

使用RESTful API时，若录音文件存储在[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，支持使用以 `oss://`为前缀的临时 URL：

**重要**

-   临时 URL 有效期48小时，过期后无法使用，**请勿用于生产环境。**
    
-   文件上传凭证接口限流为 100 QPS 且不支持扩容，**请勿用于生产环境、高并发及压测场景。**
    
-   生产环境建议使用[阿里云OSS](https://help.aliyun.com/zh/oss/user-guide/what-is-oss) 等稳定存储，确保文件长期可用并规避限流问题。
    

#### **Q：多久能获取识别结果？**

任务提交后将进入排队（PENDING）状态，排队时间取决于队列长度和文件时长，无法明确给出，通常在数分钟内，请耐心等待。并且音频时长越长，所需时间越久。

### **故障排查**

如遇代码报错问题，请根据[错误码](#a370386972oa4)中的信息进行排查。

#### **Q：一直轮询不到结果？**

可能是限流原因，请耐心等待。

#### **Q：无法识别语音（无识别结果）是什么原因？**

请检查音频格式和采样率是否正确且符合参数约束。

可以使用[ffprobe](https://ffmpeg.org/ffprobe.html)工具获取音频的容器、编码、采样率、声道等信息：

```
ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
```
