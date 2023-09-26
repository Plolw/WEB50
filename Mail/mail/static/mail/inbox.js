document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

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
    email.innerHTML = `<a id="a${content.id}" data-id="${content.id}" class="email" href="#"><div>${content.sender}</div><div>${content.subject}</div><div>${content.timestamp}</div></a>`;
    if (content.read == false) {
      email.style.background = 'white';
    } else {
      email.style.background = 'rgb(86, 147, 232)';
    }
    document.querySelector('#emails-view').append(email);
    element = document.querySelector(`#a${content.id}`);
    element.addEventListener('click', () => {
      fetch(`/emails/${element.dataset.id}`)
      .then(response => response.json())
      .then(email => {
        let from = document.createElement('p');
        from.innerHTML = `${email.sender}`;
        document.querySelector('#from').append(from);
  
        let to = document.createElement('p');
        to.innerHTML = `${email.recipients}`;
        document.querySelector('#to').append(to);
  
        let subject = document.createElement('p');
        subject.innerHTML = `${email.subject}`;
        document.querySelector('#subject').append(subject);
  
        let timestamp = document.createElement('p');
        timestamp.innerHTML = `${email.timestamp}`;
        document.querySelector('#timestamp').append(timestamp);
      });
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#email-view').style.display = 'block';
    });
  }
}