import json
import random


def process_search_results(search_json, target_username):
    data = json.loads(search_json)
    for user_data in data.get('users', []):
        user = user_data.get('user', {})
        if user.get('username') == target_username:
            return {
                'username': user.get('username'),
                'full_name': user.get('full_name'),
                'profile_pic_url': user.get('profile_pic_url')
            }
    return None

def process_followers_list(followers_json):
    data = json.loads(followers_json)
    followers = []
    for follower in data.get('following', []):
        followers.append({
            'username': follower.get('username'),
            'full_name': follower.get('full_name'),
            'profile_pic_url': follower.get('profile_pic_url')  # We'll fill this later
        })
    return followers

def get_random_follower(followers):
    return random.choice(followers) if followers else None

def wrapper(search_json, followers_json, target_username):
    user = process_search_results(search_json, target_username)
    if not user:
        print(f"User {target_username} not found in search results.")
        return
    print(f"Found user: {user['username']}, {user['full_name']}")
    print(f"Profile picture URL: {user['profile_pic_url']}")

    # Process followers list
    followers = process_followers_list(followers_json)
    print(f"\nFound {len(followers)} followers.")

    return followers

def main(search_json, followers_json, target_username):
    # Process search results
    user = process_search_results(search_json, target_username)
    if not user:
        print(f"User {target_username} not found in search results.")
        return

    print(f"Found user: {user['username']}, {user['full_name']}")
    print(f"Profile picture URL: {user['profile_pic_url']}")

    # Process followers list
    followers = process_followers_list(followers_json)
    print(f"\nFound {len(followers)} followers.")

    # You would typically fetch profile pictures for followers here,
    # but for this example, we'll use placeholder URLs
    # for i, follower in enumerate(followers):
    #     follower['profile_pic_url'] = f"https://example.com/{follower['username']}.jpg"

    # Demonstrate random follower selection
    for _ in range(len(followers)):
        random_follower = get_random_follower(followers)
        if random_follower:
            print(f"\nRandom follower: {random_follower['username']}, {random_follower['full_name']}")
            print(f"Profile picture URL: {random_follower['profile_pic_url']}")


if __name__ == "__main__":
    # Example usage
    search_json = '''
    {
    "users": [
        {
        "user": {
            "username": "example_user",
            "full_name": "Example User",
            "profile_pic_url": "https://example.com/example_user.jpg"
        }
        },
        {
        "user": {
            "username": "target_user",
            "full_name": "Target User",
            "profile_pic_url": "https://example.com/target_user.jpg"
        }
        }
    ]
    }
    '''

    followers_json = '''{
    "following": [
        {
        "username": "exampleUser1",
        "full_name": "Example User One",
        "profile_pic_url": "http://example.com/pic1.jpg"
        },
        {
        "username": "exampleUser2",
        "full_name": "Example User Two",
        "profile_pic_url": "http://example.com/pic2.jpg"
        },
        {
        "username": "exampleUser3",
        "full_name": "Example User three",
        "profile_pic_url": "http://example.com/pic3.jpg"
        }
    ]
    }'''
    target_username = "target_user"

    main(search_json, followers_json, target_username)