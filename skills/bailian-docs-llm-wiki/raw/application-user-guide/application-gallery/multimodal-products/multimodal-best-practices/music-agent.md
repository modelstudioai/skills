# 接入音乐电台Agent

本文档介绍了音乐电台Agent的功能说明以及通过SDK接入的方法。

## **功能说明**

开启后，随机播放推荐音乐。

当前曲库：纯音乐（无人声）

音乐试听：

音乐名

试听

描述

Hold on a Sec

Chill，放松，愉快，爵士

One Step Closer

奇幻，想象、神秘

The Celebrated Minuet

古典、优雅

Shining Stars

情绪，治愈，平缓

Village Tarantella

异域风情、独特律动

Quick Metal Riff 1

摇滚，亢奋，充满力量感

Patron Saint of Heists

俏皮，节奏感

Painful Disorientation

古典，细腻优雅，俏皮

Jethro on the Run

乡村，欢快，节奏

Joey's Song

治愈，平缓，怀旧

## **通过SDK接入音乐电台Agent**

### **1\. 通过语音或者文本进入音乐电台**

> 语音说：“进入音乐电台”，“打开音乐电台”

> 通过文本指令调用： requestToRespond("prompt", "进入音乐电台"， null)

### **2\. 获取音乐**

成功进入音乐电台，服务会返回一首音乐信息，包含一个可下载的 mp3 链接。 注意，由于语音应用和多模态应用的返回数据格式不同，我们需要分别进行处理。您可以根据您接入的应用类型选择使用。

#### **2.1 使用语音应用接入音乐电台**

解析服务端返回的 RespondingContent 类型结果的 payload.output.extra\_info.tool\_calls。

参数

类型

其他

说明

tool\_calls\[\]

type

String

字段名一般固定为“FUNCTION”。代表 function call

id

String

音乐电台默认为music\_radio

function

name

String

字段为自定义的工具函数名称，与多模态应用的 domain 类似

arguments\[\]

list

插件或者技能下发的参数列表

music\_info

jsonString

音乐资源信息

music\_keyword

String

音乐类型，如“爵士布鲁斯”

```
{
    "tool_calls": [
        {
            "id": "music_radio",
            "function": {
                "name": "play_music",
                "arguments": [
                    {
                        "music_info": "{\"songName\":\"Hold on a Sec\",\"song_transition\":\"\",\"_q_score\":0.8128400446231343,\"source\":\"freePD\",\"_score\":0.0,\"tags\":\"[\\\"杂项_爵士乐\\\",\\\"稍等一下\\\"]\",\"_rc_score\":4.835166,\"_scores\":{\"gte-rerank-v2\":0.0},\"audios\":\"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/FreePD_mp3s/Miscellaneaous_Jazz_mp3/Hold%20on%20a%20Sec.mp3\",\"_id\":\"2102\",\"id\":\"2102\",\"category\":\"Miscellaneaous_Jazz\",\"songId\":7877949454}"
                    },
                    {
                        "music_keyword": "爵士布鲁斯"
                    }
                ]
            },
            "type": "FUNCTION"
        }
    ]
}
```

#### **2.2 使用多模态应用接入音乐电台**

解析服务端返回的 RespondingContent 类型结果的 payload.output.extra\_info.commands。

参数

类型

说明

commands\[\]

intent\_info

String

多模态意图

domain

String

音乐电台默认为music\_radio

intent

String

意图，如open\_music\_radio打开音乐电台等

name

String

play\_music

params\[\]

object.music\_info

jsonString

音乐资源信息,包含音量链接地址等

object.music\_keyword

音乐类型，如“爵士布鲁斯”

```
[
    {
        "intent_info": {
            "domain": "music_radio",
            "intent": "open_music_radio"
        },
        "name": "play_music",
        "params": [
            {
                "name": "music_info",
                "normValue": "{\"songName\":\"Lukewarm Banjo\",\"song_transition\":\"\",\"_q_score\":0.9366762545655505,\"source\":\"freePD\",\"_score\":0.0,\"tags\":\"[\\\"杂项_乡村\\\",\\\"不冷不热的五弦琴\\\"]\",\"_rc_score\":28.435673,\"_scores\":{\"gte-rerank-v2\":0.0},\"audios\":\"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/FreePD_mp3s/Miscellaneaous_Country_mp3/Lukewarm%20Banjo.mp3\",\"_id\":\"2003\",\"id\":\"2003\",\"category\":\"Miscellaneaous_Country\",\"songId\":1046525568}"
            },
            {
                "name": "music_keyword",
                "normValue": "乡村"
            }
        ]
    }
]
```

### **3\. 音乐播放**

我们下发的音乐为URL形式的MP3 文件链接。您在获取URL后需要下载或使用网络播放器播放这个URL文件。

-   以 Android 为例。我们提供一个URL MP3 播放器示例代码。您可以在项目中集成这个示例。
    

