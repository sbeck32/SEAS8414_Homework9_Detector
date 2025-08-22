# Filename: 2_analyze_domain.py
import h2o
import pandas as pd
import math
import argparse
import os
import google.generativeai as genai

def get_entropy(s):
    p, lns = {}, float(len(s))
    for c in s:
        p[c] = p.get(c, 0) + 1
    return -sum(count/lns * math.log(count/lns, 2) for count in p.values())

def analyze_domain(domain_name):
    print(f"\nAnalyzing domain: {domain_name}...")

    print("Loading H2O model...")
    model_path = os.path.join("model", "DGA_Leader.zip")
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return
    model = h2o.import_mojo(model_path)

    print("Computing features...")
    length = len(domain_name)
    entropy = get_entropy(domain_name)
    features = pd.DataFrame([[length, entropy]], columns=['length', 'entropy'])
    h2o_features = h2o.H2OFrame(features)
    print(f"  - Length: {length}")
    print(f"  - Entropy: {entropy}")

    print("Predicting and generating SHAP explanation...")
    # First, get the standard prediction results
    predictions = model.predict(h2o_features)

    # Then, get the SHAP contributions using H2O's built-in method
    shap_contribs = model.predict_contributions(h2o_features)

    # Convert H2O Frames to pandas DataFrames for easier handling
    prediction_df = predictions.as_data_frame()
    shap_values_df = shap_contribs.as_data_frame()

    # Extract prediction and confidence from the prediction results
    prediction = prediction_df['predict'][0]
    confidence = prediction_df['dga'][0] if prediction == 'dga' else prediction_df['legit'][0]

    print(f"  - Prediction: {prediction.upper()}")
    print(f"  - Confidence: {confidence:.2%}")

    print("Summarizing SHAP findings...")
    shap_summary = (
        "Domain Analysis Summary:\n"
        f"- Domain: {domain_name}\n"
        f"- Prediction: This domain is classified as '{prediction.upper()}'.\n"
        f"- Confidence Score: {confidence:.2%}\n"
        "Feature Contributions (Explanation):\n"
    )
    # The column names in the SHAP frame are the feature names
    for feature in shap_values_df.columns:
        if feature == 'BiasTerm': continue
        value = shap_values_df[feature].iloc[0]
        impact = "increases" if value > 0 else "decreases"
        original_feature_value = features[feature].iloc[0]
        shap_summary += (
            f"  - The '{feature}' value of {original_feature_value:.2f} "
            f"{impact} the likelihood of it being a DGA domain.\n"
        )
    print(shap_summary)

    print("Generating incident response playbook with Google's Gemini model...")
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

        # Use an updated, stable model name
        generative_model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "You are a senior cybersecurity analyst. Based on the following domain analysis summary, "
            "generate a concise, step-by-step incident response playbook for a junior analyst. "
            "The playbook should be written in Markdown format and include specific, actionable steps. "
            "If the domain is predicted as DGA, the playbook should be strict and focus on containment. "
            "If it's legitimate, the playbook should focus on verification and closing the ticket.\n\n"
            "--- ANALYSIS SUMMARY ---\n"
            f"{shap_summary}"
            "\n--- END SUMMARY ---\n\n"
            "Generate the playbook now."
        )
        response = generative_model.generate_content(prompt)
        playbook = response.text

        print("\n" + "="*20 + " INCIDENT RESPONSE PLAYBOOK " + "="*20)
        print(playbook)
        print("="*64 + "\n")
    except Exception as e:
        print(f"\nCould not generate playbook. Error: {e}")
        print("Please ensure your GOOGLE_API_KEY is set correctly.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a domain for DGA characteristics.")
    parser.add_argument("-d", "--domain", required=True, help="The domain name to analyze.")
    args = parser.parse_args()

    h2o.init(nthreads=-1, max_mem_size="4g", log_level="ERRR")
    analyze_domain(args.domain)
    h2o.shutdown(prompt=False)