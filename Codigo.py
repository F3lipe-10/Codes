#Hola
import streamlit as st
from scipy.optimize import fsolve
import numpy as np

st.set_page_config(page_title="Calculadora reposicionamiento", layout="wide")

with st.container():
    st.title("Calculadora de Reposicionamientos")
    st.write("Bienvenido(a)! Con esta calculadora podrá saber la frecuencia de reposicionamientos de paciente en una unidad de cuidados intensivos, a continuación se solicitarán datos del paciente, con los cuales se calculará la frecuencia. Además se le solicitará que haga la valoración de la escala de Braden para el calculo completo. ¡Adelante!")
st.markdown("---")

edad = st.number_input("Escriba la edad del paciente")
IMC = st.number_input("Escriba el IMC del paciente")
braden_valores = []
ECV1 = st.selectbox("Si el paciente presenta ECV, escogja 1, de lo contrario, escoja 0", options=(0.0,1.0))
btn2 = st.button("Guardar datos")

def clicked():
    braden_valores.append(braden)
    braden_valores.append(braden2)
    braden_valores.append(braden3)
    braden_valores.append(braden4)
    braden_valores.append(braden5)
    braden_valores.append(braden6)
    riesgos(edad, IMC, braden_valores,ECV1)
    promedionoches_solucion = riesgos(edad, IMC, braden_valores,ECV1)
    st.subheader(f"Por noche, el paciente debe ser reposicionado: {promedionoches_solucion} veces")
    st.markdown("---")            


st.markdown("---")


with st.container():
    datos1, datos2 = st.columns(2)
    with datos1:
        braden = st.selectbox("Valore de 1 a 4 el riesgo Percepción Sensorial", options=(1, 2, 3, 4))
        braden2 = st.selectbox("Valore de 1 a 4 el riesgo Exposición a la humedad", options=(1, 2, 3, 4))
        braden3 = st.selectbox("Valore de 1 a 4 el riesgo Actividad", options=(1, 2, 3, 4))
        braden4 = st.selectbox("Valore de 1 a 4 el riesgo Movilidad", options=(1, 2, 3, 4))
        braden5 = st.selectbox("Valore de 1 a 4 el riesgo Nutrición", options=(1, 2, 3, 4))
        braden6 = st.selectbox("Valore de 1 a 3 el riesgo Problemas en la piel", options=(1, 2, 3))
    with datos2: 
        st.image("Escala-de-Braden.jpg", caption=("Imagen tomada de https://enfermeriacreativa.com/2019/01/28/escala-de-braden/"))

def riesgos(edad, IMC, braden_valores,ECV1):

    suma1 = sum(braden_valores)
    if suma1 < 12:
        riesgo_braden = "Alto"
    elif suma1 >= 12 and suma1 < 14:
        riesgo_braden = "Medio"
    elif suma1 >= 14 and suma1 <= 23:
        riesgo_braden = "Bajo"
    #calculo
    intercept = -1.802
    coef_promedionoches = -0.479
    coef_edad = 0.04
    coef_ecv = 1.401
    coef_braden_malta = 0.525
    coef_obesidad = 3.751

    if IMC > 35 and IMC< 39.999:
        obesidad = 1
    else:
        obesidad = 0    

    if riesgo_braden == "Alto":
        braden_malta = 1
    else:
        braden_malta = 0

    logit_base = (intercept +
                coef_edad * edad +
                coef_ecv * ECV1 +
                coef_braden_malta * braden_malta +
                coef_obesidad * obesidad)
    riesgo_base = 1 / (1 + np.exp(-logit_base))
    riesgo_80 = 0.80 * riesgo_base

        
    promedionoches_solucion = -(np.log((1 / riesgo_80) - 1) + intercept + coef_edad * edad + coef_ecv * ECV1 + coef_braden_malta * braden_malta + coef_obesidad * obesidad) / coef_promedionoches
    promedionoches_solucion = round(promedionoches_solucion,1)
    return promedionoches_solucion
    

btn = st.button("ENVIAR", on_click=clicked) 
st.markdown("---")
