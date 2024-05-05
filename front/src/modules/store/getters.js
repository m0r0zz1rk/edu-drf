const getters = {
  isAuthenticated: state => !!state.cokoToken,
  isAdministrator: state => state.cokoRole === 'centre',
  isDepartment: state => state.cokoRole === 'dep',
  isStudent: state => state.cokoRole === 'student',
  getAuthStatus: state => state.authStatus
}

export default getters
