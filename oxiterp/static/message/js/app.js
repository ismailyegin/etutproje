let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

function updateUserList() {
    $.getJSON('api/v1/kul/', function (data) {
        console.log(data);
        userList.children('.user').remove();
        for (let i = 0; i < data.count; i++) {
            console.log('beklenilen =' + data.results[i]['username'])
            const userItem = ` <a class="list-group-item user" id="${data.results[i]['username']}"><img class="img-circle" style="width: 30px;height: 30px;" src='/media/${data.results[i]['image']}'>    ${data.results[i]['first_name']} ${data.results[i]['last_name']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentRecipient(selected.id);
        });
    });
}

function drawMessage(message) {
    console.log("draw mesaj ");
    let position = 'left';
    const date = new Date(message.creationDate);
    if (message.user === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(recipient) {
    console.log("get convert");
    $.getJSON(`/sbs/message/api/v1/mesaj/?target=${recipient}`, function (data) {
        console.log(data);
        messageList.children('.message').remove();
        for (let i = data['results'].length - 1; i >= 0; i--) {
            drawMessage(data['results'][i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}
function getMessageById(message) {
    console.log("get mesaj ");
    id = JSON.parse(message).message
    $.getJSON(`/sbs/message/api/v1/mesaj/${id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            drawMessage(data);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {

    $.post('/sbs/message/api/v1/mesaj/', {
        recipient: recipient,
        body: body
    }).fail(function () {

        alert('Error! Check console!');
    });
}

function setCurrentRecipient(username) {

    console.log("set curre");
    currentRecipient = username;
    getConversation(currentRecipient);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    console.log("disable input ");
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    updateUserList();
    disableInput();

    var q = document.URL.split('?')[1];
    console.log(q)
    if (q != null) {
        var username = q.split('=')[1]
        if (username != null) {

            setCurrentRecipient(username)
        }

    }





    console.log("gelecek ws");

    // // let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    // var socket = new WebSocket(
    //     'ws://' + window.location.host +
    //     '/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentRecipient, chatInput.val());
            chatInput.val('');
        }
    });

    // socket.onmessage = function (e) {
    //     console.log("onmessage");
    //     alert();
    //     getMessageById(e.data);
    // };
});


