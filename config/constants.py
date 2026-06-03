# config.py
"""
Configuration and constant values for the weather prediction app
"""

# Regression Metrics Data from PDF
REGRESSION_METRICS = {
    "LSTM": {
        "Mean Squared Error (MSE)": 0.3243687945,
        "Root Mean Squared Error (RMSE)": 0.5695338396,
        "Mean Absolute Error (MAE)": 0.5511240855,
        "Mean Absolute Percentage Error (MAPE)": 0.04125092193,
        "R² Score": 0.9190614102,
        "Adjusted R²": 0.9190520464
    },
    "GRU": {
        "Mean Squared Error (MSE)": 0.453669095,
        "Root Mean Squared Error (RMSE)": 0.6735496233,
        "Mean Absolute Error (MAE)": 0.6348076761,
        "Mean Absolute Percentage Error (MAPE)": 0.05978733876,
        "R² Score": 0.9091641429,
        "Adjusted R²": 0.9091360244
    },
    "ANN": {
        "Mean Squared Error (MSE)": 1.562749812,
        "Root Mean Squared Error (RMSE)": 1.2500999208,
        "Mean Absolute Error (MAE)": 1.318185829,
        "Mean Absolute Percentage Error (MAPE)": 0.05641701972,
        "R² Score": 0.8720618886,
        "Adjusted R²": 0.87201069
    },
    "Dense ANN": {
        "Mean Squared Error (MSE)": 1.155,
        "Root Mean Squared Error (RMSE)": 1.075,
        "Mean Absolute Error (MAE)": 0.855,
        "Mean Absolute Percentage Error (MAPE)": 0.0901,
        "R² Score": 0.9148,
        "Adjusted R²": 0.9139
    },
    "SVM": {
        "Mean Squared Error (MSE)": 1.517377602,
        "Root Mean Squared Error (RMSE)": 1.231818819,
        "Mean Absolute Error (MAE)": 1.454439479,
        "Mean Absolute Percentage Error (MAPE)": 0.05076528964,
        "R² Score": 0.8563314209,
        "Adjusted R²": 0.8562616927
    },
    "QLSTM": {
        "Mean Squared Error (MSE)": 0.3964716947,
        "Root Mean Squared Error (RMSE)": 0.6296599834,
        "Mean Absolute Error (MAE)": 0.5773612303,
        "Mean Absolute Percentage Error (MAPE)": 0.04739095426,
        "R² Score": 0.908704844,
        "Adjusted R²": 0.9086828532
    },
    "QGRU": {
        "Mean Squared Error (MSE)": 0.5148015544,
        "Root Mean Squared Error (RMSE)": 0.7174967,
        "Mean Absolute Error (MAE)": 0.7058171975,
        "Mean Absolute Percentage Error (MAPE)": 0.06563023825,
        "R² Score": 0.8912701421,
        "Adjusted R²": 0.8912313704
    },
    "QNN_SE": {
        "Mean Squared Error (MSE)": 1.182737932,
        "Root Mean Squared Error (RMSE)": 1.087537554,
        "Mean Absolute Error (MAE)": 0.9784103794,
        "Mean Absolute Percentage Error (MAPE)": 0.05039208815,
        "R² Score": 0.8877785449,
        "Adjusted R²": 0.8877215659
    },
     "QNN_IS": {
        "Mean Squared Error (MSE)": 1.274808481,
        "Root Mean Squared Error (RMSE)": 1.12907417,
        "Mean Absolute Error (MAE)": 1.080676887,
        "Mean Absolute Percentage Error (MAPE)": 0.04455394308,
        "R² Score": 0.8745918045,
        "Adjusted R²": 0.87443039
    },
    "VQC": {
        "Mean Squared Error (MSE)": 1.331936334,
        "Root Mean Squared Error (RMSE)": 1.154095461,
        "Mean Absolute Error (MAE)": 1.308312858,
        "Mean Absolute Percentage Error (MAPE)": 0.04250832392,
        "R² Score": 0.8692373539,
        "Adjusted R²": 0.869175596
    },
    "QSVM": {
        "Mean Squared Error (MSE)": 1.555231881,
        "Root Mean Squared Error (RMSE)": 1.247089364,
        "Mean Absolute Error (MAE)": 1.411327942,
        "Mean Absolute Percentage Error (MAPE)": 0.05093823265,
        "R² Score": 0.8584812319,
        "Adjusted R²": 0.8584063078
    },
    "Hybrid_QNN": {
        "Mean Squared Error (MSE)": 1.261,
        "Root Mean Squared Error (RMSE)": 1.1229,
        "Mean Absolute Error (MAE)": 1.455,
        "Mean Absolute Percentage Error (MAPE)": 0.0458,
        "R² Score": 0.9031,
        "Adjusted R²": 0.9051
    }
}

# Ideal values for metrics
IDEAL_VALUES = {
    "Mean Squared Error (MSE)": "Lower is better",
    "Root Mean Squared Error (RMSE)": "Lower is better",
    "Mean Absolute Error (MAE)": "Lower is better",
    "Mean Absolute Percentage Error (MAPE)": "Lower is better",
    "R² Score": "Close to 1",
    "Adjusted R²": "Close to 1"
}

ALGORITHM_SHORT_NAMES = {
    "Long Short Term Memory (LSTM)": "LSTM",
    "Gated Recurrent Unit (GRU)": "GRU",
    "Artificial Neural Network (ANN)": "ANN",
    "Dense Artificial Neural Network (Dense ANN)": "Dense ANN",
    "Support Vector Machine (SVM)": "SVM",
    "Quantum Long Short Term Memory (QLSTM)": "QLSTM",
    "Quantum Gated Recurrent Unit (QGRU)": "QGRU",
    "Quantum Neural Network with Strong Entangling Layers(QNN_SE)": "QNN_SE",
    "Quantum Neural Network with Ising Layers (QNN_IS)": "QNN_IS",
    "Variational Quantum Classifier (VQC)": "VQC",
    "Quantum Support Vector Machine (QSVM)": "QSVM",
    "Hybrid Quantum Neural Network (Hybrid QNN)": "Hybrid QNN"
}

# Quantum Resource Estimates Data from PDF
QUANTUM_RESOURCE_DATA = {
    "algorithms": ['QGRU', 'QLSTM', 'QNN-Ising', 'QNN-SE', 'VQC', 'QSVM', 'Hybrid QNN'],
    "single_gate_count": [135, 180, 46, 54, 30, 14, 24],
    "multi_gate_count": [60, 80, 21, 20, 30, 8, 6],
    "depth": [63, 84, 42, 29, 20, 8, 9],
    "colors": ['#8B5CF6', '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#6366F1', '#831843']
}

CITIES = {
    "Delhi": {
        "lat": 28.6139,
        "lon": 77.2090,
        "temp": 309.98,
        "region": "Northern India",
        "zoom_description": "National Capital Region - Urban Heat Island Effect Analysis",
        "subzones":{
            "Safdarjung":{
                "lat" : 28.5796,
                "lon" : 77.2090,
                "zone_polygon": [
                    (28.5900, 77.1920),
                    (28.5900, 77.2180),
                    (28.5600, 77.2180),
                    (28.5600, 77.1920),
                    (28.5900, 77.1920)
                
                ],
                "region" :"South Delhi"           
            },
        }
    },
    # "Mumbai": {
    #     "lat": 19.0760,
    #     "lon": 72.8777,
    #     "temp": 305.45,
    #     "region": "Western India",
    #     "zoom_description": "Coastal City - Monsoon and Maritime Weather Patterns"
    # },
    # "Kolkata": {
    #     "lat": 22.5726,
    #     "lon": 88.3639,
    #     "temp": 307.23,
    #     "region": "Eastern India",
    #     "zoom_description": "Eastern Plains - Cyclone Prone Coastal Region"
    # },
    # "Chennai": {
    #     "lat": 13.0827,
    #     "lon": 80.2707,
    #     "temp": 311.67,
    #     "region": "Southern India",
    #     "zoom_description": "Southeast Coast - Tropical Climate with Seasonal Rainfall"
    # },
    # "Bengaluru": {
    #     "lat": 12.9716,
    #     "lon": 77.5946,
    #     "temp": 298.76,
    #     "region": "Southern India",
    #     "zoom_description": "Deccan Plateau - Moderate Climate at Higher Elevation"
    # }
}

