# flask-graphene-sqlalchemy-react-starter

simple flask setup to serve a react app

This is a work in progress, it is certainly not production ready but I am hoping to be working on this regularly.

# Getting Started

* check out the package.json in static for more handy scripts but these will get you started
* `npm run docker-build` will get the app built and served on localhost:3000
* `npm run start` will start up the app without a build
* `npm run docker-down` this takes all volumes down and removes them, this is handy if you are seeing any weirdness that isn't solved just from rebuilding
* `npm run docker-newdep-js` this runs the docker-down script and then runs a docker-build, I run this everytime I add a new dependency to make sure everything is synced

# Additional Notes

* please don't hesitate to open an issue, I am learning more every day and I'm sure there are some rookie mistakes. I would be glad to have as much constructive criticism as you have time to give.

Thanks and happy hacking!
