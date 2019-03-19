function showHidden() {
    let btnsHidden = document.getElementById('hide-btns');
    let chBoxs = document.getElementsByClassName("email-box");

    for (let i = 0; i < chBoxs.length; i++) {
        if (chBoxs[i].checked === true) {
            btnsHidden.style.visibility = 'visible';
            break;
        } else {
            btnsHidden.style.visibility = 'hidden';
        }
    }
}

function showMessage() {
    window.open('show_message.html', '_self');
}

function compose() {
    window.open('compose.html', '_self');
}

function createGroup() {
    open('admin_adds_member.html', '_self');
}

function validateForm() {
    let myForm = document.formLogin;

    if (myForm.formemail.value == "admin@eric.com") {
        if (myForm.formpassword.value == "admin") {
            return true;
        } else {
            alert("Password Incorrect. Please try again")
            return false;
        }
    } else {
        open('email_box.html', '_self');
        return false;
    }
}

function openInbox() {
    open('email_box.html', '_self');
}