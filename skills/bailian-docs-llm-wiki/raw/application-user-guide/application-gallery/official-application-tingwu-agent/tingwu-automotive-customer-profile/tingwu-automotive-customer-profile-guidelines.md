# 使用指南

本文介绍如何配置并使用通义听悟-购车客户画像 Agent。

## 准备工作

[开通](https://common-buy.aliyun.com/?commodityCode=sfm_TingWuAgent_public_cn)通义听悟 Agent 服务。

**说明**开通后即可使用阿里云百炼平台全系通义听悟 Agent 服务。

## 一、创建应用

点击[控制台](https://bailian.console.aliyun.com/?tab=app#/app/app-market/tingwu/tingwu-automotive-customer-profile)页面中间或右上角的**创建应用**按钮，进行应用创建，支持创建多个应用。

![1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996347.webp)

## 二、调试配置

完成调试配置后，您可多次[体验效果](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-guidelines#0212744c1075p)，确认效果满足预期后再[发布应用](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-guidelines#54ad18c3206oz)，并参照[API接入](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-guidelines#18067199c3nfh)进行实际开发调用。

### 1\. 提供待洞察的内容

![2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996348.webp)

#### 内容来源

您选择以下任一方式输入内容：

-   **音频文件：**支持 mp3、wav、m4a、wma、aac、ogg、amr、flac、aiff 格式的音频文件和 mp4、wmv、m4v、flv、rmvb、dat、mov、mkv、webm、avi、mpeg、3gp、ogg 格式的视频文件。文件大小不超过6GB。
    
-   **通义听悟任务：**填写通义听悟 Agent 历史已完成的转写任务ID（TaskID），可节省语音转文字成本。
    
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

### 2\. 制定客户画像规则

![3](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996349.webp)

#### 洞察模型

目前支持以下模型：

-   **ccai-pro**（默认，基于qwen-plus增强内容理解和指令遵循，效果最佳）
-   **qwen-plus**
-   **qwq**

#### 场景描述

在**“请输入品牌名称”**处填写需要洞察分析的品牌名称。

#### 分析结果

勾选本次调试需要的客户画像分析结果维度：

-   **试驾意向评分**
-   **销售线索评分**
-   **一句话客户画像**
-   **客户详细关注点分析**（必选项）

#### 关注点

-   **默认分析项**：15大类62项（涵盖车辆信息、用户体验、产品配置、用车成本等）
-   **自定义分析项**（上限100项）：添加更匹配您业务场景的洞察分析关注点，添加时需要输入分析项名称、分析标准

#### 角色设定

系统默认提供 **客户**、**销售**、**导航**、**车机助手**四个默认角色，您可以自定义编辑修改，删除某个角色以及创建新的角色。目前最多支持创建5个角色。请注意，**客户**和 **销售**角色默认不可删除。

-   **客户：**对车辆提出疑问，表达使用感受、询问车型信息及价格等
-   **销售：**介绍车辆的不同配置、性能与技术、舒适性与便利性、解释客户提问等
-   **导航：**播报行驶路线，例如前方路口左拐，前方红绿灯直行
-   **车机助手：**响应车内人员指令，例如已为您打开通风、空调已打开、已关闭音乐

**说明**界面化的应用配置可对 API 生效，您同时也可在 API 中更新参数，覆盖界面应用配置。

完成上述配置后，即可点击**立即分析**按钮进行调试（步骤[3\. API 调用配置](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-guidelines#b20c42d508vop)仅在接口调用时需要参考）。

如需查看**调试效果**和**测试记录**，请参见[体验效果](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-guidelines#0212744c1075p)。

### 3\. API 调用配置

![4](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996350.webp)

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

点击**立即分析**按钮后，稍等片刻，即可查看对话内容和分析结果。

![5](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996351.webp)

#### 对话内容

-   若输入内容来源为**音频文件**或**通义听悟任务**，则对话内容展示框中将呈现对应的音视频文字转写结果，并标识对话人ID和对话时间戳。
-   若输入内容来源为**对话内容**文字输入，则可能无法展示对话时间戳信息，但不会影响洞察结果分析。

#### 分析结果

在洞察结果分析展示框中，可查看**试驾意向评分**、**销售线索评分**、**一句话客户画像**、**客户关注点分析**。其中**客户关注点分析**中会体现**有命中**和**未命中**的分析结果，以及具体命中的原文内容。

分析项可在左侧进行配置，详见[调试配置](https://help.aliyun.com/zh/model-studio/tingwu-automotive-customer-profile-guidelines#eb0ed3305exw8)。

**试驾意向评分**

**销售线索评分**

AI评分结果为**2**分，评分理由：客户详细询问车辆配置与价格，虽未直接提及试驾，但有较高的购车意向，可能需要试驾以做决策。

评分结果等级为**A**，评分理由："客户详细询问车辆配置与价格，讨论贷款购车方案，表明有一定购车意愿"。

**一句话客户画像**

**客户关注点分析**

**一句话客户画像**功能的输出示例：系统生成客户画像卡片，包含客户关注点（车型、外观、内饰、配置、续航、预计到店时间）和购车顾虑点（车辆品质、贷款审批、车辆价格波动）等维度的摘要信息，各维度自动提取对话中的关键词填充。

**客户关注点分析**功能将话题分为**客户关注**和**客户未提及**两类标签页（各标签页后标注话题数量），每个话题以卡片形式展示，包含话题标签（如"电动脚托或脚垫"）、AI 生成的摘要（如"销售提到这款宝马X7带有原厂自带的电动脚托"）以及多段原文内容溯源，卡片右上角提供**定位至对话**按钮可跳转至对应对话位置。

#### 测试记录

当前应用的所有调试测试结果，将统一进行保存记录，点击控制台右上角的**测试记录**按钮可查看。

测试记录列表会展示多维度的信息，具体包括测试时间、任务ID、任务状态、转写模型、洞察模型、对话内容、洞察命中项，以及查看**详情**的操作按钮。

点击某条测试记录最右侧的**详情**按钮，可以查看完整详细的**对话内容**和**分析结果**。

## 四、发布应用

点击控制台右上角的**发布**按钮，输入版本描述信息，即可完成发布，应用发布后线上将立即生效。

![6](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996352.webp)

### 版本管理

应用发布后，可在控制台右上角的**版本管理**中查看历史版本。选择某个历史版本，点击右下角**覆盖当前草稿**按钮，则该版本的配置信息将自动带入到当前草稿中。

![9](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996355.webp)

## 五、API接入

应用发布完成后，稍等片刻，点击控制台顶部**API 接入**按钮，查看对应的 Java 和 Python 接入参考代码，然后接入到您的业务系统中。

![7](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996353.webp)

## 六、删除应用

在**我的应用**列表中，可**删除**某个应用。

**删除后不可恢复，为避免影响您的线上业务，请务必谨慎操作。** ![8](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2979894571/p996354.webp)
