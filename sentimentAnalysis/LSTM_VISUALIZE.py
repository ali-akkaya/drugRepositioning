# Visualize history
import matplotlib.pyplot as plt

def plot_history(key):
  t_dict = {'Loss': 'loss', 'Accuracy': 'acc'}
  v_dict = {'Loss': 'val_loss', 'Accuracy': 'val_acc'}
  plt.title(f'{key} history')
  plt.plot(history.history[t_dict[key]], "-b", label="train")
  plt.plot(history.history[v_dict[key]], "--ro", label="valid")
  plt.legend(loc="upper left")
  plt.ylabel(f'{key}')
  plt.xlabel('Steps')
  plt.show()

# Plot history: Loss
plot_history('Loss')

# Plot history: Accuracy
plot_history('Accuracy')