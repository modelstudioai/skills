# RTOS SDK（License模式）视觉模块接入

本文介绍如何基于RTOS SDK（License模式）实现视觉相关能力，如视频对话、拍照问答。

## 1\. 开发准备

### 1.1. 前置说明

-   本文依赖前置文档 “[基于RTOS SDK (License模式) 实现聊天能力](raw/application-user-guide/application-gallery/multimodal-products/multimodal-best-practices/chat-capability-based-on-rtos-sdk.md)” ，请在阅读本文前先完成相关内容的学习与环境准备。
-   默认开发者已完成SDK接入，并可正常运行语音交互流程。
-   此最佳实践将会使用[基于RTOS SDK (License模式) 实现聊天能力](raw/application-user-guide/application-gallery/multimodal-products/multimodal-best-practices/chat-capability-based-on-rtos-sdk.md)中的部分伪代码和交互流程。

### 1.2. 配置启用视觉模块

-   在**百炼控制台**创建多模态应用，创建完成后如下所述
    
    创建完成后，应用卡片中显示**应用 ID**（以 `mm_` 开头）和**License 用量**状态。若 License 显示"未购买"，可单击**购买**获取许可。单击**配置应用**进入应用配置页面。
    
-   点击`配置应用`开启`视频通话`或/和`拍照问答`或/和`拍照翻译`或/和`极速视频通话`的Agent
    
    操作位置为**技能**页签下**Agent**区域的**百炼应用**列表。
    

## 2\. 端侧视觉模块功能开发

视觉模块功能包括拍照问答、视频通话、拍照翻译、极速视频通话。

未进入视频通话时或未进入极速视频通话时，所有类似“我前面有什么”的问答都会触发VQA

未进入视频通话时或未进入极速视频通话时，所有类似“翻译下面前的路牌”的带翻译意图的问答都会触发拍照翻译

一旦进入视频通话或进入极速视频通话，所有图片问答逻辑由视频通话或极速视频通话处理。

### 2.1. SDK目录及文件结构说明

获取的SDK包解压后，与本文相关的文件及目录结构如下

获取SDK包可以参考文档：[RTOS C SDK（License模式）](raw/application-user-guide/application-gallery/multimodal-products/multimodal-sdk/mmi-rtos-sdk.md)

```
qwen_sdk/
├── include
│   ├── c_utils
│   │   └── ...
│   ├── c_visual
│   │   └── c_visual.h
│   └── ...
├── libs
│   ├── libc_visual.a
│   └── ...
└── ...
```

启用视觉模块功能的时候需要加载`c_visual.h`头文件和`libc_visual.a`静态库文件。

### 2.2. c\_visual初始化

示例代码

```
int32_t app_visual_init(void)
{
    c_visual_config_t config = {
        // mode设置采用多重设置，即可以设置为 C_VISUAL_MODE_VQA ｜ C_VISUAL_MODE_LIVE_AI,
        // 设置为如上形式时可以同时使用VQA和LIVE AI，
        // C_VISUAL_MODE_NONE 表示不启用任何视觉功能，不能作为 visual_mode 的取值（配置会被拒绝）。
        .visual_mode = C_VISUAL_MODE_VQA | C_VISUAL_MODE_LIVE_AI | C_VISUAL_MODE_OMNI,
        // 图片格式设置，该参数目前不影响实际功能，目前支持的图片格式为头文件枚举项
        .image_format = C_VISUAL_PIC_FORMAT_JPG,
        // 必选项
        .data_type = C_VISUAL_DATA_BASE64,
        // 该参数目前不影响实际功能
        // 实际传入图像的宽度和高度均应大于10像素，宽高比不应超过200:1或1:200。
        .frame_size = C_VISUAL_FRAMESIZE_320x240,
        // 图片大小设置，现阶段百炼云端单张照片只支持180KB
        .image_size = 180 * 1024,
        // 建议fps设置为2
        .fps = 2,
        .event_callback = _visual_callback
    };
    c_visual_config(&config);
    return UTIL_SUCCESS;
}
```

初始化参考日志如下：

```
[UT][D][c_visual_config]mode 14
[UT][D][c_visual_config]VISUAL set params success
[UT][D][c_mmi_set_upstream_type]upstream_type[AudioAndVideo]
[UT][I][c_visual_config]upgrade to video stream
[UT][D][c_mm_cmd_register]create new domain [visual_qa]
[UT][D][c_mm_cmd_register]domain [visual_qa] add [visual_qa]
[UT][D][c_mm_cmd_register]create new domain [video_chat]
[UT][D][c_mm_cmd_register]domain [video_chat] add [open_videochat]
[UT][D][c_mm_cmd_register]domain [video_chat] add [switch_video_call_success]
[UT][D][c_mm_cmd_register]domain [video_chat] add [quit_videochat]
[UT][D][c_mm_cmd_register]domain [video_chat] add [exit_video_call_success]
[UT][D][c_mm_cmd_register]create new domain [omni]
[UT][D][c_mm_cmd_register]domain [omni] add [send_video_stream]
[UT][D][c_mm_cmd_register]domain [omni] add [stop_video_stream]
[UT][I][c_visual_config]done
```

