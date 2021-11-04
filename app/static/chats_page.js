const getChatsURL = window.location.href.split('/')[0] + '//' + window.location.href.split('/')[2] + '/api/get_chats'

const socket = io(window.location.href.split('/')[0] + '//' + window.location.href.split('/')[2])


function makeNewListElement(elementData) {
    let newElemNode = document.createElement("a")
    newElemNode.href = './chats/' + elementData['chat_id']
    newElemNode.classList.add('list-group-item', 'list-group-item-action')
    newElemNode.id = 'chat' + elementData['chat_id']
    
    let hasMsgCircleHTML
    if (elementData['has_new_msg']) {
        hasMsgCircleHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-circle-fill new-msg-circle" viewBox="0 0 18 18"><circle cx="8" cy="8" r="8"/></svg>'
    } 
    else {
        hasMsgCircleHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" class="bi bi-circle" viewBox="0 0 18 18"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/></svg>'
    } 
    
    newElemNode.innerHTML = `
        <div class="row">
            <div class="col-5 pe-0"><strong>${elementData["chat_name"]}</strong></div>
            <div class="col text-end ps-0">${elementData["date"]} | ${elementData["time"]}
            ${hasMsgCircleHTML}
        </div>`

    return newElemNode
}


function getChats() {
    const resultsList = document.getElementById("chats-list-group")
    if ((resultsList.scrollHeight - resultsList.scrollTop) < 2 * resultsList.clientHeight && !allResultsGot) {
        const messages_offset = document.querySelectorAll(".list-group-item").length - 1
        const xhr = new XMLHttpRequest()

        xhr.open('GET', getChatsURL + '?offset=' + messages_offset)
        xhr.responseType = 'json'
        xhr.onload = function() {
            xhr.response.forEach((elementData) => document.getElementById("chats-list-group").appendChild(makeNewListElement(elementData)))
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


document.getElementById("chats-list-group").onscroll = function() {
    if (!scrollCallbackIsWorking) {
        scrollCallbackIsWorking = true
        getChats()
    }
}


socket.on('connect', () => {
    socket.emit('listen_all_chats')
})


socket.on('message', (data) => {
    hi = document.getElementById("chat" + data['chat_id'])
    console.log(hi)
    document.getElementById("chat" + data['chat_id']).remove()
    document.querySelectorAll(".list-group-item")[0].after(makeNewListElement(data))
})


var scrollCallbackIsWorking = false
var allResultsGot = false
getChats()