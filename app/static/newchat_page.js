const usersearchURL = 'http://localhost:5000/api/usersearch'


/**
 * 
 * @param {[{id: id1, nickname: nickname1}, ...]} requestJSON 
 */

function addToUsersList(requestJSON) {
    requestJSON.forEach(function(elem) {
        let newElemNode = document.createElement("a")
        newElemNode.href = './chats/' + elem['id']
        newElemNode.classList.add('list-group-item', 'list-group-item-action')
        newElemNode.innerHTML = '<strong>' + elem['nickname'] + '</strong>'
        document.getElementById("results-list-group").appendChild(newElemNode)
    })
}


function getResults() {
    const resultsList = document.getElementById("results-list-group")
    if ((resultsList.scrollHeight - resultsList.scrollTop) < 2 * resultsList.clientHeight && !allResultsGot) {
        let results_offset = document.querySelectorAll(".list-group-item").length
        const xhr = new XMLHttpRequest()

        xhr.open('GET', usersearchURL + '?query=' + document.getElementById("query").value.trim() + '&offset=' + results_offset)
        xhr.responseType = 'json'
        xhr.onload = function() {
            addToUsersList(xhr.response)
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


document.getElementById("query").oninput = function() {
    allResultsGot = false
    document.getElementById("results-list-group").innerHTML = ''

    getResults()
}


document.getElementById("results-list-group").onscroll = function() {
    if (!scrollCallbackIsWorking) {
        scrollCallbackIsWorking = true
        getResults()
    }
}



var scrollCallbackIsWorking = false
var allResultsGot = false
getResults()