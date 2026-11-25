# 设备端C SDK实现音量控制

本文介绍如何基于设备端C SDK实现音量控制能力。

<a id="1-开发准备"></a>

<a id="7e4f5c9822yar"></a>

## 1\. 开发准备

<a id="1-1-前置说明"></a>

<a id="45375c150fq4y"></a>

### 1.1. 前置说明

-   本文依赖前置文档 “[基于设备端C SDK实现聊天能力](chat-capability-based-on-rtos-sdk-019f5c7ac38b3d0b.md)” ，请在阅读本文前先完成相关内容的学习与环境准备。
-   默认开发者已完成SDK接入，并可正常运行语音交互流程。

<a id="1-2-配置音量控制"></a>

<a id="086f9b03fduv7"></a>

### 1.2. 配置音量控制

-   在**百炼控制台**创建应用
    
-   点击`技能/指令`开启`音量设置`
    
    在弹出的指令弹窗中，选择**系统指令**页签。
    

<a id="2-端侧功能开发"></a>

<a id="fceb26e9c95km"></a>

## 2\. 端侧功能开发

<a id="2-1-sdk目录及文件结构说明"></a>

<a id="da35882bfb69c"></a>

### 2.1. SDK目录及文件结构说明

获取SDK包可以参考文档：[设备端C SDK](mmi-rtos-sdk-dbfd414713bc31c9.md)

<a id="code-block"></a>

```text
qwen_sdk/
├── include
│   ├── c_mmi_cmd
│   │   ├──c_mmi_cmd_volume.h
│   │   ├──c_mmi_cmd.h
│   │   └── ...
├── libs
│   ├── libc_mmi_cmd_volume.a
│   ├── libc_mmi_cmd.a
│   └── ...
└── ...
```

> **重要**
>
> 启用音量控制功能的时候需要加载`libc_mmi_cmd.a`和`libc_mmi_cmd_volume.a`静态库文件。

<a id="2-2-示例代码"></a>

<a id="367adb38e3514"></a>

### 2.2. 示例代码

SDK已将音量控制功能抽象成下列5种事件

<a id="code-block-2"></a>

```text
//event 音量设置相关命令的枚举定义
enum {
    C_MMI_CMD_VOLUME_UNKNOWN = 0,
    C_MMI_CMD_VOLUME_INCREASE,
    C_MMI_CMD_VOLUME_DECREASE,
    C_MMI_CMD_VOLUME_SET,
    C_MMI_CMD_VOLUME_MUTE,
    C_MMI_CMD_VOLUME_UNMUTE
};
```

触发事件时传入参数格式如下

<a id="code-block-3"></a>

```text
//params 音量设置相关命令的参数定义
typedef struct {
    uint32_t value;
    uint32_t type;
} c_mm_volume_param_t;
```

参数说明

> **说明**
>
> 在多模态链路中，c\_mm\_volume\_param\_t.type表示设置的音量类型，正常情况下可忽略该参数，具体枚举值如下：
>
> <a id="code-block-4"></a>
>
> ```text
> enum {
>     C_MM_CMD_TYPE_UNKNOWN = 0,
>     C_MM_CMD_TYPE_SYSTEM,	// 系统
>     C_MM_CMD_TYPE_MEDIA,	// 媒体
>     C_MM_CMD_TYPE_CALL		// 通话
> };
> ```

> **说明**
>
> 参数c\_mm\_volume\_param\_t.value取值范围0-100，映射至设备端的实际音量调整关系由应用层根据实际情况自行决定。
>
> 当参数c\_mm\_volume\_param\_t.value == C\_MMI\_CMD\_VALUE\_UNDEFINED时，表示音量调整默认等级，具体默认等级调整量由应用层根据实际情况自行决定。

示例代码

<a id="code-block-5"></a>

```text
#include "c_mmi_cmd.h"
#include "c_mmi_cmd_volume.h"
static int32_t _cmd_vol_callback(uint32_t event, char *req_id, void *p)
{
    c_mm_volume_param_t *param = (c_mm_volume_param_t *)p;
    (void)req_id;
    switch (event) {
        case C_MMI_CMD_VOLUME_SET:
            UTIL_LOG_I("set volume to [%u] for [%u]", param->value, param->type);
            break;
        case C_MMI_CMD_VOLUME_INCREASE:
            UTIL_LOG_I("increase volume by [%u] for [%u]", param->value, param->type);
            break;
        case C_MMI_CMD_VOLUME_DECREASE:
            UTIL_LOG_I("decrease volume by [%u] for [%u]", param->value, param->type);
            break;
        case C_MMI_CMD_VOLUME_MUTE:
            UTIL_LOG_I("mute");
            break;
        case C_MMI_CMD_VOLUME_UNMUTE:
            UTIL_LOG_I("unmute");
            break;
        default:
            UTIL_LOG_W("invalid volume command");
            return UTIL_ERR_FAIL;
            break;
    }
    return UTIL_SUCCESS;
}
int32_t main(void)
{
    int32_t err = c_mmi_cmd_volume_register(_cmd_vol_callback);
    if (err) {
        UTIL_LOG_E("volume no load");
    }
    return 0;
}
```