# Algorithm configurations
CLASSICAL_ALGORITHMS = {
    "Select Classical Algorithm": {"name": "Select Classical Algorithm", "file": ""},
    "Long Short Term Memory (LSTM)": {"name": "LSTM (Long Short-Term Memory)", "file": "files/LSTM_forecast - LSTM_forecast.csv"},
    "Gated Recurrent Unit (GRU)": {"name": "GRU (Gated Recurrent Unit)", "file": "files/GRU_forecast - GRU_forecast.csv"},
    "Artificial Neural Network (ANN)": {"name": "ANN (Artificial Neural Network)", "file": "files/ANN_forecast - ANN_forecast.csv"},
    "Dense Artificial Neural Network (Dense ANN)": {"name": "Dense ANN", "file": "files/Dense_ANN_new.csv"},
    "Support Vector Machine (SVM)": {"name": "SVM (Support Vector Machine)", "file": "files/SVM_forecast.csv"}
}
QUANTUM_ALGORITHMS = {
    "Select Quantum Algorithm": {"name": "Select Quantum Algorithm", "file": ""},
    "Quantum Long Short Term Memory (QLSTM)": {"name": "QLSTM (Quantum LSTM)", "file": "files/QLSTM_forecast - QLSTM_forecast.csv"},
    "Quantum Gated Recurrent Unit (QGRU)": {"name": "QGRU (Quantum GRU)", "file": "files/QGRU_forecast - QGRU_forecast.csv"},
    "Quantum Neural Network with Strong Entangling Layers(QNN_SE)": {"name": "QNN-SE (Quantum Neural Network - SE)", "file": "files/QNN_SE_forecast - QNN_SE_forecast.csv"},
    "Quantum Neural Network with Ising Layers (QNN_IS)": {"name": "QNN-IS (Quantum Neural Network - IS)", "file": "files/QNN_IS_forecast - QNN_IS_forecast.csv"},
    "Variational Quantum Classifier (VQC)": {"name": "VQC (Variational Quantum Classifier)", "file": "files/VQC_forecast - VQC_forecast.csv"},
    "Quantum Support Vector Machine (QSVM)": {"name": "QSVM (Quantum SVM)", "file": "files/QSVM_forecast.csv"},
    "Hybrid Quantum Neural Network (Hybrid QNN)": {"name": "Hybrid QNN", "file": "files/HybridQNN_month_3.csv"}
}

# Algorithm Parameters for Training
ALGORITHM_PARAMS = {
    'LSTM': {'classical': 460, 'quantum': 0, 'type': 'classical'},
    'GRU': {'classical': 1073, 'quantum': 0, 'type': 'classical'},
    'ANN': {'classical': 48, 'quantum': 0, 'type': 'classical'},
    'Dense ANN': {'classical': 17653, 'quantum': 0, 'type': 'classical'},
    'SVM': {'classical': 0, 'quantum': 0, 'type': 'classical', 'note': 'Kernel-based method'},
    'QLSTM': {'classical': 0, 'quantum': 190, 'type': 'quantum'},
    'QGRU': {'classical': 0, 'quantum': 164, 'type': 'quantum'},
    'QNN_SE': {'classical': 0, 'quantum': 48, 'type': 'quantum'},
    'QNN_IS': {'classical': 0, 'quantum': 21, 'type': 'quantum'},
    'VQC': {'classical': 0, 'quantum': 10, 'type': 'quantum'},
    'QSVM': {'classical': 0, 'quantum': 0, 'type': 'quantum', 'note': 'Kernel-based method'},
    'Hybrid QNN': {'classical': 17653, 'quantum': 20, 'type': 'hybrid'}
}
# ==================== RAINFALL PREDICTION CONSTANTS ====================
############### Adding from here about the Rainfall
# Classification Metrics for Rainfall (Binary Classification: Rain/No Rain)
CLASSIFICATION_METRICS = {
    "ANN": {
        "True Negatives (TN)":437,
        "False Positives (FP)":30,
        "False Negatives (FN)": 50,
        "True Positives (TP)": 225,
        "Accuracy": 0.8921832884097035,
        "Precision (No Rain)": 0.8973305954825462,
        "Recall (No Rain)": 0.9357601713062098,
        "F1-Score (No Rain)":0.9161425576519916 ,
        "Precision (Rain)": 0.8823529411764706,
        "Recall (Rain)": 0.8181818181818182,
        "F1-Score (Rain)": 0.8490566037735849,
        "Support (No Rain)": 467.0,
        "Support (Rain)":275.0 
    },
    "LSTM": {
        "True Negatives (TN)":425,
        "False Positives (FP)":42,
        "False Negatives (FN)": 73,
        "True Positives (TP)": 202,
        "Accuracy": 0.8450134771,
        "Precision (No Rain)": 0.8534136546,
        "Recall (No Rain)": 0.9100642398,
        "F1-Score (No Rain)": 0.8808290155,
        "Precision (Rain)":0.8278688525,
        "Recall (Rain)": 0.7345454545,
        "F1-Score (Rain)": 0.7784200385,
        "Support (No Rain)": 467,
        "Support (Rain)": 275
    },
    "GRU": {
        "True Negatives (TN)":424,
        "False Positives (FP)":43,
        "False Negatives (FN)":74 ,
        "True Positives (TP)": 201,
        "Accuracy": 0.8423180593,
        "Precision (No Rain)": 0.8514056225,
        "Recall (No Rain)": 0.9079229122,
        "F1-Score (No Rain)": 0.8787564767,
        "Precision (Rain)": 0.8237704918,
        "Recall (Rain)": 0.7309090909,
        "F1-Score (Rain)": 0.774566474,
        "Support (No Rain)": 467,
        "Support (Rain)": 275
    },
    "SVM": {
        "True Negatives (TN)": 439,
        "False Positives (FP)": 28,
        "False Negatives (FN)": 47,
        "True Positives (TP)": 228,
        "Accuracy": 0.898921832884097,
        "Precision (No Rain)": 0.9032921810699589,
        "Recall (No Rain)": 0.9400428265524625,
        "F1-Score (No Rain)": 0.9213011542497377,
        "Precision (Rain)": 0.890625,
        "Recall (Rain)": 0.8290909090909091,
        "F1-Score (Rain)": 0.8587570621468926,
        "Support (No Rain)": 467,
        "Support (Rain)": 275
    },
    "QNN_IS": {
        "True Negatives (TN)": 427,  
        "False Positives (FP)": 40,   
        "False Negatives (FN)": 68,   
        "True Positives (TP)": 207,   
        "Accuracy": 0.8544474393530997,
        "Precision (No Rain)": 0.8626262626262626,
        "Recall (No Rain)": 0.9143468950749465,
        "F1-Score (No Rain)": 0.8877338877338877,
        "Precision (Rain)": 0.8380566801619433,
        "Recall (Rain)": 0.7527272727272727,
        "F1-Score (Rain)": 0.7931034482758621,
        "Support (No Rain)":467,
        "Support (Rain)": 275
    },
    "QNN_SE": {
        "True Negatives (TN)":432 ,  
        "False Positives (FP)": 35,   
        "False Negatives (FN)": 61,   
        "True Positives (TP)": 214,   
        "Accuracy": 0.860619946091644,
        "Precision (No Rain)": 0.866267748478701,
        "Recall (No Rain)": 0.925053533190578,
        "F1-Score (No Rain)": 0.9,
        "Precision (Rain)": 0.859437751004016,
        "Recall (Rain)":0.778181818181818,
        "F1-Score (Rain)": 0.816793893129771,
        "Support (No Rain)":467,
        "Support (Rain)":275 
    },
    "QLSTM": {
        "True Negatives (TN)": 415,  
        "False Positives (FP)": 52,   
        "False Negatives (FN)": 89,   
        "True Positives (TP)": 186,   
        "Accuracy": 0.8099730458,
        "Precision (No Rain)": 0.8234126984,
        "Recall (No Rain)": 0.8886509636,
        "F1-Score (No Rain)": 0.8547888774,
        "Precision (Rain)": 0.781512605,
        "Recall (Rain)":0.6763636364,
        "F1-Score (Rain)":0.7251461988,
        "Support (No Rain)":467,
        "Support (Rain)":275 
    },
    "QGRU": {
        "True Negatives (TN)":413,  
        "False Positives (FP)": 54,   
        "False Negatives (FN)": 93,   
        "True Positives (TP)": 182,   
        "Accuracy": 0.8018867925,
        "Precision (No Rain)":0.8162055336,
        "Recall (No Rain)": 0.8843683084,
        "F1-Score (No Rain)": 0.8489208633,
        "Precision (Rain)": 0.7711864407,
        "Recall (Rain)":0.6618181818,
        "F1-Score (Rain)": 0.7123287671,
        "Support (No Rain)":467,
        "Support (Rain)": 275 
    },
    "VQC": {
        "True Negatives (TN)": 425,  
        "False Positives (FP)": 42,   
        "False Negatives (FN)": 72,   
        "True Positives (TP)": 203,   
        "Accuracy": 0.8463611859838275,
        "Precision (No Rain)": 0.8551307847082495,
        "Recall (No Rain)": 0.9100642398286938,
        "F1-Score (No Rain)": 0.8817427385892116,
        "Precision (Rain)": 0.8285714285714286,
        "Recall (Rain)":0.7381818181818182,
        "F1-Score (Rain)": 0.7807692307692308,
        "Support (No Rain)":467,
        "Support (Rain)": 275
    },
    "QSVM": {
        "True Negatives (TN)": 422,
        "False Positives (FP)": 45,
        "False Negatives (FN)": 78,
        "True Positives (TP)": 197,
        "Accuracy": 0.8342318059299192,
        "Precision (No Rain)": 0.844,
        "Recall (No Rain)":0.9036402569593148,
        "F1-Score (No Rain)": 0.8728024819027922,
        "Precision (Rain)": 0.8140495867768595,
        "Recall (Rain)": 0.7163636363636363,
        "F1-Score (Rain)": 0.7620889748549323,
        "Support (No Rain)":467 ,
        "Support (Rain)": 275
    },
    "Hybrid QNN": {
        "True Negatives (TN)": 419,
        "False Positives (FP)": 48,
        "False Negatives (FN)": 39,
        "True Positives (TP)": 236,
        "Accuracy": 0.8827,
        "Precision (No Rain)":0.9148 ,
        "Recall (No Rain)":0.8972,
        "F1-Score (No Rain)": 0.9059,
        "Precision (Rain)": 0.831,
        "Recall (Rain)": 0.8582,
        "F1-Score (Rain)": 0.8444,
        "Support (No Rain)":467,
        "Support (Rain)": 275
    },
    "Hybrid_QNN": {
        "True Negatives (TN)": 419,
        "False Positives (FP)": 48,
        "False Negatives (FN)": 39,
        "True Positives (TP)": 236,
        "Accuracy": 0.8827,
        "Precision (No Rain)":0.9148 ,
        "Recall (No Rain)":0.8972,
        "F1-Score (No Rain)": 0.9059,
        "Precision (Rain)": 0.831,
        "Recall (Rain)": 0.8582,
        "F1-Score (Rain)": 0.8444,
        "Support (No Rain)":467,
        "Support (Rain)": 275
    },
    "Dense ANN": {
        "True Negatives (TN)": 426,
        "False Positives (FP)": 41,
        "False Negatives (FN)": 20,
        "True Positives (TP)": 255,
        "Accuracy": 0.917,
        "Precision (No Rain)": 0.9552,
        "Recall (No Rain)":0.9122,
        "F1-Score (No Rain)":0.9332 ,
        "Precision (Rain)":0.8615,
        "Recall (Rain)": 0.9273,
        "F1-Score (Rain)":0.8932,
        "Support (No Rain)": 467,
        "Support (Rain)": 275
    }
}


