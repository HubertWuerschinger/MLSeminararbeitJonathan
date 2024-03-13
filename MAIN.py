
import streamlit as st
import pandas as pd
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np

def load_model():
    # Laden des trainierten CNN-Modells
    model = tf.keras.models.load_model('Final_model.h5')
    return model

def main():
    st.title("Werkzeugverschleiß Überwachung")

    # Erfassung von Daten
    st.subheader("Erfassung")
    state = st.file_uploader("Bilddaten hochladen", type=['jpg', 'png'])
    tool_type = st.text_input("Werkzeugtyp eingeben")
    vorschub = st.text_input("Vorschub eingeben (In mm/min)")
    drehzahl = st.text_input("Drehzahl eingeben (In min-1)")
    zustellung = st.text_input("Zustellung eingeben (In mm)")
    component_name = st.text_input("Bauteilname eingeben")
    machining_duration = st.number_input("Bearbeitungsdauer pro Bauteil eingeben (in Sekunden)", 
                                     min_value=0, 
                                     step=1, 
                                     format="%d")

    # Daten speichern
    if st.button("Daten speichern"):
        save_data(state, tool_type, vorschub, drehzahl, zustellung, component_name, machining_duration)
        st.success("Daten erfolgreich gespeichert!")

    # Darstellung der erfassten Daten
    st.subheader("Erfasste Daten")
    data_display = load_data()
    st.write(data_display)

    # Visualisierung des Verschleißverlaufs
    st.subheader("Verschleißverlauf")
    if not data_display.empty:
        st.line_chart(data_display['Machining Duration'])

    # Klassifizierung der hochgeladenen Bilder
    st.subheader("Bildklassifizierung")
    if state is not None:
        model = load_model()
        img = image.load_img(state, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)
        classes = ['Neu', 'Mittel', 'Defekt']
        result = classes[np.argmax(prediction)]
        st.write(f"Das hochgeladene Bild wird als '{result}' klassifiziert.")

def save_data(state, tool_type, vorschub, drehzahl, zustellung, component_name, machining_duration):
    data = {
        'State': [state],
        'Tool Type': [tool_type],
        'Vorschub': [vorschub],
        'Drehzahl': [drehzahl],
        'Zustellung': [zustellung],
        'Component Name': [component_name],
        'Machining Duration': [machining_duration]
    }
    if not os.path.exists('data.csv'):
        df = pd.DataFrame(data)
        df.to_csv('data.csv', index=False)
    else:
        df = pd.read_csv('data.csv')
        new_data = pd.DataFrame(data)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv('data.csv', index=False)


def load_data():
    if os.path.exists('data.csv'):
        return pd.read_csv('data.csv')
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    main()
