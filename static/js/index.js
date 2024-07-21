// Store data about users' followings and the current user being guessed
let followingData = [];
let currentUser = null;
let currentIndex = 0; // Track the current user index in the shuffled array
let score = 0; // Initialize score
let hintPressCount = 0; // Track the number of times the hint button is pressed

// Update score and display it
function updateScore(correct) {
    if (correct) {
        score++;
        document.getElementById('score').textContent = score;
    }
}

// Modified showHint function
function showHint() {
    if (currentUser && currentUser.name) {
        hintPressCount++; // Increment the hint press count
        const hintLetters = currentUser.name.substring(0, hintPressCount); // Get the first N letters
        document.getElementById('hint').textContent = hintLetters; // Display the hint letters
    }
}

// Shuffle the array to ensure a random order without repetition
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]]; // Swap elements
    }
}

// Fetch user data from server
fetch('/data')
    .then(response => response.json())
    .then(data => {
        data.users.forEach(user => {
            followingData = followingData.concat(user.following);
        });
        shuffleArray(followingData); // Shuffle the followingData array
        displayRandomUser(); // Display the first user from the shuffled array
    })
    .catch(error => console.error('Error fetching data:', error));

// Function to display a user's profile picture
function displayRandomUser() {
    if (currentIndex < followingData.length) {
        currentUser = followingData[currentIndex];
        const imageElement = document.getElementById('pfpImage');
        if (imageElement) {
            imageElement.src = '/static/' + currentUser.pfp; // Set the image source
        }
        currentIndex++; // Move to the next user
        hintPressCount = 0; // Reset the hint press count
    } else {
        alert('Congratulations! You have guessed all users.');
        window.location.href = '/'; // Redirect to the main page
    }
}

// Handle guess submission
document.getElementById('submitBtn').addEventListener('click', function(event) {
    event.preventDefault(); // Stop the form from submitting
    const inputElement = document.querySelector('input[name="username"]');
    if (inputElement && currentUser && inputElement.value === currentUser.name) {
        updateScore(true); // Update the score
        if (currentIndex >= followingData.length) {
            alert('Congratulations! You have guessed all users.');
            window.location.href = '/';
        } else {
            displayRandomUser(); // Display the next user
        }
    } else {
        alert('Wrong guess! Try again.');
    }
    inputElement.value = ''; // Clear the input field
});