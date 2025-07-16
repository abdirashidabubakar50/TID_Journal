def individual_serial(User) -> dict:
    return {
        "id": str(User["_id"]),
        "username": User["username"],
        "email": User["email"]
    }

def list_serial(users) -> list:
    return[individual_serial(User) for User in users]

def serialize_for_model(User: dict) -> dict:
    if "_id" in User:
        User["_id"] = str(User["_id"])
    return User