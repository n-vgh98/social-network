from mysql_connection import mydb

# create posts table
posts_table = mydb.cursor()

posts_table.execute("CREATE TABLE posts(id INT AUTO_INCREMENT PRIMARY KEY, text VARCHAR(255) NOT NULL, user_id INT, create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (user_id) REFERENCES users(id))")
