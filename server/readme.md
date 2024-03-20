# Client request formats

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
  'time': '2023-05-01 12:00:00',
  'token': 'jflkajflajfjas'
}

# File request format
{
  'mode': 'file',
  'user': 'fei',
  'file_name': 'abc.txt',
  'file_size': 52532235,
  'md5': 'faifjaslkflafl',
  'time': '2023-05-01 12:00:00',
  'token': 'jflkajflajfjas'
}

# Reconnect request format
{
  'mode': 'reconnect',
  'user': 'fei',
  'token': 'jflkajflajfjas'
}

# Administrator update announcement request format
# Registration response format
{
  'code': 200,
  'mode': 'register',
  'msg': 'Registration successful!'
}
{
  'code': 400,
  'mode': 'register',
  'msg': 'Username already exists!'
}

# Login response format
{
  'code': 200,
  'mode': 'login',
  'user': 'fei',
  'msg': 'Login successful!',
  'token': 'jflakfajflkjalfja',
  'notice': 'Group announcement',
  'users': ('Little Fei', 'Medium Fei', 'Big Fei')
}
{
  'code': 400,
  'mode': 'login',
  'user': 'fei',
  'msg': 'Incorrect account password!'
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
  'time': '2023-05-01 12:00:00',  # World Standard Time
}

# File response format
{
  'code': 200,
  'mode': 'file',
  'user': 'fei',
  'file_name': 'abc.txt',
  'file_size': 52532235,
  'md5': 'faifjaslkflafl',
  'time': '2023-05-01 12:00:00',
}

# Reconnect response format
{
  'code': 200,
  'mode': 'reconnect',
  'users': ('Little Fei', 'Medium Fei', 'Big Fei')
}
{
  'code': 400,
  'mode': 'reconnect',
  'msg': 'Token is invalid, please log in again'
}

# Announcement response format
{
  'code': 200,
  'mode': 'update_notice',
  'msg': 'Announcement updated successfully.'
}
{
  'code': 400,
  'mode': 'update_notice',
  'msg': 'Failed to update the announcement.'
}
