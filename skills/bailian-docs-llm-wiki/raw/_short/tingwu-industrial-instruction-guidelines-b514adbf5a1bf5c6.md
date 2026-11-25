# 使用指南

本文介绍如何配置并使用通义听悟-工业生产指令转写Agent。

<a id="准备工作"></a>

<a id="cfcc565184fdr"></a>

## 准备工作

[开通](https://common-buy.aliyun.com/?commodityCode=sfm_TingWuAgent_public_cn)通义听悟 Agent 服务。

> **说明**
>
> 开通后即可使用阿里云百炼平台全系通义听悟 Agent 服务。

<a id="一-创建应用"></a>

<a id="00458686b0nqj"></a>

## 一、创建应用

点击[控制台](https://bailian.console.aliyun.com/?tab=app#/app/app-market/tingwu/tingwu-industrial-instruction)页面中间或右上角的**创建应用**按钮，进行应用创建，支持创建最多100个应用。

![42](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004408.webp)

<a id="二-调试配置"></a>

<a id="fded198e69tqd"></a>

## 二、调试配置

完成调试配置后，您可多次[体验效果](tingwu-industrial-instruction-guidelines-b514adbf5a1bf5c6.md#0212744c1075p)，确认效果满足预期后再[发布应用](tingwu-industrial-instruction-guidelines-b514adbf5a1bf5c6.md#54ad18c3206oz)，并参照[API接入](tingwu-industrial-instruction-guidelines-b514adbf5a1bf5c6.md#18067199c3nfh)进行实际开发调用。

<a id="1-选择指令集"></a>

<a id="dff06118e337u"></a>

### 1\. 选择指令集

![43](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004411.webp)

您可以在此选择在转写中生效的指令集，指令集中可以包含应用场景中难以识别的专业词汇或特殊指令，如：

-   左翼子板和左前围
-   漆渣
-   放倒后排右侧座椅靠背
-   肠系膜上动脉栓塞

如果您未添加过指令集，您可以通过上传文件的方式添加指令集，支持.xlsx, .xls, .csv, .txt格式的文件，请注意：

1.  每个指令集最多包含1000行指令，每条指令长度必须在2-30字符之间。
2.  指令仅支持中文、英文和数字，不支持符号。
3.  具体文件格式请点击**下载模板**并参考其中的指令集文件内容。

您最多可以添加10个指令集，指令集在所有工业指令转写应用间共享。

<a id="2-语音输入"></a>

<a id="4c5387822cib9"></a>

### 2\. 语音输入

![44](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004413.webp)

<a id="sec-tabs"></a>

<a id="模型选择"></a>

<a id="模型选择-h4"></a>

#### 模型选择

目前支持以下模型：

-   一句话识别及翻译 V1.0模型（支持最长60s的音频识别和翻译）。

<a id="输入语种"></a>

<a id="输入语种-h4"></a>

#### 输入语种

此处可配置录音时的识别语种，目前支持：

-   多语种：将自动识别发言语种。
-   单语种：若您的应用场景仅存在单一语种，可以指定单一语种，目前支持中文、英文、粤语、韩语、日语、德语、法语、俄语、意大利语和西班牙语。

> **说明**
>
> 界面化的应用配置在发布后会对 API 生效。

完成上述配置后，即可点击**立即录音**按钮进行调试（步骤[3\. 应用信息](tingwu-industrial-instruction-guidelines-b514adbf5a1bf5c6.md#b20c42d508vop)仅在接口调用时需要参考）。

如需查看**调试效果**和**测试记录**，请参见[体验效果](tingwu-industrial-instruction-guidelines-b514adbf5a1bf5c6.md#0212744c1075p)。

<a id="3-应用信息"></a>

<a id="b20c42d508vop"></a>

### 3\. 应用信息

![415](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004417.webp)

<a id="sec-tabs-2"></a>

<a id="应用名称"></a>

<a id="应用名称-h4"></a>

#### 应用名称

在此处复制或修改本应用名称。

<a id="应用id"></a>

<a id="应用id-h4"></a>

#### 应用ID

在此处查看或复制本应用ID。

<a id="应用描述"></a>

<a id="应用描述-h4"></a>

#### 应用描述

在此处添加本应用的描述信息。

<a id="三-体验效果"></a>

<a id="0212744c1075p"></a>

## 三、体验效果

点击**立即录音**按钮后，浏览器可能会申请您的麦克风权限，请点击允许访问。

之后您可以通过麦克风输入待测试的工业指令，点击结束录音或模型自动识别到一句话说完后，会返回工业指令的最终纠正结果。

![46](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004439.webp)

<a id="sec-tabs-3"></a>

<a id="对话内容"></a>

<a id="对话内容-h4"></a>

#### 对话内容

对话内容中显示的是输入音频的中文翻译结果。

<a id="指令纠正"></a>

<a id="指令纠正-h4"></a>

#### 指令纠正

指令纠正中显示的是对话内容通过大模型纠正后的指令结果。

<a id="测试记录"></a>

<a id="测试记录-h4"></a>

#### 测试记录

当前应用的所有调试测试结果，将统一进行保存记录，点击控制台右上角的**测试记录**按钮可进行查看。

![47](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004440.webp)

测试记录列表会展示多维度的信息，具体包括测试时间、任务ID、任务状态、使用的指令集、对话内容和指令纠正结果。

![416](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004442.webp)

<a id="四-发布应用"></a>

<a id="54ad18c3206oz"></a>

## 四、发布应用

点击控制台右上角的**发布**按钮，输入版本描述信息，即可完成发布，应用发布后线上将立即生效。

![48](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004443.webp)

<a id="版本管理"></a>

<a id="0551030be1t70"></a>

### 版本管理

应用发布后，可在控制台右上角的**版本管理**中查看历史版本。选择某个历史版本，点击右下角**覆盖当前草稿**按钮，则该版本的配置信息将自动带入到当前草稿中。

![419](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004447.webp)

<a id="五-api接入"></a>

<a id="18067199c3nfh"></a>

## 五、API接入

应用发布完成后，稍等片刻，点击控制台顶部**API 接入**按钮，查看对应的 Java 和 Python 接入参考代码，然后接入到您的业务系统中。

![412](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004446.webp)

<a id="六-删除应用"></a>

<a id="6659473930ruf"></a>

## 六、删除应用

在**我的应用**列表中，可**删除**某个应用。

**删除后不可恢复，为避免影响您的线上业务，请务必谨慎操作。** ![49](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4025297571/p1004444.webp)
