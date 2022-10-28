from mysql_connection.mysql_connection import *

# start user class
class User:
    def __init__(self,first_name,last_name,email,password,phone_number):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone_number = phone_number

# start login function scope
    def login(self):
        self.email = input("email: ")
        self.password = input("password: ")
    # get data from db for check email and password
        get_users_from_db = mydb.cursor()
        sql ="SELECT * FROM users where email = %s and password = %s"
        get_users_from_db.execute(sql,[(self.email),(self.password)])
        users = get_users_from_db.fetchall()
        # save user id
        if users:
            global id
            id = []
            for i in users:
                for j in i:
                    id.append(j)
            print(f'*****HELLO {id[1]}*****')
            User.login_menu()
            return id[0]
        else:
            print("your password or email is incorrect!")
# end login function scope

# start register function scope
    def register(self):
        self.first_name = input("your first name: ")
        self.last_name = input("your last name: ")
        self.email = input("your email: ")
        self.phone_number = input("your phone number: ")
        self.password = input("your password: ")
        # save data of user in db
        create_new_user = mydb.cursor()
        create_new_user.execute("INSERT INTO users (first_name, last_name, email, password, phone_number) VALUES(%s, %s, %s, %s, %s)",
                           (self.first_name, self.last_name, self.email, self.password, self.phone_number))
        
        mydb.commit()
        create_new_user.close()
        # get id from user
        last_user_db = mydb.cursor()
        last_user_db.execute("SELECT * FROM users ORDER BY ID DESC LIMIT 1")
        user = last_user_db.fetchall()
        # save id of user that register
        global id
        id = []
        for i in user:
            for j in i:
                id.append(j)
        
        print("****** your account created successfully! ******\n")
        print(f'********* WELCOME {id[1]} *********')
        User.login_menu()
        return id[0]
# end register function scope

# start login_menu function scope for user
    def login_menu():
        while True:
            print("1. your posts\n2. your followers\n3. your following\n4. create new post\n5. follow user\n6. unfollow user\n7. Exit")
            menu_1 = int(input("please select: "))
            if menu_1 == 4:
                Post(None).set_text()
            elif menu_1 == 1:
                Post(None).get_user_post()
            elif menu_1 == 5:
                Follower(None,None,None,None,None).set_follow()
            elif menu_1 == 2:
                Follower(None,None,None,None,None).get_follower()
            elif menu_1 == 3:
                Follower(None,None,None,None,None).get_following()
            elif menu_1 == 6:
                Follower(None,None,None,None,None).unfollow()
            elif menu_1 == 7:
                break
#end login_menu fuction scope

#end User class



#start Post class
class Post:
    def __init__(self,text):
        self.text = text

    # start set_text function scope for every user
    def set_text(self):
        print("please enter your text: ")
        self.text = input("")
        
        # save data in db
        create_new_post = mydb.cursor()
        create_new_post.execute("INSERT INTO posts (text, user_id) VALUES(%s, %s)",
                           (self.text,id[0]))
        mydb.commit()
        create_new_post.close()
        mydb.close()
        print("your post created!")
    # end set_text function scope

    # start get_user_post scope for gave all posts of every user
    def get_user_post(self):
        # check for id login user
        user_posts = mydb.cursor()
        user_posts.execute("SELECT text FROM posts WHERE user_id = %s",[(id[0])])
        posts = user_posts.fetchall()
        c = 1
        if posts:
            for i in posts:
                for j in i:
                    print(f'{c}. {j}')
                    c += 1
        else:
            print("please create new post")
    # end get_user_post scope 
#end Post class

# start Follower class
class Follower(User):
    # start set follower scope for every user can select follower for own self
    def set_follow(self):
        print("which user do you want to follow? ")
        get_user_for_follow = mydb.cursor()
        get_user_for_follow.execute("SELECT id,first_name,last_name,email FROM users WHERE id != %s",[(id[0])])
        follow_user = get_user_for_follow.fetchall()
        for i in follow_user:
            print(i)
        self.follow = int(input("please enter user id to follow that? "))
        set_follow = mydb.cursor()
        set_follow.execute("INSERT INTO followers (user_id, follow) VALUES(%s, %s)",
                                (id[0],self.follow))  
        mydb.commit()
        set_follow.close()
        print("you follow successfully!")
    # end set follower scope

    # start get follower: all user can read name of own followers
    def get_follower(self):
        # list of follower id from follower table
        get_follower_id = mydb.cursor()
        get_follower_id.execute("SELECT user_id FROM followers WHERE follow = %s",[(id[0])])
        user_followers_id = get_follower_id.fetchall()
        follower_id = []
        if user_followers_id:
            for i in user_followers_id:
                for j in i:
                    follower_id.append(j)
        else:
            print("Ops,,, no body follow you.")

        # name from users table 
        get_follower_name = mydb.cursor()
        for num in follower_id:
            get_follower_name.execute("SELECT first_name FROM users WHERE id = %s",[(num)])
            user_follower_name = get_follower_name.fetchall()
            print(user_follower_name)
    # end get_follower scope

    # start get following:  all user can read name of own following
    def get_following(self):
        # list of following id from follower table
        get_following_id = mydb.cursor()
        get_following_id.execute("SELECT follow FROM followers WHERE user_id = %s",[(id[0])])
        user_following_id = get_following_id.fetchall()
        following_id = []
        if user_following_id:
            for i in user_following_id:
                for j in i:
                    following_id.append(j)
        else:
            print("please follow your firend!")

        # name from users table
        get_following_name = mydb.cursor()
        for num in following_id:
            get_following_name.execute("SELECT id,first_name FROM users WHERE id = %s",[(num)])
            user_following_name = get_following_name.fetchall()
            print(user_following_name)
    # end get following scope

    #start unfollow scope for unfollow following
    def unfollow(self):
        Follower(None,None,None,None,None).get_following()
        print("please enter id that you wnat to unfollow: ")
        unfollow_id = int(input(""))
        unfollow_following = mydb.cursor()
        unfollow_following.execute("DELETE FROM followers WHERE follow =%s",[(unfollow_id)])
        mydb.commit()
        print("you unfollow successfully!")
    # end unfollow scope
# end Follower claas


# create varaible that user in main.py
user_login = User(None,None,None,None,None)
user_register = User(None,None,None,None,None)