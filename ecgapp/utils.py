from .database_download import *
from io import BytesIO
import base64
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph







def get_plot(abs_path):
    value = get_values(abs_path)
    # print(value)
    plt.clf()
  
    
    plt.figure(1, figsize=(8.65, 2.35), dpi=100)

    plt.plot(value[0])
    plt.grid()
  

    graph = get_graph
    return graph


