import React, { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  Button,
  Radio,
  RadioGroup,
  FormControlLabel,
  LinearProgress,
  Fade,
} from '@mui/material'
import api from '../api'
import Loader from '../components/Loader'
import ErrorMessage from '../components/ErrorMessage'

// Ejemplo de preguntas, en producción esto vendría del backend
const sampleQuestions = [
  {
    id: 1,
    question: '¿Cuál es el resultado de 2 + 2?',
    options: ['2', '3', '4', '5'],
    answer: 2,
    topic_id: 1,
    level_id: 1,
  },
  {
    id: 2,
    question: '¿Qué es una ecuación lineal?',
    options: [
      'Una ecuación de segundo grado',
      'Una ecuación de primer grado',
      'Una ecuación con raíces cuadradas',
      'Ninguna de las anteriores',
    ],
    answer: 1,
    topic_id: 1,
    level_id: 1,
  },
  // ...más preguntas
]

export default function TestPage() {
  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState([])
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const current = sampleQuestions[step]
  const total = sampleQuestions.length

  const handleSelect = (e) => {
    const newAnswers = [...answers]
    newAnswers[step] = parseInt(e.target.value)
    setAnswers(newAnswers)
  }

  const handleNext = () => {
    if (step < total - 1) {
      setStep(step + 1)
    } else {
      handleSubmit()
    }
  }

  const handleSubmit = async () => {
    setSubmitting(true)
    setError(null)
    // Calcular score simple (en producción, lógica más avanzada)
    let score = 0
    sampleQuestions.forEach((q, i) => {
      if (answers[i] === q.answer) score += 1
    })
    score = score / total
    try {
      // Enviar resultado al backend
      const res = await api.post('/tests', {
        topic_id: current.topic_id,
        level_id: current.level_id,
        score,
      })
      setResult(res.data)
    } catch (err) {
      setError('No se pudo guardar el test.')
    } finally {
      setSubmitting(false)
    }
  }

  if (submitting) return <Loader />
  if (error) return <ErrorMessage message={error} />

  if (result) {
    return (
      <Fade in={true}>
        <Box
          display="flex"
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          minHeight="80vh"
        >
          <Paper
            elevation={4}
            sx={{ p: 4, minWidth: 320, maxWidth: 400, textAlign: 'center' }}
          >
            <Typography variant="h5" mb={2}>
              ¡Test completado!
            </Typography>
            <Typography variant="body1" mb={2}>
              Tu puntaje: <b>{(result.score * 100).toFixed(0)}%</b>
            </Typography>
            <Button variant="contained" color="primary" href="/recommendations">
              Ver recomendaciones
            </Button>
          </Paper>
        </Box>
      </Fade>
    )
  }

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="80vh"
    >
      <Paper elevation={4} sx={{ p: 4, minWidth: 320, maxWidth: 400 }}>
        <Typography variant="h6" mb={2} color="primary">
          Pregunta {step + 1} de {total}
        </Typography>
        <LinearProgress
          variant="determinate"
          value={((step + 1) / total) * 100}
          sx={{ mb: 3 }}
        />
        <Typography variant="body1" mb={2}>
          {current.question}
        </Typography>
        <RadioGroup value={answers[step] ?? ''} onChange={handleSelect}>
          {current.options.map((opt, idx) => (
            <FormControlLabel
              key={idx}
              value={idx}
              control={<Radio color="primary" />}
              label={opt}
            />
          ))}
        </RadioGroup>
        <Button
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 3 }}
          disabled={answers[step] === undefined}
          onClick={handleNext}
        >
          {step < total - 1 ? 'Siguiente' : 'Finalizar'}
        </Button>
      </Paper>
    </Box>
  )
}
