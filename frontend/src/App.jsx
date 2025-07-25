import React from 'react'
import { Provider } from 'react-redux'
import { store } from './store'
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProfilePage from './pages/ProfilePage'
import RecommendationsPage from './pages/RecommendationsPage'
import TestPage from './pages/TestPage'
import ProtectedRoute from './components/ProtectedRoute'
import Navbar from './components/Navbar'
import { CssBaseline, ThemeProvider, createTheme } from '@mui/material'
import { useSelector } from 'react-redux'

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#1976d2' },
    secondary: { main: '#9c27b0' },
  },
})

function AppRoutes() {
  const token = useSelector((state) => state.user.token)
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        {token && <Navbar />}
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <ProfilePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/recommendations"
            element={
              <ProtectedRoute>
                <RecommendationsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/test"
            element={
              <ProtectedRoute>
                <TestPage />
              </ProtectedRoute>
            }
          />
          <Route path="/" element={<Navigate to="/profile" />} />
          <Route path="*" element={<Navigate to="/profile" />} />
        </Routes>
      </Router>
    </ThemeProvider>
  )
}

export default function App() {
  return (
    <Provider store={store}>
      <AppRoutes />
    </Provider>
  )
}
