import React from 'react'
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material'
import { Link, useNavigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { logout } from '../userSlice'

export default function Navbar() {
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  return (
    <AppBar position="static" color="primary">
      <Toolbar>
        <Typography
          variant="h6"
          component={Link}
          to="/profile"
          sx={{ flexGrow: 1, color: 'inherit', textDecoration: 'none' }}
        >
          Recommendation XAI
        </Typography>
        <Box>
          <Button color="inherit" component={Link} to="/profile">
            Perfil
          </Button>
          <Button color="inherit" component={Link} to="/recommendations">
            Recomendaciones
          </Button>
          <Button color="inherit" component={Link} to="/test">
            Test
          </Button>
          <Button color="inherit" onClick={handleLogout}>
            Cerrar sesión
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  )
}
