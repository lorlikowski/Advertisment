import {session, ads, relation} from './session'


export function login(login: string, password: string) {
    return session.post("login", {email: login, password: password})
}

export function get_user(id: string) {
    return session.get("public_data/" + id, {});
}

export function advertisements(id: string) {
    return ads.get("users/"+ id + "/advertisements");
}

export function following(type: string, id: string) {
    return relation.get("following/" + type + "/" + id);
}