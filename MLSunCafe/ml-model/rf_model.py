import pickle

# Save model
with open("rf_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save training columns
with open("training_columns.pkl", "wb") as f:
    pickle.dump(training_columns, f)
