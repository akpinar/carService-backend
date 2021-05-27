class ProfileObject(object):

    def __init__(self, photo, about, firstName, lastName, gender, age, weight, height, inseam, email, phoneNumber,
                 location, friends, onLine):
        self.photo = photo
        self.about = about
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.age = age
        self.weight = weight
        self.height = height
        self.inseam = inseam
        self.email = email
        self.phoneNumber = phoneNumber
        self.location = location
        self.friends = friends
        self.onLine = onLine


class ProfileObjectForFlutter(object):
    notification = True
    email = ''

    def __init__(self, profileImage, username, pinCount):
        self.profileImage = profileImage
        self.username = username
        self.pinCount = pinCount