`c_visual_config` 仅保存配置并注册指令回调，不分配图像缓冲区；PSRAM 图像缓冲区由 SDK 在收到云端视觉启动指令时自动分配，也可在会话前调用 `c_visual_malloc` 显式预分配。分配完成前，`c_visual_task_handle`、`c_visual_image_get_buffer` 等接口返回 `UTIL_ERR_NO_INIT` 或 `NULL`。此外，`c_visual_config` 必须在 `c_mmi_init` 之前调用，否则返回错误。

### 2.3. c\_visual事件说明

```
enum {
    C_VISUAL_EVENT_MALLOC_PREPARE,  // 分配 PSRAM 资源前触发，可在回调中腾挪资源；返回非 0 则中止本次分配（回调在模块锁内执行，禁止调用本模块锁相关接口）
    C_VISUAL_EVENT_VQA_START,       // 开启拍照问答时触发，可在该事件回调中激活摄像头并开始拍照
    C_VISUAL_EVENT_VQA_END,         // 结束拍照问答时触发，建议在该事件回调中关闭摄像头
    C_VISUAL_EVENT_LIVEAI_START,    // 开启视频通话时触发（含极速），建议在该事件回调中开启摄像头
    C_VISUAL_EVENT_LIVEAI_ACTION,   // 视频通话抽帧时触发，可在该事件回调中进行图片采集
    C_VISUAL_EVENT_LIVEAI_STOP,     // 关闭视频通话时触发，建议在该事件回调中关闭摄像头
    C_VISUAL_EVENT_PROACTOR_START,  // 开始主动交互时触发，建议在该事件回调中开启摄像头
    C_VISUAL_EVENT_PROACTOR_STOP,   // 退出主动交互时触发，建议在该事件回调中关闭摄像头
};
```

#### 2.3.1. 拍照问答 & 拍照翻译

拍照问答 & 拍照翻译事件响应示例如下：

```
static int32_t _visual_callback(uint32_t event, char *req_id, void *params)
{
    (void)req_id;
    (void)params;
    switch (event) {
    case C_VISUAL_EVENT_VQA_START:
        UTIL_LOG_I("vqa start");
        c_camera_open();
        // 手动触发拍照，根据实际实现方案确认是否要调用
        c_camera_capture();
        break;
    case C_VISUAL_EVENT_VQA_END:
        UTIL_LOG_I("vqa end");
        c_camera_close();
        break;
    ...
    }
    return UTIL_SUCCESS;
}
```

#### 2.3.2. 视频通话 & 极速视频通话

视频通话 & 极速视频通话事件响应示例如下：

```
static int32_t _visual_callback(uint32_t event, char *req_id, void *params)
{
    (void)req_id;
    (void)params;
    switch (event) {
    case C_VISUAL_EVENT_LIVEAI_START:
        UTIL_LOG_I("liveai start");
        c_camera_open();
        break;
    case C_VISUAL_EVENT_LIVEAI_ACTION:
        UTIL_LOG_I("liveai capture");
        // 手动触发拍照，根据实际实现方案确认是否要调用
        c_camera_capture();
        break;
    case C_VISUAL_EVENT_LIVEAI_STOP:
        UTIL_LOG_I("liveai stop");
        c_camera_close();
        break;
    ...
    }
    return UTIL_SUCCESS;
}
```

### 2.4. 摄像头实现

#### 2.4.1. 图像采集逻辑

通过下述方式将摄像头采集的图像给到c\_visual模块，c\_visual会根据视觉模型的要求完成数据封装和上行。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7656439771/CAEQaxiBgMD3sbPi3BkiIDRjY2UxMWViNjBkZjQxMjU5ZDVmYmExNGZmYWQxZjcy6149252_20260107211205.843.svg)

示例代码1，通过摄像头回调将采集数据送入c\_visual

```
// 将摄像头采集的image数据传递给c_visual
int32_t hal_camera_capture_callback(uint8_t *image, uint32_t image_size)
{
  uint8_t *buffer;
  uint32_t buffer_size;
  buffer = c_visual_image_get_buffer(&buffer_size);
  if (buffer == NULL) {
    UTIL_LOG_W("get buffer fail");
    return -1;
  }
  if (buffer_size < image_size) {
    UTIL_LOG_W("image_siz > buffer_size");
    return -1;
  }
  memcpy(buffer, image, image_size);
  c_visual_image_action(image_size);
  return 0;
}
```