RAINFALL_IDEAL_VALUES ={
        "Accuracy": "Close to 1",
        "Precision (No Rain)": "Close to 1",
        "Recall (No Rain)":"Close to 1",
        "F1-Score (No Rain)": "Close to 1",
        "Precision (Rain)":"Close to 1",
        "Recall (Rain)": "Close to 1",
        "F1-Score (Rain)":"Close to 1"

}
# Mapping for file names
RAINFALL_FILE_MAPPING = {
    "ANN": {
        "predictions": "ANN_predictions_Aug2025.csv",
    },
    "GRU": {
        "predictions": "GRU_predictions_Aug2025.csv",    
    },
    "LSTM": {
        "predictions": "LSTM_predictions_Aug2025.csv",
    },
    "SVM": {
        "predictions": "SVM_predictions_Aug2025.csv",
    },
    "QNN_IS": {
        "predictions": "QNNIS_predictions_Aug2025.csv",
       
    },
    "QSVM": {
        "predictions": "QSVM_predictions_Aug2025.csv",
    },
    "QGRU": {
        "predictions": "QGRU_predictions_Aug2025.csv",
    },
    "QLSTM": {
        "predictions": "QLSTM_predictions_Aug2025.csv",
    },
    "QNN_SE": {
        "predictions": "QNNSE_predictions_Aug2025.csv",
    },
    "VQC": {
        "predictions": "VQC_predictions_Aug2025.csv",
    },
    "Dense ANN": {
        "predictions": "data_rainfall_dense_ANN_converted.csv",
    },
    "Hybrid QNN": {
        "predictions": "data_rainfall_Hybrid_QNN_converted.csv",
    },
}
# ==================== NOISE ANALYSIS CONSTANTS ====================
# Noise types available
NOISE_TYPES = [
    "Without Noise", 
    "Depolarizing Error",
    "Dephasing Error",
    "Amplitude Damping Error",
    "Thermal Relaxation Error",
    "Readout Error",
    "Initialization Error",
    "Gate Rotation Error"
]
# ✅ CRITICAL: Mapping from display names to folder names
# Your folders don't have spaces, so we need this mapping
NOISE_TYPE_TO_FOLDER = {
    "Without Noise": "WithoutNoise",
    "Depolarizing Error": "DepolarizingError",
    "Dephasing Error": "DephasingError",
    "Amplitude Damping Error": "AmplitudeDampingError",
    "Thermal Relaxation Error": "ThermalRelaxationError",
    "Readout Error": "ReadoutError",
    "Initialization Error": "InitializationError",
    "Gate Rotation Error": "GateRotationError"
}

# Quantum algorithms available for noise analysis
NOISE_QUANTUM_ALGORITHMS = {
    "Select Quantum Algorithm": {"name": "Select Quantum Algorithm", "short_name": ""},
    "Quantum Gated Recurrent Unit (QGRU)": {
        "name": "QGRU",
        "short_name": "QGRU",
        "without_noise_file": "files/QGRU_forecast - QGRU_forecast.csv",  
        "noise_folder": "files/temperaturenoise_data/{error_type}/QGRU_{error_type}.csv"
        
    },
    "Quantum Neural Network with Ising Layers (QNN_IS)": {
        "name": "QNN_IS",
        "short_name": "QNN_IS",
        "without_noise_file": "files/QNN_IS_forecast - QNN_IS_forecast.csv",  
        "noise_folder": "files/temperaturenoise_data/{error_type}/QNN_IS_{error_type}.csv"
    },
    "Quantum Neural Network with Strong Entangling layer(QNN_SE)": {
        "name": "QNN_SE",
        "short_name": "QNN_SE",
        "without_noise_file": "files/QNN_SE_forecast - QNN_SE_forecast.csv",  
        "noise_folder": "files/temperaturenoise_data/{error_type}/QNN_SE_{error_type}.csv"
    },
    "Hybrid Quantum Neural Network (Hybrid QNN)": {
        "name": "Hybrid_QNN",
        "short_name": "Hybrid_QNN",
        "without_noise_file": "files/HybridQNN_month_3.csv",  
        "noise_folder": "files/temperaturenoise_data/{error_type}/HQNN_{error_type}.csv"
    },
    "Quantum Long Short Term Memory (QLSTM)": {
        "name": "QLSTM",
        "short_name": "QLSTM",
        "without_noise_file": "files/QLSTM_forecast - QLSTM_forecast.csv",
        "noise_folder": "files/temperaturenoise_data/{error_type}/QLSTM_{error_type}.csv"
    },
     "Quantum Support Vector Machine (QSVM)": {
        "name": "QSVM",
        "short_name": "QSVM",
        "without_noise_file": "files/QSVM_forecast.csv",
        "noise_folder": "files/temperaturenoise_data/{error_type}/QSVM_{error_type}.csv"
    },
    "Variational Quantum Classifier (VQC)": {
        "name": "VQC",
        "short_name": "VQC",
        "without_noise_file": "files/VQC_forecast - VQC_forecast.csv",
        "noise_folder": "files/temperaturenoise_data/{error_type}/VQC_{error_type}.csv"
    },
}

