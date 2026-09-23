# 实时会议 - API调用方法介绍

本文介绍会议纪要实时会议转写API的调用流程。

## 介绍

通过实时转写系列API，您可以实现：

1.  创建实时会议并通过WebSocket API流式传入音频，并实时获取语音识别结果和翻译结果，从而实现字幕实时上屏等功能。
2.  会议暂停及恢复。
3.  会议结束后，您可以获取本会议的智能纪要。

## 调用流程

### 创建会议

您首先需要调用CreateTask API创建一个实时会议，并获取会议的dataId，详细调用过程及配置参数请参考[CreateTask](raw/_short/tingwu-meeting-api-create-task-0e89c21ae62d15f6.md)。

### 调用WebSocket API实现流式识别

之后您可以通过调用WebSocket API流式传入音频，并获取实时识别结果和翻译结果，详细调用过程及配置参数请参考[音频转写交互协议（WebSocket）](raw/_short/tingwu-meeting-api-websocket-56258086daf1459d.md)。

会议中您可以通过断开WebSocket连接暂停会议。

在dataId的有效期（24h）内，您可以通过再次建立WebSocket连接恢复指定会议。

### 结束会议并创建会议纪要

当您的会议结束后，您可以通过调用CreateTask API创建会议纪要分析任务，详细调用过程及配置参数请参考[CreateTask](raw/_short/tingwu-meeting-api-create-task-0e89c21ae62d15f6.md)。

注意：会议结束后，您必须主动调用CreateTask API才能创建会议纪要分析任务，听悟Agent不会自动为您创建分析任务。

### 获取会议纪要生成状态及结果

之后您可以通过调用GetTask API获取纪要生成状态及结果，详细调用过程和返回值请参考[GetTask](raw/_short/tingwu-meeting-api-get-task-17f4492d4e1dcd72.md)。
