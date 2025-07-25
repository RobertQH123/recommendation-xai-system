import React from 'react'
import { CircularProgress, Box } from '@mui/material'

export default function Loader() {
  return (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="200px"
    >
      <CircularProgress />
    </Box>
  )
}
