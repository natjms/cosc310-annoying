import { useState, useEffect } from 'preact/hooks'
import '@/app.css'

import { Router, Route } from 'preact-router'

import * as security from '@/utils/security'
import { SecurityContext } from '@/utils/security'
import type { SecurityReference } from '@/utils/security'

import RestaurantListPage from '@/pages/restaurant-list'
import RestaurantPage from '@/pages/restaurant'
import CreateAccountPage from '@/pages/create-account'
import AccountPage from '@/pages/account'
import LogInPage from '@/pages/login'
import LogOutPage from '@/pages/logout'

import Navbar from '@/components/navbar'

export function App() {
    const [security, setSecurity]: [SecurityReference, (s: SecurityReference) => void] = useState(null);

    const storage_change_handler = (e) => {
        if (e.storageArea === localStorage) {
            if (e.key === security.LOCALSTORAGE_LOGOUT_FLAG && e.newValue === 'true') {
                localStorage.removeItem(security.LOCALSTORAGE_USER_FLAG);
                localStorage.removeItem(security.LOCALSTORAGE_TOKEN_KEY);
                localStorage.removeItem(security.LOCALSTORAGE_USER_KEY);
                localStorage.removeItem(security.LOCALSTORAGE_ROLES_KEY);
            }

            if (e.key === security.LOCALSTORAGE_LOGIN_FLAG && e.newValue === 'true') {
                localStorage.removeItem(security.LOCALSTORAGE_LOGIN_FLAG);
                setSecurity({
                    user: JSON.parse(localStorage.getItem(security.LOCALSTORAGE_USER_KEY)),
                    token: localStorage.getItem(security.LOCALSTORAGE_TOKEN_KEY),
                    roles: JSON.parse(localStorage.getItem(security.LOCALSTORAGE_ROLES_KEY)),
                })
            }
        }
    };
    window.addEventListener('storage', storage_change_handler);
    useEffect(() => {
        return () => {
            window.removeEventListener('storage', storage_change_handler);
        };
    }, []);

    return (
        <>
            <SecurityContext value={security}>
                <Navbar />
                <Router>
                    <Route path='/' component={HomePage} />
                    <Route path='/restaurants' component={RestaurantListPage} />
                    <Route path='/_/:restaurant_id' component={RestaurantPage} />
                    { security === null && [
                        <Route path='/login' component={LogInPage} />,
                        <Route path='/create-account' component={CreateAccountPage} />
                    ]}
                    { security !== null && [
                        <Route path='/logout' component={LogOutPage} />,
                        <Route path='/account' component={AccountPage} />,
                    ]}
                </Router>
            </SecurityContext>
        </>
    );
}

function HomePage() {
    return <>
        <p>Hello, world!</p>
    </>;
}