NOISE_METRICS = {
    "Without Noise": {
        "QGRU": {
            "Mean Squared Error (MSE)": 0.5148015544,
            "Root Mean Squared Error (RMSE)": 0.7174967,
            "Mean Absolute Error (MAE)": 0.7058171975,
            "Mean Absolute Percentage Error (MAPE)": 0.06563023825,
            "R² Score": 0.8912701421,
            "Adjusted R²": 0.8912313704
        },
        "QNN_IS": {
            "Mean Squared Error (MSE)": 1.274808481,
            "Root Mean Squared Error (RMSE)": 1.12907417,
            "Mean Absolute Error (MAE)": 1.080676887,
            "Mean Absolute Percentage Error (MAPE)": 0.04455394308,
            "R² Score": 0.8745918045,
            "Adjusted R²": 0.87443039
        },
        "QNN_SE": {
            "Mean Squared Error (MSE)": 1.182737932,
            "Root Mean Squared Error (RMSE)": 1.087537554,
            "Mean Absolute Error (MAE)": 0.9784103794,
            "Mean Absolute Percentage Error (MAPE)": 0.05039208815,
            "R² Score": 0.8877785449,
            "Adjusted R²": 0.8877215659
        },
        "Hybrid_QNN": {
            "Mean Squared Error (MSE)": 1.261,
            "Root Mean Squared Error (RMSE)": 1.1229,
            "Mean Absolute Error (MAE)": 1.455,
            "Mean Absolute Percentage Error (MAPE)": 0.0458,
            "R² Score": 0.908,
            "Adjusted R²": 0.9067
        },
        "QLSTM": {
            "Mean Squared Error (MSE)": 0.3964716947,
            "Root Mean Squared Error (RMSE)": 0.6296599834,
            "Mean Absolute Error (MAE)": 0.5773612303,
            "Mean Absolute Percentage Error (MAPE)": 0.04739095426,
            "R² Score": 0.908704844,
            "Adjusted R²": 0.9086828532
        },
        "QSVM": {
            "Mean Squared Error (MSE)": 1.555231881,
            "Root Mean Squared Error (RMSE)": 1.247089364,
            "Mean Absolute Error (MAE)": 1.411327942,
            "Mean Absolute Percentage Error (MAPE)": 0.05093823265,
            "R² Score": 0.8584812319,
            "Adjusted R²": 0.8584063078
        },
        "VQC": {
            "Mean Squared Error (MSE)": 1.331936334,
            "Root Mean Squared Error (RMSE)": 1.154095461,
            "Mean Absolute Error (MAE)": 1.308312858,
            "Mean Absolute Percentage Error (MAPE)": 0.04250832392,
            "R² Score": 0.8692373539,
            "Adjusted R²": 0.869175596
        },

    },
    "Gate Rotation Error": {
        "QGRU": {
            "Mean Squared Error (MSE)": 1.069,
            "Root Mean Squared Error (RMSE)": 1.034,
            "Mean Absolute Error (MAE)": 1.234,
            "Mean Absolute Percentage Error (MAPE)": 0.097,
            "R² Score": 0.862,
            "Adjusted R²": 0.862
        },
        "QNN_IS": {
            "Mean Squared Error (MSE)": 1.53118403048678,
            "Root Mean Squared Error (RMSE)": 1.2374102110807,
            "Mean Absolute Error (MAE)": 1.3557323685167,
            "Mean Absolute Percentage Error (MAPE)": 0.05912146463153,
            "R² Score": 0.855339693587321,
            "Adjusted R²": 0.855265927991622
        },
        "QNN_SE": {
            "Mean Squared Error (MSE)": 1.62521467500854,
            "Root Mean Squared Error (RMSE)": 1.2748390780834,
            "Mean Absolute Error (MAE)": 1.11531947884344,
            "Mean Absolute Percentage Error (MAPE)": 0.0625334565686961,
            "R² Score": 0.861982981566162,
            "Adjusted R²": 0.861904685994727
        },
        "Hybrid_QNN": {
            "Mean Squared Error (MSE)": 1.3621,
            "Root Mean Squared Error (RMSE)":1.167 ,
            "Mean Absolute Error (MAE)": 1.521,
            "Mean Absolute Percentage Error (MAPE)": 0.053,
            "R² Score": 0.879,
            "Adjusted R²": 0.876
        },
        "QLSTM": {
            "Mean Squared Error (MSE)": 1.5359,
            "Root Mean Squared Error (RMSE)": 1.2393143265531954,
            "Mean Absolute Error (MAE)": 1.3291,
            "Mean Absolute Percentage Error (MAPE)": 0.052941,
            "R² Score":0.8717,
            "Adjusted R²": 0.8715268556005399
        },
        "QSVM": {
            "Mean Squared Error (MSE)": 4.559233425741876,
            "Root Mean Squared Error (RMSE)": 2.1352361522187366,
            "Mean Absolute Error (MAE)": 1.7229808675917355,
            "Mean Absolute Percentage Error (MAPE)":0.05559940926026863 ,
            "R² Score": 0.83724419070727,
            "Adjusted R²": 0.8370245472399384
        },
        "VQC": {
            "Mean Squared Error (MSE)": 4.29733,
            "Root Mean Squared Error (RMSE)":2.073,
            "Mean Absolute Error (MAE)":1.95 ,
            "Mean Absolute Percentage Error (MAPE)": 0.0525,
            "R² Score": 0.689,
            "Adjusted R²": 0.687
        },
        
    },
    "Amplitude Damping Error": {
        # ✅ Add metrics here when you process the new files
        "QGRU": {
            "Mean Squared Error (MSE)": 0.88,  # Replace with actual values
            "Root Mean Squared Error (RMSE)": 0.938,
            "Mean Absolute Error (MAE)": 0.947,
            "Mean Absolute Percentage Error (MAPE)": 0.084,
            "R² Score": 0.879,
            "Adjusted R²": 0.879
        },
        "QNN_IS": {
            "Mean Squared Error (MSE)": 1.45245580185677,
            "Root Mean Squared Error (RMSE)": 1.20517874270034,
            "Mean Absolute Error (MAE)": 1.24725458501829,
            "Mean Absolute Percentage Error (MAPE)":0.0623750361999526,
            "R² Score": 0.868150138977661,
            "Adjusted R²": 0.868080166155768
        },
        "QNN_SE": {
            "Mean Squared Error (MSE)": 1.46700577043147,
            "Root Mean Squared Error (RMSE)": 1.21120013640664,
            "Mean Absolute Error (MAE)": 1.2647143497032,
            "Mean Absolute Percentage Error (MAPE)": 0.0749324157616123,
            "R² Score": 0.877630733259763,
            "Adjusted R²": 0.877560059485485
        },
        "QLSTM": {
            "Mean Squared Error (MSE)": 1.1359,
            "Root Mean Squared Error (RMSE)": 1.0657860948614408,
            "Mean Absolute Error (MAE)": 1.1291,
            "Mean Absolute Percentage Error (MAPE)": 0.042941,
            "R² Score":0.8817,
            "Adjusted R²": 0.8815403508771931
        },
        "QSVM": {
            "Mean Squared Error (MSE)": 3.7766025515378248,
            "Root Mean Squared Error (RMSE)": 1.943348283642905,
            "Mean Absolute Error (MAE)": 1.5666706909612247,
            "Mean Absolute Percentage Error (MAPE)": 0.05059174425360869,
            "R² Score": 0.8651825982012513,
            "Adjusted R²": 0.8650006583877577
        },
        "VQC": {
            "Mean Squared Error (MSE)": 4.55396,
            "Root Mean Squared Error (RMSE)": 2.134,
            "Mean Absolute Error (MAE)": 2.05,
            "Mean Absolute Percentage Error (MAPE)": 0.0575,
            "R² Score": 0.675,
            "Adjusted R²": 0.673
        },
         "Hybrid_QNN": {
            "Mean Squared Error (MSE)":  1.372,
            "Root Mean Squared Error (RMSE)": 1.1713,
            "Mean Absolute Error (MAE)":  1.4713,
            "Mean Absolute Percentage Error (MAPE)": 0.0467,
            "R² Score": 0.891,
            "Adjusted R²": 0.8921
        },
        
    },
    "Initialization Error":{
        "Hybrid_QNN": {
            "Mean Squared Error (MSE)": 1.312 ,
            "Root Mean Squared Error (RMSE)": 1.145,
            "Mean Absolute Error (MAE)": 1.49 ,
            "Mean Absolute Percentage Error (MAPE)": 0.049,
            "R² Score": 0.891,
            "Adjusted R²": 0.8923 
        },
        "QSVM": {
            "Mean Squared Error (MSE)": 4.585199813666629,
            "Root Mean Squared Error (RMSE)": 2.1413079679641203,
            "Mean Absolute Error (MAE)": 1.7278755782963302,
            "Mean Absolute Percentage Error (MAPE)": 0.0557577778437997,
            "R² Score":0.8363172409140787,
            "Adjusted R²": 0.8360963465023568
        },
        "QLSTM": {
            "Mean Squared Error (MSE)": 1.7128,
            "Root Mean Squared Error (RMSE)": 1.308739851918631,
            "Mean Absolute Error (MAE)": 1.3912,
            "Mean Absolute Percentage Error (MAPE)": 0.051341,
            "R² Score": 0.8669,
            "Adjusted R²": 0.8667203778677464
        },
        "QNN_IS": {
            "Mean Squared Error (MSE)": 1.653,
            "Root Mean Squared Error (RMSE)": 1.285,
            "Mean Absolute Error (MAE)": 1.481,
            "Mean Absolute Percentage Error (MAPE)":0.052,
            "R² Score":0.8591,
            "Adjusted R²": 0.8597
        },
        "QNN_SE": {
            "Mean Squared Error (MSE)": 1.751,
            "Root Mean Squared Error (RMSE)": 1.323,
            "Mean Absolute Error (MAE)":1.312,
            "Mean Absolute Percentage Error (MAPE)": 0.064,
            "R² Score": 0.8551,
            "Adjusted R²": 0.8557
        },
        "QGRU": {
            "Mean Squared Error (MSE)": 1.3,  # Replace with actual values
            "Root Mean Squared Error (RMSE)": 1.14,
            "Mean Absolute Error (MAE)": 1.4,
            "Mean Absolute Percentage Error (MAPE)": 0.11,
            "R² Score": 0.845,
            "Adjusted R²":0.844
        },
        "VQC": {
            "Mean Squared Error (MSE)": 4.4016,
            "Root Mean Squared Error (RMSE)": 2.098,
            "Mean Absolute Error (MAE)": 2.0,
            "Mean Absolute Percentage Error (MAPE)":5.5,
            "R² Score": 0.672,
            "Adjusted R²": 0.67
        },
    },
    "Thermal Relaxation Error":{
        "QLSTM": {
            "Mean Squared Error (MSE)": 1.2997,
            "Root Mean Squared Error (RMSE)": 1.140043858805441,
            "Mean Absolute Error (MAE)": 1.2471,
            "Mean Absolute Percentage Error (MAPE)": 0.04368,
            "R² Score": 0.8829,
            "Adjusted R²": 0.8827419703103914
        },
        "QSVM": {
            "Mean Squared Error (MSE)": 3.418089319851106,
            "Root Mean Squared Error (RMSE)": 1.8488075399703199,
            "Mean Absolute Error (MAE)": 1.4903954270958897,
            "Mean Absolute Percentage Error (MAPE)": 0.04813030555771635,
            "R² Score": 0.8779808267007779,
            "Adjusted R²": 0.8778161584507115
        },
        "VQC": {
            "Mean Squared Error (MSE)": 4.8488,
            "Root Mean Squared Error (RMSE)": 2.202,
            "Mean Absolute Error (MAE)": 2.15,
            "Mean Absolute Percentage Error (MAPE)":0.062,
            "R² Score": 0.66,
            "Adjusted R²": 0.658
        },
        "QNN_SE": {
            "Mean Squared Error (MSE)": 1.4127,
            "Root Mean Squared Error (RMSE)": 1.1885,
            "Mean Absolute Error (MAE)": 1.2736,
            "Mean Absolute Percentage Error (MAPE)":0.0542,
            "R² Score": 0.8901,
            "Adjusted R²": 0.8912
        },
        "QNN_IS": {
            "Mean Squared Error (MSE)": 1.4482,
            "Root Mean Squared Error (RMSE)": 1.2034,
            "Mean Absolute Error (MAE)": 1.3841,
            "Mean Absolute Percentage Error (MAPE)": 0.0478,
            "R² Score": 0.8802,
            "Adjusted R²": 0.8819
        },
        "Hybrid_QNN": {
            "Mean Squared Error (MSE)":  1.413,
            "Root Mean Squared Error (RMSE)": 1.1886,
            "Mean Absolute Error (MAE)":  1.4945,
            "Mean Absolute Percentage Error (MAPE)": 0.0484,
            "R² Score": 0.8874,
            "Adjusted R²": 0.8871
        },
        "QGRU": {
            "Mean Squared Error (MSE)": 1.05,  # Replace with actual values
            "Root Mean Squared Error (RMSE)": 1.025,
            "Mean Absolute Error (MAE)": 1.2,
            "Mean Absolute Percentage Error (MAPE)":0.09,
            "R² Score": 0.87,
            "Adjusted R²": 0.869
        },
    },
     "Depolarizing Error":{
        "QLSTM": {
            "Mean Squared Error (MSE)": 1.5128,
            "Root Mean Squared Error (RMSE)": 1.229959349,
            "Mean Absolute Error (MAE)": 1.2912,
            "Mean Absolute Percentage Error (MAPE)": 0.053341,
            "R² Score":0.8769,
            "Adjusted R²":0.8767338731
        },
        "Hybrid_QNN": {
            "Mean Squared Error (MSE)": 1.5493 ,
            "Root Mean Squared Error (RMSE)": 1.2447,
            "Mean Absolute Error (MAE)": 1.537,
            "Mean Absolute Percentage Error (MAPE)": 0.0472,
            "R² Score":0.8851,
            "Adjusted R²":0.8812
        },
        "QSVM": {
            "Mean Squared Error (MSE)": 4.08575916190733,
            "Root Mean Squared Error (RMSE)": 2.0213260899487073,
            "Mean Absolute Error (MAE)": 1.6295624339033778,
            "Mean Absolute Percentage Error (MAPE)": 0.052621681043822255,
            "R² Score": 0.8541463055572311,
            "Adjusted R²": 0.853949471961492
        },
        "VQC": {
            "Mean Squared Error (MSE)": 5.1529,
            "Root Mean Squared Error (RMSE)": 2.27,
            "Mean Absolute Error (MAE)": 2.3,
            "Mean Absolute Percentage Error (MAPE)":0.0675,
            "R² Score": 0.645,
            "Adjusted R²": 0.643
        },
        "QNN_IS": {
            "Mean Squared Error (MSE)": 1.6213,
            "Root Mean Squared Error (RMSE)": 1.2733,
            "Mean Absolute Error (MAE)": 1.476,
            "Mean Absolute Percentage Error (MAPE)":0.04972,
            "R² Score": 0.8623,
            "Adjusted R²": 0.8614
        },
        "QNN_SE": {
            "Mean Squared Error (MSE)": 1.7203,
            "Root Mean Squared Error (RMSE)": 1.3116,
            "Mean Absolute Error (MAE)":1.351,
            "Mean Absolute Percentage Error (MAPE)": 0.0653,
            "R² Score": 0.8691,
            "Adjusted R²": 0.8638
        },
        "QGRU": {
            "Mean Squared Error (MSE)": 1.2,  # Replace with actual values
            "Root Mean Squared Error (RMSE)": 1.095,
            "Mean Absolute Error (MAE)": 1.3,
            "Mean Absolute Percentage Error (MAPE)":0.102,
            "R² Score": 0.855,
            "Adjusted R²": 0.854
        },

    },
    "Readout Error":{
        "QNN_IS": {
            "Mean Squared Error (MSE)":1.4521 ,
            "Root Mean Squared Error (RMSE)": 1.205,
            "Mean Absolute Error (MAE)": 1.213,
            "Mean Absolute Percentage Error (MAPE)":0.0571,
            "R² Score": 0.8591,
            "Adjusted R²": 0.8514
        },
        "QNN_SE": {
            "Mean Squared Error (MSE)": 1.3549,
            "Root Mean Squared Error (RMSE)": 1.164,
            "Mean Absolute Error (MAE)": 1.2137,
            "Mean Absolute Percentage Error (MAPE)": 0.0627,
            "R² Score": 0.8617,
            "Adjusted R²": 0.8651
        },
        "Hybrid_QNN": {
            "Mean Squared Error (MSE)": 1.4712,
            "Root Mean Squared Error (RMSE)": 1.2129,
            "Mean Absolute Error (MAE)":1.5914,
            "Mean Absolute Percentage Error (MAPE)": 0.0475,
            "R² Score":0.8914,
            "Adjusted R²":0.8819
        },
        "QSVM": {
            "Mean Squared Error (MSE)": 4.567894878945117,
            "Root Mean Squared Error (RMSE)": 2.137263408881815,
            "Mean Absolute Error (MAE)": 1.7246184157753377,
            "Mean Absolute Percentage Error (MAPE)":0.055652157139780565 ,
            "R² Score": 0.836934993591416,
            "Adjusted R²": 0.8367149328540224
        },
        "QLSTM": {
            "Mean Squared Error (MSE)": 2.5,
            "Root Mean Squared Error (RMSE)": 1.5811388300841898,
            "Mean Absolute Error (MAE)": 1.8,
            "Mean Absolute Percentage Error (MAPE)": 0.079,
            "R² Score": 0.835,
            "Adjusted R²": 0.8347773279352226
        },
        "QGRU": {
            "Mean Squared Error (MSE)": 0.65,  # Replace with actual values
            "Root Mean Squared Error (RMSE)": 0.806,
            "Mean Absolute Error (MAE)": 0.85,
            "Mean Absolute Percentage Error (MAPE)": 0.078,
            "R² Score": 0.89,
            "Adjusted R²": 0.889
        },
        "VQC": {
            "Mean Squared Error (MSE)": 5.7504,
            "Root Mean Squared Error (RMSE)": 2.398,
            "Mean Absolute Error (MAE)": 2.55,
            "Mean Absolute Percentage Error (MAPE)":7.9,
            "R² Score": 0.615,
            "Adjusted R²": 0.613
        },


    },
    "Dephasing Error":{
        "QNN_IS": {
            "Mean Squared Error (MSE)":1.451,
            "Root Mean Squared Error (RMSE)": 1.2045,
            "Mean Absolute Error (MAE)": 1.381,
            "Mean Absolute Percentage Error (MAPE)":0.0472,
            "R² Score": 0.8771,
            "Adjusted R²": 0.871
        },
        "QNN_SE": {
            "Mean Squared Error (MSE)": 1.571,
            "Root Mean Squared Error (RMSE)":1.2533 ,
            "Mean Absolute Error (MAE)": 1.239,
            "Mean Absolute Percentage Error (MAPE)": 0.0627,
            "R² Score": 0.8912,
            "Adjusted R²": 0.8917
        },
        "Hybrid_QNN": {
            "Mean Squared Error (MSE)": 1.5819,
            "Root Mean Squared Error (RMSE)": 1.257,
            "Mean Absolute Error (MAE)":1.5937,
            "Mean Absolute Percentage Error (MAPE)": 0.0491,
            "R² Score":0.8817,
            "Adjusted R²":0.882
        },
        "VQC": {
            "Mean Squared Error (MSE)": 5.44756,
            "Root Mean Squared Error (RMSE)": 2.334,
            "Mean Absolute Error (MAE)": 2.4,
            "Mean Absolute Percentage Error (MAPE)":0.073,
            "R² Score": 0.63,
            "Adjusted R²": 0.628
        },
        "QSVM": {
            "Mean Squared Error (MSE)": 4.246835002184547,
            "Root Mean Squared Error (RMSE)": 2.0607850451186187,
            "Mean Absolute Error (MAE)": 1.6628789228091803,
            "Mean Absolute Percentage Error (MAPE)": 0.05366097512893546,
            "R² Score": 0.8483962098078434,
            "Adjusted R²": 0.8481916162988121
        },
        "QLSTM": {
            "Mean Squared Error (MSE)": 2.35,
            "Root Mean Squared Error (RMSE)": 1.5329709716755893,
            "Mean Absolute Error (MAE)": 1.72,
            "Mean Absolute Percentage Error (MAPE)": 0.073,
            "R² Score":0.841,
            "Adjusted R²":0.8407854251012146
        },
        "QGRU": {
            "Mean Squared Error (MSE)": 0.75,  # Replace with actual values
            "Root Mean Squared Error (RMSE)": 0.866,
            "Mean Absolute Error (MAE)": 0.9,
            "Mean Absolute Percentage Error (MAPE)": 0.080,
            "R² Score": 0.885,
            "Adjusted R²": 0.884
        },

    }
# Add more error types as you receive data
}

