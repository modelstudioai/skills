# 实现硬件设备控制能力

本文档用于指导开发者如何加载并使用多模态交互套件中的 技能-指令 模块，用以控制设备。

## 1\. 开发准备

⚠️注意：先参考[SDK安装](raw/application-user-guide/application-gallery/multimodal-products/multimodal-sdk.md)完成应用创建及SDK对接。

### 1.1. 多模态应用创建和配置

根据[应用配置](raw/application-user-guide/application-gallery/multimodal-products/multimodal-guidelines/multimodal-app-configuration.md)的文档完成应用的配置，指令模块配置见下：

-   **指令模块应用配置**

在应用配置界面，点击“**添加**”，勾选需要的系统指令，如音量设置。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1597593571/p990048.png)

添加完成后，将在应用上显示已配置的指令模块，如下图所示。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1597593571/p990047.png) **注意，红框部分不可更改，否则会导致模块无法解析** ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1597593571/p990049.png)

### 1.2. 端侧SDK开发和对接

在启用指令模块功能前，要求设备已完成SDK接入，不同类型的硬件设备需要根据不同的SDK接入方式进行开发和对接。

## 2\. 使用官方RTOS/Linux SDK实现设备控制能力

参考[RTOS C SDK（License模式）](raw/application-user-guide/application-gallery/multimodal-products/multimodal-sdk/mmi-rtos-sdk.md)。

### 2.1. 加载模块说明

启用指令模块对应功能模块，首先需要在编辑配置中添加对应的组件库；组件库在SDK包中`ali_sdk/build_<PLATFORM>/core/c_aliyun/mmi/command`目录下，组件库名称以`libcmd_`开头，如`libcmd_volume.a`。

加载组件库示例代码如下（ESP32平台）：

```
//加载预编译库
add_prebuilt_library(brightness_command ${LIBS_DIR}/../core/c_aliyun/mmi/command/libcmd_volume.a)

target_link_libraries(${COMPONENT_TARGET} INTERFACE
    volume_command
)
```

### 2.2. 引用头文件说明

在加载组件库后，源码中需要引用`ali_sdk/build_<PLATFORM>/aliyun_sdk/include/lib_c_mmi_cmd.h`。

### 2.3. 注册事件回调

注册事件回调相关接口在lib\_c\_mmi\_cmd.h定义如下：

```
// cmd_module 指令模块的枚举类型，用于标识不同的指令类别
enum {
    C_MMI_CMD_BRIGHTNESS,   // 亮度设置
    C_MMI_CMD_VOLUME,       // 音量设置
    C_MMI_CMD_DEVICE,       // 设备控制
    C_MMI_CMD_SCREEN,       // 屏幕控制
    C_MMI_CMD_MUTILMEDIA,   // 多媒体控制
    C_MMI_CMD_APPLICATION,  // 应用开关
    C_MMI_CMD_CAMERA,       // 拍照录像
    C_MMI_CMD_RECORDING,    // 录音
    C_MMI_CMD_MUSIC,        // 音乐
    C_MMI_CMD_TELEPHONE,    // 打电话
};

/**
 * @brief command事件回调函数类型
 *
 * @details 当command模块收到云端对应指令时触发的回调函数，用于处理指令事件
 *
 * @param event 事件类型，取值为加载某个指令组的指令事件枚举
 * @param param 事件参数，根据事件类型不同指向相对应的参数，没有参数时为NULL
 * @return int32_t 返回0表示处理成功，非0表示处理失败
 */
typedef int32_t(*command_user_callback)(uint32_t event, void *params);

/**
 * @brief 加载指定的指令模块组件
 *
 * @param cmd_module 指令模块类型
 * @param cb 回调函数，用户来实现，用于处理指令事件
 * @return int32_t 返回0表示处理成功，非0表示处理失败
 */
int32_t c_mmi_cmd_load(uint8_t cmd_module, command_user_callback cb);
```

如音量设置组件示例代码如下：

```
#include "lib_c_mmi_cmd.h"

static int32_t _cmd_vol_callback(uint32_t event, void *p)
{
    ... // 此函数事件枚举和参数内容见下节
}

int main(void)
{
    ...	// 其他业务逻辑

    c_mmi_cmd_load(C_MMI_CMD_VOLUME, _cmd_vol_callback);

    ... // 其他业务逻辑
}
```

### 2.4. 实现指令响应函数

指令响应函数相关事件及参数在`lib_c_mmi_cmd.h`均有说明：

如音量设置组件相关说明下：

```
#define C_MMI_CMD_VALUE_UNDEFINED       0x7FFFFFFF

enum {
    C_MMI_CMD_TYPE_UNKNOWN = 0,
    C_MMI_CMD_TYPE_SYSTEM,
    C_MMI_CMD_TYPE_MEDIA,
    C_MMI_CMD_TYPE_CALL
} c_mmi_cmd_type_t;

/*************************** 音量设置组件开始 ***************************/
//event 音量设置相关命令的枚举定义
enum {
    C_MMI_CMD_VOLUME_UNKNOWN = 0,
    C_MMI_CMD_VOLUME_INCREASE,
    C_MMI_CMD_VOLUME_DECREASE,
    C_MMI_CMD_VOLUME_SET,
    C_MMI_CMD_VOLUME_MUTE,
    C_MMI_CMD_VOLUME_UNMUTE
};

//params 音量设置相关命令的参数定义
typedef struct {
    uint32_t value;		// 当值为C_MMI_CMD_VALUE_UNDEFINED表示默认值（用户自定义）
    uint32_t type;		// 类型为c_mmi_cmd_type_t
} c_mmi_cmd_volume_param_t;
/*************************** 音量设置组件结束 ***************************/
```

