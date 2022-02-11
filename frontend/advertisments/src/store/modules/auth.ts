import { BareActionContext } from "vuex-typex"
import { storeBuilder, RootState } from "@/store/RootState"
import * as auth_api from '@/api/auth'


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
}

function LoginSuccess(state: AuthState) {
    localStorage.setItem('lo', "1");
    state.authenticated = true;
    state.error = false;
}

function LoginError(state: AuthState) {
    state.authenticated = false;
    state.error = true;
}

function Logout(state: AuthState) {
    state.authenticated = false;
    state.error = false;
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
    }
    catch(error) {
        mutations.LoginError();
        return false;
    }
    mutations.LoginSuccess();
    return true;        
}

async function logout(context: ActionContext) {
    mutations.Logout();
}

/** TODO change data*/

/**
 * 
 * @param {string} data.username
 * @param {string} data.email
 * @param {string} data.password
 * @param {string} data.first_name
 * @param {string} data.last_name
 * @param {number} data.graduation_year
 */
/** TODO 
register({commit}, data) {
    return auth_api.register(data);
}*/
async function initialize(context: ActionContext) {
    mutations.setBase();
    const token = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token) {
        mutations.LoginSuccess();
        return true;
    }
    return false;
}

export const actions = {
  login: b.dispatch(login),
  logout: b.dispatch(logout),
  initialize: b.dispatch(initialize)
}