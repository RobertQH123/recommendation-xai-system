import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setUser, setLoading, setError, logout } from '../userSlice'
import api from '../api'
import { Box, Typography, Button, Paper } from '@mui/material'
import Loader from '../components/Loader'
import ErrorMessage from '../components/ErrorMessage'
import { useNavigate } from 'react-router-dom'

export default function ProfilePage() {
  const dispatch = useDispatch()
  const { user, loading, error } = useSelector((state) => state.user)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchUser = async () => {
      dispatch(setLoading(true))
      dispatch(setError(null))
      try {
        const res = await api.get('/me')
        dispatch(setUser(res.data))
      } catch (err) {
        dispatch(setError('No autenticado.'))
        dispatch(logout())
        navigate('/login')
      } finally {
        dispatch(setLoading(false))
      }
    }
    fetchUser()
    // eslint-disable-next-line
  }, [])

  if (loading) return <Loader />
  if (error) return <ErrorMessage message={error} />
  if (!user) return null

  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
    >
      <Paper elevation={3} sx={{ p: 4, minWidth: 320 }}>
        <Typography variant="h5" mb={2}>
          Perfil de Usuario
        </Typography>
        <Typography>
          <b>Nombre:</b> {user.name}
        </Typography>
        <Typography>
          <b>Email:</b> {user.email}
        </Typography>
        <Typography>
          <b>Registrado:</b> {new Date(user.registration_date).toLocaleString()}
        </Typography>
        <Box mt={2}>
          <Button
            variant="contained"
            color="secondary"
            onClick={() => {
              dispatch(logout())
              navigate('/login')
            }}
          >
            Cerrar sesión
          </Button>
        </Box>
      </Paper>
    </Box>
  )
}
