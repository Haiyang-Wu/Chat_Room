## 协议格式

客户端请求格式

```python
# 注册请求格式
{
  'mode': 'register',
  'user': 'fei',
  'pwd': 123
}

# 登陆请求格式
{
  'mode': 'login',
  'user': 'fei',
  'pwd': 123
}

# 聊天请求格式
{
  'mode': 'chat',
  'user': 'fei',
  'msg': 'hello',
  'time': '2023-05-01 12:00:00',
  'token': 'jflkajflajfjas'
}

# 文件请求格式
{
  'mode': 'file',
  'user': 'fei',
  'file_name': 'abc.txt',
  'file_size': 52532235,
  'md5': 'faifjaslkflafl',
  'time': '2023-05-01 12:00:00',
  'token': 'jflkajflajfjas'
}

# 重连请求格式
{
  'mode': 'reconnect',
  'user': 'fei',
  'token': 'jflkajflajfjas'
}

# 管理员修改公告请求格式
```

服务端响应

```python
# 注册响应格式
{
  'code': 200,
  'mode': 'register',
  'msg': '注册成功！'
}
{
  'code': 400,
  'mode': 'register',
  'msg': '用户名已存在！'
}

#登陆响应格式
{
  'code': 200,
  'mode': 'login',
  'user': 'fei',
  'msg': '登陆成功！',
  'token': 'jflakfajflkjalfja',
  'notice': '群公告',
  'users': ('小飞', '中飞', '大飞')
}
{
  'code': 400,
  'mode': 'login',
  'user': 'fei',
  'msg': '账号密码错误！'
}

# 广播响应格式
{
  'code': 200,
  'mode': 'broadcast',
  'status': 'online',
  'user': 'fei',
}
{
  'code': 200,
  'mode': 'broadcast',
  'status': 'offline',
  'user': 'fei',
}

# 聊天响应格式
{
  'code': 200,
  'mode': 'chat',
  'user': 'fei',
  'msg': 'hello',
  'time': '2023-05-01 12:00:00',  # 世界标准时间
}

# 文件响应格式
{
  'code': 200,
  'mode': 'file',
  'user': 'fei',
  'file_name': 'abc.txt',
  'file_size': 52532235,
  'md5': 'faifjaslkflafl',
  'time': '2023-05-01 12:00:00',
}

# 重连响应格式
{
  'code': 200,
  'mode': 'reconnect',
  'users': ('小飞', '中飞', '大飞')
}
{
  'code': 400,
  'mode': 'reconnect',
  'msg': 'token无效，请重新登陆'
}

# 公告响应格式
```





