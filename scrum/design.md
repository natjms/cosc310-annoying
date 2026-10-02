# Design Document

## URL Design

- api/                Return a health status.  
    - restaurants/    Return all restaurants.  
    - restaurant/     INACCESSIBLE.  
        - create/  
        - ID/         Return a single restaurant.  
            - update/  
            - menus/  Return a list of restaurant menus.  
    - menu/           INACCESSIBLE.  
        - create/  
        - ID/         Return a single menu.  
            - update/  
    - dish/  
        - create/  
        - ID/  
            - update/  
