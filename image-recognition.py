# from GH user eldor4do at https://github.com/eldor4do/Tensorflow-Examples/blob/master/retraining-example.py , with some modifications
import sys
import getopt
import numpy as np
import tensorflow as tf

imagePath = 'meme.jpg'
modelFullPath = '/tmp/output_graph.pb'
labelsFullPath = '/tmp/output_labels.txt'

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:h', ['image=', 'help'])
except getopt.GetoptError:
    print "Uh oh, something went wrong. Try again, and read the docs! Use image-recognition.py -h if you need help."
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print "Help docs coming soon!"
        sys.exit(2)
    elif opt in ('-i', '--image'):
        imagePath = arg
    else:
        print "Uh oh, something went wrong. Try again, and read the docs! Use image-recognition.py -h if you need help."
        sys.exit(2)


def create_graph():
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image():
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph()

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        answer = labels[top_k[0]]
        return answer


if __name__ == '__main__':
    run_inference_on_image()
