from networksecurity.entity.artifact_entity import ClassificationArtifact
from networksecurity.exception.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score

def get_classification_score(y_true,y_pred)->ClassificationArtifact:
    try:
        model_f1_score = f1_score(y_true,y_pred)
        model_precision_score = precision_score(y_true,y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        classification_artifact = ClassificationArtifact(
            f1_score=model_f1_score,
            precision=model_precision_score,
            recall=model_recall_score
        )
        return classification_artifact
    except Exception as e:
        raise NetworkSecurityException(e,sys)