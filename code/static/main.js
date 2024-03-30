// main.js

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get the form element
    var form = document.getElementById('recommendation-form');

    // Add submit event listener to the form
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior
        
        // Get the input value
        var titleInput = document.getElementById('title');
        var title = titleInput.value;

        // Send AJAX request to the Flask backend
        fetch('/recommend?title=' + title)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle the response data
                if (data.error) {
                    alert(data.error);
                } else {
                    // Display recommendations on the current page
                    displayRecommendations(data);
                }
            })
            .catch(error => console.error('Error:', error));
    });
});

function displayRecommendations(data) {
    var moviesList = document.getElementById('movies-list');
    var tvShowsList = document.getElementById('tv-shows-list');

    // Clear previous recommendations
    moviesList.innerHTML = '';
    tvShowsList.innerHTML = '';

    // Add movies to the list
    data.movies.forEach(function(movie) {
        var listItem = document.createElement('li');
        listItem.textContent = movie;
        moviesList.appendChild(listItem);
    });

    // Add TV shows to the list
    data.tv_shows.forEach(function(tvShow) {
        var listItem = document.createElement('li');
        listItem.textContent = tvShow;
        tvShowsList.appendChild(listItem);
    });
}
