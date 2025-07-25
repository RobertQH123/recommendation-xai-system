import { configureStore } from '@reduxjs/toolkit'
import userReducer from './userSlice'
import recommendationsReducer from './recommendationsSlice'

export const store = configureStore({
  reducer: {
    user: userReducer,
    recommendations: recommendationsReducer,
  },
})
