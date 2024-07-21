from flask import Flask, render_template, request, redirect, url_for
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
        # grab username
        target_username = request.form['username']
        
        # check if username is sudip.tt0 (hardcode until API)
        if target_username == 'sudip.tt0':
            return redirect(url_for("verify"))
        else:
            return redirect(url_for("error"))
    
    # for GET requests
    return render_template('search.html')

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    return render_template('result.html')

@app.route('/error', methods=['GET'])
def error():
    return render_template('error.html')



if __name__ == '__main__':
    app.run(debug=True)