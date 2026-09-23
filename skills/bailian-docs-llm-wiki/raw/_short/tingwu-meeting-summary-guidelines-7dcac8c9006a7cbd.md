# 使用指南

本文介绍如何配置并使用通义听悟-智能纪要Agent。

## 准备工作

[开通](https://common-buy.aliyun.com/?commodityCode=sfm_TingWuAgent_public_cn)通义听悟 Agent 服务。

**说明**开通后即可使用阿里云百炼平台全系通义听悟 Agent 服务。

## 一、创建应用

点击[控制台](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.3de05528VSlyVV&tab=app#/app/app-market/tingwu/tingwu-meeting-summary)页面中间或右上角的**创建应用**按钮，进行应用创建，支持创建最多100个应用。

![20251013175114](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1015569.webp)

## 二、调试配置

完成调试配置后，您可多次[体验效果](https://help.aliyun.com/zh/model-studio/tingwu-meeting-summary-guidelines#0212744c1075p)，确认效果满足预期后再[发布应用](https://help.aliyun.com/zh/model-studio/tingwu-meeting-summary-guidelines#54ad18c3206oz)，并参照[API接入](https://help.aliyun.com/zh/model-studio/tingwu-meeting-summary-guidelines#18067199c3nfh)进行实际开发调用。

### 1\. 选择音频输入方式

![20251009135412](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014046.webp)

#### 内容来源

选择以下任一内容来源：

-   **录音文件识别：**支持mp3、wav、m4a、wma、aac、ogg、amr、flac、aiff格式的音频文件和mp4、wmv、m4v、flv、rmvb、dat、mov、mkv、webm、avi、mpeg、3gp、ogg格式的视频文件。文件大小不超过6 GB。
    
-   **实时转写：**采集音频并进行实时转写。
    
-   **通义听悟任务：**填写当前应用历史已完成的转写任务ID（TaskID），可节省语音转文字成本。
    
    **说明**任务创建成功后，系统将在响应中返回TaskID字段。
    
-   **会议文本内容：**按格式录入对话内容文本，也可节省语音转文字成本。
    

```
示例1：
发言人1：对话内容。
发言人2：对话内容。
示例2：
销售：对话内容。
客户：对话内容。
```

#### 音频类型

![20251009142933](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014038.webp)

仅限内容来源为**录音文件识别**时需要选择音频类型：

-   **电话录音 或 16K及以上单声道**
-   **16K及以上多声道（车载设备录制）**

#### 转写模型

![20251009142955](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014039.webp)

仅限内容来源为**录音文件识别**和**实时转写**时需要选择转写模型：

-   **paraformer-v2（中英文）**
-   **paraformer-v2（中英日韩粤语）**
-   **paraformer-v2 (英)**
-   **paraformer-v2 (粤)**
-   **paraformer-v2 (日)**
-   **paraformer-v2 (韩)**
-   **教育领域模型（中英）**
-   **汽车领域模型（中英粤）**

#### 转写配置

![20251009143013](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014040.webp)

仅限内容来源为**录音文件识别**和**实时转写**时可以配置角色分离和识别语种：

**角色分离：**支持选择两人或多人角色分离。

**识别语种：**基于不同转写模型选择，提供对应的识别语种选项。

**翻译：**支持对识别原文进行翻译，语种包括中文、英语、日语、韩语、德语、法语、俄语。

**热词：**支持添加并管理热词组，使用热词可以有效提高语音识别效果。

### 2\. 设定大模型参数

![20251009143038](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014042.webp)

#### 分析模型

目前支持以下模型：

-   **默认项（官方搭配最佳效果的模型组合）**
-   **tingwu-plus**
-   **qwen-plus**
-   **qwq**

#### 分析项

配置大模型分析选项，包括以下能力：

**要点提炼：**支持关键词和待办事项提取。

**摘要总结：**支持全文摘要、发言总结、要点回顾、思维导图提取。

-   全文摘要，支持选择一段话摘要或 Markdown 格式摘要。
-   思维导图，支持选择带时间戳或不带时间戳。

**PPT分析：**当内容来源为**录音文件识别**，且文件为视频时，支持对视频中的 PPT进行提取和讲解总结。

**其他：**包括章节速览、口语书面化、自定义 Prompt 功能。

-   章节速览支持对速览粒度（细粒度、中粒度、粗粒度）和标题长度（长、中等、短）进行设定。
-   自定义 Prompt 是指由客户自主定义大模型提示词，引导大模型完成客户定义的各类任务。自定义 Prompt 模型可单独选择，和所选分析模型不冲突。使用自定义 Prompt 功能时，支持设定大模型输出格式，包括：仅发言人信息+转写结果、句子序号+发言人信息+转写结果、仅转写结果三种格式。

**说明**界面化的应用配置可对 API 生效，也可在 API 中更新参数，覆盖界面应用配置。

完成上述配置后，即可点击**立即分析**按钮进行调试（步骤[3\. API 调用配置](https://help.aliyun.com/zh/model-studio/tingwu-meeting-summary-guidelines#b20c42d508vop)仅在接口调用时需要参考）。

如需查看**调试效果**和**测试记录**，请参见[体验效果](https://help.aliyun.com/zh/model-studio/tingwu-meeting-summary-guidelines#0212744c1075p)。

### 3\. API 调用配置

![20251009143103](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014047.webp)

#### 回调方式

**说明**此处回调方式设置请参考 [如何通过回调获取异步任务结果](https://help.aliyun.com/zh/tingwu/how-to-get-asynchronous-task-result-through-callback)

-   **HTTP post 协议：**需要您输入对应 URL 地址，通义听悟会向配置的HTTP URL发送post请求，返回的HTTP status为200则检查通过。
-   **不设置回调（主动轮询）：**如果您选择不设置回调，自行主动轮询，可使用Agent任务的轮询接口：getTask；默认每个账户轮询的 QPS 为：100
-   **事件总线：**处理结果将按事件总线北京 Region 的 default 配置，发送到您的服务（需要提前开通 [阿里云事件总线](https://eventbridge.console.aliyun.com/cn-beijing/event-buses) ）

当服务端接收到回调消息，并返回200的 HTTP 状态码后，该应用项目才能创建成功，消息格式如下：

```
{
  "output": {
      "transcriptionPath": "https://***.oss-cn-hangzhou.aliyuncs.com/***",
      "status": 0
  },
  "requestId": "***",
  "taskInfo": {
      "dataId": "***",
      "userSpaceId": "llm-***",
      "appId": "***",
      "model": "tingwu-***",
      "userId": "***"
  }
}
```

#### 应用名称

在此处复制或修改本应用名称。

#### 应用ID

在此处查看或复制本应用ID。

#### 应用描述

在此处添加本应用的描述信息。

## 三、体验效果

点击**立即体验**按钮后，稍等片刻，即可查看智能纪要的对话内容和分析结果。

![20251009141949](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014048.webp)

#### 对话内容

![20251009144017](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014053.webp)

-   若输入内容来源为**录音文件识别**或**实时转写**或**通义听悟任务**，则对话内容展示框中将呈现对应的音视频文字转写结果，并标识对话人ID和对话时间戳。支持播放音频文件进行比对。
-   若输入内容来源为**会议文本内容**文字输入，则可能无法展示对话时间戳信息，但不会影响结果分析。

#### 分析结果

在分析结果展示框中，可查看智能速览、思维导图、自定义 Prompt 的分析结果。分析项可在左侧进行配置，详见[调试配置](https://help.aliyun.com/zh/model-studio/tingwu-meeting-summary-guidelines#fded198e69tqd)。

其中智能速览页包括关键词、全文概要、章节速览、发言总结、要点回顾、提取 PPT 等结果展示。

章节速览效果：

![20251009142224](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014058.webp)

发言总结效果：

![20251009142144](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014060.webp)

要点回顾效果：

![20251009142117](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014061.webp)

提取 PPT 效果：

![20251009142053](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014062.webp)

思维导图提取效果：

![20251009142015](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014064.webp)

#### 测试记录

当前应用的所有调试测试结果，将统一进行保存记录，点击控制台右上角的**测试记录**按钮可查看。

测试记录列表会展示多维度的信息，具体包括测试时间、任务ID、任务状态、分析模型、对话内容，以及查看**详情**的操作按钮。

![20251009143153](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014052.webp)

点击某条测试记录最右侧的**详情**按钮，可以查看完整详细的**会议内容**和**分析结果**。

![20251009141910](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014051.webp)

## 四、发布应用

点击控制台右上角的**发布**按钮，输入版本描述信息，即可完成发布，应用发布后线上将立即生效。

![20251009143218](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014065.webp)

### 版本管理

应用发布后，可在控制台右上角的**版本管理**中查看历史版本。选择某个历史版本，点击右下角**覆盖当前草稿**按钮，则该版本的配置信息将自动带入到当前草稿中。

![20251009143241](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014044.webp)

## 五、API接入

应用发布完成后，稍等片刻，点击控制台顶部**API 接入**按钮，查看对应的 Java 和 Python 接入参考代码，然后接入到您的业务系统中。

![20251009141759](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1014045.webp)

## 六、删除应用

在**我的应用**列表中，可**删除**某个应用。

**删除后不可恢复，为避免影响您的线上业务，请务必谨慎操作。** ![20251013175233](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8687050671/p1015571.webp)
