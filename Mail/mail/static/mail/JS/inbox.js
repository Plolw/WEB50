document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Load email
  document.addEventListener('click', event => {
    const element = event.target;
    if (element.id.startsWith('email')) {
      load_email(element);
    }
  })

  // Archive
  document.addEventListener('click', event => {
    const element = event.target;
    if (element.id === 'archivebtn') {
      archive_email(element.dataset.id);
    }
  })
  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Get E-mail data
  document.querySelector('#compose-form').onsubmit = () => {
    let recipients = document.querySelector('#compose-recipients').value;
    let subject = document.querySelector('#compose-subject').value;
    let body = document.querySelector('#compose-body').value;
    
    //POST email data
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });

    //Redirect to sent
    load_mailbox('sent')
    return false;
  }
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Fetch info
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      emails.forEach(add_email);
      // ... do something else with emails ...
  });

  function add_email(content) {
    let email = document.createElement('div');
    email.innerHTML = `<a id="email${content.id}" data-id="${content.id}" class="email" href="#"><div>${content.sender}</div><div>${content.subject}</div><div>${content.timestamp}</div></a>`;
    if (content.read == false) {
      email.style.background = 'white';
    } else {
      email.style.background = 'lightgrey';
    }
    document.querySelector('#emails-view').append(email);
  }
}

function load_email(mail) {
  fetch(`/emails/${mail.dataset.id}`)
  .then(response => response.json())
  .then(email => {
    document.querySelector('#from').innerHTML = `${email.sender}`;
    document.querySelector('#to').innerHTML = `${email.recipients}`;
    document.querySelector('#subject').innerHTML = `${email.subject}`;
    document.querySelector('#timestamp').innerHTML = `${email.timestamp}`;
    document.querySelector('#archivebtn').value = email.archived ? 'Unarchive': 'Archive';
  });
  fetch(`/emails/${mail.dataset.id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
  document.querySelector('#archivebtn').setAttribute('id', `${mail.dataset.id}`);
}

function archive_email(id) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: email.archived? 'True': 'False'
    })
  });
  document.querySelector('#archivebtn').value = email.archived ? 'Unarchive': 'Archive';
}