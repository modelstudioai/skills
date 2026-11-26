# 移动端语音 SDK 选型与下载

下载用于百炼语音服务的 NUI 移动端 SDK，按平台和版本应用号选择整合包，并查看兼容要求与更新说明。

<a id="版本选择"></a>

## 版本选择

版本号（如 `2.7.4`）表示 SDK 的发布版本；版本应用号（如 `037`、`047`）表示整合包的能力组合。

> **说明**
>
> V2.7.3 及以前版本不支持百炼新版工作空间域名，使用该域名会导致 SDK 初始化或连接失败。请使用以下旧版通用地址：
>
> -   华北2（北京）：`wss://dashscope.aliyuncs.com/api-ws/v1/inference`
> -   新加坡：`wss://dashscope-intl.aliyuncs.com/api-ws/v1/inference`
>
> V2.7.4 及以上版本支持新版工作空间域名。

下列版本应用号的最新标准整合包支持以下百炼云端能力：

-   Qwen-Audio-TTS/CosyVoice 语音合成
-   Sambert 语音合成
-   Qwen-Audio-ASR/Fun-ASR 语音识别/录音文件识别
-   Gummy 语音识别/翻译
-   Qwen-Livetranslate-Realtime 实时音频翻译
-   Qwen-Audio-Realtime 实时语音对话

各版本应用号的端侧能力如下。

| 版本应用号 | 端侧语音合成 | 端侧语音唤醒 | 端侧回声消除和人声检测 |
| --- | --- | --- | --- |
| `039` | 支持 | 支持 | 不支持 |
| `038` | 支持 | 不支持 | 不支持 |
| `037` | 不支持 | 不支持 | 不支持 |
| `049` | 支持 | 支持 | 支持 |
| `047` | 不支持 | 不支持 | 支持 |

<a id="sdk-下载"></a>

## SDK 下载

请按平台和所需功能选择 SDK。

> **说明**
>
> 标准整合包用于常规集成。若工程中已集成同名 SDK，可使用改名整合包解决包冲突。

<a id="sec-tabs"></a>

<a id="android"></a>

<a id="android-h4"></a>

#### Android

平台更新时间：2026-10-27。

包名：`com.alibaba.idst.nui`。支持 Android 5.0 及以上版本（API Level 21），架构为 `armeabi-v7a`、`arm64-v8a`、`x86_64`。

<a id="sec-tabs-2"></a>

<a id="标准整合包"></a>

<a id="标准整合包-h4"></a>

#### 标准整合包

| 版本应用号 | 版本 | 下载 | MD5 |
| --- | --- | --- | --- |
| `039` | 2.7.6 | [V2.7.6-039-20261027\_Android\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/iiskgd/V2.7.6-039-20261027_Android_TLS.tar.gz) | `e4267e1e2e159a58bf0253abe4c057da` |
| `038` | 2.7.6 | [V2.7.6-038-20261027\_Android\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/lvtdjr/V2.7.6-038-20261027_Android_TLS.tar.gz) | `f1cfea702d60dec1dd9d704386643838` |
| `037` | 2.7.6 | [V2.7.6-037-20261027\_Android\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/izmhvf/V2.7.6-037-20261027_Android_TLS.tar.gz) | `4aa0469122d0656d6ffea299d52e0ff7` |
| `049` | 2.7.6 | [V2.7.6-049-20261027\_Android\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/xrefej/V2.7.6-049-20261027_Android_TLS.tar.gz) | `31490f3e3cf230ec14a3c1ae5b01a08c` |
| `047` | 2.7.6 | [V2.7.6-047-20261027\_Android\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/yudoni/V2.7.6-047-20261027_Android_TLS.tar.gz) | `c1191f473ca119a32a8f5078b9b4fc28` |

<a id="改名整合包"></a>

<a id="改名整合包-h4"></a>

#### 改名整合包

| 版本应用号 | 版本 | 下载 | MD5 |
| --- | --- | --- | --- |
| `039` | 2.7.6 | [V2.7.6-039-20261027\_Android\_MIT\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/juzefk/V2.7.6-039-20261027_Android_MIT_TLS.tar.gz) | `15280f242d8be8b830fa2a0aa557ecde` |
| `038` | 2.7.6 | [V2.7.6-038-20261027\_Android\_MIT\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/hxfnhb/V2.7.6-038-20261027_Android_MIT_TLS.tar.gz) | `cd1ef2a378528df49ce218726946c533` |
| `037` | 2.7.6 | [V2.7.6-037-20261027\_Android\_MIT\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/zhwuki/V2.7.6-037-20261027_Android_MIT_TLS.tar.gz) | `ee2e1f730d43ecf3c4e06c6a1ba06157` |

<a id="ios"></a>

<a id="ios-h4"></a>

#### iOS

平台更新时间：2026-10-26。

最低支持 iOS 12，架构为 `arm64-device`、`arm64-simulator`、`x86_64-simulator`。

<a id="sec-tabs-3"></a>

<a id="标准整合包-2"></a>

<a id="标准整合包-2-h4"></a>

#### 标准整合包

