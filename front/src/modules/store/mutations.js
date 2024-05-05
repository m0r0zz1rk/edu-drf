const mutations = {
  AUTH_REQUEST (state) {
    state.authStatus = 'loading'
  },
  AUTH_SUCCESS (state, token, role) {
    state.authStatus = 'success'
    state.cokoToken = token
    state.cokoRole = role
  },
  AUTH_LOGOUT (state) {
    state.cokoToken = ''
  },
  AUTH_ERROR (state) {
    state.authStatus = 'error'
  },
}

export default mutations
