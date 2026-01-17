import streamlit as st
import joblib
import pickle
import numpy as np

# ==============================
# Load saved files
# ==============================

@st.cache_resource
def load_artifacts():
    model = joblib.load("lgbm_final_model.pkl")

    with open("feature_order.pkl", "rb") as f:
        feature_order = pickle.load(f)

    with open("optimal_threshold.pkl", "rb") as f:
        threshold = pickle.load(f)

    return model, feature_order, threshold


model, feature_order, threshold = load_artifacts()

# ==============================
# Streamlit UI
# ==============================

st.set_page_config(page_title="Transaction Prediction", layout="centered")

st.title("💳 Transaction Prediction App")
st.write("This app predicts the transaction outcome using a trained ML model.")

st.info(f"🔢 Model expects **{len(feature_order)} input values**")

st.markdown(
    """
    ### Instructions
    - Enter **numeric values only**
    - Values must be **comma-separated**
    - Total numbers must be **exactly the same as model features**
    """
)

# ==============================
# Input
# ==============================

features_input = st.text_area(
    "Enter feature values (comma separated)",
    height=150,
    placeholder="Example: 0, 1, 5000, 0, 0, 1, ...",
)

# ==============================
# Prediction
# ==============================

if st.button("🔮 Predict"):
    try:
        # Convert input text to list of floats
        values = [float(x.strip()) for x in features_input.split(",") if x.strip() != ""]

        # Validate feature length
        if len(values) != len(feature_order):
            st.error(
                f"❌ Expected {len(feature_order)} values, but got {len(values)}"
            )
        else:
            input_array = np.array(values).reshape(1, -1)

            # Model prediction
            probability = model.predict(input_array)[0]
            prediction = int(probability >= threshold)

            # Output
            st.success("✅ Prediction Successful")
            st.write(f"**Prediction:** {prediction}")
            st.write(f"**Probability:** {probability:.4f}")

    except Exception as e:
        st.error(f"Error: {e}")

# ==============================
# Footer
# ==============================

st.markdown("---")
st.caption("🚀 Deployed using Streamlit Cloud")
