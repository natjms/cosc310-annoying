import { useState, useEffect } from 'preact/hooks'
import '@/app.css'

import { Router, Route } from 'preact-router'

import * as security from '@/utils/security'
import { SecurityContext, useSecurity } from '@/utils/security'
import type { SecurityReference } from '@/utils/security'

import RestaurantListPage from '@/pages/restaurant-list'
//import RestaurantPage from '@/pages/restaurant'
import UpdateRestaurantPage from '@/pages/update-restaurant'
import CreateRestaurantPage from '@/pages/create-restaurant'

//import AccountPage from '@/pages/account'
import CreateAccountPage from '@/pages/create-account'
import UpdateAccountPage from '@/pages/update-account'
//
//import MenuPage from '@/pages/menu'
import CreateMenuPage from '@/pages/create-menu'
import UpdateMenuPage from '@/pages/update-menu'
//
//import MenuItemPage from '@/pages/menu-item'
import CreateMenuItemPage from '@/pages/create-menu-item'
import UpdateMenuItemPage from '@/pages/update-menu-item'
//
//import CartPage from '@/pages/cart'
//import OrderListPage from '@/pages/order-list'
//import OrderPage from '@/pages/order'

import LogInPage from '@/pages/login'
import LogOutPage from '@/pages/logout'

import Navbar from '@/components/navbar'

export function App() {
    const security = useSecurity();
    /*
    const [security, setSecurity]: [SecurityReference, (s: SecurityReference) => void] = useState(null);

    const storage_change_handler = (e) => {
        console.info('here, storage updated');
        if (e.storageArea === localStorage) {
            if (e.key === security.LOCALSTORAGE_LOGOUT_FLAG && e.newValue === 'true') {
                localStorage.removeItem(security.LOCALSTORAGE_LOGOUT_FLAG);
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

    useEffect(() => {
        window.addEventListener('storage', storage_change_handler);
        return () => {
            window.removeEventListener('storage', storage_change_handler);
        };
    }, []);
    */

    return (
        <>
                <Navbar />
                <Router>
                    <Route path='/' component={HomePage} />
                    <Route path='/restaurants' component={RestaurantListPage} />
                    {/*<Route path='/_/:restaurant_id' component={RestaurantPage} />*/}
                    <Route path='/_/:restaurant_id/create-menu' component={CreateMenuPage} />
                    <Route path='/_/:restaurant_id/update' component={UpdateRestaurantPage} />
                    <Route path='/_/:restaurant_id/:menu_id/update' component={UpdateMenuPage} />
                    {/*<Route path='/_/:restaurant_id/:menu_id/create-menu-item' component={CreateMenuItemPage} />*/}
                    <Route path='/_/:restaurant_id/:menu_id/:menu_item_id/update' component={UpdateMenuItemPage} />


                    <Route path='/restaurants/create' component={CreateRestaurantPage} />
                    <Route path='/account/update' component={UpdateAccountPage} />

                    { security === null && [
                        <Route path='/login' component={LogInPage} />,
                        <Route path='/create-account' component={CreateAccountPage} />
                    ]}
                    { security !== null &&
                        <Route path='/logout' component={LogOutPage} />
                    }
                </Router>
        </>
    );
}

function HomePage() {
    const security = useSecurity();
    return <>
        <p>Hello, world!</p>
        { security &&
            <p> Welcome, {security.user.username} </p> }
    </>;
}
