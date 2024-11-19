"""
Main driver for a simple social network project
"""

import csv
import users
import user_status


def init_user_collection():
    """
    Creates and returns a new instance of UserCollection
    """
    return users.UserCollection()


def init_status_collection():
    """
    Creates and returns a new instance of UserStatusCollection
    """
    return user_status.UserStatusCollection()


def load_users(filename, user_collection):
    """
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    """
    try:
        with open(filename, mode="r", encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if all(
                        key in row and row[key]
                        for key in ["USER_ID", "EMAIL", "NAME", "LASTNAME"]
                ):
                    user_collection.add_user(
                        row["USER_ID"], row["EMAIL"], row["NAME"], row["LASTNAME"]
                    )
                else:
                    print(f"Skipping invalid row: {row}")
                    return False
            return True
    except FileNotFoundError:
        return False
    except KeyError:
        return False


def save_users(filename, user_collection):
    """
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such as an invalid filename).
    - Otherwise, it returns True.
    """
    try:
        with open(filename, encoding="utf-8", mode="w", newline="") as csvfile:
            fieldnames = ["USER_ID", "EMAIL", "NAME", "LASTNAME"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user in user_collection.database.values():
                writer.writerow(
                    {
                        "USER_ID": user.user_id,
                        "EMAIL": user.email,
                        "NAME": user.user_name,
                        "LASTNAME": user.user_last_name,
                    }
                )
        return True
    except IOError:
        return False


def load_status_updates(filename, status_collection):
    """
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    """
    try:
        with open(filename, encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["STATUS_ID"] and row["USER_ID"] and row["STATUS_TEXT"]:
                    status_collection.add_status(
                        row["STATUS_ID"], row["USER_ID"], row["STATUS_TEXT"]
                    )
                else:
                    return False
        return True
    except FileNotFoundError:
        print("File Not Found")
        return False


def save_status_updates(filename, status_collection):
    """
    Saves all statuses in status_collection into a CSV file

    Requirements:
    - If there is an existing file, it will overwrite it.
    - Returns False if there are any errors(such an invalid filename).
    - Otherwise, it returns True.
    """
    try:
        with open(filename, mode="w", encoding="utf-8", newline="") as csvfile:
            fieldnames = ["STATUS_ID", "USER_ID", "STATUS_TEXT"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for status in status_collection.database.values():
                writer.writerow(
                    {
                        "STATUS_ID": status.status_id,
                        "USER_ID": status.user_id,
                        "STATUS_TEXT": status.status_text,
                    }
                )
        return True
    except IOError:
        print("IO Error")
        return False


def add_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Creates a new instance of Users and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    """

    if user_id in user_collection.database:
        return False
    return user_collection.add_user(user_id, email, user_name, user_last_name)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    if user_id not in user_collection.database:
        return False
    user = user_collection.database[user_id]
    user.email = email
    user.user_name = user_name
    user.user_last_name = user_last_name
    return True


def delete_user(user_id, user_collection):
    """
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    """
    if user_id not in user_collection.database:
        return False
    user_collection.delete_user(user_id)
    return True


def search_user(user_id, user_collection):
    """
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    """
    if user_id in user_collection.database:
        return user_collection.database[user_id]
    return None


def add_status(user_id, status_id, status_text, status_collection):
    """
    Creates a new instance of UserStatus and stores it in
    status_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in status_collection.
    - Returns False if there are any errors (for example, if
      status_collection.add_status() returns False).
    - Otherwise, it returns True.
    """
    try:
        return status_collection.add_status(status_id, user_id, status_text)
    except IOError:
        print("An error occurred while adding status")
        return False


def update_status(status_id, user_id, status_text, status_collection):
    """
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    """
    print(f"update status: {status_id}")
    print(f"Current database: {status_collection.database}")
    if status_id not in status_collection.database:
        return False
    result = status_collection.modify_status(status_id, user_id, status_text)
    print(f"Update result: {result}")
    return result


def delete_status(status_id, status_collection):
    """
    Deletes a status_id from status_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    """
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
    """
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    """
    return status_collection.search_status(status_id)
