# 小程序 SDK 更新日志

<Toc />

## 版本 V4.15.0 Dev 2025-5-21（开发版）

### 新增特性

- 支持获取 [群组](group_manage.html#获取群成员列表)/[聊天室成员列表](room_members.html#获取聊天室成员列表) 时，列明成员的用户 ID 和角色。
- [撤回消息](message_recall.html) 时，支持群组中群主/管理员撤回其他用户发送的消息。
- 群组成员进出事件支持一次通知多个成员进出群组。调整前，SDK 会为每个加入/退出的成员单独回调一条事件。
  - 新增群成员进出事件 [membersPresence](group_manage.html#监听群组事件) 和 [membersAbsence](group_manage.html#监听群组事件)。原事件 `memberPresence` 和 `membersAbsence` 仍有效。 
   
### 优化

- 修改 Token 即将过期事件 `onTokenWillExpire` 的触发时机。SDK 会在 Token 有效期达到 80% 时（之前版本为 50% ）回调即将过期通知。
- 获取群组成员列表的原方法 `listGroupMembers` 废弃。使用 [getGroupMembers](group_manage.html#获取群成员列表) 替换。
- 获取群组成员列表的原方法 `listChatRoomMembers` 废弃。使用 [getChatRoomMembers](room_members.html#获取聊天室成员列表) 替换。

## 版本 V4.14.0 Dev 2025-4-21（开发版）

### 新增特性

- 支持 [发送](message_send.html#发送-gif-图片消息) 和 [接收 GIF 图片消息](message_receive.html#接收-gif-图片消息)。
- 支持 [群组头像功能](group_attributes.html#管理群组头像)。
- 支持 [消息附件鉴权功能](message_receive.html)。该功能需要联系商务开通，开通后必须调用 SDK 的 API 才能下载消息附件。
- 支持 [自定义设备平台](multi_device.html#设置登录设备的平台)。
- Uni-app 离线推送安卓平台支持 [Google FCM](push/uniapp_push_fcm.html)。

### 优化

- 原创建群组方法 `createGroup` 方法废弃，使用 [createGroupVNext](group_manage.html#创建群组) 方法代替。

## 版本 V4.13.0 Dev 2025-3-12（开发版）

### 新增特性

- [IM SDK] 发送后修改消息接口 [modifyMessage](message_modify.html) 支持修改各类消息：
  - 文本消息：支持修改 `msg` 和 `ext` 字段。
  - 自定义消息：支持修改 `customEvent` 、`customExts` 和 `ext` 字段。
  - 图片/语音/视频/文件/位置/合并消息：仅支持修改 `ext` 字段。
  - 命令消息：不支持修改。

- [IM SDK] 小程序 SDK 支持运行到微信小游戏平台。

### 优化

[IM SDK] SDK 内部捕获重试 DNS 失败的错误。

## 版本 V4.12.0 2025-1-10

### 新增特性

- [IM SDK] 消息修改事件 `onModifiedMessage` 中增加消息 `ext` 字段。添加该字段后，修改发送成功的消息后，消息接收方会收到发送方发送修改后的消息时添加的扩展信息。
-  加入聊天室 `joinChatRoom` 成功的回调新增 `info` 字段，包含如下信息，即用户加入聊天室后会收到如下信息：
   - 聊天室创建时间：`createTimestamp`。
   - 是否开启全员禁言：`isAllMembersMuted`。
   - 是否在白名单中：`isInAllowlist`。
   - 当前聊天室成员数：`memberCount`。
   - 成员禁言到期时间：`muteExpireTimestamp`。
  
### 优化

- [IM SDK] 小程序 SDK 支持 HTTPDNS, 默认开启, 用户无需手动传入 `url` 和 `apiUrl`，SDK 会自动获取。

### 修复

- [IM SDK] 格式化小程序 SDK API 请求失败错误码，与 Web 端统一。**请注意使用密码登录 IM 返回的错误码和旧版本不兼容**。
- [IM SDK] 修复 Uniapp SDK 4.36 版本运行到鸿蒙平台，出现的重连问题。
- [IM SDK] 修复偶现的无法拉取消息的问题。

## 版本 V4.11.0 Dev 2024-12-3（开发版）

### 新增特性

- [IM SDK] 新增[拉取服务器漫游消息](message_retrieve.html#从服务器获取指定会话的消息)时会读取服务端的消息已读和送达状态。该功能只适用于单聊消息，默认关闭，如果需要，请联系环信商务开通。
- [IM SDK] 聊天室禁言回调 `muteMember` 新增 `muteTimestamp` 参数，表示禁言过期时间。
- [IM SDK] 群组/聊天室禁言事件 `muteMember` 新增 `userId` 字段，表示被禁言的成员。
- [IM SDK] uniapp SDK 支持鸿蒙系统。

### 优化

[IM SDK] SDK 的 message 对象中新增 `parseDownloadResponse`、`download` 方法。目前，SDK 的 utils 对象和 message 对象中均包含 `parseDownloadResponse`、`download` 方法。

### 修复

[IM SDK] 修复消息置顶事件 `onMessagePinEvent` 中的 `conversationId` 参数值错误的问题。

## 版本 V4.10.0 2024-10-11（开发版）

### 新增特性

- 聊天室公告修改事件中增加公告内容：`updateAnnouncement` 事件中增加 `announcement` 字段，表示更新的公告。
- 新增两个[错误码](error.html)：
  - `WEBIM_USER_ALREADY_LOGIN` 208：用户已登录。单设备登录时，若调用登录方法 `open` 时用户已经登录，会触发该错误。
  - `MESSAGE_SEND_TIMEOUT` 512：发送消息超时。例如，发消息时连接断开，会提示该错误。
- 新增 `onShow` 方法，小程序或 uniapp 在 `onShow` 生命周期中执行该方法，可优化重连速度。
   
### 优化

调整了登录方法的 `open().then` 与连接成功事件 `onConnected` 的触发时机。优化后，调用登录方法 `open` 后，先触发连接成功与否的事件 `onConnected` 或 `onDisconnected`，然后再触发登录 `open().then` 或者 `open().catch`，以确保连接完全建立后再进行后续处理。之前版本为调用登录方法，先触发登录回调，然后触发连接事件，导致需要等待连接成功事件 `onConnected` 触发后才能发送消息。同时，优化后，鉴权失败等登录错误会在 `open.catch` 中抛出。

## 版本 V4.9.2 2024-09-20（开发版）

### 新增特性

- [IM SDK] `removeHistoryMessages` 方法[支持单向删除服务端的聊天室消息](message_delete.html#单向删除服务端的历史消息)。

## 版本 V4.9.1 Dev 2024-09-06（开发版）

### 新增特性

- [IM SDK] uni-app SDK 支持 [uni-app 推送插件](/document/applet/push/uniapp_push.html)。

### 修复
  
- [IM SDK] 修复一些类型问题。

## 版本 V4.8.1 Dev 2024-07-17（开发版）

### 新增特性

- [IM SDK] 新增[日志上报](initialization.html#日志上报)功能, 即将日志会上传到环信的服务器。该功能默认关闭，如有需要, 可联系商务开通。

## 版本 V4.8.0 Dev 2024-07-01（开发版）

### 新增特性

- [IM SDK] [`onDisconnected` 事件](initialization.html#连接状态相关)新增断开原因回调参数, 告知用户触发 `onDisconnected` 的原因。
- [IM SDK] 新增[设备登录时允许携带自定义消息，并将其传递给被踢的设备](multi_device.html#设置登录设备的扩展信息)： 
  - `setLoginInfoCustomExt`：设置登录设备的扩展信息。
  - `onDisconnected`：多设备登录场景下，若当前设备被新登录设备踢下线，被踢设备收到的事件中会携带新设备的扩展信息。
- [IM SDK] 支持[加入聊天室时携带扩展信息、是否退出之前加入的全部聊天室](room_manage.html#加入聊天室)：
  - `joinChatRoom` 方法新增 `ext` 和 `leaveOtherRooms` 参数，支持设置加入聊天室时携带的扩展信息，并指定是否退出所有其他聊天室。
  - `ChatroomEvent` 新增 `ext` 扩展字段，当用户加入聊天室携带了扩展信息时，聊天室内其他人可以在用户加入聊天室的回调中，获取到扩展信息。
- [IM SDK] 新增 `ConnectionParameters#isFixedDeviceId` 初始化参数，默认为 `true`，[使用固定的设备 ID](multi_device.html)。之前，每个 SDK 实例连接时，SDK 默认均使用不同的随机字符串作为设备标识。
- [IM SDK] `destroyChatRoom` 方法[支持聊天室所有者解散聊天室](room_manage.html#解散聊天室)。

## 版本 V4.7.0 Dev 2024-04-30（开发版）

### 新增特性

- [IM SDK] 新增 `getJoinedChatRooms` 方法，用于[获取当前用户加入的聊天室列表](room_manage.html#获取当前用户加入的聊天室列表)。
- [IM SDK] [撤回消息](message_recall.html#实现方法)接口 `recallMessage` 中新增 `ext` 参数，支持传入自定义字符串，设置扩展信息。
- [IM SDK] SDK logger 中新增 `setConsoleLogVisibility` 方法，用于[设置日志是否输出到控制台](initialization.html#输出信息到日志文件)。

### 修复

- [IM SDK] 修复消息 `allowGroupAck` 状态错误问题。

## 版本 V4.6.0 Dev 2024-04-02（开发版）

### 新增特性

- [IM SDK] 新增[置顶消息功能](message_pin.html)。
  - `pinMessage`: 置顶消息。
  - `unpinMessage`: 取消置顶消息。
  - `getServerPinnedMessages`：从服务器获取指定会话的置顶消息。
  - `onMessagePinEvent`: 当用户在群组或聊天室会话进行置顶操作时，群组或聊天室中的其他成员会收到该回调。
- [IM SDK] 消息修改回调 `onModifiedMessage` 中支持返回[通过 RESTful API 修改的自定义消息](/document/server-side/message_modify.html)。
- [IM SDK] 支持[获取聊天室漫游消息](message_retrieve.html#从服务器获取指定会话的消息)。

### 优化

- [IM SDK] 优化 Token 登录时的错误提示信息，使错误提示更精细。

### 修复

- [IM SDK] 修复消息 `onlineState` 状态错误问题。

## 版本 V4.5.1 Dev 2024-02-22（开发版）

### 优化

- [IM SDK] 统一消息附件的 URL 格式。

### 修复

- [IM SDK] 修复 uni-app SDK 运行到 iOS 平台发送群组定向消息报错的问题。

## 版本 V4.5.0 Dev 2024-01-30（开发版）

### 新增特性

- [IM SDK] [聊天室和群组成员进出事件增加成员人数 `memberCount` 字段](room_manage.html#实时更新聊天室成员人数)。
- [IM SDK] 新增 [deleteAllMessagesAndConversations](message_delete.html#单向清空服务端的聊天记录) 方法, 用于清空当前用户的聊天记录，包括消息和会话。
- [IM SDK] 新增 [getSelfIdsOnOtherPlatform](multi_device.html#获取当前用户的其他登录设备的登录-id-列表) 方法, 可以获取当前用户其他登录设备的登录 ID 列表，实现对指定设备发送消息。
- [IM SDK] 新增 [useReplacedMessageContents](message_send.html#发送消息前的内容审核) 开关。开启后，发送消息时如果被内容审核进行了内容替换，发送方可以获取替换后的内容。

### 优化

- [IM SDK] 抖音小程序重连缓慢。
- [IM SDK] 格式化会话列表中最近一条自定义消息的 `customExts` 字段。
- [IM SDK] 重复拉消息问题。

### 修复

- [IM SDK] 修复 `onMessage` 回调消息顺序异常问题。

## 版本 V4.4.0 Dev 2023-12-22（开发版）

### 新增特性

- [IM SDK] 新增[会话标记功能](conversation_mark.html)。
  - `addConversationMark`：[标记会话](conversation_mark.html#标记会话)。
  - `removeConversationMark`：[取消标记会话](conversation_mark.html#取消标记会话)。
  - `getServerConversationsByFilter`：[根据会话标记从服务器分页查询会话列表](conversation_mark.html#根据会话标记从服务器分页查询会话列表)。
  - `onMultiDeviceEvent#markConversation/unMarkConversation`：[多设备场景下的会话标记事件](multi_device.html#实现方法)。当前用户在一台登录设备上更新了会话标记，包括添加和移除会话标记，其他登录设备会收到该事件。
- [IM SDK] 增加 `onMessage` 回调。在收到文本、图片、视频、语音、地理位置和文件等消息时，批量将消息回调给应用。

### 修复

- [IM SDK] SDK 类型修正。

## 版本 V4.3.0 Dev 2023-11-17

### 新增特性

- [IM SDK] 新增[好友备注功能](user_relationship.html#设置好友备注)。
- [IM SDK] 消息结构新增 `broadcast` 字段, 用于判断该消息是否为聊天室全局广播消息。可通过[调用 REST API 发送聊天室全局广播消息](/document/server-side/message_broadcast.html#发送聊天室全局广播消息)。

### 优化

- [IM SDK] Token 登录增加即将过期及已过期的回调，即 Token 已过期或有效期过半时也触发 `onTokenExpired` 和 `onTokenWillExpire` 回调。

### 修复

- [IM SDK] 修复会话列表最后一条消息中获取不到 `reaction` 的问题。

## 版本 V4.2.1 Dev 2023-09-27

### 新增特性

- [IM SDK] 用户申请加群被拒绝的回调 `joinPublicGroupDeclined` 中增加申请人的用户 ID。

## 版本 V4.2.0 Dev 2023-07-27

### 新增特性

- [IM SDK] 新增 [发送](message_send.html#发送合并消息) 和 [接收合并转发消息](message_receive.html#接收合并消息) 功能。
- [IM SDK] 新增[消息修改功能](message_modify.html)。
- [IM SDK] 新增[在群组或聊天室会话中发送定向消息](message_target.html)。通过在构建消息的方法 `create` 中添加 `receiverList` 参数实现该特性。

### 修复

修复发送不必要的消息送达回执的问题。

## 版本 V4.1.6 Dev 2023-04-17

### 新增特性

- [IM SDK] `getHistoryMessages` 方法的 `searchOptions` 中新增 `from`、`msgTypes`、`startTime` 和 `endTime` 参数，允许用户按消息发送方、消息类型或时间段从服务端拉取历史消息。
- [IM SDK] 新增错误码 511，即 MESSAGE_SIZE_LIMIT，若[消息体大小超过限制](message_overview.html#消息类型)时提示用户。

## 版本 V4.1.4 Dev 2023-03-16

### 新增特性

- [IM SDK] 新增 [群成员自定义属性功能](group_members.html#管理群成员自定义属性)并增加[自定义属性更新事件](group_manage.html#监听群组事件)实现群成员设置和获取在群组中的昵称和头像等属性。
- [IM SDK] 在消息创建参数中新增 `deliverOnlineOnly` 字段实现发消息只投递给在线用户。若开启了该功能，用户离线时消息不投递。
- [IM Demo] 新增群成员昵称修改与展示功能。 

### 优化

[IM SDK] 优化聊天室进入和退出实现，提升性能。

### 修复

- [IM SDK] 修复 TypeScript 代码的一些类型错误。
- [IM SDK] 修复 `getHistoryMessages` 方法无法捕获错误的问题。

## 版本 V4.1.3 Dev 2023-02-21

#### 新增特性

- [IM SDK] 在 `getConversationlist` 方法中新增分页参数 `pageNum` 和 `pageSize`，支持[分页方法获取会话列表](conversation_list.html#从服务器分页获取会话列表)。
- [IM SDK] 新增[群组创建事件 `create`](group_manage.html#监听群组事件)。群组创建后，群主的其他设备会收到该事件。

#### 优化

- [IM SDK] 缩减 MiniCore 的大小。
- [IM SDK] 优化重连逻辑。

#### 修复

- [IM SDK] 修复 TypeScript 代码的一些类型错误。
- [IM SDK] 修复 `getConversationlist` 方法的返回值缺少 `customExts` 字段的问题。
- [IM SDK] 修复设置 `useOwnUploadFun` 允许用户自己上传图片时图片消息中的 `size` 字段不生效的问题。

## 版本 V4.1.2 Dev 2022-11-08

### 新增特性

- [IM SDK] [创建群组方法 `createGroup`](group_manage.html#创建群组) 和[修改群信息方法 `modifyGroup`](group_attributes.html#修改群组信息) 新增 `ext` 字段支持群扩展信息。
- [IM SDK] 群组通知事件增加[群组信息修改事件 `updateInfo`](group_manage.html#监听群组事件)。
- [IM SDK] 新增[聊天室消息优先级](#聊天室消息优先级与消息丢弃逻辑)。
- [IM SDK] 支持同时[对多个群组成员禁言和解除禁言](group_members.html#管理群组禁言)。

## 版本 V4.1.1 Dev 2022-9-26

### 修复

修复聊天室自定义属性功能中的问题。

## 版本 V4.1.0 Dev 2022-9-16

### 新增特性

- [IM SDK] 新增[聊天室自定义属性功能](room_attributes.html)。
- [IM SDK] 新增 `onLog` 方法，实现用户日志回调。
- [IM SDK] `getJoinedGroups` 方法中新增 `needAffiliations` 和 `needRole` 参数支持获取群组成员数和用户自己的角色。

### 优化

- 增加内嵌文档。
- 优化重连逻辑。

### 修复

[IM SDK] 修复 IM Uniapp 在手机上运行时上报 `addEventListener` 方法相关错误的问题。

## 版本 V4.0.9 2022-7-29

### 新增特性

- [IM SDK] 优化协议，减少数据量。
- [IM SDK] SDK 内部在群组聊天室部分 API 请求时增加 `resourceId`，增加操作的多设备通知提醒。
- [IM SDK] [getJoinedGroups](/document/web/group_manage.html#获取群组列表) 方法中增加请求参数支持返回群组成员人数和自己的角色。

## 版本 V4.0.8 2022-6-17

### 新增特性

- [IM SDK] 新增群组事件回调 [onGroupEvent](https://doc.easemob.com/jsdoc/interfaces/Types.EventHandlerType.EventHandlerType.html#onGroupEvent) 和聊天室事件回调 [onChatroomEvent](https://doc.easemob.com/jsdoc/interfaces/Types.EventHandlerType.EventHandlerType.html#onChatroomEvent)。原回调可继续使用；
- [IM SDK] 新增群聊消息限流错误码 [MESSAGE_CURRENT_LIMITING](/document/web/error.html)
- [IM SDK] 邀请加入群聊回调 `onGroupChange` 返回中新增 群名称 参数值。

### 优化

- [IM SDK] 支持批量查询群组详情 [getGroupInfo](/document/web/group_manage.html#获取群组详情信息)。

## 版本 V4.0.7 2022-5-25

### 新增特性:

- [IM SDK] 新增消息子区（message thread）功能；
- [IM SDK] 新增 [getConversationList](/document/web/conversation_list.html) 方法解析会话中的最新一条消息；

### 优化：

- [IM SDK] 消息事件监听器中新增 onlineState 字段标记离线消息。

## 版本 V4.0.5 2022-5-16

### 新增特性:

- [IM SDK] 新增举报 API 用于内容审核；
- [IM SDK] 新增推送设置 API，支持不同的推送配置；
- [IM SDK] 增加数据上报功能；
- [IM SDK] 新增获取加入的群组支持分页 API；

### 优化：

- [IM SDK] 创建群组时，支持设置群组人数；
- [IM SDK] 接收到的图片消息增加缩略图 URL；

### 修复：

- [IM SDK] 解决切换账号群组消息有缓存的 BUG。

## 版本 V4.0.4 2022-4-19

:::tip
仅 V4.0.4 及以下版本支持私有化部署。
:::

### 新增特性:

- [IM SDK] 增加用户在线状态(Presence)订阅功能。
- [IM SDK] 增加自动翻译接口。除了按需翻译，IM 实现自动翻译。

### 优化：

- [IM SDK] 小程序不需要 isHttpDNS 参数。

### 修复：

- [IM SDK] 修复 Uni_SDK 无法运行到浏览器问题。
- [IM SDK] 修复创建群组时无法修改群简介问题。
- [IM SDK] 修复 SSR 兼容性。

## 版本：v4.0.3 2022-1-19

- [IM SDK] 'fetchGroupSharedFileList' 支持分页。
- [IM SDK] 默认关闭 DNS。

## 版本：v4.0.2 2022-1-14

- [IM SDK] 增加删除会话 API。
- [IM SDK] 位置消息增加 “buildingName” 字段。
- [IM SDK] 增加非好友发消息失败 error。
- [IM SDK] 增加因全局禁言发消息失败 error。
- [IM SDK] 增加支持钉钉小程序。
- [IM SDK] 修复不回调 “onChannelMessage” 事件 bug。
- [IM SDK] 修复其他已知错误。

## 版本：v4.0.1 2021-12-10

- [IM SDK] 修复类型错误。
- [IM SDK] 修复收不到 delivery ack。
- [IM SDK] 修复群公告不能设为空。
- [IM SDK] 修复聊天中禁言报错。
- [IM SDK] 更新部分函数命名与注释。
- [IM SDK] 增加部分错误码。

## 版本：v4.0.0 2021-10-22

- [IM SDK] 支持 typescript
- [IM SDK] 发送消息、好友操作支持 Promise
- [IM SDK] 支持使用 agora token 登录
- [IM SDK] 增加新的事件监听方式 eventHandler
- [IM SDK] 增加新的构造消息 API
- [IM SDK] 优化部分 API，减少不必要参数，增加错误提示。
- [IM SDK] 修复部分已知 bug

## 版本：v3.6.3 2021-07-30

- [IM SDK] 增加下载文件验证 secret 功能
- [IM SDK] 增加发送消息被自定义拦截的错误类型
- [IM SDK] 优化漫游消息 api, 增加 start 参数，指定开始拉取消息的位置
- [IM SDK] 修复百度小程序兼容问题
- [IM SDK] 登录上报区分不同小程序

## 版本：v3.6.2 2021-07-08

- [IM SDK] 修复 ios14.5 以上小程序如果使用插件导致 SDK 登录不成功

## 版本：v3.6.0 2021-06-30

- [IM SDK] 更新 dnsconfig
- [IM SDK] 启用 dns 的情况下使用动态端口
- [IM SDK] 优化输出日志
- [IM SDK] 修复重连问题

## 版本：v3.5.1 2021-04-14

- [IM SDK] 增加用户属性功能 [用户属性](https://docs-im.easemob.com/im/web/basics/profile)
- [IM SDK] 增加修改推送昵称 API
- [IM SDK] 申请加群 joinGroup 方法增加请求信息参数 message
- [IM SDK] 修复退出聊天室没有清除缓存消息

## 版本：v3.5.0 2021-03-01

- [IM SDK] 登陆接口去掉 apiUrl 参数
- [IM SDK] 默认关闭日志采集
- [IM SDK] 修复未登录状态发消息报错
- [IM SDK] 修复大型聊天室消息堵塞

## 版本：v3.4.2 2021-01-09

- [IM SDK] 增加获取会话列表功能
- [IM SDK] 增加 channel ack 消息
- [IM SDK] 修复由 uniapp 生成 h5 时登陆报错
- [IM SDK] 修复部分已知 bug

## 版本：v3.4.0 2020-12-10

- [IM SDK] 增加支持支付宝小程序
- [IM SDK] 增加移动端上传推送 token api
- [IM SDK] 撤回消息、已读消息增加 from、to 字段
- [IM SDK] CMD、自定义消息增加 type 字段
- [音视频 SDK] 支持 uniapp 生成的原生客户端

## 版本：v3.3.2 2020-10-19

- [IM SDK] 增加支持设置固定 deviceId
- [IM SDK] 修改 getGroup 方法去掉参数
- [IM SDK] 修复拉历史消息 bug
- [IM SDK] 修复发送附件消息对 3.3.0 之前 api 的兼容问题
- [IM SDK] 修复使用 uniapp 打包的 app，退到后台回来时 websocket 无法连接的问题
- [小程序 demo] 增加支持发视频消息
- [小程序 demo] 增加提示注册失败原因：用户名超出 64 字节
- [小程序 demo] 增加支持会话列表显示陌生人会话

## 版本：v3.3.0 2020-09-16

- [IM SDK] 增加支持 promise
- [IM SDK] 增加 onContactInvited、onContactDeleted、onContactAdded、onContactRefuse、onContactAgreed 好友相关的回调
- [IM SDK] 增加 addContact、deleteContact、acceptInvitation、declineInvitation 代替原 subscribe、removeRoster、subscribed、unsubscribed 好友操作 API
- [IM SDK] 增加状态码 40，在 onError 中 type 为 40 会回调出因为 socket 断开导致发送失败的消息
- [IM SDK] 修改默认的 resource，以便区分 web 端和小程序端的用户
- [IM SDK] 修改 getChatRooms 获取聊天室 API，去掉 apiUrl 参数
- [IM SDK] 修改 构造 cmd 消息 API, 去掉 msg 参数
- [IM SDK] 优化构造消息 API，使用 chatType 来区分消息类型（单聊/群聊/聊天室）
- [IM SDK] 修复发送位置消息成功后并不执行 success 回调
- [IM SDK] 增加容错处理

## 版本：v3.2.2 2020-08-25

- [IM SDK] 创建群组时增加被邀请人是否需要同意的参数
- [IM SDK] onError 回调增加 error message

## 版本：v3.2.1 2020-07-28

- [IM SDK] 修改创建聊天室 api，不需要传 owner 参数
- [demo] 修复小程序收到好友申请，如果发起方不在线，那么收到方拒绝后发起方收不到回调
- [demo] 修复 iOS 小程序在音视频会议后，发送单聊消息不显示，必须退出单聊窗口再进入才会显示
- [demo] 修复小程序音视频通话过程中关闭美颜，美颜图标和字体，只有字体置灰
- [demo] 增加小程序音视频时显示时长

## 版本：v3.2.0 2020-07-09

- [IM SDK] 增加创建聊天室、查询\修改聊天室详情、查询\设置\移除管理员
- [IM SDK] 修复对消息扩展类型解析错误
- [IM SDK] 修复发送图片、文件消息时，直接发送 url 时下载不成功
- [IM SDK] 修改对于被禁言、拉黑等导致的发送消息失败，将从 fail 回调出去，不再从全局的 onError 回调

## 版本：v3.1.6 2020-07-03

- [音视频 SDK] 增加 joinRoom API
- [demo] 部分机型在视频会议时被来电打断后，无法继续推拉流，此时自动退出会议。

## 版本：v3.1.4 2020-06-11

- [IM SDK] 支持附件下载重定向
- [IM SDK] 支持图片检测违规抛出单独的异常
- [IM SDK] 增加分页获取聊天室成员 api
- [IM SDK] 修复收消息有延迟情况
- [音视频 SDK] 增加断网重连

## 版本：v3.1.2 2020-05-14

- [IM SDK] 增加上传修改群/聊天室公告、获取群/聊天室公告、上传/下载/删除群/聊天室文件、获取群/聊天室文件列表, 增加上传修改群/聊天室公告、获取群/聊天室公告、上传/下载/删除群/聊天室文件、获取群/聊天室文件列表
- [IM SDK] 修改重连间隔
- [IM SDK] 去掉对上传文件大小的限制, 由服务端来限制
- [IM SDK] 修复拉历史消息 bug
- [IM SDK] 修复自定义消息没有 time

## 版本：v3.1.1 2020-04-28

- [demo] 适配 v3.1.1 IM SDK
- [IM SDK] 更新私有协议, 与 web 端统一
- [IM SDK] 增加漫游消息 api
- [IM SDK] 增加聊天室禁言、解除禁言、获取禁言列表、加入黑名单、移除黑名单、获取黑明单列表等 api
- [IM SDK] 增加聊天室、群组一键禁言、白名单等 api
- [IM SDK] 增加发送自定义消息
- [IM SDK] 增加群组回执
- [音视频 SDK] 兼容 v3.1.1 IM SDK
- [音视频 SDK] 增加关闭摄像头的回调事件
- [音视频 SDK] 修复不能销毁会议

## 版本：v1.3.1 2020-02-16

- [demo] 调整音视频最大码率为 300

## 版本：v1.3.0 2020-02-10

- [demo] 增加音视频会议功能。
- [sdk] 增加音视频 SDK src/emedia/emedia_for_miniProgram.js。

## 版本：v1.2.0 2019-06-24

- [demo] 增加消息状态，比如断网时发的消息显示失败。
- [demo] 增加 socket 连接成功的提示。
- [demo] 修改了语音消息播放时再下载。
- [demo] 修复聊天页面切后台，再切前台收到的离线消息有重复。
- [demo] 由 rest1 迁移到 rest2 后开始校验 token,导致附件消息收不到。
- [demo] 语音发送成功后点击听取后，语音依然闪烁动画。
- [demo] 联系人分类为#，显示问题。
- [sdk] 增加 onSocketConnected 事件 – socket 连接成功。
- [sdk] onError 增加 type='sendMsgError' - 发送消息失败。
- [sdk] sdk 重连时关闭上次创建的的 socket，而不是所有的 socket。

## 版本：v1.1.1 2019-04-10

- [sdk] 增加重连机制
- [demo] 实时更新联系人列表
- [bug] 修复进入群组时，群组名称错误
- [bug] 修复可以同时播放多条语音
- [bug] 群组聊天页显示问题

## 版本：v1.1.0 2019-03-22

- [sdk] [demo] 增加 token 登录
- [demo] 新版 demo，修改 ui
- [demo] 增加搜索功能
- [demo] 增加联系人按字母排序
- [demo] 增加最近聊天按时间排序
- [demo] 增加群组消息提醒
- [demo] 增加测滑删除功能
- [demo] 增加聊天历史分页
- [demo] 增加用户名不区分大小写
- [demo] 增加接收文件消息提示
- [demo] 适配 iphone X，以及 XS max 等机型
- [demo] 主页面由联系人页改为聊天页
- [bug] 修改 A 给好友 B 发语音消息，B 没有显示语音的未读消息数
- [bug] iOS 聊天界点击输入框进行输入时历史消息展示不合理
- [bug] iOS 端小程序收到消息时，会话界面来消息的提醒有时会没有提醒，只显示消息数
- [bug] 语音消息时长为 0

## 版本：v1.0.5 2018-09-12

新功能：

- [sdk]开放注册
- [sdk]登录
- [sdk]退出登录
- [sdk]监听 IM 链接状态
- [sdk]消息发送（文字、图片、语音等）
- [sdk]接收消息
- [sdk]获取用户会话和聊天记录
- [sdk]添加好友
- [sdk]删除好友
- [sdk]同意添加好友请求
- [sdk]拒绝添加好友请求
- [sdk]获取用户好友列表
- [sdk]收发群组消息
- [sdk]创建群组
- [sdk]添加群组成员
- [sdk]退出群组
- [sdk]解散群组
- [sdk]获取完整的群成员列表
- [sdk]获取群组列表
- [sdk]获取群组详情
- [demo]获取未读消息数
- [demo]用户未读消息数清空
- [demo]清空用户会话和聊天记录
