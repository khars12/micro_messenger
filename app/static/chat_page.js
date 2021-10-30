const getMessagesURL = 'https://' + window.location.href.split('/')[2] + '/api/get_messages'
const chatID = window.location.href.split('/')[4]
var currentUserID

const socket = io('https://' + window.location.href.split('/')[2])


function addToMessagesList(requestJSON) {
    requestJSON.forEach(function(elem) {
        let newElemNode = document.createElement("div")
        if (elem['is_received']) {
            newElemNode.classList.add('list-group-item', 'msg-received')
            newElemNode.innerHTML = elem['text']
        }
        else {
            newElemNode.classList.add('list-group-item', 'msg-sent')
            newElemNode.innerHTML = '<div class="d-inline-block float-end">' + elem['text'] + '</div>'
        }
        list = document.querySelectorAll(".list-group-item")
        if (list.length) {
            list[0].before(newElemNode)
        }
        else {
            document.getElementById("msgs-list-group").appendChild(newElemNode)
        }
    })
}


function getMessages() {
    const resultsList = document.getElementById("msgs-list-group")
    if ((resultsList.scrollHeight - resultsList.scrollTop) < 2 * resultsList.clientHeight && !allResultsGot) {
        const messages_offset = document.querySelectorAll(".list-group-item").length
        const xhr = new XMLHttpRequest()

        xhr.open('GET', getMessagesURL + '?chat_id=' + chatID + '&offset=' + messages_offset)
        xhr.responseType = 'json'
        xhr.onload = function() {
            addToMessagesList(xhr.response)
            if (xhr.response.length === 0) {
                allResultsGot = true
            }
            scrollCallbackIsWorking = false
        }
        xhr.send()
    }
    else {
        scrollCallbackIsWorking = false
    }
}


document.getElementById("msgs-list-group").onscroll = function() {
    if (!scrollCallbackIsWorking) {
        scrollCallbackIsWorking = true
        getMessages()
    }
}


document.getElementById("chat-sendbtn").onclick = (event) => {
    event.preventDefault()
    if (document.getElementById("chat-input").value != '') {
        socket.send({chat_id: chatID, text: document.getElementById("chat-input").value.trim()})
        document.getElementById("chat-input").value = ''
    }
    document.getElementById("chat-input").focus()
}


socket.on('connect', () => {
    socket.emit('join', {chat_id: chatID})
})


socket.on('current_user_id', (data) => {
    console.log(1)
    currentUserID = data['current_user_id']
})


socket.on('message', (data) => {
    if (data['sender_id'] == currentUserID) {
        addToMessagesList([{is_received: false, text: data['text']}])
    }
    else {
        addToMessagesList([{is_received: true, text: data['text']}])
    }
})


var scrollCallbackIsWorking = false
var allResultsGot = false
getMessages()