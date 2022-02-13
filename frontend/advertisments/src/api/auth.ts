import session from './session'

import {AdvertisementFillableData} from '@/store/types/advertisement'

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
    return session.get("users/"+ id + "/advertisements");
}

export function my_advertisements() {
    return session.get("users/me/advertisements/");
    
}

export function following(type: string, id: string) {
    return session.get("following/" + type + "/" + id);
}

export function get_advertisement(id: number) {
    return session.get(`/advertisements/${id}/`);
}

export function get_advertisement_content(id: number) {
    return session.get(`/advertisements/${id}/content`);
}

export function update_advertisement_views(id: number) {
    return session.post(`/advertisements/${id}/update_views`);
}

export function get_popular_advertisements_in_category(category: string, page: number, perPage: number) {
    return session.get(`/categories/${category}/advertisements/popular/?limit=${perPage}&skip=${(page-1)*perPage}`)
}

export function get_advertisements_in_category(category: string, page: number, perPage: number) {
    return session.get(`/categories/${category}/advertisements/?limit=${perPage}&skip=${(page-1)*perPage}`)
}

export function get_popular_advertisements(page: number, perPage: number) {
    return session.get(`/advertisements/popular/?limit=${perPage}&skip=${(page-1)*perPage}`)
}

export function get_categories(){
    return session.get('/categories');
}

export function register(data: data) {
    return session.post("/register", {"email": data.email, "password": data.password, "is_admin": false})
}

export function change(publicData: publicData,  data: changeData) {
    return session.post("/change_data", {"email": publicData.email, "password": data.password, "password1": data.password1, "is_admin": publicData.is_admin})
}

export function createAdvertisement(advertisement: AdvertisementFillableData) {
    return session.post("/users/me/advertisements/", advertisement);
}

export function updateAdvertisement(advertisement_id: number, advertisement: AdvertisementFillableData) {
    return session.put(`/advertisements/${advertisement_id}/`, advertisement);
}