import session from './session'

export function login(login: string, password: string) {
    return session.post("login", {email: login, password: password})
}