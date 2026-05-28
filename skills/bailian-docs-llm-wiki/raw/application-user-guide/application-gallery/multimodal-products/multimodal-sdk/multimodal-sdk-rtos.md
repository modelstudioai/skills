# RTOS C SDK

本文介绍了如何使用阿里云百炼大模型服务提供的实时多模交互嵌入式端RTOS C SDK，包括SDK下载安装、关键接口及代码示例。

## **前提条件**

开通阿里云百炼实时多模交互应用，获取[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#732535cfc959h)、[APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id#2612f896detsz)和[API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

## **多模态实时交互服务接入架构**

![多模态实时交互服务接入架构-通用-流程图](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7227370571/p976841.jpg)

## **下载安装**

**序号**

**最新SDK包**

**硬件平台信息**

**MD5**

**厂商**

**芯片平台**

01

[V0.0.5-02C-20250731\_Linux.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250731/bdutul/V0.0.5-02C-20250731_Linux.tar.gz)

Linux

x86\_64

41546c75cd2c4518c3c7066a0a62817b

02

[V0.0.5-02C-20250731\_ESP32S3.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250731/kxbkjf/V0.0.5-02C-20250731_ESP32S3.tar.gz)

乐鑫

ESP32S3

3410570590862c9d767ef7586155b60b

## 接口说明

### **create\_conversation**

创建交互，设置回调。对应销毁接口为[destroy\_conversation](#e7fedc918etk7)。

```
/**
 * @brief 创建交互，设置回调。对应销毁接口为destroy_conversation
 * @param on_message : 各事件监听回调，参见下文具体回调
 * @param user_data : 回调返回
 * @return conv_instance_t : Conversation单例指针
 */
conv_instance_t create_conversation(const conv_event_callback_t on_message,
                                    void* user_data);
```

其中conv\_event\_callback\_t类型如下：

#### **conv\_event\_callback\_t SDK事件回调**

```
/**
 * @brief SDK各事件回调
 * @param conv_event_t*
 * ：回调事件，可通过调用其中具体方法获得事件及相关信息。具体方法见下方conv_event_t
 * @param void* ：用户设置的user_data
 */
typedef void (*conv_event_callback_t)(conv_event_t *, void *);
```

##### **conv\_event\_t** 成员列表

**成员**

**说明**

int status\_code;

获取状态码，正常情况为0或者20000000，失败时对应失败的错误码。错误码参考下文 [SDK错误码](#0d2aeed1571bo)。

conv\_event\_type\_t msg\_type;

获取当前所发生Event的类型，详见[conv\_event\_type\_t](#5117000896vli)。

conv\_event\_type\_t sub\_msg\_type;

获取当前所发生Event的子类型，当msg\_type为CONV\_EVENT\_RTC\_MESSAGE时使用。Websocket模式下可不关注。

char\* msg;

获得此conv\_event\_type\_t的完整json格式response。

char task\_id\[64\];

获取任务的task id，定位问题建议用dialog\_id。

char dialog\_id\[64\];

获取会话的dialog id。

unsigned char\* binary\_data;

获取云端返回的二进制数据。当msg\_type为[CONV\_EVENT\_BINARY](#c4777bfbb5wji)时使用。

unsigned int binary\_data\_bytes;

获得这一次二进制数据的字节数。当msg\_type为[CONV\_EVENT\_BINARY](#c4777bfbb5wji)时使用。

dialog\_state\_changed\_t dialog\_state;

获得对话当前状态，当msg\_type为[CONV\_EVENT\_DIALOG\_STATE\_CHANGED](#f2b88903842po)时使用。

```
typedef enum {
  DIALOG_STATE_NONE = -1,
  DIALOG_STATE_IDLE = 0,
  DIALOG_STATE_LISTENING,
  DIALOG_STATE_RESPONDING,
  DIALOG_STATE_THINKING
} dialog_state_changed_t;
```

###### **conv\_event\_type\_t 事件类型**

**事件名称**

**事件说明**

CONV\_EVENT\_CONVERSATION\_FAILED

会话任务发生错误。收到此事件后需要根据错误信息判断如何处理，也可以使用此dialog\_id重新连接，继续会话。

CONV\_EVENT\_CONVERSATION\_CONNECTED

与AI服务建连成功。

CONV\_EVENT\_CONVERSATION\_STARTED

AI（服务端）登场, 会话任务成功启动，可以开始语音对话。

CONV\_EVENT\_CONVERSATION\_COMPLETED

AI（服务端）退场，语音对话停止。

CONV\_EVENT\_SPEECH\_STARTED

HUMAN开始说话。PushToTalk模式按键则触发此事件，TapToTalk和Duplex模式是用户开始说话触发此事件。

CONV\_EVENT\_SPEECH\_ENDED

HUMAN说话结束。PushToTalk模式按键松开则触发此事件，TapToTalk和Duplex模式是用户说话结束触发此事件。

CONV\_EVENT\_RESPONDING\_STARTED

AI（服务端）开始传送TTS数据。这时需要打开播放器。

CONV\_EVENT\_RESPONDING\_ENDED

AI（服务端）TTS数据合成完成且接收完成。此事播放器仍然在播放，不可把此事件当成播放结束。

CONV\_EVENT\_BINARY

表示此事件消息中包含AI(服务端)传回的TTS数据包。

CONV\_EVENT\_SOUND\_LEVEL

最近一次传入的HUMAN说话声音数据的音量值。

CONV\_EVENT\_DIALOG\_STATE\_CHANGED

对话状态发生变化。

CONV\_EVENT\_INTERRUPT\_ACCEPTED

AI（服务端）接收按键请求（如打断）。这个时候需要停止正在运行的播放器。

CONV\_EVENT\_INTERRUPT\_DENIED

AI（服务端）拒绝按键请求（如打断）。

CONV\_EVENT\_VOICE\_INTERRUPT\_ACCEPTED

AI（服务端）接收语音请求（如打断）。这个时候需要停止正在运行的播放器。

CONV\_EVENT\_VOICE\_INTERRUPT\_DENIED

AI（服务端）拒绝语音请求（如打断）。

CONV\_EVENT\_CONNECTION\_CONNECTED

SDK与服务端链接。

CONV\_EVENT\_CONNECTION\_DISCONNECTED

SDK与服务端断开链接。

CONV\_EVENT\_SPEECH\_CONTENT

用户语音识别出的详细信息，比如文本。

CONV\_EVENT\_RESPONDING\_CONTENT

系统对外输出的详细信息，比如LLM大模型返回的结果。

CONV\_EVENT\_NETWORK\_STATUS

网络状态信息, 比如网络延迟。

CONV\_EVENT\_OTHER\_MESSAGE

未定义消息。

CONV\_EVENT\_RTC\_MESSAGE

表示将事件整理成RTC消息。当前仅支持Websocket模式，可不关注。

### **destroy\_conversation**

销毁交互。对应创建接口为[create\_conversation](#)。

```
/**
 * @brief 销毁交互，若交互进行中，则内部完成conversation_disconnect
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t destroy_conversation();
```

### **conversation\_connect**

组装一个start请求，用于发起对服务端的链接。返回成功并不代表与语音对话服务链接成功，仅代表发起Start请求构建成功，是否链接成功以返回的Response为准。

```
/**
 * @brief 与服务端建立链接
 * @param params ：json string形式的初始化参数
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t conversation_connect(const char* params);
```

#### **参数设置说明**

**一级参数**

**二级参数**

**三级参数**

**类型**

**必须**

**说明**

apikey

String

是

临时凭证，具体请查看[获取API Key](https://help.aliyun.com/zh/model-studio/get-api-key)。

url

String

是

请求的网关域名，百炼请求域名："wss://dashscope.aliyuncs.com/api-ws/v1/inference"。

chain\_mode

int

是

默认0，启用Websocket交互方式。目前仅支持Websocket交互方式。

app\_id

String

是

客户在管控台创建的应用id，可以根据值规律确定使用哪个对话系统。详见[APP ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。

workspace\_id

String

是

用户业务空间id。详见[Workspace ID](https://help.aliyun.com/zh/model-studio/obtain-the-app-id-and-workspace-id)。

mode

String

否

运行模式，目前支持"push2talk"和"tap2talk"。

log\_level

int

否

日志级别，默认INFO级别。

```
typedef enum {
  CONV_LOG_LEVEL_VERBOSE,
  CONV_LOG_LEVEL_DEBUG,
  CONV_LOG_LEVEL_INFO,
  CONV_LOG_LEVEL_WARNING,
  CONV_LOG_LEVEL_ERROR,
  CONV_LOG_LEVEL_NONE
} conv_log_level_t;
```

upstream

JSONObject

是

type

String

是

上行类型：

AudioOnly 仅语音通话；

AudioAndVideo 上传视频。

mode

String

否

运行模式，目前支持"push2talk"和"tap2talk"。此upstream.mode须与mode一致。

sample\_rate

int

否

上行语音的采样率，支持范围：

-   8000
    
-   16000
    
-   24000
    
-   48000
    

默认为16000。

audio\_format

String

否

上行音频格式，支持pcm、opus和raw-opus。用户送入的音频参数必须为单通道、16bit。

-   pcm：pcm格式。
    
-   opus：Ogg封装的Opus编码格式。
    
-   raw-opus：无Ogg封装的裸Opus。
    

downstream

JSONObject

否

type

String

否

下行媒体类型：

Text：不需要下发语音；

Audio：输出语音，默认值。

voice

String

否

合成语音的音色，支持范围取决于用户在管控台选择的tts模型。具体选择范围可参考[Python SDK](https://help.aliyun.com/zh/model-studio/cosyvoice-python-sdk#fbe0209896w38)。

sample\_rate

int

否

合成语音的采样率，支持范围：

-   16000
    
-   24000
    
-   48000
    

默认为24000。

audio\_format

String

否

下行音频格式，默认为pcm，可设置pcm、mp3、opus、raw-opus、raw-opus2、raw-opu和raw-opu2。用户接收到的音频参数为单通道、16bit。

-   pcm：pcm格式。
    
-   mp3：mp3格式。
    
-   opus：Ogg封装的Opus编码格式。
    
-   raw-opus：无Ogg封装的裸Opus，首包含Opus音频头部信息。
    
-   raw-opus2：无Ogg封装的裸Opus，不含Opus音频头部信息。
    
-   raw-opu：无Ogg封装的裸Opus，首包含Opus音频头部信息，且每包数据的头2个字节记录此包真实数据字节数。
    
-   raw-opu2：无Ogg封装的裸Opus，不含Opus音频头部信息，且每包数据的头2个字节记录此包真实数据字节数。
    

注意：由于SDK内部无解码能力，需用户自行处理接收到的音频数据。

volume

int

否

合成音频的音量，取值范围0-100，默认50。

speech\_rate

int

否

合成音频的语速，取值范围50-200，表示默认语速的50%-200%，默认100。

pitch\_rate

int

否

合成音频的声调，取值范围50-200，默认100。

frame\_size

int

否

合成音频的帧大小，单位为毫秒。仅在downstream.audio\_format为opus、raw-opus、raw-opus2、raw-opu、raw-opu2时生效。

取值范围：10、20、40、60、100、120。默认为60。

intermediate\_text

String

否

控制返回给用户哪些中间文本：

-   transcript：返回用户语音识别结果
    
-   dialog：返回对话系统回答中间结果
    

可以设置多种，以逗号分隔，默认为transcript。

transmit\_rate\_limit

int

否

合成音频发送速率限制，单位：字节每秒。默认无限制。

client\_info

JSONObject

是

user\_id

String

是

终端用户ID，客户根据自己业务规则生成，用来针对不同终端用户实现定制化功能。

device

JSONObject

否

uuid

String

否

客户端全局唯一的ID，需要用户自己生成，传入SDK。

network

JSONObject

否

ip

String

否

调用方公网IP。

location

JSONObject

否

latitude

String

否

调用方纬度信息，在需要客户端精确位置的业务场景提交。

longitude

String

否

调用方经度信息，在需要客户端精确位置的业务场景提交。

city\_name

String

否

调用方所在城市，指明客户端粗略位置。

biz\_params

JSONObject

否

user\_defined\_params

JSONObject

否

其他需要透传给agent的参数。

user\_defined\_tokens

JSONObject

否

透传agent所需鉴权信息。

user\_prompt\_params

JSONObject

否

用于设置用户自定义prompt中的变量。

user\_query\_params

JSONObject

否

用于设置用户自定义query中的变量。

### **conversation\_disconnect**

组装一个stop请求，用于发送指令告诉服务端中止链接。返回成功并不代表与VoiceChat Server断链成功，仅代表发起stop请求构建成功，是否断链成功以返回的Response为准。

```
/**
 * @brief 断开链接
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t conversation_disconnect();
```

### **conversation\_interrupt**

打断交互，使AI进入听状态。

```
/**
 * @brief 按键(Tap)打断。正在播放时，调用此接口请求打断播放。
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t conversation_interrupt();
```

### conversation\_send\_audio\_data

推送实时采集的音频数据。

```
/**
 * @brief 推送音频数据
 * @param data : 音频数据，PCM格式
 * @param data_size : 音频数据字节数
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t conversation_send_audio_data(const uint8_t* data,
                                             size_t data_size);
```

### **conversation\_send\_ref\_data**

推送参考音频数据，在音频数据送给播放器时推送。暂不启用此接口。

```
/**
 * @brief 推送参考音频数据，在音频数据送给播放器时推送
 * @param data : 音频数据，PCM格式
 * @param data_size : 音频数据字节数
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t conversation_send_ref_data(const uint8_t* data,
                                           size_t data_size);
```

### **conversation\_send\_response\_data**

Listening/Idle状态下，通知服务端与用户主动交互，可以直接把上传的文本转换为语音下发，也可以上传文本调用大模型，返回的结果再转换为语音下发。

```
/**
 * @brief
 * 通知服务端与用户主动交互，可以直接把上传的文本转换为语音下发，也可以上传文本调用大模型，返回的结果再转换为语音下发
 * @param params ：json string形式的初始化参数
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t conversation_send_response_data(const char* params);
```

#### **params参数设置**

**参数**

**类型**

**必须**

**说明**

type

String

是

服务应该采取的交互类型：

transcript 表示直接把文本转语音

prompt 表示把文本送大模型回答

text

String

是

要处理的文本，可以是""空字符串，非null即可

parameters

JSONObject

否

-   parameters.images
    

JSONArray

否

需要分析的图片信息，图片数据以base64编码的形式传入。格式参考下方示例。

-   parameters.biz\_params
    

JSONArray

否

与Start消息中biz\_params相同，传递对话系统自定义参数。RequestToRespond的biz\_params参数只在本次请求中生效。

#### **parameters示例**

```
{
  	"text": "今天天气怎么样？",
	"type": "transcript",
	"parameters": {
		"biz_params": {
			"user_defined_params": {},
			"videos": [{
				"action": "connect",
				"type": "voicechat_video_channel"
			}, {
				"action": "exit",
				"type": "voicechat_video_channel"
			}]
		},
		"images": [{
			"type": "base64",
			"value": "base64String"
		}]
	}
}
```

### **conversation\_update\_message**

此接口为万能接口，可更新内部参数，或者直接发送定制事件，如UpdateInfo。

```
/**
 * @brief 发送如P2T相关的参数
 * @param params : 参数
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t conversation_update_message(const char* params);
```

#### **发送参数（UpdateInfo）**

##### **百炼协议参数**

**参数**

**类型**

**必须**

**说明**

type

String

是

update\_info

parameters

JSONObject

是

-   parameters.images
    

JSONArray

否

图片数据

-   parameters.client\_info
    

JSONObject

否

-   parameters.client\_info.status
    

JSONObject

否

客户端当前状态

-   parameters.biz\_params
    

JSONObject

否

与Start消息中biz\_params相同，传递对话系统自定义参数

##### **百炼协议示例**

```
{
  	"type": "update_info",
	"parameters": {
		"biz_params": {},
		"client_info": {
			"status": {
				"bluetooth_announcement": {
					"status": "stopped"
				}
			}
		},
		"images": [{
			"type": "base64",
			"value": "base64String"
		}]
	}
}
```

#### **发送万能参数**

```
{
	"type": "update_custom_message",
	"header": {
		"TEST1": "XXX"
	},
	"payload": {
		"TEST2": "YYY"
	}
}
返回的对应消息
{
	"header": {
		"TEST1": "XXX",
		"dialog_id": "2b9bea3d2b2749a0808bae06a9da493c",
		"namespace": "VoiceChat",
		"request_id": "c48cfe7bbadd485db2e387136ce6608c",
		"task_id": "fffffff707fe4c288869931b0eeeeeee"
	},
	"payload": {
		"TEST2": "YYY"
	}
}
```

### **conversation\_set\_action**

需要有一个音频（播放）开始/结束事件告知到SDK。

```
/**
 * @brief 触发SDK动作，比如音频（播放）开始/结束事件告知到SDK
 * @param action : 触发的动作类型
 * @param data : 此次SDK动作附带的数据, 比如音频数据比如json字符串
 * @param data_size : 此次SDK动作附带的数据的字节数
 * @return conv_ret_code_t : 状态码
 */
conv_ret_code_t conversation_set_action(conv_action_t action,
                                        const uint8_t* data, size_t data_size);
```

#### **conv\_action\_t**

**枚举名**

**说明**

ACTION\_MIC\_STARTED

MIC开始工作

ACTION\_MIC\_STOPPED

MIC停止录音

ACTION\_PLAYER\_STARTED

开始播放

ACTION\_PLAYER\_STOPPED

播放完毕。注意：需确保播放器中缓存数据全部播放完毕后给出，否则会导致自打断或播放数据进入 ASR。

ACTION\_ENABLE\_VOICE\_INTERRUPTION

开启语音打断功能

ACTION\_DISABLE\_VOICE\_INTERRUPTION

关闭语音打断功能

ACTION\_VOICE\_MUTE

语音静音。若正在AI听阶段，则主动告知AI，用户已经说完话。

ACTION\_VOICE\_UNMUTE

语音静音关闭

ACTION\_START\_HUMAN\_SPEECH

仅在push2talk模式有效, 表示用户开始说话

ACTION\_STOP\_HUMAN\_SPEECH

仅在push2talk模式有效, 表示用户说话完毕

ACTION\_CANCEL\_HUMAN\_SPEECH

仅在push2talk模式有效, 表示用户说话取消

### **conversation\_get\_state**

获得当前各种状态。

```
/**
 * @brief 获得当前状态
 * @param type : 状态类型
 * @return conv_ret_code_t : 状态码
 */
int conversation_get_state(state_type_t type);
```

#### **state\_type\_t**

**枚举名**

**说明**

STATE\_TYPE\_DIALOG\_STATE

对话（AI）当前状态，枚举值为dialog\_state\_changed\_t

STATE\_TYPE\_CONNECTION\_STATE

链接状态

STATE\_TYPE\_MIC\_STATE

MIC当前状态

STATE\_TYPE\_PLAYER\_STATE

PLAYER当前状态

#### dialog\_state\_changed\_t

**枚举名**

**说明**

DIALOG\_STATE\_IDLE

当前处于空闲未工作状态

DIALOG\_STATE\_LISTENING

AI（服务端）处于听状态，接收用户输入数据（如MIC音频数据）。

DIALOG\_STATE\_RESPONDING

AI（服务端）处于反馈状态，送出AI的数据（如TTS音频数据）。

DIALOG\_STATE\_THINKING

AI（服务端）处于思考阶段。

## **代码示例**

### **语音对话初始化**

这一步通过设置回调函数来接收交互过程中的所有事件，包括对话状态、对话结果等。

```
void event_callback(conv_event_t* event, void* param) {
  if (event->msg_type == CONV_EVENT_BINARY) {
    // 写入缓存或直接进行播放
  } else {
    printf("== %s ==\n", get_conv_event_type_string(event->msg_type));
    if (event->msg_type == CONV_EVENT_DIALOG_STATE_CHANGED) {
      // 可通过对话状态event->dialog_state进行相关业务逻辑操作
      printf("- DIALOG_STATE_CHANGED: %s -\n",
          get_dialog_state_changed_string(event->dialog_state));
    } else if (event->msg_type == CONV_EVENT_RESPONDING_STARTED) {
      // 后续将接收语音合成数据, 这里可启动播放器。
      // 播放器启动后需要通知SDK
      // conversation_set_action(ACTION_PLAYER_STARTED, NULL, 0);
    } else if (event->msg_type == CONV_EVENT_RESPONDING_ENDED) {
      // 接收语音合成数据完成, 这里需要通知播放器已经送完数据。
      // 注意, 这里只是接收完语音合成数据, 而非播放完成, 缓存或播放器中还有大量数据待播放。
      // 完全播放完后必须通知SDK
      // conversation_set_action(ACTION_PLAYER_STOPPED, NULL, 0);
    } else if (event->msg_type == CONV_EVENT_SPEECH_CONTENT ||
               event->msg_type == CONV_EVENT_RESPONDING_CONTENT) {
      cJSON* response_json = cJSON_Parse(event->msg);
      if (response_json != NULL) {
        cJSON* payload = cJSON_GetObjectItem(response_json, "payload");
        if (payload == NULL) {
          goto OUT_CONTENT;
        }
        cJSON* output = cJSON_GetObjectItem(payload, "output");
        if (output == NULL) {
          goto OUT_CONTENT;
        }
        cJSON* text = cJSON_GetObjectItem(output, "text");
        if (text == NULL) {
          goto OUT_CONTENT;
        }
        printf("%s: %s\n",
               event->msg_type == CONV_EVENT_SPEECH_CONTENT ? "HUMAN" : "AI",
                 text->valuestring);

      OUT_CONTENT:
        cJSON_Delete(response_json);
      }
    } else if (event->msg_type == CONV_EVENT_INTERRUPT_ACCEPTED) {
      // 允许打断, 这里可以关闭正在播放的音频
    } else if (event->msg_type == CONV_EVENT_CONVERSATION_FAILED ||
               event->msg_type == CONV_EVENT_CONNECTION_DISCONNECTED ||
               event->msg_type == CONV_EVENT_CONVERSATION_COMPLETED) {
      // 对话中止, 进行相关业务逻辑操作
    }

    // 可通过接收到的事件event->msg_type进行相关业务逻辑操作
  }
}

// 创建语音对话单例, SDK内部管理此单例
create_conversation(event_callback, NULL);
```

### **语音对话发起建连**

建连参数把包括账号信息以json的形式构建，具体参考接口文档。PushToTalk模式下，建连成功后对话状态处于Idle状态。

```
const char* genInitParams() {
  cJSON* root = cJSON_CreateObject();
  
  cJSON_AddStringToObject(root, "apikey", "sk-");
  cJSON_AddStringToObject(root, "url", CONFIG_DEFAULT_URL);
  
  cJSON_AddStringToObject(root, "app_id", "user_app_id");
  cJSON_AddStringToObject(root, "workspace_id", "user_workspace_id");
  
  cJSON_AddStringToObject(root, "model", CONFIG_DEFAULT_PROTOCOL_MODEL);

  cJSON_AddNumberToObject(root, "chain_mode", CONFIG_DEFAULT_CONV_CHAIN_MODE);
  cJSON_AddNumberToObject(root, "ws_protocol_ver",
                          CONFIG_DEFAULT_WS_PROTOCOL_VER);
  cJSON_AddStringToObject(root, "mode", CONFIG_DEFAULT_CONV_SERVICE_MODE);
  cJSON_AddStringToObject(root, "task_group",
                          CONFIG_DEFAULT_PROTOCOL_TASK_GROUP);
  cJSON_AddStringToObject(root, "task", CONFIG_DEFAULT_PROTOCOL_TASK);
  cJSON_AddStringToObject(root, "function", CONFIG_DEFAULT_PROTOCOL_FUNCTION);
  cJSON_AddNumberToObject(root, "log_level", CONV_LOG_LEVEL_VERBOSE);

  cJSON* upstream = cJSON_CreateObject();
  cJSON_AddStringToObject(upstream, "type", CONFIG_DEFAULT_UPSTREAM_TYPE);
  cJSON_AddStringToObject(upstream, "mode", CONFIG_DEFAULT_CONV_SERVICE_MODE);
  cJSON_AddStringToObject(upstream, "audio_format",
                          CONFIG_DEFAULT_RECORDER_FORMAT);
  cJSON_AddItemToObject(root, "upstream", upstream);

  cJSON* downstream = cJSON_CreateObject();
  cJSON_AddStringToObject(downstream, "type", CONFIG_DEFAULT_DOWNSTREAM_TYPE);
  cJSON_AddStringToObject(downstream, "audio_format",
                          CONFIG_DEFAULT_PLAYER_FORMAT);
  cJSON_AddStringToObject(downstream, "voice", "longcheng_v2");
  cJSON_AddStringToObject(downstream, "intermediate_text",
                          CONFIG_DEFAULT_DOWNSTREAM_INTERMEDIATE_TEXT);
  cJSON_AddItemToObject(root, "downstream", downstream);

  cJSON* client_info = cJSON_CreateObject();
  cJSON_AddStringToObject(client_info, "user_id", "empty_user_id");
  cJSON_AddItemToObject(root, "client_info", client_info);

  cJSON* dialog_attributes = cJSON_CreateObject();
  cJSON_AddStringToObject(dialog_attributes, "prompt",
                          CONFIG_DEFAULT_DIALOG_ATTRIBUTES_PROMPT);
  cJSON_AddItemToObject(root, "dialog_attributes", dialog_attributes);

  char* result_json = cJSON_Print(root);
  cJSON_Delete(root);

  return result_json;
}

// 发起建连, 可通过返回值判断是否建连成功。
// 若建连失败可通过返回值和回调信息进行判断。
conv_ret_code_t ret = conversation_connect(genInitParams());
```

### **PushToTalk模式用户开始说话**

对话状态处于Idle状态时调用此接口，对话状态进入Listening。若对话状态处于Responding和Thinking，则打断当前状态重新进入Listening。调用接口成功后，用户所说的话持续送给服务端进行交互，直到停止。

```
conv_ret = conversation_set_action(ACTION_START_HUMAN_SPEECH, NULL, 0);
```

### **PushToTalk模式用户结束说话**

用户所说的话持续送给服务端进行交互，直到调用此接口，AI将根据用户所说的话进行对应的反馈。

```
conv_ret = conversation_set_action(ACTION_STOP_HUMAN_SPEECH, NULL, 0);
```

### **文本合成TTS**

SDK支持通过文本直接请求服务端合成音频。

您需要在客户端处于Listening状态下发送conversation\_send\_response\_data()请求。

若当前状态非Listening，需要先调用conversation\_interrupt()接口打断当前播报。

```
cJSON *root = cJSON_CreateObject();
cJSON_AddItemToObject(root, "text", cJSON_CreateString("幸福是一种技能，是你摒弃了外在多余欲望后的内心平和。"));
cJSON_AddItemToObject(root, "type", cJSON_CreateString("transcript"));
char *json_str = cJSON_PrintUnformatted(root);

conv_ret_code_t ret = conversation_send_response_data(json_str);

cJSON_Delete(root);
free(json_str);
```

### **VQA交互发送图片实现多模交互**

VQA 是在对话过程中通过发送图片实现图片+语音的多模交互的功能。

核心过程是语音或者文本通过conversation\_send\_response\_data()接口发送多模交互指令。

```
cJSON *root = cJSON_CreateObject();

cJSON_AddItemToObject(root, "text", cJSON_CreateString("看看图片里是什么？"));
cJSON_AddItemToObject(root, "type", cJSON_CreateString("prompt"));

cJSON *parameters = cJSON_CreateObject();
cJSON_AddItemToObject(root, "parameters", parameters);

cJSON *biz_params = cJSON_CreateObject();
cJSON_AddItemToObject(parameters, "biz_params", biz_params);

cJSON *user_defined_params = cJSON_CreateObject();
cJSON_AddItemToObject(biz_params, "user_defined_params", user_defined_params);

cJSON *videos = cJSON_CreateArray();
cJSON_AddItemToObject(biz_params, "videos", videos);

// video1: 进入视频模式
cJSON *video1 = cJSON_CreateObject();
cJSON_AddItemToObject(video1, "action", cJSON_CreateString("connect"));
cJSON_AddItemToObject(video1, "type", cJSON_CreateString("voicechat_video_channel"));
cJSON_AddItemToArray(videos, video1);

// video2: 退出视频模式
cJSON *video2 = cJSON_CreateObject();
cJSON_AddItemToObject(video2, "action", cJSON_CreateString("exit"));
cJSON_AddItemToObject(video2, "type", cJSON_CreateString("voicechat_video_channel"));
cJSON_AddItemToArray(videos, video2);

cJSON *images = cJSON_CreateArray();
cJSON_AddItemToObject(parameters, "images", images);

// 这里演示两种上传base64数据和url的形式
// image1: base64
cJSON *image1 = cJSON_CreateObject();
cJSON_AddItemToObject(image1, "type", cJSON_CreateString("base64"));
cJSON_AddItemToObject(image1, "value", cJSON_CreateString("xxxxxxxx"));
cJSON_AddItemToArray(images, image1);
// image2: url
cJSON *image2 = cJSON_CreateObject();
cJSON_AddItemToObject(image2, "type", cJSON_CreateString("url"));
cJSON_AddItemToObject(image2, "value", cJSON_CreateString("https://xxxx"));
cJSON_AddItemToArray(images, image2);

char *json_str = cJSON_PrintUnformatted(root);
    
conv_ret_code_t ret = conversation_send_response_data(json_str);

cJSON_Delete(root);
free(json_str);
```

### **LiveAI交互发送图片实现多模交互**

若使用此功能，需要Connect()入参中upstream.type设置为AudioAndVideo，即通过UpdateInfo接口持续发送图片数据来实现图片+语音的多模交互。图片大小只支持720p、480p。视频模式每500ms传一次。

```
// 发送图片base64数据的示例
const char *base64_content = "xxxxxxxx";

cJSON *root = cJSON_CreateObject();
cJSON_AddItemToObject(root, "type", cJSON_CreateString("update_info"));

cJSON *parameters = cJSON_CreateObject();
cJSON_AddItemToObject(root, "parameters", parameters);

cJSON *biz_params = cJSON_CreateObject();
cJSON_AddItemToObject(parameters, "biz_params", biz_params);

cJSON *client_info = cJSON_CreateObject();
cJSON_AddItemToObject(parameters, "client_info", client_info);
cJSON *bluetooth_announcement = cJSON_CreateObject();
cJSON_AddItemToObject(bluetooth_announcement, "status", cJSON_CreateString("stopped"));
cJSON *status = cJSON_CreateObject();
cJSON_AddItemToObject(status, "bluetooth_announcement", bluetooth_announcement);
cJSON_AddItemToObject(client_info, "status", status);

cJSON *images = cJSON_CreateArray();
cJSON_AddItemToObject(parameters, "images", images);

cJSON *image = cJSON_CreateObject();
cJSON_AddItemToObject(image, "type", cJSON_CreateString("base64"));
cJSON_AddItemToObject(image, "value", cJSON_CreateString(base64_content));
cJSON_AddNumberToObject(image, "width", 480);
cJSON_AddNumberToObject(image, "height", 720);
cJSON_AddItemToArray(images, image);

char *json_str = cJSON_PrintUnformatted(root);

conv_ret_code_t ret = conversation_update_message(json_str);

cJSON_Delete(root);
free(json_str);
```

### **自定义提示词变量和传值**

-   在管控台项目【提示词】配置自定义变量。
    

如下图示例，定义了一个`user_name`字段代表用户昵称。并将变量`user_name`以占位符形式${user\_name} 插入到Prompt 中。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5309552571/p983098.png)

-   在代码中设置变量。
    

如下示例，设置`"user_name" = "大米"`。

```
/* 以下示例在<语音对话发起建连>的示例上, 新增传入参数biz_params */
const char* genInitParams() {
  /* 其他初始化参数不再赘述, 请看<语音对话发起建连> */

  cJSON* biz_params = cJSON_CreateObject();
  cJSON_AddStringToObject(biz_params, "user_name", "大米");
  cJSON_AddItemToObject(root, "biz_params", biz_params);
  
  char* result_json = cJSON_Print(root);
  cJSON_Delete(root);

  return result_json;
}

// 发起建连, 可通过返回值判断是否建连成功。
// 若建连失败可通过返回值和回调信息进行判断。
conv_ret_code_t ret = conversation_connect(genInitParams());
```

### **语音对话结束**

```
conv_ret ret = conversation_disconnect();
```

### **语音对话释放**

```
conv_ret ret = destroy_conversation()
```

## **SDK错误码**

**枚举值**

**枚举**

**说明**

0

CONV\_SUCCESS

10

CONV\_ERR\_DEFAULT

默认错误，表示未定义的错误类型。

11

CONV\_ERR\_MEM\_ALLOC\_FAILED

内存分配失败。

12

CONV\_ERR\_JSON\_PARSE\_FAILED

JSON解析失败。

13

CONV\_ERR\_DEAD\_LOCK

内部发生死锁。

14

CONV\_ERR\_TRY\_AGAIN

请再次尝试。

15

CONV\_ERR\_NOT\_FOUND

未发现资源。

16

CONV\_ERR\_BUSY

系统处于忙碌。

50

CONV\_ERR\_INIT\_FAILED

初始化为不支持的模式。

51

CONV\_ERR\_NOT\_CONNECTED

链接失败，如联网超时等。

52

CONV\_ERR\_ENGINE\_NULL

交互引擎未创建，不可使用。

53

CONV\_ERR\_ILLEGAL\_PARAM

设置参数非法。

54

CONV\_ERR\_ILLEGAL\_INIT\_PARAM

初始化参数非法。

55

CONV\_ERR\_INVALID\_STATE

当前交互状态无法调用此接口。

56

CONV\_ERR\_HAS\_INVOKED

已经调用了此接口。

57

CONV\_ERR\_NOT\_CREATE\_CONVERSATION

还未创建会话即未调用create\_conversation()就开始操作。

58

CONV\_ERR\_SKIP\_SEND\_DATA

当前交互状态忽略此次音频。

59

CONV\_ERR\_SEND\_DATA\_FAILED

发送音频失败。

60

CONV\_ERR\_INVALID\_AUDIO\_DATA

无效音频。

61

CONV\_ERR\_STOP\_FAILED

stop()失败，如调用超时。

62

CONV\_ERR\_CANCEL\_FAILED

cancel()失败，如调用超时。

63

CONV\_ERR\_INVOKE\_TIMEOUT

接口调用超时。

64

CONV\_ERR\_REQUEST\_DENIED

打断请求拒绝。

65

CONV\_ERR\_REQUEST\_ACCEPTED

允许打断请求。

66

CONV\_ERR\_SKIP\_DESTROY\_CONVERSATION

当前SDK未创建，跳过释放操作。

67

CONV\_ERR\_INVOKE\_INVALID\_ACTION

SetAction()调用错误事件。

200

CONV\_ERR\_EMPTY\_CONV\_ERR\_EVENT

非法ConvEvent事件。

201

CONV\_ERR\_INVALID\_CONV\_ERR\_EVENT\_MSG\_TYPE

非法的ConvEvent事件类型。

301

CONV\_ERR\_SERVER\_NOT\_ACCESS

链接服务端失败，比如服务端不可链接，dns不可解析等。

310

CONV\_ERR\_NO\_SUPPORT\_MODE

不支持的服务端交互协议。

311

CONV\_ERR\_JSON\_FORMAT\_ERROR

接收到服务端返回的消息不符合json格式。

312

CONV\_ERR\_SSL\_ERROR

SSL失败，比如握手失败。

313

CONV\_ERR\_SSL\_CONNECT\_FAILED

SSL链接失败。

350

CONV\_ERR\_REQ\_IS\_NULLPTR

服务请求为空，表示当前交互状态错误。

351

CONV\_ERR\_REQ\_INVOKE\_TIMEOUT

向服务端发送请求操作超时。

352

CONV\_ERR\_REQ\_START\_FAILED

向服务端发送建立会话请求失败，常为网络问题。

353

CONV\_ERR\_REQ\_STOP\_FAILED

向服务端发送停止会话请求失败，常为网络问题。

354

CONV\_ERR\_REQ\_CANCEL\_FAILED

向服务端发送停止会话请求失败，常为网络问题。

355

CONV\_ERR\_REQ\_START\_INBOUND\_FAILED

向服务端发送启动对话任务请求失败，常为网络问题。

358

CONV\_ERR\_REQ\_CANCEL\_BOUND\_FAILED

向服务端发送停止对话任务请求失败，常为网络问题。

359

CONV\_ERR\_REQ\_SET\_PARAMS\_FAILED

设置请求参数错误，比如设置token无效。

360

CONV\_ERR\_REQ\_SEND\_AUDIO\_FAILED

向服务端发送音频数据失败，常为网络问题。

361

CONV\_ERR\_REQ\_CONTROL\_FAILED

UpdateInfo等向服务端发送指令失败。

* * *

## **时序图说明**

### **push2talk**

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7553460571/p964952.png)

### **tap2talk**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2310834571/p992231.png)
