import {session, ads, relation} from './session'

interface data {
    email: string;
    password: string;
    password1: string;
}


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

export function get_advertisement(id: number) {
    return ads.get("/advertisements/" + id.toString());
}

export function register(data: data) {
    return session.post("/register", {"email": data.email, "password": data.password, "is_admin": false})
}