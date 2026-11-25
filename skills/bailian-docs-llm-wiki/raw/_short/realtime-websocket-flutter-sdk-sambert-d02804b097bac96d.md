# Sambert Flutter SDK

Sambert 的 Flutter SDK 接入指南，包含 Dart 调用流程、请求参数和事件。

Sambert 使用单向流式接口。应用一次提交完整文本，并分片接收合成音频。

<a id="前提条件"></a>

## 前提条件

-   为目标平台配置 Flutter 开发环境。示例工程要求 Dart 3.4 及以上、低于 4.0。
-   [获取 API Key](../model-api-reference/preparations/get-api-key.md)。请选择与 API Key 同地域的服务地址。使用工作空间专属域名时，还需获取[业务空间 ID](../model-user-guide/get-started-with-models/regions.md)。

移动端应用请勿硬编码长期 API Key。调用支持临时 API Key 的模型时，由应用服务端[生成临时 API Key](../model-api-reference/more-about-models/generate-temporary-api-key.md)并下发给客户端。

<a id="安装-sdk"></a>

### 安装 SDK

打开[移动端语音 SDK 选型与下载](https://help.aliyun.com/zh/model-studio/sdk-selection-and-download)，在 **Flutter** 标签下下载安装包并解压。

将解压后的 SDK 目录复制到 Flutter 项目的 `packages/aliyun_neonui`，在 `pubspec.yaml` 中添加本地依赖。

<a id="code-block"></a>

```yaml
dependencies:
  aliyun_neonui:
    path: packages/aliyun_neonui
```

运行 `flutter pub get`，然后在 Dart 文件中导入 SDK。

<a id="code-block-2"></a>

```dart
import 'package:aliyun_neonui/neonui.dart';
```

<a id="快速开始"></a>

## 快速开始

<a id="运行示例"></a>

### 运行示例

1.  连接目标设备，在解压后的 SDK 目录中运行以下命令。
    
    <a id="code-block-3"></a>
    
    ```bash
    cd example
    flutter pub get
    flutter run
    ```
    
2.  打开示例应用首页的 **百炼(DashScope)**，选择服务地址并填写 **API Key**。使用工作空间专属域名时，同时填写 **WorkspaceId**。
    
3.  打开 **Sambert 单向流式语音合成** 并运行示例。
    

完整示例见整合包中的 `example/lib/pages/dashscope/dash_sambert_tts_page.dart`。

<a id="包内示例提供的模型"></a>

### 包内示例提供的模型

-   `sambert-zhinan-v1`

<a id="调用步骤"></a>

### 调用步骤

下面的方法通过 `NativeNui()` 获取的实例调用。

1.  先订阅 `ttsEventStream` 和 `ttsAudioStream`，再调用以下方法。
    
2.  下面用请求参数中的连接 JSON 作为 `initJson`。将任务参数按键值传给 `ttsSetParam`。
    
    <a id="code-block-4"></a>
    
    ```dart
    await nui.ttsInitialize(params: initJson);
    for (final entry in taskParams.entries) {
      await nui.ttsSetParam(entry.key, entry.value);
    }
    await nui.ttsStart(priority: '1', taskId: '', text: '你好，欢迎使用语音合成。');
    ```
    
    初始化后逐个设置任务参数。调用 `ttsStart` 发送完整文本，应用从音频流读取返回音频。
    
3.  收到 `TTS_EVENT_END` 后可继续处理已收到的音频。任务用完后调用 `ttsRelease`。
    

<a id="请求参数"></a>

## 请求参数

下例使用包内示例的一个模型。需要调整其他字段时，可参考同一整合包的 `example/lib/dashscope_params.dart`。更多参数说明见[Android SDK](sambert-android-sdk-8827dfd4fba2386d.md)、[iOS SDK](sambert-ios-sdk-3a58fd71fde42af6.md)、[HarmonyOS SDK](sambert-harmonyos-sdk-6ffde1be395ffb11.md)。

将 `YOUR_WS_HOST` 替换为相应地域的 WebSocket 主机名，`YOUR_DEVICE_ID` 替换为设备标识，并按所选地域设置 `YOUR_API_KEY`。

<a id="连接参数"></a>

### 连接参数

示例中的 JSON 作为字符串传入 Dart 方法。

<a id="code-block-5"></a>

```json
{
  "url": "wss://YOUR_WS_HOST/api-ws/v1/inference",
  "device_id": "YOUR_DEVICE_ID",
  "mode_type": "2"
}
```

<a id="任务参数"></a>

### 任务参数

通过 `ttsSetParam(key, value)` 逐项设置任务参数。表中的数值也以字符串传入。

<a id="code-block-6"></a>

```json
{
  "apikey": "YOUR_API_KEY",
  "model": "sambert-zhinan-v1",
  "format": "pcm",
  "enable_audio_decoder": "0",
  "sample_rate": "48000",
  "volume": "50",
  "rate": "1.0",
  "pitch": "1.0"
}
```

Sambert 用 `model` 设置音色对应的模型 ID。下例与包内 48 kHz 音色示例一致，应用按相同采样率播放。

<a id="接口参考"></a>

## 接口参考

<a id="方法"></a>

### 方法

返回 `Future<int>` 的方法中，结果码 `0` 表示成功。

| 方法签名 | 用途 |
| --- | --- |
| `Future<int> ttsInitialize({required String params, int logLevel = 0, bool saveLog = false})` | 初始化 SDK。`params` 为连接参数 JSON 字符串。 |
| `Future<int> ttsSetParam(String key, String value)` | 逐项设置字符串参数。 |
| `Future<int> ttsStart({required String priority, required String taskId, required String text})` | 提交完整待合成文本，示例使用 `priority: '1'`、`taskId: ''`。 |
| `Future<int> ttsPause()` | 暂停合成。 |
| `Future<int> ttsResume()` | 继续合成。 |
| `Future<int> ttsCancel(String taskId)` | 按任务 ID 取消合成。 |
| `Future<String?> ttsGetParam(String key)` | 读取指定参数，可用 `error_msg` 查看错误详情。 |
| `Future<int> ttsRelease()` | 释放 SDK 资源。 |

<a id="事件与音频流"></a>

### 事件与音频流

事件从 `ttsEventStream` 读取。收到 Dart Map 时，以 `event` 识别事件名，任务类事件的 `resultCode` 可用于判断错误。

音频流 `ttsAudioStream` 返回音频分片。应用负责播放音频。

| 事件 | 用途 |
| --- | --- |
| `TTS_EVENT_START` | 合成或回复音频开始 |
| `TTS_EVENT_END` | 任务或当前音频输出完成 |
| `TTS_EVENT_CANCEL` | 任务已取消 |
| `TTS_EVENT_ERROR` | 任务失败 |
