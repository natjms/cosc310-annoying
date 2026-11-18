import { useState } from 'preact/hooks'
import '@/app.css'

import { NatsFriendlyRouter, Route } from '@/utils/nats-friendly-router'

import RestaurantListPage from '@/pages/restaurant-list-page'

export function App() {
  return (
    <>
        <NatsFriendlyRouter>
            <Route path='/' component={<HomePage />} />
            <Route path='/restaurants' component={<RestaurantListPage />} />
        </NatsFriendlyRouter>
    </>
  )
}

function HomePage() {
    return (
        <p>Hello, world!</p>
    );
}
