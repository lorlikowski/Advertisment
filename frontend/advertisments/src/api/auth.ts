import session from './session'

import {AdvertisementFillableData, AdvertisementSearch} from '@/store/types/advertisement'

const DEFAULT_TIMEOUT = 30;

function getFromCache(key: string, timeout_s: number) {
    const cache = localStorage.getItem(`cache_${key}`);
    if (cache == null) {
        return null;
    }
    if (Date.now() - Number(cache) > timeout_s * 1000) {
        localStorage.removeItem(`cache_${key}`);
        localStorage.removeItem(key);
        return null;
    }
    return localStorage.getItem(key);
}

function setInCache(key: string, value: string) {
    localStorage.setItem(`cache_${key}`, Date.now().toString());
    localStorage.setItem(key, value);
}
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

export async function following(type: string, id: string) {
    const response = await session.get("following/" + type + "/" + id);
    return response.data.map(el => el.object_id);
}

export async function following_cached(type: string, id: string) {
    const data = getFromCache(`following_${type}_${id}`, DEFAULT_TIMEOUT);
    let follows: Array<any> = [];
    if (data != null) {
        follows = JSON.parse(data);
    }
    else {
        follows = await following(type, id);
        setInCache(`following_${type}_${id}`, JSON.stringify(follows));
    }
    const local_data = getFromCache(`following_${type}_local_${id}`, DEFAULT_TIMEOUT);

    if (local_data != null) {
        const local_follows = JSON.parse(local_data)

        for (const el of local_follows) {
            if (follows.indexOf(el) == -1) {
                follows.push(el);
            }
        }
    }
    
    return follows;
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
    return session.get('/categories/');
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

export function searchAdvertisements(form: AdvertisementSearch) {
    const obj = {};
    for (const key in form) {
        if (form[key] != null) {
            obj[key] = form[key].toString();
        }
    }
    const searchParams = new URLSearchParams(obj);
    return session.get(`/advertisements/?${searchParams}`)
}

export async function follow_user(authUser: string, follow: string) {
    const response = await session.post("/add", {"object_id": follow, "user_id": authUser, "type": "user"});
    if (response.status == 200) {
        const s = getFromCache(`following_user_local_${authUser}`, DEFAULT_TIMEOUT) ;
        let data:Array<any> = [];
        if (s != null) {
            data = JSON.parse(s);
        }
        data.push(follow);
        setInCache(`following_user_local_${authUser}`, JSON.stringify(data));
    }
    return response;
}

export async function follow_advertisement(authUser: string, follow: string) {
    const response = await session.post("/add", {"object_id": follow, "user_id": authUser, "type": "advertisement"});
    if (response.status == 200) {
        const s = getFromCache(`following_advertisement_local_${authUser}`, DEFAULT_TIMEOUT) ;
        let data:Array<any> = [];
        if (s != null) {
            data = JSON.parse(s);
        }
        data.push(follow);
        setInCache(`following_advertisement_local_${authUser}`, JSON.stringify(data));
    }
    return response;
}