date: 20 nov
location: art xxx
members present: nat christopher sarthak
members absent: lua
agenda

description:
nat's working on frontend
filling out the milestone - around 11am
refer to last notes for ttd (things to do)
sarthak's working on the routers for orders

nts: reconcile this and the last one 
talk about the carts depending on menu thing
talk about the ulid issue

description:
nat's working on frontend
filling out the milestone - around 11am
refer to last notes for ttd (things to do)
sarthak's working on the routers for orders

discussion about the get_active_cart function: does it rely upon
# tentative: we're going to rely upon the session variable

discussion about the frontend and what library to use (preact)
check-in: what's the state of the auth and user backend

session date: nov19
primary agenda: milestone2 sprint

members present: nat and sarthak and christopher (later)
members absent: lua
location: around eme 2257

## today order of operations:
both -> {
    review prs (below)
}

i -> {
    work on order and cart
    scrum-notes.md + provenance.md + update readme.md
    linting (figure out what's next)
}

nat -> {
    user routes before and frontend after
}

christopher = {
    documenting the routes
    style guide
}

# tomorrow:
document types of roles
document what the error types even are
document why ulid
document the session length and such
flow diagram for the route - repo layer stuff
update docstrings
create markdown todo lists
create gantt possibly idk
create scrum diagrams (dfd or whatever)
create implementation decision flowcharts
commit representative data - DONE
-> also look into the envfile thing i talked about on signal
update codestyle
create pr-title-style
create submission pdf
add assignees
add menu tests

document what's in the representative data
document my changes further
document json lines for the repo layer
document write-ahead-log concerns

close prs:
166 - rename menu item DONE
165 - rename menu DONE
163 - rename restaurant routes DONE
173 - in memory repos in tests DONE
172 - user and session for auth DONE
169 - role based authorization DONE

118 - post post milestone cleanup
124 - representative data
128 - full-text search by lua : CLOSED
^ maybe this can be done for now with a simple substring search


orders by a restaurant by a restaurant id parameter so the restauarnts can see what orders are coming in for their restaurant

verify if the person making that request is a restauranter + they own the restaraunt they wanna see the orders for

carts for the design.md

#181 make an issue for this pr
Now
