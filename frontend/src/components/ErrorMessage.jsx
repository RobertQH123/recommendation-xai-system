import React from 'react'
import { Alert, Box } from '@mui/material'

export default function ErrorMessage({ message }) {
  if (!message) return null
  return (
    <Box my={2}>
      <Alert severity="error">{message}</Alert>
    </Box>
  )
}
