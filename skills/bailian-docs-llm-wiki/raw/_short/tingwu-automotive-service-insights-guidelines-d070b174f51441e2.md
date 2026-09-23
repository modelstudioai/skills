# 使用指南

本文介绍如何配置并使用通义听悟-汽车销售服务洞察 Agent。

## 准备工作

[开通](https://common-buy.aliyun.com/?commodityCode=sfm_TingWuAgent_public_cn)通义听悟 Agent 服务。

**说明**开通后即可使用阿里云百炼平台全系通义听悟 Agent 服务。

## 一、创建应用

点击[控制台](https://bailian.console.aliyun.com/?tab=app#/app/app-market/tingwu/tingwu-automotive-service-insights)页面中间或右上角的**创建应用**按钮，进行应用创建，支持创建多个应用。

![11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996376.webp)

## 二、调试配置

完成调试配置后，您可多次[体验效果](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-guidelines#0212744c1075p)，确认效果满足预期后再[发布应用](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-guidelines#54ad18c3206oz)，并参照[API接入](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-guidelines#18067199c3nfh)进行实际开发调用。

### 1\. 提供待洞察的内容

![12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996377.webp)

#### 内容来源

选择以下任一内容来源：

-   **音频文件：**支持 mp3、wav、m4a、wma、aac、ogg、amr、flac、aiff 格式的音频文件和 mp4、wmv、m4v、flv、rmvb、dat、mov、mkv、webm、avi、mpeg、3gp、ogg 格式的视频文件。文件大小不超过6GB。
    
-   **通义听悟任务：**填写当前应用历史已完成的转写任务ID（TaskID），可节省语音转文字成本。
    
    **说明**任务创建成功后，系统将在响应中返回TaskID字段。
    
-   **对话内容：**按格式录入对话内容文本，也可节省语音转文字成本。
    

```
示例1：
发言人1：对话内容。
发言人2：对话内容。
示例2：
销售：对话内容。
客户：对话内容。
```

#### 转写模型

仅限内容来源为**音频文件**时需要选择转写模型：

-   **汽车领域模型（中英粤）**
-   **paraformer-v2（中英日韩粤）**
-   **paraformer-8k-v2（中文）**
-   **paraformer-v1（中英）**
-   **paraformer-8k-v1（中文）**
-   **教育领域模型（中英）**

#### 音频类型

仅限内容来源为**音频文件**时需要选择音频类型：

-   **电话录音 或 16K及以上单声道**
-   **16K及以上多声道（车载设备录制）**

### 2\. 制定洞察规则

![13](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996378.webp)

#### 洞察模型

目前支持以下模型：

-   **ccai-pro**（默认，基于qwen-plus增强内容理解和指令遵循，效果最佳）
-   **qwen-plus**
-   **qwq**

#### 场景描述

在**“请输入品牌名称”**处填写需要洞察分析的品牌名称。

#### 洞察标准

输入自定义洞察标准，例如：“请检测上述对话中销售人员的表现。”

#### 洞察项

-   **默认洞察项**：11大类74项（涵盖开场介绍、意向确认、现场接待、需求沟通等）
-   **自定义洞察项**（上限100项）：添加更匹配业务场景的洞察分析关注点，需输入洞察项名称、洞察标准和此项对应的评价分值（加减分，将在接口中返回结果，非必选项）

**说明**界面化的应用配置可对 API 生效，也可在 API 中更新参数，覆盖界面应用配置。

完成上述配置后，即可点击**立即分析**按钮进行调试（步骤[3\. API 调用配置](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-guidelines#b20c42d508vop)仅在接口调用时需要参考）。

如需查看**调试效果**和**测试记录**，请参见[体验效果](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-guidelines#0212744c1075p)。

### 3\. API 调用配置

![14](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996379.webp)

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

点击**立即分析**按钮后，稍等片刻，即可查看对话内容和洞察结果。

![15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996380.webp)

#### 对话内容

-   若输入内容来源为**音频文件**或**通义听悟任务**，则对话内容展示框中将呈现对应的音视频文字转写结果，并标识对话人ID和对话时间戳。
-   若输入内容来源为**对话内容**文字输入，则可能无法展示对话时间戳信息，但不会影响洞察结果分析。

#### 洞察结果

在洞察结果分析展示框中，可查看**有命中**和**未命中**的洞察结果，并查看具体命中的原文内容。

洞察项可在左侧进行配置，详见[调试配置](https://help.aliyun.com/zh/model-studio/tingwu-automotive-service-insights-guidelines#fded198e69tqd)。

#### 测试记录

当前应用的所有调试测试结果，将统一进行保存记录，点击控制台右上角的**测试记录**按钮可查看。

测试记录列表会展示多维度的信息，具体包括测试时间、任务ID、任务状态、转写模型、洞察模型、对话内容、洞察命中项，以及查看**详情**的操作按钮。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p988966.png)

点击某条测试记录最右侧的**详情**按钮，可以查看完整详细的**对话内容**和**洞察结果**。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p988956.png)

## 四、发布应用

点击控制台右上角的**发布**按钮，输入版本描述信息，即可完成发布，应用发布后线上将立即生效。

![16](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996381.webp)

### 版本管理

应用发布后，可在控制台右上角的**版本管理**中查看历史版本。选择某个历史版本，点击右下角**覆盖当前草稿**按钮，则该版本的配置信息将自动带入到当前草稿中。

![17](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996382.webp)

## 五、API接入

应用发布完成后，稍等片刻，点击控制台顶部**API 接入**按钮，查看对应的 Java 和 Python 接入参考代码，然后接入到您的业务系统中。

![18](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996383.webp)

## 六、删除应用

在**我的应用**列表中，可**删除**某个应用。

**删除后不可恢复，为避免影响您的线上业务，请务必谨慎操作。** ![19](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2779894571/p996386.webp)
