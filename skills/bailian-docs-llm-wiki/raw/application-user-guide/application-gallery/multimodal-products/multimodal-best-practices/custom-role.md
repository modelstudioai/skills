# 自定义对话角色实践

本文档系统阐述多模态自定义对话角色配置标准及多角色切换流程，核心内容包括：自定义变量、编写角色 prompt、选配音色、维护用户与角色的映射关系。

## **概述**

多模态交互套件支持用户级别的多角色切换，通过为不同角色配置独立的提示词（prompt）和音色（voice），实现同一应用内多人设的个性化交互体验。本文档基于多模态套件能力，描述自定义多角色的最佳实践，涵盖自定义角色配置、切换时机及完整实现流程。整体分为两个阶段：

1.  **自定义角色配置**：在控制台配置自定义变量，编写角色 prompt，并为角色选配音色。
    
2.  **多角色切换**：客户端维护用户与角色的映射关系，切换时重建 WebSocket 连接。
    

**重要**

voice（音色）与 user\_prompt\_params（提示词自定义变量）属于连接级参数，必须在建联阶段的首帧 run-task 指令中传入。切换角色或音色需要重新建立 WebSocket 连接，系统不支持在同一个网络连接内进行动态热切换。

## **步骤一：自定义角色配置**

自定义一个角色需要完成三件事：配置变量、编写 prompt、选配音色。

### **配置自定义变量**

自定义变量允许在Prompt 中使用标准占位符（如 ${name}），在运行时由客户端传入实际值，实现不同用户、不同角色展示个性化内容的效果。参考文档：[RTOS SDK (License模式) 提示词变量设置](https://help.aliyun.com/zh/model-studio/rtos-license-prompt-params)。

-   在百炼控制台创建应用
    
-   修改「提示词」新增「自定义变量」
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8599890871/p1080420.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8599890871/p1080421.png)

#### **1\.** 协议参数说明

客户端在与服务端建立 WebSocket 连接并发送 run-task 开始指令时，需在 parameters 中携带自定义角色的音色与提示词变量。

**参数路径**

**类型**

**是否必填**

**说明**

**示例值**

`payload.parameters.downstream.voice`

String

是

选配的角色音色编码。

`longanhuan`

`payload.parameters.biz_params.user_prompt_params`

Object

否

提示词自定义变量键值对，KV 结构需与控制台配置一致。

`{"name": "阿云", "skill": "唱歌"}`

#### **2\.** 建联请求示例（JSON 协议）

```
{
  "header": {
    "action": "run-task",
    "streaming": "duplex",
    "task_id": "Task_Id_Example"
  },
  "payload": {
    "task_group": "aigc",
    "task": "multimodal-generation",
    "function": "generation",
    "model": "multimodal-dialog",
    "input": {
      "workspace_id": "Workspace_Id_Example",
      "app_id": "App_Id_Example",
      "directive": "Start"
    },
    "parameters": {
      "upstream": {
        "sample_rate": 16000,
        "type": "AudioAndVideo",
        "mode": "tap2talk",
        "audio_format": "pcm",
        "enable_server_vad_start": false
      },
      "downstream": {
        "voice": "longanhuan",
        "sample_rate": 16000,
        "audio_format": "mp3",
        "volume": 50,
        "speech_rate": 100,
        "pitch_rate": 100,
        "intermediate_text": "transcript,dialog",
        "transmit_rate_limit": 16000
      },
      "client_info": {
        "user_id": "test_1",
        "device": {
          "uuid": "test_1"
        }
      },
      "biz_params": {
        "user_prompt_params": {
          "name": "阿云",
          "skill": "唱歌"
        }
      }
    }
  }
}
```

### 编写角色 Prompt

Prompt 定义了角色的人设、风格和行为规则。在 prompt 中用 ${变量名} 引用已配置的自定义变量，系统在运行时自动替换为实际值。

**Prompt模板结构**

```
##角色
你叫 ${name}，是搭载在 APP 中的 AI 助手，性格${role_personality}。
你的用户是 ${user_name}。

##风格
1. 用口语化方式回答，适时加入语气词，让对话自然亲切。
2. 回复简洁，不超过 3 句话，避免冗长。
3. 对用户情绪有共情，让对方感受到被理解和支持。

##回复要求
1. 回复要简洁、亲切、自然。
2. 避免过于正式或说教的语气。

##系统条件
用户当前所处的位置：${location}
今天的日期：${date}
```

**带表情/动作的Prompt示例（可选）**

