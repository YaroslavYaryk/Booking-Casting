from users.services import user_handle


def change_user_password_admin(data, user):
    print(data)
    print(user)
    if data["password1"] == data["password2"]:
        user.set_password(data["password1"])
        user.save()
    else:
        raise ValueError("Password dont match")
    print("set new password")


def delete_user(user_id):
    user_handle.get_user_by_id(user_id).delete()


def delete_user_ability(id) :
    return user_handle.get_user_ability_by_id(id).delete()
