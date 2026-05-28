# 快速集成智能纪要Agent

在多模应用中快速集成离线智能纪要Agent。

## **前提条件**

您已开通通义听悟-智能纪要后付费服务，并已发布一个智能纪要应用，您可以访问[通义听悟-智能纪要控制台](https://bailian.console.aliyun.com/?tab=app#/app/app-market/tingwu/tingwu-meeting-summary)查看您的应用。

## **在多模应用中配置智能纪要Agent**

1.  在 应用配置 - Agent - 百炼应用 - 添加 - 推荐应用 中找到智能纪要并勾选，并确保本应用已开启意图识别功能。
    
2.  点击智能纪要右侧的设置按钮，进入配置应用。
    
3.  在“选择通义听悟应用”处选择一个您已发布的智能纪要应用。
    
4.  您可以对离线录音总结设置进行修改，各配置项的含义如下：
    
    1.  启动指令：配置启动离线转写的个性化指令，如开启离线纪要等，该指令可以在控台体验。注意，由于多模应用本来已有录音技能，为避免录音技能和离线智能纪要Agent的启动指令的意图识别模糊，首选方案是关闭录音技能，仅集成离线智能纪要Agent；次选方案是将启动指令的相应语料在内容上加以区分，比如配置为“开启离线纪要”。
        
    2.  退出指令：退出离线转写的个性化指令，由于依赖sdk进行端侧录音状态更新，无法在控台体验。
        
    3.  暂停指令：暂停离线转写的个性化指令，由于依赖sdk进行端侧录音状态更新，无法在控台体验。
        
    4.  恢复指令：恢复离线转写的个性化指令，由于依赖sdk进行端侧录音状态更新，无法在控台体验。
        
5.  点击确定，保存并发布应用。您也可以在控制台页面通过语音指令测试实时转写能力。
    

在百炼控制台侧完成如上的智能纪要应用绑定和指令录入后，可以开始下面的集成流程。

## **集成整体流程**

用户在配置好智能纪要Agent的多模应用中，可以利用SDK来体验如下流程，示例代码参见：[完整流程示例代码](#d34d1fb9bdhuu)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7376314671/p1023968.png)

上面流程图中主要包含了用户在多模应用中集成智能纪要涉及到的5条指令，其对应的功能和支持的用户语音输入槽位如下：

指令名称

指令效果

支持槽位

开启录音

开启录音的标识，成功识别后返回`start_local_recording`指令。

支持翻译和发言人分离个数的槽位，例如：开启录音翻译成英文并且按照3人发言来进行总结。

翻译参数和发言人分离个数参数含义可以分别参考：

-   [parameters.transcription.translationTargetLang](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-create-task#f7758cd2fagt7)
    
-   [parameters.transcription.diarizationSpeakerCount](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-create-task#f7758cd2fagt7)
    

暂停录音

暂停录音的标识，成功识别后返回`pause_local_recording`。

无

恢复录音

恢复录音的标识，成功识别后返回`resume_local_recording`。

无

结束录音

结束录音的标识，成功识别后返回`end_local_recording`指令。

支持翻译和发言人分离个数的槽位，若与开启录音有相同槽位则覆盖开启录音的槽位信息。

结束录音执行结果

在结束录音后，用户会将录音文件的ossUrl上传，然后多模应用会根据该url执行智能纪要的离线转写任务，任务的创建返回会在`end_local_recording_execution_res`指令中进行返回。

无

注意，强烈建议在[Start](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#5b2363d40585y)消息中传入：`parameters.client_info.device.uuid`，用来区分同一个多模应用下不同的硬件设备，否则同一个多模应用下多个硬件设备提取的槽位将无法区分，带来使用体验问题。

## **集成协议**

### **用户端侧状态设计**

为了提升用户体验，我们设计了端侧本地的录音状态管理的状态机，该状态需要用户端侧进行维护，然后收到不同的指令更新端侧本地的录音状态。

-   端的状态定义：未开始（初始状态）、录音中、暂停中
    
-   端能够发送的指令定义：启动录音，暂停录音，恢复录音，结束录音，被允许的状态在4种指令中发生切换
    

端侧状态

状态编码

状态转换

未开始

0

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6583970771/CAEQYxiBgMDdy5.U0RkiIDk1MzIxNzBlNmE3ZTQ3MjNiODE0M2I2MGQzYzU1ZWM25830155_20251027173629.760.svg)

录音中

1

暂停中

2

该状态维护在：多模态交互的`user_defined_params.tingwu_meeting.clientRecordingStatus`中，可以通过以下两种方式设置这个状态：

-   [Start消息](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#5b2363d40585y)
    
-   [客户端更新事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#39b223a2f6y9y)
    

名称

类型

是否必填

说明

clientRecordingStatus

string

否

端侧录音状态，参考：[用户端侧状态设计](#ae6eeb3687yv4)，不填时默认为"0"

### **开启录音触发**

多模对话中输入当时用户自己配置的开启录音短语即可触发。

触发后将会在多模的[文本下发事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#3b421d978fco5)收到的开启录音指令，在该事件payload里的`output.extra_info.commands`字段里，以json格式字符串返回相关指令，示例如下：

```
{
  "output": {
    "extra_info": {
      "commands": "[{\"intent_info\":{\"domain\":\"tingwu_meeting\",\"intent\":\"audio_recording\"},\"command_request_id\":\"multi_modal_meeting_slots#llm-***-mm_***-shanglu-123456#***#84178828aab44509\",\"name\":\"start_local_recording\"}]"
    }
  }
}
```

commands是一个jsonArray的字符串，这个字符串反序列化后，关注到该指令列表中的指令的name字段为`start_local_recording`则表示开启录音成功。

```
[
  {
    "command_request_id": "multi_modal_meeting_slots#llm-***-mm_***-shanglu-123456#***#84178828aab44509",
    "name": "start_local_recording"
  }
]
```

若要复用该ws链接，则需要调用[客户端更新事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#39b223a2f6y9y)来更新端侧的录音状态，将`user_defined_params.tingwu_meeting.clientRecordingStatus`更新为`1`，即表示端侧录音状态为录音中。

### **暂停录音触发**

多模对话中输入当时用户自己配置的暂停录音短语即可触发，但需要注意该指令触发时`user_defined_params.tingwu_meeting.clientRecordingStatus`的值应该为`1`。

-   若是在新建的ws链接中，则可以在[Start消息](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#5b2363d40585y)中来设置`user_defined_params.tingwu_meeting.clientRecordingStatus`为`1`。
    
-   若是在某个已经存在的ws链接中，需要确保`user_defined_params.tingwu_meeting.clientRecordingStatus`为`1`，通过调用[客户端更新事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#39b223a2f6y9y)可以实现更新；
    

触发后将会在多模的[文本下发事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#3b421d978fco5)收到的暂停录音指令，在该事件`payload`里的`output.extra_info.commands`字段里，以json格式字符串返回相关指令，示例如下：

```
{
  "output": {
    "extra_info": {
      "commands": "[{\"intent_info\":{\"domain\":\"tingwu_meeting\",\"intent\":\"pause_audio_recording\"},\"name\":\"pause_local_recording\"}]"
    }
  }
}
```

将commands是一个jsonArray的字符串，这个字符串反序列化后，关注到该指令列表中的指令的name字段为`pause_local_recording`则表示暂停录音成功。

若要复用该ws链接，则需要调用[客户端更新事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#39b223a2f6y9y)来更新端侧的录音状态，将`user_defined_params.tingwu_meeting.clientRecordingStatus`更新为`2`，即表示端侧录音状态为暂停中。

### **恢复录音触发**

多模对话中输入当时用户自己配置的恢复录音短语即可触发，同时注意触发该指令时，`user_defined_params.tingwu_meeting.clientRecordingStatus`的值应该为`2`。

触发后将会在多模的[文本下发事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#3b421d978fco5)收到的恢复录音指令，同时注意指令列表中的指令的name字段为`resume_local_recording`则表示恢复录音指令。

若要复用该ws链接，则需要调用[客户端更新事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#39b223a2f6y9y)来更新端侧的录音状态，将`user_defined_params.tingwu_meeting.clientRecordingStatus`更新为`1`，即表示端侧录音状态为录音中。

### **结束录音触发**

多模对话中输入当时用户自己配置的结束录音短语即可触发，同时注意触发该指令时，`user_defined_params.tingwu_meeting.clientRecordingStatus`的值应该为`1 或者 2`。

触发后将会在多模的[文本下发事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#3b421d978fco5)收到的结束录音指令，`payloa.output.extra_info.commands`是一个jsonArray的字符串，注意指令列表中的指令的name字段为`end_local_recording`则表示收到结束录音指令，如下是`commands`返回的一个示例。

```
[
  {
    "intent_info": {
      "domain": "tingwu_meeting",
      "intent": "quit_audio_recording"
    },
    "command_request_id": "multi_modal_meeting_slots#llm-***-mm_***-shanglu-123456#***#84178828aab44509",
    "name": "end_local_recording"
  }
]
```

若要复用该ws链接，则需要调用[客户端更新事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#39b223a2f6y9y)来更新端侧的录音状态，将`user_defined_params.tingwu_meeting.clientRecordingStatus`更新为`0`，即表示端侧录音状态为录音中。

### **提交结束录音执行结果**

在[结束录音触发](#df0154d97cbs0)章节里：`commands`反序列化后，`end_local_recording`指令会返回一个`command_request_id`，该id是提交端侧录音文件的一个凭证。利用多模的[RequestToRespond指令](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#ea3b4279e717m)提交录音文件的ossUrl，提交协议如下：

名称

类型

说明

示例值

parameters.biz\_params.command\_results\[0\].command\_request\_id

string

结束录音指令返回的command\_request\_id

结束录音返回的`command_request_id`

parameters.biz\_params.command\_results\[0\].invoke\_result

String

用户提交的录音文件url，其为一个jsonObject的string：

jsonObject中仅有一个key为：fileUrl，代表上传的音频文件的ossUrl地址

```
{
    "fileUrl" : "https://***"
}
```

示例json如下：

```
{
  "parameters": {
    "biz_params": {
      "command_results": [
        {
          "invoke_result": "{\"fileUrl\":\"https://***.oss-cn-hangzhou.aliyuncs.com/%E8%AF%95%E9%A9%BE%E6%A1%88%E4%BE%8Bsmall.wav?OSSAccessKeyId=LTAI************&Expires=1764817795&Signature=9FuGR4ZMf%2BD8ZuW373HjS4jGrzM%3D\"}",
          "command_request_id": "multi_modal_meeting_slots#llm-***-mm_***-shanglu-123456#***#84178828aab44509"
        }
      ]
    }
  }
}
```

提交后将会在多模的[文本下发事件](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#3b421d978fco5)收到的**提交结束录音执行结果**的返回，返回中包含一个dataId，该dataId就是智能纪要中[CreateTask](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-create-task#5827c2ab596ko)接口返回的dataId。具体返回协议为，在事件的`payloa.output.extra_info.commands`中，是一个jsonArray的字符串，如下：

```
{
  "output": {
    "extra_info": {
      "commands": "[{\"intent_info\":{\"domain\":\"tingwu_meeting\",\"intent\":\"quit_audio_recording\"},\"name\":\"end_local_recording_execution_res\",\"params\":[{\"name\":\"dataId\",\"value\":\"fgVnGvyXN5xA\",\"normValue\":\"fgVnGvyXN5xA\"}]}]"
    }
  }
}
```

`commands`反序列化为jsonArray后如下，注意其中name为`end_local_recording_execution_res`的命令，该命令的params数组中name为`dataId`的一项，该项的value即为返回的dataId。

```
[
  {
    "intent_info": {
      "domain": "tingwu_meeting",
      "intent": "quit_audio_recording"
    },
    "name": "end_local_recording_execution_res",
    "params": [
      {
        "name": "dataId",
        "value": "fgVnGvyXN5xA",
        "normValue": "fgVnGvyXN5xA"
      }
    ]
  }
]
```

## **异步获取智能纪要结果**

参考智能纪要中的[通过回调获取异步任务结果](https://help.aliyun.com/zh/model-studio/tingwu-agent-async-get-task-result#ad8a228269hfv)来获取转写结果。

多模集成下智能纪要返回协议请参考：[多模集成下的智能纪要Agent事件总线回调协议](https://eventbridge.console.aliyun.com/cn-beijing/event-bus/default/event-source/acs.tingwuagent/detail)中type字段为`tingwuagent:TaskStateUpdated:UniversalAgentResultChanged`的事件，该事件中data字段为返回的智能纪要结果，其说明如下：

**字段名**

**类型**

**说明**

**示例值**

agentId

string

agent类型，固定值为tingwu-meeting

tingwu-meeting，代表的应用类型

appId

string

多模态应用id

mm\_\*\*\*

taskStatus

String

任务状态码，分别代表处理中，成功，失败

-   PROCESSING
    
-   SUCCESS
    
-   FAILED
    

SUCCESS

errorCode

string

错误码（失败时才有）

TSC.FileError

errorMessage

string

错误描述信息（失败时才有）

File cannot be read.

output

string

智能纪要结果，为一个json字符串，需要反序列化到object当中进行使用，其中的格式参考：

```
"{\"autoChaptersPath\":\"https://***/***?***\",\"customPromptPath\":\"https://***/***?***\",\"meetingAssistancePath\":\"https://***/***?***\",\"playbackUrl\":\"https://***/***?***\",\"pptExtractionPath\":\"https://***/***?***\",\"status\":0,\"summarizationPath\":\"https://***/***?***\",\"textPolishPath\":\"https://***/***?***\",\"transcriptionPath\":\"https://***/***?***\",\"translationsPath\":\"https://***/***?***\"}"
```

extension

string

智能纪要任务额外信息

```
"{\"appId\":\"***\",\"dataId\":\"***\",\"model\":\"***\",\"userId\":\"***\",\"userSpaceId\":\"***\"}"
```

requestId

string

请求的唯一标识

fa7760d\*\*\*

#### **output解析**

output的json字符串反序列化以后会是类似如下json：

```
{
  "autoChaptersPath": "https://***/***?***",
  "customPromptPath": "https://***/***?***",
  "meetingAssistancePath": "https://***/***?***",
  "playbackUrl": "https://***/***?***",
  "pptExtractionPath": "https://***/***?***",
  "status": 0,
  "summarizationPath": "https://***/***?***",
  "textPolishPath": "https://***/***?***",
  "transcriptionPath": "https://***/***?***",
  "translationsPath": "https://***/***?***"
}
```

其中每个path的解析协议请参考：[智能纪要GetTask的返回参数](https://help.aliyun.com/zh/model-studio/tingwu-meeting-offline-api-get-task#117fc92769d5k)。

#### **extension解析**

extension的json字符串反序列化以后会是类似如下json：

```
{
  "appId": "***",
  "dataId": "***",
  "model": "ingwu-meeting",
  "userId": "***",
  "userSpaceId": "***"
}
```

每个字段解释如下：

字段名

含义

appId

通义听悟智能纪要应用id

dataId

通义听悟智能纪要dataId，唯一标识本次会议/转写/记录等数据对象

model

通义听悟Agent类型

userId

阿里云用户主账号id

userSpaceId

百炼用户工作空间id

## **完整流程示例代码**

XML

```
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.alibaba.tingwu</groupId>
    <artifactId>test</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>8</maven.compiler.source>
        <maven.compiler.target>8</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>com.aliyun</groupId>
            <artifactId>aliyun-java-sdk-core</artifactId>
            <version>4.6.4</version>
        </dependency>

        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>fastjson</artifactId>
            <version>1.2.74</version>
        </dependency>

        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.30</version>
            <scope>provided</scope>
        </dependency>

        <!-- Java-WebSocket -->
        <dependency>
            <groupId>org.java-websocket</groupId>
            <artifactId>Java-WebSocket</artifactId>
            <version>1.5.3</version>
        </dependency>

        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.9.3</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.13.1</version>
            <scope>compile</scope>
        </dependency>

        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>dashscope-sdk-java</artifactId>
            <version>2.21.16</version>
        </dependency>
        <dependency>
            <groupId>io.reactivex.rxjava2</groupId>
            <artifactId>rxjava</artifactId>
            <version>2.2.21</version>
        </dependency>
        <dependency>
            <groupId>org.projectlombok</groupId>
            <artifactId>lombok</artifactId>
            <version>1.18.26</version>
            <scope>compile</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-engine</artifactId>
            <version>5.10.2</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter-api</artifactId>
            <version>5.10.2</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.junit-pioneer</groupId>
            <artifactId>junit-pioneer</artifactId>
            <version>1.9.1</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>io.javalin</groupId>
            <artifactId>javalin</artifactId>
            <version>4.4.0</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
            <version>2.8.9</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>2.0.7</version>
        </dependency>
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>2.0.7</version>
        </dependency>
        <dependency>
            <groupId>org.jetbrains.kotlin</groupId>
            <artifactId>kotlin-stdlib-jdk8</artifactId>
            <version>1.8.21</version>
        </dependency>
        <dependency>
            <groupId>com.squareup.okio</groupId>
            <artifactId>okio</artifactId>
            <version>3.6.0</version>
        </dependency>
        <dependency>
            <groupId>com.squareup.okhttp3</groupId>
            <artifactId>mockwebserver</artifactId>
            <version>4.12.0</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.squareup.okhttp3</groupId>
            <artifactId>logging-interceptor</artifactId>
            <version>4.12.0</version>
        </dependency>
        <dependency>
            <groupId>com.squareup.okhttp3</groupId>
            <artifactId>okhttp-sse</artifactId>
            <version>4.12.0</version>
        </dependency>
        <dependency>
            <groupId>com.squareup.okhttp3</groupId>
            <artifactId>okhttp</artifactId>
            <version>4.12.0</version>
        </dependency>
        <dependency>
            <groupId>com.github.victools</groupId>
            <artifactId>jsonschema-generator</artifactId>
            <version>4.31.1</version>
        </dependency>
    </dependencies>

</project>
```

Java

```
import com.alibaba.dashscope.multimodal.MultiModalDialog;
import com.alibaba.dashscope.multimodal.MultiModalDialogCallback;
import com.alibaba.dashscope.multimodal.MultiModalRequestParam;
import com.alibaba.dashscope.multimodal.State;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.alibaba.fastjson.annotation.JSONField;
import com.google.gson.JsonObject;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import javax.sound.sampled.*;
import java.nio.ByteBuffer;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static java.lang.Thread.sleep;

@Slf4j
public class MultiModalMeetingOfflineSDKDemo {
    @Data
        public static class CommandDTO {
            @JSONField(name = "intent_info")
            private IntentInfo intentInfo;
            @JSONField(name = "command_request_id")
            private String commandRequestId;
            private String name;

            private JSONArray params;
            @Data
                public static class IntentInfo {
                    private String domain;
                    private String intent;
                }
        }

    static int enterListeningTimes = 0;
    static State.DialogState currentState;
    static MultiModalDialog conversation;
    static int sampleRate = 16000;
    static String model = "multimodal-dialog";
    static String workspaceId = "your_workspace_id"; // 替换为您的Workspace ID
    static String appId = "your_app_id"; // 替换为您的 APP ID
    static String dialogId = "";
    static String apiKey = "your_api_key"; // 替换为您的API Key
    static String localRecordedFileUrl = ""; // 你的本地录音文件的fileUrl
    @Test
    public void testMultimodalDuplex() throws Exception {
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        log.info("baseWebsocketApiUrl: {}", Constants.baseWebsocketApiUrl);

        /*
step1. 设置duplex
step2. 从本地麦进行录制，执行相关指令(至少依次说出， 开启录音/结束录音 两条指令)
step3. 每条指令收到回复后在callback中更新端侧状态
step4. 结束录用后用户需要手动提交转写，而后在callback中获取纪要转写结果
*/
        MultiModalRequestParam params =
            MultiModalRequestParam.builder()
            .customInput(MultiModalRequestParam.CustomInput.builder()
                         .appId(appId)
                         .workspaceId(workspaceId)
                         .dialogId("")
                         .build()
                        )
            .upStream(
                MultiModalRequestParam.UpStream.builder()
                .mode("duplex")
                .audioFormat("pcm")
                .build())
            .downStream(
                MultiModalRequestParam.DownStream.builder()
                .voice("longxiaochun_v2")
                .sampleRate(sampleRate)
                .build())
            .clientInfo(
                MultiModalRequestParam.ClientInfo.builder()
                .userId("1234")
                .device(MultiModalRequestParam.ClientInfo.Device.builder().uuid("1234").build())
                .build())
            .apiKey(apiKey)
            .model(model)
            .build();

        log.info("params: {}", JsonUtils.toJson(params));

        conversation = new MultiModalDialog(params, getCallback());

        conversation.start();
        while (currentState != State.DialogState.LISTENING) {
            try {
                sleep(100);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }

        // 发送音频
        sendAudioFromLocalMicrophone(conversation);

        conversation.stop();

        System.out.println("############ End Test duplex ############");
    }

    public void sendAudioFromLocalMicrophone(MultiModalDialog conversation) throws Exception {
        AudioFormat format = new AudioFormat(sampleRate, 16, 1, true, false);
        DataLine.Info info = new DataLine.Info(TargetDataLine.class, format);
        TargetDataLine targetLine = (TargetDataLine) AudioSystem.getLine(info);
        targetLine.open(format);
        targetLine.start();

        byte[] buffer = new byte[3200]; // 和服务端协议 buffer 匹配
        System.out.println("Start capture audio from microphone, press Ctrl+C to stop...");
        long start = System.currentTimeMillis();

        int i = 0;
        while (true) {
            int numBytesRead = targetLine.read(buffer, 0, buffer.length);
            if (numBytesRead > 0) {
                conversation.sendAudioData((ByteBuffer.wrap(buffer, 0, numBytesRead)));
            }
            // 1 分钟后自动停止发送
            if(System.currentTimeMillis() - start > 60000) { // 连续发送1分钟
                break;
            }
            ++i;
            if (i%10 == 0) {
                System.out.println("local microphone sending!");
            }
            Thread.sleep(100); // 控制发送速率
        }
        targetLine.stop();
        targetLine.close();
        System.out.println("Mic audio capture ended");
    }

    public static MultiModalDialogCallback getCallback() {
        return new MultiModalDialogCallbackImpl();
    }

    public static class MultiModalDialogCallbackImpl extends MultiModalDialogCallback {
        @Override
        public void onConnected() {}

        @Override
        public void onStarted(String dialogId) {

            log.info("onStarted: {}, self {}", dialogId, this);

        }

        private void changeToNewRecordingStatus(String newStatus) {

            JSONObject tingwuMeetingObj = new JSONObject();
            JSONObject clientRecordingStatus = new JSONObject();
            clientRecordingStatus.put("clientRecordingStatus", newStatus);
            tingwuMeetingObj.put("tingwu_meeting", clientRecordingStatus);

            // 调用updateInfo更新端侧录音状态到录音中
            conversation.updateInfo(
                MultiModalRequestParam.UpdateParams.builder()
                .bizParams(MultiModalRequestParam.BizParams.builder()
                           .userDefinedParams(
                               tingwuMeetingObj
                           )
                           .build())
                .build()
            );
        }

        @Override
        public void onStopped(String dialogId) {
            log.info("onStopped: {}", dialogId);
        }

        @Override
        public void onSpeechStarted(String dialogId) {
            log.info("onSpeechStarted: {}", dialogId);
        }

        @Override
        public void onSpeechEnded(String dialogId) {
            log.info("onSpeechEnded: {}", dialogId);
        }
        @Override
        public void onError(String dialogId, String errorCode, String errorMsg) {
            log.error("onError: {}, {}, {}, self {}", dialogId, errorCode, errorMsg, this);
            enterListeningTimes++ ; //force quit dialog test
        }

        @Override
        public void onStateChanged(State.DialogState state) {
            log.info("onStateChanged: {}", state);
            currentState = state;
            if (currentState == State.DialogState.LISTENING) {
                enterListeningTimes++;
                log.info("enterListeningTimes: {}", enterListeningTimes);
            }
        }

        @Override
        public void onSpeechAudioData(ByteBuffer audioData) {
            System.out.println("Received binary message (audio data)");
        }

        @Override
        public void onRespondingStarted(String dialogId) {
            log.info("onRespondingStarted: {}", dialogId);
            conversation.localRespondingStarted();
        }

        @Override
        public void onRespondingEnded(String s, JsonObject jsonObject) {
        }

        @Override
        public void onRespondingContent(String dialogId, JsonObject content) {
            log.info("onRespondingContent: {}, {}", dialogId, content);

            if (content != null && content.has("extra_info")) {
                JsonObject extraInfo = content.get("extra_info").getAsJsonObject();
                if (extraInfo != null && extraInfo.has("commands")) {
                    String commandsStr = extraInfo.get("commands").getAsString();
                    List<CommandDTO> commands = JSONObject.parseArray(commandsStr, CommandDTO.class);
                    for (CommandDTO commandDTO : commands) {
                        // 处理开启录音
                        if (commandDTO != null && commandDTO.getName().equals("start_local_recording")) {
                            changeToNewRecordingStatus("1");
                        }
                            // 处理暂停录音
                        else if (commandDTO != null && commandDTO.getName().equals("pause_local_recording")) {
                            changeToNewRecordingStatus("2");
                        }
                            // 处理恢复录音
                        else if (commandDTO != null && commandDTO.getName().equals("resume_local_recording")) {
                            changeToNewRecordingStatus("1");
                        }
                            // 处理结束录音
                        else if (commandDTO != null && commandDTO.getName().equals("end_local_recording")) {
                            changeToNewRecordingStatus("0");
                            System.out.println("Received end_local_recording command!");

                            String reqId = commandDTO.getCommandRequestId();
                            JSONObject invokeResObj = new JSONObject();
                            invokeResObj.put("fileUrl", localRecordedFileUrl);
                            JSONObject cmdRes = new JSONObject();
                            cmdRes.put("command_request_id", reqId);
                            cmdRes.put("invoke_result", JSONObject.toJSONString(invokeResObj));
                            JSONArray cmdResList = new JSONArray();
                            cmdResList.add(cmdRes);

                            Map<String, Object> paasThroughParams = new HashMap<>();
                            paasThroughParams.put("command_results", JSONObject.toJSON(cmdResList));

                            // 发送结束录音指令执行结果
                            conversation.requestToRespond(
                                "prompt",
                                "",
                                MultiModalRequestParam.UpdateParams.builder()
                                .bizParams(MultiModalRequestParam.BizParams.builder()
                                           .passThroughParams(paasThroughParams)
                                           .build())
                                .build()
                            );
                            try {
                                Thread.sleep(100);
                            } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                            }
                        }
                            // 处理结束录音提交文件进行转写的返回结果
                        else if (commandDTO != null && commandDTO.getName().equals("end_local_recording_execution_res")) {
                            System.out.println("Received end_local_recording_execution_res command!");
                            System.out.println("dataId param is: " + JSONObject.toJSONString(commandDTO.getParams()));
                        }
                    }
                }
            }
        }

        @Override
        public void onSpeechContent(String dialogId, JsonObject content) {
            log.info("onSpeechContent: {}, {}", dialogId, content);
        }

        @Override
        public void onRequestAccepted(String dialogId) {
            log.info("onRequestAccepted: {}", dialogId);
        }

        @Override
        public void onClosed() {
            log.info("onClosed , self {}", this);
            enterListeningTimes++ ;
        }
    }
}
```
