from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import (
    db,
    User,
    Resource,
    Interaction,
    Test,
    KnowledgeProfile,
    Topic,
    Level,
    RecommendationHistory,
)
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestRegressor
import shap

rec_bp = Blueprint("recommendation_bp", __name__)


@rec_bp.route("/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations():
    user_id = int(get_jwt_identity())

    # 1. Cargar recursos
    resources = Resource.query.all()
    recursos_df = pd.DataFrame(
        [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description or "",
                "topic_id": r.topic_id,
                "level_id": r.level_id,
            }
            for r in resources
        ]
    )
    recursos_df["text"] = recursos_df["name"] + " " + recursos_df["description"]

    # 2. Cargar interacciones
    interacciones = Interaction.query.with_entities(
        Interaction.user_id, Interaction.resource_id, Interaction.rating
    ).all()
    inter_df = pd.DataFrame(interacciones, columns=["user_id", "resource_id", "rating"])

    # 3. Perfil del usuario
    perfil = {}
    perfil_rows = KnowledgeProfile.query.filter_by(user_id=user_id).all()

    for row in perfil_rows:
        tema = Topic.query.get(row.topic_id).name
        nivel = Level.query.get(row.level_id).name
        perfil[(tema, nivel)] = float(row.mastery_level)

    # 4. TF-IDF + SVD
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(recursos_df["text"])
    svd = TruncatedSVD(n_components=10, random_state=42)
    tfidf_reduced = svd.fit_transform(tfidf_matrix)

    # 5. Score colaborativo (rating promedio)
    coll_mean = inter_df.groupby("resource_id")["rating"].mean()
    recursos_df["score_collab"] = recursos_df["id"].map(lambda x: coll_mean.get(x, 0))
    recursos_df["score_collab_norm"] = MinMaxScaler().fit_transform(
        recursos_df[["score_collab"]]
    )

    # 6. Necesidad (1 - dominio)
    def calc_need(row):
        topic_name = Topic.query.get(row.topic_id).name
        level_name = Level.query.get(row.level_id).name
        dom = perfil.get((topic_name, level_name), 0)
        return 1 - dom

    recursos_df["need"] = recursos_df.apply(calc_need, axis=1)
    recursos_df["need_norm"] = MinMaxScaler().fit_transform(recursos_df[["need"]])

    # 7. Similaridad de interés
    worst = sorted(perfil.items(), key=lambda x: x[1])[:2]
    temas_text = " y ".join([f"{tema} {nivel}".lower() for (tema, nivel), _ in worst])
    interes_vector = vectorizer.transform([f"Me interesa aprender {temas_text}"])
    sim_scores = (
        (interes_vector @ tfidf_matrix.T).toarray().flatten().astype(np.float32)
    )
    recursos_df["sim_norm"] = MinMaxScaler().fit_transform(sim_scores.reshape(-1, 1))

    # 8. Score híbrido
    alpha, beta = 0.5, 0.3
    recursos_df["score_hybrid"] = (1 - beta) * (
        alpha * recursos_df["sim_norm"] + (1 - alpha) * recursos_df["score_collab_norm"]
    ) + beta * recursos_df["need_norm"]

    # 9. Modelo explicable
    X_num = recursos_df[["score_collab_norm", "need_norm"]].values
    X = np.hstack((tfidf_reduced, X_num))
    y = recursos_df["score_hybrid"]
    model = RandomForestRegressor(random_state=42).fit(X, y)
    explainer = shap.Explainer(model, X)

    # 10. Top 5 recomendaciones
    top_recursos = (
        recursos_df.sort_values("score_hybrid", ascending=False).head(5).reset_index()
    )
    results = []

    for _, row in top_recursos.iterrows():
        idx = int(row["index"])
        shap_vals = explainer(X[idx : idx + 1])
        vals = shap_vals.values[0]
        explanations = {
            "text_similarity": float(vals[-3]),
            "score_collab": float(vals[-2]),
            "need": float(vals[-1]),
        }

        # Guardar historial de recomendación
        history = RecommendationHistory(
            user_id=user_id, resource_id=int(row["id"]), status="pending"
        )
        db.session.add(history)

        # 🔤 Generar explicación en texto

        # 1. Coincidencias de texto
        palabras_interes = [
            w for w in temas_text.split() if w in vectorizer.get_feature_names_out()
        ]
        coincidencias = [w for w in palabras_interes if w in row["text"].lower()]

        # 2. Dominio del usuario
        topic_name = Topic.query.get(row["topic_id"]).name
        level_name = Level.query.get(row["level_id"]).name
        dom = perfil.get((topic_name, level_name), 0)

        # 3. Calificación colaborativa
        calif = coll_mean.get(row["id"], 0)

        # # 4. Mensaje de explicación
        # explicacion_texto = f"Este recurso fue recomendado porque contiene los temas: {', '.join(coincidencias)} relacionados con tus intereses recientes. "
        # if dom < 0.5:
        #     explicacion_texto += f"Además, tu nivel de dominio en '{topic_name} - {level_name}' es bajo , por lo que necesitas reforzar ese tema. "
        # if calif > 0:
        #     explicacion_texto += (
        #         f"Otros usuarios lo calificaron con un promedio de {calif:.1f}/5."
        #     )

        # 4. Mensaje de explicación con SHAP
        total = sum(abs(v) for v in vals[-3:]) + 1e-8  # evitar división por cero
        impact_sim = abs(vals[-3]) / total * 100
        impact_collab = abs(vals[-2]) / total * 100
        impact_need = abs(vals[-1]) / total * 100

        # 1. Coincidencias de texto
        palabras_interes = [
            w for w in temas_text.split() if w in vectorizer.get_feature_names_out()
        ]
        coincidencias = [w for w in palabras_interes if w in row["text"].lower()]

        # 2. Dominio del usuario
        topic_name = Topic.query.get(row["topic_id"]).name
        level_name = Level.query.get(row["level_id"]).name
        dom = perfil.get((topic_name, level_name), 0)

        # 3. Calificación colaborativa
        calif = coll_mean.get(row["id"], 0)

        # 📘 Explicación basada en SHAP
        explicacion_texto = (
            f"Este recurso fue recomendado principalmente porque tu nivel de dominio en el tema "
            f"'{topic_name} - {level_name}' es bajo, lo que representó un impacto del {impact_need:.1f}% sobre la recomendación. "
        )

        if coincidencias:
            explicacion_texto += (
                f"Además, el contenido coincide con tus intereses recientes ('{', '.join(coincidencias)}'), "
                f"con un impacto del {impact_sim:.1f}%. "
            )
        else:
            explicacion_texto += f"El contenido también mostró cierta relación con tus intereses, aportando un {impact_sim:.1f}% a la recomendación. "

        if calif > 0:
            explicacion_texto += (
                f"Finalmente, otros estudiantes calificaron este recurso con un promedio de {calif:.1f}/5, "
                f"lo que aportó un {impact_collab:.1f}%."
            )

        # 📌 Añadir al resultado
        results.append(
            {
                "resource_id": int(row["id"]),
                "name": row["name"],
                "score": float(row["score_hybrid"]),
                "explanation": explanations,
                "explanation_text": explicacion_texto.strip(),
            }
        )
    db.session.commit()

    return jsonify(recommendations=results), 200
