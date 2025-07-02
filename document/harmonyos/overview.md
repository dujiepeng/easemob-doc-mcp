# SDK 集成概述

<Toc />

介绍 HarmonyOS 集成相关内容。

## 前提条件

开始前，请注册有效的环信即时通讯 IM 开发者账号并取得 App key，见 [环信即时通讯云管理后台](https://console.easemob.com/user/login)。

## 集成环境

详见 [快速开始中的开发环境要求](quickstart.html#准备开发环境)。

## 添加权限

1. 找到模块的文件 `module.json5`
2. SDK 最少需要添加的权限如下：

```xml
<!-- 访问网络权限 -->
ohos.permission.INTERNET
<!-- 获取网络信息权限 -->
ohos.permission.GET_NETWORK_INFO
```

## SDK 初始化

初始化是使用 SDK 的必要步骤，需在所有接口方法调用前完成。

如果进行多次初始化操作，只有第一次初始化以及相关的参数生效。

初始化示例代码：

```typescript
let options = new ChatOptions({
  appKey: "你的 AppKey"
});
......// 其他 ChatOptions 配置。
// 初始化时传入上下文以及 options
ChatClient.getInstance().init(context, options);
```

## 注册用户

目前用户注册方式有以下几种：
- 通过控制台注册。
- 通过 REST API 接口注册。
- 调用 SDK 接口注册。

### 控制台注册

通过控制台注册用户，详见[创建 IM 用户](/product/enable_and_configure_IM.html#创建-im-用户)。

### REST API 注册

请参考 [注册用户](/document/server-side/account_system.html#注册用户)。

### SDK 注册

若支持 SDK 注册，需登录[环信即时通讯云控制台](https://console.easemob.com/user/login)，选择 **即时通讯** > **服务概览**，将 **设置**下的 **用户注册模式** 设置为 **开放注册**。

```typescript
ChatClient.getInstance().createAccount(userId, pwd).then(()=> {
    // success logic
});
```

:::tip
该注册模式为在客户端注册，旨在方便测试，并不推荐在正式环境中使用。
:::

## 用户登录

目前登录服务器支持手动和自动登录。手动登录有两种方式：

- 用户 ID + 密码
- 用户 ID + token

手动登录时传入的用户 ID 必须为 string 类型，支持的字符集详见[用户注册的 RESTful 接口](/document/server-side/account_system.html#注册用户)。

调用登录接口后，收到 `onConnected` 回调表明 SDK 与环信服务器连接成功。

用户登录流程详见[用户注册与登录的产品说明文档](/product/product_user_registration_login.html)。

### 手动登录

**用户 ID + 密码** 登录是传统的登录方式。用户名和密码均由你的终端用户自行决定，密码需要符合密码规则要求。

```typescript
ChatClient.getInstance().login(userId, pwd).then(() => {
    // 登录成功回调
}).catch((e: ChatError) => {
    // 登录失败回调，包含错误信息
});
```

**用户 ID + token** 是更加安全的登录方式。token 可以通过调用 REST API 获取。详见 [环信用户 token 的获取](/document/server-side/easemob_user_token.html)。

:::tip
使用 token 登录时需要处理 token 过期的问题，比如在每次登录时更新 token 等机制。
:::

```typescript
ChatClient.getInstance().loginWithToken(userId, token).then(() => {
    // 登录成功回调
}).catch((e: ChatError) => {
    // 登录失败回调，包含错误信息
});
```

登录重试机制如下：

- 登录时，若服务器返回明确的失败原因，例如，token 不正确，SDK 不会重试登录。
- 若登录因超时失败，SDK 会重试登录。

### 自动登录

初始化时可以设置是否自动登录。如果设置为自动登录，则登录成功之后，后续启动初始化的时候会自动登录。

自动登录时，SDK 尝试连接服务器失败后，延时随机一段时间后自动重连。

## 退出登录

```typescript
ChatClient.getInstance().logout().then(()=> {
    // success logic       
})
```
## 连接状态相关

你可以通过注册连接监听确认连接状态。

```typescript
let connectionListener: ConnectionListener = {
  onConnected: (): void => {
    // 长连接建立
  },
  onDisconnected: (errorCode: number): void => {
    // 长连接断开
  },
  onLogout: (errorCode: number, info: LoginExtInfo): void => {
    // 触发退出，需要主动调用 ChatClient#logout 方法
  },
  onTokenExpired: (): void => {
    // 使用 token 登录时，token 过期触发。
  },
  onTokenWillExpire: (): void => {
    // 使用 token 登录时，token 将要过期时触发。
    // 注意：如果本次登录服务器没有离线消息，不会触发该回调。
  },
  onOfflineMessageSyncStart: () => {
    // 连接成功，开始从服务器拉取离线消息时触发。
  },
  onOfflineMessageSyncFinish: () => {
    // 离线用户上线后从服务器拉取离线消息结束时触发。
    // 注意：如果再拉取离线过程中因网络或其他原因导致连接断开，不会触发该回调。
  }
}
// 注册连接状态监听
ChatClient.getInstance().addConnectionListener(connectionListener);
// 移除连接状态监听
ChatClient.getInstance().removeConnectionListener(connectionListener);
```

### 断网自动重连

如果由于网络信号弱、切换网络等引起的连接终端，SDK 会自动尝试重连。重连成功或者失败的结果分别会收到通知 `onConnected` 和 `onDisconnected`。

### 被动退出登录

你可以通过监听回调 `ConnectionListener#onLogout` 后，调用 `ChatClient#logout` 进行退出并返回登录界面。

`ConnectionListener#onLogout(number)` 返回的 `errorCode` 有如下：

- `APP_ACTIVE_NUMBER_REACH_LIMITATION = 8`: 应用程序的日活跃用户数量（DAU）或月活跃用户数量（MAU）达到上限
- `USER_LOGIN_ANOTHER_DEVICE = 206`: 用户已经在其他设备登录
- `USER_REMOVED = 207`: 用户账户已经被移除
- `USER_BIND_ANOTHER_DEVICE = 213`: 用户已经绑定其他设备
- `USER_LOGIN_TOO_MANY_DEVICES = 214`: 用户登录设备超出数量限制
- `USER_KICKED_BY_CHANGE_PASSWORD = 216`: 由于密码变更被踢下线
- `USER_KICKED_BY_OTHER_DEVICE = 217`: 由于其他设备登录被踢下线
- `USER_DEVICE_CHANGED = 220`: 和上次设备不同导致下线
- `SERVER_SERVICE_RESTRICTED = 305`:  Chat 功能限制

以上参数具体可以参考 [ChatError](https://sdkdocs.easemob.com/apidoc/harmony/chat3.0/classes/ChatError.ChatError.html#errorCode) 对应说明。

## 输出信息到日志文件

环信即时通讯 IM 日志记录 SDK 相关的信息和事件。环信技术支持团队帮你排查问题时可能会请你发送 SDK 日志。

默认情况下，SDK 最多可生成和保存三个文件，`easemob.log` 和两个 `easemob_YYYY-MM-DD_HH-MM-SS.log` 文件。这些文件为 UTF-8 编码，每个不超过 2 MB。SDK 会将最新的日志写入 `easemob.log` 文件，写满时则会将其重命名为对应时间点的 `easemob_YYYY-MM-DD_HH-MM-SS.log` 文件，若日志文件超过三个，则会删除最早的文件。

例如，SDK 在 2024 年 1 月 1 日上午 8:00:00 记录日志时会生成 `easemob.log` 文件，若在 8:30:00 将 `easemob.log` 文件写满则会将其重命名为 `easemob_2024-01-01_08-30-00.log` 文件，随后在 9:30:30 和 10:30:30 分别生成了 `easemob_2024-01-01_09-30-30.log` 和 `easemob_2024-01-01_10-30-30.log` 文件，则此时 `easemob_2024-01-01_08-30-00.log` 文件会被移除。

SDK 默认输出调试信息（所有日志，包括调试信息、警告和错误），如果只需输出错误日志，需要关闭调试模式。

```typescript
ChatLog.setLogLevel(ChatLogLevel.ERROR_LEVEL);
```

### 获取本地日志

打开以下目录，获取本地日志。

```
hdc file recv /data/app/el2/100/base/{应用包名}/{App Key}/core_log
```

获取本地日志，需要将 `{应用包名}` 替换为应用的包名，例如 `com.hyphenate.chatuidemo`；`{App Key}` 需要替换为应用的环信 App Key。