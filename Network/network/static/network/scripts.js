document.addEventListener('DOMContentLoaded', () => {
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    //Event listeners
    document.querySelector('#content-submit').addEventListener('click', () => new_post(csrftoken));
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.id.startsWith('author')) {
            load_profile(element);
        }
        else if (element.id == 'follow-btn') {
            follow(element.dataset.num);
        }
        else {

        }
    })
    load_posts('allposts');
})

function new_post(csrftoken) {
    console.log(csrftoken);
    console.log(csrftoken.length);
    content = document.querySelector('#content').value;
    if (content) {
        fetch('/posts', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken, // Include the CSRF token in the headers
            },
            body: JSON.stringify({
                content: content
            })
        })
        .then(response => response.json())
        .then(result => {
              // Print result
              console.log(result);
              load_posts('allposts');
        });
    }
}

function load_posts(category) {
    document.querySelector('#allposts-view').innerHTML = '';
    //Load view and uload others
    document.querySelector('#create-new').style.display = 'block';
    document.querySelector('#allposts-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    //Fetch data
    fetch(`/postscat/${category}`)
    .then(response => response.json())
    .then(posts => {
        // Print posts
        posts.forEach(add_post);
    });

    function add_post(content) {
        let post = document.createElement('div');
        post.innerHTML = `<a href="#"><h2 data-num="${content.author_id}" id="author${content.author_id}">${content.author}</h2></a>
        <a href="" data-num="${content.id}" id="Edit">Edit</a>
        <p id="post-content">${content.content}</p>
        <p id="post-dateTime">${content.dateTime}</p>
        <p id="likes">${content.likes}</p>`;
        document.querySelector('#allposts-view').append(post);
    }
}

function load_profile(author) {
    document.querySelector('#create-new').style.display = 'none';
    document.querySelector('#allposts-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'block';
    //Fill profile info
    fetch(`/profile/${author.dataset.num}`)
    .then(response => response.json())
    .then(content => {
        //console.log(content);
        document.querySelector('#username').innerHTML = content.username;
        document.querySelector('#followers').innerHTML = content.followers;
        document.querySelector('#following').innerHTML = content.following;
        document.querySelector('#follow-btn').dataset.num = content.id;
    });
    //Load profile posts
    fetch(`/posts/${author.dataset.num}`)
    .then(response => response.json())
    .then(posts => {
        // Print posts
        posts.forEach(add_post);
    });


    function add_post(content) {
        let post = document.createElement('div');
        post.innerHTML = `<a href=""><h2 id="author${content.author_id}">${content.author}</h2></a>
        <a href="" data-num="${content.id}" id="Edit">Edit</a>
        <p id="post-content">${content.content}</p>
        <p id="post-dateTime">${content.dateTime}</p>
        <p id="likes">${content.likes}</p>`;
        document.querySelector('#profile-posts').append(post);
    }
}

function follow(csrftoken, userId) {
    console.log(csrftoken);
    console.log(csrftoken.length);
    fetch(`/follow/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            // Include any necessary data
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        // Handle the response ddd
    })
    .catch(error => {
        console.error('Error:', error);
    });
}