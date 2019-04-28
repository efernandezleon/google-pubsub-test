import os
import sys
from google.cloud import pubsub_v1

publisher = pubsub_v1.PublisherClient()
topic_name = 'projects/{project_id}/topics/{topic}'.format(
    project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
    topic='test'
)
message = sys.argv[1] if 1 < len(sys.argv) else 'default message'
publisher.publish(topic_name, str.encode(message), spam='eggs')
