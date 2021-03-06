import os, sys
sys.path.insert(0, os.path.abspath(".."))

import pandas as pd
import pytest
import pycaret.regression
import pycaret.datasets

def test():
    # loading dataset
    data = pycaret.datasets.get_data('boston')
    assert isinstance(data, pd.core.frame.DataFrame)

    # init setup
    reg1 = pycaret.regression.setup(data, target='medv',silent=True, log_experiment=True, html=False, session_id=123)
    assert isinstance(reg1, tuple)
    assert isinstance(reg1[0], pd.core.frame.DataFrame)
    assert isinstance(reg1[1], pd.core.series.Series)
    assert isinstance(reg1[2], pd.core.frame.DataFrame)
    assert isinstance(reg1[3], pd.core.frame.DataFrame)
    assert isinstance(reg1[4], pd.core.series.Series)
    assert isinstance(reg1[5], pd.core.series.Series)
    assert isinstance(reg1[6], int)
    assert isinstance(reg1[9], list)
    assert isinstance(reg1[10], bool)
    assert isinstance(reg1[11], int)
    assert isinstance(reg1[12], bool)
    assert isinstance(reg1[13], list)
    assert isinstance(reg1[14], list)
    assert isinstance(reg1[15], list)
    assert isinstance(reg1[16], str)
    assert isinstance(reg1[17], bool)
    assert isinstance(reg1[18], bool)
    assert isinstance(reg1[19], str)

    # compare models
    top3 = pycaret.regression.compare_models(n_select = 3, exclude = ['catboost'])
    assert isinstance(top3, list)

    # tune model
    tuned_top3 = [pycaret.regression.tune_model(i, n_iter=3) for i in top3]
    assert isinstance(tuned_top3, list)

    # ensemble model
    bagged_top3 = [pycaret.regression.ensemble_model(i) for i in tuned_top3]
    assert isinstance(bagged_top3, list)

    # blend models
    blender = pycaret.regression.blend_models(top3)

    # stack models
    stacker = pycaret.regression.stack_models(estimator_list = top3[1:], meta_model = top3[0])

    # select best model
    best = pycaret.regression.automl(optimize = 'MAPE')

    # hold out predictions
    predict_holdout = pycaret.regression.predict_model(best)
    assert isinstance(predict_holdout, pd.core.frame.DataFrame)

    # predictions on new dataset
    predict_holdout = pycaret.regression.predict_model(best, data=data)
    assert isinstance(predict_holdout, pd.core.frame.DataFrame)
    
    # finalize model
    final_best = pycaret.regression.finalize_model(best)

    # save model
    pycaret.regression.save_model(best, 'best_model_23122019')
 
    # load model
    saved_best = pycaret.regression.load_model('best_model_23122019')
    
    # returns table of models
    all_models = pycaret.regression.models()
    assert isinstance(all_models, pd.core.frame.DataFrame)

    # get config
    X_train = pycaret.regression.get_config('X_train')
    X_test = pycaret.regression.get_config('X_test')
    y_train = pycaret.regression.get_config('y_train')
    y_test = pycaret.regression.get_config('y_test')
    assert isinstance(X_train, pd.core.frame.DataFrame)
    assert isinstance(X_test, pd.core.frame.DataFrame)
    assert isinstance(y_train, pd.core.series.Series)
    assert isinstance(y_test, pd.core.series.Series)

    # set config
    pycaret.classification.set_config('seed', 124)
    seed = pycaret.classification.get_config('seed')
    assert seed == 124

    assert 1 == 1
    
if __name__ == "__main__":
    test()