如设备支持表情或动作，可在 prompt 中声明对应标识符，模型输出时会携带这些标签供客户端解析执行，参考文档：[动作情绪控制实践](https://help.aliyun.com/zh/model-studio/action-emotion-control-practice)。

```
##表情和动作
###表情
你在互动中，可以如下表情执行，格式为<表情代码，表情描述>，表情代码用[emoji-xx]表示，是你需要输出到结果中的部分，表情描述是一段文本，解释该表情代码的具体含义。每次回复最多只能输出一种表情。
[emoji-01] : 大笑
[emoji-02] : 死鱼眼
[emoji-03]: 害羞
[emoji-04]: 大哭
[emoji-05]: 委屈

###动作
你在互动中，支持如下动作执行，格式为<动作代码，动作描述>，动作代码用[action-xx]表示，是你需要输出到结果中的部分，动作描述是一段文本，解释该动作代码的具体含义。每次回复最多只能输出一种动作。
[action-01] : 往前走
[action-02] : 抱抱
[action-03]: 转身
[action-04]: 跳一下
[action-05]: 跺脚

##回复要求
1.你的回复内容可以包含动作、表情、语气音的序列，但不需要每次回复都有，请根据对话上文、用户当前情绪和意图、你的性格设定，给出最恰当的反馈，反馈内容可以包含动作、表情、文本或它们之间的组合，但必须自然、一致，符合正常交互的表现。
2. 每次回复不要包含过多要素，或在多轮之间机械重复。

##回复示例
Case 1
输入：小云，你好可爱
输出：[emoji-01][action-01]哎呀，你这么说我都不好意思了
```

### **选择音色**

音色通过 parameters.downstream.voice参数传入，在 SDK 层面生效。不同 voice 值对应不同的音色风格，建议根据角色性格选择匹配的音色。完整音色列表详见： [音色列表](https://help.aliyun.com/zh/model-studio/multimodal-timbre-list)。

**推荐音色**

**适用场景**

**名称**

**音色名称**

**（voice参考值）**

**年龄**

**音色特质**

**合成文案及样音试听**

**语言**

备注

**标杆音色**

龙安欢

longanhuan

20-30岁

**欢脱元气女**

你看我刚从食堂买的豆沙包！还是热乎的，我特意多买了一个给你，甜而不腻超好吃。对了对了，下午课间咱们一起去操场晒晒太阳吧，今天天气超级好！

中英双语

龙安洋

longanyang

20-30岁

**阳光大男孩**

我呀，周末打算去书店逛逛，听说新到了一批科普杂志，你要是有空的话，咱们可以一起去，看完还能顺路去旁边的甜品店坐会儿。哦对了，你上次说想买的那支笔，我路过文具店帮你带了，试试好不好用。

中英双语

龙呼呼

longhuhu\_v3

年龄6-10岁

**天真烂漫女童**

喂，你有没有想过，如果我们能飞到更高的地方，是不是就能够看到整个大陆的全貌了呢！呼呼想想就觉得好激动啊！

中英双语

消费电子-儿童陪伴

龙汪汪

longwangwang\_v3

年龄6-15岁

**台湾少年音**

大家好！我是专为3至12岁儿童设计的智能陪伴机器人，集语音对话、中英双语故事、儿歌播放、习惯养成与情绪互动于一体。我采用安全环保材质，具备护眼屏幕和家长远程管控功能，用温暖声音和趣味内容，全天候陪伴孩子快乐学习、健康成长！

中英双语

多模态交互开发套件专属音色

陪伴闲聊

龙安朔

longanshuo\_v3

20-25岁

**干净清爽男**

那个……要是你搬东西需要帮忙，随时叫我，我力气还挺大的，之前帮同学搬宿舍，好几箱书都是我扛上去的，别客气啊。

中英双语

多模态交互开发套件专属音色

女声

龙菲菲

longfeifei\_v3

20-25

**甜美娇气女**

你最近是不是又熬夜了？明天我给你带热牛奶，顺便给你看我收藏的护眼食谱，保证让你眼睛亮晶晶的！

中英双语

多模态交互开发套件专属音色

陪伴闲聊

龙安智

longanzhi\_v3

25-35岁

**睿智轻熟男**

各位听众朋友们，欢迎收听今天的播客，今天咱们来探讨一下人生选择这个话题，每个人在人生的不同阶段都会面临各种选择，希望我分享的一些观点，能给你们带来一些启发。

中英双语

陪伴闲聊-接地气女

龙安亲

longanqin\_v3

20-25岁

**亲和活泼女**

哎！你们听说了吗？楼下新开了家奶茶店，装修得特别清新，还有好多新奇的口味，像什么杨枝甘露爆珠茶、草莓奶冻茶，听着就想喝。咱们下班一起去试试呗，要是好喝的话，以后下午茶就有着落啦！

中英双语

陪伴闲聊

龙安灵

longanling\_v3

20-30岁

**思维灵动女**

欢迎大家来到今天的播客节目，今天咱们要聊的话题是关于职场成长的，我会跟大家分享一些实用的小技巧，希望能帮助大家在工作中少走一些弯路，更快地实现自己的目标。

中英双语

陪伴闲聊-高雅气质女

龙安雅

longanya\_v3

25-35岁

**高雅气质女**

周末在家泡一壶茶，选一本喜欢的书，坐在窗边晒晒太阳，阳光洒在身上暖暖的，茶香伴着书香，这样安安静静的时光，感觉心里特别舒服。偶尔还会写几笔毛笔字，让自己的节奏慢下来，享受这份惬意。

中英双语

语音助手

龙安温

longanwen\_v3

25-35岁

**优雅知性女**

晚上好，现在为您播放舒缓的音乐，帮助您放松身心，进入睡眠状态，如果您有其他需求，比如设置明天的闹钟，随时跟我说。

中英双语

语音助手

龙安昀

longanyun\_v3

30-35岁

**居家暖男**

您已经辛苦一天了，我已经为您调整好室内温度，还准备了您喜欢的饮品，您可以放松休息一下，有任何需要，都可以叫我哦。

中英双语

## **步骤二：多角色切换实现**

### **维护角色映射表**

#### **1\. 角色配置映射表**

由于客户端开发语言存在差异，SDK 不代为管理角色列表，需由客户端在业务层自主实现配置管理。

建议在业务层维护一张角色与参数的映射表（每个角色包含固定的音色 voice 和对应的 user\_prompt\_params 变量组），同时在本地或业务服务端持久化存储当前用户（UID）与角色 ID 的绑定关系。

**角色 ID (role\_id)**

**角色名称**

**音色 (voice)**

**提示词变量组 (user\_prompt\_params)**

`role_01`

小欢

`longanhuan`

`{"name": "小欢", "role_personality": "活泼开朗"}`

`role_02`

小阳

`longanyang`

`{"name": "小阳", "role_personality": "阳光积极"}`

#### **2\. 客户端通用数据结构示例（JSON）**

开发时，建议在本地客户端将上述映射关系及用户绑定关系以类似如下的通用结构进行存储（各语言可自行转化为本地的 Map/Dictionary/Object 结构）：

```
{
  "header": {
    "action": "run-task",
    "streaming": "duplex",
    "task_id": "Task_Id_Example"
  },
  "payload": {
    "task_group": "aigc",
    "task": "multimodal-generation",
    "function": "generation",
    "model": "multimodal-dialog",
    "input": {
      "workspace_id": "Workspace_Id_Example",
      "app_id": "App_Id_Example",
      "directive": "Start"
    },
    "parameters": {
      "upstream": {
        "sample_rate": 16000,
        "type": "AudioAndVideo",
        "mode": "tap2talk",
        "audio_format": "pcm",
        "enable_server_vad_start": false
      },
      "downstream": {
        "voice": "longanhuan",
        "sample_rate": 16000,
        "audio_format": "mp3",
        "volume": 50,
        "speech_rate": 100,
        "pitch_rate": 100,
        "intermediate_text": "transcript,dialog",
        "transmit_rate_limit": 16000
      },
      "client_info": {
        "user_id": "test_1",
        "device": {
          "uuid": "test_1"
        }
      },
      "biz_params": {
        "user_prompt_params": {
          "name": "阿云",
          "skill": "唱歌"
        }
      }
    }
  }
}
```

### **角色切换流程**

当用户在客户端界面触发“切换角色”或“切换音色”时，由于音色和提示词属于连接级参数，不支持在同一个 WebSocket 连接内热切换。客户端必须遵循“先断开、再重连”的标准流程：

#### **1\. 切换步骤说明**

1.  断开当前连接：客户端主动关闭当前的 WebSocket 连接，并销毁相关实例，释放底层音频双工通道及硬件资源。
    
2.  更新绑定关系：在本地或业务服务端，将当前用户（UID）绑定的 Role ID 更新为新选定的角色。
    
3.  加载新配置重连：从角色映射表中提取新角色的 voice 和 user\_prompt\_params 参数，重新发起 WebSocket 握手建联，并在首帧 run-task 指令中传入新参数。
    

#### **2\. 角色切换业务时序图**

```
客户端 UI             客户端业务层 (SDK)             百炼服务端
   │                       │                             │
   │ 1. 触发切换新角色       │                             │
   ├──────────────────────>│                             │
   │                       │ 2. 主动断开当前连接          │
   │                       ├────────────────────────────>X (断开旧连接)
   │                       │                             │
   │                       │ 3. 读取新角色配置及变量     │
   │                       │    (voice & prompt params)  │
   │                       │                             │
   │                       │ 4. 携新参数发起 WebSocket    │
   │                       ├────────────────────────────>──┐ (重新建联)
   │                       │                               │
   │                       │<──────────────────────────────┘
   │ 5. 提示切换成功       │                             │
   |<──────────────────────┤                             │
```

**重要**

关于上下文继承的注意事项：重新建立连接后，新链路在服务端的对话上下文会重置（变为空白）。如果您的业务场景需要继承上一角色的部分对话记忆，需由客户端在业务层自行维护历史文本，并在新连接建立后的首轮对话请求中，以历史消息的形式拼接到请求体中一并传入。