示例代码如下：

```
#include "lib_c_mmi_cmd.h"

static int32_t _cmd_vol_callback(uint32_t event, void *p)
{
    volume_param_t *param = (volume_param_t *)p;

   // 根据event和指令参数进行处理，具体由用户实现
   // 例如，可以根据 event 类型执行不同的音量操作
    switch (event) {
        case C_MMI_CMD_VOLUME_SET:			// 设置音量
            UTIL_LOG_I("set volume to [%u] for [%u]", param->value, param->type);
            break;
        case C_MMI_CMD_VOLUME_INCREASE:		// 音量增大
            UTIL_LOG_I("increase volume by [%u] for [%u]", param->value, param->type);
            break;
        case C_MMI_CMD_VOLUME_DECREASE:		// 音量减小
            UTIL_LOG_I("decrease volume by [%u] for [%u]", param->value, param->type);
            break;
        case C_MMI_CMD_VOLUME_MUTE:			// 静音
            UTIL_LOG_I("mute");
            break;
        case C_MMI_CMD_VOLUME_UNMUTE:		// 解除静音
            UTIL_LOG_I("unmute");
            break;
        default:
            UTIL_LOG_W("invalid volume command");
            return UTIL_ERR_FAIL;
            break;
    }
    return UTIL_SUCCESS;
}
```

参数示例如下：

-   场景一：音量调大一点

```
uint32_t event = C_MMI_CMD_VOLUME_INCREASE;

c_mmi_cmd_volume_param_t param =
{
    .value = C_MMI_CMD_VALUE_UNDEFINED,
    .type = C_MMI_CMD_TYPE_SYSTEM
};
```

-   场景二：通话音量调低10

```
uint32_t event = C_MMI_CMD_VOLUME_DECREASE;

c_mmi_cmd_volume_param_t param =
{
    .value = 10,
    .type = C_MMI_CMD_TYPE_CALL
};
```

-   场景三：通话音量调低/调高/设置到10

```
uint32_t event = C_MMI_CMD_VOLUME_SET;

c_mmi_cmd_volume_param_t param =
{
    .value = 10,
    .type = C_MMI_CMD_TYPE_CALL
};
```

## 3.使用官方Android/iOS SDK 实现设备控制能力

在 Android 和 iOS SDK 中，服务端下发的结果会透传给客户端，客户端解析下发结果`payload.output.extra_info.commands`中的指令名称，执行对应的指令操作。系统指令和对应的说明请参考：[应用配置](raw/application-user-guide/application-gallery/multimodal-products/multimodal-guidelines/multimodal-app-configuration.md)。

服务端下发指令格式示例：

```
{
    "commands": [
        {
            "name": "send_sms",
            "params": [
                {
                    "name": "send_to",
                    "value": "妈妈",
                    "normValue": "妈妈"
                },
                {
                    "name": "sms_content",
                    "value": "明天下雨记得带伞",
                    "normValue": "明天下雨记得带伞"
                }
            ]
        }
    ]
}
```

在客户端实现设备控制：

-   Android

```
private void executeCommand(String command) {
        Log.d(TAG, "执行命令: " + command);

        try {
            String cmdName = new JSONArray(command).getJSONObject(0).getString("name");

            switch (cmdName) {
                case "visual_qa":
                    executeVQACommand();
                    break;
                case "quit_videochat":
                    stopVideoMode();
                    break;
                case "set_volume":
                    setVolume(command); //解析音量参数
                    break;
                case "quit":
                    quit();
                    break;
                    // .....
                default:
                    executeDefaultCommand();
                    break;
            }
        } catch (Exception e) {
            Log.e(TAG, "命令执行失败", e);
            isExecutingCommand = false;
        }
    }
```

-   iOS

```
//handle command
private func handleCommand(output: [String: Any]?) -> [[String: Any]]?{
    guard let output = output,
              let extraInfo = output["extra_info"] as? [String: Any],
              let commandsString = extraInfo["commands"] as? String,
          let commandsData = commandsString.data(using: .utf8) else {
        return nil
    }

    do {
            // 解析commands字符串为JSON数组
            if let commands = try JSONSerialization.jsonObject(with: commandsData) as? [[String: Any]] {

                for command in commands {
                    let name = command["name"] as? String
                        if name == "visual_qa" {
                            self.executeVQACommand()
                        }else if name == "quit_videochat"{
                            self.quitVideoMode()
                        }else if name == "set_volume"{
                            self.setVolume(command)
                        }else if name == "quit"{
                            self.quit()
                        }
                    //......
                    }
                return commands
            }
            return nil
        } catch {
            print("解析commands时出错: \(error)")
            return nil
        }
    }
```
