import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import {
  setRecommendations,
  setLoading,
  setError,
} from '../recommendationsSlice'
import api from '../api'
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  Chip,
} from '@mui/material'
import Loader from '../components/Loader'
import ErrorMessage from '../components/ErrorMessage'

export default function RecommendationsPage() {
  const dispatch = useDispatch()
  const { items, loading, error } = useSelector(
    (state) => state.recommendations
  )

  useEffect(() => {
    const fetchRecommendations = async () => {
      dispatch(setLoading(true))
      dispatch(setError(null))
      try {
        const res = await api.get('/recommendations')
        dispatch(setRecommendations(res.data.recommendations))
      } catch (err) {
        dispatch(setError('No se pudieron cargar las recomendaciones.'))
      } finally {
        dispatch(setLoading(false))
      }
    }
    fetchRecommendations()
    // eslint-disable-next-line
  }, [])

  if (loading) return <Loader />
  if (error) return <ErrorMessage message={error} />

  return (
    <Box
      display="flex"
      justifyContent={{ xs: 'center', md: 'center' }}
      alignItems={{ xs: 'flex-start', md: 'center' }}
      minHeight="80vh"
      sx={{
        background: {
          xs: '#f5f5f5',
          sm: 'linear-gradient(135deg, #e3f2fd 0%, #fce4ec 100%)',
        },
        py: { xs: 2, md: 6 },
      }}
    >
      <Paper
        elevation={6}
        sx={{
          p: { xs: 2, sm: 4 },
          minWidth: { xs: '90vw', sm: 320 },
          width: { xs: '100%', sm: 500, md: 600 },
          maxWidth: { xs: '100vw', md: 700 },
          borderRadius: 4,
          boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.15)',
          mx: 'auto', // Center horizontally
        }}
      >
        <Typography
          variant="h4"
          mb={3}
          align="center"
          color="primary.main"
          fontWeight={700}
        >
          Recomendaciones
        </Typography>
        <List sx={{ width: '100%' }}>
          {items.length === 0 && (
            <Typography align="center" color="text.secondary" my={4}>
              No hay recomendaciones disponibles.
            </Typography>
          )}
          {items.map((rec) => (
            <ListItem
              key={rec.resource_id}
              divider
              sx={{
                flexDirection: 'column',
                alignItems: 'flex-start',
                bgcolor: 'background.paper',
                borderRadius: 2,
                mb: 2,
                boxShadow: '0 2px 8px 0 rgba(31, 38, 135, 0.08)',
                transition: 'box-shadow 0.2s',
                '&:hover': {
                  boxShadow: '0 4px 16px 0 rgba(31, 38, 135, 0.16)',
                  bgcolor: 'grey.50',
                },
              }}
            >
              <ListItemText
                primary={
                  <Typography
                    variant="h6"
                    color="secondary.main"
                    fontWeight={600}
                  >
                    {rec.name}
                  </Typography>
                }
                secondary={
                  <Box mt={1}>
                    <Typography variant="body2" color="text.secondary" mb={1}>
                      {rec.explanation_text}
                    </Typography>
                    <Box mt={1} display="flex" flexWrap="wrap" gap={1}>
                      <Chip
                        label={`Necesidad: ${rec.explanation.need.toFixed(2)}`}
                        color="success"
                        variant="outlined"
                        sx={{ fontWeight: 500 }}
                      />
                      <Chip
                        label={`Similitud: ${rec.explanation.text_similarity.toFixed(
                          2
                        )}`}
                        color="primary"
                        variant="outlined"
                        sx={{ fontWeight: 500 }}
                      />
                      <Chip
                        label={`Colaborativo: ${rec.explanation.score_collab.toFixed(
                          2
                        )}`}
                        color="secondary"
                        variant="outlined"
                        sx={{ fontWeight: 500 }}
                      />
                      <Chip
                        label={`Score: ${rec.score.toFixed(2)}`}
                        color="default"
                        variant="outlined"
                        sx={{ fontWeight: 500 }}
                      />
                    </Box>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  )
}
