from faststream.nats import NatsRouter

router = NatsRouter()


@router.subscriber("scan-input")
@router.publisher("scan-output")
async def handle_scan(body):
    print(body)
    return body
