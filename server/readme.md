## 协议格式

Client request format

```python
# Registration request format
{
  'mode': 'register',
  'user': 'fei',
  'pwd': 123
}

# Login request format
{
  'mode': 'login',
  'user': 'fei',
  'pwd': 123
}

# Chat request format
{
  'mode': 'chat',
  'user': 'fei',
  'msg': 'hello',
  'time': '2024-03-08 12:00:00',
  'token': 'jflkajflajfjas'
}

# File request format
{
  'mode': 'file',
  'user': 'fei',
  'file_name': 'abc.txt',
  'file_size': 52532235,
  'md5': 'faifjaslkflafl',
  'time': '2024-03-08 12:00:00',
  'token': 'jflkajflajfjas'
}

# Reconnection request format
{
  'mode': 'reconnect',
  'user': 'fei',
  'token': 'jflkajflajfjas'
}

# The administrator modified the bulletin request format
```

Server response

```python
# Registration response format
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

# Login response format
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

# Broadcast response format
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

# Chat response format
{
  'code': 200,
  'mode': 'chat',
  'user': 'fei',
  'msg': 'hello',
  'time': '2024-03-08 12:00:00',  # 世界标准时间
}

# File response format
{
  'code': 200,
  'mode': 'file',
  'user': 'fei',
  'file_name': 'abc.txt',
  'file_size': 52532235,
  'md5': 'faifjaslkflafl',
  'time': '2024-03-08 12:00:00',
}

# Reconnection response format
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