```
package com.tongyi.multimodal_dialog.utils;

import android.media.MediaPlayer;
import android.util.Log;

import java.io.IOException;

/**
 * 网络MP3播放工具类
 * 支持通过URL播放MP3文件，提供播放、停止和播放完成回调功能
 */
public class NetworkMp3Player {
    private static final String TAG = "NetworkMp3Player";
    
    private MediaPlayer mediaPlayer;
    private OnPlayCallback playCallback;
    private boolean isPlaying = false;
    private String currentUrl = null;

    /**
     * 播放回调接口
     */
    public interface OnPlayCallback {
        /**
         * 播放开始回调
         */
        void onPlayStart();

        /**
         * 播放完成回调
         */
        void onPlayComplete();

        /**
         * 播放错误回调
         * @param error 错误信息
         */
        void onPlayError(String error);
    }

    public NetworkMp3Player() {
        initMediaPlayer();
    }

    /**
     * 初始化MediaPlayer
     */
    private void initMediaPlayer() {
        if (mediaPlayer == null) {
            mediaPlayer = new MediaPlayer();
            mediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
                @Override
                public void onCompletion(MediaPlayer mp) {
                    isPlaying = false;
                    if (playCallback != null) {
                        playCallback.onPlayComplete();
                    }
                }
            });

            mediaPlayer.setOnErrorListener(new MediaPlayer.OnErrorListener() {
                @Override
                public boolean onError(MediaPlayer mp, int what, int extra) {
                    isPlaying = false;
                    String errorMsg = "播放错误: what=" + what + ", extra=" + extra;
                    Log.e(TAG, errorMsg);
                    if (playCallback != null) {
                        playCallback.onPlayError(errorMsg);
                    }
                    return true;
                }
            });

            mediaPlayer.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
                @Override
                public void onPrepared(MediaPlayer mp) {
                    if (playCallback != null) {
                        playCallback.onPlayStart();
                    }
                    mediaPlayer.start();
                    isPlaying = true;
                }
            });
        }
    }

    /**
     * 播放网络MP3
     * @param url MP3文件的URL地址
     * @param callback 播放回调
     */
    public void play(String url, OnPlayCallback callback) {
        if (url == null || url.isEmpty()) {
            if (callback != null) {
                callback.onPlayError("URL不能为空");
            }
            return;
        }

        this.playCallback = callback;
        this.currentUrl = url; // 保存当前播放的URL

        try {
            stop(); // 停止当前播放
            initMediaPlayer(); // 重新初始化

            mediaPlayer.setDataSource(url);
            mediaPlayer.prepareAsync(); // 异步准备播放
        } catch (IOException e) {
            Log.e(TAG, "播放失败: " + e.getMessage());
            if (playCallback != null) {
                playCallback.onPlayError("播放失败: " + e.getMessage());
            }
        } catch (Exception e) {
            Log.e(TAG, "播放异常: " + e.getMessage());
            if (playCallback != null) {
                playCallback.onPlayError("播放异常: " + e.getMessage());
            }
        }
    }

    /**
     * 停止播放
     */
    public void stop() {
        if (mediaPlayer != null && isPlaying) {
            try {
                mediaPlayer.stop();
                mediaPlayer.reset();
                isPlaying = false;
                currentUrl = null; // 清除当前播放的URL
            } catch (Exception e) {
                Log.e(TAG, "停止播放失败: " + e.getMessage());
            }
        }
    }

    /**
     * 暂停播放
     */
    public void pause() {
        if (mediaPlayer != null && isPlaying) {
            mediaPlayer.pause();
            isPlaying = false;
        }
    }

    /**
     * 恢复播放
     */
    public void resume() {
        if (mediaPlayer != null && !isPlaying) {
            mediaPlayer.start();
            isPlaying = true;
        }
    }

    /**
     * 是否正在播放
     * @return true表示正在播放，false表示未播放
     */
    public boolean isPlaying() {
        return isPlaying;
    }

    /**
     * 释放资源
     */
    public void release() {
        stop();
        if (mediaPlayer != null) {
            mediaPlayer.release();
            mediaPlayer = null;
        }
        isPlaying = false;
    }

    /**
     * 获取当前播放的URL
     * @return 当前播放的URL，如果没有播放则返回null
     */
    public String getCurrentUrl() {
        return currentUrl;
    }
}
```

-   解析上述下发结果中的“audios” 获取音乐地址。并通过 mp3 播放器进行播放。在 demo 中，我们适配了一个简单的 UI 用于显示音乐播放状态。  
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6440007671/p1039326.png)
    
-   完整代码请参考 Android SDK demo。其他语言请通过类似的解析和播放实现相同功能。
    

### **4\. 连续播放：**

播放结束后，端上可以发指令要求继续播放，您可以监听NetworkMp3Player.OnPlayCallback()的onPlayComplete方法，在上一首音乐播放结束后，向服务端发起播放下一首请求：

```
multiModalDialog.requestToRespond("prompt","下一首", null);
```

播放中您可以不保持长连接，在下一次启动会话时，使用同一个dialog\_id 发起请求，实现跨链接的对话继承。
