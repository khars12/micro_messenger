document.getElementById('btn_delete_user').onclick = (event) => {
    event.preventDefault()
    document.getElementById('delete_user').value=true
    document.getElementById('settings_form').submit()
}