#Rain Noise Analysis Constant 
# Available noise types for rainfall (same as temperature)
RAIN_NOISE_TYPES = [
    "Without Noise",
    "Depolarizing Error",
    "Dephasing Error",
    "Amplitude Damping Error",
    "Thermal Relaxation Error",
    "Readout Error",
    "Initialization Error",
    "Gate Rotation Error"
]

# Also add for rainfall if you have it
RAIN_NOISE_TYPE_TO_FOLDER = {
    "Without Noise": "WithoutNoise",
    "Depolarizing Error": "DepolarizingError",
    "Dephasing Error": "DephasingError",
    "Amplitude Damping Error": "AmplitudeDampingError",
    "Thermal Relaxation Error": "ThermalRelaxationError",
    "Readout Error": "ReadoutError",
    "Initialization Error": "InitializationError",
    "Gate Rotation Error": "GateRotationError"  # ✅ Matches your folder name
}

# Quantum algorithms available for rain noise analysis
RAIN_NOISE_QUANTUM_ALGORITHMS = {
    "Select Quantum Algorithm":{"name":"Select Quantum ALgorithm","short_name":""},
    "Quantum Gated Recurrent Unit (QGRU)":{
        "name":"QGRU",
        "short_name":"QGRU",
        "without_noise_file": "files/rainfall_data/QGRU_predictions_Aug2025.csv",
        "noise_folder":"files/rain_noise_data/{error_type}/QGRU_{error_type}.csv"
    },
    "Quantum Neural Network with Ising Layers (QNN_IS)":{
        "name":"QNN_IS",
        "short_name":"QNN_IS",
        "without_noise_file": "files/rainfall_data/QNNIS_predictions_Aug2025.csv",
        "noise_folder":"files/rain_noise_data/{error_type}/QNN_IS_{error_type}.csv"
    },
    "Quantum Neural Network with Strong Entangling Layers(QNN_SE)":{
        "name":"QGRU",
        "short_name":"QGRU",
        "without_noise_file": "files/rainfall_data/QNNSE_predictions_Aug2025.csv",
        "noise_folder":"files/rain_noise_data/{error_type}/QNN-SE_{error_type}.csv"
    }
}
# Rain noise classification metrics (confusion metrix values)
RAIN_NOISE_CLASSIFICATION_METRICS = {
    "Without Noise":{
        "ANN": {
            "True Negatives (TN)":437,
            "False Positives (FP)":30,
            "False Negatives (FN)": 50,
            "True Positives (TP)": 225,
            "Accuracy": 0.8921832884097035,
            "Precision (No Rain)": 0.8973305954825462,
            "Recall (No Rain)": 0.9357601713062098,
            "F1-Score (No Rain)":0.9161425576519916 ,
            "Precision (Rain)": 0.8823529411764706,
            "Recall (Rain)": 0.8181818181818182,
            "F1-Score (Rain)": 0.8490566037735849,
            "Support (No Rain)": 467.0,
            "Support (Rain)":275.0 
        },
        "LSTM": {
            "True Negatives (TN)":425,
            "False Positives (FP)":42,
            "False Negatives (FN)": 73,
            "True Positives (TP)": 202,
            "Accuracy": 0.8450134771,
            "Precision (No Rain)": 0.8534136546,
            "Recall (No Rain)": 0.9100642398,
            "F1-Score (No Rain)": 0.8808290155,
            "Precision (Rain)":0.8278688525,
            "Recall (Rain)": 0.7345454545,
            "F1-Score (Rain)": 0.7784200385,
            "Support (No Rain)": 467,
            "Support (Rain)": 275
        },
        "GRU": {
            "True Negatives (TN)":424,
            "False Positives (FP)":43,
            "False Negatives (FN)":74 ,
            "True Positives (TP)": 201,
            "Accuracy": 0.8423180593,
            "Precision (No Rain)": 0.8514056225,
            "Recall (No Rain)": 0.9079229122,
            "F1-Score (No Rain)": 0.8787564767,
            "Precision (Rain)": 0.8237704918,
            "Recall (Rain)": 0.7309090909,
            "F1-Score (Rain)": 0.774566474,
            "Support (No Rain)": 467,
            "Support (Rain)": 275
        },
        "SVM": {
            "True Negatives (TN)": 439,
            "False Positives (FP)": 28,
            "False Negatives (FN)": 47,
            "True Positives (TP)": 228,
            "Accuracy": 0.898921832884097,
            "Precision (No Rain)": 0.9032921810699589,
            "Recall (No Rain)": 0.9400428265524625,
            "F1-Score (No Rain)": 0.9213011542497377,
            "Precision (Rain)": 0.890625,
            "Recall (Rain)": 0.8290909090909091,
            "F1-Score (Rain)": 0.8587570621468926,
            "Support (No Rain)": 467,
            "Support (Rain)": 275
        },
        "QNN_IS": {
            "True Negatives (TN)": 427,  
            "False Positives (FP)": 40,   
            "False Negatives (FN)": 68,   
            "True Positives (TP)": 207,   
            "Accuracy": 0.8544474393530997,
            "Precision (No Rain)": 0.8626262626262626,
            "Recall (No Rain)": 0.9143468950749465,
            "F1-Score (No Rain)": 0.8877338877338877,
            "Precision (Rain)": 0.8380566801619433,
            "Recall (Rain)": 0.7527272727272727,
            "F1-Score (Rain)": 0.7931034482758621,
            "Support (No Rain)":467,
            "Support (Rain)": 275
        },
        "QNN_SE": {
            "True Negatives (TN)":432 ,  
            "False Positives (FP)": 35,   
            "False Negatives (FN)": 61,   
            "True Positives (TP)": 214,   
            "Accuracy": 0.860619946091644,
            "Precision (No Rain)": 0.866267748478701,
            "Recall (No Rain)": 0.925053533190578,
            "F1-Score (No Rain)": 0.9,
            "Precision (Rain)": 0.859437751004016,
            "Recall (Rain)":0.778181818181818,
            "F1-Score (Rain)": 0.816793893129771,
            "Support (No Rain)":467,
            "Support (Rain)":275 
        },
        "QLSTM": {
            "True Negatives (TN)": 415,  
            "False Positives (FP)": 52,   
            "False Negatives (FN)": 89,   
            "True Positives (TP)": 186,   
            "Accuracy": 0.8099730458,
            "Precision (No Rain)": 0.8234126984,
            "Recall (No Rain)": 0.8886509636,
            "F1-Score (No Rain)": 0.8547888774,
            "Precision (Rain)": 0.781512605,
            "Recall (Rain)":0.6763636364,
            "F1-Score (Rain)":0.7251461988,
            "Support (No Rain)":467,
            "Support (Rain)":275 
        },
        "QGRU": {
            "True Negatives (TN)":413,  
            "False Positives (FP)": 54,   
            "False Negatives (FN)": 93,   
            "True Positives (TP)": 182,   
            "Accuracy": 0.8018867925,
            "Precision (No Rain)":0.8162055336,
            "Recall (No Rain)": 0.8843683084,
            "F1-Score (No Rain)": 0.8489208633,
            "Precision (Rain)": 0.7711864407,
            "Recall (Rain)":0.6618181818,
            "F1-Score (Rain)": 0.7123287671,
            "Support (No Rain)":467,
            "Support (Rain)": 275 
        },
        "VQC": {
            "True Negatives (TN)": 425,  
            "False Positives (FP)": 42,   
            "False Negatives (FN)": 72,   
            "True Positives (TP)": 203,   
            "Accuracy": 0.8463611859838275,
            "Precision (No Rain)": 0.8551307847082495,
            "Recall (No Rain)": 0.9100642398286938,
            "F1-Score (No Rain)": 0.8817427385892116,
            "Precision (Rain)": 0.8285714285714286,
            "Recall (Rain)":0.7381818181818182,
            "F1-Score (Rain)": 0.7807692307692308,
            "Support (No Rain)":467,
            "Support (Rain)": 275
        },
        "QSVM": {
            "True Negatives (TN)": 422,
            "False Positives (FP)": 45,
            "False Negatives (FN)": 78,
            "True Positives (TP)": 197,
            "Accuracy": 0.8342318059299192,
            "Precision (No Rain)": 0.844,
            "Recall (No Rain)":0.9036402569593148,
            "F1-Score (No Rain)": 0.8728024819027922,
            "Precision (Rain)": 0.8140495867768595,
            "Recall (Rain)": 0.7163636363636363,
            "F1-Score (Rain)": 0.7620889748549323,
            "Support (No Rain)":467 ,
            "Support (Rain)": 275
        },
        "Hybrid QNN": {
            "True Negatives (TN)": 419,
            "False Positives (FP)": 48,
            "False Negatives (FN)": 39,
            "True Positives (TP)": 236,
            "Accuracy": 0.8827,
            "Precision (No Rain)":0.9148 ,
            "Recall (No Rain)":0.8972,
            "F1-Score (No Rain)": 0.9059,
            "Precision (Rain)": 0.831,
            "Recall (Rain)": 0.8582,
            "F1-Score (Rain)": 0.8444,
            "Support (No Rain)":467,
            "Support (Rain)": 275
        },
        "Dense ANN": {
            "True Negatives (TN)": 426,
            "False Positives (FP)": 41,
            "False Negatives (FN)": 20,
            "True Positives (TP)": 255,
            "Accuracy": 0.917,
            "Precision (No Rain)": 0.9552,
            "Recall (No Rain)":0.9122,
            "F1-Score (No Rain)":0.9332 ,
            "Precision (Rain)":0.8615,
            "Recall (Rain)": 0.9273,
            "F1-Score (Rain)":0.8932,
            "Support (No Rain)": 467,
            "Support (Rain)": 275
        }
    },
    "Gate Rotation Error":{
        "QGRU":{
            "True Negatives (TN)": 401,
            "False Positives (FP)": 66,
            "False Negatives (FN)":112,
            "True Positives (TP)": 163,
            "Accuracy": 0.76010781671159,
            "Precision (No Rain)": 0.781676413255361,
            "Recall (No Rain)": 0.858672376873662,
            "F1-Score (No Rain)": 0.818367346938776,
            "Precision (Rain)": 0.7117903930131,
            "Recall (Rain)": 0.592727272727273,
            "F1-Score (Rain)": 0.646825396825397,
            "Support (No Rain)": 467,
            "Support (Rain)": 275
        },
        "QNN_IS":{
            "True Negatives (TN)": 420,
            "False Positives (FP)": 47,
            "False Negatives (FN)": 79,
            "True Positives (TP)": 196,
            "Accuracy": 0.830188679245283,
            "Precision (No Rain)": 0.841683366733467,
            "Recall (No Rain)": 0.899357601713062,
            "F1-Score (No Rain)": 0.869565217391304,
            "Precision (Rain)": 0.806584362139918,
            "Recall (Rain)": 0.712727272727273,
            "F1-Score (Rain)":0.756756756756757,
            "Support (No Rain)": 467,
            "Support (Rain)": 275
        },
        "QNN_SE":{
            "True Negatives (TN)": 422,
            "False Positives (FP)": 45,
            "False Negatives (FN)":78,
            "True Positives (TP)": 197,
            "Accuracy": 0.824231805929919,
            "Precision (No Rain)": 0.844,
            "Recall (No Rain)": 0.903640256959315,
            "F1-Score (No Rain)": 0.872802481902792,
            "Precision (Rain)": 0.81404958677686,
            "Recall (Rain)": 0.716363636363636,
            "F1-Score (Rain)":0.762088974854932,
            "Support (No Rain)": 467,
            "Support (Rain)": 275
        },

    }
}

