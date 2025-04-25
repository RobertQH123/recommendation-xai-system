CREATE TABLE estudiantes (
    estudiante_id SERIAL PRIMARY KEY,  -- ID único para cada estudiante
    nombre VARCHAR(100),
    correo VARCHAR(100),
    nivel_academico INT,  -- Un número que indique el nivel académico del estudiante
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_actividad TIMESTAMP  -- Fecha de la última interacción con el sistema
);


CREATE TABLE recursos (
    recurso_id SERIAL PRIMARY KEY,  -- ID único para cada recurso
    nombre VARCHAR(200),
    descripcion TEXT,  -- Descripción breve del recurso
    tipo_recurso VARCHAR(50),  -- Tipo de recurso (ejercicio, video, artículo, etc.)
    dificultad INT,  -- Dificultad del recurso, por ejemplo, 1 para fácil, 5 para difícil
    tema VARCHAR(100),  -- Tema relacionado con el recurso (por ejemplo, álgebra, geometría)
    url_recurso TEXT,  -- URL para acceder al recurso (si aplica)
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE interacciones (
    interaccion_id SERIAL PRIMARY KEY,
    estudiante_id INT REFERENCES estudiantes(estudiante_id),  -- ID del estudiante
    recurso_id INT REFERENCES recursos(recurso_id),  -- ID del recurso utilizado
    tiempo_invertido INT,  -- Tiempo que el estudiante pasó en el recurso (en minutos)
    puntuacion INT,  -- Puntuación obtenida (si aplica)
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recomendaciones (
    recomendacion_id SERIAL PRIMARY KEY,
    estudiante_id INT REFERENCES estudiantes(estudiante_id),
    recurso_id INT REFERENCES recursos(recurso_id),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    explicacion TEXT  -- Explicación generada por el LLM sobre por qué se recomienda el recurso
);

CREATE TABLE feedback (
    feedback_id SERIAL PRIMARY KEY,
    estudiante_id INT REFERENCES estudiantes(estudiante_id),
    recomendacion_id INT REFERENCES recomendaciones(recomendacion_id),
    puntuacion INT,  -- Valoración del estudiante sobre la recomendación
    comentario TEXT,  -- Comentarios del estudiante sobre la recomendación
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
