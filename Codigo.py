#Hola
import streamlit as st
import math

st.set_page_config(page_title="Calculadora reposicionamiento", layout="wide")

with st.container():
    st.title("Calculadora de Reposicionamientos")
    st.write("Bienvenido(a)! Con esta calculadora podrá saber cada cuanto tiempo se debe reposicionar un paciente en una unidad de cuidados intensivos, a continuación se solicitarán datos del paciente, con los cuales se calculará el tiempo. Además se le solicitará que haga la valoración de la escala de Braden para el calculo completo. ¡Adelante!")
st.markdown("---")


edad = st.number_input("Escriba la edad del paciente")
IMC = st.number_input("Escriba el IMC del paciente")
braden_valores = []
Patologias = {"Diabetes":'Diabetes Melitus',
              "Endocrino":'Enfermedad endocrina',
              "Cardiovascular":'Enfermedad cardiaca',
              "Hepatitis":'Enfermedad hepatica',
              "Respiratorio":'Enfermedad respiratoria',
              "Renal":'Enfermedad renal', 
              "Neurologico":'Problema neurologico'
              }

def clicked():
    braden_valores.append(braden)
    braden_valores.append(braden2)
    braden_valores.append(braden3)
    braden_valores.append(braden4)
    braden_valores.append(braden5)
    braden_valores.append(braden6)
    riesgos(edad, IMC, braden_valores,pato2)
    he, me, s, r = riesgos(edad, IMC, braden_valores,pato2)
    st.header("El paciente presenta un riesgo de aparición de Úlceras por presión de:")
    st.subheader(round(r,3))
    if r > 0.9:
        st.header("El paciente debe ser movilizado cada hora, su estado de salud es demasiado delicado")
    else:
        st.header("A este paciente se le debe hacer un reposicionamiento cada:")
        with st.container():
            a, b, c, d, e, f = st.columns(6)
            with a:
                st.write(he)
            with b:
                st.text("Hora(s)")
            with c:
                st.write(me)    
            with d:
                st.text("Minuto(s)")
            with e:
                st.write(s)
            with f:
                st.text("Segundo(s)")
    st.markdown("---")            

pato1 = st.multiselect("Escoja la categoría de complicación que presenta el paciente", options=("Diabetes", "Cardiovascular", "Renal", "Respiratorio", "Neurologico", "Hepatitis", "Endocrino"))
pato2 = []
for patologia in pato1:
    if patologia in Patologias:        
        pato2.append(Patologias[patologia])

st.multiselect("Escoja la complicación asociada a la categoría que escogió",options = (pato2))
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

def riesgos(edad, IMC, braden_valores,pato2):
    horas_enteras = 0
    minutos_enteros = 0
    minutos_float = 0
    segundos = 0
    DM1,Ene,Enc,Enfhep,Enren, Pn , Enresp = [0]*7
    patologia_dict = {
        "Diabetes Melitus 1": "DM1",
        "Enfermedad endocrina": "Ene",
        "Enfermedad cardiaca": "Enc",
        "Enfermedad hepática": "Enfhep",
        "Enfermedad renal": "Enren",
        "Enfermedad respiratoria": "Enresp",
        "Problema neurológico": "Pn"
    }
    variables = {
        "DM1": DM1,  "Ene": Ene, "Enc": Enc,
        "Enfhep": Enfhep, "Enren": Enren, "Pn": Pn,
        "Enresp": Enresp
    }
    for patologia in pato2:
        if patologia in patologia_dict:
            variables[patologia_dict[patologia]] = 1

    DM1, Ene, Enc, Enfhep, Enren, Pn, Enresp = \
        variables["DM1"], variables["Ene"], variables["Enc"], \
        variables["Enfhep"], variables["Enren"], variables["Pn"], variables["Enresp"]
    
 
    u = -7.366 - 0.01*edad + 0.179*IMC + 0.326*Enresp - 19.194*DM1 + 0.215*Pn - 18.574*Enc + 0.125*Enren -18.586*Enfhep + 0.713*Ene
    Riesgo_total = ((math.exp(u))/(1+math.exp(u)))

    suma1 = sum(braden_valores)
    if suma1 < 12:
        riesgo_braden = "Alto"
    elif suma1 >= 12 and suma1 < 14:
        riesgo_braden = "Medio"
    elif suma1 >= 14 and suma1 <= 23:
        riesgo_braden = "Bajo"
    if riesgo_braden == "Alto":
        Riesgo_total = Riesgo_total + 0.1
    elif riesgo_braden == "Bajo":
        Riesgo_total = Riesgo_total - 0.01
    elif riesgo_braden == "Medio":
        Riesgo_total = Riesgo_total - 0.025

    Riesgo_total1 = 3- (3*Riesgo_total)
    horas_enteras = int(Riesgo_total1)
    minutos_float = (Riesgo_total1 - horas_enteras) * 60
    minutos_enteros = int(minutos_float)
    segundos = int((minutos_float - minutos_enteros) * 60)
    DM1,Ene,Enc,Enfhep,Enren,Pn,Enresp = [0]*7
    return horas_enteras, minutos_enteros, segundos, Riesgo_total
    

btn = st.button("ENVIAR", on_click=clicked) 
st.markdown("---")
