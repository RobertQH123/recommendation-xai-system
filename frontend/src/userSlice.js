import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  token: localStorage.getItem('token') || null,
  user: null,
  loading: false,
  error: null,
}

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setToken(state, action) {
      state.token = action.payload
      localStorage.setItem('token', action.payload)
    },
    setUser(state, action) {
      state.user = action.payload
    },
    setLoading(state, action) {
      state.loading = action.payload
    },
    setError(state, action) {
      state.error = action.payload
    },
    logout(state) {
      state.token = null
      state.user = null
      localStorage.removeItem('token')
    },
  },
})

export const { setToken, setUser, setLoading, setError, logout } =
  userSlice.actions
export default userSlice.reducer
