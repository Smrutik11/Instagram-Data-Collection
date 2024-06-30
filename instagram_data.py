# -*- coding: utf-8 -*-

from instagram_private_api import Client
import mysql.connector
from datetime import datetime

# Instagram credentials 
username = 'instagram_username'
password = 'username_password'

# Connect to the MySQL database
db_connection = mysql.connector.connect(
    host="localhost",
    user="mySQL_username",
    password="MySQL_password",
    database="instagram_db",
    charset='utf8mb4',  # Ensure MySQL connection uses UTF-8
    collation='utf8mb4_unicode_ci'
)
cursor = db_connection.cursor()

try:
    # Initialize the Instagram API client 
    api = Client(username, password)
    results = api.feed_timeline()

    # Iterate through the results
    for item in results.get('feed_items', []):
        # Check if the item is a valid post
        if isinstance(item, dict) and item.get('media_or_ad'):
            post = item.get('media_or_ad')
            post_id = post.get('id')
            user = post.get('user', {})
            user_id = user.get('pk')
            timestamp = post.get('taken_at')

            # Convert Unix timestamp to datetime string
            timestamp_str = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            content = post.get('caption', {}).get('text', '')
            if content:
                content = content[:1023]  # Limit content length for MySQL VARCHAR

            likes = post.get('like_count', 0)
            shares = post.get('comment_count', 0)

            # Insert data into the MySQL table with INSERT IGNORE
            insert_query = "INSERT IGNORE INTO instagram_posts (post_id, user_id, timestamp, content, likes, shares) " \
                           "VALUES (%s, %s, %s, %s, %s, %s)"
            insert_values = (post_id, user_id, timestamp_str, content, likes, shares)
            cursor.execute(insert_query, insert_values)
            db_connection.commit()

        else:
            # Ignore entries that have not been posted
            print(f"Ignoring non-post item: {item}")

except Exception as e:
    print(f"Error fetching or storing Instagram data: {str(e)}")

finally:
    # Close database connection
    cursor.close()
    db_connection.close()

