import {session, ads, relation} from './session'

interface data {
    email: string;
    password: string;
    password1: string;
}

interface changeData {
    password: string,
    password1: string
}


interface publicData {
    email: string,
    is_admin: boolean
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

export function get_advertisement_content(id: number) {
    return ads.get(`/advertisements/${id}/content`);
}

export function update_advertisement_views(id: number) {
    return ads.post(`/advertisements/${id}/update_views`);
}

export function get_popular_advertisements_in_category(category: string, page: number, perPage: number) {
    return ads.get(`/categories/${category}/advertisements/popular/?limit=${perPage}&skip=${(page-1)*perPage}`)
}

export function get_categories(){
    return ads.get('/categories');
}

export function register(data: data) {
    return session.post("/register", {"email": data.email, "password": data.password, "is_admin": false})
}

export function change(publicData: publicData,  data: changeData) {
    return session.post("/change_data", {"email": publicData.email, "password": data.password, "password1": data.password1, "is_admin": publicData.is_admin})
}