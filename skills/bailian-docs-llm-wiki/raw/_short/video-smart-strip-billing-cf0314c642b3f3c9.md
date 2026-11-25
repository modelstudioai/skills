# 视频智能拆条计费

全妙产品矩阵包含4个SaaS产品妙笔/妙策/妙搜/妙读和若干个AI Agent（场景化能力），本文档主要介绍AI Agent中视频智能拆条应用的计费。

<a id="计费说明"></a>

<a id="681f8eba46jdi"></a>

## 计费说明

我们提供**实时**和**异步**两种模式，推荐优先使用**异步模式**离线调用：

-   **实时模式>在线调用**：
    
    -   每个阿里云主账号提供1个免费并发，暂不支持增加并发配额；
    -   支持处理的单个视频时长最多不超过30分钟，且单个视频大小小于200MB，分辨率不超过1080P。
-   **异步模式>离线调用**：
    
    -   每个阿里云主账号提供2个免费并发，且支持增加并发配额，最多支持扩展到30并发；
    -   支持处理的单个视频时长最多不超过1小时，且单个视频大小小于450MB，分辨率不超过1080P，队列中的任务不超过10万个视频文件。

> **说明**
>
> 千问系列模型的[新人免费额度](../model-user-guide/test-1/new-free-quota.md)不适用于视频智能拆条功能。

<a id="计费详情"></a>

<a id="4a7eb881d0yty"></a>

## 计费详情

<table><thead><tr><th><strong>模式</strong></th><th><strong>套餐组合</strong></th><th><strong>计费</strong></th></tr></thead><tbody><tr><td rowspan="3"><p>实时模式</p></td><td><p>大模型推理（必选）</p></td><td><ul><li><p>全妙LLM-turbo</p><ul><li>输入：0.0008元/千Token</li><li>输出：0.002元/千Token</li></ul></li><li><p>全妙LLM-plus</p><ul><li>输入：0.0024元/千Token</li><li>输出：0.0096元/千Token</li></ul></li><li><p>全妙LLM-max（思考与非思考模式）</p><ul><li>输入：0.0048元/千Token</li><li>输出：0.0192元/千Token</li></ul></li><li><p>deepseek r1</p><ul><li>输入：0.004元/千Token</li><li>输出：0.016元/千Token</li></ul></li></ul></td></tr><tr><td><p>多模态信息处理（必选）</p><blockquote><p>包含视频格式的转化、连接、分镜、抽帧、ASR识别</p></blockquote></td><td><p>2.8元/小时（按照实际成功处理的视频总时长计费）</p></td></tr><tr><td><p>分镜增强（可选）</p><blockquote><p>利用VL模型及OCR模型提高视频拆条的准确率。</p></blockquote><blockquote><p>可根据视频特点及拆条效果自由选择</p></blockquote></td><td><ul><li><p>全妙VL</p><ul><li>输入：0.0016元/千Token</li><li>输出：0.004元/千Token</li></ul></li><li><p>ocr</p><ul><li>输入：0.0003元/千Token</li><li>输出：0.0005元/千Token</li></ul></li></ul></td></tr><tr><td rowspan="4"><p>异步模式</p></td><td><p>大模型推理（必选）</p></td><td><ul><li><p>全妙LLM-turbo</p><ul><li>输入：0.0008元/千Token</li><li>输出：0.002元/千Token</li></ul></li><li><p>全妙LLM-plus</p><ul><li>输入：0.0024元/千Token</li><li>输出：0.0096元/千Token</li></ul></li><li><p>全妙LLM-max（思考与非思考模式）</p><ul><li>输入：0.0048元/千Token</li><li>输出：0.0192元/千Token</li></ul></li><li><p>deepseek r1</p><ul><li>输入：0.004元/千Token</li><li>输出：0.016元/千Token</li></ul></li></ul></td></tr><tr><td><p>多模态信息处理（必选）</p><blockquote><p>包含视频格式的转化、连接、分镜、抽帧、ASR识别</p></blockquote></td><td><p>2.8元/小时（按照实际成功处理的视频总时长计费）</p></td></tr><tr><td><p>分镜增强（可选）</p><blockquote><p>利用VL模型及OCR模型提高视频拆条的准确率。</p></blockquote><blockquote><p>可根据视频特点及拆条效果自由选择</p></blockquote></td><td><ul><li><p>全妙VL</p><ul><li>输入：0.0016元/千Token</li><li>输出：0.004元/千Token</li></ul></li><li><p>ocr</p><ul><li>输入：0.0003元/千Token</li><li>输出：0.0005元/千Token</li></ul></li></ul></td></tr><tr><td><p>增加并发配额（可选）</p></td><td><p>1元/小时*并发数</p><p>（例如用10并发处理共30小时视频，那就是1<em>30</em>10=300元）</p><ul><li>上传任务优先使用免费并发，如果免费并发已全部占用，则使用付费并发，并按照当前任务实际处理时长计费。</li><li>可以通过GetVideoAnalysisConfig、UpdateVideoAnalysisConfig这两个接口查看和扩缩并发</li></ul></td></tr></tbody></table>

<a id="开通与账单地址"></a>

<a id="5002613c90d66"></a>

## 开通与账单地址

开通地址：使用视频智能拆条需先开通影视传媒视频理解（免费开通）[视频理解开通地址](https://common-buy.aliyun.com/?commodityCode=sfm_videoanalysis_public_cn)；

账单查询地址：[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail?spm=a2c4g.11186623.0.0.619355efACwmfT)。

<a id="产品地址"></a>

<a id="7b5539e694r56"></a>

## 产品地址

可点击[产品地址](https://api.aliyun.com/api/QuanMiaoLightApp/2024-08-01/RunVideoDetectShot?spm=a2c4g.11186623.0.0.566445d0x4wCxV&RegionId=cn-beijing)进行产品体验。

<a id="产品相关文档"></a>

<a id="03b3d4a1e8bu6"></a>

## 产品相关文档

-   技术文档
    
    可点击[视频智能拆条接口文档](api-quanmiaolightapp-2024-08-01-dir-film-and-tel-ba1dc245c3d4270b.md)进行查看；
    

<a id="常见问题"></a>

<a id="5de1f8d74fb87"></a>

## 常见问题

<a id="1-离线调用怎么增加并发配额"></a>

<a id="04e102e5dc3le"></a>

#### 1\. 离线调用怎么增加并发配额？

可以通过[智能拆条-获取配置](api-quanmiaolightapp-2024-08-01-getvideodetectsh-9cd22ac53507d103.md)、[智能拆条-更新配置](api-quanmiaolightapp-2024-08-01-updatevideodetec-4e8f4cc6d43a8ca0.md)接口查看和扩缩并发。

<a id="2-一并发收费是1元-小时-这个时间是怎么定义的"></a>

<a id="6ccfc589791yn"></a>

#### 2\. 一并发收费是1元/小时，这个时间是怎么定义的？

收费的时间计算范围是从客户提交任务的时间点开始算到任务执行结束为止。

<a id="3-任务运行到中途失败了-怎么计费"></a>

<a id="5b6c37e007rt4"></a>

#### 3\. 任务运行到中途失败了，怎么计费？

当任务运行到中途失败时，主要是看最后一个事件消息的event，如果是task-failed，就不计费；其他运行成功部分计费，失败部分不计费。在产品客户端页面立即中断并展示状态。

<a id="5-购买视频智能拆条api节省计划后能退订吗"></a>

<a id="2494a1ef7f11a"></a>

#### 5.购买视频智能拆条API节省计划后能退订吗？

支持退订。
