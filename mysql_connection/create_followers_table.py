from mysql_connection import mydb

# create followers table
followers_table = mydb.cursor()

followers_table.execute("CREATE TABLE followers(id INT AUTO_INCREMENT PRIMARY KEY, user_id INT, follow INT, create_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (follow) REFERENCES users(id))")
