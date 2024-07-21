from flask import Flask, render_template, request, redirect
import json
import random

app = Flask(__name__)

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
        return None

    followers = process_followers_list(followers_json)
    return {
        'user': user,
        'followers': followers
    }

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        target_username = request.form['username']

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

        result = wrapper(search_json, followers_json, target_username)
        if result:
            return render_template('result.html', result=result)
        else:
            return error()
    else:
        return render_template('search.html')

@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')



if __name__ == '__main__':
    app.run(debug=True)