############ NCMRWF Data Source start from here 

NCMRWF_CLASSICAL_ALGORITHMS = {
    "Select Quantum Algorithm": {"name": "Select Quantum Algorithm", "file":""},
    "Gated Recurrent Unit (GRU)":{
        "name": "GRU (Gated Recurrent Unit)",
        # "file": "files/NCMRWF_TemperatureData/predictions_gru_1.csv",
        "file": "files/NCMRWF_TemperatureData/predictions_gru_v2_rect (1).csv",
        "pred_col": "GRU_Pred",
        "actual_col": "Actual"
    },
    "Long Short Term Memory (LSTM)":{
        "name": "LSTM (Long Short-Term Memory)",
        # "file": "files/NCMRWF_TemperatureData/predictions_gru_1.csv",
        "file": "files/NCMRWF_TemperatureData/predictions_classical_lstm_v1_rect.csv",
        "pred_col": "LSTM_Pred",
        "actual_col": "Actual"
    },
    "Artificial Neural Network (ANN)":{
        "name":"ANN (Artificial Neural Network)",
        # "file": "files/NCMRWF_TemperatureData/predictions_qgru_v2.csv",
        "file": "files/NCMRWF_TemperatureData/ANN_ncmrwf_data.csv",
        "pred_col": "ANN_Pred",
        "actual_col":"Actual"
    },

}

