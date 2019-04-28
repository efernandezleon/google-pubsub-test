# Example project to test Websockets with Google Cloud Pub/Sub

This is a PoC of how to use Python 3+, AIOHTTP and Google Cloud Pub/Sub to forward messages from a subscription to a web client by using websockets. 

### Prerequisites

First of all, obviously you should have a Google Cloud account and a configured project with Pub/Sub enabled in order to make some tests. The following links will help you to create the topic, subtopic and get the credentials in json format:

- Pub/Sub website: https://cloud.google.com/pubsub/
- Create a topic and a subscription: https://cloud.google.com/pubsub/docs/admin
- How to get credentials in json format for service account: https://cloud.google.com/iam/docs/creating-managing-service-account-keys

In addition, you should export the following environment variables:

```bash
$ export GOOGLE_CLOUD_PROJECT=your_gcloud_project
$ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
$ export GOOGLE_CLOUD_PUBSUB_TOPIC=your_topic_name
$ export GOOGLE_CLOUD_PUBSUB_SUBSCRIPTION=your_subscription_name
```
### Installing

In order to set up the environment you should have installed Python 3.7 and create a virtual env. To do that, run the following commands in your terminal:

```bash
$ mkdir venv
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Running the server

To run the server just execute the following command (remember export the previous env variables):

```bash
$ python app.py venv
```

Once the server is running you can use your browser pointing at http://localhost:8080/index.html to see a very simple web page showing the last message in the topic and the incoming messages in real time.

## Send a message to the topic

To see how a new message goes to the Pub/Sub and the webpage changes by using websockets, you can use the next helper command:

```bash
$ python pub.py my-new-message
```

## Built With

* [AIOHTTP](https://aiohttp.readthedocs.io/en/stable/) - Async REST server with WebSockets support
* [VueJs](https://vuejs.org/) + [Axious](https://vuejs.org/v2/cookbook/using-axios-to-consume-apis.html)- Javascript framework
* [Google Cloud Pub/Sub](https://cloud.google.com/pubsub/) - Message Queue from Google