import pickle
from sklearn.ensemble import RandomForestClassifier
classification_model = RandomForestClassifier(n_estimators=100)


# After training your model, pickle it
with open('flood_classification_model.pkl', 'wb') as file:
    pickle.dump(classification_model, file)

print("Model has been saved as 'flood_classification_model.pkl'")
