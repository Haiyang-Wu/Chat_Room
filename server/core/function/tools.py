import uuid

from server.db.connection import connect_to_database

"""
Generate unique message id
"""
def generate_unique_message_id():
    return str(uuid.uuid4())


"""
Store message to database
"""
async def store_message_to_database(user_id, msg, message_id):
    async with await connect_to_database() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO messages (message_id, user_id, content, status) VALUES (%s, %s, %s, %s)",
                (message_id, user_id, msg, 'sent',)
            )
            await conn.commit()
            return cur.lastrowid  # Return the ID of the newly inserted row


# """
# Logic for message revocation
# """
# def mark_message_as_revoked(message_id):
#     # Find the corresponding message element on the interface and update its display to "This message was revoked"
#     # The implementation details here depend on your user interface framework
#     message_element = find_message_element_by_id(message_id)
#     if message_element:
#         message_element.text = "This message was revoked."


async def save_file_info_to_database(user, file_name, file_size, file_path):
    # Assuming connect_to_database() can establish a database connection
    async with await connect_to_database() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO files (user_id, file_name, file_size, file_path) VALUES (%s, %s, %s, %s)",
                (user, file_name, file_size, file_path)
            )
            await conn.commit()
            return cur.lastrowid  # Assuming an auto-increment ID is used as the unique identifier for the file
