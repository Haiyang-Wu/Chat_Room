import aiomysql as aiomysql


async def connect_to_database():
    connection = await aiomysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="wuhaiyang",
        db="chatroom",
    )
    return connection