| 版本应用号 | 版本 | 下载 | MD5 |
| --- | --- | --- | --- |
| `039` | 2.7.6 | [V2.7.6-039-20261026\_iOS\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/dtvkml/V2.7.6-039-20261026_iOS_TLS.tar.gz) | `89853d24a05bbc60d488cfc38fcd097f` |
| `038` | 2.7.6 | [V2.7.6-038-20261026\_iOS\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/vzecoc/V2.7.6-038-20261026_iOS_TLS.tar.gz) | `fb45f51aa78b907c641c3b7b1c78ae1c` |
| `037` | 2.7.6 | [V2.7.6-037-20261026\_iOS\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/rjhipo/V2.7.6-037-20261026_iOS_TLS.tar.gz) | `a4a73c7c87be781d450a73865fe0fe7f` |
| `049` | 2.7.6 | [V2.7.6-049-20261026\_iOS\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/spcfhl/V2.7.6-049-20261026_iOS_TLS.tar.gz) | `bb751b35b2d211385072affa2b97d9ab` |
| `047` | 2.7.6 | [V2.7.6-047-20261026\_iOS\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261027/dbnffx/V2.7.6-047-20261026_iOS_TLS.tar.gz) | `98b5e7354edd95b2249efe2e37dc5c0f` |

<a id="改名整合包-2"></a>

<a id="改名整合包-2-h4"></a>

#### 改名整合包

| 版本应用号 | 版本 | 下载 | MD5 |
| --- | --- | --- | --- |
| `039` | 2.7.2 | [V2.7.2-039-20260225\_iOS\_MIT\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260225/bcousy/V2.7.2-039-20260225_iOS_MIT_OpenSSL.tar.gz) | `c1192a125b0239ff295cf9c9ff598807` |
| `038` | 2.7.2 | [V2.7.2-038-20260225\_iOS\_MIT\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260225/luwrff/V2.7.2-038-20260225_iOS_MIT_OpenSSL.tar.gz) | `d9da2453a60bc69d43b9a35bd0c9f303` |
| `037` | 2.7.2 | [V2.7.2-037-20260225\_iOS\_MIT\_TLS.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260225/lfkafa/V2.7.2-037-20260225_iOS_MIT_OpenSSL.tar.gz) | `bb3cd0a35d12e3fc0c35b016f0788fbf` |

<a id="harmonyos"></a>

<a id="harmonyos-h4"></a>

#### HarmonyOS

平台更新时间：2026-10-15。

<a id="sec-tabs-4"></a>

<a id="标准整合包-3"></a>

<a id="标准整合包-3-h4"></a>

#### 标准整合包

| 版本应用号 | 版本 | 下载 | MD5 |
| --- | --- | --- | --- |
| `037` | 2.7.5 | [2.7.5-037-20261015\_Harmony.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261016/eogmyr/2.7.5-037-20261015_Harmony.tar.gz) | `39871fc03d544097e70c8348f24a16e4` |
| `047` | 2.7.5 | [2.7.5-047-20261015\_Harmony.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261015/hizley/2.7.5-047-20261015_Harmony.tar.gz) | `ed8809877ada63dbddde7adc8e414d4c` |
| `049` | 2.7.5 | [2.7.5-049-20261015\_Harmony.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261015/wgnamq/2.7.5-049-20261015_Harmony.tar.gz) | `495f678e3b33ec1ef1b5d091703d8e33` |

<a id="改名整合包-3"></a>

<a id="改名整合包-3-h4"></a>

#### 改名整合包

暂未提供。

<a id="flutter"></a>

<a id="flutter-h4"></a>

#### Flutter

平台更新时间：2026-10-23。

| 版本应用号 | 版本 | 下载 | MD5 |
| --- | --- | --- | --- |
| `037` | 2.7.5 | [flutter\_neonui\_sdk\_V2.7.5\_20261023.tar.gz](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20261023/ceocie/flutter_neonui_sdk_V2.7.5_20261023.tar.gz) | `917e80c3cb5bc8ab7d95ca2d9522643b` |

<a id="更新说明"></a>

## 更新说明

<a id="v2-7-6"></a>

### V2.7.6

-   非实时识别支持 Qwen-Audio-ASR 新模型。

<a id="v2-7-5"></a>

### V2.7.5

-   优化实时识别断网续传功能。
-   支持 Qwen-Audio-ASR 新模型。
-   修复万能参数设置接口失效的问题。

<a id="v2-7-4"></a>

### V2.7.4

-   新增 Qwen-Audio-Realtime 实时语音对话。
-   支持百炼新版工作空间域名。

<a id="v2-7-3"></a>

### V2.7.3

-   新增实时音频翻译功能。
-   新增断网续传功能和断网报错。

<a id="v2-7-2"></a>

### V2.7.2

-   修复缺陷。

<a id="v2-7-1"></a>

### V2.7.1

-   修复缺陷。

<a id="v2-7-0"></a>

### V2.7.0

-   新增百炼语音识别与语音合成支持。
-   语音合成新增将 Opus 和 MP3 解码为 PCM 的能力。
-   精简 OpenSSL 以减少包大小。
