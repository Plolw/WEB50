document.addEventListener('DOMContentLoaded', () => {
    //Event listeners
    
    let page = 1;
    load_posts('allposts', page);
    if (typeof csrftoken !== 'undefined') {
        document.querySelector('#content-submit').addEventListener('click', () => new_post(csrftoken, page));
        document.addEventListener('click', event => {
            const element = event.target;
            if (element.id == 'follow-btn') {
                follow(csrftoken, element);
            }
            if (element.id.startsWith('edit')) {
                load_edit(element.dataset.num);
            }
            if (element.id.startsWith('content-edit-submit')) {
                edit(csrftoken, element.dataset.num);
            }
            if (element.id.startsWith('btn-likes')) {
                console.log("post liked!");
                console.log(page);
                like(csrftoken, element.dataset.num, page);
            }
        })
    }
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.id == 'nav-following') {
            load_posts('following', page);
        }
        if (element.id.startsWith('author')) {
            page = 1;
            load_profile(element, page);
        }
        if (element.id == 'previous') {
            page--;
            if (currentpage == 'allposts') {
                load_posts('allposts', page);
            }
            else {
                load_profile(profilelement, page);
            }
        }
        if (element.id == 'next') {
            page++;
            if (currentpage == 'allposts') {
                load_posts('allposts', page);
            }
            else {
                load_profile(profilelement, page);
            }
        }
    })
})

function new_post(csrftoken, page) {
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
    currentpage = 'allposts';
    document.querySelector('#create-new').style.display = 'block';
    document.querySelector('#allposts-view').style.display = 'block';
    document.querySelector('#profile-view').style.display = 'none';
    //Fetch data
    fetch(`/postscat/${category}/${page}`)
    .then(response => response.json())
    .then(posts => {
        if (posts.hasOwnProperty('error')) {
            if (posts.error == 'page < 1') {
                page++;
            }
            if (posts.error == 'page > max') {
                page--;
            }
            console.log(posts.error == 'page > max');
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
        let liked = '';
        if (typeof currentUserId !== 'undefined') {
            liked = (content.likes.includes(parseInt(currentUserId))) ? 
            `<i id="btn-likes${content.id}" data-num="${content.id}" class="fa-solid fa-heart" style="color: #f50000;"></i>` :
            `<i id="btn-likes${content.id}" data-num="${content.id}" class="fa-regular fa-heart" style="color: #f50000;"></i>`;
        }
        if (typeof currentUserId !== 'undefined' && currentUserId == content.author_id) {
            let post = document.createElement('div');
            post.innerHTML = `<a href="#"><h2 data-num="${content.author_id}" id="author${content.author_id}">${content.author}</h2></a>
            <a href="javascript:void(0);" data-num="${content.id}" id="edit${content.id}">Edit</a>
            <div id="post-content${content.id}"><p class="contents">${content.content}</p></div>
            <p id="post-dateTime" class="date_time">${content.dateTime}</p>
            <div id="likes${content.id}"><button style="border: none; background-color: transparent;">${(typeof currentUserId !== 'undefined') ? liked: `<i class="fa-regular fa-heart" style="color: #f50000;"></i>`}</button></div>
            <p id="like${content.id}">${content.likes.length}</p>`;
            post.className = 'post';
            document.querySelector('#allposts-view').append(post);
        }
        else {
            console.log(typeof currentUserId !== 'undefined');
            let post = document.createElement('div');
            post.innerHTML = `<a href="#"><h2 data-num="${content.author_id}" id="author${content.author_id}">${content.author}</h2></a>
            <p id="post-content" class="contents">${content.content}</p>
            <p id="post-dateTime" class="date_time">${content.dateTime}</p>
            <div id="likes${content.id}"><button style="border: none; background-color: transparent;">${(typeof currentUserId !== 'undefined') ? liked: `<i class="fa-regular fa-heart" style="color: #f50000;"></i>`}</button></div>
            <p id="like${content.id}">${content.likes.length}</p>`;
            post.className = 'post';
            document.querySelector('#allposts-view').append(post);
        }
    }
    profilelement = '';
}

function load_profile(author, page) {
    profilelement = author;
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
        if (typeof currentUserId !== 'undefined') {
            let liked = (content.likes.includes(parseInt(currentUserId))) ? 
            `<i id="btn-likes${content.id}" data-num="${content.id}" class="fa-solid fa-heart" style="color: #f50000;"></i>` :
            `<i id="btn-likes${content.id}" data-num="${content.id}" class="fa-regular fa-heart" style="color: #f50000;"></i>`;
        }
        if (typeof currentUserId !== 'undefined' && currentUserId == content.author_id) {
                post.innerHTML = `<a href=""><h2 id="author${content.author_id}">${content.author}</h2></a>
                <a href="javascript:void(0);" data-num="${content.id}" id="edit${content.id}">Edit</a>
                <div id="post-content${content.id}"><p class="contents">${content.content}</p></div>
                <p id="post-dateTime" class="date_time">${content.dateTime}</p>
                <div id="likes${content.id}"><button style="border: none; background-color: transparent;">${(typeof liked !== 'undefined') ? liked: `<i class="fa-regular fa-heart" style="color: #f50000;"></i>`}</button></div>
                <p id="like${content.id}">${content.likes.length}</p>`;
                post.className = 'post';
                document.querySelector('#profile-posts').append(post);
        }
        else {
            post.innerHTML = `<a href=""><h2 id="author${content.author_id}">${content.author}</h2></a>
            <p id="post-content" class="contents">${content.content}</p>
            <p id="post-dateTime" class="date_time">${content.dateTime}</p>
            <div id="likes${content.id}"><button style="border: none; background-color: transparent;">${(typeof liked !== 'undefined') ? liked: `<i class="fa-regular fa-heart" style="color: #f50000;"></i>`}</button></div>
            <p id="like${content.id}">${content.likes.length}</p>`;
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

//function edit(csrftoken, postId) {}

function load_edit(postId) {
    let cont = document.querySelector(`#post-content${postId}`).firstElementChild.innerHTML;
    let element = document.querySelector(`#post-content${postId}`);
    let form = document.createElement('form');
    form.innerHTML = `
    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
    <textarea class="form-control" id="contentEdit${postId}" name="contentEdit" placeholder="Write your post">${cont}</textarea>
    <input id="content-edit-submit${postId}" data-num="${postId}" class="btn btn-primary" type="button" value="Save">`;
    element.innerHTML = '';
    element.appendChild(form);
}

function edit(csrftoken, postId) {
    cont = document.querySelector(`#contentEdit${postId}`).value;
    fetch(`/edit/${postId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            content: cont
        })
    });
    newcont = document.createElement('p');
    newcont.innerHTML = cont;
    element = document.querySelector(`#post-content${postId}`);
    element.innerHTML = '';
    element.appendChild(newcont);
}

function like(csrftoken, postId, page) {
    console.log(page);
    fetch(`/edit/${postId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            liker: currentUserId
        })
    })
    .then(response => response.json())
    .then(() => {
        reload(page)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function reload(page) {
    console.log(page);
    if (currentpage == 'allposts' || currentpage == 'following') {
        load_posts(currentpage, page);
    }
    if (currentpage == 'profile') {
        load_profile(profilelement, page);
    }
}