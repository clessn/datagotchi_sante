from sklearn.metrics import mean_squared_error


# MSE
def MSE(y_true, y_pred):
    MSE = mean_squared_error(y_true, y_pred)
    return MSE


y_true = [1, 0, 0, 1]
y_pred = [1, 0, 1, 0]
print(MSE(y_true, y_pred))
