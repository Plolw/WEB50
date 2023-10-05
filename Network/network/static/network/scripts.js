document.addEventListener('DOMContentLoaded', () => {
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    //Event listeners
    document.querySelector('#content-submit').addEventListener('click', () => new_post(csrftoken));
    document.querySelector('#post-author').addEventListener('click', () => );
    load_posts('allposts');
})

function new_post(csrftoken) {
    content = document.querySelector('#content').value;
    if (content) {
        fetch('/posts', {
            method: 'POST',
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
    document.querySelector('#allposts-view').style.display = 'block';
    document.querySelector('#following-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'none';
    //Fetch data
    fetch(`/posts/${category}`)
    .then(response => response.json())
    .then(posts => {
        // Print emails
        posts.forEach(add_post);
        // ... do something else with emails ...
    });

    function add_post(content) {
        let post = document.createElement('div');
        post.innerHTML = `<a href="" id="post-author" data-num="${content.author_id}"><h2>${content.author}</h2></a>
        <a href="" data-num="${content.id}" id="Edit">Edit</a>
        <p id="post-content">${content.content}</p>
        <p id="post-dateTime">${content.dateTime}</p>
        <p id="likes">${content.likes}</p>`;
        document.querySelector('#allposts-view').append(post);
    }
}

function load_profile(author) {
    fetch(`/posts/${author.dataset.num}`)
    .then(response => response.json())
    .then(content => {
       
    });
}