示例代码2，通过创建线程，周期性调用摄像头采集数据送入c\_visual

```
void hal_camera_task_handle(void *param)
{
  (void)param;
  int32_t err;
  uint8_t *buffer;
  uint32_t buffer_size;
  while (1) {
    buffer = c_visual_image_get_buffer(&buffer_size);
    if (buffer == NULL) {
      UTIL_LOG_D("get buffer fail");
      util_msleep(20);
      continue;
    }
    err = hal_camera_capture(buffer, &buffer_size);
    if (err) {
      UTIL_LOG_D("capture fail");
      util_msleep(20);
      continue;
    }
    UTIL_LOG_I("capture success");
    c_visual_image_action(buffer_size);
    util_msleep(100);  // 休眠一段时间后再次调用camera采集图像
  }
}
```

#### 2.4.2. 实现示例

下述示例代码通过创建线程周期性采集摄像头图像方案实现，开发者可根据硬件特性选择合适的实现方式。

```
#include "hal_camera.h"
#include "c_visual.h"
#define CAMERA_DROP_NUM         (4)
typedef struct {
    uint8_t camera_initd;
    uint8_t camera_work;
    util_task_t* task;
    uint8_t task_running;
    uint8_t drop_img_num;
} _camera_info_t;
static _camera_info_t _camera_info = { 0 };
static void _camera_task_entry(void* params) {
    (void)params;
    int32_t err;
    uint8_t *buffer;
    uint32_t buffer_size;
    while (_camera_info.task_running) {
        if (_camera_info.camera_work == 0) {
            util_msleep(20);
            continue;
        }
        buffer = c_visual_image_get_buffer(&buffer_size);
        if (buffer == NULL) {
            UTIL_LOG_D("get buffer fail");
            util_msleep(20);
            continue;
        }
        err = hal_camera_capture(buffer, &buffer_size);
        if (err) {
            UTIL_LOG_D("capture fail");
            util_msleep(20);
            continue;
        }
        UTIL_LOG_I("capture success");
        if (_camera_info.drop_img_num) {
            UTIL_LOG_I("drop [%d]", _camera_info.drop_img_num);
            _camera_info.drop_img_num--;
            continue;
        }
        c_visual_image_action(buffer_size);
        c_visual_task_handle();
    }
    util_task_t* del_task = _camera_info.task;
    memset(&_camera_info, 0, sizeof(_camera_info));
    hal_camera_close();
    UTIL_LOG_I("task will exit");
    util_task_delete(del_task);
}
int32_t c_camera_init(void)
{
    int32_t err;
    if (_camera_info.camera_initd) {
        return UTIL_SUCCESS;
    }
    memset(&_camera_info, 0, sizeof(_camera_info));
    _camera_info.drop_img_num = CAMERA_DROP_NUM;
    hal_camera_open();
    _camera_info.task_running = 1;
    _camera_info.task = util_task_create("CAMERA", CAMERA_TASK_PRIORITY, CAMERA_STACK_SIZE, _camera_task_entry, NULL);
    _camera_info.camera_initd = 1;
    UTIL_LOG_I("done");
    return UTIL_SUCCESS;
}
int32_t c_camera_open(void)
{
    if (_camera_info.camera_initd == 0) {
        c_camera_init();
    }
    if (_camera_info.camera_work) {
        UTIL_LOG_D("already");
        return UTIL_SUCCESS;
    }
    c_visual_data_reset();
    hal_camera_open();
    _camera_info.drop_img_num = CAMERA_DROP_NUM;
    _camera_info.camera_work = 1;
    UTIL_LOG_I("done");
    return UTIL_SUCCESS;
}
int32_t c_camera_close(void)
{
    if (_camera_info.camera_initd == 0) {
        UTIL_LOG_E("no inited");
        return UTIL_ERR_NO_INIT;
    }
    if (_camera_info.camera_work == 0) {
        UTIL_LOG_D("already");
        return UTIL_SUCCESS;
    }
    _camera_info.camera_work = 0;
    hal_camera_close();
    UTIL_LOG_I("done");
    return UTIL_SUCCESS;
}
int32_t c_camera_deinit(void)
{
    if (_camera_info.camera_initd == 0) {
        UTIL_LOG_D("already");
        return UTIL_SUCCESS;
    }
    _camera_info.task_running = 0;
    UTIL_LOG_I("prepare");
    return UTIL_SUCCESS;
}
```
