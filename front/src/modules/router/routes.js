import base_routes from "./routes/base_routes.js";
import centre_routes from "@/modules/router/routes/centre_routes";
import users_routes from "@/modules/router/routes/users_routes";
// import users_routes from "./routes/users_routes.js";

//const routes = base_routes.concat(centre_routes).concat(users_routes)
const routes = base_routes
  .concat(centre_routes)
  .concat(users_routes)

export default routes
