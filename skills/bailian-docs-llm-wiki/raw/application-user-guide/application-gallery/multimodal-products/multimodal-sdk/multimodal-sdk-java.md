# 服务端Java SDK

本文介绍了如何使用阿里云百炼大模型服务提供的实时多模交互服务端 Java SDK，包括SDK下载安装、关键接口及代码示例。

## **多模态实时交互服务架构**

![多模态实时交互服务接入架构-通用-流程图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7227370571/p976841.jpg)

## **前提条件**

开通阿里云百炼实时多模交互应用，获取[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)、[APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)和[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## **环境和安装**

您可以通过maven或者gradle集成阿里云Dashscope官方SDK（版本号 >= 2.21.16）。

```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>dashscope-sdk-java</artifactId>
    <version>2.21.16</version>
</dependency>
```

## **交互模式说明**

SDK支持 **Push2Talk**、 **Tap2Talk**和**Duplex**（全双工）三种交互模式。

-   Push2Talk: 长按说话，抬起结束（或者点击开始，点击结束 ）的收音方式。
    
-   Tap2Talk: 点击开始说话，自动判断用户说话结束的收音方式。
    
-   Duplex: 全双工交互，连接后支持在任意时刻说话，支持语音打断。视频交互建议使用duplex模式。
    

## **音频格式说明**

服务端接入方式只支持 websocket 传输协议。

-   音频格式说明：
    
    -   上行：支持 pcm 和 opus 格式音频进行语音识别。
        
    -   下行：支持 pcm 和 mp3 音频流。
        

## **接口说明**

### **MultiModalDialog**

服务入口类

#### 1、MultiModalDialog(MultiModalRequestParam param, MultiModalDialogCallback callback)

初始化服务对象，设置对话参数和回调。

```
/**
 * Constructor initializes service options and creates a duplex communication API instance.
 *
 * @param param Request parameter
 * @param callback Callback interface
 */
public MultiModalDialog(MultiModalRequestParam param, MultiModalDialogCallback callback)
```

#### **2**、**start**

启动对话服务，返回onStarted回调。注意onStarted会回调dialogId。

```
/**
 * Starts the conversation session.
 */
public void start()
```

#### **3**、startSpeech

通知服务端开始上传音频，注意需要在Listening状态才可以调用。只需要在Push2Talk模式下调用。

```
/**
 * Starts upload speech.
 */
public void startSpeech()
```

#### **4**、sendAudioData

通知服务端上传音频。

```
/**
 * Sends audio frame.
 *
 * @param audioFrame Audio frame data
 */
public void sendAudioData(ByteBuffer audioFrame)
```

#### **5**、stopSpeech

通知服务端结束上传音频。只需要在 Push2Talk(按键说) 模式下调用。

```
/**
 * Stops upload speech.
 */
public void stopSpeech()
```

#### **6**、**interrupt**

通知服务端，客户端需要打断当前交互，开始说话。会返回RequestAccepted。

```
/**
 * Interrupts current operation.
 */
public void interrupt()
```

#### **7**、localRespondingStarted

通知服务端，客户端开始播放tts音频。

```
/**
 * Local player start broadcast tts
 */
public void localRespondingStarted()
```

#### **8**、localRespondingEnded

通知服务端，客户端结束播放tts音频。

```
/**
 * Local player broadcast tts end
 */
public void localRespondingEnded()
```

#### **9**、**stop**

结束当前轮次对话。

```
/**
 * Stops the conversation.
 */ 
public void stop()
```

#### **10**、getDialogState

获得当前对话服务状态。DialogState枚举。

```
/**
 * Gets current dialogue state.
 *
 * @return Current dialogue state
 */
public State.DialogState getDialogState()
```

#### **11**、requestToRespond

端侧主动通过文本直接发起tts语音合成，或者向服务端发起图片等其他请求。

```
/**
 * Requests response.
 *
 * @param type Response type
 * @param text Response text
 * @param updateParams Update parameters
 */
public void requestToRespond(String type, String text, MultiModalRequestParam.updateParams updateParams)
```

#### **12**、updateInfo

更新参数信息等操作。

```
/**
 * Updates information.
 *
 * @param updateParams Update parameters
 */
public void updateInfo(MultiModalRequestParam.updateParams updateParams)
```

#### **13 sendHeartBeat**

发送心跳信息，否则存在60秒超时报错。需要保持长连接场景使用，请每20秒调用一次发送接口。

```
/**
 * Send heart beat.
 *
 */
public void sendHeartBeat()
```

### MultiModalDialogCallback

回调函数

```
import com.alibaba.dashscope.multimodal.State;

/**
 * Abstract class representing callbacks for multi-modal conversation events.
 *
 * @author songsong.shao
 * @date 2025/4/27
 */
public abstract class MultiModalDialogCallback {

    /**
     * Called when the conversation is connected.
     */
    public abstract void onConnected();

    /**
     * Called when a conversation starts with a specific dialog ID.
     *
     * @param dialogId The unique identifier for the dialog.
     */
    public abstract void onStarted(String dialogId);

    /**
     * Called when a conversation stops with a specific dialog ID.
     *
     * @param dialogId The unique identifier for the dialog.
     */
    public abstract void onStopped(String dialogId);

    /**
     * Called when speech starts in a specific dialog.
     *
     * @param dialogId The unique identifier for the dialog.
     */
    public abstract void onSpeechStarted(String dialogId);

    /**
     * Called when speech ends in a specific dialog.
     *
     * @param dialogId The unique identifier for the dialog.
     */
    public abstract void onSpeechEnded(String dialogId);

    /**
     * Called when an error occurs during a conversation.
     *
     * @param dialogId The unique identifier for the dialog.
     * @param errorCode The error code associated with the error.
     * @param errorMsg The error message associated with the error.
     */
    public abstract void onError(String dialogId, String errorCode, String errorMsg);

    /**
     * Called when the conversation state changes.
     *
     * @param state The new state of the conversation.
     */
    public abstract void onStateChanged(State.DialogState state);

    /**
     * Called when speech audio data is available.
     *
     * @param audioData The audio data as a ByteBuffer.
     */
    public abstract void onSpeechAudioData(ByteBuffer audioData);

    /**
     * Called when responding starts in a specific dialog.
     *
     * @param dialogId The unique identifier for the dialog.
     */
    public abstract void onRespondingStarted(String dialogId);

    /**
     * Called when responding ends in a specific dialog.
     *
     * @param dialogId The unique identifier for the dialog.
     * @param content The content of the response as a JsonObject.
     */
    public abstract void onRespondingEnded(String dialogId, JsonObject jsonObject);

    /**
     * Called when responding content is available in a specific dialog.
     *
     * @param dialogId The unique identifier for the dialog.
     * @param content The content of the response as a JsonObject.
     */
    public abstract void onRespondingContent(String dialogId, JsonObject content);

    /**
     * Called when speech content is available in a specific dialog.
     *
     * @param dialogId The unique identifier for the dialog.
     * @param content The content of the speech as a JsonObject.
     */
    public abstract void onSpeechContent(String dialogId, JsonObject content);

    /**
     * Called when a request is accepted in a specific dialog.
     *
     * @param dialogId The unique identifier for the dialog.
     */
    public abstract void onRequestAccepted(String dialogId);

    /**
     * Called when the conversation closes.
     */
    public abstract void onClosed();
}
```

### MultiModalRequestParam

请求参数类

请求参数均支持builder模式设置参数，参数的值和说明参考如下。

#### **Start建联请求参数**

[Start - Input Message](https://help.aliyun.com/zh/model-studio/multimodal-interaction-protocol#b5d943046av48)

一级参数

二级参数

三级参数

四级参数

类型

是否必选

说明

task\_group

任务组名称，固定为"aigc"

task

任务名称，固定为"multimodal-generation"

function

调用功能，固定为"generation"

model

服务名称，固定为"multimodal-dialog"

input

workspace\_id

string

是

用户业务空间ID

app\_id

string

是

客户在管控台创建的应用ID，可以根据值规律确定使用哪个对话系统

directive

string

是

指令名称：Start

dialog\_id

string

否

对话ID，如果传入表示接着聊

parameters

upstream

type

string

是

上行类型：

-   AudioOnly：仅语音通话
    
-   AudioAndVideo：上传视频
    

mode

string

否

客户端使用的模式，可选项：

-   push2talk
    
-   tap2talk
    
-   duplex
    

默认tap2talk

audio\_format

string

否

音频格式，支持pcm，opus，默认为pcm

downstream

voice

string

否

合成语音的音色

sample\_rate

int

否

合成语音的采样率，默认采样率24k

intermediate\_text

string

否

控制返回给用户哪些中间文本：

-   transcript：返回用户语音识别结果
    
-   dialog：返回对话系统回答中间结果
    

可以设置多种，以逗号分隔，默认为transcript

audio\_format

string

否

音频格式，支持pcm，mp3，默认为pcm

client\_info

user\_id

string

是

终端用户ID，用来做用户相关的处理

device

uuid

string

否

客户端全局唯一的ID，需要用户自己生成，传入SDK

network

ip

string

否

调用方公网IP

location

latitude

string

否

调用方维度信息

longitude

string

否

调用方经度信息

city\_name

string

否

调用方所在城市

biz\_params

user\_defined\_params

object

否

其他需要透传给agent的参数

user\_defined\_tokens

object

否

透传agent所需鉴权信息

tool\_prompts

object

否

透传agent所需prompt

user\_query\_params

object

否

透传用户请求自定义参数

user\_prompt\_params

object

否

透传用户prompt自定义参数

#### **RequestToRespond 请求参数**

一级参数

二级参数

三级参数

类型

是否必选

说明

input

directive

string

是

指令名称：RequestToRespond

dialog\_id

string

是

对话ID

type

string

是

服务应该采取的交互类型：

-   transcript：表示直接把文本转语音
    
-   prompt：表示把文本发送给大模型并获取回答
    

text

string

是

要处理的文本，可以是""空字符串，非null即可

parameters

images

list\[\]

否

需要分析的图片信息

biz\_params

object

否

与Start消息中biz\_params相同，传递对话系统自定义参数。RequestToRespond的biz\_params参数只在本次请求中生效。

#### **UpdateInfo 请求参数**

一级参数

二级参数

三级参数

类型

是否必选

说明

input

directive

string

是

指令名称：UpdateInfo

dialog\_id

string

否

对话ID

parameters

images

list\[\]

否

图片数据

client\_info

status

object

否

客户端当前状态

biz\_params

object

否

与Start消息中biz\_params相同，传递对话系统自定义参数

### **对话状态说明（**DialogState**）**

voicechat服务有LISTENING、THINKING、RESPONDING三个状态，分别代表：

```
IDLE("Idle"), 系统尚未建立连接
LISTENING("Listening"), 表示机器人正在监听用户输入。用户可以发送音频。
THINKING("Thinking"),表示机器人正在思考。
RESPONDING("Responding")表示机器人正在生成语音或语音回复中。
```

### **对话LLM输出结果**

onRespondingContent

一级参数

二级参数

三级参数

类型

是否必选

说明

output

event

string

是

事件名称如：RequestAccepted

dialog\_id

string

是

对话ID

round\_id

string

是

本轮交互的ID

llm\_request\_id

string

是

调用LLM的request\_id

text

string

是

系统对外输出的文本，流式全量输出

spoken

string

是

合成语音时使用的文本，流式全量输出

finished

bool

是

输出是否结束

extra\_info

object

否

其他扩展信息，目前支持：

-   commands: 命令字符串
    
-   agent\_info: 智能体信息
    
-   tool\_calls: 插件返回的信息
    
-   dialog\_debug: 对话debug信息
    
-   timestamps: 链路中各节点时间戳
    

## **调用交互时序图**

![image.svg](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6421377471/p957898.svg)

## **调用示例**

### **1、初始化对话参数**

调用MultiModalRequestParam类中的各子类的builder方法构建参数。

```
MultiModalRequestParam params =
        MultiModalRequestParam.builder()
            .customInput(
                MultiModalRequestParam.CustomInput.builder()
                    .build())
            .upStream(
                MultiModalRequestParam.UpStream.builder()
                    .mode("push2talk")
                    .audioFormat("pcm")
                    .build())
            .downStream(
                MultiModalRequestParam.DownStream.builder()
                    .voice("longxiaochun_v2")
                    .sampleRate(48000)
                    .build())
            .dialogAttributes(
                MultiModalRequestParam.DialogAttributes.builder().prompt("你好").build())
            .clientInfo(
                MultiModalRequestParam.ClientInfo.builder()
                    .userId("1234")
                    .device(MultiModalRequestParam.ClientInfo.Device.builder().uuid("1234").build())
                    .build())
            .apiKey("sk-9d11****************************")
            .model("multimodal-dialog")
            .build();
```

### **2、实例化回调函数**

```
public static MultiModalDialogCallback getCallback() {
    return new MultiModalDialogCallbackImpl();
  }

  public static class MultiModalDialogCallbackImpl extends MultiModalDialogCallback {
    ...
  }
```

### **3、创建**MultiModalDialog对象

`conversation = new MultiModalDialog(params, getCallback());`

### **完整调用示例**

建议使用 Maven 或 Gradle 构建工具运行代码示例，并在相应的配置文件（Maven 的 pom.xml 或 Gradle 的 build.gradle）中添加所需的依赖项，包括 Gson、OkHttp、RxJava、Apache Log4j、Lombok 和 JUnit。

## 配置文件

具体配置可能因所使用的 Maven 或 Gradle 版本而异，以下内容仅供参考，请根据实际环境进行相应调整。

## Maven

```
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.alibaba.nls</groupId>
    <artifactId>bailian-demo</artifactId>
    <version>1.0-SNAPSHOT</version>
    <dependencies>
        <dependency>
            <groupId>com.alibaba</groupId>
            <artifactId>dashscope-sdk-java</artifactId>
            <version>2.20.5</version>
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
        <!--  dependent by okhttp -->
        <dependency>
            <groupId>org.jetbrains.kotlin</groupId>
            <artifactId>kotlin-stdlib-jdk8</artifactId>
            <version>1.8.21</version>
        </dependency>
        <!--  dependent by okhttp -->
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
        <!--  function call support  -->
        <dependency>
            <groupId>com.github.victools</groupId>
            <artifactId>jsonschema-generator</artifactId>
            <version>4.31.1</version>
        </dependency>
    </dependencies>
    <properties>
        <maven.compiler.source>11</maven.compiler.source>
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

</project>
```

## Gradle

```
plugins {
    id 'java'
}

group = 'com.test'
version = '1.0-SNAPSHOT'

repositories {
    mavenCentral()
    maven {
        url 'https://maven.aliyun.com/repository/public'
    }
    maven {
        url 'https://plugins.gradle.org/m2/'
    }
}

dependencies {
    // Dashscope SDK
    implementation 'com.alibaba:dashscope-sdk-java:2.20.5'
    // 第三方库
    // https://mvnrepository.com/artifact/com.google.code.gson/gson
    implementation 'com.google.code.gson:gson:2.13.1'
    // https://mvnrepository.com/artifact/io.reactivex.rxjava2/rxjava
    implementation 'io.reactivex.rxjava2:rxjava:2.2.21'
    // https://mvnrepository.com/artifact/com.squareup.okhttp3/okhttp
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'          // 核心 OkHttp
    implementation 'com.squareup.okhttp3:logging-interceptor:4.12.0' // 日志拦截器

    // 日志相关依赖
    implementation 'org.apache.logging.log4j:log4j-core:2.17.1'
    implementation 'org.apache.logging.log4j:log4j-api:2.17.1'
    // 如果你使用 SLF4J 门面
    implementation 'org.apache.logging.log4j:log4j-slf4j-impl:2.17.1'

    // 测试相关依赖
    testImplementation 'org.junit.jupiter:junit-jupiter-api:5.10.0'
    testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.10.0'
    testImplementation 'org.apache.logging.log4j:log4j-core:2.17.1'
    testImplementation 'org.apache.logging.log4j:log4j-slf4j-impl:2.17.1'
    testAnnotationProcessor 'org.projectlombok:lombok:1.18.30'

    // Lombok 支持
    implementation 'org.projectlombok:lombok:1.18.30'
    annotationProcessor 'org.projectlombok:lombok:1.18.30'
}

test {
    useJUnitPlatform()
}
```

## Java代码

## MultiModalDialogTestCases.java

```
package org.alibaba.speech.examples.speech_plus;

import com.alibaba.dashscope.multimodal.MultiModalDialog;
import com.alibaba.dashscope.multimodal.MultiModalDialogCallback;
import com.alibaba.dashscope.multimodal.MultiModalRequestParam;
import com.alibaba.dashscope.multimodal.State;
import com.alibaba.dashscope.utils.Constants;
import com.alibaba.dashscope.utils.JsonUtils;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import org.alibaba.speech.examples.speech_plus.utils.FileWriterUtil;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.*;

import static java.lang.Thread.sleep;

/**
 * Multi-modal dialog test cases for demonstrating various interaction modes
 * including push-to-talk, tap-to-talk, duplex communication, text synthesis,
 * visual Q&A, and agent DJ functionality.
 * 
 * @author songsong.shao
 * @date 2025/4/28
 */

public class MultiModalDialogTestCases {
    private static final Logger log = LoggerFactory.getLogger(MultiModalDialogTestCases.class);
    // Constants for audio processing
    private static final int AUDIO_CHUNK_SIZE = 3200; // Audio chunk size in bytes
    private static final int SLEEP_INTERVAL_MS = 100;  // Sleep interval in milliseconds
    private static final int WAIT_TIMEOUT_MS = 2000;   // Wait timeout in milliseconds
    private static final int VIDEO_FRAME_INTERVAL_MS = 500;

    // State management variables
    private static State.DialogState currentState;
    private static MultiModalDialog conversation;
    private static int enterListeningTimes = 0;
    private static FileWriterUtil fileWriterUtil;
    private static boolean vqaUseUrl = false;
    private volatile boolean isVideoStreamingActive = false;
    private Thread videoStreamingThread;
    
    // Configuration parameters - should be set before running tests
    public static String workspaceId = "";
    public static String appId = "";
    public static String dialogId = "";
    public static String apiKey = "";
    public static String model = "";

    /**
     * Test push-to-talk mode interaction
     * Flow: Set push2talk -> Wait for listening -> Start speech -> Send audio -> Stop speech -> Wait for response
     */
    public void testMultimodalPush2Talk() {
        log.info("############ Starting Push2Talk Test ############");
        
        try {
            // Build request parameters for push-to-talk mode
            MultiModalRequestParam params = buildBaseRequestParams("push2talk");
            log.debug("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation with callback
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Wait for the system to enter listening state
            waitForListeningState();
            
            // Start speech recognition
            conversation.startSpeech();
            
            // Send audio data from file
            sendAudioFromFile("../../../../sample-data/1_plus_1.wav");
            
            // Stop speech recognition
            conversation.stopSpeech();

            // Wait for conversation completion
            waitForConversationCompletion(2);
            
            // Clean up
            stopConversation();
            
        } catch (Exception e) {
            log.error("Error in push2talk test: ", e);
        } finally {
            log.info("############ Push2Talk Test Completed ############");
        }
    }

    /**
     * Test tap-to-talk mode interaction
     * Flow: Set tap2talk -> Wait for listening -> Start speech manually -> Send audio -> Wait for response
     */
    public void testMultimodalTap2Talk() {
        log.info("############ Starting Tap2Talk Test ############");
        
        try {
            // Build request parameters for tap-to-talk mode
            MultiModalRequestParam params = buildBaseRequestParams("tap2talk");
            log.debug("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Wait for listening state
            waitForListeningState();
            
            // Manually start speech (required for tap2talk mode)
            conversation.startSpeech();
            
            // Send audio data
            sendAudioFromFile("../../../../sample-data/1_plus_1.wav");

            // Wait for conversation completion
            waitForConversationCompletion(2);
            
            // Clean up
            stopConversation();
            
        } catch (Exception e) {
            log.error("Error in tap2talk test: ", e);
        } finally {
            log.info("############ Tap2Talk Test Completed ############");
        }
    }

    /**
     * Test duplex mode interaction
     * Flow: Set duplex -> Wait for listening -> Send audio -> Wait for response
     */
    public void testMultimodalDuplex() {
        log.info("############ Starting Duplex Test ############");
        
        try {
            // Build request parameters for duplex mode
            MultiModalRequestParam params = buildBaseRequestParams("duplex");
            log.info("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Wait for listening state
            waitForListeningState();
            
            // Send audio data directly (no manual start needed for duplex)
            sendAudioFromFile("../../../../sample-data/1_plus_1.wav");

            // Wait for conversation completion
            waitForConversationCompletion(2);
            
            // Clean up
            stopConversation();
            
        } catch (Exception e) {
            log.error("Error in duplex test: ", e);
        } finally {
            log.info("############ Duplex Test Completed ############");
        }
    }

    /**
     * Test text synthesis functionality
     * Flow: Send text for TTS -> Save synthesized audio
     */
    public void testMultimodalTextSynthesizer() {
        log.info("############ Starting Text Synthesizer Test ############");
        
        try {
            // Initialize file writer for audio output
            fileWriterUtil = new FileWriterUtil();
            
            // Build request parameters
            MultiModalRequestParam params = buildBaseRequestParams("push2talk");
            log.debug("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Wait for listening state
            waitForListeningState();
            
            // Create output file for synthesized audio
            fileWriterUtil.createFile("./test.pcm");
            
            // Request text synthesis
            String textToSynthesize = "幸福是一种技能，是你摒弃了外在多余欲望后的内心平和。";
            conversation.requestToRespond("transcript", textToSynthesize, null);

            // Wait for synthesis completion
            waitForConversationCompletion(2);
            
            // Finalize audio file
            fileWriterUtil.finishWriting();
            
            // Clean up
            conversation.stop();
            
        } catch (IOException e) {
            log.error("File operation error in text synthesizer test: ", e);
        } catch (Exception e) {
            log.error("Error in text synthesizer test: ", e);
        } finally {
            log.info("############ Text Synthesizer Test Completed ############");
        }
    }

    /**
     * Test Visual Q&A functionality using URL-based images
     * Flow: Send VQA request -> Receive visual_qa command -> Send image list -> Get response
     */
    public void testMultimodalVQA() {
        log.info("############ Starting VQA Test (URL-based) ############");
        
        try {
            vqaUseUrl = true;
            
            // Build request parameters
            MultiModalRequestParam params = buildBaseRequestParams("push2talk");
            log.debug("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Wait for listening state
            waitForListeningState();
            
            // Send VQA request
            conversation.requestToRespond("prompt", "拍照看看前面有什么东西", null);
            
            // Wait for VQA processing completion
            waitForConversationCompletion(3);
            
            // Clean up
            stopConversation();
            
        } catch (Exception e) {
            log.error("Error in VQA test: ", e);
        } finally {
            log.info("############ VQA Test Completed ############");
        }
    }

    /**
     * Test Visual Q&A functionality using Base64-encoded images
     * Flow: Send VQA request -> Receive visual_qa command -> Send base64 image -> Get response
     */
    public void testMultimodalVQABase64() {
        log.info("############ Starting VQA Test (Base64-based) ############");
        
        try {
            vqaUseUrl = false;
            
            // Build request parameters
            MultiModalRequestParam params = buildBaseRequestParams("push2talk");
            log.debug("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Wait for listening state
            waitForListeningState();
            
            // Send VQA request
            conversation.requestToRespond("prompt", "拍照看看前面有什么东西", null);
            
            // Wait for VQA processing completion
            waitForConversationCompletion(3);
            
            // Clean up
            stopConversation();
            
        } catch (Exception e) {
            log.error("Error in VQA Base64 test: ", e);
        } finally {
            log.info("############ VQA Base64 Test Completed ############");
        }
    }

    /**
     * Test brightness adjustment functionality
     * Flow: Send brightness adjustment request -> Process response
     */
    public void testMultimodalAdjustBrightness() {
        log.info("############ Starting Brightness Adjustment Test ############");
        
        try {
            vqaUseUrl = true;
            
            // Build request parameters
            MultiModalRequestParam params = buildBaseRequestParams("push2talk");
            log.debug("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Wait for listening state
            waitForListeningState();
            
            // Send brightness adjustment request
            conversation.requestToRespond("prompt", "调高亮度到10", null);

            // Create status update for bluetooth announcement
            JsonObject status = new JsonObject();
            JsonObject bluetoothAnnouncement = new JsonObject();
            bluetoothAnnouncement.addProperty("status", "stopped");
            status.add("bluetooth_announcement", bluetoothAnnouncement);

            MultiModalRequestParam.UpdateParams updateParams = MultiModalRequestParam.UpdateParams.builder()
                    .clientInfo(MultiModalRequestParam.ClientInfo.builder()
                            .status(status)
                            .build())
                    .build();

            // Wait for processing completion
            waitForConversationCompletion(2);
            
            log.info("############ Before stopping conversation ############");
            
            // Clean up
            stopConversation();
            
        } catch (Exception e) {
            log.error("Error in brightness adjustment test: ", e);
        } finally {
            log.info("############ Brightness Adjustment Test Completed ############");
        }
    }

    /**
     * Test Agent DJ functionality
     * Flow: Send radio station request -> Process response
     */
    public void testMultimodalAgentDJ() {
        log.info("############ Starting Agent DJ Test ############");
        
        try {
            vqaUseUrl = false;
            
            // Build request parameters
            MultiModalRequestParam params = buildBaseRequestParams("push2talk");
            log.debug("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Wait for listening state
            waitForListeningState();
            
            // Send DJ request
            conversation.requestToRespond("prompt", "打开新闻电台", null);
            
            // Wait for DJ processing completion
            waitForConversationCompletion(3);
            
            // Clean up
            stopConversation();
            
        } catch (Exception e) {
            log.error("Error in Agent DJ test: ", e);
        } finally {
            log.info("############ Agent DJ Test Completed ############");
        }
    }

    /**
     * Test LiveAI functionality with real-time video streaming and audio interaction
     * Flow: Set duplex mode -> Start video streaming -> Wait for listening -> Connect video channel
     *       -> Send audio queries -> Process responses with visual context
     */
    public void testMultimodalLiveAI() {
        log.info("############ Starting LiveAI Test ############");

        try {
            // Build request parameters for duplex mode
            MultiModalRequestParam params = buildBaseRequestParams("duplex");
            log.info("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Start send video frame loop
            startVideoFrameStreaming();
            // Wait for listening state
            waitForListeningState();
            conversation.sendHeartBeat();
            // Send video channel connect request, will response command : switch_video_call_success
            conversation.requestToRespond("prompt", "", connectVideoChannelRequest());

            // Send audio data directly (no manual start needed for duplex)
            sendAudioFromFile("./src/main/resources/what_in_picture.wav");

            // Wait for listening state twice
            waitForListeningState();

            sendAudioFromFile("./src/main/resources/what_color.wav");

            // Wait for conversation completion
            waitForConversationCompletion(3);

            // Clean up
            stopConversation();

            isVideoStreamingActive = false;
            if (videoStreamingThread != null && videoStreamingThread.isAlive()) {
                videoStreamingThread.interrupt();
            }

        } catch (Exception e) {
            log.error("Error in LiveAI test: ", e);
        } finally {
            log.info("############ LiveAI Test Completed ############");
        }
    }

    // ==================== Helper Methods ====================

    /**
     * Build base request parameters with common configuration
     * @param mode The interaction mode (push2talk, tap2talk, duplex)
     * @return Configured MultiModalRequestParam
     */
    private MultiModalRequestParam buildBaseRequestParams(String mode) {
        return MultiModalRequestParam.builder()
                .customInput(
                        MultiModalRequestParam.CustomInput.builder()
                                .workspaceId(workspaceId)
                                .appId(appId)
                                .build())
                .upStream(
                        MultiModalRequestParam.UpStream.builder()
                                .mode(mode)
                                .audioFormat("pcm")
                                .build())
                .downStream(
                        MultiModalRequestParam.DownStream.builder()
                                .voice("longxiaochun_v2")
                                .sampleRate(48000)
                                .build())
                .clientInfo(
                        MultiModalRequestParam.ClientInfo.builder()
                                .userId("1234")
                                .device(MultiModalRequestParam.ClientInfo.Device.builder()
                                        .uuid("1234")
                                        .build())
                                .build())
                .apiKey(apiKey)
                .model(model)
                .build();
    }

    /**
     * Build video channel connection request for LiveAI
     * This establishes the video streaming channel that enables visual context for AI responses
     *
     * @return UpdateParams containing video channel connection configuration
     */
    private MultiModalRequestParam.UpdateParams connectVideoChannelRequest(){

        Map<String, String> video = new HashMap<>();
        video.put("action", "connect");
        video.put("type", "voicechat_video_channel");
        ArrayList<Map<String, String>> videos = new ArrayList<>();
        videos.add(video);
        MultiModalRequestParam.BizParams bizParams = MultiModalRequestParam.BizParams.builder().videos(videos).build();

        return MultiModalRequestParam.UpdateParams.builder().bizParams(bizParams).build();
    }

    /**
     * Wait for the system to enter listening state
     */
    private void waitForListeningState() {
        while (currentState != State.DialogState.LISTENING) {
            try {
                Thread.sleep(SLEEP_INTERVAL_MS);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted while waiting for listening state", e);
            }
        }
        log.info("System entered listening state");
    }

    /**
     * Send audio data from a file to the conversation
     * @param filePath Path to the audio file
     */
    private void sendAudioFromFile(String filePath) {
        File audioFile = new File(filePath);
        
        if (!audioFile.exists()) {
            log.error("Audio file not found: {}", filePath);
            return;
        }
        
        try (AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(audioFile)) {
            byte[] audioBuffer = new byte[AUDIO_CHUNK_SIZE];
            int bytesRead;
            int totalBytesRead = 0;
            
            log.info("Starting to send audio data from: {}", filePath);
            
            // Read and send audio data in chunks
            while ((bytesRead = audioInputStream.read(audioBuffer)) != -1) {
                totalBytesRead += bytesRead;
                
                // Send audio chunk to conversation
                conversation.sendAudioData(ByteBuffer.wrap(audioBuffer, 0, bytesRead));
                
                // Add small delay to simulate real-time audio streaming
                Thread.sleep(SLEEP_INTERVAL_MS);
            }
            
            log.info("Finished sending audio data. Total bytes sent: {}", totalBytesRead);
            
        } catch (Exception e) {
            log.error("Error sending audio from file: {}", filePath, e);
        }
    }

    /**
     * Wait for conversation completion
     * @param expectedListeningTimes Expected number of listening state entries
     */
    private void waitForConversationCompletion(int expectedListeningTimes) {
        while (enterListeningTimes < expectedListeningTimes) {
            try {
                Thread.sleep(WAIT_TIMEOUT_MS);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new RuntimeException("Interrupted while waiting for conversation completion", e);
            }
        }
        log.info("Conversation completed after {} listening cycles", expectedListeningTimes);
    }

    /**
     * Stop the conversation and clean up resources
     */
    private void stopConversation() {
        try {
            if (conversation != null) {
                conversation.stop();
                Thread.sleep(1000); // Allow time for cleanup
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.warn("Interrupted while stopping conversation");
        }
    }

    /**
     * Get the callback implementation for handling conversation events
     * @return MultiModalDialogCallback instance
     */
    public static MultiModalDialogCallback getCallback() {
        return new MultiModalDialogCallbackImpl();
    }

    /**
     * Implementation of MultiModalDialogCallback for handling various conversation events
     */
    public static class MultiModalDialogCallbackImpl extends MultiModalDialogCallback {
        
        @Override
        public void onConnected() {
            log.info("WebSocket connection established");
        }

        @Override
        public void onStarted(String dialogId) {
            log.info("Dialog started with ID: {}", dialogId);
        }

        @Override
        public void onStopped(String dialogId) {
            log.info("Dialog stopped with ID: {}", dialogId);
        }

        @Override
        public void onSpeechStarted(String dialogId) {
            log.info("Speech recognition started for dialog: {}", dialogId);
        }

        @Override
        public void onSpeechEnded(String dialogId) {
            log.info("Speech recognition ended for dialog: {}", dialogId);
        }
        
        @Override
        public void onError(String dialogId, String errorCode, String errorMsg) {
            log.error("Error occurred - Dialog: {}, Code: {}, Message: {}", dialogId, errorCode, errorMsg);
            enterListeningTimes++; // Force quit dialog test on error
        }

        @Override
        public void onStateChanged(State.DialogState state) {
            log.info("Dialog state changed to: {}", state);
            currentState = state;
            
            if (currentState == State.DialogState.LISTENING) {
                enterListeningTimes++;
                log.info("Entered listening state {} times", enterListeningTimes);
            }
        }

        @Override
        public void onSpeechAudioData(ByteBuffer audioData) {
            try {
                // Write audio data to file if file writer is available
                if (fileWriterUtil != null) {
                    fileWriterUtil.Writing(audioData);
                }
            } catch (IOException e) {
                log.error("Error writing audio data to file: ", e);
                throw new RuntimeException("Failed to write audio data", e);
            }
        }

        @Override
        public void onRespondingStarted(String dialogId) {
            log.info("Response generation started for dialog: {}", dialogId);
            if (conversation != null) {
                conversation.localRespondingStarted();
            }
        }

        @Override
        public void onRespondingEnded(String dialogId, JsonObject jsonObject) {
            log.info("Response generation ended for dialog: {}", dialogId);
            if (conversation != null) {
                conversation.localRespondingEnded();
            }
        }

        @Override
        public void onRespondingContent(String dialogId, JsonObject content) {
            log.info("Response content received - Dialog: {}, Content: {}", dialogId, content);
            
            // Handle visual Q&A commands
            handleVisualQACommands(content);
        }

        @Override
        public void onSpeechContent(String dialogId, JsonObject content) {
            log.info("Speech content received - Dialog: {}, Content: {}", dialogId, content);
        }

        @Override
        public void onRequestAccepted(String dialogId) {
            log.info("Request accepted for dialog: {}", dialogId);
        }

        @Override
        public void onClosed() {
            log.info("Connection closed");
            enterListeningTimes++; // Increment to trigger test completion
        }

        /**
         * Handle visual Q&A commands from response content
         * @param content Response content containing potential commands
         */
        private void handleVisualQACommands(JsonObject content) {
            if (!content.has("extra_info")) {
                return;
            }
            
            JsonObject extraInfo = content.getAsJsonObject("extra_info");
            if (!extraInfo.has("commands")) {
                return;
            }
            
            try {
                String commandsStr = extraInfo.get("commands").getAsString();
                log.info("Processing commands: {}", commandsStr);
                
                JsonArray commands = new Gson().fromJson(commandsStr, JsonArray.class);
                
                for (JsonElement command : commands) {
                    JsonObject commandObj = command.getAsJsonObject();
                    
                    if (commandObj.has("name")) {
                        String commandName = commandObj.get("name").getAsString();
                        
                        if ("visual_qa".equals(commandName)) {
                            log.info("Visual Q&A command detected - triggering image capture");
                            
                            // Send mock image data for visual Q&A
                            MultiModalRequestParam.UpdateParams updateParams = 
                                    MultiModalRequestParam.UpdateParams.builder()
                                            .images(getMockImageRequest())
                                            .build();
                            
                            if (conversation != null) {
                                conversation.requestToRespond("prompt", "", updateParams);
                            }
                        }
                    }
                }
            } catch (Exception e) {
                log.error("Error processing visual Q&A commands: ", e);
            }
        }
    }

    /**
     * Create mock image data for testing purposes
     * @return List of image objects (URL or Base64 based on vqaUseUrl flag)
     */
    public static List<Object> getMockImageRequest() {
        List<Object> images = new ArrayList<>();
        
        try {
            JsonObject imageObject = new JsonObject();
            
            if (vqaUseUrl) {
                // Use URL-based image
                imageObject.addProperty("type", "url");
                imageObject.addProperty("value", "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7043267371/p909896.png");
                imageObject.addProperty("bucket", "bucketName");
                imageObject.add("extra", new JsonObject());
            } else {
                // Use Base64-encoded image
                imageObject.addProperty("type", "base64");
                imageObject.addProperty("value", getLocalImageBase64());
            }
            
            images.add(imageObject);
//            log.info("Created mock image data with type: {}", vqaUseUrl ? "URL" : "Base64");
            
        } catch (Exception e) {
            log.error("Error creating mock image data: ", e);
        }
        
        return images;
    }

    /**
     * Convert local image file to Base64 string
     * @return Base64-encoded image string
     */
    public static String getLocalImageBase64() {
        String imagePath = "./src/main/resources/jpeg-bridge.jpg";
        
        try (FileInputStream fileInputStream = new FileInputStream(new File(imagePath))) {
            byte[] imageBytes = new byte[fileInputStream.available()];
            fileInputStream.read(imageBytes);
            
            String base64Image = Base64.getEncoder().encodeToString(imageBytes);
            log.info("Successfully converted image to Base64, size: {} bytes", imageBytes.length);
            
            return base64Image;
            
        } catch (IOException e) {
            log.error("Error converting image to Base64: {}", imagePath, e);
            return null;
        }
    }

    /**
     * Start continuous video frame streaming for LiveAI
     */
    private void startVideoFrameStreaming() {
        log.info("Starting continuous video frame streaming for LiveAI...");

        vqaUseUrl = false;
        isVideoStreamingActive = true;

        videoStreamingThread = new Thread(() -> {
            try {
                while (isVideoStreamingActive && !Thread.currentThread().isInterrupted()) {
                    Thread.sleep(VIDEO_FRAME_INTERVAL_MS);

                    MultiModalRequestParam.UpdateParams videoUpdate =
                            MultiModalRequestParam.UpdateParams.builder()
                                    .images(getMockImageRequest())
                                    .build();

                    if (conversation != null && isVideoStreamingActive) {
                        conversation.updateInfo(videoUpdate);
                        log.debug("Video frame sent to LiveAI");
                    }
                }
            } catch (InterruptedException e) {
                log.info("Video streaming thread interrupted - stopping video stream");
                Thread.currentThread().interrupt();
            } catch (Exception e) {
                log.error("Error in video streaming thread: ", e);
            } finally {
                log.info("Video streaming thread terminated");
            }
        });

        videoStreamingThread.setDaemon(true);
        videoStreamingThread.setName("LiveAI-VideoStreaming");
        videoStreamingThread.start();

        log.info("Video streaming thread started successfully");
    }

    /**
     * Main method to run the test cases
     * Configure the required parameters before running
     */
    public static void main(String[] args) {
        log.info("############ Initializing Multi-modal Dialog Tests ############");
        
        // Configure WebSocket API URL
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
        log.info("WebSocket API URL: {}", Constants.baseWebsocketApiUrl);

        // Reset state variables
        enterListeningTimes = 0;

        // Configure test parameters (replace with actual values)
        MultiModalDialogTestCases.workspaceId = "";
        MultiModalDialogTestCases.appId = "";
        MultiModalDialogTestCases.apiKey = "";
        MultiModalDialogTestCases.model = "multimodal-dialog";
        
        // Validate configuration
        if (apiKey.isEmpty() || workspaceId.isEmpty() || appId.isEmpty()) {
            log.error("Please configure workspaceId, appId, and apiKey before running tests");
            return;
        }

        // Create test instance and run specific test
        MultiModalDialogTestCases testCases = new MultiModalDialogTestCases();
        
        try {
            // Run the desired test case
            testCases.testMultimodalPush2Talk();
            
            // Uncomment other test cases as needed:
            // testCases.testMultimodalTap2Talk();
            // testCases.testMultimodalDuplex();
            // testCases.testMultimodalTextSynthesizer();
            // testCases.testMultimodalVQA();
            // testCases.testMultimodalVQABase64();
            // testCases.testMultimodalAdjustBrightness();
            // testCases.testMultimodalAgentDJ();
            // testCases.testMultimodalLiveAI();
            
        } catch (Exception e) {
            log.error("Error running test cases: ", e);
        }
        
        log.info("############ Multi-modal Dialog Tests Completed ############");
    }
}
```

## FileWriterUtil.java

```
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;

/**
 * 文件写入工具类。
 * 支持创建文件、开始写入数据、追加写入数据和结束写入操作。
 * 使用 ByteBuffer 存储数据并将数据写入指定的文件中。
 */
public class FileWriterUtil {

    private File file;
    private FileOutputStream fos;
    private FileChannel fc;

    /**
     * 创建一个新的文件。
     *
     * @param filePath 文件路径
     */
    public void createFile(String filePath) throws IOException {
        file = new File(filePath);
        if (!file.exists()) {
            file.createNewFile();
        }

        fos = new FileOutputStream(file, true);
        fc = fos.getChannel();
    }

    /**
     * 写入数据。
     *
     * @param data 要追加的数据
     */
    public void Writing(ByteBuffer data) throws IOException {
        fc.position(fc.size());
        fc.write(data);
    }

    /**
     * 结束写入操作。
     */
    public void finishWriting() throws IOException {
        if (fc != null) {
            fc.close();
        }

        if (fos != null) {
            fos.close();
        }
    }
}
```

## **更多SDK接口使用说明**

### **VQA交互**

VQA 是对话过程中通过发送图片实现图片+语音的多模交互的功能。

核心过程是语音或者文本请求拍照意图触发**"visual\_qa"**拍照指令。

当收到拍照指令后， 发送图片链接或者base64数据（支持图片大小<180KB）。

-   建联后发起拍照请求。
    

```
@Test
  void testMultimodalVQA() {
    /*
      step1. 发送”看看前面有什么东西“，onRespondingContent 返回visual_qa 指令
      step2. 发送图片列表
      step3. 返回图片的对话结果
      */
    System.out.println("############ Start Test VQA ############");
    vqaUseUrl = true;

    log.debug("params: {}", JsonUtils.toJson(params));

    conversation = new MultiModalDialog(params, getCallback());

    conversation.start();
    while (currentState != State.DialogState.LISTENING) {
      try {
        sleep(100);
      } catch (InterruptedException e) {
        throw new RuntimeException(e);
      }
    }
    conversation.requestToRespond("prompt","拍照看看前面有什么东西",null);
    // 增加交互流程等待
    while (enterListeningTimes < 3) {
      try {
        sleep(2000);
      } catch (InterruptedException e) {
        throw new RuntimeException(e);
      }
    }
    conversation.stop();
    try {
      sleep(1000);
    } catch (InterruptedException e) {
      throw new RuntimeException(e);
    }
    System.out.println("############ End Test Push2Talk ############");
  }
```

-   处理"visual\_qa" command和上传拍照。
    

```
@Override
    public void onRespondingContent(String dialogId, JsonObject content) {
      log.info("onRespondingContent: {}, {}", dialogId, content);
      if (content.has("extra_info")) {
        JsonObject extraInfo = content.getAsJsonObject("extra_info");
        if (extraInfo.has("commands")) {
          String commandsStr = extraInfo.get("commands").getAsString();
          log.info("commandsStr: {}", commandsStr);
          //"[{\"name\":\"visual_qa\",\"params\":[{\"name\":\"shot\",\"value\":\"拍照看看\",\"normValue\":\"True\"}]}]"
          JsonArray commands = new Gson().fromJson(commandsStr, JsonArray.class);
          for (JsonElement command : commands) {
            JsonObject commandObj = command.getAsJsonObject();
            if (commandObj.has("name")) {
              String commandStr = commandObj.get("name").getAsString();
              if (commandStr.equals("visual_qa")) {
                log.info("拍照了！！！！");
                MultiModalRequestParam.UpdateParams updateParams = MultiModalRequestParam.UpdateParams.builder()
                        .images(getMockOSSImage())
                        .build();
                conversation.requestToRespond("prompt","",updateParams);
              }
            }
          }
        }
      }
    }

//上传拍照
public static List<Object> getMockOSSImage() {
    JsonObject imageObject = new JsonObject();
    JsonObject extraObject = new JsonObject();
    List<Object> images = new ArrayList<>();
    try{
      if (vqaUseUrl){
        imageObject.addProperty("type", "url");
        imageObject.addProperty("value", "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7043267371/p909896.png");
        imageObject.addProperty("bucket", "bucketName");
        imageObject.add("extra", extraObject);
      }else {
        imageObject.addProperty("type", "base64");
        imageObject.addProperty("value", getLocalImageBase64());
      }
      images.add(imageObject);

    }catch (Exception e){
      e.printStackTrace();
    }
    return images;
  }
```

### **文本合成TTS**

SDK支持通过文本直接请求服务端合成音频。

您需要在客户端处于Listening状态下发送`requestToRespond`请求。

若当前状态非Listening，需要先调用`Interrupt` 接口打断当前播报。

```
@Test
  void testMultimodalTextSynthesizer() {
    /*
      step1. 发送文本合成tts
      step2. 保存tts音频
      */
    System.out.println("############ Start Test TextSynthesizer ############");

    conversation = new MultiModalDialog(params, getCallback());

    conversation.start();
    while (currentState != State.DialogState.LISTENING) {
      try {
        sleep(100);
      } catch (InterruptedException e) {
        throw new RuntimeException(e);
      }
    }
    try {
      fileWriterUtil.createFile("./test.pcm");
    } catch (IOException e) {
      log.error(e.getMessage());
      throw new RuntimeException(e);
    }
    conversation.requestToRespond("transcript","幸福是一种技能，是你摒弃了外在多余欲望后的内心平和。",null);

    // 增加交互流程等待
    while (enterListeningTimes < 2) {
      try {
        sleep(2000);
      } catch (InterruptedException e) {
        throw new RuntimeException(e);
      }
    }
    try {
      fileWriterUtil.finishWriting();
    } catch (IOException e) {
      log.error(e.getMessage());
      throw new RuntimeException(e);
    }
    conversation.stop();

    System.out.println("############ End Test TextSynthesizer ############");
  }
```

### **通过Websocket请求LiveAI**

LiveAI （视频通话）是百炼多模交互提供的官方Agent。通过Java SDK发送图片序列的方式，可以实现视频通话的功能。 我们推荐您的服务端和客户端（网页或者APP）通过RTC传输视频和音频，然后将服务端采集到的视频帧以 500ms/张 的速度发送给SDK，同时保持实时的音频输入。

注意：LiveAI发送图片只支持base64编码，每张图片的大小在180K以下。

-   LiveAI调用时序
    

#### ![截屏2025-06-20 11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1903140571/p975541.png)

-   关键代码示例
    

完整代码请参考 [Github示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/multimodal_dialog)。

```
public void testMultimodalLiveAI() {
        log.info("############ Starting LiveAI Test ############");

        try {
            // Build request parameters for duplex mode
            MultiModalRequestParam params = buildBaseRequestParams("duplex");
            log.info("Request parameters: {}", JsonUtils.toJson(params));

            // Initialize conversation
            conversation = new MultiModalDialog(params, getCallback());
            conversation.start();

            // Start send video frame loop
            startVideoFrameStreaming();
            // Wait for listening state
            waitForListeningState();
            conversation.sendHeartBeat();
            // Send video channel connect request, will response command : switch_video_call_success
            conversation.requestToRespond("prompt", "", connectVideoChannelRequest());

            // Send audio data directly (no manual start needed for duplex)
            sendAudioFromFile("./src/main/resources/what_in_picture.wav");

            // Wait for listening state twice
            waitForListeningState();

            sendAudioFromFile("./src/main/resources/what_color.wav");

            // Wait for conversation completion
            waitForConversationCompletion(3);

            // Clean up
            stopConversation();

            isVideoStreamingActive = false;
            if (videoStreamingThread != null && videoStreamingThread.isAlive()) {
                videoStreamingThread.interrupt();
            }

        } catch (Exception e) {
            log.error("Error in LiveAI test: ", e);
        } finally {
            log.info("############ LiveAI Test Completed ############");
        }
    }

/**
     * Build video channel connection request for LiveAI
     *
     * @return UpdateParams containing video channel connection configuration
     */
    private MultiModalRequestParam.UpdateParams connectVideoChannelRequest(){

        Map<String, String> video = new HashMap<>();
        video.put("action", "connect");
        video.put("type", "voicechat_video_channel");
        ArrayList<Map<String, String>> videos = new ArrayList<>();
        videos.add(video);
        MultiModalRequestParam.BizParams bizParams = MultiModalRequestParam.BizParams.builder().videos(videos).build();

        return MultiModalRequestParam.UpdateParams.builder().bizParams(bizParams).build();
    }

/**
     * Start continuous video frame streaming for LiveAI
     */
    private void startVideoFrameStreaming() {
        log.info("Starting continuous video frame streaming for LiveAI...");

        vqaUseUrl = false;
        isVideoStreamingActive = true;

        videoStreamingThread = new Thread(() -> {
            try {
                while (isVideoStreamingActive && !Thread.currentThread().isInterrupted()) {
                    Thread.sleep(VIDEO_FRAME_INTERVAL_MS);

                    MultiModalRequestParam.UpdateParams videoUpdate =
                            MultiModalRequestParam.UpdateParams.builder()
                                    .images(getMockImageRequest())
                                    .build();

                    if (conversation != null && isVideoStreamingActive) {
                        conversation.updateInfo(videoUpdate);
                        log.debug("Video frame sent to LiveAI");
                    }
                }
            } catch (InterruptedException e) {
                log.info("Video streaming thread interrupted - stopping video stream");
                Thread.currentThread().interrupt();
            } catch (Exception e) {
                log.error("Error in video streaming thread: ", e);
            } finally {
                log.info("Video streaming thread terminated");
            }
        });

        videoStreamingThread.setDaemon(true);
        videoStreamingThread.setName("LiveAI-VideoStreaming");
        videoStreamingThread.start();

        log.info("Video streaming thread started successfully");
    }
```

### **自定义提示词变量和传值**

-   在管控台项目【提示词】配置自定义变量。
    

如下示例，定义了一个`user_name`字段代表用户昵称。并将变量`user_name`以占位符形式${user\_name} 插入到Prompt 中。

其中**自定义变量**按钮位于提示词配置页面顶部的**可引入变量**区域。

-   在代码中设置变量。
    

如下示例，设置`"user_name" = "大米"`。

```
//在请求参数构建中传入biz_params.user_prompt_params
MultiModalRequestParam.builder()
        .bizParams(
                MultiModalRequestParam.BizParams.builder()
                        .userPromptParams(setUserPromptParams())
                        .build())
        .apiKey(apiKey)
        .model(model)
        .build();   
private HashMap<String, String> setUserPromptParams() {
        HashMap<String, String> promptSettings = new HashMap<>();
        promptSettings.put("user_name", "大米");
        return promptSettings;
    }
```

-   请求回复
    

智能体在响应中使用**亲爱的大米**称呼用户，例如："亲爱的大米，今天你哪里的天气让你关心呢？"，表明 `user_name` 变量已成功传入并在 Prompt 中生效。

### **ASR结果即时纠错**

在对话过程中，ASR 识别结果有可能出现错误或者非预期的结果。 除了配置热词之外，您也可以通过即时纠错功能接口上传词表进行实时干预。

-   参数说明。
    

通过配置UpStream的AsrPostProcessing 参数来配置纠错词表。

参数

一级参数

二级参数

类型

说明

AsrPostProcessing

Object

ASR 纠错词表

ReplaceWord\[\]

List

词表列表，每个ReplaceWord 对应一组词的替换规则

source

String

需要被替换的文本

target

String

替换目标文本

match\_mode

String

匹配模式，默认为exact：

**exact**：整句精确匹配，只有文本与source完全相同才匹配成功

**partial**：部分匹配，文本中部分字符与source相同即匹配成功

**说明**

注意：使用本功能 Java SDK 版本需>=2.21.14。

```
//构建AsrPostProcessing对象
MultiModalRequestParam.UpStream.AsrPostProcessing asrPostProcessing = 
MultiModalRequestParam.UpStream.AsrPostProcessing
.builder()
.replaceWords(Collections.singletonList(
        ReplaceWord.builder()
        .source("1加1")
        .target("一加一")
        .matchMode("partial")
        .build()
        ))
.build();
// 在创建对话请求时将asrPostProcessing 传入UpStream.AsrPostProcessing
```

### **更多使用示例**

请参考 [Github示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/multimodal_dialog)。