NCMRWF_QUANTUM_ALGORITHMS = {
    "Select Quantum Algorithm": {"name": "Select Quantum Algorithm", "file":""},
    "Quantum Gated Recurrent Unit (QGRU)":{
        "name": "QGRU (Quantum GRU)",
        # "file": "files/NCMRWF_TemperatureData/predictions_qgru_v2.csv",
        "file": "files/NCMRWF_TemperatureData/predictions_qgru_v1_rect (5).csv",
        "pred_col": "QGRU_Pred",
        "actual_col":"Actual"
    },
    

    "Quantum Long Short Term Memory (QLSTM)":{
        "name": "QLSTM (Quantum LSTM)",
        # "file": "files/NCMRWF_TemperatureData/predictions_qgru_v2.csv",
        "file": "files/NCMRWF_TemperatureData/predictions_qlstm_v1_rect.csv",
        "pred_col": "QLSTM_Pred",
        "actual_col":"Actual"
    },
    # "Quantum Neural Network with Ising Layers (QNN_IS)":{
    #     "name": "QNN_IS",
    #     # "file": "files/NCMRWF_TemperatureData/predictions_qgru_v2.csv",
    #     "file": "files/NCMRWF_TemperatureData/predictions_QNNIS.csv",
    #     "pred_col": "QNNIS_Pred",
    #     "actual_col":"Actual"
    # },
    "Quantum Neural Network with Ising Layers version 2.0(QNN_IS_2.0)":{
        "name": "QNN_IS_2.0",
        # "file": "files/NCMRWF_TemperatureData/predictions_qgru_v2.csv",
        "file": "files/NCMRWF_TemperatureData/predictions_qnn_ising_HYBRID_RECT.csv",
        "pred_col": "HybridQNNIS_Pred",
        "actual_col":"Actual"
    },
    "Hybrid Quantum Neural Network with Strong Entangling Layers (Hybrid QNN_SE)": {
        "name": "Hybrid QNN_SE",
        # "file": "files/NCMRWF_TemperatureData/predictions_qgru_v2.csv",
        "file": "files/NCMRWF_TemperatureData/Hybrid QNN-SE_ncmrwf_data.csv",
        "pred_col": "HybridQNNSE_Pred",
        "actual_col":"Actual"
    },
     "Variational Quantum Classifier (VQC)": {
        "name": "VQC", 
        "file": "files/NCMRWF_TemperatureData/test_predictions_vqc_linear_rect.csv",
        # D:\QML_UI\QML\weather_prediction_of_all_doing_changes\files\NCMRWF_TemperatureData\test_predictions_vqc_linear_rect.csv
        "pred_col": "VQC_Pred",
        "actual_col":"Actual",
        "date_col": "Datetime"  # ← Add this
        },
    # "Quantum Support Vector Machine (QSVM)": {
    #     "name": "QSVM",
    #     "file": "files/NCMRWF_TemperatureData/QSVM_Forecast.csv",
    #     "pred_col": "QSVM_Pred",
    #     "actual_col":"Actual"
    # },

    
}

NCMRWF_REGRESSION_METRICS = {
    
    "GRU": {
        "Mean Squared Error (MSE)": 2.8159186840057373,
        "Root Mean Squared Error (RMSE)": 1.678069928222819,
        "Mean Absolute Error (MAE)": 1.386562705039978,
        "Mean Absolute Percentage Error (MAPE)": 0.4750686585903168,
        "R² Score": 0.9322474002838135
    },
     "ANN": {
        "Mean Squared Error (MSE)": 5.8854,
        "Root Mean Squared Error (RMSE)": 2.426,
        "Mean Absolute Error (MAE)": 1.13192,
        "Mean Absolute Percentage Error (MAPE)": 0.069,
        "R² Score": 0.8584,
        "Adjusted R²": 0.8586
    },
    "QGRU": {
        "Mean Squared Error (MSE)": 2.193955421447754,
        "Root Mean Squared Error (RMSE)":1.4812006688655504,
        "Mean Absolute Error (MAE)": 1.1450302600860596,
        "Mean Absolute Percentage Error (MAPE)":0.39287930727005005,
        "R² Score": 0.9472122192382812
    },
    "LSTM": {
        "Mean Squared Error (MSE)": 2.5972821712493896,
        "Root Mean Squared Error (RMSE)":1.611608566386202,
        "Mean Absolute Error (MAE)": 1.2182209491729736,
        "Mean Absolute Percentage Error (MAPE)":0.4173746407032013,
        "R² Score": 0.9375079274177551
    },
    "QLSTM": {
        "Mean Squared Error (MSE)": 2.248197078704834,
        "Root Mean Squared Error (RMSE)":1.4993989057968644,
        "Mean Absolute Error (MAE)":  1.1498159170150757,
        "Mean Absolute Percentage Error (MAPE)":0.39403560757637024,
        "R² Score": 0.9459071159362793
    },
    #  "QNN_IS": {
    #     "Mean Squared Error (MSE)": 2.2547693252563477,
    #     "Root Mean Squared Error (RMSE)":1.5015889335155437,
    #     "Mean Absolute Error (MAE)": 1.1814645528793335,
    #     "Mean Absolute Percentage Error (MAPE)":0.4051353335380554,
    #     "R² Score": 0.9457489848136902
    # },
    "QNN_IS_2.0": {
        "Mean Squared Error (MSE)": 2.314905,
        "Root Mean Squared Error (RMSE)":1.521481,
        "Mean Absolute Error (MAE)": 1.194824,
        "Mean Absolute Percentage Error (MAPE)":0.409614,
        "R² Score":0.944302
    },
    "Hybrid QNN_SE":{
        "Mean Squared Error (MSE)": 5.3038,
        "Root Mean Squared Error (RMSE)":2.303,
        "Mean Absolute Error (MAE)": 0.9192,
        "Mean Absolute Percentage Error (MAPE)":0.0591,
        "R² Score":0.8724
    },
    "VQC": {
        "Mean Squared Error (MSE)": 2.3655292987823486,
        "Root Mean Squared Error (RMSE)": 1.5380277301734024,
        "Mean Absolute Error (MAE)": 1.2462096214294434,
        "Mean Absolute Percentage Error (MAPE)": 0.42604827880859375,
        "R² Score": 0.9430840611457825,
        # "Adjusted R²": 
    },
    # "QSVM": {
    #     "Mean Squared Error (MSE)": 3.812139471011485,
    #     "Root Mean Squared Error (RMSE)": 1.9524700947803235,
    #     "Mean Absolute Error (MAE)": 1.5424860279632204,
    #     "Mean Absolute Percentage Error (MAPE)": 0.5240881338674699,
    #     "R² Score": 0.7471458582551938,
    #     # "Adjusted R²": 0.7453776474737616
    # },
}

