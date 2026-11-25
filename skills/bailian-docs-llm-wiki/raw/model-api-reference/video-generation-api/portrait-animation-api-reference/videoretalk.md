# 视频口型替换-声动人像VideoRetalk

声动人像VideoRetalk是一个人物视频生成模型，可基于人物视频和人声音频，生成人物讲话口型与输入音频相匹配的新视频。

> **重要**
>
> 本文档仅适用于华北2（北京）地域，且必须使用该地域的[API Key](https://bailian.console.aliyun.com/model/settings/api-key)。

<a id="模型概览"></a>

<a id="2c5fd145d6aab"></a>

## 模型概览

<a id="模型效果示例"></a>

<a id="0b4fcc80c1dfp"></a>

### 模型效果示例

| 输入示例 | 输出示例 |
| --- | --- |
| 人物视频：<br><br>人声音频： |  |

<a id="资费与限流"></a>

<a id="babef7c7bcvfy"></a>

## 资费与限流

| 模型名称 | 单价 | **免费额度**[（查看）](../../../model-user-guide/test-1/new-free-quota.md) | 任务下发接口RPS限制 | 同时处理中任务数量 |
| --- | --- | --- | --- | --- |
| videoretalk | 后付费，按生成视频的时长计费：0.08元/秒 | 1800秒 | 1 | 1<br><br>（在同一时刻，只有1个作业实际处于运行状态，其他队列中的作业处于排队状态） |

<a id="模型调用"></a>

<a id="a71eae78f68zw"></a>

### 模型调用

-   声动人像VideoRetalk模型支持后付费调用。目前仅支持通过API调用，不支持在阿里云百炼的控制台在线体验。
-   调用“声动人像VideoRetalk”模型，输入画面清晰且正面镜头的人物视频，以及人声清晰的音频文件，即可生成人物口型替换视频。具体操作请参见[VideoRetalk视频生成](videoretalk/videoretalk-api.md)。
