# Filename: 1_train_and_export.py
import h2o
from h2o.automl import H2OAutoML
import os

print("Starting H2O...")
h2o.init(nthreads=-1, max_mem_size="4g")

print("Importing data...")
train = h2o.import_file("dga_dataset_train.csv")

x = train.columns
y = "class"
x.remove(y)
x.remove("domain")

train[y] = train[y].asfactor()

print("Running AutoML...")
# Constrain AutoML to only run algorithms that support predict_contributions
aml = H2OAutoML(max_runtime_secs=120, seed=1,
                include_algos=["GBM", "DRF", "XGBoost"])
aml.train(x=x, y=y, training_frame=train)

print("AutoML training complete. Leader model:")
leader = aml.leader
print(leader)

model_path = os.path.join(os.getcwd(), "model")

if not os.path.exists(model_path):
    os.makedirs(model_path)
    print(f"Created directory: {model_path}")

print(f"Exporting leader model to {model_path}...")
mojo_path = leader.download_mojo(path=model_path, get_genmodel_jar=False)
print(f"Model saved to: {mojo_path}")

new_mojo_path = os.path.join(model_path, "DGA_Leader.zip")
os.rename(mojo_path, new_mojo_path)
print(f"Renamed model to: {new_mojo_path}")

print("Shutting down H2O.")
h2o.shutdown(prompt=False)