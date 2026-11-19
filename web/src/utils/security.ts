import { useContext, createContext } from 'react'

export const SecurityContext = createContext(null);

enum RoleName {
    ADMIN = 'admin',
    CUSTOMER = 'customer',
    RESTAURATEUR = 'restaurateur'
}

type SecurityReference = {
    user: User,
    token: string,
    roles: RoleName[]
};

export const LOCALSTORAGE_TOKEN_KEY = 'annoying-session-token';
export const LOCALSTORAGE_USER_KEY = 'annoying-user';
export const LOCALSTORAGE_ROLE_KEY = 'annoying-role';
export const LOCALSTORAGE_LOGOUT_FLAG = 'annoying-logout';
