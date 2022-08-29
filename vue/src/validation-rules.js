export function validateEmail(email) {
    return (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
}

export function validatePassword(password) {
    return (/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,100}$/.test(password))
}

export function validateUsername(username) {
    return (/^[A-Za-z][A-Za-z0-9_]{4,30}$/.test(username))
}