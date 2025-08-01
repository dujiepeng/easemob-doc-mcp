# 撤回消息

<Toc />

发送方可以撤回一条发送成功的消息，包括已经发送的历史消息，离线消息或漫游消息。
- **除了透传消息，其他各类型的消息都支持撤回**。
- 默认情况下，发送方可撤回发出 2 分钟内的消息。你可以在[环信即时通讯云控制台](https://console.easemob.com/user/login)的 **功能配置** > **功能配置总览** > **基础功能** 页面设置消息撤回时长，该时长不超过 7 天。
- 撤回消息时，服务端的消息（历史消息，离线消息或漫游消息）以及消息发送方和接收方的内存和数据库中的消息均会被移出。
- 对于附件类型消息，包括图片、音频和视频和文件消息，撤回消息后，消息附件也相应删除。

## 技术原理

环信即时通讯 IM 通过 `EMChatManager` 和 `EMMessage` 类支持你撤回一条发送成功的消息：

- `recallMessage`：撤回一条发送成功的消息。

## 前提条件

开始前，请确保满足以下条件：

- 完成 SDK 初始化，详见 [快速开始](quickstart.html)。
- 了解环信即时通讯 IM 的使用限制，详见 [使用限制](/product/limitation.html)。

## 实现方法

### 撤回消息

你可以调用 `recallMessage` 方法撤回一条发送成功的消息。消息撤回后，消息的接收方会收到 `onMessagesRecalledInfo` 事件。

对于 4.6.1 及以上版本的 SDK，你可以通过 ext 字段（字符串类型）传入自定义信息。

```dart
try {
  await EMClient.getInstance.chatManager.recallMessage(msgId, ext: 'ext');
} on EMError catch (e) {
}
```

### 设置消息撤回监听

你可以设置消息撤回监听，通过 `onMessagesRecalledInfo` 事件监听发送方对已接收的消息的撤回。

- 若用户在线接收了消息，消息撤回时，该事件中的 `RecallMessageInfo` 中的 `recallMessage` 为撤回的消息的内容，`recallMessageId` 属性返回撤回的消息的 ID。
- 若消息发送和撤回时接收方离线，该事件中的 `EMRecallMessageInfo` 中的 `recallMessage` 为空，`recallMessageId` 属性返回撤回的消息的 ID。

```dart
void onMessagesRecalledInfo(List<RecallMessageInfo> infos) {}
```