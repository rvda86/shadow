export function validateEmail(email) {
    return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
}

export function validatePassword(password) {
    return !(/^(.{0,7}|[^0-9]*|[^A-Za-z]*)$/.test(password))
}

export function validateUsername(username) {
    return (/^[A-Za-z][A-Za-z0-9_]{4,30}$/.test(username))
}