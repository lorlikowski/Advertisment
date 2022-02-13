import axios from "axios";

//export default axios;

const session = axios.create({
    headers: {
        "Accept": "application/json",
        "Content-Type": "application/json",
    },
    baseURL: 'http://localhost:8012',
    timeout: 15000
})

export default session;