# 撤回消息

<Toc />

单聊、群聊和聊天室聊天支持撤回一条发送成功的消息：

- 对于单聊会话，只支持发送方撤回发送成功的消息。若消息过期，撤回失败。
- 对于群组/聊天室会话，普通成员只能撤回自己发送的消息，若消息过期，撤回失败。群主/聊天室所有者和管理员可撤回其他用户发送的消息，即使消息过期也能撤回。
- **除了透传消息，其他各类型的消息都支持撤回**。
- 默认情况下，发送方可撤回发出 2 分钟内的消息。你可以在[环信即时通讯云控制台](https://console.easemob.com/user/login)的 **功能配置** > **功能配置总览** > **基础功能** 页面设置消息撤回时长，该时长不超过 7 天。
- 撤回消息时，服务端的消息（历史消息，离线消息或漫游消息）以及消息发送方和接收方的内存和数据库中的消息均会被移出。
- 对于附件类型消息，包括图片、音频和视频和文件消息，撤回消息后，消息附件也相应删除。
  
## 技术原理

环信即时通讯 IM 通过 `EMChatManager` 类和 `EMChatMessage` 类支持你撤回一条发送成功的消息：

- `recallMessageWithMessageId`：撤回一条发送成功的消息。

## 前提条件

开始前，请确保满足以下条件：

- 完成 SDK 初始化，详见 [快速开始](quickstart.html)。
- 了解环信即时通讯 IM 的使用限制，详见 [使用限制](/product/limitation.html)。

## 实现方法

### 撤回消息

- 对于 SDK 4.6.0 及以上版本，调用 `recallMessageWithMessageId:ext:completion:` 方法撤回一条发送成功的消息。调用该方法时，你可以通过 `ext` 字段传入自定义信息。消息撤回后，接收方会收到 `messagesInfoDidRecall` 事件。

```objectivec
// 异步方法
[[EMClient sharedClient].chatManager recallMessageWithMessageId:messageId ext:@"extension info" completion:^(EMError *aError) {
    if (!aError) {
        NSLog(@"撤回消息成功");
    } else {
        NSLog(@"撤回消息失败的原因 --- %@", aError.errorDescription);
    }
}];
```

- 对于 SDK 4.6.0 之前的版本，你可以调用 `recallMessageWithMessageId` 方法撤回一条发送成功的消息。该方法不支持通过 `ext` 字段传入自定义信息。

```objectivec
// 异步方法
[[EMClient sharedClient].chatManager recallMessageWithMessageId:messageId completion:^(EMError *aError) {
    if (!aError) {
        NSLog(@"撤回消息成功");
    } else {
        NSLog(@"撤回消息失败的原因 --- %@", aError.errorDescription);
    }
}];
```

### 设置消息撤回监听

你可以设置消息撤回监听，通过 `messagesInfoDidRecall` 事件监听发送方对已接收的消息的撤回。该事件的 `EMRecallMessageInfo` 中的 `recallBy` 为消息撤回者的用户 ID，`recallMessageId` 为撤回的消息 ID，`ext` 为扩展信息，`conversationId` 为撤回的消息所属的会话 ID。

- 若用户在线接收了消息，消息撤回时，该事件中的 `EMRecallMessageInfo` 中的 `recallMessage` 为撤回的消息。
- 若消息发送和撤回时接收方离线，该事件中的 `EMRecallMessageInfo` 中的 `recallMessage` 为空。

```objectivec
- (void)messagesInfoDidRecall:(NSArray<EMRecallMessageInfo *> * _Nonnull)aRecallMessagesInfo;
{
}
```
