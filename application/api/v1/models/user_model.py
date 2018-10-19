class Users():
    """Class contain user model functions"""

    users_dict = []

    def __init__(self, name, username, email, password, gender, role):
        """Initialises the user model"""
        self.name = name
        self.username = username
        self.email = email
        self.password = email
        self.gender = gender
        self.role = role
        

    def create_user(self):
        """Creates a new user"""
        new_user = dict(
            name = self.name,
            username = self.username,
            email = self.email,
            password = self.password, 
            gender = self.gender,
            role = self.role    
        )

        self.users_dict.append(new_user)

        return self.users_dict

    def search_by_username(self, username):
        """search for existing user"""
        user = [user for user in self.users_dict if user['username'] == username]
        return user

    
    def get_all_users(self):
        """Fetches all users"""
        pass

    def get_one_user(self, user_id):
        """Fetches one user by id"""
        pass
