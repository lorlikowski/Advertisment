import { BareActionContext } from "vuex-typex"
import { storeBuilder, RootState } from "@/store/RootState"
import * as auth_api from '@/api/auth'
import { session } from "@/api/session"


const TOKEN_STORAGE_KEY = "NOTE"

export class AuthState {
    authenticated = false
    error = false
    firstLogin = true
    user: string | null = null
}

const b = storeBuilder.module<AuthState>("auth", new AuthState())


function isAuthenticated(state: AuthState) {
    return state.authenticated;
}

function authUser(state: AuthState) {
    return state.user;
}

export const getters = {
    authUser: b.read(authUser),
    isAuthenticated: b.read(isAuthenticated)
}


function LoginStart(state: AuthState) {
    state.authenticated = false;
    state.error = false;
    state.user = null;
}

function LoginSuccess(state: AuthState, id: string) {
    localStorage.setItem('lo', "1");
    state.user = id;
    state.authenticated = true;
    state.error = false;
}

function LoginError(state: AuthState) {
    state.authenticated = false;
    state.error = true;
    state.user = null;
}

function Logout(state: AuthState) {
    state.authenticated = false;
    state.error = false;
    state.user = null;
}

function setBase(state: AuthState) {
    if (localStorage.getItem('lo')) {
        state.firstLogin = false;
    }
}

export const mutations = {
  setBase: b.commit(setBase),
  Logout: b.commit(Logout),
  LoginError: b.commit(LoginError),
  LoginSuccess: b.commit(LoginSuccess),
  LoginStart: b.commit(LoginStart),
}

// actions

type ActionContext = BareActionContext<AuthState, RootState>

async function login(context: ActionContext, payload: { username: string; password: string }) {
    mutations.LoginStart();
    const {username, password} = payload;
    try {
    const response = await auth_api.login(username, password);
    localStorage.setItem(TOKEN_STORAGE_KEY, response.data.key);
    session.defaults.headers.common['Authorization'] = 'Bearer ' + response.data.key;
    mutations.LoginSuccess(response.data.id);
    }
    catch(error) {
        mutations.LoginError();
        return false;
    }
    return true;        
}

async function logout(context: ActionContext) {
    mutations.Logout();
}




interface data {
    email: string
    password: string
    password1: string
}

async function register(context: ActionContext,  data: data) {
    try {
        if (data.password != data.password1)
            return false;
        const response = await auth_api.register(data);
        return response.status == 200;
    }
    catch(error) {
        console.log(error);
        return false;
    }
}

interface changeData {
    password: string,
    password1: string
}

async function change(context: ActionContext, changeData: changeData) {
    try {
        const user = getters.authUser();
        if (user != null) {
            const publicData = await auth_api.get_user(user);
            const response = await auth_api.change(publicData.data, changeData);
            return response.status == 200;
        }
        else {
            return false;
        }
    }
    catch(error) {
        console.log(error);
        return false;
    }
}


export const actions = {
  login: b.dispatch(login),
  logout: b.dispatch(logout),
  register: b.dispatch(register),
  change: b.dispatch(change)
}