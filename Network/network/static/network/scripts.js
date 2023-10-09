document.addEventListener('DOMContentLoaded', () => {
    //Event listeners
    let currentpage = 'allposts';
    let page = 1;
    if (typeof csrftoken !== 'undefined') {
        document.querySelector('#content-submit').addEventListener('click', () => new_post(csrftoken, page));
        document.addEventListener('click', event => {
            const element = event.target;
            if (element.id == 'follow-btn') {
                console.log(element.dataset.num);
                follow(csrftoken, element);
            }
        })
    }
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.id.startsWith('author')) {
            load_profile(element, page);
        }
        if (element.id == 'previous') {
            page--;
            if (currentpage == 'allposts') {
                load_posts('allposts', page);
            }
            else {
                load_profile(element, page);
            }
        }
        if (element.id == 'next') {
            page++;
            if (currentpage == 'allposts') {
                load_posts('allposts', page);
            }
            else {
                load_profile(element, page);
            }
        }
    })
    load_posts('allposts', page);
})

function new_post(csrftoken, page) {
    console.log(csrftoken);
    console.log(csrftoken.length);
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
              load_posts('allposts', page);
        });
    }
}

function load_posts(category, page) {
    //Load view and uload others
    document.querySelector('#create-new').style.display = 'block';
    document.querySelector('#allposts-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    //Fetch data
    fetch(`/postscat/${category}/${page}`)
    .then(response => response.json())
    .then(posts => {
        if (posts.hasOwnProperty('error')) {
            if (posts.error == 'page < 1') {
                console.log(2);
                page++;
            }
            if (posts.error == 'page > max') {
                console.log(1);
                console.log(page);
                page--;
                console.log(page);
            }
            console.log(posts.error == 'page > max');
            //console.log(posts.error);
            //console.log(page);
            return false;
        }
        document.querySelector('#allposts-view').innerHTML = '';
        // Print posts
        posts.forEach(add_post);
    })
    .catch(error => {
        console.log('Error:', error);
    });

    function add_post(content) {
        if (typeof currentUserId !== 'undefined' && currentUserId == content.author_id) {
            let post = document.createElement('div');
            post.innerHTML = `<a href="#"><h2 data-num="${content.author_id}" id="author${content.author_id}">${content.author}</h2></a>
            <a href="" data-num="${content.id}" id="Edit">Edit</a>
            <p id="post-content">${content.content}</p>
            <p id="post-dateTime">${content.dateTime}</p>
            <p id="likes">${content.likes}</p>`;
            post.className = 'post';
            document.querySelector('#allposts-view').append(post);
        }
        else {
            let post = document.createElement('div');
            post.innerHTML = `<a href="#"><h2 data-num="${content.author_id}" id="author${content.author_id}">${content.author}</h2></a>
            <p id="post-content">${content.content}</p>
            <p id="post-dateTime">${content.dateTime}</p>
            <p id="likes">${content.likes}</p>`;
            post.className = 'post';
            document.querySelector('#allposts-view').append(post);
        }
    }
    currentpage = 'allposts';
}

function load_profile(author, page) {
    document.querySelector('#create-new').style.display = 'none';
    document.querySelector('#allposts-view').style.display = 'none';
    document.querySelector('#profile-view').style.display = 'block';
    //Fill profile info
    fetch(`/profile/${author.dataset.num}`)
    .then(response => response.json())
    .then(content => {
        //console.log(content);
        document.querySelector('#username').innerHTML = content.username;
        document.querySelector('#followers').innerHTML = `<strong>Followers:</strong>${content.followers.length}`;
        document.querySelector('#following').innerHTML = `<strong>Follows:</strong>${content.following.length}`;
        document.querySelector('#follow-btn').dataset.num = content.id;
        if (typeof currentUserId !== 'undefined') {
            document.querySelector('#follow-btn').innerHTML = (content.followers.includes(parseInt(currentUserId))) ? 'Unfollow' : 'Follow';
        }
    });
    //Load profile posts
    fetch(`/posts/${author.dataset.num}/${page}`)
    .then(response => response.json())
    .then(posts => {
        // Print posts
        document.querySelector('#profile-posts').innerHTML = '';
        posts.forEach(add_post);
    })
    .catch(error => {
        console.log('Error:', error);
    });


    function add_post(content) {
        let post = document.createElement('div');
        if (typeof currentUserId !== 'undefined' && currentUserId == content.author_id) {
                post.innerHTML = `<a href=""><h2 id="author${content.author_id}">${content.author}</h2></a>
                <a href="" data-num="${content.id}" id="Edit">Edit</a>
                <p id="post-content">${content.content}</p>
                <p id="post-dateTime">${content.dateTime}</p>
                <p id="likes">${content.likes}</p>`;
                post.className = 'post';
                document.querySelector('#profile-posts').append(post);
        }
        else {
            post.innerHTML = `<a href=""><h2 id="author${content.author_id}">${content.author}</h2></a>
            <p id="post-content">${content.content}</p>
            <p id="post-dateTime">${content.dateTime}</p>
            <p id="likes">${content.likes}</p>`;
            post.className = 'post';
            document.querySelector('#profile-posts').append(post);
        }
    }
    currentpage = 'profile';
}

function follow(csrftoken, userId) {
    fetch(`/follow/${userId.dataset.num}`, {
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
        load_profile(userId);
        // Handle the response ddd
    })
    .catch(error => {
        console.error('Error:', error);
    });
}