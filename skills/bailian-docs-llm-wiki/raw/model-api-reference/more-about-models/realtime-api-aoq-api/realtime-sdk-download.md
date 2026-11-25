# SDK 下载

本文介绍如何集成各平台的 AOQ SDK 和 AOQ Web SDK，并提供下载链接和版本更新说明。

<a id="集成-sdk"></a>

## 集成 SDK

选择目标平台查看集成步骤。手动集成所需的安装包可在[SDK 发布日志](#sdkdl-h2-aoq)中下载。

<a id="sec-tabs"></a>

<a id="android"></a>

<a id="android-h4"></a>

#### Android

支持 Android 5.0（API 21）及以上版本，提供 `armeabi-v7a` 和 `arm64-v8a` 两种架构。默认音频配置使用 Opus。仅在使用 Opus 编解码时才需要引入插件。

<a id="sec-tabs-2"></a>

<a id="通过-maven-central-集成-推荐"></a>

<a id="通过-maven-central-集成-推荐-h4"></a>

#### 通过 Maven Central 集成（推荐）

1.  在项目的 `settings.gradle` 中，确认 `dependencyResolutionManagement.repositories` 包含 `mavenCentral()`。
    
    <a id="code-block"></a>
    
    ```groovy
    dependencyResolutionManagement {
        repositories {
            google()
            mavenCentral()
        }
    }
    ```
    
    如果旧项目在项目级 `build.gradle` 中管理依赖仓库，将 `mavenCentral()` 加到已有的 `repositories` 中即可。
    
2.  在应用模块的 `build.gradle` 中添加 SDK 和 Opus 插件依赖。
    
    <a id="code-block-2"></a>
    
    ```groovy
    dependencies {
        implementation 'com.alibaba.aoq:aoq-client-sdk:1.4.1'
        implementation 'com.alibaba.aoq:aoq-plugin-opus:1.4.1'
    }
    ```
    
3.  在 Android Studio 中执行 **Sync Project with Gradle Files**。
    

<a id="手动导入-aar-和插件"></a>

<a id="手动导入-aar-和插件-h4"></a>

#### 手动导入 AAR 和插件

1.  下载 `AoqClientSdk-release.aar` 并放到 `app/libs/`。使用 Opus 编解码时，同时下载 `libPluginOpus.zip`。
    
2.  在 `app/build.gradle` 中添加本地 AAR 依赖。
    
    <a id="code-block-3"></a>
    
    ```groovy
    dependencies {
        implementation files('libs/AoqClientSdk-release.aar')
    }
    ```
    
3.  使用 Opus 编解码时，解压插件包，将 `libPluginOpus.so` 按 ABI 放到 `app/src/main/jniLibs/` 下。
    
    <a id="code-block-4"></a>
    
    ```text
    app/
    ├── libs/
    │   └── AoqClientSdk-release.aar
    └── src/main/jniLibs/
        ├── armeabi-v7a/libPluginOpus.so
        └── arm64-v8a/libPluginOpus.so
    ```
    
    只保留应用支持的 ABI，并确保 SDK 与插件的架构一致。使用默认目录时无需配置 `sourceSets`；如果通过 `jniLibs.srcDirs` 配置了其他目录，请将插件放到该目录。
    
4.  在 Android Studio 中同步并构建项目。
    

<a id="ios"></a>

<a id="ios-h4"></a>

#### iOS

iOS 安装包仅包含 arm64 真机 framework，不支持模拟器。默认音频配置使用 Opus；不使用 Opus 编解码时，可省略 Opus 插件。仅在使用屏幕共享时才需要引入 `AoqScreenShare`。

<a id="sec-tabs-3"></a>

<a id="通过-cocoapods-集成-推荐"></a>

<a id="通过-cocoapods-集成-推荐-h4"></a>

#### 通过 CocoaPods 集成（推荐）

1.  在 `Podfile` 中添加主 SDK 和 Opus 插件。将 `YourApp` 替换为实际的主应用 target 名。
    
    <a id="code-block-5"></a>
    
    ```ruby
    platform :ios, '13.0'
    use_frameworks!
    
    target 'YourApp' do
      pod 'AoqClientSdk', '1.4.1'
      pod 'AoqPluginOpus', '1.4.1'
    end
    ```
    
2.  如需屏幕共享，在主应用和 Broadcast Upload Extension 的 target 中均添加 `AoqScreenShare`。用以下配置替换上一步的 target 定义，保留 `platform` 和 `use_frameworks!`，并将两个 target 名替换为实际名称。
    
    <a id="code-block-6"></a>
    
    ```ruby
    target 'YourApp' do
      pod 'AoqClientSdk', '1.4.1'
      pod 'AoqPluginOpus', '1.4.1'
      pod 'AoqScreenShare', '1.4.1'
    end
    
    target 'YourBroadcastExtension' do
      pod 'AoqScreenShare', '1.4.1'
    end
    ```
    
3.  在 `Podfile` 所在目录执行以下命令，然后通过生成的 `.xcworkspace` 打开项目。
    
    <a id="code-block-7"></a>
    
    ```bash
    pod install
    ```
    

主 SDK 不会自动引入 Opus 或屏幕共享 Pod。使用相应功能时，需要显式声明依赖。

<a id="手动导入-framework"></a>

<a id="手动导入-framework-h4"></a>

#### 手动导入 framework

1.  下载并解压 `AoqClientSdk.framework.zip`，将 framework 导入 Xcode 项目。使用 Opus 编解码时，同时导入 `PluginOpus.framework.zip` 解压后的 framework。
2.  在主应用 target 的 **General** > **Frameworks, Libraries, and Embedded Content** 中，为导入的动态 framework 选择 **Embed & Sign**。
3.  如需屏幕共享，下载并解压同版本的 `AoqScreenShare.framework.zip`，在主应用中设置 **Embed & Sign**。在 Broadcast Upload Extension 的 **Link Binary With Libraries** 中链接该 framework，并在 **Runpath Search Paths** 中添加 `@executable_path/../../Frameworks`。

App Group 为可选配置。如需使用，主应用和 Broadcast Upload Extension 必须使用同一个 App Group。屏幕采集接口参见 [iOS SDK](aoq-ios-sdk-reference.md#aoq-api-category-10)。

<a id="harmonyos"></a>

<a id="harmonyos-h4"></a>

#### HarmonyOS

<a id="sec-tabs-4"></a>

<a id="手动导入-har-和插件"></a>

<a id="手动导入-har-和插件-h4"></a>

#### 手动导入 HAR 和插件

1.  下载 `AoqClientSdk.har` 并放到项目根目录下的 `libs/`。默认音频配置使用 Opus；使用 Opus 编解码时，同时下载 `libPluginOpus.zip`。
    
2.  在 `entry/oh-package.json5` 的 `dependencies` 中添加本地依赖，保留其他配置。
    
    <a id="code-block-8"></a>
    
    ```json
    {
      "dependencies": {
        "@aoq/client-sdk": "file:../libs/AoqClientSdk.har"
      }
    }
    ```
    
3.  使用 Opus 编解码时，解压插件包，将 `libPluginOpus.so` 放到应用模块的对应架构目录。v1.4.2 的 HAR 包含 arm64 原生库，请使用 arm64 插件。
    
    <a id="code-block-9"></a>
    
    ```text
    libs/AoqClientSdk.har
    entry/libs/arm64-v8a/libPluginOpus.so
    ```
    
4.  在 DevEco Studio 中同步依赖并构建项目。业务代码从 `@aoq/client-sdk` 导入所需的 SDK 类型。
    

<a id="windows"></a>

<a id="windows-h4"></a>

#### Windows

<a id="sec-tabs-5"></a>

<a id="手动导入-sdk"></a>

<a id="手动导入-sdk-h4"></a>

#### 手动导入 SDK

1.  下载并解压 `AoqClientSdk-windows-x64.zip`，使用 x64 构建配置。
2.  将包内的 `include/` 加到头文件搜索路径，将 `lib/` 加到库搜索路径，并链接 `AoqClientSdk.lib`。
3.  将 `bin/` 中的 `AoqClientSdk.dll` 和 `alivcffmpeg.dll` 复制到可执行文件所在目录。默认音频配置使用 Opus；使用 Opus 编解码时，一并复制包内的 `PluginOpus.dll`，无需另外下载插件。

接口用法参见 [Windows SDK](aoq-windows-sdk-reference.md)。

<a id="macos"></a>

<a id="macos-h4"></a>

#### macOS

<a id="sec-tabs-6"></a>

<a id="手动导入-framework-2"></a>

<a id="手动导入-framework-2-h4"></a>

#### 手动导入 framework

1.  下载并解压 macOS 的 `AoqClientSdk.framework.zip`，不要使用 iOS 安装包。默认音频配置使用 Opus；使用 Opus 编解码时，同时下载并解压同版本的 `PluginOpus.framework.zip`。
2.  将主 SDK 和按需引入的插件 framework 导入 Xcode。在应用 target 的 **Frameworks, Libraries, and Embedded Content** 中选择 **Embed & Sign**。
3.  保留主 framework 的完整目录结构、符号链接、资源以及 `openhevc.framework` 等内置依赖，不要只复制主二进制文件。

接口用法参见 [macOS SDK](aoq-macos-sdk-reference.md)。

<a id="electron"></a>

<a id="electron-h4"></a>

#### Electron

<a id="sec-tabs-7"></a>

<a id="通过-npm-集成-推荐"></a>

<a id="通过-npm-集成-推荐-h4"></a>

#### 通过 npm 集成（推荐）

在项目根目录执行以下命令：

<a id="code-block-10"></a>

```bash
npm install aoq-electron-sdk@1.4.0-59463182
```

使用示例中的完整 npm 版本号，不要简写为 `1.4.0`。

<a id="安装本地-tgz-包"></a>

<a id="安装本地-tgz-包-h4"></a>

#### 安装本地 tgz 包

下载 `aoq-electron-sdk-1.4.0-59463182.tgz`，放到项目的 `libs/` 后执行以下命令：

<a id="code-block-11"></a>

```bash
npm install ./libs/aoq-electron-sdk-1.4.0-59463182.tgz
```

使用 npm 安装完整包。安装和打包时保留原生模块、依赖库和目录结构，不要单独提取 `.node` 文件或复制原生库。接口用法参见 [Electron SDK](aoq-electron-sdk-reference.md)。

<a id="linux-c-python"></a>

<a id="linux-c-python-h4"></a>

#### Linux C++ / Python

<a id="sec-tabs-8"></a>

<a id="手动导入-sdk-2"></a>

<a id="手动导入-sdk-2-h4"></a>

#### 手动导入 SDK

1.  根据部署环境选择 `x86_64` 或 `arm64` 对应的 `AoqClientSdk.zip` 并解压，不要混用不同架构的库。
2.  **C++**：将包内的 `include/` 加到头文件搜索路径，链接 `libAoqClientSdk.so`，并确保运行时的动态库搜索路径包含该库所在目录。接口用法参见 [Linux C++ SDK](aoq-linux-cpp-sdk-reference.md)。
3.  **Python**：使用包内的 `aoq_client_sdk.py`，保留它与 `libAoqClientSdk.so` 的目录关系，并将模块所在目录加到 Python 模块搜索路径。接口用法参见 [Linux Python SDK](aoq-linux-python-sdk-reference.md)。

<a id="web"></a>

<a id="web-h4"></a>

#### Web

<a id="sec-tabs-9"></a>

<a id="通过-npm-集成-推荐-2"></a>

<a id="通过-npm-集成-推荐-2-h4"></a>

#### 通过 npm 集成（推荐）

在项目根目录执行以下命令：

<a id="code-block-12"></a>

```bash
npm install aoq-web-sdk@1.0.1-60040320
```

<a id="安装本地-tgz-包-2"></a>

<a id="安装本地-tgz-包-2-h4"></a>

#### 安装本地 tgz 包

下载 `aoq-web-sdk-1.0.1-60040320.tgz`，放到项目的 `libs/` 后执行以下命令：

<a id="code-block-13"></a>

```bash
npm install ./libs/aoq-web-sdk-1.0.1-60040320.tgz
```

Web SDK 独立维护版本号，不需要引入原生 SDK 的 Opus 插件。接口用法参见 [Web SDK](aoq-web-sdk-reference.md)。

<a id="sdk-发布日志"></a>

<a id="sdkdl-h2-aoq"></a>

## SDK 发布日志

<a id="sdkdl-h2-aoq-web"></a>

<a id="aoq-sdk下载"></a>

<a id="aoq-web-sdk下载"></a>

<a id="sdkdl-h2-websocket"></a>

<a id="websocket-sdk下载"></a>

<table><thead><tr><th><strong>版本</strong></th><th><strong>平台</strong></th><th><strong>下载</strong></th><th><strong>更新日期</strong></th><th><strong>更新说明</strong></th></tr></thead><tbody><tr><td rowspan="3"><p>v1.4.2</p></td><td><p>Android</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f91ce.aar">AoqClientSdk-release.aar</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939f.zip">libPluginOpus.zip</a></p></td><td rowspan="3"><p>2026-11-24</p></td><td rowspan="3"><ol><li>新增 TTS 播放前的 PCM 音频数据回调，应用可自行缓存音频并播放。</li><li>修复已知的稳定性问题。</li></ol></td></tr><tr><td><p>iOS</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f91cd.zip">AoqClientSdk.framework.zip</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f91c3.zip">AoqScreenShare.framework.zip</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939d.zip">PluginOpus.framework.zip</a></p></td></tr><tr><td><p>HarmonyOS</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f91c1.har">AoqClientSdk.har</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9393.zip">libPluginOpus.zip</a></p></td></tr><tr><td rowspan="3"><p>v1.4.1</p></td><td><p>Android</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f919e.aar">AoqClientSdk-release.aar</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939f.zip">libPluginOpus.zip</a></p></td><td rowspan="3"><p>2026-11-23</p></td><td rowspan="3"><ol><li>优化 HarmonyOS 平台日志与统计数据上报的兼容性和稳定性。</li><li>外部音频输入支持数据驱动模式。</li><li>Android SDK 不再内置屏幕共享权限声明。</li></ol></td></tr><tr><td><p>iOS</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f919d.zip">AoqClientSdk.framework.zip</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9190.zip">AoqScreenShare.framework.zip</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939d.zip">PluginOpus.framework.zip</a></p></td></tr><tr><td><p>HarmonyOS</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f919c.har">AoqClientSdk.har</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9393.zip">libPluginOpus.zip</a></p></td></tr><tr><td><p>v1.0.1</p></td><td><p>Web</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/files/6a4b3c2d1e0f90ff.tgz">aoq-web-sdk-1.0.1-60040320.tgz</a></p><p>也可以通过 npm 安装：</p><p><code>npm install aoq-web-sdk@1.0.1-60040320</code></p></td><td><p>2026-11-16</p></td><td><ol><li>发布 AOQ Web SDK，支持在浏览器中接入实时音视频与数据交互能力。</li><li>支持实时音频采集与播放，满足双向语音交互需求。</li><li>支持视频采集、本地预览、远端视频渲染及摄像头切换。</li><li>支持双向数据消息收发，便于业务指令与交互信息传递。</li><li>提供会话管理、连接状态通知、异常回调及运行统计能力。</li></ol></td></tr><tr><td><p>v1.4.1</p></td><td><p>Linux</p></td><td><p><code>x86_64</code>: <a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/files/6a4b3c2d1e0f90fb.zip">AoqClientSdk.zip</a></p><p><code>arm64</code>: <a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/zh/files/6a4b3c2d1e0f90fa.zip">AoqClientSdk.zip</a></p></td><td><p>2026-11-16</p></td><td><p>支持 Linux 客户端 H.264 编解码。</p></td></tr><tr><td rowspan="7"><p>v1.4.0</p></td><td><p>Android</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f93a6.aar">AoqClientSdk-release.aar</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939f.zip">libPluginOpus.zip</a></p></td><td rowspan="7"><p>2026-10-27</p></td><td rowspan="7"><ol><li>支持从外部输入 H.264 视频。</li><li>优化性能。</li><li>修复已知的稳定性问题。</li></ol></td></tr><tr><td><p>iOS</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9398.zip">AoqClientSdk.framework.zip</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939e.zip">AoqScreenShare.framework.zip</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939d.zip">PluginOpus.framework.zip</a></p></td></tr><tr><td><p>HarmonyOS</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f939c.har">AoqClientSdk.har</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9393.zip">libPluginOpus.zip</a></p></td></tr><tr><td><p>Windows</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9392.zip">AoqClientSdk-windows-x64.zip</a></p></td></tr><tr><td><p>macOS</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f93a1.zip">AoqClientSdk.framework.zip</a></p><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9391.zip">PluginOpus.framework.zip</a></p></td></tr><tr><td><p>Electron</p></td><td><p><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9390.tgz">aoq-electron-sdk-1.4.0-59463182.tgz</a></p><p>也可以通过 npm 安装：</p><p><code>npm install aoq-electron-sdk@1.4.0-59463182</code></p></td></tr><tr><td><p>Linux</p></td><td><p><code>x86_64</code>: <a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9397.zip">AoqClientSdk.zip</a></p><p><code>arm64</code>: <a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9396.zip">AoqClientSdk.zip</a></p></td></tr><tr><td rowspan="7">v1.3.0</td><td>Android</td><td><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9dab.aar">AoqClientSdk-release.aar</a></div><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d8c.zip">libPluginOpus.zip</a></div></td><td rowspan="7">2026-09-18</td><td rowspan="7"><ol><li><p>新增屏幕共享能力。</p></li><li><p>废弃 bitcode。</p></li><li><p>支持远程加载 .so 库。</p></li><li><p>支持从外部设置编码帧最大值。</p></li><li><p>将默认编解码器调整为 Opus。</p></li><li><p>优化性能。</p></li><li><p>修复已知的稳定性问题。</p></li></ol></td></tr><tr><td>iOS</td><td><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d83.zip">AoqClientSdk.framework.zip</a></div><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d82.zip">AoqScreenShare.framework.zip</a></div><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d81.zip">PluginOpus.framework.zip</a></div></td></tr><tr><td>HarmonyOS</td><td><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d80.har">AoqClientSdk.har</a></div><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d87.zip">libPluginOpus.zip</a></div></td></tr><tr><td>Windows</td><td><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d86.zip">AoqClientSdk-windows-x64.zip</a></td></tr><tr><td>macOS</td><td><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d85.zip">AoqClientSdk.framework.zip</a></div><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d84.zip">PluginOpus.framework.zip</a></div></td></tr><tr><td>Electron</td><td><div><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d9b.tgz">aoq-electron-sdk-1.3.0-58586345.tgz</a></div><div>也可以通过 npm 安装：<code>npm install aoq-electron-sdk@1.3.0-58586345</code></div></td></tr><tr><td>Linux</td><td><div>x86_64: <a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d9a.zip">AoqClientSdk.zip</a></div><div>arm64: <a href="https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/files/6a4b3c2d1e0f9d99.zip">AoqClientSdk.zip</a></div></td></tr><tr><td>v1.2.2</td><td>iOS</td><td><a href="https://g-adoc.alcasset.com/media/maas_docs/sfm/common/files/6a4b3c2d1e0f9e68.zip">AoqClientSdk.framework.zip</a></td><td>2026-09-09</td><td><ol><li><p>修复 iOS 通话被系统或第三方语音通话打断后，在中断结束时无法恢复通话的问题。</p></li><li><p>优化 iOS 通话起始阶段的回声抑制效果。</p></li></ol></td></tr><tr><td rowspan="7">v1.2.0</td><td>Android</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/eiejsg/AoqClientSdk-release.aar">AoqClientSdk-release.aar</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/kvogns/libPluginOpus.zip">libPluginOpus.zip</a></div></td><td rowspan="7">2026-08-17</td><td rowspan="7"><ol><li><p>新增macOS平台支持</p></li><li><p>新增Windows平台支持</p></li><li><p>新增Electron平台支持</p></li><li><p>Linux平台同时支持Python和C++接口</p></li><li><p>新增音量检测功能</p></li><li><p>优化性能</p></li><li><p>修复已知的稳定性问题</p></li></ol></td></tr><tr><td>iOS</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/xojbbu/AoqClientSdk.framework.zip">AoqClientSdk.framework.zip</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/hdcfjp/PluginOpus.framework.zip">PluginOpus.framework.zip</a></div></td></tr><tr><td>HarmonyOS</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/txwctz/AoqClientSdk.har">AoqClientSdk.har</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/ogziwz/libPluginOpus.zip">libPluginOpus.zip</a></div></td></tr><tr><td>Windows</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/ryieyw/AoqClientSdk-windows-x64.zip">AoqClientSdk-windows-x64.zip</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/jsooaa/PluginOpus.dll.zip">PluginOpus.dll.zip</a></div></td></tr><tr><td>macOS</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/xwgbgr/AoqClientSdk.framework.zip">AoqClientSdk.framework.zip</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/cusppf/PluginOpus.framework.zip">PluginOpus.framework.zip</a></div></td></tr><tr><td>Electron</td><td><div>安装包：<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/kgxgow/aoq-electron-sdk-1.2.0-57407598.tgz">aoq-electron-sdk-1.2.0-57407598.tgz</a></div><div>也可以通过npm安装：<code>npm install aoq-electron-sdk@1.2.0-57407598</code></div></td></tr><tr><td>Linux</td><td><div>x86_64：<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/duxbqa/AoqClientSdk.zip">AoqClientSdk.zip</a></div><div>arm64：<a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260817/nknxye/AoqClientSdk.zip">AoqClientSdk.zip</a></div></td></tr><tr><td rowspan="4">v1.1.0</td><td>Android</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/mzfhfm/AoqClientSdk-v1.1.0.aar">AoqClientSdk-v1.1.0.aar</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/mnwwkr/libPluginOpus.zip">libPluginOpus.zip</a></div></td><td rowspan="4">2026-07-31</td><td rowspan="4"><ol><li><p>支持ASR模型</p></li><li><p>支持TTS模型</p></li><li><p>支持多模态交互套件</p></li><li><p>新增支持Linux平台</p></li><li><p>优化性能</p></li><li><p>解决已知的稳定性问题</p></li></ol></td></tr><tr><td>iOS</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/bhiqbu/AoqClientSdk-v1.1.0.zip">AoqClientSdk-v1.1.0.zip</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/shapwe/PluginOpus.framework.zip">PluginOpus.framework.zip</a></div></td></tr><tr><td>HarmonyOS</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/qtyubq/AoqClientSdk-v1.1.0.har">AoqClientSdk-v1.1.0.har</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/hugetl/libPluginOpus.zip">libPluginOpus.zip</a></div></td></tr><tr><td>Linux</td><td><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260803/swaqde/AoqClientSdk.zip">AoqClientSdk.zip</a></td></tr><tr><td rowspan="3">v1.0.1</td><td>Android</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/sqsjum/AoqClientSdk-v1.0.1.aar">AoqClientSdk-v1.0.1.aar</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/oxzenn/libPluginOpus.zip">libPluginOpus.zip</a></div></td><td rowspan="3">2026-07-09</td><td rowspan="3"><ol><li><p>支持AOQ协议接入模型/应用</p></li><li><p>支持音视频编解码参数</p></li><li><p>支持音视频设备采集及播放</p></li><li><p>支持自定义外部输入音频采集</p></li><li><p>支持自定义外部输入视频采集</p></li><li><p>支持自定义外部输入视频编码</p></li><li><p>支持控制媒体流的发送</p></li></ol></td></tr><tr><td>iOS</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/vlyumo/AoqClientSdk-v1.0.1.zip">AoqClientSdk-v1.0.1.zip</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/rbvmfq/PluginOpus.framework.zip">PluginOpus.framework.zip</a></div></td></tr><tr><td>HarmonyOS</td><td><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/zwlikp/AoqClientSdk-v1.0.1.har">AoqClientSdk-v1.0.1.har</a></div><div><a href="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260715/wvtyrh/libPluginOpus.zip">libPluginOpus.zip</a></div></td></tr></tbody></table>