NCMRWF_ALGORITHM_SHORT_NAMES = {
    "Gated Recurrent Unit (GRU)": "GRU",  # ✅ MATCHES key above
    "Artificial Neural Network (ANN)":"ANN",
    "Quantum Gated Recurrent Unit (QGRU)": "QGRU",  # ✅ MATCHES key above
    "Long Short Term Memory (LSTM)": "LSTM",  # ✅ MATCHES key above
    "Quantum Long Short Term Memory (QLSTM)": "QLSTM",  # ✅ MATCHES key above
    # "Quantum Neural Network with Ising Layers (QNN_IS)": "QNN_IS",
    "Quantum Neural Network with Ising Layers version 2.0(QNN_IS_2.0)":"QNN_IS_2.0",
    "Hybrid Quantum Neural Network with Strong Entangling Layers (Hybrid QNN_SE)": "Hybrid QNN_SE",
    "Variational Quantum Classifier (VQC)": "VQC",
    # "Quantum Support Vector Machine (QSVM)": "QSVM",

}

# ==================== NCMRWF TRAINING PARAMETERS & QUANTUM RESOURCES ====================

# Training Parameters for NCMRWF Models
NCMRWF_ALGORITHM_PARAMS = {
    'GRU': {'classical': 1649, 'quantum': 0, 'type': 'classical'},
    'ANN': {'classical': 1649, 'quantum': 0, 'type': 'classical'},
    'LSTM': {'classical': 2129, 'quantum': 0, 'type': 'classical'},
    'QGRU': {'classical': 0, 'quantum': 677, 'type': 'quantum'},
    'QLSTM': {'classical': 0, 'quantum': 877, 'type': 'quantum'},
    # 'QNN_IS': {'classical': 0, 'quantum': 444, 'type': 'quantum'},
    'QNN_IS_2.0': {'classical': 10409, 'quantum': 12, 'type': 'quantum'},
    "Hybrid QNN_SE" :{'classical': 11111, 'quantum': 8, 'type': 'quantum'},
    'VQC': {'classical': 10409, 'quantum': 12, 'type': 'quantum'}
    # "QSVM" :{'classical': 11111, 'quantum': 8, 'type': 'quantum'}

}
# Univariate Training Parameters for NCMRWF Models
NCMRWF_UNIVARIATE_ALGORITHM_PARAMS = {
    'GRU':  {'classical': 1649, 'quantum': 0, 'type': 'classical'},
    'LSTM': {'classical': 2129, 'quantum': 0, 'type': 'classical'},
    'QGRU': {'classical': 0, 'quantum': 497, 'type': 'quantum'},
    'QLSTM':{'classical': 0, 'quantum': 637, 'type': 'quantum'},
}
# Quantum Resource Data for NCMRWF Models
NCMRWF_QUANTUM_RESOURCE_DATA = {
    "algorithms": ['QGRU', 'QLSTM','QNN_IS_2.0','Hybrid QNN_SE','VQC'],
    "single_gate_count": [84, 64, 4,5,8],
    "multi_gate_count": [24, 16, 12,5,3],
    "depth": [15, 8, 13,5,5],
    "colors": ['#8B5CF6','#3B82F6','#F59E0B','#EF4444','#831843']
    #    "colors": ['#8B5CF6', '#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#6366F1', '#831843']
}
# ==================== NCMRWF UNIVARIATE ALGORITHMS ====================

NCMRWF_UNIVARIATE_CLASSICAL_ALGORITHMS = {
    "Select Classical Algorithm": {"name": "Select Classical Algorithm", "file": ""},
    "Gated Recurrent Unit (GRU)": {
        "name": "GRU (Gated Recurrent Unit)",
        "file": "files/NCMRWF_TemperatureData/temperature_gru_rectified.csv",
        "pred_col": "y_pred",        # ← CHANGE THIS (was 'GRU_Pred')
        "actual_col": "y_true"       # ← CHANGE THIS (was 'Actual')
    },
    "Long Short Term Memory (LSTM)": {
        "name": "LSTM (Long Short-Term Memory)",
        "file": "files/NCMRWF_TemperatureData/temperature_rectified_lstm.csv",
        
        "pred_col": "y_pred",        # ← CHANGE THIS (was 'LSTM_Pred')
        "actual_col": "y_true"       # ← CHANGE THIS (was 'Actual')
    },
}

NCMRWF_UNIVARIATE_QUANTUM_ALGORITHMS = {
    "Select Quantum Algorithm": {"name": "Select Quantum Algorithm", "file": ""},
    "Quantum Gated Recurrent Unit (QGRU)": {
        "name": "QGRU (Quantum GRU)",
        "file": "files/NCMRWF_TemperatureData/temperature_qgru_RECT_2.csv",
        "pred_col": "y_pred",        # ← CHANGE THIS (was 'QGRU_Pred')
        "actual_col": "y_true"       # ← CHANGE THIS (was 'Actual')
    },
    "Quantum Long Short Term Memory (QLSTM)": {
        "name": "QLSTM (Quantum LSTM)",
        "file": "files/NCMRWF_TemperatureData/ncmrwf_qlstm_univariate.csv",
       # C:\Users\es31-noida\Downloads\QML_UI\QML_UI\QML\weather_prediction_of_all_doing_changes\files\NCMRWF_TemperatureData\ncmrwf_qlstm_univariate.csv
        "pred_col": "y_pred",        # ← CHANGE THIS (was 'QLSTM_Pred')
        "actual_col": "y_true"       # ← CHANGE THIS (was 'Actual')
    },
}

# ==================== NCMRWF UNIVARIATE METRICS ====================
# These are separate from multivariate metrics
# Replace values below with your actual univariate model results

NCMRWF_UNIVARIATE_REGRESSION_METRICS = {
    "GRU": {
        "Mean Squared Error (MSE)": 1.419016361,
        "Root Mean Squared Error (RMSE)": 1.191224732,
        "Mean Absolute Error (MAE)": 0.92864114,
        "Mean Absolute Percentage Error (MAPE)": 0.318546504,
        "R² Score": 0.965857685
    },
    "LSTM": {
        "Mean Squared Error (MSE)": 1.636808157,
        "Root Mean Squared Error (RMSE)": 1.279378035,
        "Mean Absolute Error (MAE)": 1.034855366,
        "Mean Absolute Percentage Error (MAPE)": 0.354819357,
        "R² Score": 0.960617483
    },
    "QGRU": {
        "Mean Squared Error (MSE)": 1.178618312,
        "Root Mean Squared Error (RMSE)": 1.085641889,
        "Mean Absolute Error (MAE)": 0.833719134,
        "Mean Absolute Percentage Error (MAPE)": 0.285975486,
        "R² Score": 0.971641779
    },
    "QLSTM": {
        "Mean Squared Error (MSE)": 1.267688,
        "Root Mean Squared Error (RMSE)":1.1259166,
        "Mean Absolute Error (MAE)": 0.884024,
        "Mean Absolute Percentage Error (MAPE)":0.303183 ,
        "R² Score": 0.969499
    },
}

# Short name mapping for univariate algorithms
NCMRWF_UNIVARIATE_ALGORITHM_SHORT_NAMES = {
    "Gated Recurrent Unit (GRU)": "GRU",
    "Long Short Term Memory (LSTM)": "LSTM",
    "Quantum Gated Recurrent Unit (QGRU)": "QGRU",
    "Quantum Long Short Term Memory (QLSTM)": "QLSTM",
}