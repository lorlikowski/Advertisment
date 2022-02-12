import axios from "axios";

//export default axios;

const session = axios.create({
    headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
    },
    baseURL: 'http://localhost:8002',
    timeout: 15000
})

const ads = axios.create({
    headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
    },
    baseURL: 'http://localhost:8001',
    timeout: 15000
})

const relation = axios.create({
    headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
    },
    baseURL: 'http://localhost:8003',
    timeout: 15000
})

export {
    session,
    ads,
    relation
}