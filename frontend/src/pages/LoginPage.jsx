import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setToken, setLoading, setError } from '../userSlice'
import api from '../api'
import { TextField, Button, Box, Typography, Paper } from '@mui/material'
import Loader from '../components/Loader'
import ErrorMessage from '../components/ErrorMessage'
import { useNavigate, Link } from 'react-router-dom'

export default function LoginPage() {
  const dispatch = useDispatch()
  const loading = useSelector((state) => state.user.loading)
  const error = useSelector((state) => state.user.error)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    dispatch(setLoading(true))
    dispatch(setError(null))
    try {
      const res = await api.post('/login', { email, password })
      dispatch(setToken(res.data.token))
      navigate('/profile')
    } catch (err) {
      dispatch(setError(err.response?.data?.error || 'Error de autenticación'))
    } finally {
      dispatch(setLoading(false))
    }
  }

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
    >
      <Paper elevation={3} sx={{ p: 4, minWidth: 320 }}>
        <Typography variant="h5" mb={2}>
          Iniciar Sesión
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Correo electrónico"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            fullWidth
            margin="normal"
            required
          />
          <TextField
            label="Contraseña"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
            margin="normal"
            required
          />
          <ErrorMessage message={error} />
          <Box mt={2}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              disabled={loading}
            >
              {loading ? <Loader /> : 'Entrar'}
            </Button>
          </Box>
        </form>
        <Box mt={2} textAlign="center">
          <Typography variant="body2">
            ¿No tienes cuenta? <Link to="/register">Regístrate</Link>
          </Typography>
        </Box>
      </Paper>
    </Box>
  )
}
