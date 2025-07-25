import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  items: [],
  loading: false,
  error: null,
}

const recommendationsSlice = createSlice({
  name: 'recommendations',
  initialState,
  reducers: {
    setRecommendations(state, action) {
      state.items = action.payload
    },
    setLoading(state, action) {
      state.loading = action.payload
    },
    setError(state, action) {
      state.error = action.payload
    },
  },
})

export const { setRecommendations, setLoading, setError } =
  recommendationsSlice.actions
export default recommendationsSlice.reducer
